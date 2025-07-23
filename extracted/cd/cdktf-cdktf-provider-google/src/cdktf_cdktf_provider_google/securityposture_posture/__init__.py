r'''
# `google_securityposture_posture`

Refer to the Terraform Registry for docs: [`google_securityposture_posture`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture).
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


class SecurityposturePosture(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosture",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture google_securityposture_posture}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        parent: builtins.str,
        policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySets", typing.Dict[builtins.str, typing.Any]]]],
        posture_id: builtins.str,
        state: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SecurityposturePostureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture google_securityposture_posture} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location of the resource, eg: global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param parent: The parent of the resource, an organization. Format should be 'organizations/{organization_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#parent SecurityposturePosture#parent}
        :param policy_sets: policy_sets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_sets SecurityposturePosture#policy_sets}
        :param posture_id: Id of the posture. It is an immutable field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#posture_id SecurityposturePosture#posture_id}
        :param state: State of the posture. Update to state field should not be triggered along with with other field updates. Possible values: ["DEPRECATED", "DRAFT", "ACTIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#state SecurityposturePosture#state}
        :param description: Description of the posture. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#id SecurityposturePosture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#timeouts SecurityposturePosture#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7697c142bb0da4188491eeceb3c517e83d422abf7f68be60e33cfc4b09a0bd82)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecurityposturePostureConfig(
            location=location,
            parent=parent,
            policy_sets=policy_sets,
            posture_id=posture_id,
            state=state,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a SecurityposturePosture resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecurityposturePosture to import.
        :param import_from_id: The id of the existing SecurityposturePosture that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecurityposturePosture to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71108f598f0ff47bd57a6382aab6d6298263f1971e7d29179e445f5eab403f95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPolicySets")
    def put_policy_sets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1779508c30a560ddecf0045c9dc9ce9a2c831d3d8d5c30c7768510b843052010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicySets", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#create SecurityposturePosture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#delete SecurityposturePosture#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#update SecurityposturePosture#update}.
        '''
        value = SecurityposturePostureTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="policySets")
    def policy_sets(self) -> "SecurityposturePosturePolicySetsList":
        return typing.cast("SecurityposturePosturePolicySetsList", jsii.get(self, "policySets"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="revisionId")
    def revision_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SecurityposturePostureTimeoutsOutputReference":
        return typing.cast("SecurityposturePostureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="policySetsInput")
    def policy_sets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySets"]]], jsii.get(self, "policySetsInput"))

    @builtins.property
    @jsii.member(jsii_name="postureIdInput")
    def posture_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postureIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecurityposturePostureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecurityposturePostureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbd4bc511d3081232bda0b91f55db09420d94cb159d62efdf748c815df81893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a7891f5bff187b08e34c613552fb7527dbde1d7cef1f52bc4ca793f15f30b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b62dda492e2a7b8c3350b6510f35789415e839e4fa9696fc18d6dec00b3269f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517aaac98bc69940dedd31c8e37d6fd31151d997a290c611fce824fcc9ed6dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postureId")
    def posture_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postureId"))

    @posture_id.setter
    def posture_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb4dcf2aadd89d4954a54b831cae0273f594dc7f45253523815a22a2497249a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753b5201e0b4e735742505ce62038d62a4a61e026eaefc9c64a035cd04df00db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePostureConfig",
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
        "parent": "parent",
        "policy_sets": "policySets",
        "posture_id": "postureId",
        "state": "state",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class SecurityposturePostureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        parent: builtins.str,
        policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySets", typing.Dict[builtins.str, typing.Any]]]],
        posture_id: builtins.str,
        state: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SecurityposturePostureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location of the resource, eg: global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param parent: The parent of the resource, an organization. Format should be 'organizations/{organization_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#parent SecurityposturePosture#parent}
        :param policy_sets: policy_sets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_sets SecurityposturePosture#policy_sets}
        :param posture_id: Id of the posture. It is an immutable field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#posture_id SecurityposturePosture#posture_id}
        :param state: State of the posture. Update to state field should not be triggered along with with other field updates. Possible values: ["DEPRECATED", "DRAFT", "ACTIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#state SecurityposturePosture#state}
        :param description: Description of the posture. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#id SecurityposturePosture#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#timeouts SecurityposturePosture#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SecurityposturePostureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e744464e62ababea440ba6177a12fa7e78f88334c19836063cb613da103a564c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument policy_sets", value=policy_sets, expected_type=type_hints["policy_sets"])
            check_type(argname="argument posture_id", value=posture_id, expected_type=type_hints["posture_id"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "parent": parent,
            "policy_sets": policy_sets,
            "posture_id": posture_id,
            "state": state,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
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
        '''Location of the resource, eg: global.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent of the resource, an organization. Format should be 'organizations/{organization_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#parent SecurityposturePosture#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_sets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySets"]]:
        '''policy_sets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_sets SecurityposturePosture#policy_sets}
        '''
        result = self._values.get("policy_sets")
        assert result is not None, "Required property 'policy_sets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySets"]], result)

    @builtins.property
    def posture_id(self) -> builtins.str:
        '''Id of the posture. It is an immutable field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#posture_id SecurityposturePosture#posture_id}
        '''
        result = self._values.get("posture_id")
        assert result is not None, "Required property 'posture_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''State of the posture.

        Update to state field should not be triggered along with
        with other field updates. Possible values: ["DEPRECATED", "DRAFT", "ACTIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#state SecurityposturePosture#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the posture.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#id SecurityposturePosture#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SecurityposturePostureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#timeouts SecurityposturePosture#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SecurityposturePostureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePostureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySets",
    jsii_struct_bases=[],
    name_mapping={
        "policies": "policies",
        "policy_set_id": "policySetId",
        "description": "description",
    },
)
class SecurityposturePosturePolicySets:
    def __init__(
        self,
        *,
        policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        policy_set_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param policies: policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policies SecurityposturePosture#policies}
        :param policy_set_id: ID of the policy set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_set_id SecurityposturePosture#policy_set_id}
        :param description: Description of the policy set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158a0479c913000d5259fcf113f768bf6dfbdd791a0d5de6a4f9318927f2a100)
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument policy_set_id", value=policy_set_id, expected_type=type_hints["policy_set_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policies": policies,
            "policy_set_id": policy_set_id,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPolicies"]]:
        '''policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policies SecurityposturePosture#policies}
        '''
        result = self._values.get("policies")
        assert result is not None, "Required property 'policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPolicies"]], result)

    @builtins.property
    def policy_set_id(self) -> builtins.str:
        '''ID of the policy set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_set_id SecurityposturePosture#policy_set_id}
        '''
        result = self._values.get("policy_set_id")
        assert result is not None, "Required property 'policy_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the policy set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af61e90207089045e796002210733be9da9dabc951f75d475b9bd1d7c69870fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityposturePosturePolicySetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b628b2d6106e24262d4e6139547b46a423014d5c7dd016570dc1b36234f79bef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityposturePosturePolicySetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae44c867429877cb04e87a792448146a11ecc7fa4cfc3efd25cec5e03586f60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8769dcab42fb08f8c382773117e94c6eb252131283f67b499dd01ec87f78a00a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__096e2044fc641b08309d2735b1323cb85b9ce56d701431d4e0d0c721711dced3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16761b016933ec2e5961bf4dbe1f5a03dfedb49d3772dae89bfda107e7938791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53cdd3902add819b25db19cbec2693fb8158c604844a3960ac7d07bd2f41a3a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicies")
    def put_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d066401ebc8239e58ffa7ae3590fa481143457ee1775de41216c18cb1d082b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicies", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> "SecurityposturePosturePolicySetsPoliciesList":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesList", jsii.get(self, "policies"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="policiesInput")
    def policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPolicies"]]], jsii.get(self, "policiesInput"))

    @builtins.property
    @jsii.member(jsii_name="policySetIdInput")
    def policy_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policySetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c0da95a64502faeb73c5cb5efc223424b91ce89cba551ff89f5efd8bbafb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policySetId")
    def policy_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policySetId"))

    @policy_set_id.setter
    def policy_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4127a407119fb824fc631ff5806e5360615e3dd1b756ba03cfcc47a49d2bd8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policySetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abed790be5183b1e5fc67737b77bca5b3197137a45faed3c2d4eae5916d46788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "constraint": "constraint",
        "policy_id": "policyId",
        "compliance_standards": "complianceStandards",
        "description": "description",
    },
)
class SecurityposturePosturePolicySetsPolicies:
    def __init__(
        self,
        *,
        constraint: typing.Union["SecurityposturePosturePolicySetsPoliciesConstraint", typing.Dict[builtins.str, typing.Any]],
        policy_id: builtins.str,
        compliance_standards: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesComplianceStandards", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param constraint: constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#constraint SecurityposturePosture#constraint}
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_id SecurityposturePosture#policy_id}
        :param compliance_standards: compliance_standards block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#compliance_standards SecurityposturePosture#compliance_standards}
        :param description: Description of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        if isinstance(constraint, dict):
            constraint = SecurityposturePosturePolicySetsPoliciesConstraint(**constraint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db2e503d18cb8959d2d353acfdd0903f66c1e576c4081c61cd5f9991ab94f09)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument compliance_standards", value=compliance_standards, expected_type=type_hints["compliance_standards"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "constraint": constraint,
            "policy_id": policy_id,
        }
        if compliance_standards is not None:
            self._values["compliance_standards"] = compliance_standards
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def constraint(self) -> "SecurityposturePosturePolicySetsPoliciesConstraint":
        '''constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#constraint SecurityposturePosture#constraint}
        '''
        result = self._values.get("constraint")
        assert result is not None, "Required property 'constraint' is missing"
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraint", result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''ID of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_id SecurityposturePosture#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compliance_standards(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesComplianceStandards"]]]:
        '''compliance_standards block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#compliance_standards SecurityposturePosture#compliance_standards}
        '''
        result = self._values.get("compliance_standards")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesComplianceStandards"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesComplianceStandards",
    jsii_struct_bases=[],
    name_mapping={"control": "control", "standard": "standard"},
)
class SecurityposturePosturePolicySetsPoliciesComplianceStandards:
    def __init__(
        self,
        *,
        control: typing.Optional[builtins.str] = None,
        standard: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control: Mapping of security controls for the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#control SecurityposturePosture#control}
        :param standard: Mapping of compliance standards for the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#standard SecurityposturePosture#standard}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4504f51b8bd3d117a46b91ef8269013f937b9213bd8410689194a52a20af603f)
            check_type(argname="argument control", value=control, expected_type=type_hints["control"])
            check_type(argname="argument standard", value=standard, expected_type=type_hints["standard"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control is not None:
            self._values["control"] = control
        if standard is not None:
            self._values["standard"] = standard

    @builtins.property
    def control(self) -> typing.Optional[builtins.str]:
        '''Mapping of security controls for the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#control SecurityposturePosture#control}
        '''
        result = self._values.get("control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard(self) -> typing.Optional[builtins.str]:
        '''Mapping of compliance standards for the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#standard SecurityposturePosture#standard}
        '''
        result = self._values.get("standard")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesComplianceStandards(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesComplianceStandardsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesComplianceStandardsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdda51542e23d72b50a6faaf7b016aa621394daa9049d331695c5c45bcfd8bcc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718fa5cdc732b0ec71c25b3ffb7178eeff3c24507572f6a0632d5ae55999c829)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5fc48a305bf4d140f21fbf0582e3e11aa08871a143f1d0fb742fd3ffd2c160)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd9845170e9468b9513bad60f4361a3022916f6faf6cc6af2f8ceeb618e2ecc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96c4542986c8e27d5cb32d2ffdfbbed2e561cd20f99025f5f68e8114db88bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesComplianceStandards]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesComplianceStandards]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesComplianceStandards]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88fbf4da20d80fb2582201837a2cb6c707aeb0d28557e4fdac7d5f29849b5453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37df75d2d59f546764dd50ea6bc47ec11ca750cfaea3bda8aaed40e0243a27e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetControl")
    def reset_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControl", []))

    @jsii.member(jsii_name="resetStandard")
    def reset_standard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandard", []))

    @builtins.property
    @jsii.member(jsii_name="controlInput")
    def control_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlInput"))

    @builtins.property
    @jsii.member(jsii_name="standardInput")
    def standard_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "standardInput"))

    @builtins.property
    @jsii.member(jsii_name="control")
    def control(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "control"))

    @control.setter
    def control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1977caa240bbb8af320767d628aeaab518dcbd6c6b3a916b0e994a45492bc32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "control", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="standard")
    def standard(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standard"))

    @standard.setter
    def standard(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4066bb91cb535979fecbfcfbfdfeb578cbd417f815ee582d181354bd8e29d799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesComplianceStandards]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesComplianceStandards]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesComplianceStandards]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98ef5839e6225507db169f2fff2fe928d15dceb275c1709fc36a54f1f4e5c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraint",
    jsii_struct_bases=[],
    name_mapping={
        "org_policy_constraint": "orgPolicyConstraint",
        "org_policy_constraint_custom": "orgPolicyConstraintCustom",
        "security_health_analytics_custom_module": "securityHealthAnalyticsCustomModule",
        "security_health_analytics_module": "securityHealthAnalyticsModule",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraint:
    def __init__(
        self,
        *,
        org_policy_constraint: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint", typing.Dict[builtins.str, typing.Any]]] = None,
        org_policy_constraint_custom: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom", typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_custom_module: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule", typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_module: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param org_policy_constraint: org_policy_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#org_policy_constraint SecurityposturePosture#org_policy_constraint}
        :param org_policy_constraint_custom: org_policy_constraint_custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#org_policy_constraint_custom SecurityposturePosture#org_policy_constraint_custom}
        :param security_health_analytics_custom_module: security_health_analytics_custom_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#security_health_analytics_custom_module SecurityposturePosture#security_health_analytics_custom_module}
        :param security_health_analytics_module: security_health_analytics_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#security_health_analytics_module SecurityposturePosture#security_health_analytics_module}
        '''
        if isinstance(org_policy_constraint, dict):
            org_policy_constraint = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint(**org_policy_constraint)
        if isinstance(org_policy_constraint_custom, dict):
            org_policy_constraint_custom = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom(**org_policy_constraint_custom)
        if isinstance(security_health_analytics_custom_module, dict):
            security_health_analytics_custom_module = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule(**security_health_analytics_custom_module)
        if isinstance(security_health_analytics_module, dict):
            security_health_analytics_module = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule(**security_health_analytics_module)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fcb805adfcb0aff4464dbc6fa54975f3452b1763272fd102f2d5de82a6142ea)
            check_type(argname="argument org_policy_constraint", value=org_policy_constraint, expected_type=type_hints["org_policy_constraint"])
            check_type(argname="argument org_policy_constraint_custom", value=org_policy_constraint_custom, expected_type=type_hints["org_policy_constraint_custom"])
            check_type(argname="argument security_health_analytics_custom_module", value=security_health_analytics_custom_module, expected_type=type_hints["security_health_analytics_custom_module"])
            check_type(argname="argument security_health_analytics_module", value=security_health_analytics_module, expected_type=type_hints["security_health_analytics_module"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if org_policy_constraint is not None:
            self._values["org_policy_constraint"] = org_policy_constraint
        if org_policy_constraint_custom is not None:
            self._values["org_policy_constraint_custom"] = org_policy_constraint_custom
        if security_health_analytics_custom_module is not None:
            self._values["security_health_analytics_custom_module"] = security_health_analytics_custom_module
        if security_health_analytics_module is not None:
            self._values["security_health_analytics_module"] = security_health_analytics_module

    @builtins.property
    def org_policy_constraint(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint"]:
        '''org_policy_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#org_policy_constraint SecurityposturePosture#org_policy_constraint}
        '''
        result = self._values.get("org_policy_constraint")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint"], result)

    @builtins.property
    def org_policy_constraint_custom(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom"]:
        '''org_policy_constraint_custom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#org_policy_constraint_custom SecurityposturePosture#org_policy_constraint_custom}
        '''
        result = self._values.get("org_policy_constraint_custom")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom"], result)

    @builtins.property
    def security_health_analytics_custom_module(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"]:
        '''security_health_analytics_custom_module block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#security_health_analytics_custom_module SecurityposturePosture#security_health_analytics_custom_module}
        '''
        result = self._values.get("security_health_analytics_custom_module")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"], result)

    @builtins.property
    def security_health_analytics_module(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"]:
        '''security_health_analytics_module block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#security_health_analytics_module SecurityposturePosture#security_health_analytics_module}
        '''
        result = self._values.get("security_health_analytics_module")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint",
    jsii_struct_bases=[],
    name_mapping={
        "canned_constraint_id": "cannedConstraintId",
        "policy_rules": "policyRules",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint:
    def __init__(
        self,
        *,
        canned_constraint_id: builtins.str,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param canned_constraint_id: Organization policy canned constraint Id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#canned_constraint_id SecurityposturePosture#canned_constraint_id}
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_rules SecurityposturePosture#policy_rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d6ed0649dffde771f2c17dfcd719dcaa8e1210d716946e3a31e7d97d2a5972)
            check_type(argname="argument canned_constraint_id", value=canned_constraint_id, expected_type=type_hints["canned_constraint_id"])
            check_type(argname="argument policy_rules", value=policy_rules, expected_type=type_hints["policy_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "canned_constraint_id": canned_constraint_id,
            "policy_rules": policy_rules,
        }

    @builtins.property
    def canned_constraint_id(self) -> builtins.str:
        '''Organization policy canned constraint Id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#canned_constraint_id SecurityposturePosture#canned_constraint_id}
        '''
        result = self._values.get("canned_constraint_id")
        assert result is not None, "Required property 'canned_constraint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]]:
        '''policy_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_rules SecurityposturePosture#policy_rules}
        '''
        result = self._values.get("policy_rules")
        assert result is not None, "Required property 'policy_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom",
    jsii_struct_bases=[],
    name_mapping={
        "policy_rules": "policyRules",
        "custom_constraint": "customConstraint",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom:
    def __init__(
        self,
        *,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        custom_constraint: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_rules SecurityposturePosture#policy_rules}
        :param custom_constraint: custom_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#custom_constraint SecurityposturePosture#custom_constraint}
        '''
        if isinstance(custom_constraint, dict):
            custom_constraint = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint(**custom_constraint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa3a7254b01645b28d380d7f9396f940c85c1eb4834fd1a86016d9c0dee4eae)
            check_type(argname="argument policy_rules", value=policy_rules, expected_type=type_hints["policy_rules"])
            check_type(argname="argument custom_constraint", value=custom_constraint, expected_type=type_hints["custom_constraint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_rules": policy_rules,
        }
        if custom_constraint is not None:
            self._values["custom_constraint"] = custom_constraint

    @builtins.property
    def policy_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]]:
        '''policy_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_rules SecurityposturePosture#policy_rules}
        '''
        result = self._values.get("policy_rules")
        assert result is not None, "Required property 'policy_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]], result)

    @builtins.property
    def custom_constraint(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint"]:
        '''custom_constraint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#custom_constraint SecurityposturePosture#custom_constraint}
        '''
        result = self._values.get("custom_constraint")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint",
    jsii_struct_bases=[],
    name_mapping={
        "action_type": "actionType",
        "condition": "condition",
        "method_types": "methodTypes",
        "name": "name",
        "resource_types": "resourceTypes",
        "description": "description",
        "display_name": "displayName",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint:
    def __init__(
        self,
        *,
        action_type: builtins.str,
        condition: builtins.str,
        method_types: typing.Sequence[builtins.str],
        name: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_type: The action to take if the condition is met. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#action_type SecurityposturePosture#action_type}
        :param condition: A CEL condition that refers to a supported service resource, for example 'resource.management.autoUpgrade == false'. For details about CEL usage, see `Common Expression Language <https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        :param method_types: A list of RESTful methods for which to enforce the constraint. Can be 'CREATE', 'UPDATE', or both. Not all Google Cloud services support both methods. To see supported methods for each service, find the service in `Supported services <https://cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#method_types SecurityposturePosture#method_types}
        :param name: Immutable. The name of the custom constraint. This is unique within the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#name SecurityposturePosture#name}
        :param resource_types: Immutable. The fully qualified name of the Google Cloud REST resource containing the object and field you want to restrict. For example, 'container.googleapis.com/NodePool'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_types SecurityposturePosture#resource_types}
        :param description: A human-friendly description of the constraint to display as an error message when the policy is violated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param display_name: A human-friendly name for the constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#display_name SecurityposturePosture#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52598a7a3bb4b9822e154263e3e3ffc7640b15172e8c0cc92866ae8b23acc323)
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument method_types", value=method_types, expected_type=type_hints["method_types"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_type": action_type,
            "condition": condition,
            "method_types": method_types,
            "name": name,
            "resource_types": resource_types,
        }
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def action_type(self) -> builtins.str:
        '''The action to take if the condition is met. Possible values: ["ALLOW", "DENY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#action_type SecurityposturePosture#action_type}
        '''
        result = self._values.get("action_type")
        assert result is not None, "Required property 'action_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> builtins.str:
        '''A CEL condition that refers to a supported service resource, for example 'resource.management.autoUpgrade == false'. For details about CEL usage, see `Common Expression Language <https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def method_types(self) -> typing.List[builtins.str]:
        '''A list of RESTful methods for which to enforce the constraint.

        Can be 'CREATE', 'UPDATE', or both. Not all Google Cloud services support both methods. To see supported methods for each service, find the service in `Supported services <https://cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#method_types SecurityposturePosture#method_types}
        '''
        result = self._values.get("method_types")
        assert result is not None, "Required property 'method_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Immutable. The name of the custom constraint. This is unique within the organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#name SecurityposturePosture#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''Immutable.

        The fully qualified name of the Google Cloud REST resource containing the object and field you want to restrict. For example, 'container.googleapis.com/NodePool'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_types SecurityposturePosture#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-friendly description of the constraint to display as an error message when the policy is violated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A human-friendly name for the constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#display_name SecurityposturePosture#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__661a6b64c019512ab23d021ac4d63ac942877aa2d8e1d369eda5b8cd86bbd885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="actionTypeInput")
    def action_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="methodTypesInput")
    def method_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionType"))

    @action_type.setter
    def action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d731aaa451387b1bef6184e50866b31f9d8dce20229a89eea2a32962269936dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc8b114cc5fe053fdd408d99054c0a6289dab6de93e1b2b5b47b5fe18ed054d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0cbbdba82ade89111baab5bbf649dd1601fb6f99ab627e0c7e5cd636214604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdd9cc29d809730d54cb15734c785e2eff60a825347d692550dc8bd4c741942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="methodTypes")
    def method_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methodTypes"))

    @method_types.setter
    def method_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7c6e4aa5c39a2b21f2c2aedbe9622f98cfaddc3a58b232723c74dddc36fd55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methodTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89085134a7e59f07e660493644b9c3de1a1646b90589466ca437e615bd14ee21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0234b49f828126101aed35e1f91aa41c07897d6a28a0c37d044f1aab30f21e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58338433e51143478249f23454cd6b48c50695466b1959b280b53a689df1c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38441e824e690dbd4364a05e1c563839d493ece1a14cc01aeb44344a9c08a404)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomConstraint")
    def put_custom_constraint(
        self,
        *,
        action_type: builtins.str,
        condition: builtins.str,
        method_types: typing.Sequence[builtins.str],
        name: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_type: The action to take if the condition is met. Possible values: ["ALLOW", "DENY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#action_type SecurityposturePosture#action_type}
        :param condition: A CEL condition that refers to a supported service resource, for example 'resource.management.autoUpgrade == false'. For details about CEL usage, see `Common Expression Language <https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-custom-constraints#common_expression_language>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        :param method_types: A list of RESTful methods for which to enforce the constraint. Can be 'CREATE', 'UPDATE', or both. Not all Google Cloud services support both methods. To see supported methods for each service, find the service in `Supported services <https://cloud.google.com/resource-manager/docs/organization-policy/custom-constraint-supported-services>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#method_types SecurityposturePosture#method_types}
        :param name: Immutable. The name of the custom constraint. This is unique within the organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#name SecurityposturePosture#name}
        :param resource_types: Immutable. The fully qualified name of the Google Cloud REST resource containing the object and field you want to restrict. For example, 'container.googleapis.com/NodePool'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_types SecurityposturePosture#resource_types}
        :param description: A human-friendly description of the constraint to display as an error message when the policy is violated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param display_name: A human-friendly name for the constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#display_name SecurityposturePosture#display_name}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint(
            action_type=action_type,
            condition=condition,
            method_types=method_types,
            name=name,
            resource_types=resource_types,
            description=description,
            display_name=display_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConstraint", [value]))

    @jsii.member(jsii_name="putPolicyRules")
    def put_policy_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1f5cb1659f8d94ad1b2a4a92a40da15b53c0a0b6b5e973e2a465a52ac8134d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyRules", [value]))

    @jsii.member(jsii_name="resetCustomConstraint")
    def reset_custom_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConstraint", []))

    @builtins.property
    @jsii.member(jsii_name="customConstraint")
    def custom_constraint(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference, jsii.get(self, "customConstraint"))

    @builtins.property
    @jsii.member(jsii_name="policyRules")
    def policy_rules(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList", jsii.get(self, "policyRules"))

    @builtins.property
    @jsii.member(jsii_name="customConstraintInput")
    def custom_constraint_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint], jsii.get(self, "customConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="policyRulesInput")
    def policy_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules"]]], jsii.get(self, "policyRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2900579a31a91355e1a7c532432fb6d26695a5e84894a62ee1044c5f07613d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all": "allowAll",
        "condition": "condition",
        "deny_all": "denyAll",
        "enforce": "enforce",
        "values": "values",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        condition: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to true means that all values are allowed. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allow_all SecurityposturePosture#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        :param deny_all: Setting this to true means that all values are denied. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#deny_all SecurityposturePosture#deny_all}
        :param enforce: If 'true', then the policy is enforced. If 'false', then any configuration is acceptable. This field can be set only in policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#enforce SecurityposturePosture#enforce}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#values SecurityposturePosture#values}
        '''
        if isinstance(condition, dict):
            condition = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition(**condition)
        if isinstance(values, dict):
            values = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80a68d3c749857f6043be04736d4aa1caedb1182bb257861c9e4b59223f3340)
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument deny_all", value=deny_all, expected_type=type_hints["deny_all"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if condition is not None:
            self._values["condition"] = condition
        if deny_all is not None:
            self._values["deny_all"] = deny_all
        if enforce is not None:
            self._values["enforce"] = enforce
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def allow_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are allowed.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allow_all SecurityposturePosture#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition"], result)

    @builtins.property
    def deny_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are denied.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#deny_all SecurityposturePosture#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', then the policy is enforced.

        If 'false', then any configuration is acceptable.
        This field can be set only in policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#enforce SecurityposturePosture#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#values SecurityposturePosture#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda938d617df209eb6d3b6683c89bb6ecf2214eafe25c01bf11ffb0c1eb655c1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b81171792c0a1f083230e2a69d6c9f8ba3c0afbeebc8cb770bc1ad4b88ddaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55e3e4c240c27053b42f0f7e7429659b678faa0ec1c86711c970d1eb3de75db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf32f320b08b4ac363859e2e6b23411254da0fa709d0535d04575818065825da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f58a9c5f573c58e351222b2d7d14395b2fbdae3856f4b35aeb43de4a22882fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5b5ef621d15ff100704cdc30dc1c5d5b3d37954b494ef95fd416375d41f023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5de77b82d11dad5b4ebdb7e974908b76a8b53ef14129baadd45b192d9d64a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ee38d52f9f343b115806ccaf9a91742d939cc3e82d65c4f28bc79ecd82df03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d8b7a62210bafe75860ec60f04da90999bedd06181eff68d757d25fbed12ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54f7742fb4259139757e8b5f1f56b2c036725ed287c0c656ad5569ee5f36a48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d39da1dfc79f3aa85f5a104a0cf70461206952c11b9212703c06e61f361818f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c49e6edd3d042e23dd466f9c31000d77d2e15d31b0f54cb7f7cd7bb62cc1737a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d73a416ba5485d204fe891c5a22332fba755299fd9dd6fca1d051462e88c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf10b0844466173652854ab00739a9f69ec70416d952bbcdf16f36f90c5ca823)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allowed_values SecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#denied_values SecurityposturePosture#denied_values}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues(
            allowed_values=allowed_values, denied_values=denied_values
        )

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDenyAll")
    def reset_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyAll", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="denyAllInput")
    def deny_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "denyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues"], jsii.get(self, "valuesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e62a448cd174c17cb49e4f98ad3115e6611de1fcdc7d87735389d9032d043c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473f5ec8eee6a4de4950b8cbf2a9ed2c5df67ee26c15cedef4d9818ea7650a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce41fbb9372096bb12ecc65423b5305c954aaf158b56432b79d4062148ea393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa3c667f48a08008097dc45c39692f87dfb9fcbe35b20f0262200b9b1a74402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allowed_values SecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#denied_values SecurityposturePosture#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757ffe0ad3788e381c475a590ddcad968dd42d050bb5966fa048a62b869753a8)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument denied_values", value=denied_values, expected_type=type_hints["denied_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if denied_values is not None:
            self._values["denied_values"] = denied_values

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values allowed at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allowed_values SecurityposturePosture#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#denied_values SecurityposturePosture#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a0001f257623544618585d3ef5dc4e73975ed1f09b32026e2b78ca19004b6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedValues")
    def reset_allowed_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedValues", []))

    @jsii.member(jsii_name="resetDeniedValues")
    def reset_denied_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedValues", []))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedValuesInput")
    def denied_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedValues"))

    @allowed_values.setter
    def allowed_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee04d672684a850af9e3121a4f455f7dd10f9a191ef54684c152ce2552d386c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a42a38846f4ff38523d0e0347514f385bdbc52d6620ac965a40d5dad453d872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b7c42f1b1c56b0090a68294c03ccbb008d7a987c6abe3c10732ee11f46e930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8193d56e737b6f8df76a1a2c35536388461a8934ace8ecd48e2356266305fd0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPolicyRules")
    def put_policy_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8be0c42e20f3ac9b554e460ce8e5eed68b6042bb5e2eabffc6c9af0543260a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyRules", [value]))

    @builtins.property
    @jsii.member(jsii_name="policyRules")
    def policy_rules(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList", jsii.get(self, "policyRules"))

    @builtins.property
    @jsii.member(jsii_name="cannedConstraintIdInput")
    def canned_constraint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedConstraintIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyRulesInput")
    def policy_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules"]]], jsii.get(self, "policyRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedConstraintId")
    def canned_constraint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedConstraintId"))

    @canned_constraint_id.setter
    def canned_constraint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f9f2fa7dc3108a38f4e6f156ff59b5d3cf82a8b26ddb58ec70cab29db3ab70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedConstraintId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c124a3466d6df169c72b89a7a3fcb5d17a6c876b6256ec56050fee873bc2cf99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all": "allowAll",
        "condition": "condition",
        "deny_all": "denyAll",
        "enforce": "enforce",
        "values": "values",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules:
    def __init__(
        self,
        *,
        allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        condition: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_all: Setting this to true means that all values are allowed. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allow_all SecurityposturePosture#allow_all}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        :param deny_all: Setting this to true means that all values are denied. This field can be set only in policies for list constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#deny_all SecurityposturePosture#deny_all}
        :param enforce: If 'true', then the policy is enforced. If 'false', then any configuration is acceptable. This field can be set only in policies for boolean constraints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#enforce SecurityposturePosture#enforce}
        :param values: values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#values SecurityposturePosture#values}
        '''
        if isinstance(condition, dict):
            condition = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition(**condition)
        if isinstance(values, dict):
            values = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues(**values)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7077c4881b6c28b88600dc0712948eba6416f61efab7caa668a91af8f1847e)
            check_type(argname="argument allow_all", value=allow_all, expected_type=type_hints["allow_all"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument deny_all", value=deny_all, expected_type=type_hints["deny_all"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all is not None:
            self._values["allow_all"] = allow_all
        if condition is not None:
            self._values["condition"] = condition
        if deny_all is not None:
            self._values["deny_all"] = deny_all
        if enforce is not None:
            self._values["enforce"] = enforce
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def allow_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are allowed.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allow_all SecurityposturePosture#allow_all}
        '''
        result = self._values.get("allow_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#condition SecurityposturePosture#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition"], result)

    @builtins.property
    def deny_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to true means that all values are denied.

        This field can be set only in policies for list constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#deny_all SecurityposturePosture#deny_all}
        '''
        result = self._values.get("deny_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If 'true', then the policy is enforced.

        If 'false', then any configuration is acceptable.
        This field can be set only in policies for boolean constraints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#enforce SecurityposturePosture#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"]:
        '''values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#values SecurityposturePosture#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5104ee763db7378525f242674f3804b98977544f86c5d395e8fc22a1c269c82a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d984ad8b2fd894a2a2909ee88bc707bbdeb23db86a9e90ad5ff212ec7f1e60ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d326b81f092a23bbba727649093682a07f9e5530b88adfb6f64068f5c0234209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c111f01c1dd6f5afcab97d150db4b34ce3db80b8f9cf67a8d74be87b600e9be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a646160faafd817710d404893330a57da621569dbe44fc62bf484b6f0a7c1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ec66ca63de8ba8eef35bdfda76dca63fb37f39a53e7843d895db8395e46c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5539f041882c34755a756ba085398de7345b1a63c325ccc643f9033f0cf878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__757bcecd5de4378be374b382316a23cd30e6fc2e845600e1f4436a4e6516689d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4d2176971578f2aabb1640e36bb21f642a1d8801d1e4bc95632de8d401bc4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b94576db7b67d87ffa1af85b0236d5c5d827450f58c244e244a2b684c5bb8be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ec42370f470cdbd54fc7b7ff7933a23f32b1303abef3aa3587e87b4e426f48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1588aaf90580a96003ac0003e25bb5d74bf6b54ee412fbcd0ce11258870b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec60cbadad4745dcb8705f4a0787f12073b307dd94f7eecd9d4c7e08077b37f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56bece96c43427455e55f73ed6a053cca4ae1bc09227f933e738355bf059e85a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putValues")
    def put_values(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allowed_values SecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#denied_values SecurityposturePosture#denied_values}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues(
            allowed_values=allowed_values, denied_values=denied_values
        )

        return typing.cast(None, jsii.invoke(self, "putValues", [value]))

    @jsii.member(jsii_name="resetAllowAll")
    def reset_allow_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAll", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDenyAll")
    def reset_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyAll", []))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference", jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="allowAllInput")
    def allow_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="denyAllInput")
    def deny_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "denyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues"], jsii.get(self, "valuesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__873caab7302f750fa588624d8edca9afbb98a8bb28a338a7d15be7fe507d0084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="denyAll")
    def deny_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "denyAll"))

    @deny_all.setter
    def deny_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764712dddfc4cced4636d237716a1d3f2b09eb6dd8d227605af04475e348e5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46a863ebb9bc15b5204c060be9c47f1e56dc0fc7679808f37c952a937902115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6261b801a86c4c9887bf0a7103f90baf5783bce273c7e344ef70ffc899a93986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues", "denied_values": "deniedValues"},
)
class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues:
    def __init__(
        self,
        *,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_values: List of values allowed at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allowed_values SecurityposturePosture#allowed_values}
        :param denied_values: List of values denied at this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#denied_values SecurityposturePosture#denied_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2117ff008fe59ed40cd970624068d654752ce6a8ee34898f63b443a99c2060f0)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument denied_values", value=denied_values, expected_type=type_hints["denied_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if denied_values is not None:
            self._values["denied_values"] = denied_values

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values allowed at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#allowed_values SecurityposturePosture#allowed_values}
        '''
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def denied_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values denied at this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#denied_values SecurityposturePosture#denied_values}
        '''
        result = self._values.get("denied_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a15e1a977f3908f102588e6836b557d07f7486da9e6220e69c9626fb6799c62a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedValues")
    def reset_allowed_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedValues", []))

    @jsii.member(jsii_name="resetDeniedValues")
    def reset_denied_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeniedValues", []))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="deniedValuesInput")
    def denied_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deniedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedValues"))

    @allowed_values.setter
    def allowed_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f54759daec6d13e6c498d210edf8ccec2190a42d9ea4dd0d38ad21e28a8add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deniedValues")
    def denied_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deniedValues"))

    @denied_values.setter
    def denied_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7133a08fa4308479a6a532be43a2f5b313acb5e0b75719efb2feaeb14740cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deniedValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000ad7a4580e298da4e8d2718889f92a402be82fda8c7ae4999a7744cc105cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96e718f423c2eb47b0631c557b4b2463a9d4ea94274e0f1a80ae68966944767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOrgPolicyConstraint")
    def put_org_policy_constraint(
        self,
        *,
        canned_constraint_id: builtins.str,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param canned_constraint_id: Organization policy canned constraint Id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#canned_constraint_id SecurityposturePosture#canned_constraint_id}
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_rules SecurityposturePosture#policy_rules}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint(
            canned_constraint_id=canned_constraint_id, policy_rules=policy_rules
        )

        return typing.cast(None, jsii.invoke(self, "putOrgPolicyConstraint", [value]))

    @jsii.member(jsii_name="putOrgPolicyConstraintCustom")
    def put_org_policy_constraint_custom(
        self,
        *,
        policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
        custom_constraint: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param policy_rules: policy_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#policy_rules SecurityposturePosture#policy_rules}
        :param custom_constraint: custom_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#custom_constraint SecurityposturePosture#custom_constraint}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom(
            policy_rules=policy_rules, custom_constraint=custom_constraint
        )

        return typing.cast(None, jsii.invoke(self, "putOrgPolicyConstraintCustom", [value]))

    @jsii.member(jsii_name="putSecurityHealthAnalyticsCustomModule")
    def put_security_health_analytics_custom_module(
        self,
        *,
        config: typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: typing.Optional[builtins.str] = None,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#config SecurityposturePosture#config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#display_name SecurityposturePosture#display_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_enablement_state SecurityposturePosture#module_enablement_state}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule(
            config=config,
            display_name=display_name,
            module_enablement_state=module_enablement_state,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHealthAnalyticsCustomModule", [value]))

    @jsii.member(jsii_name="putSecurityHealthAnalyticsModule")
    def put_security_health_analytics_module(
        self,
        *,
        module_name: builtins.str,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module_name: The name of the module eg: BIGQUERY_TABLE_CMEK_DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_name SecurityposturePosture#module_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_enablement_state SecurityposturePosture#module_enablement_state}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule(
            module_name=module_name, module_enablement_state=module_enablement_state
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityHealthAnalyticsModule", [value]))

    @jsii.member(jsii_name="resetOrgPolicyConstraint")
    def reset_org_policy_constraint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgPolicyConstraint", []))

    @jsii.member(jsii_name="resetOrgPolicyConstraintCustom")
    def reset_org_policy_constraint_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgPolicyConstraintCustom", []))

    @jsii.member(jsii_name="resetSecurityHealthAnalyticsCustomModule")
    def reset_security_health_analytics_custom_module(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHealthAnalyticsCustomModule", []))

    @jsii.member(jsii_name="resetSecurityHealthAnalyticsModule")
    def reset_security_health_analytics_module(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityHealthAnalyticsModule", []))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraint")
    def org_policy_constraint(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference, jsii.get(self, "orgPolicyConstraint"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraintCustom")
    def org_policy_constraint_custom(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference, jsii.get(self, "orgPolicyConstraintCustom"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsCustomModule")
    def security_health_analytics_custom_module(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference", jsii.get(self, "securityHealthAnalyticsCustomModule"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsModule")
    def security_health_analytics_module(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference", jsii.get(self, "securityHealthAnalyticsModule"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraintCustomInput")
    def org_policy_constraint_custom_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom], jsii.get(self, "orgPolicyConstraintCustomInput"))

    @builtins.property
    @jsii.member(jsii_name="orgPolicyConstraintInput")
    def org_policy_constraint_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint], jsii.get(self, "orgPolicyConstraintInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsCustomModuleInput")
    def security_health_analytics_custom_module_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule"], jsii.get(self, "securityHealthAnalyticsCustomModuleInput"))

    @builtins.property
    @jsii.member(jsii_name="securityHealthAnalyticsModuleInput")
    def security_health_analytics_module_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule"], jsii.get(self, "securityHealthAnalyticsModuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraint]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304ff7769f9ed6b2b24117fccff1f0749ea0a27b7d641b82b99df380ed0ac607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "display_name": "displayName",
        "module_enablement_state": "moduleEnablementState",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule:
    def __init__(
        self,
        *,
        config: typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: typing.Optional[builtins.str] = None,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#config SecurityposturePosture#config}
        :param display_name: The display name of the Security Health Analytics custom module. This display name becomes the finding category for all findings that are returned by this custom module. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#display_name SecurityposturePosture#display_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_enablement_state SecurityposturePosture#module_enablement_state}
        '''
        if isinstance(config, dict):
            config = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba681072f67bfc61e90b1b50203341556214a6ad2588355d347c5e5f82c256f5)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument module_enablement_state", value=module_enablement_state, expected_type=type_hints["module_enablement_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if module_enablement_state is not None:
            self._values["module_enablement_state"] = module_enablement_state

    @builtins.property
    def config(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#config SecurityposturePosture#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig", result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Security Health Analytics custom module.

        This
        display name becomes the finding category for all findings that are
        returned by this custom module.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#display_name SecurityposturePosture#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_enablement_state(self) -> typing.Optional[builtins.str]:
        '''The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_enablement_state SecurityposturePosture#module_enablement_state}
        '''
        result = self._values.get("module_enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "predicate": "predicate",
        "resource_selector": "resourceSelector",
        "severity": "severity",
        "custom_output": "customOutput",
        "description": "description",
        "recommendation": "recommendation",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig:
    def __init__(
        self,
        *,
        predicate: typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate", typing.Dict[builtins.str, typing.Any]],
        resource_selector: typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector", typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        recommendation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#predicate SecurityposturePosture#predicate}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_selector SecurityposturePosture#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["SEVERITY_UNSPECIFIED", "CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#severity SecurityposturePosture#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#custom_output SecurityposturePosture#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#recommendation SecurityposturePosture#recommendation}
        '''
        if isinstance(predicate, dict):
            predicate = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate(**predicate)
        if isinstance(resource_selector, dict):
            resource_selector = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector(**resource_selector)
        if isinstance(custom_output, dict):
            custom_output = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput(**custom_output)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f61f57fa89b3d58f9450ea851288ffd7c2cebd7f8a375a083f94a48f9de98bc)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument resource_selector", value=resource_selector, expected_type=type_hints["resource_selector"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument custom_output", value=custom_output, expected_type=type_hints["custom_output"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument recommendation", value=recommendation, expected_type=type_hints["recommendation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "predicate": predicate,
            "resource_selector": resource_selector,
            "severity": severity,
        }
        if custom_output is not None:
            self._values["custom_output"] = custom_output
        if description is not None:
            self._values["description"] = description
        if recommendation is not None:
            self._values["recommendation"] = recommendation

    @builtins.property
    def predicate(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate":
        '''predicate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#predicate SecurityposturePosture#predicate}
        '''
        result = self._values.get("predicate")
        assert result is not None, "Required property 'predicate' is missing"
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate", result)

    @builtins.property
    def resource_selector(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector":
        '''resource_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_selector SecurityposturePosture#resource_selector}
        '''
        result = self._values.get("resource_selector")
        assert result is not None, "Required property 'resource_selector' is missing"
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector", result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''The severity to assign to findings generated by the module. Possible values: ["SEVERITY_UNSPECIFIED", "CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#severity SecurityposturePosture#severity}
        '''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_output(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput"]:
        '''custom_output block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#custom_output SecurityposturePosture#custom_output}
        '''
        result = self._values.get("custom_output")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text that describes the vulnerability or misconfiguration that the custom module detects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recommendation(self) -> typing.Optional[builtins.str]:
        '''An explanation of the recommended steps that security teams can take to resolve the detected issue.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#recommendation SecurityposturePosture#recommendation}
        '''
        result = self._values.get("recommendation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties"},
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput:
    def __init__(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#properties SecurityposturePosture#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b7a3dec091b5091cb2936b9058b2269c442cb56ac85544cbb99891508c98b1)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#properties SecurityposturePosture#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d034449625d40812def459e3e15eb24ab4f694be6e96e6362798abe09d17d02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098f2071efcf7a58367f9789164868fda662b6bc9a3a8ac6d158c01603b66038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties"]]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bdcde31d80eecc42d2897c84f8f6e27e09a07a700cf4c04da4129e8fd990797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value_expression": "valueExpression"},
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties:
    def __init__(
        self,
        *,
        name: builtins.str,
        value_expression: typing.Optional[typing.Union["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the property for the custom output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#name SecurityposturePosture#name}
        :param value_expression: value_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#value_expression SecurityposturePosture#value_expression}
        '''
        if isinstance(value_expression, dict):
            value_expression = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression(**value_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc521967c4177527b02b85a7380beb0a5a0aa9423014ec4177e49ddff69740b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value_expression", value=value_expression, expected_type=type_hints["value_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value_expression is not None:
            self._values["value_expression"] = value_expression

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the property for the custom output.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#name SecurityposturePosture#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_expression(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"]:
        '''value_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#value_expression SecurityposturePosture#value_expression}
        '''
        result = self._values.get("value_expression")
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03ef66d2a86443e55090141bd3baca2e91c173a70e9a64ae225d3790d9ca1d74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fa538cc3945a8aa0b092c16de80677b09ab3c1b3500c9c38c22593b986ff98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2eb614ed5ab5f8f7ba5a301f96093d651d0b24bebe67542ea3bdd88f29f6d2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__070bd3571a9cda787bb40f4c3a7214902ce1daa3d3e005a7eda3cfae4db44264)
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
            type_hints = typing.get_type_hints(_typecheckingstub__540711edc65ffb2c7d9847606d08756a61d5814c916397ecf32ff6c8821028a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9120194406692311c1898a61a33e1368c51f208200f1f9202f64dadc6a655ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5a26c2b00b774ae6183deefaebeb9f9cff0382168b3f12ddf29111211caa77e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueExpression")
    def put_value_expression(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putValueExpression", [value]))

    @jsii.member(jsii_name="resetValueExpression")
    def reset_value_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueExpression", []))

    @builtins.property
    @jsii.member(jsii_name="valueExpression")
    def value_expression(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference", jsii.get(self, "valueExpression"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueExpressionInput")
    def value_expression_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression"], jsii.get(self, "valueExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c475cd5c3ae7e67fb80f3be5be82bd16f8260e06c5a372a74239e63dc2f435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b403dd9f0171284326ce04fc8d8d9c98570372b812d375c7dae1a6ffd548902d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9f5d28fcc9a14492d6d29be0f2e543fd8980597f2af23dd5dd00e3a479879d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a18b63376c9798919ea27ec2fc6467eeffc676456e0640151a0b319fc34bbc3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff50e66ed842961eaed90fd5983b0f83d12552779cc431e613aee2b7d6ec6887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8ab4d5397322fc44f04e07df504471e5a2e4dc89bd3c647511cb2eeb830a86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0870b3a989c30a8657be35e16bf4eb35d43f38a995331f8bf93d38a06d99133a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e340408b367b1ecf232787749c58e030ae8b81719c77c0218abf220c69700a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497e70fc71479c6908662d60df98e6c7164658709845d51b4c2dbd1d2ea18c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e9ba2f05ab2b8d90871e652839131b3fe8ef380a4429e83487e51d4602e0541)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomOutput")
    def put_custom_output(
        self,
        *,
        properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#properties SecurityposturePosture#properties}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput(
            properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomOutput", [value]))

    @jsii.member(jsii_name="putPredicate")
    def put_predicate(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putPredicate", [value]))

    @jsii.member(jsii_name="putResourceSelector")
    def put_resource_selector(
        self,
        *,
        resource_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_types SecurityposturePosture#resource_types}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector(
            resource_types=resource_types
        )

        return typing.cast(None, jsii.invoke(self, "putResourceSelector", [value]))

    @jsii.member(jsii_name="resetCustomOutput")
    def reset_custom_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOutput", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRecommendation")
    def reset_recommendation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendation", []))

    @builtins.property
    @jsii.member(jsii_name="customOutput")
    def custom_output(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference, jsii.get(self, "customOutput"))

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference", jsii.get(self, "predicate"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelector")
    def resource_selector(
        self,
    ) -> "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference":
        return typing.cast("SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference", jsii.get(self, "resourceSelector"))

    @builtins.property
    @jsii.member(jsii_name="customOutputInput")
    def custom_output_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput], jsii.get(self, "customOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="predicateInput")
    def predicate_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate"], jsii.get(self, "predicateInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationInput")
    def recommendation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSelectorInput")
    def resource_selector_input(
        self,
    ) -> typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector"]:
        return typing.cast(typing.Optional["SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector"], jsii.get(self, "resourceSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2433dd72cd652d9f7a915605f05597405882fb6cfbf146942ef35fcdc494fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recommendation")
    def recommendation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendation"))

    @recommendation.setter
    def recommendation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9434e3e3c7aa6afecd5957a977c19120c0857fceba72d7c2abe8d9027d9bac79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe93e8b6534d2179943182dccb357929c20168774d46468691133ecea0da98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5353d6bcbf6e64af6e3d79a952bf0a8b7c1f624cecf511bb0f946294f4d8fe47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        :param description: Description of the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea175bbda693b014a7b75fdd6c03c0f2d145d4a70179995cf996399444d24217)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#expression SecurityposturePosture#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#location SecurityposturePosture#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#title SecurityposturePosture#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71774c375d7bed6968a89f0bfc9c679726bd36b7727e3abf7ac006e3432dbc4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b098675aa76670583e355cd01f149c6fbf67f807133c50871bb6b9c4f655c7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b84e44478357a7388753ea8a19c51970f0d57b56f5b6b27b9033d2507666dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee6590da7329dfa046e2e15514d0f4f6f60feed6f9cffd4ab880024dc04573c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4bce1e7b7a0793e94ca5433e224326ddbd5b6255d45d0632c74687f2c80aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce8581c719a8d2fb2b15dc2895787bcfd296cb09af9ff64a9434432492a62fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector:
    def __init__(self, *, resource_types: typing.Sequence[builtins.str]) -> None:
        '''
        :param resource_types: The resource types to run the detector on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_types SecurityposturePosture#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58648b1b09ee7235f05d97c28f01150a807a468cb1aca59a24a7e678f634c2b9)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_types": resource_types,
        }

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''The resource types to run the detector on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_types SecurityposturePosture#resource_types}
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1582deed4d573776af86048e9bb90f18440496b42f0e6efcaa66d1df4def7c59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b937c9bce6a9728615fce0f297acb7dc469274fb18bab6ed2dd4e5d25a18d86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef5ea9a4bee8071e60431f48e457c263420c11a972939aabe0f3bbfabc98db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f2c035039ebf7d7158c9fdca6f6870c2142ce5cf8f5e80dfa60120e4943ee73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        predicate: typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate, typing.Dict[builtins.str, typing.Any]],
        resource_selector: typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
        severity: builtins.str,
        custom_output: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        recommendation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param predicate: predicate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#predicate SecurityposturePosture#predicate}
        :param resource_selector: resource_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#resource_selector SecurityposturePosture#resource_selector}
        :param severity: The severity to assign to findings generated by the module. Possible values: ["SEVERITY_UNSPECIFIED", "CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#severity SecurityposturePosture#severity}
        :param custom_output: custom_output block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#custom_output SecurityposturePosture#custom_output}
        :param description: Text that describes the vulnerability or misconfiguration that the custom module detects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#description SecurityposturePosture#description}
        :param recommendation: An explanation of the recommended steps that security teams can take to resolve the detected issue. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#recommendation SecurityposturePosture#recommendation}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig(
            predicate=predicate,
            resource_selector=resource_selector,
            severity=severity,
            custom_output=custom_output,
            description=description,
            recommendation=recommendation,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetModuleEnablementState")
    def reset_module_enablement_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModuleEnablementState", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementStateInput")
    def module_enablement_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleEnablementStateInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8931f3f921a8c01a72064aaddc92fb5eee59aacbcaa32f6e7b79a80da3090de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementState")
    def module_enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleEnablementState"))

    @module_enablement_state.setter
    def module_enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66164880645640ecd857d3369df30f84f4916458ee6c3d26120107f9e573773e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleEnablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66bc707fee3396e9cc6ce816cc1c2deaba23073d2a09f57c8ba61d7b6dba750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule",
    jsii_struct_bases=[],
    name_mapping={
        "module_name": "moduleName",
        "module_enablement_state": "moduleEnablementState",
    },
)
class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule:
    def __init__(
        self,
        *,
        module_name: builtins.str,
        module_enablement_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param module_name: The name of the module eg: BIGQUERY_TABLE_CMEK_DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_name SecurityposturePosture#module_name}
        :param module_enablement_state: The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_enablement_state SecurityposturePosture#module_enablement_state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e18cc9fb4bb6b1113f3c1f5f6d30fc12f391c12c4794792eb644977f1e6f88)
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument module_enablement_state", value=module_enablement_state, expected_type=type_hints["module_enablement_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module_name": module_name,
        }
        if module_enablement_state is not None:
            self._values["module_enablement_state"] = module_enablement_state

    @builtins.property
    def module_name(self) -> builtins.str:
        '''The name of the module eg: BIGQUERY_TABLE_CMEK_DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_name SecurityposturePosture#module_name}
        '''
        result = self._values.get("module_name")
        assert result is not None, "Required property 'module_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def module_enablement_state(self) -> typing.Optional[builtins.str]:
        '''The state of enablement for the module at its level of the resource hierarchy. Possible values: ["ENABLEMENT_STATE_UNSPECIFIED", "ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#module_enablement_state SecurityposturePosture#module_enablement_state}
        '''
        result = self._values.get("module_enablement_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3303d7cc6888506a79e050af2afc4dd75e0bd662e854f5d726f43abad993d3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetModuleEnablementState")
    def reset_module_enablement_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModuleEnablementState", []))

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementStateInput")
    def module_enablement_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleEnablementStateInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleNameInput")
    def module_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleEnablementState")
    def module_enablement_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleEnablementState"))

    @module_enablement_state.setter
    def module_enablement_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ef52487e7a9c6490c0fc4f49cc2a090a76de2db4f71745d5341fd6edeae760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleEnablementState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="moduleName")
    def module_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleName"))

    @module_name.setter
    def module_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f36a4996567be1c22225aa442f15dd428bbac97c7e3a926a9e4ce0f5327c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "moduleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1012bea34c9302fe2aabb5081b3f1e1f5e5f66dba34fcf66419efdcb08b83f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da07c468523c27b888f2ebe89dbefae5eae5b4bd23e2a03d94cd3454461c157e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityposturePosturePolicySetsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96db00b05d116cd8127c52b68da3cac75ad34641cee16f9e6adcd1419265a149)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityposturePosturePolicySetsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229de05da84e46e72f7799f9f94665c050d9f98b922f71a5707d3cbf004b3e06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9635b20d5a0cf6cb2bc768613d82c203d4d61a7146b819f1b2cacd6394c4769)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a077bf1ba0dac6f0df0477ecdbbbffe3b6d3bdeb3d2491195253b4a1ee6f1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c594859bc4665612e2bcdb2216a5630b5b38adbbf6f5df05d524ad7adc2bea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityposturePosturePolicySetsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePosturePolicySetsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80120decd62933ba9f8da45c5f28c74fd956523e0d11b12a262f712149526ca1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putComplianceStandards")
    def put_compliance_standards(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesComplianceStandards, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc768823a3d5cdc7aee7bd5b4ff646be4a2f1c1dce3d5dd272aac54adc0d59ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComplianceStandards", [value]))

    @jsii.member(jsii_name="putConstraint")
    def put_constraint(
        self,
        *,
        org_policy_constraint: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
        org_policy_constraint_custom: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom, typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_custom_module: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule, typing.Dict[builtins.str, typing.Any]]] = None,
        security_health_analytics_module: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param org_policy_constraint: org_policy_constraint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#org_policy_constraint SecurityposturePosture#org_policy_constraint}
        :param org_policy_constraint_custom: org_policy_constraint_custom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#org_policy_constraint_custom SecurityposturePosture#org_policy_constraint_custom}
        :param security_health_analytics_custom_module: security_health_analytics_custom_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#security_health_analytics_custom_module SecurityposturePosture#security_health_analytics_custom_module}
        :param security_health_analytics_module: security_health_analytics_module block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#security_health_analytics_module SecurityposturePosture#security_health_analytics_module}
        '''
        value = SecurityposturePosturePolicySetsPoliciesConstraint(
            org_policy_constraint=org_policy_constraint,
            org_policy_constraint_custom=org_policy_constraint_custom,
            security_health_analytics_custom_module=security_health_analytics_custom_module,
            security_health_analytics_module=security_health_analytics_module,
        )

        return typing.cast(None, jsii.invoke(self, "putConstraint", [value]))

    @jsii.member(jsii_name="resetComplianceStandards")
    def reset_compliance_standards(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceStandards", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="complianceStandards")
    def compliance_standards(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesComplianceStandardsList:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesComplianceStandardsList, jsii.get(self, "complianceStandards"))

    @builtins.property
    @jsii.member(jsii_name="constraint")
    def constraint(
        self,
    ) -> SecurityposturePosturePolicySetsPoliciesConstraintOutputReference:
        return typing.cast(SecurityposturePosturePolicySetsPoliciesConstraintOutputReference, jsii.get(self, "constraint"))

    @builtins.property
    @jsii.member(jsii_name="complianceStandardsInput")
    def compliance_standards_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesComplianceStandards]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesComplianceStandards]]], jsii.get(self, "complianceStandardsInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintInput")
    def constraint_input(
        self,
    ) -> typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraint]:
        return typing.cast(typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraint], jsii.get(self, "constraintInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4f7d641db59c542d590bc10cc4f71db89c879e36c258d32c1c64f48bd3f19e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238b154c1747b75f1ade99bd0859a3001a8edd8f21dd5fa4404731577a1dbd58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2667e51aa0545e48acd2188a23067d11c5ce24ee1244ef7bbea8e71f0f8bc5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePostureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SecurityposturePostureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#create SecurityposturePosture#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#delete SecurityposturePosture#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#update SecurityposturePosture#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c66e3831f08480f8e684d847df1ec179a44af80da86227c277717f7d723c246)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#create SecurityposturePosture#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#delete SecurityposturePosture#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/securityposture_posture#update SecurityposturePosture#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityposturePostureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityposturePostureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.securityposturePosture.SecurityposturePostureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f16c3efaf08488a31f21b8cd1bd55c160f61fe026b690fc299a62f268dfcb16f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d538a0b51ef03252ad977954302e89762acaddbc53304bd18a2febb9c6392f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cb257621204f05e93df5ff072e3948b071e81b8bc0b95ebe2a7121e721ba54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d075996f627f5c29e293db5c1b6ac6a6b22ff07386cc32e0a297c6ff0062804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePostureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePostureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePostureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d38dfa764501b144ac9bd73766f110ce4cb3113ab8c7e79092b4974d3be6cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecurityposturePosture",
    "SecurityposturePostureConfig",
    "SecurityposturePosturePolicySets",
    "SecurityposturePosturePolicySetsList",
    "SecurityposturePosturePolicySetsOutputReference",
    "SecurityposturePosturePolicySetsPolicies",
    "SecurityposturePosturePolicySetsPoliciesComplianceStandards",
    "SecurityposturePosturePolicySetsPoliciesComplianceStandardsList",
    "SecurityposturePosturePolicySetsPoliciesComplianceStandardsOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraint",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraintOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesConditionOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesList",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValuesOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesConditionOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesList",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues",
    "SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValuesOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesList",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpressionOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicateOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelectorOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleOutputReference",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule",
    "SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModuleOutputReference",
    "SecurityposturePosturePolicySetsPoliciesList",
    "SecurityposturePosturePolicySetsPoliciesOutputReference",
    "SecurityposturePostureTimeouts",
    "SecurityposturePostureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7697c142bb0da4188491eeceb3c517e83d422abf7f68be60e33cfc4b09a0bd82(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    parent: builtins.str,
    policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySets, typing.Dict[builtins.str, typing.Any]]]],
    posture_id: builtins.str,
    state: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SecurityposturePostureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__71108f598f0ff47bd57a6382aab6d6298263f1971e7d29179e445f5eab403f95(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1779508c30a560ddecf0045c9dc9ce9a2c831d3d8d5c30c7768510b843052010(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbd4bc511d3081232bda0b91f55db09420d94cb159d62efdf748c815df81893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a7891f5bff187b08e34c613552fb7527dbde1d7cef1f52bc4ca793f15f30b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b62dda492e2a7b8c3350b6510f35789415e839e4fa9696fc18d6dec00b3269f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517aaac98bc69940dedd31c8e37d6fd31151d997a290c611fce824fcc9ed6dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb4dcf2aadd89d4954a54b831cae0273f594dc7f45253523815a22a2497249a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753b5201e0b4e735742505ce62038d62a4a61e026eaefc9c64a035cd04df00db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e744464e62ababea440ba6177a12fa7e78f88334c19836063cb613da103a564c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    parent: builtins.str,
    policy_sets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySets, typing.Dict[builtins.str, typing.Any]]]],
    posture_id: builtins.str,
    state: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SecurityposturePostureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158a0479c913000d5259fcf113f768bf6dfbdd791a0d5de6a4f9318927f2a100(
    *,
    policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    policy_set_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af61e90207089045e796002210733be9da9dabc951f75d475b9bd1d7c69870fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b628b2d6106e24262d4e6139547b46a423014d5c7dd016570dc1b36234f79bef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae44c867429877cb04e87a792448146a11ecc7fa4cfc3efd25cec5e03586f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8769dcab42fb08f8c382773117e94c6eb252131283f67b499dd01ec87f78a00a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096e2044fc641b08309d2735b1323cb85b9ce56d701431d4e0d0c721711dced3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16761b016933ec2e5961bf4dbe1f5a03dfedb49d3772dae89bfda107e7938791(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cdd3902add819b25db19cbec2693fb8158c604844a3960ac7d07bd2f41a3a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d066401ebc8239e58ffa7ae3590fa481143457ee1775de41216c18cb1d082b9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c0da95a64502faeb73c5cb5efc223424b91ce89cba551ff89f5efd8bbafb27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4127a407119fb824fc631ff5806e5360615e3dd1b756ba03cfcc47a49d2bd8a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abed790be5183b1e5fc67737b77bca5b3197137a45faed3c2d4eae5916d46788(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db2e503d18cb8959d2d353acfdd0903f66c1e576c4081c61cd5f9991ab94f09(
    *,
    constraint: typing.Union[SecurityposturePosturePolicySetsPoliciesConstraint, typing.Dict[builtins.str, typing.Any]],
    policy_id: builtins.str,
    compliance_standards: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesComplianceStandards, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4504f51b8bd3d117a46b91ef8269013f937b9213bd8410689194a52a20af603f(
    *,
    control: typing.Optional[builtins.str] = None,
    standard: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdda51542e23d72b50a6faaf7b016aa621394daa9049d331695c5c45bcfd8bcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718fa5cdc732b0ec71c25b3ffb7178eeff3c24507572f6a0632d5ae55999c829(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5fc48a305bf4d140f21fbf0582e3e11aa08871a143f1d0fb742fd3ffd2c160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9845170e9468b9513bad60f4361a3022916f6faf6cc6af2f8ceeb618e2ecc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96c4542986c8e27d5cb32d2ffdfbbed2e561cd20f99025f5f68e8114db88bba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fbf4da20d80fb2582201837a2cb6c707aeb0d28557e4fdac7d5f29849b5453(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesComplianceStandards]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37df75d2d59f546764dd50ea6bc47ec11ca750cfaea3bda8aaed40e0243a27e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1977caa240bbb8af320767d628aeaab518dcbd6c6b3a916b0e994a45492bc32b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4066bb91cb535979fecbfcfbfdfeb578cbd417f815ee582d181354bd8e29d799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98ef5839e6225507db169f2fff2fe928d15dceb275c1709fc36a54f1f4e5c2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesComplianceStandards]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcb805adfcb0aff4464dbc6fa54975f3452b1763272fd102f2d5de82a6142ea(
    *,
    org_policy_constraint: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
    org_policy_constraint_custom: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom, typing.Dict[builtins.str, typing.Any]]] = None,
    security_health_analytics_custom_module: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule, typing.Dict[builtins.str, typing.Any]]] = None,
    security_health_analytics_module: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d6ed0649dffde771f2c17dfcd719dcaa8e1210d716946e3a31e7d97d2a5972(
    *,
    canned_constraint_id: builtins.str,
    policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa3a7254b01645b28d380d7f9396f940c85c1eb4834fd1a86016d9c0dee4eae(
    *,
    policy_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    custom_constraint: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52598a7a3bb4b9822e154263e3e3ffc7640b15172e8c0cc92866ae8b23acc323(
    *,
    action_type: builtins.str,
    condition: builtins.str,
    method_types: typing.Sequence[builtins.str],
    name: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661a6b64c019512ab23d021ac4d63ac942877aa2d8e1d369eda5b8cd86bbd885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d731aaa451387b1bef6184e50866b31f9d8dce20229a89eea2a32962269936dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc8b114cc5fe053fdd408d99054c0a6289dab6de93e1b2b5b47b5fe18ed054d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0cbbdba82ade89111baab5bbf649dd1601fb6f99ab627e0c7e5cd636214604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdd9cc29d809730d54cb15734c785e2eff60a825347d692550dc8bd4c741942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7c6e4aa5c39a2b21f2c2aedbe9622f98cfaddc3a58b232723c74dddc36fd55(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89085134a7e59f07e660493644b9c3de1a1646b90589466ca437e615bd14ee21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0234b49f828126101aed35e1f91aa41c07897d6a28a0c37d044f1aab30f21e9d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58338433e51143478249f23454cd6b48c50695466b1959b280b53a689df1c78(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomCustomConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38441e824e690dbd4364a05e1c563839d493ece1a14cc01aeb44344a9c08a404(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1f5cb1659f8d94ad1b2a4a92a40da15b53c0a0b6b5e973e2a465a52ac8134d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2900579a31a91355e1a7c532432fb6d26695a5e84894a62ee1044c5f07613d8d(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80a68d3c749857f6043be04736d4aa1caedb1182bb257861c9e4b59223f3340(
    *,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    condition: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda938d617df209eb6d3b6683c89bb6ecf2214eafe25c01bf11ffb0c1eb655c1(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b81171792c0a1f083230e2a69d6c9f8ba3c0afbeebc8cb770bc1ad4b88ddaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e3e4c240c27053b42f0f7e7429659b678faa0ec1c86711c970d1eb3de75db6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf32f320b08b4ac363859e2e6b23411254da0fa709d0535d04575818065825da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f58a9c5f573c58e351222b2d7d14395b2fbdae3856f4b35aeb43de4a22882fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5b5ef621d15ff100704cdc30dc1c5d5b3d37954b494ef95fd416375d41f023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5de77b82d11dad5b4ebdb7e974908b76a8b53ef14129baadd45b192d9d64a7b(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ee38d52f9f343b115806ccaf9a91742d939cc3e82d65c4f28bc79ecd82df03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d8b7a62210bafe75860ec60f04da90999bedd06181eff68d757d25fbed12ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54f7742fb4259139757e8b5f1f56b2c036725ed287c0c656ad5569ee5f36a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d39da1dfc79f3aa85f5a104a0cf70461206952c11b9212703c06e61f361818f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49e6edd3d042e23dd466f9c31000d77d2e15d31b0f54cb7f7cd7bb62cc1737a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d73a416ba5485d204fe891c5a22332fba755299fd9dd6fca1d051462e88c3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf10b0844466173652854ab00739a9f69ec70416d952bbcdf16f36f90c5ca823(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62a448cd174c17cb49e4f98ad3115e6611de1fcdc7d87735389d9032d043c6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473f5ec8eee6a4de4950b8cbf2a9ed2c5df67ee26c15cedef4d9818ea7650a25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce41fbb9372096bb12ecc65423b5305c954aaf158b56432b79d4062148ea393(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa3c667f48a08008097dc45c39692f87dfb9fcbe35b20f0262200b9b1a74402(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757ffe0ad3788e381c475a590ddcad968dd42d050bb5966fa048a62b869753a8(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a0001f257623544618585d3ef5dc4e73975ed1f09b32026e2b78ca19004b6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee04d672684a850af9e3121a4f455f7dd10f9a191ef54684c152ce2552d386c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a42a38846f4ff38523d0e0347514f385bdbc52d6620ac965a40d5dad453d872(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b7c42f1b1c56b0090a68294c03ccbb008d7a987c6abe3c10732ee11f46e930(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintCustomPolicyRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8193d56e737b6f8df76a1a2c35536388461a8934ace8ecd48e2356266305fd0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8be0c42e20f3ac9b554e460ce8e5eed68b6042bb5e2eabffc6c9af0543260a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f9f2fa7dc3108a38f4e6f156ff59b5d3cf82a8b26ddb58ec70cab29db3ab70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c124a3466d6df169c72b89a7a3fcb5d17a6c876b6256ec56050fee873bc2cf99(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7077c4881b6c28b88600dc0712948eba6416f61efab7caa668a91af8f1847e(
    *,
    allow_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    condition: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5104ee763db7378525f242674f3804b98977544f86c5d395e8fc22a1c269c82a(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d984ad8b2fd894a2a2909ee88bc707bbdeb23db86a9e90ad5ff212ec7f1e60ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d326b81f092a23bbba727649093682a07f9e5530b88adfb6f64068f5c0234209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c111f01c1dd6f5afcab97d150db4b34ce3db80b8f9cf67a8d74be87b600e9be5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a646160faafd817710d404893330a57da621569dbe44fc62bf484b6f0a7c1fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ec66ca63de8ba8eef35bdfda76dca63fb37f39a53e7843d895db8395e46c40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5539f041882c34755a756ba085398de7345b1a63c325ccc643f9033f0cf878(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757bcecd5de4378be374b382316a23cd30e6fc2e845600e1f4436a4e6516689d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4d2176971578f2aabb1640e36bb21f642a1d8801d1e4bc95632de8d401bc4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b94576db7b67d87ffa1af85b0236d5c5d827450f58c244e244a2b684c5bb8be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ec42370f470cdbd54fc7b7ff7933a23f32b1303abef3aa3587e87b4e426f48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1588aaf90580a96003ac0003e25bb5d74bf6b54ee412fbcd0ce11258870b2e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec60cbadad4745dcb8705f4a0787f12073b307dd94f7eecd9d4c7e08077b37f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bece96c43427455e55f73ed6a053cca4ae1bc09227f933e738355bf059e85a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873caab7302f750fa588624d8edca9afbb98a8bb28a338a7d15be7fe507d0084(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764712dddfc4cced4636d237716a1d3f2b09eb6dd8d227605af04475e348e5e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46a863ebb9bc15b5204c060be9c47f1e56dc0fc7679808f37c952a937902115(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6261b801a86c4c9887bf0a7103f90baf5783bce273c7e344ef70ffc899a93986(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2117ff008fe59ed40cd970624068d654752ce6a8ee34898f63b443a99c2060f0(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    denied_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15e1a977f3908f102588e6836b557d07f7486da9e6220e69c9626fb6799c62a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f54759daec6d13e6c498d210edf8ccec2190a42d9ea4dd0d38ad21e28a8add(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7133a08fa4308479a6a532be43a2f5b313acb5e0b75719efb2feaeb14740cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000ad7a4580e298da4e8d2718889f92a402be82fda8c7ae4999a7744cc105cdb(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintOrgPolicyConstraintPolicyRulesValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96e718f423c2eb47b0631c557b4b2463a9d4ea94274e0f1a80ae68966944767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304ff7769f9ed6b2b24117fccff1f0749ea0a27b7d641b82b99df380ed0ac607(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba681072f67bfc61e90b1b50203341556214a6ad2588355d347c5e5f82c256f5(
    *,
    config: typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig, typing.Dict[builtins.str, typing.Any]],
    display_name: typing.Optional[builtins.str] = None,
    module_enablement_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f61f57fa89b3d58f9450ea851288ffd7c2cebd7f8a375a083f94a48f9de98bc(
    *,
    predicate: typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate, typing.Dict[builtins.str, typing.Any]],
    resource_selector: typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector, typing.Dict[builtins.str, typing.Any]],
    severity: builtins.str,
    custom_output: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    recommendation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b7a3dec091b5091cb2936b9058b2269c442cb56ac85544cbb99891508c98b1(
    *,
    properties: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d034449625d40812def459e3e15eb24ab4f694be6e96e6362798abe09d17d02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098f2071efcf7a58367f9789164868fda662b6bc9a3a8ac6d158c01603b66038(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdcde31d80eecc42d2897c84f8f6e27e09a07a700cf4c04da4129e8fd990797(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc521967c4177527b02b85a7380beb0a5a0aa9423014ec4177e49ddff69740b(
    *,
    name: builtins.str,
    value_expression: typing.Optional[typing.Union[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ef66d2a86443e55090141bd3baca2e91c173a70e9a64ae225d3790d9ca1d74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fa538cc3945a8aa0b092c16de80677b09ab3c1b3500c9c38c22593b986ff98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2eb614ed5ab5f8f7ba5a301f96093d651d0b24bebe67542ea3bdd88f29f6d2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070bd3571a9cda787bb40f4c3a7214902ce1daa3d3e005a7eda3cfae4db44264(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540711edc65ffb2c7d9847606d08756a61d5814c916397ecf32ff6c8821028a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9120194406692311c1898a61a33e1368c51f208200f1f9202f64dadc6a655ae8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a26c2b00b774ae6183deefaebeb9f9cff0382168b3f12ddf29111211caa77e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c475cd5c3ae7e67fb80f3be5be82bd16f8260e06c5a372a74239e63dc2f435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b403dd9f0171284326ce04fc8d8d9c98570372b812d375c7dae1a6ffd548902d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputProperties]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9f5d28fcc9a14492d6d29be0f2e543fd8980597f2af23dd5dd00e3a479879d(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18b63376c9798919ea27ec2fc6467eeffc676456e0640151a0b319fc34bbc3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff50e66ed842961eaed90fd5983b0f83d12552779cc431e613aee2b7d6ec6887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ab4d5397322fc44f04e07df504471e5a2e4dc89bd3c647511cb2eeb830a86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0870b3a989c30a8657be35e16bf4eb35d43f38a995331f8bf93d38a06d99133a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e340408b367b1ecf232787749c58e030ae8b81719c77c0218abf220c69700a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497e70fc71479c6908662d60df98e6c7164658709845d51b4c2dbd1d2ea18c23(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigCustomOutputPropertiesValueExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9ba2f05ab2b8d90871e652839131b3fe8ef380a4429e83487e51d4602e0541(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2433dd72cd652d9f7a915605f05597405882fb6cfbf146942ef35fcdc494fd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9434e3e3c7aa6afecd5957a977c19120c0857fceba72d7c2abe8d9027d9bac79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe93e8b6534d2179943182dccb357929c20168774d46468691133ecea0da98b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5353d6bcbf6e64af6e3d79a952bf0a8b7c1f624cecf511bb0f946294f4d8fe47(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea175bbda693b014a7b75fdd6c03c0f2d145d4a70179995cf996399444d24217(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71774c375d7bed6968a89f0bfc9c679726bd36b7727e3abf7ac006e3432dbc4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b098675aa76670583e355cd01f149c6fbf67f807133c50871bb6b9c4f655c7de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b84e44478357a7388753ea8a19c51970f0d57b56f5b6b27b9033d2507666dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee6590da7329dfa046e2e15514d0f4f6f60feed6f9cffd4ab880024dc04573c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4bce1e7b7a0793e94ca5433e224326ddbd5b6255d45d0632c74687f2c80aa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce8581c719a8d2fb2b15dc2895787bcfd296cb09af9ff64a9434432492a62fe(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigPredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58648b1b09ee7235f05d97c28f01150a807a468cb1aca59a24a7e678f634c2b9(
    *,
    resource_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1582deed4d573776af86048e9bb90f18440496b42f0e6efcaa66d1df4def7c59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b937c9bce6a9728615fce0f297acb7dc469274fb18bab6ed2dd4e5d25a18d86f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef5ea9a4bee8071e60431f48e457c263420c11a972939aabe0f3bbfabc98db4(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModuleConfigResourceSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2c035039ebf7d7158c9fdca6f6870c2142ce5cf8f5e80dfa60120e4943ee73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8931f3f921a8c01a72064aaddc92fb5eee59aacbcaa32f6e7b79a80da3090de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66164880645640ecd857d3369df30f84f4916458ee6c3d26120107f9e573773e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66bc707fee3396e9cc6ce816cc1c2deaba23073d2a09f57c8ba61d7b6dba750(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsCustomModule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e18cc9fb4bb6b1113f3c1f5f6d30fc12f391c12c4794792eb644977f1e6f88(
    *,
    module_name: builtins.str,
    module_enablement_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3303d7cc6888506a79e050af2afc4dd75e0bd662e854f5d726f43abad993d3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ef52487e7a9c6490c0fc4f49cc2a090a76de2db4f71745d5341fd6edeae760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f36a4996567be1c22225aa442f15dd428bbac97c7e3a926a9e4ce0f5327c66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1012bea34c9302fe2aabb5081b3f1e1f5e5f66dba34fcf66419efdcb08b83f(
    value: typing.Optional[SecurityposturePosturePolicySetsPoliciesConstraintSecurityHealthAnalyticsModule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da07c468523c27b888f2ebe89dbefae5eae5b4bd23e2a03d94cd3454461c157e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96db00b05d116cd8127c52b68da3cac75ad34641cee16f9e6adcd1419265a149(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229de05da84e46e72f7799f9f94665c050d9f98b922f71a5707d3cbf004b3e06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9635b20d5a0cf6cb2bc768613d82c203d4d61a7146b819f1b2cacd6394c4769(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a077bf1ba0dac6f0df0477ecdbbbffe3b6d3bdeb3d2491195253b4a1ee6f1ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c594859bc4665612e2bcdb2216a5630b5b38adbbf6f5df05d524ad7adc2bea5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityposturePosturePolicySetsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80120decd62933ba9f8da45c5f28c74fd956523e0d11b12a262f712149526ca1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc768823a3d5cdc7aee7bd5b4ff646be4a2f1c1dce3d5dd272aac54adc0d59ed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityposturePosturePolicySetsPoliciesComplianceStandards, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4f7d641db59c542d590bc10cc4f71db89c879e36c258d32c1c64f48bd3f19e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238b154c1747b75f1ade99bd0859a3001a8edd8f21dd5fa4404731577a1dbd58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2667e51aa0545e48acd2188a23067d11c5ce24ee1244ef7bbea8e71f0f8bc5bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePosturePolicySetsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c66e3831f08480f8e684d847df1ec179a44af80da86227c277717f7d723c246(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16c3efaf08488a31f21b8cd1bd55c160f61fe026b690fc299a62f268dfcb16f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d538a0b51ef03252ad977954302e89762acaddbc53304bd18a2febb9c6392f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cb257621204f05e93df5ff072e3948b071e81b8bc0b95ebe2a7121e721ba54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d075996f627f5c29e293db5c1b6ac6a6b22ff07386cc32e0a297c6ff0062804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d38dfa764501b144ac9bd73766f110ce4cb3113ab8c7e79092b4974d3be6cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityposturePostureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
