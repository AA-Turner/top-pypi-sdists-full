r'''
# `snowflake_table_constraint`

Refer to the Terraform Registry for docs: [`snowflake_table_constraint`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint).
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


class TableConstraint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.tableConstraint.TableConstraint",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint snowflake_table_constraint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        columns: typing.Sequence[builtins.str],
        name: builtins.str,
        table_id: builtins.str,
        type: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        deferrable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        foreign_key_properties: typing.Optional[typing.Union["TableConstraintForeignKeyProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initially: typing.Optional[builtins.str] = None,
        rely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint snowflake_table_constraint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param columns: Columns to use in constraint key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#columns TableConstraint#columns}
        :param name: Name of constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#name TableConstraint#name}
        :param table_id: Identifier for table to create constraint on. Format must follow: ""<db_name>"."<schema_name>"."<table_name>"" or "<db_name>.<schema_name>.<table_name>" (snowflake_table.my_table.id). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#table_id TableConstraint#table_id}
        :param type: Type of constraint, one of 'UNIQUE', 'PRIMARY KEY', or 'FOREIGN KEY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#type TableConstraint#type}
        :param comment: Comment for the table constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#comment TableConstraint#comment}
        :param deferrable: Whether the constraint is deferrable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#deferrable TableConstraint#deferrable}
        :param enable: Specifies whether the constraint is enabled or disabled. These properties are provided for compatibility with Oracle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#enable TableConstraint#enable}
        :param enforced: Whether the constraint is enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#enforced TableConstraint#enforced}
        :param foreign_key_properties: foreign_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#foreign_key_properties TableConstraint#foreign_key_properties}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#id TableConstraint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initially: Whether the constraint is initially deferred or immediate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#initially TableConstraint#initially}
        :param rely: Specifies whether a constraint in NOVALIDATE mode is taken into account during query rewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#rely TableConstraint#rely}
        :param validate: Specifies whether to validate existing data on the table when a constraint is created. Only used in conjunction with the ENABLE property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#validate TableConstraint#validate}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f847fc51ba3e1f2e74fa00f985eab007437f3fcdcab055264677e72c8e41ebe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TableConstraintConfig(
            columns=columns,
            name=name,
            table_id=table_id,
            type=type,
            comment=comment,
            deferrable=deferrable,
            enable=enable,
            enforced=enforced,
            foreign_key_properties=foreign_key_properties,
            id=id,
            initially=initially,
            rely=rely,
            validate=validate,
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
        '''Generates CDKTF code for importing a TableConstraint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TableConstraint to import.
        :param import_from_id: The id of the existing TableConstraint that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TableConstraint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d92440925415a5c265fe48c76e6e30459704e37cc3dc19f15ece9e870b45ec9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putForeignKeyProperties")
    def put_foreign_key_properties(
        self,
        *,
        references: typing.Union["TableConstraintForeignKeyPropertiesReferences", typing.Dict[builtins.str, typing.Any]],
        match: typing.Optional[builtins.str] = None,
        on_delete: typing.Optional[builtins.str] = None,
        on_update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param references: references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#references TableConstraint#references}
        :param match: The match type for the foreign key. Not applicable for primary/unique keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#match TableConstraint#match}
        :param on_delete: Specifies the action performed when the primary/unique key for the foreign key is deleted. Not applicable for primary/unique keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#on_delete TableConstraint#on_delete}
        :param on_update: Specifies the action performed when the primary/unique key for the foreign key is updated. Not applicable for primary/unique keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#on_update TableConstraint#on_update}
        '''
        value = TableConstraintForeignKeyProperties(
            references=references,
            match=match,
            on_delete=on_delete,
            on_update=on_update,
        )

        return typing.cast(None, jsii.invoke(self, "putForeignKeyProperties", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDeferrable")
    def reset_deferrable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeferrable", []))

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetEnforced")
    def reset_enforced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforced", []))

    @jsii.member(jsii_name="resetForeignKeyProperties")
    def reset_foreign_key_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForeignKeyProperties", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitially")
    def reset_initially(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitially", []))

    @jsii.member(jsii_name="resetRely")
    def reset_rely(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRely", []))

    @jsii.member(jsii_name="resetValidate")
    def reset_validate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidate", []))

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
    @jsii.member(jsii_name="foreignKeyProperties")
    def foreign_key_properties(
        self,
    ) -> "TableConstraintForeignKeyPropertiesOutputReference":
        return typing.cast("TableConstraintForeignKeyPropertiesOutputReference", jsii.get(self, "foreignKeyProperties"))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="deferrableInput")
    def deferrable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deferrableInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcedInput")
    def enforced_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforcedInput"))

    @builtins.property
    @jsii.member(jsii_name="foreignKeyPropertiesInput")
    def foreign_key_properties_input(
        self,
    ) -> typing.Optional["TableConstraintForeignKeyProperties"]:
        return typing.cast(typing.Optional["TableConstraintForeignKeyProperties"], jsii.get(self, "foreignKeyPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initiallyInput")
    def initially_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initiallyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="relyInput")
    def rely_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "relyInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bf410ba761a23cd391fba8ef48e3eb67f547f4e982ccee1d1e215f60f0d8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aa369a8bb54e80d30f3f7ef58259248ec268592a818330746cf8d71084cb08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deferrable")
    def deferrable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deferrable"))

    @deferrable.setter
    def deferrable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ae460e60808175dd2f80f265a4100043c795a9805930409139e019b929b86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deferrable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3118d3fc78d0f0723a26da01b9168f53d982393d1712b6b7c65c4ff8ca1c0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforced")
    def enforced(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforced"))

    @enforced.setter
    def enforced(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73392c63d744cc153ef7828df415325fe1fa428998618555003a818af23e1dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforced", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588056dff60afba76832322beb82e0648de2d4b85e27315d9be26b8061be49a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initially")
    def initially(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initially"))

    @initially.setter
    def initially(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c24a5e95d1103034367c8e466caceb6ceffb00a4f56292d35ff20ebd9771bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initially", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8756e8436e8eb4d533b5ca83b244dcdf3b0b2e14c9807132ee73fdd9f1146ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rely")
    def rely(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rely"))

    @rely.setter
    def rely(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adf159ac03b3aa51311f617a12615ffec815084001ffc3b0e203728e443c26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rely", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b285c3723d0aa3de5b663d75c6e0400fdb922d9927e96536ce3c02ec92c142bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a17131c16fd14d29ac5e6c0cfcec15c5f51e32cc8ea48322e4f64c7e9d92cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validate"))

    @validate.setter
    def validate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48b88b6fc5c4d58d73f1eac1aa9edc6d26d47089e3716b9b8cc4b56e7d4edcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.tableConstraint.TableConstraintConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "columns": "columns",
        "name": "name",
        "table_id": "tableId",
        "type": "type",
        "comment": "comment",
        "deferrable": "deferrable",
        "enable": "enable",
        "enforced": "enforced",
        "foreign_key_properties": "foreignKeyProperties",
        "id": "id",
        "initially": "initially",
        "rely": "rely",
        "validate": "validate",
    },
)
class TableConstraintConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        columns: typing.Sequence[builtins.str],
        name: builtins.str,
        table_id: builtins.str,
        type: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        deferrable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        foreign_key_properties: typing.Optional[typing.Union["TableConstraintForeignKeyProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        initially: typing.Optional[builtins.str] = None,
        rely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param columns: Columns to use in constraint key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#columns TableConstraint#columns}
        :param name: Name of constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#name TableConstraint#name}
        :param table_id: Identifier for table to create constraint on. Format must follow: ""<db_name>"."<schema_name>"."<table_name>"" or "<db_name>.<schema_name>.<table_name>" (snowflake_table.my_table.id). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#table_id TableConstraint#table_id}
        :param type: Type of constraint, one of 'UNIQUE', 'PRIMARY KEY', or 'FOREIGN KEY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#type TableConstraint#type}
        :param comment: Comment for the table constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#comment TableConstraint#comment}
        :param deferrable: Whether the constraint is deferrable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#deferrable TableConstraint#deferrable}
        :param enable: Specifies whether the constraint is enabled or disabled. These properties are provided for compatibility with Oracle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#enable TableConstraint#enable}
        :param enforced: Whether the constraint is enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#enforced TableConstraint#enforced}
        :param foreign_key_properties: foreign_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#foreign_key_properties TableConstraint#foreign_key_properties}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#id TableConstraint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initially: Whether the constraint is initially deferred or immediate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#initially TableConstraint#initially}
        :param rely: Specifies whether a constraint in NOVALIDATE mode is taken into account during query rewrite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#rely TableConstraint#rely}
        :param validate: Specifies whether to validate existing data on the table when a constraint is created. Only used in conjunction with the ENABLE property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#validate TableConstraint#validate}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(foreign_key_properties, dict):
            foreign_key_properties = TableConstraintForeignKeyProperties(**foreign_key_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9df5e18034107dd0cc86997e9c3a6d14510215d8880f8e141057d32e60fc2a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument deferrable", value=deferrable, expected_type=type_hints["deferrable"])
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument enforced", value=enforced, expected_type=type_hints["enforced"])
            check_type(argname="argument foreign_key_properties", value=foreign_key_properties, expected_type=type_hints["foreign_key_properties"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initially", value=initially, expected_type=type_hints["initially"])
            check_type(argname="argument rely", value=rely, expected_type=type_hints["rely"])
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "name": name,
            "table_id": table_id,
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
        if comment is not None:
            self._values["comment"] = comment
        if deferrable is not None:
            self._values["deferrable"] = deferrable
        if enable is not None:
            self._values["enable"] = enable
        if enforced is not None:
            self._values["enforced"] = enforced
        if foreign_key_properties is not None:
            self._values["foreign_key_properties"] = foreign_key_properties
        if id is not None:
            self._values["id"] = id
        if initially is not None:
            self._values["initially"] = initially
        if rely is not None:
            self._values["rely"] = rely
        if validate is not None:
            self._values["validate"] = validate

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
    def columns(self) -> typing.List[builtins.str]:
        '''Columns to use in constraint key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#columns TableConstraint#columns}
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#name TableConstraint#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''Identifier for table to create constraint on. Format must follow: ""<db_name>"."<schema_name>"."<table_name>"" or "<db_name>.<schema_name>.<table_name>" (snowflake_table.my_table.id).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#table_id TableConstraint#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of constraint, one of 'UNIQUE', 'PRIMARY KEY', or 'FOREIGN KEY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#type TableConstraint#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Comment for the table constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#comment TableConstraint#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deferrable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the constraint is deferrable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#deferrable TableConstraint#deferrable}
        '''
        result = self._values.get("deferrable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the constraint is enabled or disabled. These properties are provided for compatibility with Oracle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#enable TableConstraint#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforced(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the constraint is enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#enforced TableConstraint#enforced}
        '''
        result = self._values.get("enforced")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def foreign_key_properties(
        self,
    ) -> typing.Optional["TableConstraintForeignKeyProperties"]:
        '''foreign_key_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#foreign_key_properties TableConstraint#foreign_key_properties}
        '''
        result = self._values.get("foreign_key_properties")
        return typing.cast(typing.Optional["TableConstraintForeignKeyProperties"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#id TableConstraint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initially(self) -> typing.Optional[builtins.str]:
        '''Whether the constraint is initially deferred or immediate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#initially TableConstraint#initially}
        '''
        result = self._values.get("initially")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rely(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether a constraint in NOVALIDATE mode is taken into account during query rewrite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#rely TableConstraint#rely}
        '''
        result = self._values.get("rely")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def validate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to validate existing data on the table when a constraint is created.

        Only used in conjunction with the ENABLE property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#validate TableConstraint#validate}
        '''
        result = self._values.get("validate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableConstraintConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.tableConstraint.TableConstraintForeignKeyProperties",
    jsii_struct_bases=[],
    name_mapping={
        "references": "references",
        "match": "match",
        "on_delete": "onDelete",
        "on_update": "onUpdate",
    },
)
class TableConstraintForeignKeyProperties:
    def __init__(
        self,
        *,
        references: typing.Union["TableConstraintForeignKeyPropertiesReferences", typing.Dict[builtins.str, typing.Any]],
        match: typing.Optional[builtins.str] = None,
        on_delete: typing.Optional[builtins.str] = None,
        on_update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param references: references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#references TableConstraint#references}
        :param match: The match type for the foreign key. Not applicable for primary/unique keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#match TableConstraint#match}
        :param on_delete: Specifies the action performed when the primary/unique key for the foreign key is deleted. Not applicable for primary/unique keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#on_delete TableConstraint#on_delete}
        :param on_update: Specifies the action performed when the primary/unique key for the foreign key is updated. Not applicable for primary/unique keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#on_update TableConstraint#on_update}
        '''
        if isinstance(references, dict):
            references = TableConstraintForeignKeyPropertiesReferences(**references)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c36fcca5cba070985ff51369bc9f1b455244a9d2db1662837edce1b128f9b27)
            check_type(argname="argument references", value=references, expected_type=type_hints["references"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument on_delete", value=on_delete, expected_type=type_hints["on_delete"])
            check_type(argname="argument on_update", value=on_update, expected_type=type_hints["on_update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "references": references,
        }
        if match is not None:
            self._values["match"] = match
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if on_update is not None:
            self._values["on_update"] = on_update

    @builtins.property
    def references(self) -> "TableConstraintForeignKeyPropertiesReferences":
        '''references block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#references TableConstraint#references}
        '''
        result = self._values.get("references")
        assert result is not None, "Required property 'references' is missing"
        return typing.cast("TableConstraintForeignKeyPropertiesReferences", result)

    @builtins.property
    def match(self) -> typing.Optional[builtins.str]:
        '''The match type for the foreign key. Not applicable for primary/unique keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#match TableConstraint#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_delete(self) -> typing.Optional[builtins.str]:
        '''Specifies the action performed when the primary/unique key for the foreign key is deleted. Not applicable for primary/unique keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#on_delete TableConstraint#on_delete}
        '''
        result = self._values.get("on_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_update(self) -> typing.Optional[builtins.str]:
        '''Specifies the action performed when the primary/unique key for the foreign key is updated. Not applicable for primary/unique keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#on_update TableConstraint#on_update}
        '''
        result = self._values.get("on_update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableConstraintForeignKeyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableConstraintForeignKeyPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.tableConstraint.TableConstraintForeignKeyPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dc8751ed2b591335fc4f6e11d2a9107b007140c845b6f49b990bee54ee27f6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReferences")
    def put_references(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        table_id: builtins.str,
    ) -> None:
        '''
        :param columns: Columns to use in foreign key reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#columns TableConstraint#columns}
        :param table_id: Name of constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#table_id TableConstraint#table_id}
        '''
        value = TableConstraintForeignKeyPropertiesReferences(
            columns=columns, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putReferences", [value]))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetOnDelete")
    def reset_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnDelete", []))

    @jsii.member(jsii_name="resetOnUpdate")
    def reset_on_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="references")
    def references(
        self,
    ) -> "TableConstraintForeignKeyPropertiesReferencesOutputReference":
        return typing.cast("TableConstraintForeignKeyPropertiesReferencesOutputReference", jsii.get(self, "references"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="onDeleteInput")
    def on_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="onUpdateInput")
    def on_update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="referencesInput")
    def references_input(
        self,
    ) -> typing.Optional["TableConstraintForeignKeyPropertiesReferences"]:
        return typing.cast(typing.Optional["TableConstraintForeignKeyPropertiesReferences"], jsii.get(self, "referencesInput"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa01e166da898e6663fbd0106e7b58976801b3a781a1a52529b574e14aa9bfce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onDelete")
    def on_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onDelete"))

    @on_delete.setter
    def on_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8618e8b0020388bedfa1b2a386dc4f9b4f8849c15f53ec91c5c62e498e88a2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onUpdate")
    def on_update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onUpdate"))

    @on_update.setter
    def on_update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb85ffc8f5963d17af2f8244cdba1f6e22f3fc2742efc35e00765b9723188c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TableConstraintForeignKeyProperties]:
        return typing.cast(typing.Optional[TableConstraintForeignKeyProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TableConstraintForeignKeyProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac01f8297c3230e4bfea87cb2e1269e4b6dce76351364cb615362a01b73a42ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.tableConstraint.TableConstraintForeignKeyPropertiesReferences",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns", "table_id": "tableId"},
)
class TableConstraintForeignKeyPropertiesReferences:
    def __init__(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        table_id: builtins.str,
    ) -> None:
        '''
        :param columns: Columns to use in foreign key reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#columns TableConstraint#columns}
        :param table_id: Name of constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#table_id TableConstraint#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31407e15cbe676dec2f6226a13eb038690049edbad3d2ad07d3a3d811012fe8)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "table_id": table_id,
        }

    @builtins.property
    def columns(self) -> typing.List[builtins.str]:
        '''Columns to use in foreign key reference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#columns TableConstraint#columns}
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''Name of constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table_constraint#table_id TableConstraint#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableConstraintForeignKeyPropertiesReferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableConstraintForeignKeyPropertiesReferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.tableConstraint.TableConstraintForeignKeyPropertiesReferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26cfe93390e2f6a8ea7e95271793feaea50b0e049163823b3e7fb40ec7b624e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371829fc7e84cfeacf2d202f065eb363f8f3906b349ae7db095ccdb9dd06f9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46dd4e227a628439a08fd03c538503a34dfd1b1ff01615826556ea27f74f98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TableConstraintForeignKeyPropertiesReferences]:
        return typing.cast(typing.Optional[TableConstraintForeignKeyPropertiesReferences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TableConstraintForeignKeyPropertiesReferences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadcbb455302de2ed26ae1e79caeb68005bfeed3d4126db4f53571ff05d7b81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TableConstraint",
    "TableConstraintConfig",
    "TableConstraintForeignKeyProperties",
    "TableConstraintForeignKeyPropertiesOutputReference",
    "TableConstraintForeignKeyPropertiesReferences",
    "TableConstraintForeignKeyPropertiesReferencesOutputReference",
]

publication.publish()

def _typecheckingstub__2f847fc51ba3e1f2e74fa00f985eab007437f3fcdcab055264677e72c8e41ebe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    columns: typing.Sequence[builtins.str],
    name: builtins.str,
    table_id: builtins.str,
    type: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    deferrable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    foreign_key_properties: typing.Optional[typing.Union[TableConstraintForeignKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initially: typing.Optional[builtins.str] = None,
    rely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__7d92440925415a5c265fe48c76e6e30459704e37cc3dc19f15ece9e870b45ec9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bf410ba761a23cd391fba8ef48e3eb67f547f4e982ccee1d1e215f60f0d8eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aa369a8bb54e80d30f3f7ef58259248ec268592a818330746cf8d71084cb08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ae460e60808175dd2f80f265a4100043c795a9805930409139e019b929b86f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3118d3fc78d0f0723a26da01b9168f53d982393d1712b6b7c65c4ff8ca1c0fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73392c63d744cc153ef7828df415325fe1fa428998618555003a818af23e1dcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588056dff60afba76832322beb82e0648de2d4b85e27315d9be26b8061be49a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c24a5e95d1103034367c8e466caceb6ceffb00a4f56292d35ff20ebd9771bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8756e8436e8eb4d533b5ca83b244dcdf3b0b2e14c9807132ee73fdd9f1146ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adf159ac03b3aa51311f617a12615ffec815084001ffc3b0e203728e443c26a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b285c3723d0aa3de5b663d75c6e0400fdb922d9927e96536ce3c02ec92c142bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a17131c16fd14d29ac5e6c0cfcec15c5f51e32cc8ea48322e4f64c7e9d92cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48b88b6fc5c4d58d73f1eac1aa9edc6d26d47089e3716b9b8cc4b56e7d4edcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9df5e18034107dd0cc86997e9c3a6d14510215d8880f8e141057d32e60fc2a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    columns: typing.Sequence[builtins.str],
    name: builtins.str,
    table_id: builtins.str,
    type: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    deferrable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforced: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    foreign_key_properties: typing.Optional[typing.Union[TableConstraintForeignKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    initially: typing.Optional[builtins.str] = None,
    rely: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c36fcca5cba070985ff51369bc9f1b455244a9d2db1662837edce1b128f9b27(
    *,
    references: typing.Union[TableConstraintForeignKeyPropertiesReferences, typing.Dict[builtins.str, typing.Any]],
    match: typing.Optional[builtins.str] = None,
    on_delete: typing.Optional[builtins.str] = None,
    on_update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc8751ed2b591335fc4f6e11d2a9107b007140c845b6f49b990bee54ee27f6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa01e166da898e6663fbd0106e7b58976801b3a781a1a52529b574e14aa9bfce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8618e8b0020388bedfa1b2a386dc4f9b4f8849c15f53ec91c5c62e498e88a2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb85ffc8f5963d17af2f8244cdba1f6e22f3fc2742efc35e00765b9723188c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac01f8297c3230e4bfea87cb2e1269e4b6dce76351364cb615362a01b73a42ce(
    value: typing.Optional[TableConstraintForeignKeyProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31407e15cbe676dec2f6226a13eb038690049edbad3d2ad07d3a3d811012fe8(
    *,
    columns: typing.Sequence[builtins.str],
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cfe93390e2f6a8ea7e95271793feaea50b0e049163823b3e7fb40ec7b624e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371829fc7e84cfeacf2d202f065eb363f8f3906b349ae7db095ccdb9dd06f9d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46dd4e227a628439a08fd03c538503a34dfd1b1ff01615826556ea27f74f98e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadcbb455302de2ed26ae1e79caeb68005bfeed3d4126db4f53571ff05d7b81e(
    value: typing.Optional[TableConstraintForeignKeyPropertiesReferences],
) -> None:
    """Type checking stubs"""
    pass
