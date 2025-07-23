r'''
# `google_bigquery_dataset_access`

Refer to the Terraform Registry for docs: [`google_bigquery_dataset_access`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access).
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


class BigqueryDatasetAccessA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access google_bigquery_dataset_access}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        condition: typing.Optional[typing.Union["BigqueryDatasetAccessConditionA", typing.Dict[builtins.str, typing.Any]]] = None,
        dataset: typing.Optional[typing.Union["BigqueryDatasetAccessDatasetA", typing.Dict[builtins.str, typing.Any]]] = None,
        domain: typing.Optional[builtins.str] = None,
        group_by_email: typing.Optional[builtins.str] = None,
        iam_member: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        routine: typing.Optional[typing.Union["BigqueryDatasetAccessRoutineA", typing.Dict[builtins.str, typing.Any]]] = None,
        special_group: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDatasetAccessTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_by_email: typing.Optional[builtins.str] = None,
        view: typing.Optional[typing.Union["BigqueryDatasetAccessViewA", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access google_bigquery_dataset_access} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#condition BigqueryDatasetAccessA#condition}
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset BigqueryDatasetAccessA#dataset}
        :param domain: A domain to grant access to. Any users signed in with the domain specified will be granted the specified access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#domain BigqueryDatasetAccessA#domain}
        :param group_by_email: An email address of a Google Group to grant access to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#group_by_email BigqueryDatasetAccessA#group_by_email}
        :param iam_member: Some other type of member that appears in the IAM Policy but isn't a user, group, domain, or special group. For example: 'allUsers' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#iam_member BigqueryDatasetAccessA#iam_member}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#id BigqueryDatasetAccessA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project BigqueryDatasetAccessA#project}.
        :param role: Describes the rights granted to the user specified by the other member of the access object. Basic, predefined, and custom roles are supported. Predefined roles that have equivalent basic roles are swapped by the API to their basic counterparts, and will show a diff post-create. See `official docs <https://cloud.google.com/bigquery/docs/access-control>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#role BigqueryDatasetAccessA#role}
        :param routine: routine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#routine BigqueryDatasetAccessA#routine}
        :param special_group: A special group to grant access to. Possible values include: - 'projectOwners': Owners of the enclosing project. - 'projectReaders': Readers of the enclosing project. - 'projectWriters': Writers of the enclosing project. - 'allAuthenticatedUsers': All authenticated BigQuery users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#special_group BigqueryDatasetAccessA#special_group}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#timeouts BigqueryDatasetAccessA#timeouts}
        :param user_by_email: An email address of a user to grant access to. For example: fred@example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#user_by_email BigqueryDatasetAccessA#user_by_email}
        :param view: view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#view BigqueryDatasetAccessA#view}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a43c310b999acb5493b8cb2cf0adb79cb4ee9e05d6bc8ff6d5cf9f448abe0b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryDatasetAccessAConfig(
            dataset_id=dataset_id,
            condition=condition,
            dataset=dataset,
            domain=domain,
            group_by_email=group_by_email,
            iam_member=iam_member,
            id=id,
            project=project,
            role=role,
            routine=routine,
            special_group=special_group,
            timeouts=timeouts,
            user_by_email=user_by_email,
            view=view,
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
        '''Generates CDKTF code for importing a BigqueryDatasetAccessA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryDatasetAccessA to import.
        :param import_from_id: The id of the existing BigqueryDatasetAccessA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryDatasetAccessA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0ee15e638bce407c626fce431fc98d2ecd24d8489d18c32ad96911fc2bc598)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#expression BigqueryDatasetAccessA#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#description BigqueryDatasetAccessA#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#location BigqueryDatasetAccessA#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#title BigqueryDatasetAccessA#title}
        '''
        value = BigqueryDatasetAccessConditionA(
            expression=expression,
            description=description,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        dataset: typing.Union["BigqueryDatasetAccessDatasetDatasetA", typing.Dict[builtins.str, typing.Any]],
        target_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset BigqueryDatasetAccessA#dataset}
        :param target_types: Which resources in the dataset this entry applies to. Currently, only views are supported, but additional target types may be added in the future. Possible values: VIEWS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#target_types BigqueryDatasetAccessA#target_types}
        '''
        value = BigqueryDatasetAccessDatasetA(
            dataset=dataset, target_types=target_types
        )

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @jsii.member(jsii_name="putRoutine")
    def put_routine(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        routine_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        :param routine_id: The ID of the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#routine_id BigqueryDatasetAccessA#routine_id}
        '''
        value = BigqueryDatasetAccessRoutineA(
            dataset_id=dataset_id, project_id=project_id, routine_id=routine_id
        )

        return typing.cast(None, jsii.invoke(self, "putRoutine", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#create BigqueryDatasetAccessA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#delete BigqueryDatasetAccessA#delete}.
        '''
        value = BigqueryDatasetAccessTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putView")
    def put_view(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#table_id BigqueryDatasetAccessA#table_id}
        '''
        value = BigqueryDatasetAccessViewA(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putView", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDataset")
    def reset_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataset", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetGroupByEmail")
    def reset_group_by_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupByEmail", []))

    @jsii.member(jsii_name="resetIamMember")
    def reset_iam_member(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamMember", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetRoutine")
    def reset_routine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutine", []))

    @jsii.member(jsii_name="resetSpecialGroup")
    def reset_special_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecialGroup", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserByEmail")
    def reset_user_by_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserByEmail", []))

    @jsii.member(jsii_name="resetView")
    def reset_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetView", []))

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
    @jsii.member(jsii_name="apiUpdatedMember")
    def api_updated_member(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "apiUpdatedMember"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> "BigqueryDatasetAccessConditionAOutputReference":
        return typing.cast("BigqueryDatasetAccessConditionAOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> "BigqueryDatasetAccessDatasetAOutputReference":
        return typing.cast("BigqueryDatasetAccessDatasetAOutputReference", jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="routine")
    def routine(self) -> "BigqueryDatasetAccessRoutineAOutputReference":
        return typing.cast("BigqueryDatasetAccessRoutineAOutputReference", jsii.get(self, "routine"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryDatasetAccessTimeoutsOutputReference":
        return typing.cast("BigqueryDatasetAccessTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="view")
    def view(self) -> "BigqueryDatasetAccessViewAOutputReference":
        return typing.cast("BigqueryDatasetAccessViewAOutputReference", jsii.get(self, "view"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional["BigqueryDatasetAccessConditionA"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessConditionA"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional["BigqueryDatasetAccessDatasetA"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessDatasetA"], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByEmailInput")
    def group_by_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupByEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="iamMemberInput")
    def iam_member_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamMemberInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="routineInput")
    def routine_input(self) -> typing.Optional["BigqueryDatasetAccessRoutineA"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessRoutineA"], jsii.get(self, "routineInput"))

    @builtins.property
    @jsii.member(jsii_name="specialGroupInput")
    def special_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specialGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryDatasetAccessTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryDatasetAccessTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userByEmailInput")
    def user_by_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userByEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="viewInput")
    def view_input(self) -> typing.Optional["BigqueryDatasetAccessViewA"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessViewA"], jsii.get(self, "viewInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae6e4b4491d417b11dfd6c83c5eae4081511b5ce9887769ce90b2451ccdd1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb772d6c5a393311c2c28cfbe616729a777c82a05908f74c3751cbd8967a488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupByEmail")
    def group_by_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupByEmail"))

    @group_by_email.setter
    def group_by_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23fe0ef100657287d37ea261820f357229a765df4ec5ba56e349feef4e90034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupByEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamMember")
    def iam_member(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamMember"))

    @iam_member.setter
    def iam_member(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f138e03c3afc295f867ca6351e417998876b9a0d4b2cd7cb7988f1bb44c8c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamMember", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de07ea8630a749d47361b80f7ea24f9f08abb508e21eca22d268538a2857a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bff1801ede6fc1f8c8f3713f90826c86b295cc63bb4525e9685e5816b6c878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd8dee514e0d4d7ce938c688e85f7e064f2de0f1aba3425ec335e1a554759b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specialGroup")
    def special_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specialGroup"))

    @special_group.setter
    def special_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5624b76611f1c3f865470df03bf92d578be80dff293db2e262f62e11491fe20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specialGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userByEmail")
    def user_by_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userByEmail"))

    @user_by_email.setter
    def user_by_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bf506f6c6dfbdd85b2b0067ad73fb8472851cc03ca6f524dc8fee6d9fcef32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userByEmail", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset_id": "datasetId",
        "condition": "condition",
        "dataset": "dataset",
        "domain": "domain",
        "group_by_email": "groupByEmail",
        "iam_member": "iamMember",
        "id": "id",
        "project": "project",
        "role": "role",
        "routine": "routine",
        "special_group": "specialGroup",
        "timeouts": "timeouts",
        "user_by_email": "userByEmail",
        "view": "view",
    },
)
class BigqueryDatasetAccessAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset_id: builtins.str,
        condition: typing.Optional[typing.Union["BigqueryDatasetAccessConditionA", typing.Dict[builtins.str, typing.Any]]] = None,
        dataset: typing.Optional[typing.Union["BigqueryDatasetAccessDatasetA", typing.Dict[builtins.str, typing.Any]]] = None,
        domain: typing.Optional[builtins.str] = None,
        group_by_email: typing.Optional[builtins.str] = None,
        iam_member: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        routine: typing.Optional[typing.Union["BigqueryDatasetAccessRoutineA", typing.Dict[builtins.str, typing.Any]]] = None,
        special_group: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDatasetAccessTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_by_email: typing.Optional[builtins.str] = None,
        view: typing.Optional[typing.Union["BigqueryDatasetAccessViewA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#condition BigqueryDatasetAccessA#condition}
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset BigqueryDatasetAccessA#dataset}
        :param domain: A domain to grant access to. Any users signed in with the domain specified will be granted the specified access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#domain BigqueryDatasetAccessA#domain}
        :param group_by_email: An email address of a Google Group to grant access to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#group_by_email BigqueryDatasetAccessA#group_by_email}
        :param iam_member: Some other type of member that appears in the IAM Policy but isn't a user, group, domain, or special group. For example: 'allUsers' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#iam_member BigqueryDatasetAccessA#iam_member}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#id BigqueryDatasetAccessA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project BigqueryDatasetAccessA#project}.
        :param role: Describes the rights granted to the user specified by the other member of the access object. Basic, predefined, and custom roles are supported. Predefined roles that have equivalent basic roles are swapped by the API to their basic counterparts, and will show a diff post-create. See `official docs <https://cloud.google.com/bigquery/docs/access-control>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#role BigqueryDatasetAccessA#role}
        :param routine: routine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#routine BigqueryDatasetAccessA#routine}
        :param special_group: A special group to grant access to. Possible values include: - 'projectOwners': Owners of the enclosing project. - 'projectReaders': Readers of the enclosing project. - 'projectWriters': Writers of the enclosing project. - 'allAuthenticatedUsers': All authenticated BigQuery users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#special_group BigqueryDatasetAccessA#special_group}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#timeouts BigqueryDatasetAccessA#timeouts}
        :param user_by_email: An email address of a user to grant access to. For example: fred@example.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#user_by_email BigqueryDatasetAccessA#user_by_email}
        :param view: view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#view BigqueryDatasetAccessA#view}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = BigqueryDatasetAccessConditionA(**condition)
        if isinstance(dataset, dict):
            dataset = BigqueryDatasetAccessDatasetA(**dataset)
        if isinstance(routine, dict):
            routine = BigqueryDatasetAccessRoutineA(**routine)
        if isinstance(timeouts, dict):
            timeouts = BigqueryDatasetAccessTimeouts(**timeouts)
        if isinstance(view, dict):
            view = BigqueryDatasetAccessViewA(**view)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70993885af44f6d98cef882ba094a467109dcefa09bdd65085226a6c9a4313a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument group_by_email", value=group_by_email, expected_type=type_hints["group_by_email"])
            check_type(argname="argument iam_member", value=iam_member, expected_type=type_hints["iam_member"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument routine", value=routine, expected_type=type_hints["routine"])
            check_type(argname="argument special_group", value=special_group, expected_type=type_hints["special_group"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_by_email", value=user_by_email, expected_type=type_hints["user_by_email"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
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
        if condition is not None:
            self._values["condition"] = condition
        if dataset is not None:
            self._values["dataset"] = dataset
        if domain is not None:
            self._values["domain"] = domain
        if group_by_email is not None:
            self._values["group_by_email"] = group_by_email
        if iam_member is not None:
            self._values["iam_member"] = iam_member
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if role is not None:
            self._values["role"] = role
        if routine is not None:
            self._values["routine"] = routine
        if special_group is not None:
            self._values["special_group"] = special_group
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_by_email is not None:
            self._values["user_by_email"] = user_by_email
        if view is not None:
            self._values["view"] = view

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
    def dataset_id(self) -> builtins.str:
        '''A unique ID for this dataset, without the project name.

        The ID
        must contain only letters (a-z, A-Z), numbers (0-9), or
        underscores (_). The maximum length is 1,024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional["BigqueryDatasetAccessConditionA"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#condition BigqueryDatasetAccessA#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["BigqueryDatasetAccessConditionA"], result)

    @builtins.property
    def dataset(self) -> typing.Optional["BigqueryDatasetAccessDatasetA"]:
        '''dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset BigqueryDatasetAccessA#dataset}
        '''
        result = self._values.get("dataset")
        return typing.cast(typing.Optional["BigqueryDatasetAccessDatasetA"], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''A domain to grant access to. Any users signed in with the domain specified will be granted the specified access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#domain BigqueryDatasetAccessA#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_by_email(self) -> typing.Optional[builtins.str]:
        '''An email address of a Google Group to grant access to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#group_by_email BigqueryDatasetAccessA#group_by_email}
        '''
        result = self._values.get("group_by_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_member(self) -> typing.Optional[builtins.str]:
        '''Some other type of member that appears in the IAM Policy but isn't a user, group, domain, or special group.

        For example: 'allUsers'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#iam_member BigqueryDatasetAccessA#iam_member}
        '''
        result = self._values.get("iam_member")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#id BigqueryDatasetAccessA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project BigqueryDatasetAccessA#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''Describes the rights granted to the user specified by the other member of the access object.

        Basic, predefined, and custom roles are
        supported. Predefined roles that have equivalent basic roles are
        swapped by the API to their basic counterparts, and will show a diff
        post-create. See
        `official docs <https://cloud.google.com/bigquery/docs/access-control>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#role BigqueryDatasetAccessA#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routine(self) -> typing.Optional["BigqueryDatasetAccessRoutineA"]:
        '''routine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#routine BigqueryDatasetAccessA#routine}
        '''
        result = self._values.get("routine")
        return typing.cast(typing.Optional["BigqueryDatasetAccessRoutineA"], result)

    @builtins.property
    def special_group(self) -> typing.Optional[builtins.str]:
        '''A special group to grant access to.

        Possible values include:

        - 'projectOwners': Owners of the enclosing project.
        - 'projectReaders': Readers of the enclosing project.
        - 'projectWriters': Writers of the enclosing project.
        - 'allAuthenticatedUsers': All authenticated BigQuery users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#special_group BigqueryDatasetAccessA#special_group}
        '''
        result = self._values.get("special_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryDatasetAccessTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#timeouts BigqueryDatasetAccessA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryDatasetAccessTimeouts"], result)

    @builtins.property
    def user_by_email(self) -> typing.Optional[builtins.str]:
        '''An email address of a user to grant access to. For example: fred@example.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#user_by_email BigqueryDatasetAccessA#user_by_email}
        '''
        result = self._values.get("user_by_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view(self) -> typing.Optional["BigqueryDatasetAccessViewA"]:
        '''view block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#view BigqueryDatasetAccessA#view}
        '''
        result = self._values.get("view")
        return typing.cast(typing.Optional["BigqueryDatasetAccessViewA"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessConditionA",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "description": "description",
        "location": "location",
        "title": "title",
    },
)
class BigqueryDatasetAccessConditionA:
    def __init__(
        self,
        *,
        expression: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#expression BigqueryDatasetAccessA#expression}
        :param description: Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#description BigqueryDatasetAccessA#description}
        :param location: String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#location BigqueryDatasetAccessA#location}
        :param title: Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#title BigqueryDatasetAccessA#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33729e1f88f6731f856aa9b1b03c54f61b7eb73814d705ee09690cbf9606fbd1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#expression BigqueryDatasetAccessA#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the expression.

        This is a longer text which describes the expression,
        e.g. when hovered over it in a UI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#description BigqueryDatasetAccessA#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#location BigqueryDatasetAccessA#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#title BigqueryDatasetAccessA#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessConditionA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessConditionAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessConditionAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f70aa8316c090461e7ad6d136bdc6fa9961f8e24dae03959759a51e93e4df7aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__222b52ff65b9c8a85e53c68a7c6030ef45365c80b065d00c8be0966f7ffb2aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686c1bfe2d94835d79a1698a0e249f2c554677efcccc31217d19bede574c6887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c583753bdd8ba56c5cda6a6016cbda5b9317a0e105bb29c7dcb9e74ef29355b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8713d7ded15e5db0e8e72c8defb0db2287be976a55285c3f5e5bca14723cf95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessConditionA]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessConditionA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessConditionA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb10af04590ce55398789f9c545ea42518bc86e762ad9d893fa57691f8389768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessDatasetA",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset", "target_types": "targetTypes"},
)
class BigqueryDatasetAccessDatasetA:
    def __init__(
        self,
        *,
        dataset: typing.Union["BigqueryDatasetAccessDatasetDatasetA", typing.Dict[builtins.str, typing.Any]],
        target_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset BigqueryDatasetAccessA#dataset}
        :param target_types: Which resources in the dataset this entry applies to. Currently, only views are supported, but additional target types may be added in the future. Possible values: VIEWS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#target_types BigqueryDatasetAccessA#target_types}
        '''
        if isinstance(dataset, dict):
            dataset = BigqueryDatasetAccessDatasetDatasetA(**dataset)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fbcae22b567d36868aea1bcf0686d65e8d6769076ada8a099a64d58477ba5f)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument target_types", value=target_types, expected_type=type_hints["target_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
            "target_types": target_types,
        }

    @builtins.property
    def dataset(self) -> "BigqueryDatasetAccessDatasetDatasetA":
        '''dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset BigqueryDatasetAccessA#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast("BigqueryDatasetAccessDatasetDatasetA", result)

    @builtins.property
    def target_types(self) -> typing.List[builtins.str]:
        '''Which resources in the dataset this entry applies to.

        Currently, only views are supported,
        but additional target types may be added in the future. Possible values: VIEWS

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#target_types BigqueryDatasetAccessA#target_types}
        '''
        result = self._values.get("target_types")
        assert result is not None, "Required property 'target_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessDatasetA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessDatasetAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessDatasetAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afe090f1501b76aae438e1013c4670ad95187fd180c128c8c590340555dfc555)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        '''
        value = BigqueryDatasetAccessDatasetDatasetA(
            dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> "BigqueryDatasetAccessDatasetDatasetAOutputReference":
        return typing.cast("BigqueryDatasetAccessDatasetDatasetAOutputReference", jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional["BigqueryDatasetAccessDatasetDatasetA"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessDatasetDatasetA"], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTypesInput")
    def target_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTypes")
    def target_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetTypes"))

    @target_types.setter
    def target_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a9c9c4afa85fb1c5170f31c3437a652a00e60f111ada6f40a177e1486e5e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessDatasetA]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessDatasetA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessDatasetA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5cb5f7d005105047d481692df3e44373fa498e4059a356c7a962047b1e882c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessDatasetDatasetA",
    jsii_struct_bases=[],
    name_mapping={"dataset_id": "datasetId", "project_id": "projectId"},
)
class BigqueryDatasetAccessDatasetDatasetA:
    def __init__(self, *, dataset_id: builtins.str, project_id: builtins.str) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089fa717f9d5f51f125714da55b35483ae39eb62906da9d65c464b771039dbfb)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessDatasetDatasetA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessDatasetDatasetAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessDatasetDatasetAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__506e2d033c682849d0c87105ad5759dd851c122c6dd279e222b88ee5d5c77385)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb00568ad5a5a30062dd85a0babdad28441eb559acf484f1cb508a1e9975b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debc7ae6deb5eb1078873f5bc37221a576d93ad0ef123ee4ae8457310ecc050b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessDatasetDatasetA]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessDatasetDatasetA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessDatasetDatasetA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd2d293b6e7b0621953f1ab99c5c58c20aafe07444bb8a4e3d72b2fa9f32f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessRoutineA",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "routine_id": "routineId",
    },
)
class BigqueryDatasetAccessRoutineA:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        routine_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        :param routine_id: The ID of the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#routine_id BigqueryDatasetAccessA#routine_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5f22999a96f7f3a3471a49f74ea6f4cc16d1b1ff659720a4fe1c20757e23c1)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument routine_id", value=routine_id, expected_type=type_hints["routine_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
            "routine_id": routine_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_id(self) -> builtins.str:
        '''The ID of the routine.

        The ID must contain only letters (a-z,
        A-Z), numbers (0-9), or underscores (_). The maximum length
        is 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#routine_id BigqueryDatasetAccessA#routine_id}
        '''
        result = self._values.get("routine_id")
        assert result is not None, "Required property 'routine_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessRoutineA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessRoutineAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessRoutineAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e6f4f113fc62023ff594dd217899e95d1f777d7420193ebc37a0ea393d96dec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routineIdInput")
    def routine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f8a9ae3889d1951e38b1c681444d358f62ec2a00d10b405df355f476ca30cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5839864d2d53c39807bbe5ae6101c5a1031e7749d8cc194de3008d2502122f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routineId")
    def routine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineId"))

    @routine_id.setter
    def routine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddf8c6465e07914e55cf74d16172ba8307ceb40c8542ccde7597293257cde10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessRoutineA]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessRoutineA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessRoutineA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5079b115cea23292b54ef552c50891b96028cc00bc844748e4a71db049042799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class BigqueryDatasetAccessTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#create BigqueryDatasetAccessA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#delete BigqueryDatasetAccessA#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d910eaba22265398880ca87a7e34633038ef2bcd724207e3ecf220edfda67bf9)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#create BigqueryDatasetAccessA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#delete BigqueryDatasetAccessA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__717854df77c6622ef541bf3eec738a19c9debf5b4ebf8c0f15a6b1e9166b7934)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e8555dab0c6993f870829ab66b3f3009605e77c282e0d0008d623e025a02bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f371b004aa0d674a06cd2a507c6e96a33d13a654b632a64e336b84302a64a1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDatasetAccessTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDatasetAccessTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDatasetAccessTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f4fa90699178a141c0e512d2a97b58267f7633cec4637f091c8a13247c8375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessViewA",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class BigqueryDatasetAccessViewA:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#table_id BigqueryDatasetAccessA#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195d6323d3428ad600f76169ff9e06c7c15b8d1945f5dcb241d9b95fb6433c27)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
            "table_id": table_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#dataset_id BigqueryDatasetAccessA#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#project_id BigqueryDatasetAccessA#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The ID of the table.

        The ID must contain only letters (a-z,
        A-Z), numbers (0-9), or underscores (_). The maximum length
        is 1,024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_dataset_access#table_id BigqueryDatasetAccessA#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessViewA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessViewAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDatasetAccess.BigqueryDatasetAccessViewAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9fd8d3bcb4bc7042aa7ede65b1b20592faedf0172b1eaa0d114f23668520422)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19beff6fc41c5c0e271ab156052120d9fc3b6a11b6edea261e525616183c2501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb4e2d9cba55112fd83437ec7954adb8f9f1b436026852b68efb942f6c58a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49dd3236aca899483a2df067c050065c6b29c123d8ba3053c66d900d61852c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessViewA]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessViewA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessViewA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6ba28596ccdc3bfc488c60b581e764a12c3dca40350569ab22d3e2259e350c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryDatasetAccessA",
    "BigqueryDatasetAccessAConfig",
    "BigqueryDatasetAccessConditionA",
    "BigqueryDatasetAccessConditionAOutputReference",
    "BigqueryDatasetAccessDatasetA",
    "BigqueryDatasetAccessDatasetAOutputReference",
    "BigqueryDatasetAccessDatasetDatasetA",
    "BigqueryDatasetAccessDatasetDatasetAOutputReference",
    "BigqueryDatasetAccessRoutineA",
    "BigqueryDatasetAccessRoutineAOutputReference",
    "BigqueryDatasetAccessTimeouts",
    "BigqueryDatasetAccessTimeoutsOutputReference",
    "BigqueryDatasetAccessViewA",
    "BigqueryDatasetAccessViewAOutputReference",
]

publication.publish()

def _typecheckingstub__2a43c310b999acb5493b8cb2cf0adb79cb4ee9e05d6bc8ff6d5cf9f448abe0b0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    condition: typing.Optional[typing.Union[BigqueryDatasetAccessConditionA, typing.Dict[builtins.str, typing.Any]]] = None,
    dataset: typing.Optional[typing.Union[BigqueryDatasetAccessDatasetA, typing.Dict[builtins.str, typing.Any]]] = None,
    domain: typing.Optional[builtins.str] = None,
    group_by_email: typing.Optional[builtins.str] = None,
    iam_member: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    routine: typing.Optional[typing.Union[BigqueryDatasetAccessRoutineA, typing.Dict[builtins.str, typing.Any]]] = None,
    special_group: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryDatasetAccessTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_by_email: typing.Optional[builtins.str] = None,
    view: typing.Optional[typing.Union[BigqueryDatasetAccessViewA, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4e0ee15e638bce407c626fce431fc98d2ecd24d8489d18c32ad96911fc2bc598(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae6e4b4491d417b11dfd6c83c5eae4081511b5ce9887769ce90b2451ccdd1f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb772d6c5a393311c2c28cfbe616729a777c82a05908f74c3751cbd8967a488(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23fe0ef100657287d37ea261820f357229a765df4ec5ba56e349feef4e90034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f138e03c3afc295f867ca6351e417998876b9a0d4b2cd7cb7988f1bb44c8c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de07ea8630a749d47361b80f7ea24f9f08abb508e21eca22d268538a2857a82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bff1801ede6fc1f8c8f3713f90826c86b295cc63bb4525e9685e5816b6c878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd8dee514e0d4d7ce938c688e85f7e064f2de0f1aba3425ec335e1a554759b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5624b76611f1c3f865470df03bf92d578be80dff293db2e262f62e11491fe20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bf506f6c6dfbdd85b2b0067ad73fb8472851cc03ca6f524dc8fee6d9fcef32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70993885af44f6d98cef882ba094a467109dcefa09bdd65085226a6c9a4313a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_id: builtins.str,
    condition: typing.Optional[typing.Union[BigqueryDatasetAccessConditionA, typing.Dict[builtins.str, typing.Any]]] = None,
    dataset: typing.Optional[typing.Union[BigqueryDatasetAccessDatasetA, typing.Dict[builtins.str, typing.Any]]] = None,
    domain: typing.Optional[builtins.str] = None,
    group_by_email: typing.Optional[builtins.str] = None,
    iam_member: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    routine: typing.Optional[typing.Union[BigqueryDatasetAccessRoutineA, typing.Dict[builtins.str, typing.Any]]] = None,
    special_group: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryDatasetAccessTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_by_email: typing.Optional[builtins.str] = None,
    view: typing.Optional[typing.Union[BigqueryDatasetAccessViewA, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33729e1f88f6731f856aa9b1b03c54f61b7eb73814d705ee09690cbf9606fbd1(
    *,
    expression: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70aa8316c090461e7ad6d136bdc6fa9961f8e24dae03959759a51e93e4df7aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222b52ff65b9c8a85e53c68a7c6030ef45365c80b065d00c8be0966f7ffb2aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686c1bfe2d94835d79a1698a0e249f2c554677efcccc31217d19bede574c6887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c583753bdd8ba56c5cda6a6016cbda5b9317a0e105bb29c7dcb9e74ef29355b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8713d7ded15e5db0e8e72c8defb0db2287be976a55285c3f5e5bca14723cf95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb10af04590ce55398789f9c545ea42518bc86e762ad9d893fa57691f8389768(
    value: typing.Optional[BigqueryDatasetAccessConditionA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fbcae22b567d36868aea1bcf0686d65e8d6769076ada8a099a64d58477ba5f(
    *,
    dataset: typing.Union[BigqueryDatasetAccessDatasetDatasetA, typing.Dict[builtins.str, typing.Any]],
    target_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe090f1501b76aae438e1013c4670ad95187fd180c128c8c590340555dfc555(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a9c9c4afa85fb1c5170f31c3437a652a00e60f111ada6f40a177e1486e5e6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5cb5f7d005105047d481692df3e44373fa498e4059a356c7a962047b1e882c(
    value: typing.Optional[BigqueryDatasetAccessDatasetA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089fa717f9d5f51f125714da55b35483ae39eb62906da9d65c464b771039dbfb(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506e2d033c682849d0c87105ad5759dd851c122c6dd279e222b88ee5d5c77385(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb00568ad5a5a30062dd85a0babdad28441eb559acf484f1cb508a1e9975b68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debc7ae6deb5eb1078873f5bc37221a576d93ad0ef123ee4ae8457310ecc050b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd2d293b6e7b0621953f1ab99c5c58c20aafe07444bb8a4e3d72b2fa9f32f4a(
    value: typing.Optional[BigqueryDatasetAccessDatasetDatasetA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5f22999a96f7f3a3471a49f74ea6f4cc16d1b1ff659720a4fe1c20757e23c1(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    routine_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6f4f113fc62023ff594dd217899e95d1f777d7420193ebc37a0ea393d96dec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f8a9ae3889d1951e38b1c681444d358f62ec2a00d10b405df355f476ca30cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5839864d2d53c39807bbe5ae6101c5a1031e7749d8cc194de3008d2502122f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddf8c6465e07914e55cf74d16172ba8307ceb40c8542ccde7597293257cde10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5079b115cea23292b54ef552c50891b96028cc00bc844748e4a71db049042799(
    value: typing.Optional[BigqueryDatasetAccessRoutineA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d910eaba22265398880ca87a7e34633038ef2bcd724207e3ecf220edfda67bf9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717854df77c6622ef541bf3eec738a19c9debf5b4ebf8c0f15a6b1e9166b7934(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e8555dab0c6993f870829ab66b3f3009605e77c282e0d0008d623e025a02bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f371b004aa0d674a06cd2a507c6e96a33d13a654b632a64e336b84302a64a1f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f4fa90699178a141c0e512d2a97b58267f7633cec4637f091c8a13247c8375(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryDatasetAccessTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195d6323d3428ad600f76169ff9e06c7c15b8d1945f5dcb241d9b95fb6433c27(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fd8d3bcb4bc7042aa7ede65b1b20592faedf0172b1eaa0d114f23668520422(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19beff6fc41c5c0e271ab156052120d9fc3b6a11b6edea261e525616183c2501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb4e2d9cba55112fd83437ec7954adb8f9f1b436026852b68efb942f6c58a9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dd3236aca899483a2df067c050065c6b29c123d8ba3053c66d900d61852c67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6ba28596ccdc3bfc488c60b581e764a12c3dca40350569ab22d3e2259e350c(
    value: typing.Optional[BigqueryDatasetAccessViewA],
) -> None:
    """Type checking stubs"""
    pass
