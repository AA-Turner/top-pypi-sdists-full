r'''
# `google_chronicle_data_access_scope`

Refer to the Terraform Registry for docs: [`google_chronicle_data_access_scope`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope).
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


class ChronicleDataAccessScope(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScope",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope google_chronicle_data_access_scope}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_access_scope_id: builtins.str,
        instance: builtins.str,
        location: builtins.str,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChronicleDataAccessScopeAllowedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChronicleDataAccessScopeDeniedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ChronicleDataAccessScopeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope google_chronicle_data_access_scope} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_access_scope_id: Required. The user provided scope id which will become the last part of the name of the scope resource. Needs to be compliant with https://google.aip.dev/122 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_scope_id ChronicleDataAccessScope#data_access_scope_id}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#instance ChronicleDataAccessScope#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#location ChronicleDataAccessScope#location}
        :param allow_all: Optional. Whether or not the scope allows all labels, allow_all and allowed_data_access_labels are mutually exclusive and one of them must be present. denied_data_access_labels can still be used along with allow_all. When combined with denied_data_access_labels, access will be granted to all data that doesn't have labels mentioned in denied_data_access_labels. E.g.: A customer with scope with denied labels A and B and allow_all will be able to see all data except data labeled with A and data labeled with B and data with labels A and B. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#allow_all ChronicleDataAccessScope#allow_all}
        :param allowed_data_access_labels: allowed_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#allowed_data_access_labels ChronicleDataAccessScope#allowed_data_access_labels}
        :param denied_data_access_labels: denied_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#denied_data_access_labels ChronicleDataAccessScope#denied_data_access_labels}
        :param description: Optional. A description of the data access scope for a human reader. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#description ChronicleDataAccessScope#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#id ChronicleDataAccessScope#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#project ChronicleDataAccessScope#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#timeouts ChronicleDataAccessScope#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ebe08bda385b525eda2f675b2a2b5e85ef4c745b7f06348db9d3126ca4a4e21)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ChronicleDataAccessScopeConfig(
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
        '''Generates CDKTF code for importing a ChronicleDataAccessScope resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ChronicleDataAccessScope to import.
        :param import_from_id: The id of the existing ChronicleDataAccessScope that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ChronicleDataAccessScope to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95772cfc057a04fe6c0fa7300db4d7d512f4d7f60ae1f9aca178575067b40cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllowedDataAccessLabels")
    def put_allowed_data_access_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChronicleDataAccessScopeAllowedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981157ba28d8055215dc0a959336310f2ba3a5139f144d360759a719dda71cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedDataAccessLabels", [value]))

    @jsii.member(jsii_name="putDeniedDataAccessLabels")
    def put_denied_data_access_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChronicleDataAccessScopeDeniedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d68af9374f3f52687ca71e4f15e9860e86b1feeff312914a0dd13c381d4e5a)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#create ChronicleDataAccessScope#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#delete ChronicleDataAccessScope#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#update ChronicleDataAccessScope#update}.
        '''
        value = ChronicleDataAccessScopeTimeouts(
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
    ) -> "ChronicleDataAccessScopeAllowedDataAccessLabelsList":
        return typing.cast("ChronicleDataAccessScopeAllowedDataAccessLabelsList", jsii.get(self, "allowedDataAccessLabels"))

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
    ) -> "ChronicleDataAccessScopeDeniedDataAccessLabelsList":
        return typing.cast("ChronicleDataAccessScopeDeniedDataAccessLabelsList", jsii.get(self, "deniedDataAccessLabels"))

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
    def timeouts(self) -> "ChronicleDataAccessScopeTimeoutsOutputReference":
        return typing.cast("ChronicleDataAccessScopeTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChronicleDataAccessScopeAllowedDataAccessLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChronicleDataAccessScopeAllowedDataAccessLabels"]]], jsii.get(self, "allowedDataAccessLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccessScopeIdInput")
    def data_access_scope_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessScopeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedDataAccessLabelsInput")
    def denied_data_access_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChronicleDataAccessScopeDeniedDataAccessLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChronicleDataAccessScopeDeniedDataAccessLabels"]]], jsii.get(self, "deniedDataAccessLabelsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChronicleDataAccessScopeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChronicleDataAccessScopeTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0116fddf41cb5c544a3a47acec4ba790558e2b83760769f3cb2c0d76eb520fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessScopeId")
    def data_access_scope_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessScopeId"))

    @data_access_scope_id.setter
    def data_access_scope_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f9d566dcf8d376482ae73bdf3f18fcb46e7b1065e8f18b618885aa4af573d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessScopeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f76887d488464c936593933306fd32af39100c5cd406fa5d1c713f35a3b5b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8550f419c18e3dda378e7753e071d86db37592a3c6f45a2ca8ccc72b42289cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7a7e556bfcff39a41806a98af3d369c7b2a69f901c0de2a94352ca1a7958df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ed43b6265c4a88b305db69c1d0bcfb92b198f254f6a38d9c5c28a9f6462470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8dafdba0efe9d70d34b0593733d6841ff03eb9bc816c598316d871add52405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeAllowedDataAccessLabels",
    jsii_struct_bases=[],
    name_mapping={
        "asset_namespace": "assetNamespace",
        "data_access_label": "dataAccessLabel",
        "ingestion_label": "ingestionLabel",
        "log_type": "logType",
    },
)
class ChronicleDataAccessScopeAllowedDataAccessLabels:
    def __init__(
        self,
        *,
        asset_namespace: typing.Optional[builtins.str] = None,
        data_access_label: typing.Optional[builtins.str] = None,
        ingestion_label: typing.Optional[typing.Union["ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel", typing.Dict[builtins.str, typing.Any]]] = None,
        log_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_namespace: The asset namespace configured in the forwarder of the customer's events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#asset_namespace ChronicleDataAccessScope#asset_namespace}
        :param data_access_label: The name of the data access label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_label ChronicleDataAccessScope#data_access_label}
        :param ingestion_label: ingestion_label block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label ChronicleDataAccessScope#ingestion_label}
        :param log_type: The name of the log type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#log_type ChronicleDataAccessScope#log_type}
        '''
        if isinstance(ingestion_label, dict):
            ingestion_label = ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel(**ingestion_label)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7794e242c02b62520cc6726d4b5159f248eb7a745effed40a45c4a9292dd73b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#asset_namespace ChronicleDataAccessScope#asset_namespace}
        '''
        result = self._values.get("asset_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_access_label(self) -> typing.Optional[builtins.str]:
        '''The name of the data access label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_label ChronicleDataAccessScope#data_access_label}
        '''
        result = self._values.get("data_access_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_label(
        self,
    ) -> typing.Optional["ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel"]:
        '''ingestion_label block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label ChronicleDataAccessScope#ingestion_label}
        '''
        result = self._values.get("ingestion_label")
        return typing.cast(typing.Optional["ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel"], result)

    @builtins.property
    def log_type(self) -> typing.Optional[builtins.str]:
        '''The name of the log type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#log_type ChronicleDataAccessScope#log_type}
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleDataAccessScopeAllowedDataAccessLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel",
    jsii_struct_bases=[],
    name_mapping={
        "ingestion_label_key": "ingestionLabelKey",
        "ingestion_label_value": "ingestionLabelValue",
    },
)
class ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel:
    def __init__(
        self,
        *,
        ingestion_label_key: builtins.str,
        ingestion_label_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_key ChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_value ChronicleDataAccessScope#ingestion_label_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556112b57caeb02df7d986acff78be981965027fca92ebe078941af64ac90031)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_key ChronicleDataAccessScope#ingestion_label_key}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_value ChronicleDataAccessScope#ingestion_label_value}
        '''
        result = self._values.get("ingestion_label_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db2aa9707b2f0fa4a82aa5058f7a4280a55da5c2212d7bd005542411eee7f6aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c6ccb6d1f44176d3f8b918c9fe6b474df7f4c8ae020f2aa1d8b9c650c65a571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelValue")
    def ingestion_label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestionLabelValue"))

    @ingestion_label_value.setter
    def ingestion_label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac1aba89bcc1871ce92c07b31b3d0835d7b8d7996e92e72648a7a3e413d3ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58550da83fddda23a06c180e2fe9f277a854cec58c554fc7125c2956601378b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChronicleDataAccessScopeAllowedDataAccessLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeAllowedDataAccessLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89780b8e23d2cd5f6a156141bf719541b3b9c152f29f136916c83c34d28727a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e7cfbb27c2f6dff4d46ef1eb087ed83cafe5020cbc6c8a0259e39af7098769)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f474b122a2a97148404d9d3b71253f621ddbe1ed447ef6dfbf70346a96015e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d09d57038800c9cdd36148090c1fb7c22f0451c181d18e8ab523e6b53dd89f1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d02665779c04ec957739f8cb4d03d5bca77765f817969b950aba55a52bf02e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeAllowedDataAccessLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeAllowedDataAccessLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeAllowedDataAccessLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecea848eb60e18584cb8cc29b89746e60a7f1c93a46df6ec3a728abbd9d10457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__983fa48bbf50d324489ad5f11b6994d565fc2a2f5880f360d77c10f94a76a8a8)
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
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_key ChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_value ChronicleDataAccessScope#ingestion_label_value}
        '''
        value = ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel(
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
    ) -> ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference:
        return typing.cast(ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference, jsii.get(self, "ingestionLabel"))

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
    ) -> typing.Optional[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel], jsii.get(self, "ingestionLabelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d341943c76b167db6050e9c9fcca6bb995773dde1060a3ffc6bc758f388c2c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessLabel")
    def data_access_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessLabel"))

    @data_access_label.setter
    def data_access_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fb4a4b42b654def1ed8a19cdf8f703bb786de186e5dc85a392845581370973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))

    @log_type.setter
    def log_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8055bb5b0bb63f429910130af650de25acedc55005728c2f66e68883a4e44d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeAllowedDataAccessLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeAllowedDataAccessLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeAllowedDataAccessLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d94ea4bdc4abba32b7866da94947a03c1f5de73cec245cb0de630db8f26177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeConfig",
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
class ChronicleDataAccessScopeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChronicleDataAccessScopeDeniedDataAccessLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ChronicleDataAccessScopeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_access_scope_id: Required. The user provided scope id which will become the last part of the name of the scope resource. Needs to be compliant with https://google.aip.dev/122 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_scope_id ChronicleDataAccessScope#data_access_scope_id}
        :param instance: The unique identifier for the Chronicle instance, which is the same as the customer ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#instance ChronicleDataAccessScope#instance}
        :param location: The location of the resource. This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#location ChronicleDataAccessScope#location}
        :param allow_all: Optional. Whether or not the scope allows all labels, allow_all and allowed_data_access_labels are mutually exclusive and one of them must be present. denied_data_access_labels can still be used along with allow_all. When combined with denied_data_access_labels, access will be granted to all data that doesn't have labels mentioned in denied_data_access_labels. E.g.: A customer with scope with denied labels A and B and allow_all will be able to see all data except data labeled with A and data labeled with B and data with labels A and B. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#allow_all ChronicleDataAccessScope#allow_all}
        :param allowed_data_access_labels: allowed_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#allowed_data_access_labels ChronicleDataAccessScope#allowed_data_access_labels}
        :param denied_data_access_labels: denied_data_access_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#denied_data_access_labels ChronicleDataAccessScope#denied_data_access_labels}
        :param description: Optional. A description of the data access scope for a human reader. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#description ChronicleDataAccessScope#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#id ChronicleDataAccessScope#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#project ChronicleDataAccessScope#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#timeouts ChronicleDataAccessScope#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ChronicleDataAccessScopeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cc2de825d616a480e74340e07c99ebfe69c14f04649996b161a71f5c6d4bb1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_scope_id ChronicleDataAccessScope#data_access_scope_id}
        '''
        result = self._values.get("data_access_scope_id")
        assert result is not None, "Required property 'data_access_scope_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance(self) -> builtins.str:
        '''The unique identifier for the Chronicle instance, which is the same as the customer ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#instance ChronicleDataAccessScope#instance}
        '''
        result = self._values.get("instance")
        assert result is not None, "Required property 'instance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        This is the geographical region where the Chronicle instance resides, such as "us" or "europe-west2".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#location ChronicleDataAccessScope#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#allow_all ChronicleDataAccessScope#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_data_access_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeAllowedDataAccessLabels]]]:
        '''allowed_data_access_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#allowed_data_access_labels ChronicleDataAccessScope#allowed_data_access_labels}
        '''
        result = self._values.get("allowed_data_access_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeAllowedDataAccessLabels]]], result)

    @builtins.property
    def denied_data_access_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChronicleDataAccessScopeDeniedDataAccessLabels"]]]:
        '''denied_data_access_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#denied_data_access_labels ChronicleDataAccessScope#denied_data_access_labels}
        '''
        result = self._values.get("denied_data_access_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChronicleDataAccessScopeDeniedDataAccessLabels"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A description of the data access scope for a human reader.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#description ChronicleDataAccessScope#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#id ChronicleDataAccessScope#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#project ChronicleDataAccessScope#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ChronicleDataAccessScopeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#timeouts ChronicleDataAccessScope#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ChronicleDataAccessScopeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleDataAccessScopeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeDeniedDataAccessLabels",
    jsii_struct_bases=[],
    name_mapping={
        "asset_namespace": "assetNamespace",
        "data_access_label": "dataAccessLabel",
        "ingestion_label": "ingestionLabel",
        "log_type": "logType",
    },
)
class ChronicleDataAccessScopeDeniedDataAccessLabels:
    def __init__(
        self,
        *,
        asset_namespace: typing.Optional[builtins.str] = None,
        data_access_label: typing.Optional[builtins.str] = None,
        ingestion_label: typing.Optional[typing.Union["ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel", typing.Dict[builtins.str, typing.Any]]] = None,
        log_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_namespace: The asset namespace configured in the forwarder of the customer's events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#asset_namespace ChronicleDataAccessScope#asset_namespace}
        :param data_access_label: The name of the data access label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_label ChronicleDataAccessScope#data_access_label}
        :param ingestion_label: ingestion_label block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label ChronicleDataAccessScope#ingestion_label}
        :param log_type: The name of the log type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#log_type ChronicleDataAccessScope#log_type}
        '''
        if isinstance(ingestion_label, dict):
            ingestion_label = ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel(**ingestion_label)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2105ee515baeeb90f57fa0df0713be12ac0f0fce80644707e8dc3054f426a64c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#asset_namespace ChronicleDataAccessScope#asset_namespace}
        '''
        result = self._values.get("asset_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_access_label(self) -> typing.Optional[builtins.str]:
        '''The name of the data access label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#data_access_label ChronicleDataAccessScope#data_access_label}
        '''
        result = self._values.get("data_access_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_label(
        self,
    ) -> typing.Optional["ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel"]:
        '''ingestion_label block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label ChronicleDataAccessScope#ingestion_label}
        '''
        result = self._values.get("ingestion_label")
        return typing.cast(typing.Optional["ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel"], result)

    @builtins.property
    def log_type(self) -> typing.Optional[builtins.str]:
        '''The name of the log type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#log_type ChronicleDataAccessScope#log_type}
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleDataAccessScopeDeniedDataAccessLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel",
    jsii_struct_bases=[],
    name_mapping={
        "ingestion_label_key": "ingestionLabelKey",
        "ingestion_label_value": "ingestionLabelValue",
    },
)
class ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel:
    def __init__(
        self,
        *,
        ingestion_label_key: builtins.str,
        ingestion_label_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_key ChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_value ChronicleDataAccessScope#ingestion_label_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cd5d0b695c32721bf20e038db5c43f6bc5a8a3d1f39cd7b99e7b05c3c84ab6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_key ChronicleDataAccessScope#ingestion_label_key}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_value ChronicleDataAccessScope#ingestion_label_value}
        '''
        result = self._values.get("ingestion_label_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__387195649ff0a239ea9048b73ddbc10c7a47674268a2d9a1b50fc6c075c49561)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96d0d06073e383796947fd329e2b33508933cc5c03d37d9775a04b821b9ac9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingestionLabelValue")
    def ingestion_label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingestionLabelValue"))

    @ingestion_label_value.setter
    def ingestion_label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f50e379eefb962179a089426a3991091e34b5c8c146f0f1158dbabbe2ab0dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionLabelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babf4b30394ad1fdefdbe5a4947afe52b13c49f0e45d0b67c4fce9f26c806851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChronicleDataAccessScopeDeniedDataAccessLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeDeniedDataAccessLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18b000f779bb6718f2238dec7fe882873b521ad47b05055a2e20e8027b6f55eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2818312490e9c9c8989ab3b6278d0e01f9174d7023ff615f4590a95f7e42a1ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e115cad1a649a8666dc8880077270848b3bef09f09f0b15d895e160889cc07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cca1cd52289566444801cd0f1cdcf9194105ee471eae4adb03a570e8b95fab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c33f01ac37ca33dcc605afa171ca48e68a12e092022c742b7ac8b6bde37731b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeDeniedDataAccessLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeDeniedDataAccessLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeDeniedDataAccessLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76e06d7567ba6bb2b9eeea92c7ced41c38df38be6f66204ad0d57b904ee3435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__404439d8403f3820b5b82b32bb2f3b27f195946d95b162fbeaf20d02d9ec608b)
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
        :param ingestion_label_key: Required. The key of the ingestion label. Always required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_key ChronicleDataAccessScope#ingestion_label_key}
        :param ingestion_label_value: Optional. The value of the ingestion label. Optional. An object with no provided value and some key provided would match against the given key and ANY value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#ingestion_label_value ChronicleDataAccessScope#ingestion_label_value}
        '''
        value = ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel(
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
    ) -> ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference:
        return typing.cast(ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference, jsii.get(self, "ingestionLabel"))

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
    ) -> typing.Optional[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel]:
        return typing.cast(typing.Optional[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel], jsii.get(self, "ingestionLabelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__63ca9278224739e3f19543ce9720f258cc1145309e2bdedd87970897278da5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessLabel")
    def data_access_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessLabel"))

    @data_access_label.setter
    def data_access_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3c5c57b24e00ac6ad35ad0d8c92adf3d6233020469aec50ac573fbaab21c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))

    @log_type.setter
    def log_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87edd03f18149dc4a2f9189f2f590c72a60214b667e67a9f8129b24787c5283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeDeniedDataAccessLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeDeniedDataAccessLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeDeniedDataAccessLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a3235df760aa8d14652134a80e0d15bfd8719c0ae4314fc50696c4342e6c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ChronicleDataAccessScopeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#create ChronicleDataAccessScope#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#delete ChronicleDataAccessScope#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#update ChronicleDataAccessScope#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1686c3d1442b2edd1e02b600544dbf1d32e6845f1ef38f1ca75059e593604cd8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#create ChronicleDataAccessScope#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#delete ChronicleDataAccessScope#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/chronicle_data_access_scope#update ChronicleDataAccessScope#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChronicleDataAccessScopeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChronicleDataAccessScopeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.chronicleDataAccessScope.ChronicleDataAccessScopeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__939f646a4555cf0461b878fecb5c3dbc207134910d0d3496adf3af87113dd102)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95ce606cfd124a899a92f455103707fd35df0ee7b898fe516c66ad046f8ac397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73567f94ab1b3eeb194f15dd19c82854d9d14686ab43a5a7d3e489ad6ad660bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824767cdfd727f60067077d590ca69a866b6fad27f0102904c2cdcc384f79450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1770bb5702859e5bd72795465e1af0a641913935e6834d7f1043b35eceb6d5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ChronicleDataAccessScope",
    "ChronicleDataAccessScopeAllowedDataAccessLabels",
    "ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel",
    "ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabelOutputReference",
    "ChronicleDataAccessScopeAllowedDataAccessLabelsList",
    "ChronicleDataAccessScopeAllowedDataAccessLabelsOutputReference",
    "ChronicleDataAccessScopeConfig",
    "ChronicleDataAccessScopeDeniedDataAccessLabels",
    "ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel",
    "ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabelOutputReference",
    "ChronicleDataAccessScopeDeniedDataAccessLabelsList",
    "ChronicleDataAccessScopeDeniedDataAccessLabelsOutputReference",
    "ChronicleDataAccessScopeTimeouts",
    "ChronicleDataAccessScopeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1ebe08bda385b525eda2f675b2a2b5e85ef4c745b7f06348db9d3126ca4a4e21(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_access_scope_id: builtins.str,
    instance: builtins.str,
    location: builtins.str,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeDeniedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ChronicleDataAccessScopeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c95772cfc057a04fe6c0fa7300db4d7d512f4d7f60ae1f9aca178575067b40cb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981157ba28d8055215dc0a959336310f2ba3a5139f144d360759a719dda71cf0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d68af9374f3f52687ca71e4f15e9860e86b1feeff312914a0dd13c381d4e5a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeDeniedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0116fddf41cb5c544a3a47acec4ba790558e2b83760769f3cb2c0d76eb520fd1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f9d566dcf8d376482ae73bdf3f18fcb46e7b1065e8f18b618885aa4af573d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f76887d488464c936593933306fd32af39100c5cd406fa5d1c713f35a3b5b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8550f419c18e3dda378e7753e071d86db37592a3c6f45a2ca8ccc72b42289cc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7a7e556bfcff39a41806a98af3d369c7b2a69f901c0de2a94352ca1a7958df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ed43b6265c4a88b305db69c1d0bcfb92b198f254f6a38d9c5c28a9f6462470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8dafdba0efe9d70d34b0593733d6841ff03eb9bc816c598316d871add52405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7794e242c02b62520cc6726d4b5159f248eb7a745effed40a45c4a9292dd73b1(
    *,
    asset_namespace: typing.Optional[builtins.str] = None,
    data_access_label: typing.Optional[builtins.str] = None,
    ingestion_label: typing.Optional[typing.Union[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel, typing.Dict[builtins.str, typing.Any]]] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556112b57caeb02df7d986acff78be981965027fca92ebe078941af64ac90031(
    *,
    ingestion_label_key: builtins.str,
    ingestion_label_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2aa9707b2f0fa4a82aa5058f7a4280a55da5c2212d7bd005542411eee7f6aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6ccb6d1f44176d3f8b918c9fe6b474df7f4c8ae020f2aa1d8b9c650c65a571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac1aba89bcc1871ce92c07b31b3d0835d7b8d7996e92e72648a7a3e413d3ad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58550da83fddda23a06c180e2fe9f277a854cec58c554fc7125c2956601378b7(
    value: typing.Optional[ChronicleDataAccessScopeAllowedDataAccessLabelsIngestionLabel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89780b8e23d2cd5f6a156141bf719541b3b9c152f29f136916c83c34d28727a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e7cfbb27c2f6dff4d46ef1eb087ed83cafe5020cbc6c8a0259e39af7098769(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f474b122a2a97148404d9d3b71253f621ddbe1ed447ef6dfbf70346a96015e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09d57038800c9cdd36148090c1fb7c22f0451c181d18e8ab523e6b53dd89f1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d02665779c04ec957739f8cb4d03d5bca77765f817969b950aba55a52bf02e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecea848eb60e18584cb8cc29b89746e60a7f1c93a46df6ec3a728abbd9d10457(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeAllowedDataAccessLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983fa48bbf50d324489ad5f11b6994d565fc2a2f5880f360d77c10f94a76a8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d341943c76b167db6050e9c9fcca6bb995773dde1060a3ffc6bc758f388c2c03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fb4a4b42b654def1ed8a19cdf8f703bb786de186e5dc85a392845581370973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8055bb5b0bb63f429910130af650de25acedc55005728c2f66e68883a4e44d7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d94ea4bdc4abba32b7866da94947a03c1f5de73cec245cb0de630db8f26177(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeAllowedDataAccessLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cc2de825d616a480e74340e07c99ebfe69c14f04649996b161a71f5c6d4bb1(
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
    allowed_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeAllowedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    denied_data_access_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChronicleDataAccessScopeDeniedDataAccessLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ChronicleDataAccessScopeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2105ee515baeeb90f57fa0df0713be12ac0f0fce80644707e8dc3054f426a64c(
    *,
    asset_namespace: typing.Optional[builtins.str] = None,
    data_access_label: typing.Optional[builtins.str] = None,
    ingestion_label: typing.Optional[typing.Union[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel, typing.Dict[builtins.str, typing.Any]]] = None,
    log_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cd5d0b695c32721bf20e038db5c43f6bc5a8a3d1f39cd7b99e7b05c3c84ab6(
    *,
    ingestion_label_key: builtins.str,
    ingestion_label_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387195649ff0a239ea9048b73ddbc10c7a47674268a2d9a1b50fc6c075c49561(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d0d06073e383796947fd329e2b33508933cc5c03d37d9775a04b821b9ac9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f50e379eefb962179a089426a3991091e34b5c8c146f0f1158dbabbe2ab0dc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babf4b30394ad1fdefdbe5a4947afe52b13c49f0e45d0b67c4fce9f26c806851(
    value: typing.Optional[ChronicleDataAccessScopeDeniedDataAccessLabelsIngestionLabel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b000f779bb6718f2238dec7fe882873b521ad47b05055a2e20e8027b6f55eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2818312490e9c9c8989ab3b6278d0e01f9174d7023ff615f4590a95f7e42a1ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e115cad1a649a8666dc8880077270848b3bef09f09f0b15d895e160889cc07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cca1cd52289566444801cd0f1cdcf9194105ee471eae4adb03a570e8b95fab5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c33f01ac37ca33dcc605afa171ca48e68a12e092022c742b7ac8b6bde37731b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76e06d7567ba6bb2b9eeea92c7ced41c38df38be6f66204ad0d57b904ee3435(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChronicleDataAccessScopeDeniedDataAccessLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404439d8403f3820b5b82b32bb2f3b27f195946d95b162fbeaf20d02d9ec608b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ca9278224739e3f19543ce9720f258cc1145309e2bdedd87970897278da5fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3c5c57b24e00ac6ad35ad0d8c92adf3d6233020469aec50ac573fbaab21c72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87edd03f18149dc4a2f9189f2f590c72a60214b667e67a9f8129b24787c5283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a3235df760aa8d14652134a80e0d15bfd8719c0ae4314fc50696c4342e6c8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeDeniedDataAccessLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1686c3d1442b2edd1e02b600544dbf1d32e6845f1ef38f1ca75059e593604cd8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939f646a4555cf0461b878fecb5c3dbc207134910d0d3496adf3af87113dd102(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ce606cfd124a899a92f455103707fd35df0ee7b898fe516c66ad046f8ac397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73567f94ab1b3eeb194f15dd19c82854d9d14686ab43a5a7d3e489ad6ad660bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824767cdfd727f60067077d590ca69a866b6fad27f0102904c2cdcc384f79450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1770bb5702859e5bd72795465e1af0a641913935e6834d7f1043b35eceb6d5d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChronicleDataAccessScopeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
