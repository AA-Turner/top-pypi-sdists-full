r'''
# `google_network_security_security_profile`

Refer to the Terraform Registry for docs: [`google_network_security_security_profile`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile).
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


class NetworkSecuritySecurityProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile google_network_security_security_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        custom_intercept_profile: typing.Optional[typing.Union["NetworkSecuritySecurityProfileCustomInterceptProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_mirroring_profile: typing.Optional[typing.Union["NetworkSecuritySecurityProfileCustomMirroringProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        threat_prevention_profile: typing.Optional[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecuritySecurityProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile google_network_security_security_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the security profile resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#name NetworkSecuritySecurityProfile#name}
        :param type: The type of security profile. Possible values: ["THREAT_PREVENTION", "CUSTOM_MIRRORING", "CUSTOM_INTERCEPT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#type NetworkSecuritySecurityProfile#type}
        :param custom_intercept_profile: custom_intercept_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#custom_intercept_profile NetworkSecuritySecurityProfile#custom_intercept_profile}
        :param custom_mirroring_profile: custom_mirroring_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#custom_mirroring_profile NetworkSecuritySecurityProfile#custom_mirroring_profile}
        :param description: An optional description of the security profile. The Max length is 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#description NetworkSecuritySecurityProfile#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#id NetworkSecuritySecurityProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A map of key/value label pairs to assign to the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#labels NetworkSecuritySecurityProfile#labels}
        :param location: The location of the security profile. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#location NetworkSecuritySecurityProfile#location}
        :param parent: The name of the parent this security profile belongs to. Format: organizations/{organization_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#parent NetworkSecuritySecurityProfile#parent}
        :param threat_prevention_profile: threat_prevention_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_prevention_profile NetworkSecuritySecurityProfile#threat_prevention_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#timeouts NetworkSecuritySecurityProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41aa6d17897db920244db23671ce5b73d395fa293574cd5c9705b25aefe76677)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkSecuritySecurityProfileConfig(
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
        '''Generates CDKTF code for importing a NetworkSecuritySecurityProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkSecuritySecurityProfile to import.
        :param import_from_id: The id of the existing NetworkSecuritySecurityProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkSecuritySecurityProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5183cc2d774dbd9a60d1d9c6fd299060e4d9b19abf769a57bccd4b3e423ed8d)
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
        :param intercept_endpoint_group: The Intercept Endpoint Group to which matching traffic should be intercepted. Format: projects/{project_id}/locations/global/interceptEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#intercept_endpoint_group NetworkSecuritySecurityProfile#intercept_endpoint_group}
        '''
        value = NetworkSecuritySecurityProfileCustomInterceptProfile(
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
        :param mirroring_endpoint_group: The Mirroring Endpoint Group to which matching traffic should be mirrored. Format: projects/{project_id}/locations/global/mirroringEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#mirroring_endpoint_group NetworkSecuritySecurityProfile#mirroring_endpoint_group}
        '''
        value = NetworkSecuritySecurityProfileCustomMirroringProfile(
            mirroring_endpoint_group=mirroring_endpoint_group
        )

        return typing.cast(None, jsii.invoke(self, "putCustomMirroringProfile", [value]))

    @jsii.member(jsii_name="putThreatPreventionProfile")
    def put_threat_prevention_profile(
        self,
        *,
        antivirus_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        threat_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param antivirus_overrides: antivirus_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#antivirus_overrides NetworkSecuritySecurityProfile#antivirus_overrides}
        :param severity_overrides: severity_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#severity_overrides NetworkSecuritySecurityProfile#severity_overrides}
        :param threat_overrides: threat_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_overrides NetworkSecuritySecurityProfile#threat_overrides}
        '''
        value = NetworkSecuritySecurityProfileThreatPreventionProfile(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#create NetworkSecuritySecurityProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#delete NetworkSecuritySecurityProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#update NetworkSecuritySecurityProfile#update}.
        '''
        value = NetworkSecuritySecurityProfileTimeouts(
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
    ) -> "NetworkSecuritySecurityProfileCustomInterceptProfileOutputReference":
        return typing.cast("NetworkSecuritySecurityProfileCustomInterceptProfileOutputReference", jsii.get(self, "customInterceptProfile"))

    @builtins.property
    @jsii.member(jsii_name="customMirroringProfile")
    def custom_mirroring_profile(
        self,
    ) -> "NetworkSecuritySecurityProfileCustomMirroringProfileOutputReference":
        return typing.cast("NetworkSecuritySecurityProfileCustomMirroringProfileOutputReference", jsii.get(self, "customMirroringProfile"))

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
    ) -> "NetworkSecuritySecurityProfileThreatPreventionProfileOutputReference":
        return typing.cast("NetworkSecuritySecurityProfileThreatPreventionProfileOutputReference", jsii.get(self, "threatPreventionProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkSecuritySecurityProfileTimeoutsOutputReference":
        return typing.cast("NetworkSecuritySecurityProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="customInterceptProfileInput")
    def custom_intercept_profile_input(
        self,
    ) -> typing.Optional["NetworkSecuritySecurityProfileCustomInterceptProfile"]:
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileCustomInterceptProfile"], jsii.get(self, "customInterceptProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="customMirroringProfileInput")
    def custom_mirroring_profile_input(
        self,
    ) -> typing.Optional["NetworkSecuritySecurityProfileCustomMirroringProfile"]:
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileCustomMirroringProfile"], jsii.get(self, "customMirroringProfileInput"))

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
    ) -> typing.Optional["NetworkSecuritySecurityProfileThreatPreventionProfile"]:
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileThreatPreventionProfile"], jsii.get(self, "threatPreventionProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecuritySecurityProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecuritySecurityProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c9bc3d5524f1bcc1f01ec39c6b858452ef1d68b46c256dd472428f6ede0027f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbdd27e834bd2f5556c39c6e975d9be0356ed846748925415e9f8c0c2120bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce93e2d6e61a40124d975ef2114c4dad90d84b0e9ba36ac809b7cf7979f96560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5570a79d57302007da2cb34ba0be446879590677b04e0daf6565dcab53a2a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0be9e344e266ebada168302d946553f78285c80f8fa8807b4d18ad1e61403f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5081dde3929b7efdf8d689e72f5b950d0e96b0c1e0a442e842440fcb0413a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90fe052e1d456f23217519db0e700614849cf1c9df5133e8e0a8a3147e0c14d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileConfig",
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
class NetworkSecuritySecurityProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_intercept_profile: typing.Optional[typing.Union["NetworkSecuritySecurityProfileCustomInterceptProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_mirroring_profile: typing.Optional[typing.Union["NetworkSecuritySecurityProfileCustomMirroringProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        threat_prevention_profile: typing.Optional[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecuritySecurityProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the security profile resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#name NetworkSecuritySecurityProfile#name}
        :param type: The type of security profile. Possible values: ["THREAT_PREVENTION", "CUSTOM_MIRRORING", "CUSTOM_INTERCEPT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#type NetworkSecuritySecurityProfile#type}
        :param custom_intercept_profile: custom_intercept_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#custom_intercept_profile NetworkSecuritySecurityProfile#custom_intercept_profile}
        :param custom_mirroring_profile: custom_mirroring_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#custom_mirroring_profile NetworkSecuritySecurityProfile#custom_mirroring_profile}
        :param description: An optional description of the security profile. The Max length is 512 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#description NetworkSecuritySecurityProfile#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#id NetworkSecuritySecurityProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A map of key/value label pairs to assign to the resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#labels NetworkSecuritySecurityProfile#labels}
        :param location: The location of the security profile. The default value is 'global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#location NetworkSecuritySecurityProfile#location}
        :param parent: The name of the parent this security profile belongs to. Format: organizations/{organization_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#parent NetworkSecuritySecurityProfile#parent}
        :param threat_prevention_profile: threat_prevention_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_prevention_profile NetworkSecuritySecurityProfile#threat_prevention_profile}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#timeouts NetworkSecuritySecurityProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_intercept_profile, dict):
            custom_intercept_profile = NetworkSecuritySecurityProfileCustomInterceptProfile(**custom_intercept_profile)
        if isinstance(custom_mirroring_profile, dict):
            custom_mirroring_profile = NetworkSecuritySecurityProfileCustomMirroringProfile(**custom_mirroring_profile)
        if isinstance(threat_prevention_profile, dict):
            threat_prevention_profile = NetworkSecuritySecurityProfileThreatPreventionProfile(**threat_prevention_profile)
        if isinstance(timeouts, dict):
            timeouts = NetworkSecuritySecurityProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dd217e24fd8a66c7e070b522799df0acf14e4fea12bf4c8ac263c2779f6f44)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#name NetworkSecuritySecurityProfile#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of security profile. Possible values: ["THREAT_PREVENTION", "CUSTOM_MIRRORING", "CUSTOM_INTERCEPT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#type NetworkSecuritySecurityProfile#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_intercept_profile(
        self,
    ) -> typing.Optional["NetworkSecuritySecurityProfileCustomInterceptProfile"]:
        '''custom_intercept_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#custom_intercept_profile NetworkSecuritySecurityProfile#custom_intercept_profile}
        '''
        result = self._values.get("custom_intercept_profile")
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileCustomInterceptProfile"], result)

    @builtins.property
    def custom_mirroring_profile(
        self,
    ) -> typing.Optional["NetworkSecuritySecurityProfileCustomMirroringProfile"]:
        '''custom_mirroring_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#custom_mirroring_profile NetworkSecuritySecurityProfile#custom_mirroring_profile}
        '''
        result = self._values.get("custom_mirroring_profile")
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileCustomMirroringProfile"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the security profile. The Max length is 512 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#description NetworkSecuritySecurityProfile#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#id NetworkSecuritySecurityProfile#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#labels NetworkSecuritySecurityProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location of the security profile. The default value is 'global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#location NetworkSecuritySecurityProfile#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The name of the parent this security profile belongs to. Format: organizations/{organization_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#parent NetworkSecuritySecurityProfile#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threat_prevention_profile(
        self,
    ) -> typing.Optional["NetworkSecuritySecurityProfileThreatPreventionProfile"]:
        '''threat_prevention_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_prevention_profile NetworkSecuritySecurityProfile#threat_prevention_profile}
        '''
        result = self._values.get("threat_prevention_profile")
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileThreatPreventionProfile"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkSecuritySecurityProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#timeouts NetworkSecuritySecurityProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkSecuritySecurityProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileCustomInterceptProfile",
    jsii_struct_bases=[],
    name_mapping={"intercept_endpoint_group": "interceptEndpointGroup"},
)
class NetworkSecuritySecurityProfileCustomInterceptProfile:
    def __init__(self, *, intercept_endpoint_group: builtins.str) -> None:
        '''
        :param intercept_endpoint_group: The Intercept Endpoint Group to which matching traffic should be intercepted. Format: projects/{project_id}/locations/global/interceptEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#intercept_endpoint_group NetworkSecuritySecurityProfile#intercept_endpoint_group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed174bfa67b4a7a477f6638b599c563999cb6ba75967f99c33e610678856a12)
            check_type(argname="argument intercept_endpoint_group", value=intercept_endpoint_group, expected_type=type_hints["intercept_endpoint_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intercept_endpoint_group": intercept_endpoint_group,
        }

    @builtins.property
    def intercept_endpoint_group(self) -> builtins.str:
        '''The Intercept Endpoint Group to which matching traffic should be intercepted. Format: projects/{project_id}/locations/global/interceptEndpointGroups/{endpoint_group_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#intercept_endpoint_group NetworkSecuritySecurityProfile#intercept_endpoint_group}
        '''
        result = self._values.get("intercept_endpoint_group")
        assert result is not None, "Required property 'intercept_endpoint_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileCustomInterceptProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecuritySecurityProfileCustomInterceptProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileCustomInterceptProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2840485debd0c19ec2bcd9fd2269b2c0df07aa7b5f68114dc1041b69bd338ef0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d55c0ffe45329e3c7b98f05798580fca0564f74147e1eeb7a9d30aade40cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interceptEndpointGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecuritySecurityProfileCustomInterceptProfile]:
        return typing.cast(typing.Optional[NetworkSecuritySecurityProfileCustomInterceptProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecuritySecurityProfileCustomInterceptProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d39030921ce6ed6c7d7b524d36432737a9916365dc9c464ca1e577ff85f4e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileCustomMirroringProfile",
    jsii_struct_bases=[],
    name_mapping={"mirroring_endpoint_group": "mirroringEndpointGroup"},
)
class NetworkSecuritySecurityProfileCustomMirroringProfile:
    def __init__(self, *, mirroring_endpoint_group: builtins.str) -> None:
        '''
        :param mirroring_endpoint_group: The Mirroring Endpoint Group to which matching traffic should be mirrored. Format: projects/{project_id}/locations/global/mirroringEndpointGroups/{endpoint_group_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#mirroring_endpoint_group NetworkSecuritySecurityProfile#mirroring_endpoint_group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821490a64f85430afaa9f60754db501c0ee88f4e3e6b30f06ebe672948a9dc40)
            check_type(argname="argument mirroring_endpoint_group", value=mirroring_endpoint_group, expected_type=type_hints["mirroring_endpoint_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mirroring_endpoint_group": mirroring_endpoint_group,
        }

    @builtins.property
    def mirroring_endpoint_group(self) -> builtins.str:
        '''The Mirroring Endpoint Group to which matching traffic should be mirrored. Format: projects/{project_id}/locations/global/mirroringEndpointGroups/{endpoint_group_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#mirroring_endpoint_group NetworkSecuritySecurityProfile#mirroring_endpoint_group}
        '''
        result = self._values.get("mirroring_endpoint_group")
        assert result is not None, "Required property 'mirroring_endpoint_group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileCustomMirroringProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecuritySecurityProfileCustomMirroringProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileCustomMirroringProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a78fc52d9d265aa620ec6e9b196e1cb106cb1971eeeefeaafa5365234c68b3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98bd99ab52c862c86778a60393c1a7c5bcd058cccbc210dc27e2202999cf1040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirroringEndpointGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecuritySecurityProfileCustomMirroringProfile]:
        return typing.cast(typing.Optional[NetworkSecuritySecurityProfileCustomMirroringProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecuritySecurityProfileCustomMirroringProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c927cd3580e677e06e783b1d74d18fd7e50c3a1e8397b7054a30a7298e1cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfile",
    jsii_struct_bases=[],
    name_mapping={
        "antivirus_overrides": "antivirusOverrides",
        "severity_overrides": "severityOverrides",
        "threat_overrides": "threatOverrides",
    },
)
class NetworkSecuritySecurityProfileThreatPreventionProfile:
    def __init__(
        self,
        *,
        antivirus_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        threat_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param antivirus_overrides: antivirus_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#antivirus_overrides NetworkSecuritySecurityProfile#antivirus_overrides}
        :param severity_overrides: severity_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#severity_overrides NetworkSecuritySecurityProfile#severity_overrides}
        :param threat_overrides: threat_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_overrides NetworkSecuritySecurityProfile#threat_overrides}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7eb2885fdc25ba69359652464040dc45bfea3ea6b43f17afe638dd2f132a70)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides"]]]:
        '''antivirus_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#antivirus_overrides NetworkSecuritySecurityProfile#antivirus_overrides}
        '''
        result = self._values.get("antivirus_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides"]]], result)

    @builtins.property
    def severity_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]]:
        '''severity_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#severity_overrides NetworkSecuritySecurityProfile#severity_overrides}
        '''
        result = self._values.get("severity_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]], result)

    @builtins.property
    def threat_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]]:
        '''threat_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_overrides NetworkSecuritySecurityProfile#threat_overrides}
        '''
        result = self._values.get("threat_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileThreatPreventionProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "protocol": "protocol"},
)
class NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides:
    def __init__(self, *, action: builtins.str, protocol: builtins.str) -> None:
        '''
        :param action: Threat action override. For some threat types, only a subset of actions applies. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#action NetworkSecuritySecurityProfile#action}
        :param protocol: Required protocol to match. Possible values: ["SMTP", "SMB", "POP3", "IMAP", "HTTP2", "HTTP", "FTP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#protocol NetworkSecuritySecurityProfile#protocol}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32f85e74e127a20c0e3704fa5f942cf24d10f0f2eef11b42ac1c3ff6c6b38ee)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "protocol": protocol,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Threat action override. For some threat types, only a subset of actions applies. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#action NetworkSecuritySecurityProfile#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Required protocol to match. Possible values: ["SMTP", "SMB", "POP3", "IMAP", "HTTP2", "HTTP", "FTP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#protocol NetworkSecuritySecurityProfile#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad192ccea8736bf1f09b55e1a5c252a32d1cadd93636d2e28a1f20adf70ec266)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0acc223323af52224418f6892c9597bd154b111bf18eacadb82a5ddce088a17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cd27fa96d5f8cf396b1670e0bbbae1c1c574088b5cdbc54784ab07c803d5ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82aec1e594ccae930bbc835b60c82fd1b65141e06ad8fa13e0effa5583ce2c6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__037523632e66de2bd6a61f74baff5609a2b22578fab3ad61b1e2d4768aa00d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d1631c73483aaeffe68be9cadb8b2018e3da4b1bcd4ef99a8c5e2d0cd9884f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d9665c445ed29ceb9a7734c7e8a09d83e3beb1e12da9841d220d39614eb323f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30a0cc417ab4fb8e06f49e60319c8161f045d51f0a0f63ac7971d2191a96fe83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e675a24b43b96c852dea04a16c43aa908e1754339f952097330060f94d5b3377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92d20973cd2259d7c796d35f82fca865f74c164d2a1f2cd61ec8d36117a0d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecuritySecurityProfileThreatPreventionProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe6b77348e8dc8eea569b39ff9df968205e117555d2db2994254f7e822149728)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAntivirusOverrides")
    def put_antivirus_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02a2feb5422c42559d2ceea01319c06c1982d66b7a2873a07d6a06807853f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAntivirusOverrides", [value]))

    @jsii.member(jsii_name="putSeverityOverrides")
    def put_severity_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a70420eda58659a0c6310a90c6ebcb5c066429e1191d93e67f02911c4387b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeverityOverrides", [value]))

    @jsii.member(jsii_name="putThreatOverrides")
    def put_threat_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e641560e1bf316da743470db9f7b5c19aead5de438d414ac180f79c6390baba)
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
    ) -> NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList:
        return typing.cast(NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList, jsii.get(self, "antivirusOverrides"))

    @builtins.property
    @jsii.member(jsii_name="severityOverrides")
    def severity_overrides(
        self,
    ) -> "NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList":
        return typing.cast("NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList", jsii.get(self, "severityOverrides"))

    @builtins.property
    @jsii.member(jsii_name="threatOverrides")
    def threat_overrides(
        self,
    ) -> "NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList":
        return typing.cast("NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList", jsii.get(self, "threatOverrides"))

    @builtins.property
    @jsii.member(jsii_name="antivirusOverridesInput")
    def antivirus_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]], jsii.get(self, "antivirusOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="severityOverridesInput")
    def severity_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides"]]], jsii.get(self, "severityOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="threatOverridesInput")
    def threat_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides"]]], jsii.get(self, "threatOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecuritySecurityProfileThreatPreventionProfile]:
        return typing.cast(typing.Optional[NetworkSecuritySecurityProfileThreatPreventionProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecuritySecurityProfileThreatPreventionProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39da4493f83f38a0cff000c1be1eb3799f3cd0408a05ddca8fe946c3c119135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "severity": "severity"},
)
class NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides:
    def __init__(self, *, action: builtins.str, severity: builtins.str) -> None:
        '''
        :param action: Threat action override. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#action NetworkSecuritySecurityProfile#action}
        :param severity: Severity level to match. Possible values: ["CRITICAL", "HIGH", "INFORMATIONAL", "LOW", "MEDIUM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#severity NetworkSecuritySecurityProfile#severity}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__302a81a4e9d1413762fc07cbafe7852b61d05c74a07049f991e127cfd347534e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "severity": severity,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Threat action override. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#action NetworkSecuritySecurityProfile#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''Severity level to match. Possible values: ["CRITICAL", "HIGH", "INFORMATIONAL", "LOW", "MEDIUM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#severity NetworkSecuritySecurityProfile#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c1d5caed285fbce9c574eb44debe3f9768ca1a2a798a15204b3412a3b35b44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539f9274e931b8bd061f98f7f0e5bbc39e94b3e9913e413e9ef85bdf3871aaa0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79175ae58a6d3bb2bb887863be208ae8b2448579a2b7df2b58e0112554721747)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b0523a2608f54e6b5132498c770b8636bb241e66095265b61303bf98d2bb420)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aad0e91c5c219019418b95b9ceeb6e077b380acefc25b27a0de273865a7a3e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf0f210393e75f57fff1cebf0adff389364f005df2b55a0b3c64143350c1117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b33279719ecb84cc36a83f4138faf4b48b4fb4676c1ed55a2b825916cec02680)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b89eb0b454ae9b71eb6fbc413b6250f130ec0d822788f8df991ce6d084186684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71b69806be8473dd4ca2878837d6975d4d30797cc297e39bb6ea9522f882222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77e26362b5810a7b18ae3f3d47806f515129c5a75422322a1735c52160413c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "threat_id": "threatId"},
)
class NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides:
    def __init__(self, *, action: builtins.str, threat_id: builtins.str) -> None:
        '''
        :param action: Threat action. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#action NetworkSecuritySecurityProfile#action}
        :param threat_id: Vendor-specific ID of a threat to override. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_id NetworkSecuritySecurityProfile#threat_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6719af79071806ecf4631a26df1498cec79d0003b6d268e1f0c88f2b7b3fa2)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument threat_id", value=threat_id, expected_type=type_hints["threat_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "threat_id": threat_id,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Threat action. Possible values: ["ALERT", "ALLOW", "DEFAULT_ACTION", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#action NetworkSecuritySecurityProfile#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threat_id(self) -> builtins.str:
        '''Vendor-specific ID of a threat to override.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#threat_id NetworkSecuritySecurityProfile#threat_id}
        '''
        result = self._values.get("threat_id")
        assert result is not None, "Required property 'threat_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__839e44a099017a2aefd439aff5421309a25b28c5f5850ed2864a6afb198ad5d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a792efa36cbf66cd55c41659c2abad5e17a55299c15363eaa7e7051b1f47c834)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ad9ec7cae2dbe4e1b19aabac09c64694b166c80fa440fe3e45e44f2b7f0022)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2dc460c984043183799f5b419085a2f57c5e24a41b74ff6d11b42deb8dc2888)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f66115c5219ccf419f4ca8ee9922afdf00c4f760970c1371da791c7a4c13848f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b665ccb4b6a6c1b135d3c355a81c2ff77e5d4f33700c2885521f2dd86bc3b670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e53995a5cca9e00a4bad6eb7119dccacc9e2bc18498c88a1e492453c1d58cf2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c376e11193b3f9a88822b11dc69970a721a5c09ace1bdf2ab186904a194656e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threatId")
    def threat_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "threatId"))

    @threat_id.setter
    def threat_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe8a84daa69fcd132bc647dc8ada2d8c703dbc3670d586e48b2064795ee74db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threatId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6b112460cdfb12ff530deaadbe709d42832aeee0150efa65ddf858bc2a55fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkSecuritySecurityProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#create NetworkSecuritySecurityProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#delete NetworkSecuritySecurityProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#update NetworkSecuritySecurityProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b072d70af9288aee59a7d83fa915f40094fa57872b1448b8be11d66ba21c3d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#create NetworkSecuritySecurityProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#delete NetworkSecuritySecurityProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_security_profile#update NetworkSecuritySecurityProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecuritySecurityProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecuritySecurityProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecuritySecurityProfile.NetworkSecuritySecurityProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__325ffdf71cd0447d3002cc3c9297b09f01a9b828f965f96f1de57e4a11672afa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81da4440b830395af950bc393ff002b10f82fad1fbcf224b62667b6e91125e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a6d61c5d415beb5b4a87f37f6eab9573afe58da8f239b9f3d5ecf878e8f0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f06d07e9216cc21a24403128cb2da692517cd757ada1abde3c41201c9b365d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9c47385f144979c77d4720c77154c55a2a2538c9cc512dd7c6d434148e1e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkSecuritySecurityProfile",
    "NetworkSecuritySecurityProfileConfig",
    "NetworkSecuritySecurityProfileCustomInterceptProfile",
    "NetworkSecuritySecurityProfileCustomInterceptProfileOutputReference",
    "NetworkSecuritySecurityProfileCustomMirroringProfile",
    "NetworkSecuritySecurityProfileCustomMirroringProfileOutputReference",
    "NetworkSecuritySecurityProfileThreatPreventionProfile",
    "NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides",
    "NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesList",
    "NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverridesOutputReference",
    "NetworkSecuritySecurityProfileThreatPreventionProfileOutputReference",
    "NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides",
    "NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesList",
    "NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverridesOutputReference",
    "NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides",
    "NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesList",
    "NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverridesOutputReference",
    "NetworkSecuritySecurityProfileTimeouts",
    "NetworkSecuritySecurityProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__41aa6d17897db920244db23671ce5b73d395fa293574cd5c9705b25aefe76677(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    custom_intercept_profile: typing.Optional[typing.Union[NetworkSecuritySecurityProfileCustomInterceptProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_mirroring_profile: typing.Optional[typing.Union[NetworkSecuritySecurityProfileCustomMirroringProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    threat_prevention_profile: typing.Optional[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecuritySecurityProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d5183cc2d774dbd9a60d1d9c6fd299060e4d9b19abf769a57bccd4b3e423ed8d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bc3d5524f1bcc1f01ec39c6b858452ef1d68b46c256dd472428f6ede0027f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbdd27e834bd2f5556c39c6e975d9be0356ed846748925415e9f8c0c2120bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce93e2d6e61a40124d975ef2114c4dad90d84b0e9ba36ac809b7cf7979f96560(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5570a79d57302007da2cb34ba0be446879590677b04e0daf6565dcab53a2a4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0be9e344e266ebada168302d946553f78285c80f8fa8807b4d18ad1e61403f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5081dde3929b7efdf8d689e72f5b950d0e96b0c1e0a442e842440fcb0413a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90fe052e1d456f23217519db0e700614849cf1c9df5133e8e0a8a3147e0c14d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dd217e24fd8a66c7e070b522799df0acf14e4fea12bf4c8ac263c2779f6f44(
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
    custom_intercept_profile: typing.Optional[typing.Union[NetworkSecuritySecurityProfileCustomInterceptProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_mirroring_profile: typing.Optional[typing.Union[NetworkSecuritySecurityProfileCustomMirroringProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    threat_prevention_profile: typing.Optional[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecuritySecurityProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed174bfa67b4a7a477f6638b599c563999cb6ba75967f99c33e610678856a12(
    *,
    intercept_endpoint_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2840485debd0c19ec2bcd9fd2269b2c0df07aa7b5f68114dc1041b69bd338ef0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d55c0ffe45329e3c7b98f05798580fca0564f74147e1eeb7a9d30aade40cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d39030921ce6ed6c7d7b524d36432737a9916365dc9c464ca1e577ff85f4e5b(
    value: typing.Optional[NetworkSecuritySecurityProfileCustomInterceptProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821490a64f85430afaa9f60754db501c0ee88f4e3e6b30f06ebe672948a9dc40(
    *,
    mirroring_endpoint_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a78fc52d9d265aa620ec6e9b196e1cb106cb1971eeeefeaafa5365234c68b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bd99ab52c862c86778a60393c1a7c5bcd058cccbc210dc27e2202999cf1040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c927cd3580e677e06e783b1d74d18fd7e50c3a1e8397b7054a30a7298e1cf7(
    value: typing.Optional[NetworkSecuritySecurityProfileCustomMirroringProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7eb2885fdc25ba69359652464040dc45bfea3ea6b43f17afe638dd2f132a70(
    *,
    antivirus_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    threat_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32f85e74e127a20c0e3704fa5f942cf24d10f0f2eef11b42ac1c3ff6c6b38ee(
    *,
    action: builtins.str,
    protocol: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad192ccea8736bf1f09b55e1a5c252a32d1cadd93636d2e28a1f20adf70ec266(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0acc223323af52224418f6892c9597bd154b111bf18eacadb82a5ddce088a17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cd27fa96d5f8cf396b1670e0bbbae1c1c574088b5cdbc54784ab07c803d5ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82aec1e594ccae930bbc835b60c82fd1b65141e06ad8fa13e0effa5583ce2c6e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037523632e66de2bd6a61f74baff5609a2b22578fab3ad61b1e2d4768aa00d3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d1631c73483aaeffe68be9cadb8b2018e3da4b1bcd4ef99a8c5e2d0cd9884f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9665c445ed29ceb9a7734c7e8a09d83e3beb1e12da9841d220d39614eb323f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a0cc417ab4fb8e06f49e60319c8161f045d51f0a0f63ac7971d2191a96fe83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e675a24b43b96c852dea04a16c43aa908e1754339f952097330060f94d5b3377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92d20973cd2259d7c796d35f82fca865f74c164d2a1f2cd61ec8d36117a0d81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6b77348e8dc8eea569b39ff9df968205e117555d2db2994254f7e822149728(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02a2feb5422c42559d2ceea01319c06c1982d66b7a2873a07d6a06807853f22(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileAntivirusOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a70420eda58659a0c6310a90c6ebcb5c066429e1191d93e67f02911c4387b5b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e641560e1bf316da743470db9f7b5c19aead5de438d414ac180f79c6390baba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39da4493f83f38a0cff000c1be1eb3799f3cd0408a05ddca8fe946c3c119135(
    value: typing.Optional[NetworkSecuritySecurityProfileThreatPreventionProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__302a81a4e9d1413762fc07cbafe7852b61d05c74a07049f991e127cfd347534e(
    *,
    action: builtins.str,
    severity: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c1d5caed285fbce9c574eb44debe3f9768ca1a2a798a15204b3412a3b35b44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539f9274e931b8bd061f98f7f0e5bbc39e94b3e9913e413e9ef85bdf3871aaa0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79175ae58a6d3bb2bb887863be208ae8b2448579a2b7df2b58e0112554721747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0523a2608f54e6b5132498c770b8636bb241e66095265b61303bf98d2bb420(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad0e91c5c219019418b95b9ceeb6e077b380acefc25b27a0de273865a7a3e1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf0f210393e75f57fff1cebf0adff389364f005df2b55a0b3c64143350c1117(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33279719ecb84cc36a83f4138faf4b48b4fb4676c1ed55a2b825916cec02680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89eb0b454ae9b71eb6fbc413b6250f130ec0d822788f8df991ce6d084186684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71b69806be8473dd4ca2878837d6975d4d30797cc297e39bb6ea9522f882222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77e26362b5810a7b18ae3f3d47806f515129c5a75422322a1735c52160413c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileSeverityOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6719af79071806ecf4631a26df1498cec79d0003b6d268e1f0c88f2b7b3fa2(
    *,
    action: builtins.str,
    threat_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839e44a099017a2aefd439aff5421309a25b28c5f5850ed2864a6afb198ad5d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a792efa36cbf66cd55c41659c2abad5e17a55299c15363eaa7e7051b1f47c834(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ad9ec7cae2dbe4e1b19aabac09c64694b166c80fa440fe3e45e44f2b7f0022(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dc460c984043183799f5b419085a2f57c5e24a41b74ff6d11b42deb8dc2888(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66115c5219ccf419f4ca8ee9922afdf00c4f760970c1371da791c7a4c13848f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b665ccb4b6a6c1b135d3c355a81c2ff77e5d4f33700c2885521f2dd86bc3b670(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53995a5cca9e00a4bad6eb7119dccacc9e2bc18498c88a1e492453c1d58cf2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c376e11193b3f9a88822b11dc69970a721a5c09ace1bdf2ab186904a194656e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe8a84daa69fcd132bc647dc8ada2d8c703dbc3670d586e48b2064795ee74db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6b112460cdfb12ff530deaadbe709d42832aeee0150efa65ddf858bc2a55fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileThreatPreventionProfileThreatOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b072d70af9288aee59a7d83fa915f40094fa57872b1448b8be11d66ba21c3d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325ffdf71cd0447d3002cc3c9297b09f01a9b828f965f96f1de57e4a11672afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81da4440b830395af950bc393ff002b10f82fad1fbcf224b62667b6e91125e15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a6d61c5d415beb5b4a87f37f6eab9573afe58da8f239b9f3d5ecf878e8f0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f06d07e9216cc21a24403128cb2da692517cd757ada1abde3c41201c9b365d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9c47385f144979c77d4720c77154c55a2a2538c9cc512dd7c6d434148e1e30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecuritySecurityProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
