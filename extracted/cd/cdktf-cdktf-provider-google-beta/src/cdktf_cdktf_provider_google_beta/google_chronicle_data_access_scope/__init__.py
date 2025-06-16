r'''
# `google_chronicle_data_access_scope`

Refer to the Terraform Registry for docs: [`google_chronicle_data_access_scope`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope).
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


class GoogleChronicleDataAccessScope(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScope",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope google_chronicle_data_access_scope}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_access_scope_id: builtins.str,
        instance: builtins.str,
        location: builtins.str,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleChronicleDataAccessScopeAllowedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleChronicleDataAccessScopeDeniedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleChronicleDataAccessScopeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope google_chronicle_data_access_scope} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_access_scope_id: Required. The user provided scope id which will become the last part of the name of the scope resource. Needs to be compliant with https://google.aip.dev/122 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_scope_id GoogleChronicleDataAccessScope#data_access_scope_id}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#instance GoogleChronicleDataAccessScope#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#location GoogleChronicleDataAccessScope#location}
        :param allow_all: Optional. Whether or not the scope allows all labels, allow_all and allowed_data_access_labels are mutually exclusive and one of them must be present. denied_data_access_labels can still be used along with allow_all. When combined with denied_data_access_labels, access will be granted to all data that doesn't have labels mentioned in denied_data_access_labels. E.g.: A customer with scope with denied labels A and B and allow_all will be able to see all data except data labeled with A and data labeled with B and data with labels A and B. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#allow_all GoogleChronicleDataAccessScope#allow_all}
        :param allowed_data_access_labels: allowed_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#allowed_data_access_labels GoogleChronicleDataAccessScope#allowed_data_access_labels}
        :param denied_data_access_labels: denied_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#denied_data_access_labels GoogleChronicleDataAccessScope#denied_data_access_labels}
        :param description: Optional. A description of the data access scope for a human reader. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#description GoogleChronicleDataAccessScope#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#id GoogleChronicleDataAccessScope#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#project GoogleChronicleDataAccessScope#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#timeouts GoogleChronicleDataAccessScope#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5fa9706078c7895cbfa32891dcbf4726b3190c12e7d5333d50082b748fe4dbe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleChronicleDataAccessScopeConfig(
            data_access_scope_id=data_access_scope_id,
            instance=instance,
            location=location,
            allow_all=allow_all,
            allowed_data_access_labels=allowed_data_access_labels,
            denied_data_access_labels=denied_data_access_labels,
            description=description,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleChronicleDataAccessScope resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleChronicleDataAccessScope to import.
        :param import_from_id: The id of the existing GoogleChronicleDataAccessScope that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleChronicleDataAccessScope to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d165f0981d334c1bc81efab9be74af8b867d0c4584e5856ef2317dbdf286c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllowedDataAccessLabels")
    def put_allowed_data_access_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleChronicleDataAccessScopeAllowedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9881ba9257369dd9099c8f2db505c186ef8158a71fb31518fb1505f8665308a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedDataAccessLabels", [value]))

    @jsii.member(jsii_name="putDeniedDataAccessLabels")
    def put_denied_data_access_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleChronicleDataAccessScopeDeniedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc49ac00f5471fb04c37e1049e9437441de1e41bd5779813139b1360d36885c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeniedDataAccessLabels", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#create GoogleChronicleDataAccessScope#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#delete GoogleChronicleDataAccessScope#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#update GoogleChronicleDataAccessScope#update}.
        '''
        value = GoogleChronicleDataAccessScopeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetAllowedDataAccessLabels")
    def reset_allowed_data_access_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedDataAccessLabels", []))

    @jsii.member(jsii_name="resetDeniedDataAccessLabels")
    def reset_denied_data_access_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedDataAccessLabels", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="allowedDataAccessLabels")
    def allowed_data_access_labels(
        self,
    ) -> "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsList":
        return typing.cast("GoogleChronicleDataAccessScopeAllowedDataAccessLabelsList", jsii.get(self, "allowedDataAccessLabels"))

    @builtins.property
    @jsii.member(jsii_name="author")
    def author(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "author"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deniedDataAccessLabels")
    def denied_data_access_labels(
        self,
    ) -> "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsList":
        return typing.cast("GoogleChronicleDataAccessScopeDeniedDataAccessLabelsList", jsii.get(self, "deniedDataAccessLabels"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="lastEditor")
    def last_editor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastEditor"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleChronicleDataAccessScopeTimeoutsOutputReference":
        return typing.cast("GoogleChronicleDataAccessScopeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedDataAccessLabelsInput")
    def allowed_data_access_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleChronicleDataAccessScopeAllowedDataAccessLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleChronicleDataAccessScopeAllowedDataAccessLabels"]]], jsii.get(self, "allowedDataAccessLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccessScopeIdInput")
    def data_access_scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessScopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedDataAccessLabelsInput")
    def denied_data_access_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleChronicleDataAccessScopeDeniedDataAccessLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleChronicleDataAccessScopeDeniedDataAccessLabels"]]], jsii.get(self, "deniedDataAccessLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleChronicleDataAccessScopeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleChronicleDataAccessScopeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAll")
    def allow_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAll"))

    @allow_all.setter
    def allow_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b18d7eb56d9bffeb57cf2112e86998d050c60a830204f005155623c4299c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessScopeId")
    def data_access_scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessScopeId"))

    @data_access_scope_id.setter
    def data_access_scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b17d00967d456cc809520238de33fb585b251aa5195f2794424f6ba63d3c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessScopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e207cc0f01b54a7e9492ad59e4ae77d00d0189ed6bd5b8fe67cdaf0271e458b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ed7ebc5c48dd308bb6776787398a62c420f4a367d6eaea82a2cb4afa449701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79127b2c8205d36746c03c3063b6b4e35155e76e1a2e00d725310331c9adbaa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b920d6f6c894f5f5280b32687c27a88daa7eea0d134dbc02d62bf2dbeb3b88b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3778899747d3e94ceae011197558771cc0211b4848474ddc7a00674939b9ba8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeAllowedDataAccessLabels",
    jsii_struct_bases=[],
    name_mapping={
        "asset_namespace": "assetNamespace",
        "data_access_label": "dataAccessLabel",
        "ingestion_label": "ingestionLabel",
        "log_type": "logType",
    },
)
class GoogleChronicleDataAccessScopeAllowedDataAccessLabels:
    def __init__(
        self,
        *,
        asset_namespace: typing.Optional[builtins.str] = None,
        data_access_label: typing.Optional[builtins.str] = None,
        ingestion_label: typing.Optional[typing.Union["GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel", typing.Dict[builtins.str, typing.Any]]] = None,
        log_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_namespace: The asset namespace configured in the forwarder of the customer's events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#asset_namespace GoogleChronicleDataAccessScope#asset_namespace}
        :param data_access_label: The name of the data access label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_label GoogleChronicleDataAccessScope#data_access_label}
        :param ingestion_label: ingestion_label block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label GoogleChronicleDataAccessScope#ingestion_label}
        :param log_type: The name of the log type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#log_type GoogleChronicleDataAccessScope#log_type}
        '''
        if isinstance(ingestion_label, dict):
            ingestion_label = GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel(**ingestion_label)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6541e920a8c3d88b54b5d38a4864d8b8820e30526993acbf0dcb97116072e4ef)
            check_type(argname="argument asset_namespace", value=asset_namespace, expected_type=type_hints["asset_namespace"])
            check_type(argname="argument data_access_label", value=data_access_label, expected_type=type_hints["data_access_label"])
            check_type(argname="argument ingestion_label", value=ingestion_label, expected_type=type_hints["ingestion_label"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_namespace is not None:
            self._values["asset_namespace"] = asset_namespace
        if data_access_label is not None:
            self._values["data_access_label"] = data_access_label
        if ingestion_label is not None:
            self._values["ingestion_label"] = ingestion_label
        if log_type is not None:
            self._values["log_type"] = log_type

    @builtins.property
    def asset_namespace(self) -> typing.Optional[builtins.str]:
        '''The asset namespace configured in the forwarder of the customer's events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#asset_namespace GoogleChronicleDataAccessScope#asset_namespace}
        '''
        result = self._values.get("asset_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_access_label(self) -> typing.Optional[builtins.str]:
        '''The name of the data access label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_label GoogleChronicleDataAccessScope#data_access_label}
        '''
        result = self._values.get("data_access_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_label(
        self,
    ) -> typing.Optional["GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel"]:
        '''ingestion_label block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label GoogleChronicleDataAccessScope#ingestion_label}
        '''
        result = self._values.get("ingestion_label")
        return typing.cast(typing.Optional["GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel"], result)

    @builtins.property
    def log_type(self) -> typing.Optional[builtins.str]:
        '''The name of the log type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#log_type GoogleChronicleDataAccessScope#log_type}
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleDataAccessScopeAllowedDataAccessLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel",
    jsii_struct_bases=[],
    name_mapping={
        "ingestion_label_key": "ingestionLabelKey",
        "ingestion_label_value": "ingestionLabelValue",
    },
)
class GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel:
    def __init__(
        self,
        *,
        ingestion_label_key: builtins.str,
        ingestion_label_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_key GoogleChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_value GoogleChronicleDataAccessScope#ingestion_label_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f012c57934dc59c019825085ed309b380c04d4a331e96cfc9cc01c11bb24e593)
            check_type(argname="argument ingestion_label_key", value=ingestion_label_key, expected_type=type_hints["ingestion_label_key"])
            check_type(argname="argument ingestion_label_value", value=ingestion_label_value, expected_type=type_hints["ingestion_label_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingestion_label_key": ingestion_label_key,
        }
        if ingestion_label_value is not None:
            self._values["ingestion_label_value"] = ingestion_label_value

    @builtins.property
    def ingestion_label_key(self) -> builtins.str:
        '''Required. The key of the ingestion label. Always required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_key GoogleChronicleDataAccessScope#ingestion_label_key}
        '''
        result = self._values.get("ingestion_label_key")
        assert result is not None, "Required property 'ingestion_label_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ingestion_label_value(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The value of the ingestion label. Optional. An object
        with no provided value and some key provided would match
        against the given key and ANY value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_value GoogleChronicleDataAccessScope#ingestion_label_value}
        '''
        result = self._values.get("ingestion_label_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ff630dbd4070658fa6f13e9bd5d81089104a79256e57788a5cd70f98f83b34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIngestionLabelValue")
    def reset_ingestion_label_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngestionLabelValue", []))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelKeyInput")
    def ingestion_label_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingestionLabelKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelValueInput")
    def ingestion_label_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingestionLabelValueInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelKey")
    def ingestion_label_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestionLabelKey"))

    @ingestion_label_key.setter
    def ingestion_label_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77ff1a8902bb3f2ec22b4577bf96aa568c49f75e78fcb12f6211183d2236cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelValue")
    def ingestion_label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestionLabelValue"))

    @ingestion_label_value.setter
    def ingestion_label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014f280a60ad255847337c1661f50046a84f08af36c2890012dd8cae71208091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b29f439780c3f72b4416e386d47024f719505dbe931cf894433d5160dcfe66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleChronicleDataAccessScopeAllowedDataAccessLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeAllowedDataAccessLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdd81929facf6b59cbb44f6e79288ff1ab26ba8d58734f1123ac19f8c0b15ebd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0236eedcabe7b302f60f205fe00603c560759aa88706cff4be8c3456156b077f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3028f373995c44b3ccef897caf4670e3722a0bb81860139d4df5a61c47f76232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02175564697d4ea0b3867520f6467874f13b6ecfac549e7c8abd65569b1a4dfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24234beabc1292f523ab9720a59f2557525249be35aa6356364996737c529f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9520c301fc3f1c46505bf4d5ee182df1a55b90d1c45d55c29f7f18162781eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5471e6af47e1a1b573e515eea36f8ce83a0324f6a8f4a4d75b8929ba18316c42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIngestionLabel")
    def put_ingestion_label(
        self,
        *,
        ingestion_label_key: builtins.str,
        ingestion_label_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_key GoogleChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_value GoogleChronicleDataAccessScope#ingestion_label_value}
        '''
        value = GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel(
            ingestion_label_key=ingestion_label_key,
            ingestion_label_value=ingestion_label_value,
        )

        return typing.cast(None, jsii.invoke(self, "putIngestionLabel", [value]))

    @jsii.member(jsii_name="resetAssetNamespace")
    def reset_asset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetNamespace", []))

    @jsii.member(jsii_name="resetDataAccessLabel")
    def reset_data_access_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataAccessLabel", []))

    @jsii.member(jsii_name="resetIngestionLabel")
    def reset_ingestion_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngestionLabel", []))

    @jsii.member(jsii_name="resetLogType")
    def reset_log_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogType", []))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabel")
    def ingestion_label(
        self,
    ) -> GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference:
        return typing.cast(GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference, jsii.get(self, "ingestionLabel"))

    @builtins.property
    @jsii.member(jsii_name="assetNamespaceInput")
    def asset_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccessLabelInput")
    def data_access_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelInput")
    def ingestion_label_input(
        self,
    ) -> typing.Optional[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel], jsii.get(self, "ingestionLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="logTypeInput")
    def log_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="assetNamespace")
    def asset_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetNamespace"))

    @asset_namespace.setter
    def asset_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4b44cc248d05c29bb83768decbc252c2deef6f114fe3416e3321599f879084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessLabel")
    def data_access_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessLabel"))

    @data_access_label.setter
    def data_access_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea363ae2874494c76f5b78dfe0f06275727fec0367fc73304f935239abd6eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))

    @log_type.setter
    def log_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b15aca1afb24cc6f2c39b27206414fd8284b74d353312d70c39f6a88ea0055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeAllowedDataAccessLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeAllowedDataAccessLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7e962d1c0c8aa6a04044e5bf5b31b7f501a86487d36f0e96bddcc17e931e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_access_scope_id": "dataAccessScopeId",
        "instance": "instance",
        "location": "location",
        "allow_all": "allowAll",
        "allowed_data_access_labels": "allowedDataAccessLabels",
        "denied_data_access_labels": "deniedDataAccessLabels",
        "description": "description",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleChronicleDataAccessScopeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_access_scope_id: builtins.str,
        instance: builtins.str,
        location: builtins.str,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleChronicleDataAccessScopeDeniedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleChronicleDataAccessScopeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_access_scope_id: Required. The user provided scope id which will become the last part of the name of the scope resource. Needs to be compliant with https://google.aip.dev/122 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_scope_id GoogleChronicleDataAccessScope#data_access_scope_id}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#instance GoogleChronicleDataAccessScope#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#location GoogleChronicleDataAccessScope#location}
        :param allow_all: Optional. Whether or not the scope allows all labels, allow_all and allowed_data_access_labels are mutually exclusive and one of them must be present. denied_data_access_labels can still be used along with allow_all. When combined with denied_data_access_labels, access will be granted to all data that doesn't have labels mentioned in denied_data_access_labels. E.g.: A customer with scope with denied labels A and B and allow_all will be able to see all data except data labeled with A and data labeled with B and data with labels A and B. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#allow_all GoogleChronicleDataAccessScope#allow_all}
        :param allowed_data_access_labels: allowed_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#allowed_data_access_labels GoogleChronicleDataAccessScope#allowed_data_access_labels}
        :param denied_data_access_labels: denied_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#denied_data_access_labels GoogleChronicleDataAccessScope#denied_data_access_labels}
        :param description: Optional. A description of the data access scope for a human reader. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#description GoogleChronicleDataAccessScope#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#id GoogleChronicleDataAccessScope#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#project GoogleChronicleDataAccessScope#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#timeouts GoogleChronicleDataAccessScope#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleChronicleDataAccessScopeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7d845642b29fbef5fa0ec2375282e99b6fdec18ab8db223cd2f156c473b174)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_access_scope_id", value=data_access_scope_id, expected_type=type_hints["data_access_scope_id"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument allowed_data_access_labels", value=allowed_data_access_labels, expected_type=type_hints["allowed_data_access_labels"])
            check_type(argname="argument denied_data_access_labels", value=denied_data_access_labels, expected_type=type_hints["denied_data_access_labels"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_access_scope_id": data_access_scope_id,
            "instance": instance,
            "location": location,
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
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if allowed_data_access_labels is not None:
            self._values["allowed_data_access_labels"] = allowed_data_access_labels
        if denied_data_access_labels is not None:
            self._values["denied_data_access_labels"] = denied_data_access_labels
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def data_access_scope_id(self) -> builtins.str:
        '''Required.

        The user provided scope id which will become the last part of the name
        of the scope resource.
        Needs to be compliant with https://google.aip.dev/122

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_scope_id GoogleChronicleDataAccessScope#data_access_scope_id}
        '''
        result = self._values.get("data_access_scope_id")
        assert result is not None, "Required property 'data_access_scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''The unique identifier for the Chronicle instance, which is the same as the customer ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#instance GoogleChronicleDataAccessScope#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#location GoogleChronicleDataAccessScope#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether or not the scope allows all labels, allow_all and
        allowed_data_access_labels are mutually exclusive and one of them must be
        present. denied_data_access_labels can still be used along with allow_all.
        When combined with denied_data_access_labels, access will be granted to all
        data that doesn't have labels mentioned in denied_data_access_labels. E.g.:
        A customer with scope with denied labels A and B and allow_all will be able
        to see all data except data labeled with A and data labeled with B and data
        with labels A and B.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#allow_all GoogleChronicleDataAccessScope#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_data_access_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]]:
        '''allowed_data_access_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#allowed_data_access_labels GoogleChronicleDataAccessScope#allowed_data_access_labels}
        '''
        result = self._values.get("allowed_data_access_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]], result)

    @builtins.property
    def denied_data_access_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleChronicleDataAccessScopeDeniedDataAccessLabels"]]]:
        '''denied_data_access_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#denied_data_access_labels GoogleChronicleDataAccessScope#denied_data_access_labels}
        '''
        result = self._values.get("denied_data_access_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleChronicleDataAccessScopeDeniedDataAccessLabels"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A description of the data access scope for a human reader.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#description GoogleChronicleDataAccessScope#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#id GoogleChronicleDataAccessScope#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#project GoogleChronicleDataAccessScope#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleChronicleDataAccessScopeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#timeouts GoogleChronicleDataAccessScope#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleChronicleDataAccessScopeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleDataAccessScopeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeDeniedDataAccessLabels",
    jsii_struct_bases=[],
    name_mapping={
        "asset_namespace": "assetNamespace",
        "data_access_label": "dataAccessLabel",
        "ingestion_label": "ingestionLabel",
        "log_type": "logType",
    },
)
class GoogleChronicleDataAccessScopeDeniedDataAccessLabels:
    def __init__(
        self,
        *,
        asset_namespace: typing.Optional[builtins.str] = None,
        data_access_label: typing.Optional[builtins.str] = None,
        ingestion_label: typing.Optional[typing.Union["GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel", typing.Dict[builtins.str, typing.Any]]] = None,
        log_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_namespace: The asset namespace configured in the forwarder of the customer's events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#asset_namespace GoogleChronicleDataAccessScope#asset_namespace}
        :param data_access_label: The name of the data access label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_label GoogleChronicleDataAccessScope#data_access_label}
        :param ingestion_label: ingestion_label block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label GoogleChronicleDataAccessScope#ingestion_label}
        :param log_type: The name of the log type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#log_type GoogleChronicleDataAccessScope#log_type}
        '''
        if isinstance(ingestion_label, dict):
            ingestion_label = GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel(**ingestion_label)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80438b8944ac48f79b5e9f755fab97c6ca0654ffd2aff7cd479ad71cde529515)
            check_type(argname="argument asset_namespace", value=asset_namespace, expected_type=type_hints["asset_namespace"])
            check_type(argname="argument data_access_label", value=data_access_label, expected_type=type_hints["data_access_label"])
            check_type(argname="argument ingestion_label", value=ingestion_label, expected_type=type_hints["ingestion_label"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_namespace is not None:
            self._values["asset_namespace"] = asset_namespace
        if data_access_label is not None:
            self._values["data_access_label"] = data_access_label
        if ingestion_label is not None:
            self._values["ingestion_label"] = ingestion_label
        if log_type is not None:
            self._values["log_type"] = log_type

    @builtins.property
    def asset_namespace(self) -> typing.Optional[builtins.str]:
        '''The asset namespace configured in the forwarder of the customer's events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#asset_namespace GoogleChronicleDataAccessScope#asset_namespace}
        '''
        result = self._values.get("asset_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_access_label(self) -> typing.Optional[builtins.str]:
        '''The name of the data access label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#data_access_label GoogleChronicleDataAccessScope#data_access_label}
        '''
        result = self._values.get("data_access_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_label(
        self,
    ) -> typing.Optional["GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel"]:
        '''ingestion_label block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label GoogleChronicleDataAccessScope#ingestion_label}
        '''
        result = self._values.get("ingestion_label")
        return typing.cast(typing.Optional["GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel"], result)

    @builtins.property
    def log_type(self) -> typing.Optional[builtins.str]:
        '''The name of the log type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#log_type GoogleChronicleDataAccessScope#log_type}
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleDataAccessScopeDeniedDataAccessLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel",
    jsii_struct_bases=[],
    name_mapping={
        "ingestion_label_key": "ingestionLabelKey",
        "ingestion_label_value": "ingestionLabelValue",
    },
)
class GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel:
    def __init__(
        self,
        *,
        ingestion_label_key: builtins.str,
        ingestion_label_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_key GoogleChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_value GoogleChronicleDataAccessScope#ingestion_label_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ac63346d7285a95bc8dec8f838bacce685e254335699a602f941d72cc8fde7)
            check_type(argname="argument ingestion_label_key", value=ingestion_label_key, expected_type=type_hints["ingestion_label_key"])
            check_type(argname="argument ingestion_label_value", value=ingestion_label_value, expected_type=type_hints["ingestion_label_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingestion_label_key": ingestion_label_key,
        }
        if ingestion_label_value is not None:
            self._values["ingestion_label_value"] = ingestion_label_value

    @builtins.property
    def ingestion_label_key(self) -> builtins.str:
        '''Required. The key of the ingestion label. Always required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_key GoogleChronicleDataAccessScope#ingestion_label_key}
        '''
        result = self._values.get("ingestion_label_key")
        assert result is not None, "Required property 'ingestion_label_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ingestion_label_value(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The value of the ingestion label. Optional. An object
        with no provided value and some key provided would match
        against the given key and ANY value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_value GoogleChronicleDataAccessScope#ingestion_label_value}
        '''
        result = self._values.get("ingestion_label_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85db488e7aa3489ddb3ceda2c734b4c12b51332db8bfde8dfdcde08b9f85aaba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIngestionLabelValue")
    def reset_ingestion_label_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngestionLabelValue", []))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelKeyInput")
    def ingestion_label_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingestionLabelKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelValueInput")
    def ingestion_label_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingestionLabelValueInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelKey")
    def ingestion_label_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestionLabelKey"))

    @ingestion_label_key.setter
    def ingestion_label_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694a60494350119ebacdf503012e0ad2a1678e79fd38dbc68e9e4492251ff906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelValue")
    def ingestion_label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestionLabelValue"))

    @ingestion_label_value.setter
    def ingestion_label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046eaae4209bfb11f359b0a5d46f898986941bac19b0a4e19fc7a33d36860df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae70036218ca8891e3fab2dc5997edf30b09db7a0b7f430f9f2103b899affcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleChronicleDataAccessScopeDeniedDataAccessLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeDeniedDataAccessLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d4ace2810c84d07d30f96673216f624da3d4e330f4a22681dfabf81762b131f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2179054b8402c3b4f0336254666e6841b954d7de20024dcbba104226a1602f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23eafa8cdff6c7d39aa8168619ed71e21ec70fe40540d5c40293e04f5d4dd5f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a20eed9d5535400b64df33b5aa8593bbcf44f21d3fda81d2c9b4c87da775cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ddb596942399fbe81e3dd7a839770e9a4423edda6f2eb8a97c9b419c1a361f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeDeniedDataAccessLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeDeniedDataAccessLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeDeniedDataAccessLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157284d51b82007922f9177229746cee15f083501f5b833d1c9939df8ae8372d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f9aa00ad52295790286b16ea1c0ab75cf099dd042462bd88f5198c64dda043b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIngestionLabel")
    def put_ingestion_label(
        self,
        *,
        ingestion_label_key: builtins.str,
        ingestion_label_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_key GoogleChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#ingestion_label_value GoogleChronicleDataAccessScope#ingestion_label_value}
        '''
        value = GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel(
            ingestion_label_key=ingestion_label_key,
            ingestion_label_value=ingestion_label_value,
        )

        return typing.cast(None, jsii.invoke(self, "putIngestionLabel", [value]))

    @jsii.member(jsii_name="resetAssetNamespace")
    def reset_asset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetNamespace", []))

    @jsii.member(jsii_name="resetDataAccessLabel")
    def reset_data_access_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataAccessLabel", []))

    @jsii.member(jsii_name="resetIngestionLabel")
    def reset_ingestion_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngestionLabel", []))

    @jsii.member(jsii_name="resetLogType")
    def reset_log_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogType", []))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabel")
    def ingestion_label(
        self,
    ) -> GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference:
        return typing.cast(GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference, jsii.get(self, "ingestionLabel"))

    @builtins.property
    @jsii.member(jsii_name="assetNamespaceInput")
    def asset_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccessLabelInput")
    def data_access_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelInput")
    def ingestion_label_input(
        self,
    ) -> typing.Optional[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel], jsii.get(self, "ingestionLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="logTypeInput")
    def log_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="assetNamespace")
    def asset_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetNamespace"))

    @asset_namespace.setter
    def asset_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439b3ca64b77777ab6cace18a149c83a1cb5e52dfea02083ebf93d75379055da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessLabel")
    def data_access_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessLabel"))

    @data_access_label.setter
    def data_access_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93f87c510cfd1658014b362436713d0632255f602a84efcc67ab01736045c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))

    @log_type.setter
    def log_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbf4232d21a1e184f7c3a738798f9fcfbc6134439e59fba7d5429124ac4ece5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeDeniedDataAccessLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeDeniedDataAccessLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeDeniedDataAccessLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800859bfc2752cfdebd0199ddad22d300f6a48af6e4e0b9eb55b87e8c54ddf86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleChronicleDataAccessScopeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#create GoogleChronicleDataAccessScope#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#delete GoogleChronicleDataAccessScope#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#update GoogleChronicleDataAccessScope#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d07e29100158ca24c5a8c0f9fdcc115aefe8eb46b0de7e51fb6bb85bba6ae15)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#create GoogleChronicleDataAccessScope#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#delete GoogleChronicleDataAccessScope#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_chronicle_data_access_scope#update GoogleChronicleDataAccessScope#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleChronicleDataAccessScopeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleChronicleDataAccessScopeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleChronicleDataAccessScope.GoogleChronicleDataAccessScopeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7b5f592d4a93e553a0df37b515d7ee0c7f7d731119b7a865f34a77e25d4db9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__994b64f29db322b668e4f9e306e4eece58f847d36e85a893740a0107078805e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25b6571f8afef1c46ce823227852ae7f4dccb7b72e0c1e14bf3323bc35e4f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da675a2a592473e73f0cc08aa975a7dc0e481bc880d0f4d21ccba360920337d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6967c68aa903d7f0739380745c163dfc4a708877f1b20e4164545e85d17dd9d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleChronicleDataAccessScope",
    "GoogleChronicleDataAccessScopeAllowedDataAccessLabels",
    "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel",
    "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference",
    "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsList",
    "GoogleChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference",
    "GoogleChronicleDataAccessScopeConfig",
    "GoogleChronicleDataAccessScopeDeniedDataAccessLabels",
    "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel",
    "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference",
    "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsList",
    "GoogleChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference",
    "GoogleChronicleDataAccessScopeTimeouts",
    "GoogleChronicleDataAccessScopeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c5fa9706078c7895cbfa32891dcbf4726b3190c12e7d5333d50082b748fe4dbe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_access_scope_id: builtins.str,
    instance: builtins.str,
    location: builtins.str,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeDeniedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleChronicleDataAccessScopeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__32d165f0981d334c1bc81efab9be74af8b867d0c4584e5856ef2317dbdf286c3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9881ba9257369dd9099c8f2db505c186ef8158a71fb31518fb1505f8665308a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc49ac00f5471fb04c37e1049e9437441de1e41bd5779813139b1360d36885c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeDeniedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b18d7eb56d9bffeb57cf2112e86998d050c60a830204f005155623c4299c09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b17d00967d456cc809520238de33fb585b251aa5195f2794424f6ba63d3c7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e207cc0f01b54a7e9492ad59e4ae77d00d0189ed6bd5b8fe67cdaf0271e458b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ed7ebc5c48dd308bb6776787398a62c420f4a367d6eaea82a2cb4afa449701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79127b2c8205d36746c03c3063b6b4e35155e76e1a2e00d725310331c9adbaa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b920d6f6c894f5f5280b32687c27a88daa7eea0d134dbc02d62bf2dbeb3b88b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3778899747d3e94ceae011197558771cc0211b4848474ddc7a00674939b9ba8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6541e920a8c3d88b54b5d38a4864d8b8820e30526993acbf0dcb97116072e4ef(
    *,
    asset_namespace: typing.Optional[builtins.str] = None,
    data_access_label: typing.Optional[builtins.str] = None,
    ingestion_label: typing.Optional[typing.Union[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel, typing.Dict[builtins.str, typing.Any]]] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f012c57934dc59c019825085ed309b380c04d4a331e96cfc9cc01c11bb24e593(
    *,
    ingestion_label_key: builtins.str,
    ingestion_label_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ff630dbd4070658fa6f13e9bd5d81089104a79256e57788a5cd70f98f83b34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77ff1a8902bb3f2ec22b4577bf96aa568c49f75e78fcb12f6211183d2236cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014f280a60ad255847337c1661f50046a84f08af36c2890012dd8cae71208091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b29f439780c3f72b4416e386d47024f719505dbe931cf894433d5160dcfe66d(
    value: typing.Optional[GoogleChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd81929facf6b59cbb44f6e79288ff1ab26ba8d58734f1123ac19f8c0b15ebd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0236eedcabe7b302f60f205fe00603c560759aa88706cff4be8c3456156b077f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3028f373995c44b3ccef897caf4670e3722a0bb81860139d4df5a61c47f76232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02175564697d4ea0b3867520f6467874f13b6ecfac549e7c8abd65569b1a4dfd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24234beabc1292f523ab9720a59f2557525249be35aa6356364996737c529f32(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9520c301fc3f1c46505bf4d5ee182df1a55b90d1c45d55c29f7f18162781eb0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeAllowedDataAccessLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5471e6af47e1a1b573e515eea36f8ce83a0324f6a8f4a4d75b8929ba18316c42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4b44cc248d05c29bb83768decbc252c2deef6f114fe3416e3321599f879084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea363ae2874494c76f5b78dfe0f06275727fec0367fc73304f935239abd6eed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b15aca1afb24cc6f2c39b27206414fd8284b74d353312d70c39f6a88ea0055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7e962d1c0c8aa6a04044e5bf5b31b7f501a86487d36f0e96bddcc17e931e21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeAllowedDataAccessLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7d845642b29fbef5fa0ec2375282e99b6fdec18ab8db223cd2f156c473b174(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_access_scope_id: builtins.str,
    instance: builtins.str,
    location: builtins.str,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleChronicleDataAccessScopeDeniedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleChronicleDataAccessScopeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80438b8944ac48f79b5e9f755fab97c6ca0654ffd2aff7cd479ad71cde529515(
    *,
    asset_namespace: typing.Optional[builtins.str] = None,
    data_access_label: typing.Optional[builtins.str] = None,
    ingestion_label: typing.Optional[typing.Union[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel, typing.Dict[builtins.str, typing.Any]]] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ac63346d7285a95bc8dec8f838bacce685e254335699a602f941d72cc8fde7(
    *,
    ingestion_label_key: builtins.str,
    ingestion_label_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db488e7aa3489ddb3ceda2c734b4c12b51332db8bfde8dfdcde08b9f85aaba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694a60494350119ebacdf503012e0ad2a1678e79fd38dbc68e9e4492251ff906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046eaae4209bfb11f359b0a5d46f898986941bac19b0a4e19fc7a33d36860df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae70036218ca8891e3fab2dc5997edf30b09db7a0b7f430f9f2103b899affcd(
    value: typing.Optional[GoogleChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4ace2810c84d07d30f96673216f624da3d4e330f4a22681dfabf81762b131f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2179054b8402c3b4f0336254666e6841b954d7de20024dcbba104226a1602f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23eafa8cdff6c7d39aa8168619ed71e21ec70fe40540d5c40293e04f5d4dd5f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a20eed9d5535400b64df33b5aa8593bbcf44f21d3fda81d2c9b4c87da775cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ddb596942399fbe81e3dd7a839770e9a4423edda6f2eb8a97c9b419c1a361f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157284d51b82007922f9177229746cee15f083501f5b833d1c9939df8ae8372d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleChronicleDataAccessScopeDeniedDataAccessLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9aa00ad52295790286b16ea1c0ab75cf099dd042462bd88f5198c64dda043b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439b3ca64b77777ab6cace18a149c83a1cb5e52dfea02083ebf93d75379055da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93f87c510cfd1658014b362436713d0632255f602a84efcc67ab01736045c14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbf4232d21a1e184f7c3a738798f9fcfbc6134439e59fba7d5429124ac4ece5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800859bfc2752cfdebd0199ddad22d300f6a48af6e4e0b9eb55b87e8c54ddf86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeDeniedDataAccessLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d07e29100158ca24c5a8c0f9fdcc115aefe8eb46b0de7e51fb6bb85bba6ae15(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7b5f592d4a93e553a0df37b515d7ee0c7f7d731119b7a865f34a77e25d4db9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994b64f29db322b668e4f9e306e4eece58f847d36e85a893740a0107078805e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25b6571f8afef1c46ce823227852ae7f4dccb7b72e0c1e14bf3323bc35e4f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da675a2a592473e73f0cc08aa975a7dc0e481bc880d0f4d21ccba360920337d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6967c68aa903d7f0739380745c163dfc4a708877f1b20e4164545e85d17dd9d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleChronicleDataAccessScopeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
