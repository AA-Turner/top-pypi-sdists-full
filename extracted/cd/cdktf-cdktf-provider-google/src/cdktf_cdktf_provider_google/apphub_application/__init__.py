r'''
# `google_apphub_application`

Refer to the Terraform Registry for docs: [`google_apphub_application`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application).
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


class ApphubApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application google_apphub_application}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_id: builtins.str,
        location: builtins.str,
        scope: typing.Union["ApphubApplicationScope", typing.Dict[builtins.str, typing.Any]],
        attributes: typing.Optional[typing.Union["ApphubApplicationAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApphubApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application google_apphub_application} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_id: Required. The Application identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#application_id ApphubApplication#application_id}
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#location ApphubApplication#location}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#scope ApphubApplication#scope}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#attributes ApphubApplication#attributes}
        :param description: Optional. User-defined description of an Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#description ApphubApplication#description}
        :param display_name: Optional. User-defined name for the Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#id ApphubApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#project ApphubApplication#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#timeouts ApphubApplication#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f1f3d28ad2e57cefadfbee84def39059b351f7d69fb76a515fe3f4044e0e7d)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApphubApplicationConfig(
            application_id=application_id,
            location=location,
            scope=scope,
            attributes=attributes,
            description=description,
            display_name=display_name,
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

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ApphubApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApphubApplication to import.
        :param import_from_id: The id of the existing ApphubApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApphubApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243e57c5bc5644a79b645d8dfc1f4e67d69f921dd4bfe16ab19be4239bb22c4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        *,
        business_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubApplicationAttributesBusinessOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        criticality: typing.Optional[typing.Union["ApphubApplicationAttributesCriticality", typing.Dict[builtins.str, typing.Any]]] = None,
        developer_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubApplicationAttributesDeveloperOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment: typing.Optional[typing.Union["ApphubApplicationAttributesEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        operator_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubApplicationAttributesOperatorOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param business_owners: business_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#business_owners ApphubApplication#business_owners}
        :param criticality: criticality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#criticality ApphubApplication#criticality}
        :param developer_owners: developer_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#developer_owners ApphubApplication#developer_owners}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#environment ApphubApplication#environment}
        :param operator_owners: operator_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#operator_owners ApphubApplication#operator_owners}
        '''
        value = ApphubApplicationAttributes(
            business_owners=business_owners,
            criticality=criticality,
            developer_owners=developer_owners,
            environment=environment,
            operator_owners=operator_owners,
        )

        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putScope")
    def put_scope(self, *, type: builtins.str) -> None:
        '''
        :param type: Required. Scope Type. Possible values: REGIONAL GLOBAL Possible values: ["REGIONAL", "GLOBAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        value = ApphubApplicationScope(type=type)

        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#create ApphubApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#delete ApphubApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#update ApphubApplication#update}.
        '''
        value = ApphubApplicationTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

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
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> "ApphubApplicationAttributesOutputReference":
        return typing.cast("ApphubApplicationAttributesOutputReference", jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "ApphubApplicationScopeOutputReference":
        return typing.cast("ApphubApplicationScopeOutputReference", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApphubApplicationTimeoutsOutputReference":
        return typing.cast("ApphubApplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdInput")
    def application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(self) -> typing.Optional["ApphubApplicationAttributes"]:
        return typing.cast(typing.Optional["ApphubApplicationAttributes"], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional["ApphubApplicationScope"]:
        return typing.cast(typing.Optional["ApphubApplicationScope"], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApphubApplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApphubApplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe5268f2957206333aecb9ef63cc962fd1ba5035029c8ce772a688e147dcdd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9cb8e185bce598c8a1b0307fa0a1d1495253e685b1ea492d23890fba6955c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042c69a8fe53fb7e7345420292684d213cfaf09d7381111ad73a15cfa7bb3898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85440884005129973416a1bcf447e4715e87a0d5c21bc05fda94fb6096505546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97b0dd648bb01f15402cf18df6468e12690611e720b0edab7805cdb4df313ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f7ba4978409d1ded927680044f5bed83594f1b36c444f8147cf519f957d82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "business_owners": "businessOwners",
        "criticality": "criticality",
        "developer_owners": "developerOwners",
        "environment": "environment",
        "operator_owners": "operatorOwners",
    },
)
class ApphubApplicationAttributes:
    def __init__(
        self,
        *,
        business_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubApplicationAttributesBusinessOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        criticality: typing.Optional[typing.Union["ApphubApplicationAttributesCriticality", typing.Dict[builtins.str, typing.Any]]] = None,
        developer_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubApplicationAttributesDeveloperOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment: typing.Optional[typing.Union["ApphubApplicationAttributesEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        operator_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubApplicationAttributesOperatorOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param business_owners: business_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#business_owners ApphubApplication#business_owners}
        :param criticality: criticality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#criticality ApphubApplication#criticality}
        :param developer_owners: developer_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#developer_owners ApphubApplication#developer_owners}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#environment ApphubApplication#environment}
        :param operator_owners: operator_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#operator_owners ApphubApplication#operator_owners}
        '''
        if isinstance(criticality, dict):
            criticality = ApphubApplicationAttributesCriticality(**criticality)
        if isinstance(environment, dict):
            environment = ApphubApplicationAttributesEnvironment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc86a3e05e17f3f0c97fd399d98bb5f06c5e982105f61bb870a71bba6ecd742a)
            check_type(argname="argument business_owners", value=business_owners, expected_type=type_hints["business_owners"])
            check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
            check_type(argname="argument developer_owners", value=developer_owners, expected_type=type_hints["developer_owners"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument operator_owners", value=operator_owners, expected_type=type_hints["operator_owners"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if business_owners is not None:
            self._values["business_owners"] = business_owners
        if criticality is not None:
            self._values["criticality"] = criticality
        if developer_owners is not None:
            self._values["developer_owners"] = developer_owners
        if environment is not None:
            self._values["environment"] = environment
        if operator_owners is not None:
            self._values["operator_owners"] = operator_owners

    @builtins.property
    def business_owners(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubApplicationAttributesBusinessOwners"]]]:
        '''business_owners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#business_owners ApphubApplication#business_owners}
        '''
        result = self._values.get("business_owners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubApplicationAttributesBusinessOwners"]]], result)

    @builtins.property
    def criticality(self) -> typing.Optional["ApphubApplicationAttributesCriticality"]:
        '''criticality block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#criticality ApphubApplication#criticality}
        '''
        result = self._values.get("criticality")
        return typing.cast(typing.Optional["ApphubApplicationAttributesCriticality"], result)

    @builtins.property
    def developer_owners(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubApplicationAttributesDeveloperOwners"]]]:
        '''developer_owners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#developer_owners ApphubApplication#developer_owners}
        '''
        result = self._values.get("developer_owners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubApplicationAttributesDeveloperOwners"]]], result)

    @builtins.property
    def environment(self) -> typing.Optional["ApphubApplicationAttributesEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#environment ApphubApplication#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["ApphubApplicationAttributesEnvironment"], result)

    @builtins.property
    def operator_owners(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubApplicationAttributesOperatorOwners"]]]:
        '''operator_owners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#operator_owners ApphubApplication#operator_owners}
        '''
        result = self._values.get("operator_owners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubApplicationAttributesOperatorOwners"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesBusinessOwners",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "display_name": "displayName"},
)
class ApphubApplicationAttributesBusinessOwners:
    def __init__(
        self,
        *,
        email: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#email ApphubApplication#email}
        :param display_name: Optional. Contact's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccac1ede5906e889fabc2bd595946aa69dfa54fa4bfb7015f3e86daff992579)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def email(self) -> builtins.str:
        '''Required. Email address of the contacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#email ApphubApplication#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. Contact's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationAttributesBusinessOwners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationAttributesBusinessOwnersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesBusinessOwnersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f7770e8dafd8b1cf2664289aaf8e1f009ef236ff8940a0d20df2da3b69c8dc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubApplicationAttributesBusinessOwnersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4330df1c48b262e7599c60d0f063a9ef98257e59a25b60a614f0c6c166d510a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubApplicationAttributesBusinessOwnersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ac23f3c57f8c926975806352295e6d3cfdf11940b375c3f49d668f706551d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52303499798b071d463945b11d42365de9ed62ea81d0166700a2e0edcbd040e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e51ed37b224710da8ba23d173f887d51d5f28be411cacdd16abc0c34dc08d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesBusinessOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesBusinessOwners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesBusinessOwners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fde44e47cd74142a8495762f6103f5de7c1590b8b58149215dc979f36da9726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubApplicationAttributesBusinessOwnersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesBusinessOwnersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e01a9658846dc5e109a0e2e5cb6d937701c16d0782d9e54f4be211a077ec3a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6c2c76b4b66f9e44175c9e96ce8799043746bb30a7416d631ccdfee21178c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a0e35851cef344dc4b4b2c61380b95f2920b2c4e9316ac2418dfb6c18faa07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesBusinessOwners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesBusinessOwners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesBusinessOwners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6ddaec50e5d4990dbd66323dac09e8b92fa0d01b5f6e5b21f5f23895065004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesCriticality",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ApphubApplicationAttributesCriticality:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Criticality type. Possible values: ["MISSION_CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b9f98c5b453902835df61fc87b170f5a17cc31bf6180069c80c911babae679)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Criticality type. Possible values: ["MISSION_CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationAttributesCriticality(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationAttributesCriticalityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesCriticalityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__493b4e8ba99904e543692bb66996d20b53058744267f8cc07e0c6cbb80f8728d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a90f7fece450a2d513304c13e718d08921d50fc1bd5ed7fd854553794c41162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubApplicationAttributesCriticality]:
        return typing.cast(typing.Optional[ApphubApplicationAttributesCriticality], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubApplicationAttributesCriticality],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2cd06bcff8f9e11cbf26bdb67c3be46c4ac9132aca808e7625a77008060c9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesDeveloperOwners",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "display_name": "displayName"},
)
class ApphubApplicationAttributesDeveloperOwners:
    def __init__(
        self,
        *,
        email: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#email ApphubApplication#email}
        :param display_name: Optional. Contact's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9ffdd1ee18219f7be94a27da921d36a5de999bcb7914e1ef7e659807bf2ac1)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def email(self) -> builtins.str:
        '''Required. Email address of the contacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#email ApphubApplication#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. Contact's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationAttributesDeveloperOwners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationAttributesDeveloperOwnersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesDeveloperOwnersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b35cc169d8246378d42d2a1f6e4475002d39c86e8ce7da67b917d800a4b8f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubApplicationAttributesDeveloperOwnersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d884f82677056b1f0cddfac3fe5190485e9f6f6381921d592f9c4f3305407bc8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubApplicationAttributesDeveloperOwnersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5082e69e4b26679e4d401eb19c432f43f2e7dea912c8e2f0230f17d5e80b63aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6517605e5bc5bec5aa72080acfdd1e475714bf20f106d790e6551c4e96c35f37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__359036c3a6b794ebdd59a86cea2f66eb58721e21a130a6df52206e8f3433c1d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesDeveloperOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesDeveloperOwners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesDeveloperOwners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6ffa4eb45e242a2fc616bf2cf480b0fcf649856d45173e67f5cbf0b04e4f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubApplicationAttributesDeveloperOwnersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesDeveloperOwnersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c68eed06efb76347dd6696f4541f4a3d3f0d5352333880cfb55d3af59ea6e50b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cd0992d20aaef647df8c3a9965804c6431d9b8b3214b2e57baac04c456787b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67997ea769ce9092a44a9b7ba18b1dd950694dbb7bfd9f71e261599c24c6abaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesDeveloperOwners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesDeveloperOwners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesDeveloperOwners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe4eb121bfd5335b94402520aa8cfb3668282f00ff63e3b326179011ed896c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesEnvironment",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ApphubApplicationAttributesEnvironment:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Environment type. Possible values: ["PRODUCTION", "STAGING", "TEST", "DEVELOPMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981b74b5ac5f7b835fc20c8f734478f0f3ed16dd454c8dfb0ce938b291d29379)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Environment type. Possible values: ["PRODUCTION", "STAGING", "TEST", "DEVELOPMENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationAttributesEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationAttributesEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1899c48ed42a30c2c3a105ed6fa8035f206601e61766a939ef10525640440da3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704a8728b053aa38330b337f341288ed66e8e06bfce98641d39535deb07478f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubApplicationAttributesEnvironment]:
        return typing.cast(typing.Optional[ApphubApplicationAttributesEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubApplicationAttributesEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a78f6d611548df0800e900cc4666efae0bd6ce8e0a0bc69f558b30f1a49a84a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesOperatorOwners",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "display_name": "displayName"},
)
class ApphubApplicationAttributesOperatorOwners:
    def __init__(
        self,
        *,
        email: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Required. Email address of the contacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#email ApphubApplication#email}
        :param display_name: Optional. Contact's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75d53a1bbde7b346d71db64086c32041fe13776c53f82d549dbe03b1d2895d7)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def email(self) -> builtins.str:
        '''Required. Email address of the contacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#email ApphubApplication#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. Contact's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationAttributesOperatorOwners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationAttributesOperatorOwnersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesOperatorOwnersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04f3624895da580b698a706ca276c293033235e12659c17781296c272c842ab3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubApplicationAttributesOperatorOwnersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f801b74f4c7c5cb1e3fae033956c2de5df35ccbac81088978122c4adfa99dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubApplicationAttributesOperatorOwnersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ab682385a037459157ccf4cc1fd4469d3138cacc78b8e53a66ee8b074ea7e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52e7109ce6c99e3a0d4677da9298a01be469f18fa1e128b8f4eb5669ec496e2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58ad93c57168f833a394f0aa592e4710c99c03c6360a37f7ab5a92e306b56bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesOperatorOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesOperatorOwners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesOperatorOwners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102279c629fd0e34d02c6f213f37ebdeb240b701daf82222a0676f1705915b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubApplicationAttributesOperatorOwnersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesOperatorOwnersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09fc097f4c53a5bb26199c28b9d267371af594b1f320e4122b5794bd82412d0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2b3c6856c1b79be72aa338e389466ac79ecafe401fec9531359af2e9d9964e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666462ea313aa7893f138a04f3e98bfafdb27e7016696a181582f3df8a8a0012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesOperatorOwners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesOperatorOwners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesOperatorOwners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3686735d6bfd308006e283d0d6b2e637cda46995ed5d2918b347dbc7afae32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubApplicationAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3fba751b83dbd3bad9fd38121d616dec1d0f4753c0fff40a2b0cdf541e20df4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBusinessOwners")
    def put_business_owners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesBusinessOwners, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f211733680f96ac63773b63bebddd7604560c379a9471c05705a0b75936286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBusinessOwners", [value]))

    @jsii.member(jsii_name="putCriticality")
    def put_criticality(self, *, type: builtins.str) -> None:
        '''
        :param type: Criticality type. Possible values: ["MISSION_CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        value = ApphubApplicationAttributesCriticality(type=type)

        return typing.cast(None, jsii.invoke(self, "putCriticality", [value]))

    @jsii.member(jsii_name="putDeveloperOwners")
    def put_developer_owners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesDeveloperOwners, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b9867113462a94ade7aa09432d7c1c5ef272736d886eaf29cbb25398ac263b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeveloperOwners", [value]))

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(self, *, type: builtins.str) -> None:
        '''
        :param type: Environment type. Possible values: ["PRODUCTION", "STAGING", "TEST", "DEVELOPMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        value = ApphubApplicationAttributesEnvironment(type=type)

        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putOperatorOwners")
    def put_operator_owners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesOperatorOwners, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e444e5abf4891303caf1328bceb10eec9f2b64a9cc75c93b7fbe3a8b5ac3ca9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOperatorOwners", [value]))

    @jsii.member(jsii_name="resetBusinessOwners")
    def reset_business_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBusinessOwners", []))

    @jsii.member(jsii_name="resetCriticality")
    def reset_criticality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriticality", []))

    @jsii.member(jsii_name="resetDeveloperOwners")
    def reset_developer_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperOwners", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetOperatorOwners")
    def reset_operator_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperatorOwners", []))

    @builtins.property
    @jsii.member(jsii_name="businessOwners")
    def business_owners(self) -> ApphubApplicationAttributesBusinessOwnersList:
        return typing.cast(ApphubApplicationAttributesBusinessOwnersList, jsii.get(self, "businessOwners"))

    @builtins.property
    @jsii.member(jsii_name="criticality")
    def criticality(self) -> ApphubApplicationAttributesCriticalityOutputReference:
        return typing.cast(ApphubApplicationAttributesCriticalityOutputReference, jsii.get(self, "criticality"))

    @builtins.property
    @jsii.member(jsii_name="developerOwners")
    def developer_owners(self) -> ApphubApplicationAttributesDeveloperOwnersList:
        return typing.cast(ApphubApplicationAttributesDeveloperOwnersList, jsii.get(self, "developerOwners"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> ApphubApplicationAttributesEnvironmentOutputReference:
        return typing.cast(ApphubApplicationAttributesEnvironmentOutputReference, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="operatorOwners")
    def operator_owners(self) -> ApphubApplicationAttributesOperatorOwnersList:
        return typing.cast(ApphubApplicationAttributesOperatorOwnersList, jsii.get(self, "operatorOwners"))

    @builtins.property
    @jsii.member(jsii_name="businessOwnersInput")
    def business_owners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesBusinessOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesBusinessOwners]]], jsii.get(self, "businessOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalityInput")
    def criticality_input(
        self,
    ) -> typing.Optional[ApphubApplicationAttributesCriticality]:
        return typing.cast(typing.Optional[ApphubApplicationAttributesCriticality], jsii.get(self, "criticalityInput"))

    @builtins.property
    @jsii.member(jsii_name="developerOwnersInput")
    def developer_owners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesDeveloperOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesDeveloperOwners]]], jsii.get(self, "developerOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[ApphubApplicationAttributesEnvironment]:
        return typing.cast(typing.Optional[ApphubApplicationAttributesEnvironment], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorOwnersInput")
    def operator_owners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesOperatorOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesOperatorOwners]]], jsii.get(self, "operatorOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubApplicationAttributes]:
        return typing.cast(typing.Optional[ApphubApplicationAttributes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubApplicationAttributes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5b1f582fb6852a8757e85ab1aa9ba32cfbbee588ec25aa462fe0e66c8ef117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_id": "applicationId",
        "location": "location",
        "scope": "scope",
        "attributes": "attributes",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ApphubApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        application_id: builtins.str,
        location: builtins.str,
        scope: typing.Union["ApphubApplicationScope", typing.Dict[builtins.str, typing.Any]],
        attributes: typing.Optional[typing.Union[ApphubApplicationAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApphubApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_id: Required. The Application identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#application_id ApphubApplication#application_id}
        :param location: Part of 'parent'. See documentation of 'projectsId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#location ApphubApplication#location}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#scope ApphubApplication#scope}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#attributes ApphubApplication#attributes}
        :param description: Optional. User-defined description of an Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#description ApphubApplication#description}
        :param display_name: Optional. User-defined name for the Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#id ApphubApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#project ApphubApplication#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#timeouts ApphubApplication#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scope, dict):
            scope = ApphubApplicationScope(**scope)
        if isinstance(attributes, dict):
            attributes = ApphubApplicationAttributes(**attributes)
        if isinstance(timeouts, dict):
            timeouts = ApphubApplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae1e499fc146ad536061b211b8208d59e38d74a2596b22bdd89fcd9dc4c551c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "location": location,
            "scope": scope,
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
        if attributes is not None:
            self._values["attributes"] = attributes
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
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
    def application_id(self) -> builtins.str:
        '''Required. The Application identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#application_id ApphubApplication#application_id}
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Part of 'parent'. See documentation of 'projectsId'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#location ApphubApplication#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> "ApphubApplicationScope":
        '''scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#scope ApphubApplication#scope}
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast("ApphubApplicationScope", result)

    @builtins.property
    def attributes(self) -> typing.Optional[ApphubApplicationAttributes]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#attributes ApphubApplication#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[ApphubApplicationAttributes], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. User-defined description of an Application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#description ApphubApplication#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Optional. User-defined name for the Application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#display_name ApphubApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#id ApphubApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#project ApphubApplication#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApphubApplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#timeouts ApphubApplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApphubApplicationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationScope",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ApphubApplicationScope:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Required. Scope Type. Possible values: REGIONAL GLOBAL Possible values: ["REGIONAL", "GLOBAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3127f75fc5507b0cc5b272305ce44f9d045960986ae7f706cc12e6d72debd599)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Required. Scope Type.   Possible values: REGIONAL GLOBAL Possible values: ["REGIONAL", "GLOBAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#type ApphubApplication#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba44419446015113cc2eb2daa7cf615b359a14d4b11a59f84ecd90a1d856140)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b08f2222ff82f696f4a0069c02b6f4e543ca1dcd26fb522089b61e136158a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubApplicationScope]:
        return typing.cast(typing.Optional[ApphubApplicationScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApphubApplicationScope]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5715587b5614006711affc98096fbf1f4ea9a2ccab5b4cf295a6ac67a469790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApphubApplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#create ApphubApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#delete ApphubApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#update ApphubApplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb009f54a1138b034c5e3f9829995f31ac2813cf99885cab0309861b56d24bb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#create ApphubApplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#delete ApphubApplication#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_application#update ApphubApplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubApplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubApplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubApplication.ApphubApplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69d382a299fa3453036c1a3044ffca30ba07f6fe9f1029800e1018972553f552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f09948f53fa3eea43b2a6508d43380f4a206b6708216941d5459eaa21fbeb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58239fc34991ba0fc44dcfdee9ec659004c9c9055873ecd1b30f116c4649f363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241c821d38df6600672f23bc88b9230e102e9beab4ab8c958e1f99ab97b9c04f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31289d7cffd739226ad494c99e9742a9d53b28e1564d7ee52d92e39c90792dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApphubApplication",
    "ApphubApplicationAttributes",
    "ApphubApplicationAttributesBusinessOwners",
    "ApphubApplicationAttributesBusinessOwnersList",
    "ApphubApplicationAttributesBusinessOwnersOutputReference",
    "ApphubApplicationAttributesCriticality",
    "ApphubApplicationAttributesCriticalityOutputReference",
    "ApphubApplicationAttributesDeveloperOwners",
    "ApphubApplicationAttributesDeveloperOwnersList",
    "ApphubApplicationAttributesDeveloperOwnersOutputReference",
    "ApphubApplicationAttributesEnvironment",
    "ApphubApplicationAttributesEnvironmentOutputReference",
    "ApphubApplicationAttributesOperatorOwners",
    "ApphubApplicationAttributesOperatorOwnersList",
    "ApphubApplicationAttributesOperatorOwnersOutputReference",
    "ApphubApplicationAttributesOutputReference",
    "ApphubApplicationConfig",
    "ApphubApplicationScope",
    "ApphubApplicationScopeOutputReference",
    "ApphubApplicationTimeouts",
    "ApphubApplicationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__88f1f3d28ad2e57cefadfbee84def39059b351f7d69fb76a515fe3f4044e0e7d(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_id: builtins.str,
    location: builtins.str,
    scope: typing.Union[ApphubApplicationScope, typing.Dict[builtins.str, typing.Any]],
    attributes: typing.Optional[typing.Union[ApphubApplicationAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApphubApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__243e57c5bc5644a79b645d8dfc1f4e67d69f921dd4bfe16ab19be4239bb22c4b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe5268f2957206333aecb9ef63cc962fd1ba5035029c8ce772a688e147dcdd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9cb8e185bce598c8a1b0307fa0a1d1495253e685b1ea492d23890fba6955c0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042c69a8fe53fb7e7345420292684d213cfaf09d7381111ad73a15cfa7bb3898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85440884005129973416a1bcf447e4715e87a0d5c21bc05fda94fb6096505546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97b0dd648bb01f15402cf18df6468e12690611e720b0edab7805cdb4df313ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f7ba4978409d1ded927680044f5bed83594f1b36c444f8147cf519f957d82d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc86a3e05e17f3f0c97fd399d98bb5f06c5e982105f61bb870a71bba6ecd742a(
    *,
    business_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesBusinessOwners, typing.Dict[builtins.str, typing.Any]]]]] = None,
    criticality: typing.Optional[typing.Union[ApphubApplicationAttributesCriticality, typing.Dict[builtins.str, typing.Any]]] = None,
    developer_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesDeveloperOwners, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environment: typing.Optional[typing.Union[ApphubApplicationAttributesEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    operator_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesOperatorOwners, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccac1ede5906e889fabc2bd595946aa69dfa54fa4bfb7015f3e86daff992579(
    *,
    email: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7770e8dafd8b1cf2664289aaf8e1f009ef236ff8940a0d20df2da3b69c8dc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4330df1c48b262e7599c60d0f063a9ef98257e59a25b60a614f0c6c166d510a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ac23f3c57f8c926975806352295e6d3cfdf11940b375c3f49d668f706551d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52303499798b071d463945b11d42365de9ed62ea81d0166700a2e0edcbd040e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e51ed37b224710da8ba23d173f887d51d5f28be411cacdd16abc0c34dc08d16(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fde44e47cd74142a8495762f6103f5de7c1590b8b58149215dc979f36da9726(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesBusinessOwners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e01a9658846dc5e109a0e2e5cb6d937701c16d0782d9e54f4be211a077ec3a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6c2c76b4b66f9e44175c9e96ce8799043746bb30a7416d631ccdfee21178c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a0e35851cef344dc4b4b2c61380b95f2920b2c4e9316ac2418dfb6c18faa07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6ddaec50e5d4990dbd66323dac09e8b92fa0d01b5f6e5b21f5f23895065004(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesBusinessOwners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b9f98c5b453902835df61fc87b170f5a17cc31bf6180069c80c911babae679(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493b4e8ba99904e543692bb66996d20b53058744267f8cc07e0c6cbb80f8728d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a90f7fece450a2d513304c13e718d08921d50fc1bd5ed7fd854553794c41162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cd06bcff8f9e11cbf26bdb67c3be46c4ac9132aca808e7625a77008060c9bd(
    value: typing.Optional[ApphubApplicationAttributesCriticality],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9ffdd1ee18219f7be94a27da921d36a5de999bcb7914e1ef7e659807bf2ac1(
    *,
    email: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b35cc169d8246378d42d2a1f6e4475002d39c86e8ce7da67b917d800a4b8f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d884f82677056b1f0cddfac3fe5190485e9f6f6381921d592f9c4f3305407bc8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5082e69e4b26679e4d401eb19c432f43f2e7dea912c8e2f0230f17d5e80b63aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6517605e5bc5bec5aa72080acfdd1e475714bf20f106d790e6551c4e96c35f37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359036c3a6b794ebdd59a86cea2f66eb58721e21a130a6df52206e8f3433c1d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6ffa4eb45e242a2fc616bf2cf480b0fcf649856d45173e67f5cbf0b04e4f12(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesDeveloperOwners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68eed06efb76347dd6696f4541f4a3d3f0d5352333880cfb55d3af59ea6e50b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cd0992d20aaef647df8c3a9965804c6431d9b8b3214b2e57baac04c456787b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67997ea769ce9092a44a9b7ba18b1dd950694dbb7bfd9f71e261599c24c6abaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe4eb121bfd5335b94402520aa8cfb3668282f00ff63e3b326179011ed896c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesDeveloperOwners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981b74b5ac5f7b835fc20c8f734478f0f3ed16dd454c8dfb0ce938b291d29379(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1899c48ed42a30c2c3a105ed6fa8035f206601e61766a939ef10525640440da3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704a8728b053aa38330b337f341288ed66e8e06bfce98641d39535deb07478f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a78f6d611548df0800e900cc4666efae0bd6ce8e0a0bc69f558b30f1a49a84a(
    value: typing.Optional[ApphubApplicationAttributesEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75d53a1bbde7b346d71db64086c32041fe13776c53f82d549dbe03b1d2895d7(
    *,
    email: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f3624895da580b698a706ca276c293033235e12659c17781296c272c842ab3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f801b74f4c7c5cb1e3fae033956c2de5df35ccbac81088978122c4adfa99dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ab682385a037459157ccf4cc1fd4469d3138cacc78b8e53a66ee8b074ea7e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e7109ce6c99e3a0d4677da9298a01be469f18fa1e128b8f4eb5669ec496e2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ad93c57168f833a394f0aa592e4710c99c03c6360a37f7ab5a92e306b56bc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102279c629fd0e34d02c6f213f37ebdeb240b701daf82222a0676f1705915b3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubApplicationAttributesOperatorOwners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fc097f4c53a5bb26199c28b9d267371af594b1f320e4122b5794bd82412d0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2b3c6856c1b79be72aa338e389466ac79ecafe401fec9531359af2e9d9964e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666462ea313aa7893f138a04f3e98bfafdb27e7016696a181582f3df8a8a0012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3686735d6bfd308006e283d0d6b2e637cda46995ed5d2918b347dbc7afae32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationAttributesOperatorOwners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fba751b83dbd3bad9fd38121d616dec1d0f4753c0fff40a2b0cdf541e20df4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f211733680f96ac63773b63bebddd7604560c379a9471c05705a0b75936286(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesBusinessOwners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b9867113462a94ade7aa09432d7c1c5ef272736d886eaf29cbb25398ac263b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesDeveloperOwners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e444e5abf4891303caf1328bceb10eec9f2b64a9cc75c93b7fbe3a8b5ac3ca9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubApplicationAttributesOperatorOwners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5b1f582fb6852a8757e85ab1aa9ba32cfbbee588ec25aa462fe0e66c8ef117(
    value: typing.Optional[ApphubApplicationAttributes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae1e499fc146ad536061b211b8208d59e38d74a2596b22bdd89fcd9dc4c551c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_id: builtins.str,
    location: builtins.str,
    scope: typing.Union[ApphubApplicationScope, typing.Dict[builtins.str, typing.Any]],
    attributes: typing.Optional[typing.Union[ApphubApplicationAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApphubApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3127f75fc5507b0cc5b272305ce44f9d045960986ae7f706cc12e6d72debd599(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba44419446015113cc2eb2daa7cf615b359a14d4b11a59f84ecd90a1d856140(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b08f2222ff82f696f4a0069c02b6f4e543ca1dcd26fb522089b61e136158a60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5715587b5614006711affc98096fbf1f4ea9a2ccab5b4cf295a6ac67a469790(
    value: typing.Optional[ApphubApplicationScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb009f54a1138b034c5e3f9829995f31ac2813cf99885cab0309861b56d24bb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d382a299fa3453036c1a3044ffca30ba07f6fe9f1029800e1018972553f552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f09948f53fa3eea43b2a6508d43380f4a206b6708216941d5459eaa21fbeb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58239fc34991ba0fc44dcfdee9ec659004c9c9055873ecd1b30f116c4649f363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241c821d38df6600672f23bc88b9230e102e9beab4ab8c958e1f99ab97b9c04f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31289d7cffd739226ad494c99e9742a9d53b28e1564d7ee52d92e39c90792dd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubApplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
