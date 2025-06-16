r'''
# `google_network_security_security_profile`

Refer to the Terraform Registry for docs: [`google_network_security_security_profile`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile).
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


class GoogleNetworkSecuritySecurityProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile google_network_security_security_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        custom_intercept_profile: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileCustomInterceptProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_mirroring_profile: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileCustomMirroringProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        threat_prevention_profile: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile google_network_security_security_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the security profile resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#name GoogleNetworkSecuritySecurityProfile#name}
        :param type: The type of security profile. Possible values: ["THREAT_PREVENTION", "CUSTOM_MIRRORING", "CUSTOM_INTERCEPT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#type GoogleNetworkSecuritySecurityProfile#type}
        :param custom_intercept_profile: custom_intercept_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#custom_intercept_profile GoogleNetworkSecuritySecurityProfile#custom_intercept_profile}
        :param custom_mirroring_profile: custom_mirroring_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#custom_mirroring_profile GoogleNetworkSecuritySecurityProfile#custom_mirroring_profile}
        :param description: An optional description of the security profile. The Max length is 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#description GoogleNetworkSecuritySecurityProfile#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#id GoogleNetworkSecuritySecurityProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A map of key/value label pairs to assign to the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#labels GoogleNetworkSecuritySecurityProfile#labels}
        :param location: The location of the security profile. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#location GoogleNetworkSecuritySecurityProfile#location}
        :param parent: The name of the parent this security profile belongs to. Format: organizations/{organization_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#parent GoogleNetworkSecuritySecurityProfile#parent}
        :param threat_prevention_profile: threat_prevention_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_prevention_profile GoogleNetworkSecuritySecurityProfile#threat_prevention_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#timeouts GoogleNetworkSecuritySecurityProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4516d4e1c8f0dcd4af4e61a332a2c9baedb5cd659dd916eb14d3ba4e8c3d8a84)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkSecuritySecurityProfileConfig(
            name=name,
            type=type,
            custom_intercept_profile=custom_intercept_profile,
            custom_mirroring_profile=custom_mirroring_profile,
            description=description,
            id=id,
            labels=labels,
            location=location,
            parent=parent,
            threat_prevention_profile=threat_prevention_profile,
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
        '''Generates CDKTF code for importing a GoogleNetworkSecuritySecurityProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkSecuritySecurityProfile to import.
        :param import_from_id: The id of the existing GoogleNetworkSecuritySecurityProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkSecuritySecurityProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800525cad1762c3c930c3941d40af4ab10a3fbf2821fadce2173405bff4f4fa0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomInterceptProfile")
    def put_custom_intercept_profile(
        self,
        *,
        intercept_endpoint_group: builtins.str,
    ) -> None:
        '''
        :param intercept_endpoint_group: The Intercept Endpoint Group to which matching traffic should be intercepted. Format: projects/{project_id}/locations/global/interceptEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#intercept_endpoint_group GoogleNetworkSecuritySecurityProfile#intercept_endpoint_group}
        '''
        value = GoogleNetworkSecuritySecurityProfileCustomInterceptProfile(
            intercept_endpoint_group=intercept_endpoint_group
        )

        return typing.cast(None, jsii.invoke(self, "putCustomInterceptProfile", [value]))

    @jsii.member(jsii_name="putCustomMirroringProfile")
    def put_custom_mirroring_profile(
        self,
        *,
        mirroring_endpoint_group: builtins.str,
    ) -> None:
        '''
        :param mirroring_endpoint_group: The Mirroring Endpoint Group to which matching traffic should be mirrored. Format: projects/{project_id}/locations/global/mirroringEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#mirroring_endpoint_group GoogleNetworkSecuritySecurityProfile#mirroring_endpoint_group}
        '''
        value = GoogleNetworkSecuritySecurityProfileCustomMirroringProfile(
            mirroring_endpoint_group=mirroring_endpoint_group
        )

        return typing.cast(None, jsii.invoke(self, "putCustomMirroringProfile", [value]))

    @jsii.member(jsii_name="putThreatPreventionProfile")
    def put_threat_prevention_profile(
        self,
        *,
        antivirus_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        threat_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param antivirus_overrides: antivirus_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#antivirus_overrides GoogleNetworkSecuritySecurityProfile#antivirus_overrides}
        :param severity_overrides: severity_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#severity_overrides GoogleNetworkSecuritySecurityProfile#severity_overrides}
        :param threat_overrides: threat_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_overrides GoogleNetworkSecuritySecurityProfile#threat_overrides}
        '''
        value = GoogleNetworkSecuritySecurityProfileThreatPreventionProfile(
            antivirus_overrides=antivirus_overrides,
            severity_overrides=severity_overrides,
            threat_overrides=threat_overrides,
        )

        return typing.cast(None, jsii.invoke(self, "putThreatPreventionProfile", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#create GoogleNetworkSecuritySecurityProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#delete GoogleNetworkSecuritySecurityProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#update GoogleNetworkSecuritySecurityProfile#update}.
        '''
        value = GoogleNetworkSecuritySecurityProfileTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomInterceptProfile")
    def reset_custom_intercept_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomInterceptProfile", []))

    @jsii.member(jsii_name="resetCustomMirroringProfile")
    def reset_custom_mirroring_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMirroringProfile", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

    @jsii.member(jsii_name="resetThreatPreventionProfile")
    def reset_threat_prevention_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatPreventionProfile", []))

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
    @jsii.member(jsii_name="customInterceptProfile")
    def custom_intercept_profile(
        self,
    ) -> "GoogleNetworkSecuritySecurityProfileCustomInterceptProfileOutputReference":
        return typing.cast("GoogleNetworkSecuritySecurityProfileCustomInterceptProfileOutputReference", jsii.get(self, "customInterceptProfile"))

    @builtins.property
    @jsii.member(jsii_name="customMirroringProfile")
    def custom_mirroring_profile(
        self,
    ) -> "GoogleNetworkSecuritySecurityProfileCustomMirroringProfileOutputReference":
        return typing.cast("GoogleNetworkSecuritySecurityProfileCustomMirroringProfileOutputReference", jsii.get(self, "customMirroringProfile"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="threatPreventionProfile")
    def threat_prevention_profile(
        self,
    ) -> "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileOutputReference":
        return typing.cast("GoogleNetworkSecuritySecurityProfileThreatPreventionProfileOutputReference", jsii.get(self, "threatPreventionProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkSecuritySecurityProfileTimeoutsOutputReference":
        return typing.cast("GoogleNetworkSecuritySecurityProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="customInterceptProfileInput")
    def custom_intercept_profile_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileCustomInterceptProfile"]:
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileCustomInterceptProfile"], jsii.get(self, "customInterceptProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="customMirroringProfileInput")
    def custom_mirroring_profile_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileCustomMirroringProfile"]:
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileCustomMirroringProfile"], jsii.get(self, "customMirroringProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="threatPreventionProfileInput")
    def threat_prevention_profile_input(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileThreatPreventionProfile"]:
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileThreatPreventionProfile"], jsii.get(self, "threatPreventionProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecuritySecurityProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkSecuritySecurityProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b4a3a942f730506bfec0035b5a980fa185d4a9605982faa4e7a97c8ab8f5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a8efa7770178a6c932dc7cb96052051200f15ea892b78f88cc40ef31acd611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c047044447c427a68e957ea1f9f7b4981ac894ba30a6139555b905b0f1b4973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a7fa1a1d732ecd57fa09a03d8ca54a3ca3df5306412794e32f64f4635c07ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b5adfa3f70d13bbd953a976d0517572dc18367dc79de17ca59f46d746c0bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b976573d51fa1e4d5bbc0900edfd6020bdf806834bdfb3c725fd9d01e0bc56b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228ee92e61f76a233b8c7e580ae539cf97f1fb4b979284074ec7cc9dc2a5abd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileConfig",
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
        "type": "type",
        "custom_intercept_profile": "customInterceptProfile",
        "custom_mirroring_profile": "customMirroringProfile",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "parent": "parent",
        "threat_prevention_profile": "threatPreventionProfile",
        "timeouts": "timeouts",
    },
)
class GoogleNetworkSecuritySecurityProfileConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        type: builtins.str,
        custom_intercept_profile: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileCustomInterceptProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_mirroring_profile: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileCustomMirroringProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        threat_prevention_profile: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkSecuritySecurityProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the security profile resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#name GoogleNetworkSecuritySecurityProfile#name}
        :param type: The type of security profile. Possible values: ["THREAT_PREVENTION", "CUSTOM_MIRRORING", "CUSTOM_INTERCEPT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#type GoogleNetworkSecuritySecurityProfile#type}
        :param custom_intercept_profile: custom_intercept_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#custom_intercept_profile GoogleNetworkSecuritySecurityProfile#custom_intercept_profile}
        :param custom_mirroring_profile: custom_mirroring_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#custom_mirroring_profile GoogleNetworkSecuritySecurityProfile#custom_mirroring_profile}
        :param description: An optional description of the security profile. The Max length is 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#description GoogleNetworkSecuritySecurityProfile#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#id GoogleNetworkSecuritySecurityProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A map of key/value label pairs to assign to the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#labels GoogleNetworkSecuritySecurityProfile#labels}
        :param location: The location of the security profile. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#location GoogleNetworkSecuritySecurityProfile#location}
        :param parent: The name of the parent this security profile belongs to. Format: organizations/{organization_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#parent GoogleNetworkSecuritySecurityProfile#parent}
        :param threat_prevention_profile: threat_prevention_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_prevention_profile GoogleNetworkSecuritySecurityProfile#threat_prevention_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#timeouts GoogleNetworkSecuritySecurityProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_intercept_profile, dict):
            custom_intercept_profile = GoogleNetworkSecuritySecurityProfileCustomInterceptProfile(**custom_intercept_profile)
        if isinstance(custom_mirroring_profile, dict):
            custom_mirroring_profile = GoogleNetworkSecuritySecurityProfileCustomMirroringProfile(**custom_mirroring_profile)
        if isinstance(threat_prevention_profile, dict):
            threat_prevention_profile = GoogleNetworkSecuritySecurityProfileThreatPreventionProfile(**threat_prevention_profile)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkSecuritySecurityProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3467576ca61aaa2eab0e2d0e90b9771db2e6f207d8b3e93cb87991ebb38e7b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument custom_intercept_profile", value=custom_intercept_profile, expected_type=type_hints["custom_intercept_profile"])
            check_type(argname="argument custom_mirroring_profile", value=custom_mirroring_profile, expected_type=type_hints["custom_mirroring_profile"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument threat_prevention_profile", value=threat_prevention_profile, expected_type=type_hints["threat_prevention_profile"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
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
        if custom_intercept_profile is not None:
            self._values["custom_intercept_profile"] = custom_intercept_profile
        if custom_mirroring_profile is not None:
            self._values["custom_mirroring_profile"] = custom_mirroring_profile
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if parent is not None:
            self._values["parent"] = parent
        if threat_prevention_profile is not None:
            self._values["threat_prevention_profile"] = threat_prevention_profile
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
    def name(self) -> builtins.str:
        '''The name of the security profile resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#name GoogleNetworkSecuritySecurityProfile#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of security profile. Possible values: ["THREAT_PREVENTION", "CUSTOM_MIRRORING", "CUSTOM_INTERCEPT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#type GoogleNetworkSecuritySecurityProfile#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_intercept_profile(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileCustomInterceptProfile"]:
        '''custom_intercept_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#custom_intercept_profile GoogleNetworkSecuritySecurityProfile#custom_intercept_profile}
        '''
        result = self._values.get("custom_intercept_profile")
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileCustomInterceptProfile"], result)

    @builtins.property
    def custom_mirroring_profile(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileCustomMirroringProfile"]:
        '''custom_mirroring_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#custom_mirroring_profile GoogleNetworkSecuritySecurityProfile#custom_mirroring_profile}
        '''
        result = self._values.get("custom_mirroring_profile")
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileCustomMirroringProfile"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the security profile. The Max length is 512 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#description GoogleNetworkSecuritySecurityProfile#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#id GoogleNetworkSecuritySecurityProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key/value label pairs to assign to the resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#labels GoogleNetworkSecuritySecurityProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the security profile. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#location GoogleNetworkSecuritySecurityProfile#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The name of the parent this security profile belongs to. Format: organizations/{organization_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#parent GoogleNetworkSecuritySecurityProfile#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threat_prevention_profile(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileThreatPreventionProfile"]:
        '''threat_prevention_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_prevention_profile GoogleNetworkSecuritySecurityProfile#threat_prevention_profile}
        '''
        result = self._values.get("threat_prevention_profile")
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileThreatPreventionProfile"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkSecuritySecurityProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#timeouts GoogleNetworkSecuritySecurityProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkSecuritySecurityProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileCustomInterceptProfile",
    jsii_struct_bases=[],
    name_mapping={"intercept_endpoint_group": "interceptEndpointGroup"},
)
class GoogleNetworkSecuritySecurityProfileCustomInterceptProfile:
    def __init__(self, *, intercept_endpoint_group: builtins.str) -> None:
        '''
        :param intercept_endpoint_group: The Intercept Endpoint Group to which matching traffic should be intercepted. Format: projects/{project_id}/locations/global/interceptEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#intercept_endpoint_group GoogleNetworkSecuritySecurityProfile#intercept_endpoint_group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95d793d1a356421711e1b15545171b46b6b2f9e45768c565f6ad3ff66596265)
            check_type(argname="argument intercept_endpoint_group", value=intercept_endpoint_group, expected_type=type_hints["intercept_endpoint_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intercept_endpoint_group": intercept_endpoint_group,
        }

    @builtins.property
    def intercept_endpoint_group(self) -> builtins.str:
        '''The Intercept Endpoint Group to which matching traffic should be intercepted. Format: projects/{project_id}/locations/global/interceptEndpointGroups/{endpoint_group_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#intercept_endpoint_group GoogleNetworkSecuritySecurityProfile#intercept_endpoint_group}
        '''
        result = self._values.get("intercept_endpoint_group")
        assert result is not None, "Required property 'intercept_endpoint_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileCustomInterceptProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecuritySecurityProfileCustomInterceptProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileCustomInterceptProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75bddbd31451da45bbba630fe3fb7c5767ce8e946adcabffade55c48155e93b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="interceptEndpointGroupInput")
    def intercept_endpoint_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interceptEndpointGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="interceptEndpointGroup")
    def intercept_endpoint_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interceptEndpointGroup"))

    @intercept_endpoint_group.setter
    def intercept_endpoint_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a861e823870bbac536b667a55cdb7c046b5a93039df11dbe12dad94ee36c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interceptEndpointGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecuritySecurityProfileCustomInterceptProfile]:
        return typing.cast(typing.Optional[GoogleNetworkSecuritySecurityProfileCustomInterceptProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecuritySecurityProfileCustomInterceptProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e9fec3b128d96088ffa0cc5b2206d582e136cb073f649386eed8fc0b121249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileCustomMirroringProfile",
    jsii_struct_bases=[],
    name_mapping={"mirroring_endpoint_group": "mirroringEndpointGroup"},
)
class GoogleNetworkSecuritySecurityProfileCustomMirroringProfile:
    def __init__(self, *, mirroring_endpoint_group: builtins.str) -> None:
        '''
        :param mirroring_endpoint_group: The Mirroring Endpoint Group to which matching traffic should be mirrored. Format: projects/{project_id}/locations/global/mirroringEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#mirroring_endpoint_group GoogleNetworkSecuritySecurityProfile#mirroring_endpoint_group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15166940fcbeba50bed98fa0566191195e03f49d073caef4609d9593be0d9f9a)
            check_type(argname="argument mirroring_endpoint_group", value=mirroring_endpoint_group, expected_type=type_hints["mirroring_endpoint_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mirroring_endpoint_group": mirroring_endpoint_group,
        }

    @builtins.property
    def mirroring_endpoint_group(self) -> builtins.str:
        '''The Mirroring Endpoint Group to which matching traffic should be mirrored. Format: projects/{project_id}/locations/global/mirroringEndpointGroups/{endpoint_group_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#mirroring_endpoint_group GoogleNetworkSecuritySecurityProfile#mirroring_endpoint_group}
        '''
        result = self._values.get("mirroring_endpoint_group")
        assert result is not None, "Required property 'mirroring_endpoint_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileCustomMirroringProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecuritySecurityProfileCustomMirroringProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileCustomMirroringProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d78a20222531e896ee4854fc114e5d2772d53d87376b407a0cf17753d104c0fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="mirroringEndpointGroupInput")
    def mirroring_endpoint_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mirroringEndpointGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="mirroringEndpointGroup")
    def mirroring_endpoint_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mirroringEndpointGroup"))

    @mirroring_endpoint_group.setter
    def mirroring_endpoint_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264a954b1ae8055025ad44eeb9b5e257afc7767c8eb47d88d094898184fa6379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirroringEndpointGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecuritySecurityProfileCustomMirroringProfile]:
        return typing.cast(typing.Optional[GoogleNetworkSecuritySecurityProfileCustomMirroringProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecuritySecurityProfileCustomMirroringProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7421a30cf79032cd2285fccbc6a9969b79059ed15ed3228ed5ff8dd5245e60dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfile",
    jsii_struct_bases=[],
    name_mapping={
        "antivirus_overrides": "antivirusOverrides",
        "severity_overrides": "severityOverrides",
        "threat_overrides": "threatOverrides",
    },
)
class GoogleNetworkSecuritySecurityProfileThreatPreventionProfile:
    def __init__(
        self,
        *,
        antivirus_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        threat_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param antivirus_overrides: antivirus_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#antivirus_overrides GoogleNetworkSecuritySecurityProfile#antivirus_overrides}
        :param severity_overrides: severity_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#severity_overrides GoogleNetworkSecuritySecurityProfile#severity_overrides}
        :param threat_overrides: threat_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_overrides GoogleNetworkSecuritySecurityProfile#threat_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138804c6375988b82fa44be814657d1ce23aa9e3e9d55d7cd2f0f9e59ffe1e28)
            check_type(argname="argument antivirus_overrides", value=antivirus_overrides, expected_type=type_hints["antivirus_overrides"])
            check_type(argname="argument severity_overrides", value=severity_overrides, expected_type=type_hints["severity_overrides"])
            check_type(argname="argument threat_overrides", value=threat_overrides, expected_type=type_hints["threat_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if antivirus_overrides is not None:
            self._values["antivirus_overrides"] = antivirus_overrides
        if severity_overrides is not None:
            self._values["severity_overrides"] = severity_overrides
        if threat_overrides is not None:
            self._values["threat_overrides"] = threat_overrides

    @builtins.property
    def antivirus_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides"]]]:
        '''antivirus_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#antivirus_overrides GoogleNetworkSecuritySecurityProfile#antivirus_overrides}
        '''
        result = self._values.get("antivirus_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides"]]], result)

    @builtins.property
    def severity_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]]:
        '''severity_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#severity_overrides GoogleNetworkSecuritySecurityProfile#severity_overrides}
        '''
        result = self._values.get("severity_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]], result)

    @builtins.property
    def threat_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]]:
        '''threat_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_overrides GoogleNetworkSecuritySecurityProfile#threat_overrides}
        '''
        result = self._values.get("threat_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileThreatPreventionProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "protocol": "protocol"},
)
class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides:
    def __init__(self, *, action: builtins.str, protocol: builtins.str) -> None:
        '''
        :param action: Threat action override. For some threat types, only a subset of actions applies. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#action GoogleNetworkSecuritySecurityProfile#action}
        :param protocol: Required protocol to match. Possible values: ["SMTP", "SMB", "POP3", "IMAP", "HTTP2", "HTTP", "FTP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#protocol GoogleNetworkSecuritySecurityProfile#protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944bec7e7616e6324978cfe309f06c6a4074789b011e940d1cb7f53fc17d451c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "protocol": protocol,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Threat action override. For some threat types, only a subset of actions applies. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#action GoogleNetworkSecuritySecurityProfile#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Required protocol to match. Possible values: ["SMTP", "SMB", "POP3", "IMAP", "HTTP2", "HTTP", "FTP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#protocol GoogleNetworkSecuritySecurityProfile#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c9681c03b6fdf77bd2df6f02c47c6e6c7f8c591ad635156a5330ac03c11ca8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b57fa4f0a8a0fd7e1e1fac0ab01783dd135e09582658f25fd44d36ec6672f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afdb6a2a128fe3426fac84f736403809369fc7089e4c42f027fffca03530d78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__004882705099acaaa5cd88eeaaf1c9cbe2ea30c1de347639c7c8442a039a1ee6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__302601ca1e74cd9cda78c1e79e9777f3f1a4b9fb8a4c9c2c0038378ab67bc498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f78e880f88042e3a531b91f22163bb2777cc050ded1f2bee18e06add34ffe8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f4bec04b10fdb113b9f58a1cd2775ec552ff763052830c69de806442ad25ec9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443e73d6cec19403a13b798e932f6831e80853f87542692839f442144c3a5b7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fa83057bb3b3ef21e782a3be557c8bc27da9c18f73af33fbc85626f53f1441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00670ad6a8a5acfd319bb774a3695d686f474be67c0184a23d8e327237b91605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaa83f8f414e7e3865b113fabdaf8fb97739c8223ec462f017ea295b26cf7214)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAntivirusOverrides")
    def put_antivirus_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76822944eeb46327485c2b20347ba067cec32bc3bfadfb91e4e10987f40c86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAntivirusOverrides", [value]))

    @jsii.member(jsii_name="putSeverityOverrides")
    def put_severity_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43f8a9e3f963d70493a934f811b01882cdc5b7f9f5f3bde963506442567cf68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeverityOverrides", [value]))

    @jsii.member(jsii_name="putThreatOverrides")
    def put_threat_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8b2fcd790f237f99583c2e69cad8c0ba22908a3042cb2db39c6cd3a0f88143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThreatOverrides", [value]))

    @jsii.member(jsii_name="resetAntivirusOverrides")
    def reset_antivirus_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntivirusOverrides", []))

    @jsii.member(jsii_name="resetSeverityOverrides")
    def reset_severity_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverityOverrides", []))

    @jsii.member(jsii_name="resetThreatOverrides")
    def reset_threat_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatOverrides", []))

    @builtins.property
    @jsii.member(jsii_name="antivirusOverrides")
    def antivirus_overrides(
        self,
    ) -> GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList:
        return typing.cast(GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList, jsii.get(self, "antivirusOverrides"))

    @builtins.property
    @jsii.member(jsii_name="severityOverrides")
    def severity_overrides(
        self,
    ) -> "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList":
        return typing.cast("GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList", jsii.get(self, "severityOverrides"))

    @builtins.property
    @jsii.member(jsii_name="threatOverrides")
    def threat_overrides(
        self,
    ) -> "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList":
        return typing.cast("GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList", jsii.get(self, "threatOverrides"))

    @builtins.property
    @jsii.member(jsii_name="antivirusOverridesInput")
    def antivirus_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]], jsii.get(self, "antivirusOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="severityOverridesInput")
    def severity_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]], jsii.get(self, "severityOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="threatOverridesInput")
    def threat_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]], jsii.get(self, "threatOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkSecuritySecurityProfileThreatPreventionProfile]:
        return typing.cast(typing.Optional[GoogleNetworkSecuritySecurityProfileThreatPreventionProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkSecuritySecurityProfileThreatPreventionProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a245ffdb082a727cb2dabdf89c84aa8b8039ea2dc707549510265fe66ad544f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "severity": "severity"},
)
class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides:
    def __init__(self, *, action: builtins.str, severity: builtins.str) -> None:
        '''
        :param action: Threat action override. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#action GoogleNetworkSecuritySecurityProfile#action}
        :param severity: Severity level to match. Possible values: ["CRITICAL", "HIGH", "INFORMATIONAL", "LOW", "MEDIUM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#severity GoogleNetworkSecuritySecurityProfile#severity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c458a1bf53eab8a7e1420bef64ed8838116bbc83adb1d5fa0d1687e78875f8f)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "severity": severity,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Threat action override. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#action GoogleNetworkSecuritySecurityProfile#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''Severity level to match. Possible values: ["CRITICAL", "HIGH", "INFORMATIONAL", "LOW", "MEDIUM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#severity GoogleNetworkSecuritySecurityProfile#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fde0e259f44bfc46f48f330b45d1807bfb1b73ec3bb8c02963f74b3ade9aa279)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc85fa6b62dcab748920b2eccbc0106d3f3834f00d8e29938adb715a4942beb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f20d11d9eb111175c3993d9e94022f7b8ab8384928fb2a8db72ced70c2a183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40e1e92007de3c11b74dc93dea2f9695b63e8602eacfd0436638e2b3d3e04b33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f260526bc396c5a04068824139ff59fc6b31ea117c484aec6a93f780098cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063bfb62c3a7010599667641b7c2b9081347c0cdf0f1797c1821a110d0dd960e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2101470734c999f72cdda68b0c3b5aa367687ffefe64184766ae7dbbdc59d2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29ed354d6161ab2d161e3f856d0d0941c00ce670e0b710669ea757a537e3a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8e84ca0ff64ac1cdfcd88c18c705e0260b9198483c99d4c97dd1866f25620d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc25c56b44fb12b855a2dc9c897b94ccda67bd3bee913ec913a7eab7acade23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "threat_id": "threatId"},
)
class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides:
    def __init__(self, *, action: builtins.str, threat_id: builtins.str) -> None:
        '''
        :param action: Threat action. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#action GoogleNetworkSecuritySecurityProfile#action}
        :param threat_id: Vendor-specific ID of a threat to override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_id GoogleNetworkSecuritySecurityProfile#threat_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb97bd7cdc4ec93179c12a43899685319d6be2a3dfac7892694935d2cbe5743)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument threat_id", value=threat_id, expected_type=type_hints["threat_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "threat_id": threat_id,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Threat action. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#action GoogleNetworkSecuritySecurityProfile#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threat_id(self) -> builtins.str:
        '''Vendor-specific ID of a threat to override.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#threat_id GoogleNetworkSecuritySecurityProfile#threat_id}
        '''
        result = self._values.get("threat_id")
        assert result is not None, "Required property 'threat_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e2d0c3b9d92c960418668a3aff0a988b2f14fb8aca0964c492d3d74ed697250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81e0a0201ac3867428edf6541f9df75c76d41abdcad834b07fbb02ac59402c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6351fedd1b0a0df238a239fe4798d1ee632929bd3670ac16e5e6160641ec9b1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae96930f900bc4503d52befd37316d662856413486dd799f731dc76767051c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab61fa8ff9ed6af9bea69f5e8536e2b69b0ae6175040c41512f28f669c5a0ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085d50eccd6aca7b4247d8789e4aa136bd2742650919c0ae05c1c5f70bd0cbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81c7dd2864c61fed50f279162a5ff6c909418abadc6f9f84c7cde6b6d636c388)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="threatIdInput")
    def threat_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "threatIdInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f5bb219247ad0a9d9fc84628fd2fb9c03f02a7ba2f3dfe5fbef8ea71dfdf4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threatId")
    def threat_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "threatId"))

    @threat_id.setter
    def threat_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c198b64dacc64dfa1b86529bab9d529289ae100252167fe44a9e671ffe690847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threatId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5581021ca6cc7b3b754a0194807bd659ec1beb2960151f5ca33074ca3081ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkSecuritySecurityProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#create GoogleNetworkSecuritySecurityProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#delete GoogleNetworkSecuritySecurityProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#update GoogleNetworkSecuritySecurityProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8702ce730d6524d41cd5b13513196b0b313dd568689bfa50f8c34a623d2044)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#create GoogleNetworkSecuritySecurityProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#delete GoogleNetworkSecuritySecurityProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_security_security_profile#update GoogleNetworkSecuritySecurityProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkSecuritySecurityProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkSecuritySecurityProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkSecuritySecurityProfile.GoogleNetworkSecuritySecurityProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff7c234cd89d080daf1c5ddf7a95a312da060b14d43d17ad372791b8008eb4bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94ddfd7f93ee541b76101c653dfb8e845cb612b736a9abff4c7b5f755a9b25fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34d5b4eda311544ddec41028c924d19c18e2e2038ff900c381dd262ec14aa98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd90c380f34ae318474ac6f32b0c1fb46d6da5bf71f1764f8ffd5d39b7aa64d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8b128e292ac7e93cc8b50335ecc1bf1daaba78c7d21b16fb97e2c691cae0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkSecuritySecurityProfile",
    "GoogleNetworkSecuritySecurityProfileConfig",
    "GoogleNetworkSecuritySecurityProfileCustomInterceptProfile",
    "GoogleNetworkSecuritySecurityProfileCustomInterceptProfileOutputReference",
    "GoogleNetworkSecuritySecurityProfileCustomMirroringProfile",
    "GoogleNetworkSecuritySecurityProfileCustomMirroringProfileOutputReference",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfile",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileOutputReference",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList",
    "GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference",
    "GoogleNetworkSecuritySecurityProfileTimeouts",
    "GoogleNetworkSecuritySecurityProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4516d4e1c8f0dcd4af4e61a332a2c9baedb5cd659dd916eb14d3ba4e8c3d8a84(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    custom_intercept_profile: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileCustomInterceptProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_mirroring_profile: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileCustomMirroringProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    threat_prevention_profile: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__800525cad1762c3c930c3941d40af4ab10a3fbf2821fadce2173405bff4f4fa0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b4a3a942f730506bfec0035b5a980fa185d4a9605982faa4e7a97c8ab8f5e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a8efa7770178a6c932dc7cb96052051200f15ea892b78f88cc40ef31acd611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c047044447c427a68e957ea1f9f7b4981ac894ba30a6139555b905b0f1b4973(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a7fa1a1d732ecd57fa09a03d8ca54a3ca3df5306412794e32f64f4635c07ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b5adfa3f70d13bbd953a976d0517572dc18367dc79de17ca59f46d746c0bae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b976573d51fa1e4d5bbc0900edfd6020bdf806834bdfb3c725fd9d01e0bc56b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228ee92e61f76a233b8c7e580ae539cf97f1fb4b979284074ec7cc9dc2a5abd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3467576ca61aaa2eab0e2d0e90b9771db2e6f207d8b3e93cb87991ebb38e7b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    custom_intercept_profile: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileCustomInterceptProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_mirroring_profile: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileCustomMirroringProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    threat_prevention_profile: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkSecuritySecurityProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95d793d1a356421711e1b15545171b46b6b2f9e45768c565f6ad3ff66596265(
    *,
    intercept_endpoint_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bddbd31451da45bbba630fe3fb7c5767ce8e946adcabffade55c48155e93b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a861e823870bbac536b667a55cdb7c046b5a93039df11dbe12dad94ee36c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e9fec3b128d96088ffa0cc5b2206d582e136cb073f649386eed8fc0b121249(
    value: typing.Optional[GoogleNetworkSecuritySecurityProfileCustomInterceptProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15166940fcbeba50bed98fa0566191195e03f49d073caef4609d9593be0d9f9a(
    *,
    mirroring_endpoint_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78a20222531e896ee4854fc114e5d2772d53d87376b407a0cf17753d104c0fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264a954b1ae8055025ad44eeb9b5e257afc7767c8eb47d88d094898184fa6379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7421a30cf79032cd2285fccbc6a9969b79059ed15ed3228ed5ff8dd5245e60dc(
    value: typing.Optional[GoogleNetworkSecuritySecurityProfileCustomMirroringProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138804c6375988b82fa44be814657d1ce23aa9e3e9d55d7cd2f0f9e59ffe1e28(
    *,
    antivirus_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    threat_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944bec7e7616e6324978cfe309f06c6a4074789b011e940d1cb7f53fc17d451c(
    *,
    action: builtins.str,
    protocol: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9681c03b6fdf77bd2df6f02c47c6e6c7f8c591ad635156a5330ac03c11ca8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b57fa4f0a8a0fd7e1e1fac0ab01783dd135e09582658f25fd44d36ec6672f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afdb6a2a128fe3426fac84f736403809369fc7089e4c42f027fffca03530d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004882705099acaaa5cd88eeaaf1c9cbe2ea30c1de347639c7c8442a039a1ee6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302601ca1e74cd9cda78c1e79e9777f3f1a4b9fb8a4c9c2c0038378ab67bc498(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f78e880f88042e3a531b91f22163bb2777cc050ded1f2bee18e06add34ffe8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4bec04b10fdb113b9f58a1cd2775ec552ff763052830c69de806442ad25ec9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443e73d6cec19403a13b798e932f6831e80853f87542692839f442144c3a5b7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fa83057bb3b3ef21e782a3be557c8bc27da9c18f73af33fbc85626f53f1441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00670ad6a8a5acfd319bb774a3695d686f474be67c0184a23d8e327237b91605(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa83f8f414e7e3865b113fabdaf8fb97739c8223ec462f017ea295b26cf7214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76822944eeb46327485c2b20347ba067cec32bc3bfadfb91e4e10987f40c86f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43f8a9e3f963d70493a934f811b01882cdc5b7f9f5f3bde963506442567cf68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8b2fcd790f237f99583c2e69cad8c0ba22908a3042cb2db39c6cd3a0f88143(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a245ffdb082a727cb2dabdf89c84aa8b8039ea2dc707549510265fe66ad544f(
    value: typing.Optional[GoogleNetworkSecuritySecurityProfileThreatPreventionProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c458a1bf53eab8a7e1420bef64ed8838116bbc83adb1d5fa0d1687e78875f8f(
    *,
    action: builtins.str,
    severity: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde0e259f44bfc46f48f330b45d1807bfb1b73ec3bb8c02963f74b3ade9aa279(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc85fa6b62dcab748920b2eccbc0106d3f3834f00d8e29938adb715a4942beb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f20d11d9eb111175c3993d9e94022f7b8ab8384928fb2a8db72ced70c2a183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e1e92007de3c11b74dc93dea2f9695b63e8602eacfd0436638e2b3d3e04b33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f260526bc396c5a04068824139ff59fc6b31ea117c484aec6a93f780098cda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063bfb62c3a7010599667641b7c2b9081347c0cdf0f1797c1821a110d0dd960e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2101470734c999f72cdda68b0c3b5aa367687ffefe64184766ae7dbbdc59d2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29ed354d6161ab2d161e3f856d0d0941c00ce670e0b710669ea757a537e3a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8e84ca0ff64ac1cdfcd88c18c705e0260b9198483c99d4c97dd1866f25620d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc25c56b44fb12b855a2dc9c897b94ccda67bd3bee913ec913a7eab7acade23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb97bd7cdc4ec93179c12a43899685319d6be2a3dfac7892694935d2cbe5743(
    *,
    action: builtins.str,
    threat_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2d0c3b9d92c960418668a3aff0a988b2f14fb8aca0964c492d3d74ed697250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81e0a0201ac3867428edf6541f9df75c76d41abdcad834b07fbb02ac59402c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6351fedd1b0a0df238a239fe4798d1ee632929bd3670ac16e5e6160641ec9b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae96930f900bc4503d52befd37316d662856413486dd799f731dc76767051c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab61fa8ff9ed6af9bea69f5e8536e2b69b0ae6175040c41512f28f669c5a0ca3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085d50eccd6aca7b4247d8789e4aa136bd2742650919c0ae05c1c5f70bd0cbee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c7dd2864c61fed50f279162a5ff6c909418abadc6f9f84c7cde6b6d636c388(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f5bb219247ad0a9d9fc84628fd2fb9c03f02a7ba2f3dfe5fbef8ea71dfdf4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c198b64dacc64dfa1b86529bab9d529289ae100252167fe44a9e671ffe690847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5581021ca6cc7b3b754a0194807bd659ec1beb2960151f5ca33074ca3081ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8702ce730d6524d41cd5b13513196b0b313dd568689bfa50f8c34a623d2044(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7c234cd89d080daf1c5ddf7a95a312da060b14d43d17ad372791b8008eb4bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ddfd7f93ee541b76101c653dfb8e845cb612b736a9abff4c7b5f755a9b25fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34d5b4eda311544ddec41028c924d19c18e2e2038ff900c381dd262ec14aa98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd90c380f34ae318474ac6f32b0c1fb46d6da5bf71f1764f8ffd5d39b7aa64d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8b128e292ac7e93cc8b50335ecc1bf1daaba78c7d21b16fb97e2c691cae0b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkSecuritySecurityProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
