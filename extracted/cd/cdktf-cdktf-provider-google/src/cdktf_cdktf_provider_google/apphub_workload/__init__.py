r'''
# `google_apphub_workload`

Refer to the Terraform Registry for docs: [`google_apphub_workload`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload).
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


class ApphubWorkload(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkload",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload google_apphub_workload}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_id: builtins.str,
        discovered_workload: builtins.str,
        location: builtins.str,
        workload_id: builtins.str,
        attributes: typing.Optional[typing.Union["ApphubWorkloadAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApphubWorkloadTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload google_apphub_workload} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_id: Part of 'parent'. Full resource name of a parent Application. Example: projects/{HOST_PROJECT_ID}/locations/{LOCATION}/applications/{APPLICATION_ID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#application_id ApphubWorkload#application_id}
        :param discovered_workload: Immutable. The resource name of the original discovered workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#discovered_workload ApphubWorkload#discovered_workload}
        :param location: Part of 'parent'. Full resource name of a parent Application. Example: projects/{HOST_PROJECT_ID}/locations/{LOCATION}/applications/{APPLICATION_ID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#location ApphubWorkload#location}
        :param workload_id: The Workload identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#workload_id ApphubWorkload#workload_id}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#attributes ApphubWorkload#attributes}
        :param description: User-defined description of a Workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#description ApphubWorkload#description}
        :param display_name: User-defined name for the Workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#id ApphubWorkload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#project ApphubWorkload#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#timeouts ApphubWorkload#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c894267a27498a73e515a2e6e3706cf2953cc8f09e3486196a419d1dd00a882)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApphubWorkloadConfig(
            application_id=application_id,
            discovered_workload=discovered_workload,
            location=location,
            workload_id=workload_id,
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
        '''Generates CDKTF code for importing a ApphubWorkload resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApphubWorkload to import.
        :param import_from_id: The id of the existing ApphubWorkload that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApphubWorkload to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652aa7fd3b6912640ce6cff034a6a28cabe896afe5b740a9c0a2e2d1e25c8716)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttributes")
    def put_attributes(
        self,
        *,
        business_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubWorkloadAttributesBusinessOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        criticality: typing.Optional[typing.Union["ApphubWorkloadAttributesCriticality", typing.Dict[builtins.str, typing.Any]]] = None,
        developer_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubWorkloadAttributesDeveloperOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment: typing.Optional[typing.Union["ApphubWorkloadAttributesEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        operator_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubWorkloadAttributesOperatorOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param business_owners: business_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#business_owners ApphubWorkload#business_owners}
        :param criticality: criticality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#criticality ApphubWorkload#criticality}
        :param developer_owners: developer_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#developer_owners ApphubWorkload#developer_owners}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#environment ApphubWorkload#environment}
        :param operator_owners: operator_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#operator_owners ApphubWorkload#operator_owners}
        '''
        value = ApphubWorkloadAttributes(
            business_owners=business_owners,
            criticality=criticality,
            developer_owners=developer_owners,
            environment=environment,
            operator_owners=operator_owners,
        )

        return typing.cast(None, jsii.invoke(self, "putAttributes", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#create ApphubWorkload#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#delete ApphubWorkload#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#update ApphubWorkload#update}.
        '''
        value = ApphubWorkloadTimeouts(create=create, delete=delete, update=update)

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
    def attributes(self) -> "ApphubWorkloadAttributesOutputReference":
        return typing.cast("ApphubWorkloadAttributesOutputReference", jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApphubWorkloadTimeoutsOutputReference":
        return typing.cast("ApphubWorkloadTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="workloadProperties")
    def workload_properties(self) -> "ApphubWorkloadWorkloadPropertiesList":
        return typing.cast("ApphubWorkloadWorkloadPropertiesList", jsii.get(self, "workloadProperties"))

    @builtins.property
    @jsii.member(jsii_name="workloadReference")
    def workload_reference(self) -> "ApphubWorkloadWorkloadReferenceList":
        return typing.cast("ApphubWorkloadWorkloadReferenceList", jsii.get(self, "workloadReference"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdInput")
    def application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(self) -> typing.Optional["ApphubWorkloadAttributes"]:
        return typing.cast(typing.Optional["ApphubWorkloadAttributes"], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="discoveredWorkloadInput")
    def discovered_workload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "discoveredWorkloadInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApphubWorkloadTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApphubWorkloadTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdInput")
    def workload_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadIdInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ac094832101b417ce29716d16791ff620084f9752d2f77bc47696101c65af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9dc0a8acfbd9b6a791233165b52b6fcd015a3617e4da67231fb836679944fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="discoveredWorkload")
    def discovered_workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "discoveredWorkload"))

    @discovered_workload.setter
    def discovered_workload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81db90b946843ebc238a56ee5eb14525be9dcb373933e59f8843f806301abfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discoveredWorkload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0cbedcbade0f9fcfe50c37f59127a89bee02d53c6145022822e985989787e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9c724a028fd3640c2abddf9a1af96b34aedb8b37e5a30065efb51fa5b2606d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e789f93dcc5ad5eef686664e40d9778e581069874f537ec4cfbbe30d4c6d48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f60beeba6abfa75a952ef7d12a0b8eb4188c7c70cd9896786b2d06776adcae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadId")
    def workload_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadId"))

    @workload_id.setter
    def workload_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146f91a6d5c6aa69b1cfe0ba23fdda1ce2a7461a43e637c2dec598215486aab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "business_owners": "businessOwners",
        "criticality": "criticality",
        "developer_owners": "developerOwners",
        "environment": "environment",
        "operator_owners": "operatorOwners",
    },
)
class ApphubWorkloadAttributes:
    def __init__(
        self,
        *,
        business_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubWorkloadAttributesBusinessOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        criticality: typing.Optional[typing.Union["ApphubWorkloadAttributesCriticality", typing.Dict[builtins.str, typing.Any]]] = None,
        developer_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubWorkloadAttributesDeveloperOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment: typing.Optional[typing.Union["ApphubWorkloadAttributesEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        operator_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApphubWorkloadAttributesOperatorOwners", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param business_owners: business_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#business_owners ApphubWorkload#business_owners}
        :param criticality: criticality block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#criticality ApphubWorkload#criticality}
        :param developer_owners: developer_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#developer_owners ApphubWorkload#developer_owners}
        :param environment: environment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#environment ApphubWorkload#environment}
        :param operator_owners: operator_owners block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#operator_owners ApphubWorkload#operator_owners}
        '''
        if isinstance(criticality, dict):
            criticality = ApphubWorkloadAttributesCriticality(**criticality)
        if isinstance(environment, dict):
            environment = ApphubWorkloadAttributesEnvironment(**environment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebb5d0f6849a0e17315906e8e7b324940416aec9f4b7ccac46491380f8950ca)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubWorkloadAttributesBusinessOwners"]]]:
        '''business_owners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#business_owners ApphubWorkload#business_owners}
        '''
        result = self._values.get("business_owners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubWorkloadAttributesBusinessOwners"]]], result)

    @builtins.property
    def criticality(self) -> typing.Optional["ApphubWorkloadAttributesCriticality"]:
        '''criticality block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#criticality ApphubWorkload#criticality}
        '''
        result = self._values.get("criticality")
        return typing.cast(typing.Optional["ApphubWorkloadAttributesCriticality"], result)

    @builtins.property
    def developer_owners(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubWorkloadAttributesDeveloperOwners"]]]:
        '''developer_owners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#developer_owners ApphubWorkload#developer_owners}
        '''
        result = self._values.get("developer_owners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubWorkloadAttributesDeveloperOwners"]]], result)

    @builtins.property
    def environment(self) -> typing.Optional["ApphubWorkloadAttributesEnvironment"]:
        '''environment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#environment ApphubWorkload#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional["ApphubWorkloadAttributesEnvironment"], result)

    @builtins.property
    def operator_owners(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubWorkloadAttributesOperatorOwners"]]]:
        '''operator_owners block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#operator_owners ApphubWorkload#operator_owners}
        '''
        result = self._values.get("operator_owners")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApphubWorkloadAttributesOperatorOwners"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesBusinessOwners",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "display_name": "displayName"},
)
class ApphubWorkloadAttributesBusinessOwners:
    def __init__(
        self,
        *,
        email: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Email address of the contacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#email ApphubWorkload#email}
        :param display_name: Contact's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86fe9cf86e835a46f908b757bd5950fc39cdd14b6866a0e87ddc9c09a9a0758)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def email(self) -> builtins.str:
        '''Email address of the contacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#email ApphubWorkload#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Contact's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadAttributesBusinessOwners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadAttributesBusinessOwnersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesBusinessOwnersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1f51460c08dca69c6f0fe57576c345cda6f608d95f1856124acba2e8e05a38d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubWorkloadAttributesBusinessOwnersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425adeb2c7bfc2ef5874201527f49cd67c89b1a10ddb9dcfb62a123eaebdba91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubWorkloadAttributesBusinessOwnersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd654ae1d87a146afe61e93329d6850430f860451990952c4bdda9b3e9990317)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0755120e923f21c688b159873e73902ccc8028c1876af61c57459276190bcab8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7790cffa98f1f006ac193d2f79453244778cea167af0ea637e3a667f5908a3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesBusinessOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesBusinessOwners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesBusinessOwners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba61d1341149f54fa4dbc4c1ab62a075d7faee3d851534652f238c25066c8616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubWorkloadAttributesBusinessOwnersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesBusinessOwnersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73bb21fdffe3b4b5c64def9201b9795b01dc691bb71e8dd2e52ca46c02419018)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4670140563c562772996ffc664c2e71ef41c7be305f6eb60bfc9c53e34a5e238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada75f59f9165f42669971a271851c0a0a2edb31d8e3d0d9d8b3bad936161a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesBusinessOwners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesBusinessOwners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesBusinessOwners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e9545343c836202c2548cbd39da2c899e3129f8baaeb76dd5e3d139bed4970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesCriticality",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ApphubWorkloadAttributesCriticality:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Criticality type. Possible values: ["MISSION_CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#type ApphubWorkload#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e98c445ef735bc7ad44258cadb8b9bf860533f72bd6f257160ae0a0e83be75b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Criticality type. Possible values: ["MISSION_CRITICAL", "HIGH", "MEDIUM", "LOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#type ApphubWorkload#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadAttributesCriticality(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadAttributesCriticalityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesCriticalityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__931544f9a23473632f26db966968fb65643496889b4e1b0211e04885ace340b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa361ee709fb268435e7eb73c9cac5fe060e74163d86f1d8759255052ef2b99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubWorkloadAttributesCriticality]:
        return typing.cast(typing.Optional[ApphubWorkloadAttributesCriticality], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubWorkloadAttributesCriticality],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd28e0d5dcd4726a5475214432a9b34dc03c5c1fcd6f1a601479642816494ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesDeveloperOwners",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "display_name": "displayName"},
)
class ApphubWorkloadAttributesDeveloperOwners:
    def __init__(
        self,
        *,
        email: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Email address of the contacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#email ApphubWorkload#email}
        :param display_name: Contact's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d3bc708be042fbd2ac43875b6750a5999acb6cb2bd439c9684924014636888)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def email(self) -> builtins.str:
        '''Email address of the contacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#email ApphubWorkload#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Contact's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadAttributesDeveloperOwners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadAttributesDeveloperOwnersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesDeveloperOwnersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf777bc66a96ccf7b8fa0cf211ed19c23482b05a6726c7925067412dc13c6bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubWorkloadAttributesDeveloperOwnersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80221730937932209cb2437231e01a1740cd18efa1d02907ddb56b34dfdee4be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubWorkloadAttributesDeveloperOwnersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680fb2256364dc5f7f4ca8f0cad247a77b4cc7739ca3d9de23a4532c78e53dbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__065d51828710f386572fdbef0053ff0772627089fe330e280b0592e487e7e52e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51723f9e609937c504483d2ed18dcf4d5158a11dcee09c0ba895cc5787eaaeca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesDeveloperOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesDeveloperOwners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesDeveloperOwners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622beb5de773a15c7a580d02010d84282a3e36f25be00ebff30c48b8e04e3edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubWorkloadAttributesDeveloperOwnersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesDeveloperOwnersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9707db9ffca992749f6788bd02a67fb14781827cd7f5f381e143a0ebdc02dd5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c024c1c095a3be85f1eb4d37e3f2434112bd1708af66ca306eb79172baeb9565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8aab605cd0464cafc39b7f5cc0df7994f2093143e0d01a7c5d1c5be2d50880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesDeveloperOwners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesDeveloperOwners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesDeveloperOwners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4365cfd492126f12d7862dc80d5d1ec94299ae8ec3191da7238e878bb8c5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesEnvironment",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ApphubWorkloadAttributesEnvironment:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Environment type. Possible values: ["PRODUCTION", "STAGING", "TEST", "DEVELOPMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#type ApphubWorkload#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8724601c61fd55b43e87e0cd7219e9a05c7d7f69ed9e27d98b392a72c951958)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Environment type. Possible values: ["PRODUCTION", "STAGING", "TEST", "DEVELOPMENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#type ApphubWorkload#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadAttributesEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadAttributesEnvironmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesEnvironmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ed7f64e307d5f8e5d2144d9ec6c8d5a5b80d51ef9d5c6ce41f519c0b7033511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10106bc72023ca63ae5960e45244a5c1e38f5bae4111bc90007c447caf63f611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubWorkloadAttributesEnvironment]:
        return typing.cast(typing.Optional[ApphubWorkloadAttributesEnvironment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubWorkloadAttributesEnvironment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8932d85e5ea222d420b2eefa4a269b7cc7ac2b083f7b66432d8241dc552ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesOperatorOwners",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "display_name": "displayName"},
)
class ApphubWorkloadAttributesOperatorOwners:
    def __init__(
        self,
        *,
        email: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Email address of the contacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#email ApphubWorkload#email}
        :param display_name: Contact's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8da06818e99252de4db3a57910e58bbfd009ebe0e8fe7b9bbadad47c00475f2)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email": email,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def email(self) -> builtins.str:
        '''Email address of the contacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#email ApphubWorkload#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Contact's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadAttributesOperatorOwners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadAttributesOperatorOwnersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesOperatorOwnersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f77b8e29aa9acc767633fdc924fde35926c7091a5912eff7b5f19460f1772fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubWorkloadAttributesOperatorOwnersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bd6fd93595ac2962d0c984b3a7a984d412ea136fe646fc2a9acc2767db3b31)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubWorkloadAttributesOperatorOwnersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b33a4bb9ccda95a8028ce9fa34b0ebd9b710e602bf4debea6da08902f2277a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__914428d48bee87a84c7f753a059a2699533c9840e517cc543f9e78435915300f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc9f0eb29828219c85b9d70c3ee8537796edd1a731b36381e80c6468ea9ff7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesOperatorOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesOperatorOwners]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesOperatorOwners]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c83e021a92a26456d3b6ccda73ac84c9d8836a41a1201c251df0fbed3a0279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubWorkloadAttributesOperatorOwnersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesOperatorOwnersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4021d1e6050131ffb5a142adc23b16f0ff297ec8796ea219d22d863a8f331b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__300828bdbb91d5821475bd865f126f0bb4f36946a5be589124dc6ea73aef9620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36b23e27ec1f91bde9e2a2f4f799fcd0acc9fbb000d13a8e5282335a707d3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesOperatorOwners]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesOperatorOwners]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesOperatorOwners]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a386751d2e236a2fbd7e80dd801b501af2346b8ab6d323272e1913f0aaf6664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApphubWorkloadAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ad6c18b5cf72fe40788bcc6cc8fd24aac39f10e5c947f3b332045d9ba77045f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBusinessOwners")
    def put_business_owners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesBusinessOwners, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebb59286ecc35f219a6edc3af653fbba79408a5e9bdf952634ef07c8efdbf7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBusinessOwners", [value]))

    @jsii.member(jsii_name="putCriticality")
    def put_criticality(self, *, type: builtins.str) -> None:
        '''
        :param type: Criticality type. Possible values: ["MISSION_CRITICAL", "HIGH", "MEDIUM", "LOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#type ApphubWorkload#type}
        '''
        value = ApphubWorkloadAttributesCriticality(type=type)

        return typing.cast(None, jsii.invoke(self, "putCriticality", [value]))

    @jsii.member(jsii_name="putDeveloperOwners")
    def put_developer_owners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesDeveloperOwners, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf9cffc31c139d39438d5acb6ac71a9d5be6ed557aff0e9012af42b5c651951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeveloperOwners", [value]))

    @jsii.member(jsii_name="putEnvironment")
    def put_environment(self, *, type: builtins.str) -> None:
        '''
        :param type: Environment type. Possible values: ["PRODUCTION", "STAGING", "TEST", "DEVELOPMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#type ApphubWorkload#type}
        '''
        value = ApphubWorkloadAttributesEnvironment(type=type)

        return typing.cast(None, jsii.invoke(self, "putEnvironment", [value]))

    @jsii.member(jsii_name="putOperatorOwners")
    def put_operator_owners(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesOperatorOwners, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab502d89e08e112e304b02b3d071b65e9251b1222178fedb6fc0f8265fe21858)
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
    def business_owners(self) -> ApphubWorkloadAttributesBusinessOwnersList:
        return typing.cast(ApphubWorkloadAttributesBusinessOwnersList, jsii.get(self, "businessOwners"))

    @builtins.property
    @jsii.member(jsii_name="criticality")
    def criticality(self) -> ApphubWorkloadAttributesCriticalityOutputReference:
        return typing.cast(ApphubWorkloadAttributesCriticalityOutputReference, jsii.get(self, "criticality"))

    @builtins.property
    @jsii.member(jsii_name="developerOwners")
    def developer_owners(self) -> ApphubWorkloadAttributesDeveloperOwnersList:
        return typing.cast(ApphubWorkloadAttributesDeveloperOwnersList, jsii.get(self, "developerOwners"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> ApphubWorkloadAttributesEnvironmentOutputReference:
        return typing.cast(ApphubWorkloadAttributesEnvironmentOutputReference, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="operatorOwners")
    def operator_owners(self) -> ApphubWorkloadAttributesOperatorOwnersList:
        return typing.cast(ApphubWorkloadAttributesOperatorOwnersList, jsii.get(self, "operatorOwners"))

    @builtins.property
    @jsii.member(jsii_name="businessOwnersInput")
    def business_owners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesBusinessOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesBusinessOwners]]], jsii.get(self, "businessOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalityInput")
    def criticality_input(self) -> typing.Optional[ApphubWorkloadAttributesCriticality]:
        return typing.cast(typing.Optional[ApphubWorkloadAttributesCriticality], jsii.get(self, "criticalityInput"))

    @builtins.property
    @jsii.member(jsii_name="developerOwnersInput")
    def developer_owners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesDeveloperOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesDeveloperOwners]]], jsii.get(self, "developerOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[ApphubWorkloadAttributesEnvironment]:
        return typing.cast(typing.Optional[ApphubWorkloadAttributesEnvironment], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorOwnersInput")
    def operator_owners_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesOperatorOwners]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesOperatorOwners]]], jsii.get(self, "operatorOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubWorkloadAttributes]:
        return typing.cast(typing.Optional[ApphubWorkloadAttributes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApphubWorkloadAttributes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197d871356481d231393658e3a53c9f037677eb5b3fb3cf3d1eee94eab28f997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadConfig",
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
        "discovered_workload": "discoveredWorkload",
        "location": "location",
        "workload_id": "workloadId",
        "attributes": "attributes",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ApphubWorkloadConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        discovered_workload: builtins.str,
        location: builtins.str,
        workload_id: builtins.str,
        attributes: typing.Optional[typing.Union[ApphubWorkloadAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApphubWorkloadTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_id: Part of 'parent'. Full resource name of a parent Application. Example: projects/{HOST_PROJECT_ID}/locations/{LOCATION}/applications/{APPLICATION_ID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#application_id ApphubWorkload#application_id}
        :param discovered_workload: Immutable. The resource name of the original discovered workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#discovered_workload ApphubWorkload#discovered_workload}
        :param location: Part of 'parent'. Full resource name of a parent Application. Example: projects/{HOST_PROJECT_ID}/locations/{LOCATION}/applications/{APPLICATION_ID}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#location ApphubWorkload#location}
        :param workload_id: The Workload identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#workload_id ApphubWorkload#workload_id}
        :param attributes: attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#attributes ApphubWorkload#attributes}
        :param description: User-defined description of a Workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#description ApphubWorkload#description}
        :param display_name: User-defined name for the Workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#id ApphubWorkload#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#project ApphubWorkload#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#timeouts ApphubWorkload#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(attributes, dict):
            attributes = ApphubWorkloadAttributes(**attributes)
        if isinstance(timeouts, dict):
            timeouts = ApphubWorkloadTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1da8c9dc287263b4e72047c550a3fdd9a21defac3da811146cb761a313cd21d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument discovered_workload", value=discovered_workload, expected_type=type_hints["discovered_workload"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument workload_id", value=workload_id, expected_type=type_hints["workload_id"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "discovered_workload": discovered_workload,
            "location": location,
            "workload_id": workload_id,
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
        '''Part of 'parent'.  Full resource name of a parent Application. Example: projects/{HOST_PROJECT_ID}/locations/{LOCATION}/applications/{APPLICATION_ID}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#application_id ApphubWorkload#application_id}
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def discovered_workload(self) -> builtins.str:
        '''Immutable. The resource name of the original discovered workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#discovered_workload ApphubWorkload#discovered_workload}
        '''
        result = self._values.get("discovered_workload")
        assert result is not None, "Required property 'discovered_workload' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Part of 'parent'.  Full resource name of a parent Application. Example: projects/{HOST_PROJECT_ID}/locations/{LOCATION}/applications/{APPLICATION_ID}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#location ApphubWorkload#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workload_id(self) -> builtins.str:
        '''The Workload identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#workload_id ApphubWorkload#workload_id}
        '''
        result = self._values.get("workload_id")
        assert result is not None, "Required property 'workload_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Optional[ApphubWorkloadAttributes]:
        '''attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#attributes ApphubWorkload#attributes}
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[ApphubWorkloadAttributes], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-defined description of a Workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#description ApphubWorkload#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-defined name for the Workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#display_name ApphubWorkload#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#id ApphubWorkload#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#project ApphubWorkload#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApphubWorkloadTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#timeouts ApphubWorkload#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApphubWorkloadTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApphubWorkloadTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#create ApphubWorkload#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#delete ApphubWorkload#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#update ApphubWorkload#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8776f4c1ee081d3a26f088453850eb0f089302f433b94ea74fdd7a68214050)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#create ApphubWorkload#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#delete ApphubWorkload#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apphub_workload#update ApphubWorkload#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a308e024ed7950c4c798030bffb956c5279549582af72530972b1b319b16e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75efeba28f873010eba9ae48f6c5e458650e5671787efc32be714fe23e477d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf4ecd587ba6f015db3948987cc2679eb444d6490807268e02f71729c89772f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e15c5bc223e2e2d4132b2e5f0d37bc1b6ab50ef8c56f7af75904a36d3d63fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73399183e2796b5ed1b3d249d85c0b6b1344f1519f8793f3892c9e971e10d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadWorkloadProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApphubWorkloadWorkloadProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadWorkloadProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadWorkloadPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadWorkloadPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b3238a66e9ebb4bf4259ebc6edf4927d66922177e8aac59845ff75a9f2df912)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubWorkloadWorkloadPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7232b842e3756255f1c3c8d198387b8e4ab8b38fdf372f493d0be65bee5e99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubWorkloadWorkloadPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9036bc33fe2eefbc5d4a4bd00ec7971981fbfac27529445109e053d5593f6915)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a79e93f5a326547087d5b37e540fddbf5e824b0c127801d4261fc0deb68f38d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cca96dea63d030c198ec2d72e7f1ad261b548db1837657ca3191acd155ae1fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApphubWorkloadWorkloadPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadWorkloadPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8744f5b6388c7d371982e88138285d75a6d2613bc84b39116d27d3e5605b3273)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="gcpProject")
    def gcp_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpProject"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubWorkloadWorkloadProperties]:
        return typing.cast(typing.Optional[ApphubWorkloadWorkloadProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubWorkloadWorkloadProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9579b5da49560341fd2f2152f25d81def7afcdfae285b11baa30ffa3171bacfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadWorkloadReference",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApphubWorkloadWorkloadReference:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApphubWorkloadWorkloadReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApphubWorkloadWorkloadReferenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadWorkloadReferenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__489c48e75e0961a5fb38ddd49cfd5347c386a7c5c9efbb2d2846b5b085e1be4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApphubWorkloadWorkloadReferenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a56ff7b708fb40f8aaecc7dc7081f7d20f2c49d15f1bcc19dc0b483da82c53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApphubWorkloadWorkloadReferenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb22565a2971ea073c45d308f5f1ac29e8c8234f45e415abbfb0d9ebebef3fcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__182ace99c9b883216d782b18fce7e7b30497e80fa714f8069a95a18358a6fb67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7469aa25d9c31925acd2f3411d94942d58ce4ab559db7c093251439975687b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApphubWorkloadWorkloadReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apphubWorkload.ApphubWorkloadWorkloadReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ee3dc0a0fe6fb6bf783619383d9fa0371624511423ec72ff3784e32f8433b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApphubWorkloadWorkloadReference]:
        return typing.cast(typing.Optional[ApphubWorkloadWorkloadReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApphubWorkloadWorkloadReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa822f5b7831dabc9e7e5720cb3c0915b6eb0fa51653e719fe7317489ffcbafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApphubWorkload",
    "ApphubWorkloadAttributes",
    "ApphubWorkloadAttributesBusinessOwners",
    "ApphubWorkloadAttributesBusinessOwnersList",
    "ApphubWorkloadAttributesBusinessOwnersOutputReference",
    "ApphubWorkloadAttributesCriticality",
    "ApphubWorkloadAttributesCriticalityOutputReference",
    "ApphubWorkloadAttributesDeveloperOwners",
    "ApphubWorkloadAttributesDeveloperOwnersList",
    "ApphubWorkloadAttributesDeveloperOwnersOutputReference",
    "ApphubWorkloadAttributesEnvironment",
    "ApphubWorkloadAttributesEnvironmentOutputReference",
    "ApphubWorkloadAttributesOperatorOwners",
    "ApphubWorkloadAttributesOperatorOwnersList",
    "ApphubWorkloadAttributesOperatorOwnersOutputReference",
    "ApphubWorkloadAttributesOutputReference",
    "ApphubWorkloadConfig",
    "ApphubWorkloadTimeouts",
    "ApphubWorkloadTimeoutsOutputReference",
    "ApphubWorkloadWorkloadProperties",
    "ApphubWorkloadWorkloadPropertiesList",
    "ApphubWorkloadWorkloadPropertiesOutputReference",
    "ApphubWorkloadWorkloadReference",
    "ApphubWorkloadWorkloadReferenceList",
    "ApphubWorkloadWorkloadReferenceOutputReference",
]

publication.publish()

def _typecheckingstub__8c894267a27498a73e515a2e6e3706cf2953cc8f09e3486196a419d1dd00a882(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_id: builtins.str,
    discovered_workload: builtins.str,
    location: builtins.str,
    workload_id: builtins.str,
    attributes: typing.Optional[typing.Union[ApphubWorkloadAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApphubWorkloadTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__652aa7fd3b6912640ce6cff034a6a28cabe896afe5b740a9c0a2e2d1e25c8716(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ac094832101b417ce29716d16791ff620084f9752d2f77bc47696101c65af1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9dc0a8acfbd9b6a791233165b52b6fcd015a3617e4da67231fb836679944fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81db90b946843ebc238a56ee5eb14525be9dcb373933e59f8843f806301abfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cbedcbade0f9fcfe50c37f59127a89bee02d53c6145022822e985989787e54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9c724a028fd3640c2abddf9a1af96b34aedb8b37e5a30065efb51fa5b2606d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e789f93dcc5ad5eef686664e40d9778e581069874f537ec4cfbbe30d4c6d48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f60beeba6abfa75a952ef7d12a0b8eb4188c7c70cd9896786b2d06776adcae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146f91a6d5c6aa69b1cfe0ba23fdda1ce2a7461a43e637c2dec598215486aab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebb5d0f6849a0e17315906e8e7b324940416aec9f4b7ccac46491380f8950ca(
    *,
    business_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesBusinessOwners, typing.Dict[builtins.str, typing.Any]]]]] = None,
    criticality: typing.Optional[typing.Union[ApphubWorkloadAttributesCriticality, typing.Dict[builtins.str, typing.Any]]] = None,
    developer_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesDeveloperOwners, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environment: typing.Optional[typing.Union[ApphubWorkloadAttributesEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    operator_owners: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesOperatorOwners, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86fe9cf86e835a46f908b757bd5950fc39cdd14b6866a0e87ddc9c09a9a0758(
    *,
    email: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f51460c08dca69c6f0fe57576c345cda6f608d95f1856124acba2e8e05a38d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425adeb2c7bfc2ef5874201527f49cd67c89b1a10ddb9dcfb62a123eaebdba91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd654ae1d87a146afe61e93329d6850430f860451990952c4bdda9b3e9990317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0755120e923f21c688b159873e73902ccc8028c1876af61c57459276190bcab8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7790cffa98f1f006ac193d2f79453244778cea167af0ea637e3a667f5908a3bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba61d1341149f54fa4dbc4c1ab62a075d7faee3d851534652f238c25066c8616(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesBusinessOwners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bb21fdffe3b4b5c64def9201b9795b01dc691bb71e8dd2e52ca46c02419018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4670140563c562772996ffc664c2e71ef41c7be305f6eb60bfc9c53e34a5e238(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada75f59f9165f42669971a271851c0a0a2edb31d8e3d0d9d8b3bad936161a70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e9545343c836202c2548cbd39da2c899e3129f8baaeb76dd5e3d139bed4970(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesBusinessOwners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e98c445ef735bc7ad44258cadb8b9bf860533f72bd6f257160ae0a0e83be75b(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931544f9a23473632f26db966968fb65643496889b4e1b0211e04885ace340b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa361ee709fb268435e7eb73c9cac5fe060e74163d86f1d8759255052ef2b99e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd28e0d5dcd4726a5475214432a9b34dc03c5c1fcd6f1a601479642816494ee(
    value: typing.Optional[ApphubWorkloadAttributesCriticality],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d3bc708be042fbd2ac43875b6750a5999acb6cb2bd439c9684924014636888(
    *,
    email: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf777bc66a96ccf7b8fa0cf211ed19c23482b05a6726c7925067412dc13c6bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80221730937932209cb2437231e01a1740cd18efa1d02907ddb56b34dfdee4be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680fb2256364dc5f7f4ca8f0cad247a77b4cc7739ca3d9de23a4532c78e53dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065d51828710f386572fdbef0053ff0772627089fe330e280b0592e487e7e52e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51723f9e609937c504483d2ed18dcf4d5158a11dcee09c0ba895cc5787eaaeca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622beb5de773a15c7a580d02010d84282a3e36f25be00ebff30c48b8e04e3edc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesDeveloperOwners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9707db9ffca992749f6788bd02a67fb14781827cd7f5f381e143a0ebdc02dd5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c024c1c095a3be85f1eb4d37e3f2434112bd1708af66ca306eb79172baeb9565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8aab605cd0464cafc39b7f5cc0df7994f2093143e0d01a7c5d1c5be2d50880(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4365cfd492126f12d7862dc80d5d1ec94299ae8ec3191da7238e878bb8c5a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesDeveloperOwners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8724601c61fd55b43e87e0cd7219e9a05c7d7f69ed9e27d98b392a72c951958(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed7f64e307d5f8e5d2144d9ec6c8d5a5b80d51ef9d5c6ce41f519c0b7033511(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10106bc72023ca63ae5960e45244a5c1e38f5bae4111bc90007c447caf63f611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8932d85e5ea222d420b2eefa4a269b7cc7ac2b083f7b66432d8241dc552ed4(
    value: typing.Optional[ApphubWorkloadAttributesEnvironment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8da06818e99252de4db3a57910e58bbfd009ebe0e8fe7b9bbadad47c00475f2(
    *,
    email: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f77b8e29aa9acc767633fdc924fde35926c7091a5912eff7b5f19460f1772fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bd6fd93595ac2962d0c984b3a7a984d412ea136fe646fc2a9acc2767db3b31(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b33a4bb9ccda95a8028ce9fa34b0ebd9b710e602bf4debea6da08902f2277a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914428d48bee87a84c7f753a059a2699533c9840e517cc543f9e78435915300f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc9f0eb29828219c85b9d70c3ee8537796edd1a731b36381e80c6468ea9ff7d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c83e021a92a26456d3b6ccda73ac84c9d8836a41a1201c251df0fbed3a0279(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApphubWorkloadAttributesOperatorOwners]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4021d1e6050131ffb5a142adc23b16f0ff297ec8796ea219d22d863a8f331b22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300828bdbb91d5821475bd865f126f0bb4f36946a5be589124dc6ea73aef9620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36b23e27ec1f91bde9e2a2f4f799fcd0acc9fbb000d13a8e5282335a707d3fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a386751d2e236a2fbd7e80dd801b501af2346b8ab6d323272e1913f0aaf6664(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadAttributesOperatorOwners]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad6c18b5cf72fe40788bcc6cc8fd24aac39f10e5c947f3b332045d9ba77045f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebb59286ecc35f219a6edc3af653fbba79408a5e9bdf952634ef07c8efdbf7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesBusinessOwners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf9cffc31c139d39438d5acb6ac71a9d5be6ed557aff0e9012af42b5c651951(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesDeveloperOwners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab502d89e08e112e304b02b3d071b65e9251b1222178fedb6fc0f8265fe21858(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApphubWorkloadAttributesOperatorOwners, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197d871356481d231393658e3a53c9f037677eb5b3fb3cf3d1eee94eab28f997(
    value: typing.Optional[ApphubWorkloadAttributes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1da8c9dc287263b4e72047c550a3fdd9a21defac3da811146cb761a313cd21d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_id: builtins.str,
    discovered_workload: builtins.str,
    location: builtins.str,
    workload_id: builtins.str,
    attributes: typing.Optional[typing.Union[ApphubWorkloadAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApphubWorkloadTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8776f4c1ee081d3a26f088453850eb0f089302f433b94ea74fdd7a68214050(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a308e024ed7950c4c798030bffb956c5279549582af72530972b1b319b16e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75efeba28f873010eba9ae48f6c5e458650e5671787efc32be714fe23e477d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf4ecd587ba6f015db3948987cc2679eb444d6490807268e02f71729c89772f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e15c5bc223e2e2d4132b2e5f0d37bc1b6ab50ef8c56f7af75904a36d3d63fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73399183e2796b5ed1b3d249d85c0b6b1344f1519f8793f3892c9e971e10d09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApphubWorkloadTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3238a66e9ebb4bf4259ebc6edf4927d66922177e8aac59845ff75a9f2df912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7232b842e3756255f1c3c8d198387b8e4ab8b38fdf372f493d0be65bee5e99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9036bc33fe2eefbc5d4a4bd00ec7971981fbfac27529445109e053d5593f6915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a79e93f5a326547087d5b37e540fddbf5e824b0c127801d4261fc0deb68f38d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca96dea63d030c198ec2d72e7f1ad261b548db1837657ca3191acd155ae1fa5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8744f5b6388c7d371982e88138285d75a6d2613bc84b39116d27d3e5605b3273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9579b5da49560341fd2f2152f25d81def7afcdfae285b11baa30ffa3171bacfe(
    value: typing.Optional[ApphubWorkloadWorkloadProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489c48e75e0961a5fb38ddd49cfd5347c386a7c5c9efbb2d2846b5b085e1be4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a56ff7b708fb40f8aaecc7dc7081f7d20f2c49d15f1bcc19dc0b483da82c53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb22565a2971ea073c45d308f5f1ac29e8c8234f45e415abbfb0d9ebebef3fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182ace99c9b883216d782b18fce7e7b30497e80fa714f8069a95a18358a6fb67(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7469aa25d9c31925acd2f3411d94942d58ce4ab559db7c093251439975687b1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ee3dc0a0fe6fb6bf783619383d9fa0371624511423ec72ff3784e32f8433b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa822f5b7831dabc9e7e5720cb3c0915b6eb0fa51653e719fe7317489ffcbafe(
    value: typing.Optional[ApphubWorkloadWorkloadReference],
) -> None:
    """Type checking stubs"""
    pass
