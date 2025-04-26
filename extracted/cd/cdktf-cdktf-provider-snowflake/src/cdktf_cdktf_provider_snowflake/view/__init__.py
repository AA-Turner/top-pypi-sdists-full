r'''
# `snowflake_view`

Refer to the Terraform Registry for docs: [`snowflake_view`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view).
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


class View(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.View",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view snowflake_view}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        statement: builtins.str,
        aggregation_policy: typing.Optional[typing.Union["ViewAggregationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        change_tracking: typing.Optional[builtins.str] = None,
        column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ViewColumn", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_metric_function: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ViewDataMetricFunction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_metric_schedule: typing.Optional[typing.Union["ViewDataMetricSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_recursive: typing.Optional[builtins.str] = None,
        is_secure: typing.Optional[builtins.str] = None,
        is_temporary: typing.Optional[builtins.str] = None,
        row_access_policy: typing.Optional[typing.Union["ViewRowAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view snowflake_view} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the view. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#database View#database}
        :param name: Specifies the identifier for the view; must be unique for the schema in which the view is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#name View#name}
        :param schema: The schema in which to create the view. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#schema View#schema}
        :param statement: Specifies the query used to create the view. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#statement View#statement}
        :param aggregation_policy: aggregation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#aggregation_policy View#aggregation_policy}
        :param change_tracking: Specifies to enable or disable change tracking on the table. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#change_tracking View#change_tracking}
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#column View#column}
        :param comment: Specifies a comment for the view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#comment View#comment}
        :param copy_grants: Retains the access permissions from the original view when a view is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#copy_grants View#copy_grants}
        :param data_metric_function: data_metric_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#data_metric_function View#data_metric_function}
        :param data_metric_schedule: data_metric_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#data_metric_schedule View#data_metric_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#id View#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_recursive: Specifies that the view can refer to itself using recursive syntax without necessarily using a CTE (common table expression). Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_recursive View#is_recursive}
        :param is_secure: Specifies that the view is secure. By design, the Snowflake's ``SHOW VIEWS`` command does not provide information about secure views (consult `view usage notes <https://docs.snowflake.com/en/sql-reference/sql/create-view#usage-notes>`_) which is essential to manage/import view with Terraform. Use the role owning the view while managing secure views. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_secure View#is_secure}
        :param is_temporary: Specifies that the view persists only for the duration of the session that you created it in. A temporary view and all its contents are dropped at the end of the session. In context of this provider, it means that it's dropped after a Terraform operation. This results in a permanent plan with object creation. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_temporary View#is_temporary}
        :param row_access_policy: row_access_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#row_access_policy View#row_access_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0462f8da364bb0cc996ac2edd41517d2b2f5feaf2f8e302def5e65df13e864)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ViewConfig(
            database=database,
            name=name,
            schema=schema,
            statement=statement,
            aggregation_policy=aggregation_policy,
            change_tracking=change_tracking,
            column=column,
            comment=comment,
            copy_grants=copy_grants,
            data_metric_function=data_metric_function,
            data_metric_schedule=data_metric_schedule,
            id=id,
            is_recursive=is_recursive,
            is_secure=is_secure,
            is_temporary=is_temporary,
            row_access_policy=row_access_policy,
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
        '''Generates CDKTF code for importing a View resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the View to import.
        :param import_from_id: The id of the existing View that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the View to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71fdd2966d270044cf6cff34c439f863d0fe1bfc73fef6fdb43d777576d632e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAggregationPolicy")
    def put_aggregation_policy(
        self,
        *,
        policy_name: builtins.str,
        entity_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param policy_name: Aggregation policy name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        :param entity_key: Defines which columns uniquely identify an entity within the view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#entity_key View#entity_key}
        '''
        value = ViewAggregationPolicy(policy_name=policy_name, entity_key=entity_key)

        return typing.cast(None, jsii.invoke(self, "putAggregationPolicy", [value]))

    @jsii.member(jsii_name="putColumn")
    def put_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ViewColumn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8146c0ec022e2997332b204f376e3d9fd1aebf8a2de23df5c550984181c2b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumn", [value]))

    @jsii.member(jsii_name="putDataMetricFunction")
    def put_data_metric_function(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ViewDataMetricFunction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b39e18a45a59d46e6fb10318458188d877e6c3dbc27adb1a545439285a9825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataMetricFunction", [value]))

    @jsii.member(jsii_name="putDataMetricSchedule")
    def put_data_metric_schedule(
        self,
        *,
        minutes: typing.Optional[jsii.Number] = None,
        using_cron: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minutes: Specifies an interval (in minutes) of wait time inserted between runs of the data metric function. Conflicts with ``using_cron``. Valid values are: ``5`` | ``15`` | ``30`` | ``60`` | ``720`` | ``1440``. Due to Snowflake limitations, changes in this field are not managed by the provider. Please consider using `taint <https://developer.hashicorp.com/terraform/cli/commands/taint>`_ command, ``using_cron`` field, or `replace_triggered_by <https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#replace_triggered_by>`_ metadata argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#minutes View#minutes}
        :param using_cron: Specifies a cron expression and time zone for periodically running the data metric function. Supports a subset of standard cron utility syntax. Conflicts with ``minutes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#using_cron View#using_cron}
        '''
        value = ViewDataMetricSchedule(minutes=minutes, using_cron=using_cron)

        return typing.cast(None, jsii.invoke(self, "putDataMetricSchedule", [value]))

    @jsii.member(jsii_name="putRowAccessPolicy")
    def put_row_access_policy(
        self,
        *,
        on: typing.Sequence[builtins.str],
        policy_name: builtins.str,
    ) -> None:
        '''
        :param on: Defines which columns are affected by the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#on View#on}
        :param policy_name: Row access policy name. For more information about this resource, see `docs <./row_access_policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        value = ViewRowAccessPolicy(on=on, policy_name=policy_name)

        return typing.cast(None, jsii.invoke(self, "putRowAccessPolicy", [value]))

    @jsii.member(jsii_name="resetAggregationPolicy")
    def reset_aggregation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationPolicy", []))

    @jsii.member(jsii_name="resetChangeTracking")
    def reset_change_tracking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeTracking", []))

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCopyGrants")
    def reset_copy_grants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyGrants", []))

    @jsii.member(jsii_name="resetDataMetricFunction")
    def reset_data_metric_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataMetricFunction", []))

    @jsii.member(jsii_name="resetDataMetricSchedule")
    def reset_data_metric_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataMetricSchedule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsRecursive")
    def reset_is_recursive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRecursive", []))

    @jsii.member(jsii_name="resetIsSecure")
    def reset_is_secure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSecure", []))

    @jsii.member(jsii_name="resetIsTemporary")
    def reset_is_temporary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsTemporary", []))

    @jsii.member(jsii_name="resetRowAccessPolicy")
    def reset_row_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowAccessPolicy", []))

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
    @jsii.member(jsii_name="aggregationPolicy")
    def aggregation_policy(self) -> "ViewAggregationPolicyOutputReference":
        return typing.cast("ViewAggregationPolicyOutputReference", jsii.get(self, "aggregationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> "ViewColumnList":
        return typing.cast("ViewColumnList", jsii.get(self, "column"))

    @builtins.property
    @jsii.member(jsii_name="dataMetricFunction")
    def data_metric_function(self) -> "ViewDataMetricFunctionList":
        return typing.cast("ViewDataMetricFunctionList", jsii.get(self, "dataMetricFunction"))

    @builtins.property
    @jsii.member(jsii_name="dataMetricSchedule")
    def data_metric_schedule(self) -> "ViewDataMetricScheduleOutputReference":
        return typing.cast("ViewDataMetricScheduleOutputReference", jsii.get(self, "dataMetricSchedule"))

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "ViewDescribeOutputList":
        return typing.cast("ViewDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="rowAccessPolicy")
    def row_access_policy(self) -> "ViewRowAccessPolicyOutputReference":
        return typing.cast("ViewRowAccessPolicyOutputReference", jsii.get(self, "rowAccessPolicy"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ViewShowOutputList":
        return typing.cast("ViewShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationPolicyInput")
    def aggregation_policy_input(self) -> typing.Optional["ViewAggregationPolicy"]:
        return typing.cast(typing.Optional["ViewAggregationPolicy"], jsii.get(self, "aggregationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTrackingInput")
    def change_tracking_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "changeTrackingInput"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ViewColumn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ViewColumn"]]], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="copyGrantsInput")
    def copy_grants_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyGrantsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMetricFunctionInput")
    def data_metric_function_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ViewDataMetricFunction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ViewDataMetricFunction"]]], jsii.get(self, "dataMetricFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMetricScheduleInput")
    def data_metric_schedule_input(self) -> typing.Optional["ViewDataMetricSchedule"]:
        return typing.cast(typing.Optional["ViewDataMetricSchedule"], jsii.get(self, "dataMetricScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isRecursiveInput")
    def is_recursive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isRecursiveInput"))

    @builtins.property
    @jsii.member(jsii_name="isSecureInput")
    def is_secure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isSecureInput"))

    @builtins.property
    @jsii.member(jsii_name="isTemporaryInput")
    def is_temporary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isTemporaryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rowAccessPolicyInput")
    def row_access_policy_input(self) -> typing.Optional["ViewRowAccessPolicy"]:
        return typing.cast(typing.Optional["ViewRowAccessPolicy"], jsii.get(self, "rowAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="statementInput")
    def statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTracking")
    def change_tracking(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "changeTracking"))

    @change_tracking.setter
    def change_tracking(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ecf3e7641b58c7c70a5e9b5b9ca2785178000e8d428e4d2afa113c2fbbf52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeTracking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a872f963cb6f839357c360fed1880e3dca25f9cea4bd519fe535c9a45845401b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyGrants")
    def copy_grants(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyGrants"))

    @copy_grants.setter
    def copy_grants(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5f729bf67f2b2cb80711c8fb1c5e8b66237f1a66ec6621e74245cd4fe4d752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyGrants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e15403d909a79852aafc2fc4abd6662b1715eecafd152bd6488c3ede1170285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd1f1a3e85d62483b8f0a9bb868eb7ee89f5d579b55ea01afc583a8a44bcfdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isRecursive")
    def is_recursive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isRecursive"))

    @is_recursive.setter
    def is_recursive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6f4fce2cb615f6ff6d181cdd2d6fdc3ed5af4f9b81a042ffa43609f9ddce09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRecursive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isSecure"))

    @is_secure.setter
    def is_secure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574e1b7943b46dce0addf78beb9180246a367b59a7d363af790a32fe110fcff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isTemporary")
    def is_temporary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isTemporary"))

    @is_temporary.setter
    def is_temporary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4b08f4c1d08ed5320e5fa7e99daf1bb20bb650bae501cf23335bc6f2e4e2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTemporary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58e5a547efa8c8ad81b44d08a469712a5fbcae2a966611bb2b5a10af002a337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd3abdd09626c8e2cbba026af8927dcdb49fc4261c0e86fbff9611e88f9bbd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d59d6a1739c429e0050810a2d435e69cb64395348b98d5dfb088b36ac3bd373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewAggregationPolicy",
    jsii_struct_bases=[],
    name_mapping={"policy_name": "policyName", "entity_key": "entityKey"},
)
class ViewAggregationPolicy:
    def __init__(
        self,
        *,
        policy_name: builtins.str,
        entity_key: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param policy_name: Aggregation policy name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        :param entity_key: Defines which columns uniquely identify an entity within the view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#entity_key View#entity_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76de6e789c9f0ef301ab4206ef0865bd52b112ca49aa4c92dac68fdfeb0e0168)
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument entity_key", value=entity_key, expected_type=type_hints["entity_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_name": policy_name,
        }
        if entity_key is not None:
            self._values["entity_key"] = entity_key

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''Aggregation policy name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entity_key(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Defines which columns uniquely identify an entity within the view.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#entity_key View#entity_key}
        '''
        result = self._values.get("entity_key")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewAggregationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewAggregationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewAggregationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b302954b5da68127720408a94a7b0464d6b052ca625c66dc2e977ac7104bb3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEntityKey")
    def reset_entity_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEntityKey", []))

    @builtins.property
    @jsii.member(jsii_name="entityKeyInput")
    def entity_key_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entityKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="entityKey")
    def entity_key(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "entityKey"))

    @entity_key.setter
    def entity_key(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df0b76b1a789b3015fbf1fb71554e5b59ce0b24cca1caf0644ffc7560690221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2395a5f650bf59f825f381fc8dd8433dd47cd18ab98b6a8be59bd1bcef9a4899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewAggregationPolicy]:
        return typing.cast(typing.Optional[ViewAggregationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ViewAggregationPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61784cc13c601ce2f9c5c7eec2f5d7013fc509b730f543773d8925fad6639295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewColumn",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "comment": "comment",
        "masking_policy": "maskingPolicy",
        "projection_policy": "projectionPolicy",
    },
)
class ViewColumn:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        masking_policy: typing.Optional[typing.Union["ViewColumnMaskingPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        projection_policy: typing.Optional[typing.Union["ViewColumnProjectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param column_name: Specifies affected column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#column_name View#column_name}
        :param comment: Specifies a comment for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#comment View#comment}
        :param masking_policy: masking_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#masking_policy View#masking_policy}
        :param projection_policy: projection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#projection_policy View#projection_policy}
        '''
        if isinstance(masking_policy, dict):
            masking_policy = ViewColumnMaskingPolicy(**masking_policy)
        if isinstance(projection_policy, dict):
            projection_policy = ViewColumnProjectionPolicy(**projection_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440032759ae52a04cc398c428685da8a36b3ca1e730e5049173e2e2c4c232519)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument masking_policy", value=masking_policy, expected_type=type_hints["masking_policy"])
            check_type(argname="argument projection_policy", value=projection_policy, expected_type=type_hints["projection_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if masking_policy is not None:
            self._values["masking_policy"] = masking_policy
        if projection_policy is not None:
            self._values["projection_policy"] = projection_policy

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Specifies affected column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#column_name View#column_name}
        '''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#comment View#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def masking_policy(self) -> typing.Optional["ViewColumnMaskingPolicy"]:
        '''masking_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#masking_policy View#masking_policy}
        '''
        result = self._values.get("masking_policy")
        return typing.cast(typing.Optional["ViewColumnMaskingPolicy"], result)

    @builtins.property
    def projection_policy(self) -> typing.Optional["ViewColumnProjectionPolicy"]:
        '''projection_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#projection_policy View#projection_policy}
        '''
        result = self._values.get("projection_policy")
        return typing.cast(typing.Optional["ViewColumnProjectionPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95c663177ae94be81d2fa7f851ff6ef251632c8675c05d2687fcf59f2ba0e5d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ViewColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70170ea6d9641c8fd30ed26ee49002a46e9bd6ec138385b940b5156e421918fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ViewColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f7ec35d2432c603fd5ff0d22980362dd522056b7ac5009fcd841e36711b5a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7beb93261859f3398b5af2cadf36a4b2b7bc39ca5ec6e2304bc6bf2086a4d2b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4435edb3d2e26d6925daf6f09c5843c2d8ede3dac5df3ec2461cfc21cb0a3b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d118a36e98421d6bfcd1623e8028dd0dff050728a8e34d7068918516f7d6d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewColumnMaskingPolicy",
    jsii_struct_bases=[],
    name_mapping={"policy_name": "policyName", "using": "using"},
)
class ViewColumnMaskingPolicy:
    def __init__(
        self,
        *,
        policy_name: builtins.str,
        using: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param policy_name: Specifies the masking policy to set on a column. For more information about this resource, see `docs <./masking_policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        :param using: Specifies the arguments to pass into the conditional masking policy SQL expression. The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the column to which the masking policy is set. The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query result when a query is made on the first column. If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal masking policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#using View#using}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91be762c59dcb5373043f22b8e8a84ef6befb88891eb139130b16c2598abb15b)
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument using", value=using, expected_type=type_hints["using"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_name": policy_name,
        }
        if using is not None:
            self._values["using"] = using

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''Specifies the masking policy to set on a column. For more information about this resource, see `docs <./masking_policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def using(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the arguments to pass into the conditional masking policy SQL expression.

        The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the column to which the masking policy is set. The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query result when a query is made on the first column. If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal masking policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#using View#using}
        '''
        result = self._values.get("using")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewColumnMaskingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewColumnMaskingPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewColumnMaskingPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13f82f8eb60f778df3cad10f5cd306e88ea2037a255b13cd0234aa67fc7c3bea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUsing")
    def reset_using(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsing", []))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="usingInput")
    def using_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usingInput"))

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed7e5b2fda0b0300ff70fc851258376f01c5f81c811fc2fac325fdfa135ea3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="using")
    def using(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "using"))

    @using.setter
    def using(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34b512eb62bc953a80c1c36edbef6ba5531ebf4910ae77b46e6ae95e4647c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "using", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewColumnMaskingPolicy]:
        return typing.cast(typing.Optional[ViewColumnMaskingPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ViewColumnMaskingPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891ab3b4788e39c62374dba0080191e8e9a7a08afb8fc36058fc96c13e7011f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ViewColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6e0ef7ca483575fd8a47208aeca80de5b53a0f4034e9fd7f48772fd85b2f917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMaskingPolicy")
    def put_masking_policy(
        self,
        *,
        policy_name: builtins.str,
        using: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param policy_name: Specifies the masking policy to set on a column. For more information about this resource, see `docs <./masking_policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        :param using: Specifies the arguments to pass into the conditional masking policy SQL expression. The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the column to which the masking policy is set. The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query result when a query is made on the first column. If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal masking policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#using View#using}
        '''
        value = ViewColumnMaskingPolicy(policy_name=policy_name, using=using)

        return typing.cast(None, jsii.invoke(self, "putMaskingPolicy", [value]))

    @jsii.member(jsii_name="putProjectionPolicy")
    def put_projection_policy(self, *, policy_name: builtins.str) -> None:
        '''
        :param policy_name: Specifies the projection policy to set on a column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        value = ViewColumnProjectionPolicy(policy_name=policy_name)

        return typing.cast(None, jsii.invoke(self, "putProjectionPolicy", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetMaskingPolicy")
    def reset_masking_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaskingPolicy", []))

    @jsii.member(jsii_name="resetProjectionPolicy")
    def reset_projection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectionPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="maskingPolicy")
    def masking_policy(self) -> ViewColumnMaskingPolicyOutputReference:
        return typing.cast(ViewColumnMaskingPolicyOutputReference, jsii.get(self, "maskingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="projectionPolicy")
    def projection_policy(self) -> "ViewColumnProjectionPolicyOutputReference":
        return typing.cast("ViewColumnProjectionPolicyOutputReference", jsii.get(self, "projectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="maskingPolicyInput")
    def masking_policy_input(self) -> typing.Optional[ViewColumnMaskingPolicy]:
        return typing.cast(typing.Optional[ViewColumnMaskingPolicy], jsii.get(self, "maskingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectionPolicyInput")
    def projection_policy_input(self) -> typing.Optional["ViewColumnProjectionPolicy"]:
        return typing.cast(typing.Optional["ViewColumnProjectionPolicy"], jsii.get(self, "projectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95c174093d68310b88ec899d0f783d70daba3a7036cf9646243eccf85f2b0a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610bf3a2bac861c978d8b3962bd0ea4b79edabc7d54fe037e1f50891a357f736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4703bf345bb236dca7de96c8dc4cc1c686b1bd16d30cd259ae9c1461b48c3d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewColumnProjectionPolicy",
    jsii_struct_bases=[],
    name_mapping={"policy_name": "policyName"},
)
class ViewColumnProjectionPolicy:
    def __init__(self, *, policy_name: builtins.str) -> None:
        '''
        :param policy_name: Specifies the projection policy to set on a column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d3015a8c9907adad06a37cec71ece2a794a8f87b918a820252d5c88c4eeb00)
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_name": policy_name,
        }

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''Specifies the projection policy to set on a column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewColumnProjectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewColumnProjectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewColumnProjectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5153577545cc3b5a296580d65f326f5d7e50d13f3eb41ef2cccbc94a576b5f8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e3a863a4e09642b306345c53575e912ae483e3c29f6c357f5c0b8f7b1ed9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewColumnProjectionPolicy]:
        return typing.cast(typing.Optional[ViewColumnProjectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ViewColumnProjectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21a73bb43b4b38698f2e695543bc5e6448cef890fefb3eac63c7cb1ae601abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "name": "name",
        "schema": "schema",
        "statement": "statement",
        "aggregation_policy": "aggregationPolicy",
        "change_tracking": "changeTracking",
        "column": "column",
        "comment": "comment",
        "copy_grants": "copyGrants",
        "data_metric_function": "dataMetricFunction",
        "data_metric_schedule": "dataMetricSchedule",
        "id": "id",
        "is_recursive": "isRecursive",
        "is_secure": "isSecure",
        "is_temporary": "isTemporary",
        "row_access_policy": "rowAccessPolicy",
    },
)
class ViewConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        statement: builtins.str,
        aggregation_policy: typing.Optional[typing.Union[ViewAggregationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        change_tracking: typing.Optional[builtins.str] = None,
        column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_metric_function: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ViewDataMetricFunction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_metric_schedule: typing.Optional[typing.Union["ViewDataMetricSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_recursive: typing.Optional[builtins.str] = None,
        is_secure: typing.Optional[builtins.str] = None,
        is_temporary: typing.Optional[builtins.str] = None,
        row_access_policy: typing.Optional[typing.Union["ViewRowAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the view. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#database View#database}
        :param name: Specifies the identifier for the view; must be unique for the schema in which the view is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#name View#name}
        :param schema: The schema in which to create the view. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#schema View#schema}
        :param statement: Specifies the query used to create the view. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#statement View#statement}
        :param aggregation_policy: aggregation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#aggregation_policy View#aggregation_policy}
        :param change_tracking: Specifies to enable or disable change tracking on the table. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#change_tracking View#change_tracking}
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#column View#column}
        :param comment: Specifies a comment for the view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#comment View#comment}
        :param copy_grants: Retains the access permissions from the original view when a view is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#copy_grants View#copy_grants}
        :param data_metric_function: data_metric_function block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#data_metric_function View#data_metric_function}
        :param data_metric_schedule: data_metric_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#data_metric_schedule View#data_metric_schedule}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#id View#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_recursive: Specifies that the view can refer to itself using recursive syntax without necessarily using a CTE (common table expression). Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_recursive View#is_recursive}
        :param is_secure: Specifies that the view is secure. By design, the Snowflake's ``SHOW VIEWS`` command does not provide information about secure views (consult `view usage notes <https://docs.snowflake.com/en/sql-reference/sql/create-view#usage-notes>`_) which is essential to manage/import view with Terraform. Use the role owning the view while managing secure views. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_secure View#is_secure}
        :param is_temporary: Specifies that the view persists only for the duration of the session that you created it in. A temporary view and all its contents are dropped at the end of the session. In context of this provider, it means that it's dropped after a Terraform operation. This results in a permanent plan with object creation. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_temporary View#is_temporary}
        :param row_access_policy: row_access_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#row_access_policy View#row_access_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aggregation_policy, dict):
            aggregation_policy = ViewAggregationPolicy(**aggregation_policy)
        if isinstance(data_metric_schedule, dict):
            data_metric_schedule = ViewDataMetricSchedule(**data_metric_schedule)
        if isinstance(row_access_policy, dict):
            row_access_policy = ViewRowAccessPolicy(**row_access_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4c315392eb726cc55e03fa983a07210e0ef3fc36ec42f9f5bb319667fc81f2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument aggregation_policy", value=aggregation_policy, expected_type=type_hints["aggregation_policy"])
            check_type(argname="argument change_tracking", value=change_tracking, expected_type=type_hints["change_tracking"])
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument copy_grants", value=copy_grants, expected_type=type_hints["copy_grants"])
            check_type(argname="argument data_metric_function", value=data_metric_function, expected_type=type_hints["data_metric_function"])
            check_type(argname="argument data_metric_schedule", value=data_metric_schedule, expected_type=type_hints["data_metric_schedule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_recursive", value=is_recursive, expected_type=type_hints["is_recursive"])
            check_type(argname="argument is_secure", value=is_secure, expected_type=type_hints["is_secure"])
            check_type(argname="argument is_temporary", value=is_temporary, expected_type=type_hints["is_temporary"])
            check_type(argname="argument row_access_policy", value=row_access_policy, expected_type=type_hints["row_access_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
            "schema": schema,
            "statement": statement,
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
        if aggregation_policy is not None:
            self._values["aggregation_policy"] = aggregation_policy
        if change_tracking is not None:
            self._values["change_tracking"] = change_tracking
        if column is not None:
            self._values["column"] = column
        if comment is not None:
            self._values["comment"] = comment
        if copy_grants is not None:
            self._values["copy_grants"] = copy_grants
        if data_metric_function is not None:
            self._values["data_metric_function"] = data_metric_function
        if data_metric_schedule is not None:
            self._values["data_metric_schedule"] = data_metric_schedule
        if id is not None:
            self._values["id"] = id
        if is_recursive is not None:
            self._values["is_recursive"] = is_recursive
        if is_secure is not None:
            self._values["is_secure"] = is_secure
        if is_temporary is not None:
            self._values["is_temporary"] = is_temporary
        if row_access_policy is not None:
            self._values["row_access_policy"] = row_access_policy

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
    def database(self) -> builtins.str:
        '''The database in which to create the view.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#database View#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the view;

        must be unique for the schema in which the view is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#name View#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the view.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#schema View#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement(self) -> builtins.str:
        '''Specifies the query used to create the view.

        To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#statement View#statement}
        '''
        result = self._values.get("statement")
        assert result is not None, "Required property 'statement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregation_policy(self) -> typing.Optional[ViewAggregationPolicy]:
        '''aggregation_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#aggregation_policy View#aggregation_policy}
        '''
        result = self._values.get("aggregation_policy")
        return typing.cast(typing.Optional[ViewAggregationPolicy], result)

    @builtins.property
    def change_tracking(self) -> typing.Optional[builtins.str]:
        '''Specifies to enable or disable change tracking on the table.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#change_tracking View#change_tracking}
        '''
        result = self._values.get("change_tracking")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewColumn]]]:
        '''column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#column View#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewColumn]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the view.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#comment View#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_grants(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Retains the access permissions from the original view when a view is recreated using the OR REPLACE clause.

        This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#copy_grants View#copy_grants}
        '''
        result = self._values.get("copy_grants")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_metric_function(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ViewDataMetricFunction"]]]:
        '''data_metric_function block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#data_metric_function View#data_metric_function}
        '''
        result = self._values.get("data_metric_function")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ViewDataMetricFunction"]]], result)

    @builtins.property
    def data_metric_schedule(self) -> typing.Optional["ViewDataMetricSchedule"]:
        '''data_metric_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#data_metric_schedule View#data_metric_schedule}
        '''
        result = self._values.get("data_metric_schedule")
        return typing.cast(typing.Optional["ViewDataMetricSchedule"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#id View#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_recursive(self) -> typing.Optional[builtins.str]:
        '''Specifies that the view can refer to itself using recursive syntax without necessarily using a CTE (common table expression).

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_recursive View#is_recursive}
        '''
        result = self._values.get("is_recursive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_secure(self) -> typing.Optional[builtins.str]:
        '''Specifies that the view is secure.

        By design, the Snowflake's ``SHOW VIEWS`` command does not provide information about secure views (consult `view usage notes <https://docs.snowflake.com/en/sql-reference/sql/create-view#usage-notes>`_) which is essential to manage/import view with Terraform. Use the role owning the view while managing secure views. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_secure View#is_secure}
        '''
        result = self._values.get("is_secure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_temporary(self) -> typing.Optional[builtins.str]:
        '''Specifies that the view persists only for the duration of the session that you created it in.

        A temporary view and all its contents are dropped at the end of the session. In context of this provider, it means that it's dropped after a Terraform operation. This results in a permanent plan with object creation. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#is_temporary View#is_temporary}
        '''
        result = self._values.get("is_temporary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def row_access_policy(self) -> typing.Optional["ViewRowAccessPolicy"]:
        '''row_access_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#row_access_policy View#row_access_policy}
        '''
        result = self._values.get("row_access_policy")
        return typing.cast(typing.Optional["ViewRowAccessPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewDataMetricFunction",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "on": "on",
        "schedule_status": "scheduleStatus",
    },
)
class ViewDataMetricFunction:
    def __init__(
        self,
        *,
        function_name: builtins.str,
        on: typing.Sequence[builtins.str],
        schedule_status: builtins.str,
    ) -> None:
        '''
        :param function_name: Identifier of the data metric function to add to the table or view or drop from the table or view. This function identifier must be provided without arguments in parenthesis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#function_name View#function_name}
        :param on: The table or view columns on which to associate the data metric function. The data types of the columns must match the data types of the columns specified in the data metric function definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#on View#on}
        :param schedule_status: The status of the metrics association. Valid values are: ``STARTED`` | ``SUSPENDED``. When status of a data metric function is changed, it is being reassigned with ``DROP DATA METRIC FUNCTION`` and ``ADD DATA METRIC FUNCTION``, and then its status is changed by ``MODIFY DATA METRIC FUNCTION`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#schedule_status View#schedule_status}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cedddf968b86ed9f1cac58a9c1c1dc9ff09023b9d49155470e2094482732c69)
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
            check_type(argname="argument schedule_status", value=schedule_status, expected_type=type_hints["schedule_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_name": function_name,
            "on": on,
            "schedule_status": schedule_status,
        }

    @builtins.property
    def function_name(self) -> builtins.str:
        '''Identifier of the data metric function to add to the table or view or drop from the table or view.

        This function identifier must be provided without arguments in parenthesis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#function_name View#function_name}
        '''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on(self) -> typing.List[builtins.str]:
        '''The table or view columns on which to associate the data metric function.

        The data types of the columns must match the data types of the columns specified in the data metric function definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#on View#on}
        '''
        result = self._values.get("on")
        assert result is not None, "Required property 'on' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def schedule_status(self) -> builtins.str:
        '''The status of the metrics association.

        Valid values are: ``STARTED`` | ``SUSPENDED``. When status of a data metric function is changed, it is being reassigned with ``DROP DATA METRIC FUNCTION`` and ``ADD DATA METRIC FUNCTION``, and then its status is changed by ``MODIFY DATA METRIC FUNCTION``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#schedule_status View#schedule_status}
        '''
        result = self._values.get("schedule_status")
        assert result is not None, "Required property 'schedule_status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewDataMetricFunction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewDataMetricFunctionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewDataMetricFunctionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9f952bb185dd00df71468fbf1690d236fb2a4f493bced74ae99baabd0f2d1a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ViewDataMetricFunctionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0b3c70a8ff08185d8e82f8da14e775273d7b5df9bad8a376f467ed733a6927)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ViewDataMetricFunctionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c5d23b32549b2467a55ff8b95ebabe10c83ef30d2729fa51783a29fbfe885f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a2866d1fc8f86509a53b6b98bcf767ac783e69b42349046477289a077f0ba3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d340570c7b835630e4d3b8a109088fe71bbae6302ab39316efe8c31aa74cb87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewDataMetricFunction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewDataMetricFunction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewDataMetricFunction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201ac982948fb45b9be063f3cfe6e1de8327b177bbfd88a00ecd70c2b55195aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ViewDataMetricFunctionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewDataMetricFunctionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69be687956e90b322ab0379872d1e223a0fd1399c27c643fdd34cd4138876e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="onInput")
    def on_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "onInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStatusInput")
    def schedule_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2af941cecbcadff21046073a880b22d8ce4d62b5966ee3c3da70069959b3915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="on")
    def on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "on"))

    @on.setter
    def on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac0821ff45eb017abbe0537935e4ce2c8e57af4ada6e98eddd9528e24547e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "on", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleStatus")
    def schedule_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleStatus"))

    @schedule_status.setter
    def schedule_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96a496652e0a055f41dd10f6aa23bce34b211d3a509b546965e53eed3d46dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewDataMetricFunction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewDataMetricFunction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewDataMetricFunction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b61ff9302dd6cde283abaf9bcbc00d3c2d2c84fee421fa54a5ea170cce996d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewDataMetricSchedule",
    jsii_struct_bases=[],
    name_mapping={"minutes": "minutes", "using_cron": "usingCron"},
)
class ViewDataMetricSchedule:
    def __init__(
        self,
        *,
        minutes: typing.Optional[jsii.Number] = None,
        using_cron: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minutes: Specifies an interval (in minutes) of wait time inserted between runs of the data metric function. Conflicts with ``using_cron``. Valid values are: ``5`` | ``15`` | ``30`` | ``60`` | ``720`` | ``1440``. Due to Snowflake limitations, changes in this field are not managed by the provider. Please consider using `taint <https://developer.hashicorp.com/terraform/cli/commands/taint>`_ command, ``using_cron`` field, or `replace_triggered_by <https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#replace_triggered_by>`_ metadata argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#minutes View#minutes}
        :param using_cron: Specifies a cron expression and time zone for periodically running the data metric function. Supports a subset of standard cron utility syntax. Conflicts with ``minutes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#using_cron View#using_cron}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc271ed9e7e200c14fc1f028ea6ab736631371100f73f44d8b4f97616e5ba2c)
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument using_cron", value=using_cron, expected_type=type_hints["using_cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minutes is not None:
            self._values["minutes"] = minutes
        if using_cron is not None:
            self._values["using_cron"] = using_cron

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Specifies an interval (in minutes) of wait time inserted between runs of the data metric function.

        Conflicts with ``using_cron``. Valid values are: ``5`` | ``15`` | ``30`` | ``60`` | ``720`` | ``1440``. Due to Snowflake limitations, changes in this field are not managed by the provider. Please consider using `taint <https://developer.hashicorp.com/terraform/cli/commands/taint>`_ command, ``using_cron`` field, or `replace_triggered_by <https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#replace_triggered_by>`_ metadata argument.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#minutes View#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def using_cron(self) -> typing.Optional[builtins.str]:
        '''Specifies a cron expression and time zone for periodically running the data metric function.

        Supports a subset of standard cron utility syntax. Conflicts with ``minutes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#using_cron View#using_cron}
        '''
        result = self._values.get("using_cron")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewDataMetricSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewDataMetricScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewDataMetricScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45246b354196be101335ba37d742b6cd05fc23160f064414aa757b9712bb93e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetUsingCron")
    def reset_using_cron(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsingCron", []))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="usingCronInput")
    def using_cron_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usingCronInput"))

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91025a2b7939a8134749e2ab6f846e09d6d10df1dd553730d2e2e65e76ad5997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usingCron")
    def using_cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usingCron"))

    @using_cron.setter
    def using_cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88f65afd22a2dd3fb2df16a271ff7eca6db924a250f447ce3ef0909c7f8199d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usingCron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewDataMetricSchedule]:
        return typing.cast(typing.Optional[ViewDataMetricSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ViewDataMetricSchedule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863c64ea0fae36f88f5da2cca3bedbf8c9cba3005df398cb4c49ba3d1704d964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ViewDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6787f474a8aa90049df6123de86b4cc33bd5f306198137821ae208fa5d917ce2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ViewDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6add24a2e50248417351ee158fdd09234d912b2cbad369b48dcf62bca072cb5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ViewDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6ab7e06b1d81c22708db37ef0533725c4d9882a0b581b639e8b332954e52e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6caab484a2ff6fc5990d896d9fc04c758d49d6ef5039df37ddfc611d6452cb6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5475ce44473c8f7ece7b1142d9d3d9832b1f837a5847b683ba17fb3545ab37a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ViewDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a36cf58c09cc84578d8a868f1574c31b12d170270beed0269958cbd214e6a69a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="check")
    def check(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "check"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @builtins.property
    @jsii.member(jsii_name="isNullable")
    def is_nullable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isNullable"))

    @builtins.property
    @jsii.member(jsii_name="isPrimary")
    def is_primary(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isPrimary"))

    @builtins.property
    @jsii.member(jsii_name="isUnique")
    def is_unique(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isUnique"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @builtins.property
    @jsii.member(jsii_name="privacyDomain")
    def privacy_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privacyDomain"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewDescribeOutput]:
        return typing.cast(typing.Optional[ViewDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ViewDescribeOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc389c7c23e0880f17a902b1f0cef56799036b563e29e50822e6cc8c6a429a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewRowAccessPolicy",
    jsii_struct_bases=[],
    name_mapping={"on": "on", "policy_name": "policyName"},
)
class ViewRowAccessPolicy:
    def __init__(
        self,
        *,
        on: typing.Sequence[builtins.str],
        policy_name: builtins.str,
    ) -> None:
        '''
        :param on: Defines which columns are affected by the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#on View#on}
        :param policy_name: Row access policy name. For more information about this resource, see `docs <./row_access_policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2597efd1d1b0be59ea7d33b2d30090a27b8d99c85ae71810fe032781e131e7)
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "on": on,
            "policy_name": policy_name,
        }

    @builtins.property
    def on(self) -> typing.List[builtins.str]:
        '''Defines which columns are affected by the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#on View#on}
        '''
        result = self._values.get("on")
        assert result is not None, "Required property 'on' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''Row access policy name. For more information about this resource, see `docs <./row_access_policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/view#policy_name View#policy_name}
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewRowAccessPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewRowAccessPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewRowAccessPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b73ff6b50075d561f015c45cf568de7606ee361372cf6a53765c638e6c9807fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="onInput")
    def on_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "onInput"))

    @builtins.property
    @jsii.member(jsii_name="policyNameInput")
    def policy_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="on")
    def on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "on"))

    @on.setter
    def on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725beecf5c2e90d646354395f411e26eb79e574d8d72e47299bdd2f2dde47c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "on", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04740a1744c921407b24e30b0dcefc955252a2b5632b0d3827048868559699da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewRowAccessPolicy]:
        return typing.cast(typing.Optional[ViewRowAccessPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ViewRowAccessPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e9e589f99ed76833dcaea343cacfc5f310fa51d676edd51451c00cc69e4e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.view.ViewShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ViewShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ViewShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViewShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbdad989bc41556a185427752fb2bd6aae07161786c699144e1e1dbafe8a10f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ViewShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57775905ce60e155c24c797c90dc7d0b71011bb55b9cea75d3ddc0d181078392)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ViewShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292330c728be3613c3a3a598fbff4f4de7470383c10382a3dc7ac8502388a32d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81702bbf99b50ca37d465d5d9bbe9b052b8ca47bcc2fd86d62c19863e590b3aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2431d0e3dd299748e5be6ec448513b6db13464d28bef9f62f4aad6a3bee97a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ViewShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.view.ViewShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ea5e057259442f0b43e95476defe5aa0aaeaa265cc7eba25957139c6361269c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="changeTracking")
    def change_tracking(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "changeTracking"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="isMaterialized")
    def is_materialized(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isMaterialized"))

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isSecure"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="reserved")
    def reserved(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reserved"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ViewShowOutput]:
        return typing.cast(typing.Optional[ViewShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ViewShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d62316160784f6f0024ba3f5011ed6a6431e1fc257a2e8f0d659b3413bd87c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "View",
    "ViewAggregationPolicy",
    "ViewAggregationPolicyOutputReference",
    "ViewColumn",
    "ViewColumnList",
    "ViewColumnMaskingPolicy",
    "ViewColumnMaskingPolicyOutputReference",
    "ViewColumnOutputReference",
    "ViewColumnProjectionPolicy",
    "ViewColumnProjectionPolicyOutputReference",
    "ViewConfig",
    "ViewDataMetricFunction",
    "ViewDataMetricFunctionList",
    "ViewDataMetricFunctionOutputReference",
    "ViewDataMetricSchedule",
    "ViewDataMetricScheduleOutputReference",
    "ViewDescribeOutput",
    "ViewDescribeOutputList",
    "ViewDescribeOutputOutputReference",
    "ViewRowAccessPolicy",
    "ViewRowAccessPolicyOutputReference",
    "ViewShowOutput",
    "ViewShowOutputList",
    "ViewShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__0e0462f8da364bb0cc996ac2edd41517d2b2f5feaf2f8e302def5e65df13e864(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    statement: builtins.str,
    aggregation_policy: typing.Optional[typing.Union[ViewAggregationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    change_tracking: typing.Optional[builtins.str] = None,
    column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_metric_function: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewDataMetricFunction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_metric_schedule: typing.Optional[typing.Union[ViewDataMetricSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_recursive: typing.Optional[builtins.str] = None,
    is_secure: typing.Optional[builtins.str] = None,
    is_temporary: typing.Optional[builtins.str] = None,
    row_access_policy: typing.Optional[typing.Union[ViewRowAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c71fdd2966d270044cf6cff34c439f863d0fe1bfc73fef6fdb43d777576d632e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8146c0ec022e2997332b204f376e3d9fd1aebf8a2de23df5c550984181c2b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b39e18a45a59d46e6fb10318458188d877e6c3dbc27adb1a545439285a9825(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewDataMetricFunction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ecf3e7641b58c7c70a5e9b5b9ca2785178000e8d428e4d2afa113c2fbbf52a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a872f963cb6f839357c360fed1880e3dca25f9cea4bd519fe535c9a45845401b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5f729bf67f2b2cb80711c8fb1c5e8b66237f1a66ec6621e74245cd4fe4d752(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e15403d909a79852aafc2fc4abd6662b1715eecafd152bd6488c3ede1170285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd1f1a3e85d62483b8f0a9bb868eb7ee89f5d579b55ea01afc583a8a44bcfdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6f4fce2cb615f6ff6d181cdd2d6fdc3ed5af4f9b81a042ffa43609f9ddce09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574e1b7943b46dce0addf78beb9180246a367b59a7d363af790a32fe110fcff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4b08f4c1d08ed5320e5fa7e99daf1bb20bb650bae501cf23335bc6f2e4e2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58e5a547efa8c8ad81b44d08a469712a5fbcae2a966611bb2b5a10af002a337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd3abdd09626c8e2cbba026af8927dcdb49fc4261c0e86fbff9611e88f9bbd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d59d6a1739c429e0050810a2d435e69cb64395348b98d5dfb088b36ac3bd373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76de6e789c9f0ef301ab4206ef0865bd52b112ca49aa4c92dac68fdfeb0e0168(
    *,
    policy_name: builtins.str,
    entity_key: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b302954b5da68127720408a94a7b0464d6b052ca625c66dc2e977ac7104bb3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df0b76b1a789b3015fbf1fb71554e5b59ce0b24cca1caf0644ffc7560690221(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2395a5f650bf59f825f381fc8dd8433dd47cd18ab98b6a8be59bd1bcef9a4899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61784cc13c601ce2f9c5c7eec2f5d7013fc509b730f543773d8925fad6639295(
    value: typing.Optional[ViewAggregationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440032759ae52a04cc398c428685da8a36b3ca1e730e5049173e2e2c4c232519(
    *,
    column_name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    masking_policy: typing.Optional[typing.Union[ViewColumnMaskingPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    projection_policy: typing.Optional[typing.Union[ViewColumnProjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c663177ae94be81d2fa7f851ff6ef251632c8675c05d2687fcf59f2ba0e5d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70170ea6d9641c8fd30ed26ee49002a46e9bd6ec138385b940b5156e421918fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f7ec35d2432c603fd5ff0d22980362dd522056b7ac5009fcd841e36711b5a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7beb93261859f3398b5af2cadf36a4b2b7bc39ca5ec6e2304bc6bf2086a4d2b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4435edb3d2e26d6925daf6f09c5843c2d8ede3dac5df3ec2461cfc21cb0a3b6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d118a36e98421d6bfcd1623e8028dd0dff050728a8e34d7068918516f7d6d43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91be762c59dcb5373043f22b8e8a84ef6befb88891eb139130b16c2598abb15b(
    *,
    policy_name: builtins.str,
    using: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f82f8eb60f778df3cad10f5cd306e88ea2037a255b13cd0234aa67fc7c3bea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed7e5b2fda0b0300ff70fc851258376f01c5f81c811fc2fac325fdfa135ea3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34b512eb62bc953a80c1c36edbef6ba5531ebf4910ae77b46e6ae95e4647c02(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891ab3b4788e39c62374dba0080191e8e9a7a08afb8fc36058fc96c13e7011f9(
    value: typing.Optional[ViewColumnMaskingPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e0ef7ca483575fd8a47208aeca80de5b53a0f4034e9fd7f48772fd85b2f917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95c174093d68310b88ec899d0f783d70daba3a7036cf9646243eccf85f2b0a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610bf3a2bac861c978d8b3962bd0ea4b79edabc7d54fe037e1f50891a357f736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4703bf345bb236dca7de96c8dc4cc1c686b1bd16d30cd259ae9c1461b48c3d2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d3015a8c9907adad06a37cec71ece2a794a8f87b918a820252d5c88c4eeb00(
    *,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5153577545cc3b5a296580d65f326f5d7e50d13f3eb41ef2cccbc94a576b5f8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e3a863a4e09642b306345c53575e912ae483e3c29f6c357f5c0b8f7b1ed9d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21a73bb43b4b38698f2e695543bc5e6448cef890fefb3eac63c7cb1ae601abd(
    value: typing.Optional[ViewColumnProjectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4c315392eb726cc55e03fa983a07210e0ef3fc36ec42f9f5bb319667fc81f2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    statement: builtins.str,
    aggregation_policy: typing.Optional[typing.Union[ViewAggregationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    change_tracking: typing.Optional[builtins.str] = None,
    column: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewColumn, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_metric_function: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ViewDataMetricFunction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_metric_schedule: typing.Optional[typing.Union[ViewDataMetricSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_recursive: typing.Optional[builtins.str] = None,
    is_secure: typing.Optional[builtins.str] = None,
    is_temporary: typing.Optional[builtins.str] = None,
    row_access_policy: typing.Optional[typing.Union[ViewRowAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cedddf968b86ed9f1cac58a9c1c1dc9ff09023b9d49155470e2094482732c69(
    *,
    function_name: builtins.str,
    on: typing.Sequence[builtins.str],
    schedule_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f952bb185dd00df71468fbf1690d236fb2a4f493bced74ae99baabd0f2d1a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0b3c70a8ff08185d8e82f8da14e775273d7b5df9bad8a376f467ed733a6927(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c5d23b32549b2467a55ff8b95ebabe10c83ef30d2729fa51783a29fbfe885f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2866d1fc8f86509a53b6b98bcf767ac783e69b42349046477289a077f0ba3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d340570c7b835630e4d3b8a109088fe71bbae6302ab39316efe8c31aa74cb87(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201ac982948fb45b9be063f3cfe6e1de8327b177bbfd88a00ecd70c2b55195aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ViewDataMetricFunction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69be687956e90b322ab0379872d1e223a0fd1399c27c643fdd34cd4138876e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2af941cecbcadff21046073a880b22d8ce4d62b5966ee3c3da70069959b3915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac0821ff45eb017abbe0537935e4ce2c8e57af4ada6e98eddd9528e24547e1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96a496652e0a055f41dd10f6aa23bce34b211d3a509b546965e53eed3d46dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b61ff9302dd6cde283abaf9bcbc00d3c2d2c84fee421fa54a5ea170cce996d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ViewDataMetricFunction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc271ed9e7e200c14fc1f028ea6ab736631371100f73f44d8b4f97616e5ba2c(
    *,
    minutes: typing.Optional[jsii.Number] = None,
    using_cron: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45246b354196be101335ba37d742b6cd05fc23160f064414aa757b9712bb93e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91025a2b7939a8134749e2ab6f846e09d6d10df1dd553730d2e2e65e76ad5997(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88f65afd22a2dd3fb2df16a271ff7eca6db924a250f447ce3ef0909c7f8199d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863c64ea0fae36f88f5da2cca3bedbf8c9cba3005df398cb4c49ba3d1704d964(
    value: typing.Optional[ViewDataMetricSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6787f474a8aa90049df6123de86b4cc33bd5f306198137821ae208fa5d917ce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6add24a2e50248417351ee158fdd09234d912b2cbad369b48dcf62bca072cb5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6ab7e06b1d81c22708db37ef0533725c4d9882a0b581b639e8b332954e52e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6caab484a2ff6fc5990d896d9fc04c758d49d6ef5039df37ddfc611d6452cb6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5475ce44473c8f7ece7b1142d9d3d9832b1f837a5847b683ba17fb3545ab37a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36cf58c09cc84578d8a868f1574c31b12d170270beed0269958cbd214e6a69a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc389c7c23e0880f17a902b1f0cef56799036b563e29e50822e6cc8c6a429a2(
    value: typing.Optional[ViewDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2597efd1d1b0be59ea7d33b2d30090a27b8d99c85ae71810fe032781e131e7(
    *,
    on: typing.Sequence[builtins.str],
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73ff6b50075d561f015c45cf568de7606ee361372cf6a53765c638e6c9807fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725beecf5c2e90d646354395f411e26eb79e574d8d72e47299bdd2f2dde47c88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04740a1744c921407b24e30b0dcefc955252a2b5632b0d3827048868559699da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e9e589f99ed76833dcaea343cacfc5f310fa51d676edd51451c00cc69e4e86(
    value: typing.Optional[ViewRowAccessPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdad989bc41556a185427752fb2bd6aae07161786c699144e1e1dbafe8a10f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57775905ce60e155c24c797c90dc7d0b71011bb55b9cea75d3ddc0d181078392(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292330c728be3613c3a3a598fbff4f4de7470383c10382a3dc7ac8502388a32d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81702bbf99b50ca37d465d5d9bbe9b052b8ca47bcc2fd86d62c19863e590b3aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2431d0e3dd299748e5be6ec448513b6db13464d28bef9f62f4aad6a3bee97a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea5e057259442f0b43e95476defe5aa0aaeaa265cc7eba25957139c6361269c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d62316160784f6f0024ba3f5011ed6a6431e1fc257a2e8f0d659b3413bd87c4(
    value: typing.Optional[ViewShowOutput],
) -> None:
    """Type checking stubs"""
    pass
