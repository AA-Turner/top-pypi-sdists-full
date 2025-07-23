r'''
# `google_bigtable_table`

Refer to the Terraform Registry for docs: [`google_bigtable_table`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table).
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


class BigtableTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table google_bigtable_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_name: builtins.str,
        name: builtins.str,
        automated_backup_policy: typing.Optional[typing.Union["BigtableTableAutomatedBackupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        change_stream_retention: typing.Optional[builtins.str] = None,
        column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableTableColumnFamily", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deletion_protection: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        row_key_schema: typing.Optional[builtins.str] = None,
        split_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BigtableTableTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table google_bigtable_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_name: The name of the Bigtable instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#instance_name BigtableTable#instance_name}
        :param name: The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#name BigtableTable#name}
        :param automated_backup_policy: automated_backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#automated_backup_policy BigtableTable#automated_backup_policy}
        :param change_stream_retention: Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#change_stream_retention BigtableTable#change_stream_retention}
        :param column_family: column_family block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#column_family BigtableTable#column_family}
        :param deletion_protection: A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, currently deletion protection will be set to UNPROTECTED as it is the API default value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#deletion_protection BigtableTable#deletion_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#id BigtableTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#project BigtableTable#project}
        :param row_key_schema: Defines the row key schema of a table. To create or update a table with a row key schema, specify this argument. Note that in-place update is not supported, and any in-place modification to the schema will lead to failure. To update a schema, please clear it (by omitting the field), and update the resource again with a new schema.\\n Example:: The schema must be a valid JSON encoded string representing a Type's struct protobuf message. Note that for bytes sequence (like delimited_bytes.delimiter) the delimiter must be base64 encoded. For example, if you want to set a delimiter to a single byte character "#", it should be set to "Iw==", which is the base64 encoding of the byte sequence "#". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#row_key_schema BigtableTable#row_key_schema}
        :param split_keys: A list of predefined keys to split the table on. !> Warning: Modifying the split_keys of an existing table will cause Terraform to delete/recreate the entire google_bigtable_table resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#split_keys BigtableTable#split_keys}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#timeouts BigtableTable#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1499603ea51c36ee146261312c1a2b754f3444eb1c55f94e75e75248a4ccff11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigtableTableConfig(
            instance_name=instance_name,
            name=name,
            automated_backup_policy=automated_backup_policy,
            change_stream_retention=change_stream_retention,
            column_family=column_family,
            deletion_protection=deletion_protection,
            id=id,
            project=project,
            row_key_schema=row_key_schema,
            split_keys=split_keys,
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
        '''Generates CDKTF code for importing a BigtableTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigtableTable to import.
        :param import_from_id: The id of the existing BigtableTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigtableTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73336f724ee0dd498459fe9b3067ef3e0be1e4e66b9b8bbc2b235bdddaa9f07a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedBackupPolicy")
    def put_automated_backup_policy(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: How frequently automated backups should occur. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#frequency BigtableTable#frequency}
        :param retention_period: How long the automated backups should be retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#retention_period BigtableTable#retention_period}
        '''
        value = BigtableTableAutomatedBackupPolicy(
            frequency=frequency, retention_period=retention_period
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedBackupPolicy", [value]))

    @jsii.member(jsii_name="putColumnFamily")
    def put_column_family(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableTableColumnFamily", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08227b5d571ff63b25c450a94bdafe9b6575b2d81252f4ef583377f3fb3f33d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumnFamily", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#create BigtableTable#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#update BigtableTable#update}.
        '''
        value = BigtableTableTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutomatedBackupPolicy")
    def reset_automated_backup_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatedBackupPolicy", []))

    @jsii.member(jsii_name="resetChangeStreamRetention")
    def reset_change_stream_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeStreamRetention", []))

    @jsii.member(jsii_name="resetColumnFamily")
    def reset_column_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnFamily", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRowKeySchema")
    def reset_row_key_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowKeySchema", []))

    @jsii.member(jsii_name="resetSplitKeys")
    def reset_split_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplitKeys", []))

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
    @jsii.member(jsii_name="automatedBackupPolicy")
    def automated_backup_policy(
        self,
    ) -> "BigtableTableAutomatedBackupPolicyOutputReference":
        return typing.cast("BigtableTableAutomatedBackupPolicyOutputReference", jsii.get(self, "automatedBackupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="columnFamily")
    def column_family(self) -> "BigtableTableColumnFamilyList":
        return typing.cast("BigtableTableColumnFamilyList", jsii.get(self, "columnFamily"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigtableTableTimeoutsOutputReference":
        return typing.cast("BigtableTableTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="automatedBackupPolicyInput")
    def automated_backup_policy_input(
        self,
    ) -> typing.Optional["BigtableTableAutomatedBackupPolicy"]:
        return typing.cast(typing.Optional["BigtableTableAutomatedBackupPolicy"], jsii.get(self, "automatedBackupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="changeStreamRetentionInput")
    def change_stream_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "changeStreamRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="columnFamilyInput")
    def column_family_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableTableColumnFamily"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableTableColumnFamily"]]], jsii.get(self, "columnFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNameInput")
    def instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rowKeySchemaInput")
    def row_key_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rowKeySchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="splitKeysInput")
    def split_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "splitKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigtableTableTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigtableTableTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="changeStreamRetention")
    def change_stream_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "changeStreamRetention"))

    @change_stream_retention.setter
    def change_stream_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1e19c1572649142e47c40eb6d7a658b5879b90e91f466123ef0aadd58b9acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeStreamRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37980d768d82b4f0398d383c79344f87960671be3334a8c037bd8f956d2bab68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceea3882ac38e19378b2fddefd229040ac11e367c666a5d08be6ddf92eec8299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceName")
    def instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceName"))

    @instance_name.setter
    def instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1814af09b6dad96de17b05bdece2049ed52bcff3b00b57c95e9977a8b81a01fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225957254875e01f6756a01782eee82092c5b11b55d5403d1142108e7ffc27f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626cd0d6448d93e6b6722bb31730c4ac4389da0dcee9a25b0d120aa9345c399c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowKeySchema")
    def row_key_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rowKeySchema"))

    @row_key_schema.setter
    def row_key_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e05fedf7823a620bb15d7f8a19b7ae2ac7eb289f6acd34bcafbb9c2c390fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowKeySchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="splitKeys")
    def split_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "splitKeys"))

    @split_keys.setter
    def split_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a223e1f84d835eab9247f558608d7443615b133d0ac6f6296c38b56b27f8bf17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "splitKeys", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableAutomatedBackupPolicy",
    jsii_struct_bases=[],
    name_mapping={"frequency": "frequency", "retention_period": "retentionPeriod"},
)
class BigtableTableAutomatedBackupPolicy:
    def __init__(
        self,
        *,
        frequency: typing.Optional[builtins.str] = None,
        retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency: How frequently automated backups should occur. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#frequency BigtableTable#frequency}
        :param retention_period: How long the automated backups should be retained. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#retention_period BigtableTable#retention_period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f806529cb84fecde2d2a789f51b78d18fb5cd7f170be404d3a5fae17dd787b)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if frequency is not None:
            self._values["frequency"] = frequency
        if retention_period is not None:
            self._values["retention_period"] = retention_period

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''How frequently automated backups should occur.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#frequency BigtableTable#frequency}
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[builtins.str]:
        '''How long the automated backups should be retained.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#retention_period BigtableTable#retention_period}
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableTableAutomatedBackupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableTableAutomatedBackupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableAutomatedBackupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83d9dc49ceb4269300ed2999619d5ac026353703a2b54c7fc84acaac78482767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetRetentionPeriod")
    def reset_retention_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d651818b9f169b04386dc51836b26f4039f9a417e5825c3de4deaf762b4caf2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPeriod"))

    @retention_period.setter
    def retention_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5d7e95399cd7b01e22a51fbf4e996e147e235c075d5adaf1f0613d68b6dc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigtableTableAutomatedBackupPolicy]:
        return typing.cast(typing.Optional[BigtableTableAutomatedBackupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigtableTableAutomatedBackupPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e8b409aab4c90984e74d4b60a0b0db8a5c7acb311a119937b53dfbe8b52a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableColumnFamily",
    jsii_struct_bases=[],
    name_mapping={"family": "family", "type": "type"},
)
class BigtableTableColumnFamily:
    def __init__(
        self,
        *,
        family: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param family: The name of the column family. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#family BigtableTable#family}
        :param type: The type of the column family. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#type BigtableTable#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33841b6d6c3f8d1b070973c1960e4431b857c91f34a84bf6f32ed2b2b78001bc)
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "family": family,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def family(self) -> builtins.str:
        '''The name of the column family.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#family BigtableTable#family}
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the column family.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#type BigtableTable#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableTableColumnFamily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableTableColumnFamilyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableColumnFamilyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09046238c50fa48eb8c3301039c909588cd63b4981283647c46a7588738606e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BigtableTableColumnFamilyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7221fb213164f54396b6d4b7fd8c4edafca8357891728cc4d9ce494ebcb52bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigtableTableColumnFamilyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9eff86a983d5b867497e991c36ea9974b7a6caf0c2943d99d44543ea14bec4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8863f90c5bf8f04fb033bc13b505bbe82421b00c9a354afbe87fd02d14ecfb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__274a76f60cc622f37930806ceb722a26bc667d1e1e8ea27d4ed82b4e6975fbdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableTableColumnFamily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableTableColumnFamily]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableTableColumnFamily]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dc91a4fe8acedbb7b537a624723eb82f0fb60048c657de3e41910ef050e7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigtableTableColumnFamilyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableColumnFamilyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edef5a78419a3c6c0b779afc74a7cb8d5819394885121706370439ab5c1c501b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="familyInput")
    def family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b78c23066d868f273d409a5d426132aed1d2713d86c1e99c8c44a235224515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28751ad48dc6e24c3653b16f0c36a3d5400d788fb63ef0ae9199b67ce6778517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableColumnFamily]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableColumnFamily]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableColumnFamily]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630af987512da16e68a2b6f079748c195cdf6c3e1c80a6679bdb77dd8f24a499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_name": "instanceName",
        "name": "name",
        "automated_backup_policy": "automatedBackupPolicy",
        "change_stream_retention": "changeStreamRetention",
        "column_family": "columnFamily",
        "deletion_protection": "deletionProtection",
        "id": "id",
        "project": "project",
        "row_key_schema": "rowKeySchema",
        "split_keys": "splitKeys",
        "timeouts": "timeouts",
    },
)
class BigtableTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_name: builtins.str,
        name: builtins.str,
        automated_backup_policy: typing.Optional[typing.Union[BigtableTableAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        change_stream_retention: typing.Optional[builtins.str] = None,
        column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableTableColumnFamily, typing.Dict[builtins.str, typing.Any]]]]] = None,
        deletion_protection: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        row_key_schema: typing.Optional[builtins.str] = None,
        split_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BigtableTableTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_name: The name of the Bigtable instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#instance_name BigtableTable#instance_name}
        :param name: The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#name BigtableTable#name}
        :param automated_backup_policy: automated_backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#automated_backup_policy BigtableTable#automated_backup_policy}
        :param change_stream_retention: Duration to retain change stream data for the table. Set to 0 to disable. Must be between 1 and 7 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#change_stream_retention BigtableTable#change_stream_retention}
        :param column_family: column_family block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#column_family BigtableTable#column_family}
        :param deletion_protection: A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, currently deletion protection will be set to UNPROTECTED as it is the API default value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#deletion_protection BigtableTable#deletion_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#id BigtableTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#project BigtableTable#project}
        :param row_key_schema: Defines the row key schema of a table. To create or update a table with a row key schema, specify this argument. Note that in-place update is not supported, and any in-place modification to the schema will lead to failure. To update a schema, please clear it (by omitting the field), and update the resource again with a new schema.\\n Example:: The schema must be a valid JSON encoded string representing a Type's struct protobuf message. Note that for bytes sequence (like delimited_bytes.delimiter) the delimiter must be base64 encoded. For example, if you want to set a delimiter to a single byte character "#", it should be set to "Iw==", which is the base64 encoding of the byte sequence "#". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#row_key_schema BigtableTable#row_key_schema}
        :param split_keys: A list of predefined keys to split the table on. !> Warning: Modifying the split_keys of an existing table will cause Terraform to delete/recreate the entire google_bigtable_table resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#split_keys BigtableTable#split_keys}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#timeouts BigtableTable#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_policy, dict):
            automated_backup_policy = BigtableTableAutomatedBackupPolicy(**automated_backup_policy)
        if isinstance(timeouts, dict):
            timeouts = BigtableTableTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf1b3822b1a425036d795cf074693a0754e892bc1ba2a01009f088a1b2739e6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument automated_backup_policy", value=automated_backup_policy, expected_type=type_hints["automated_backup_policy"])
            check_type(argname="argument change_stream_retention", value=change_stream_retention, expected_type=type_hints["change_stream_retention"])
            check_type(argname="argument column_family", value=column_family, expected_type=type_hints["column_family"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument row_key_schema", value=row_key_schema, expected_type=type_hints["row_key_schema"])
            check_type(argname="argument split_keys", value=split_keys, expected_type=type_hints["split_keys"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_name": instance_name,
            "name": name,
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
        if automated_backup_policy is not None:
            self._values["automated_backup_policy"] = automated_backup_policy
        if change_stream_retention is not None:
            self._values["change_stream_retention"] = change_stream_retention
        if column_family is not None:
            self._values["column_family"] = column_family
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if row_key_schema is not None:
            self._values["row_key_schema"] = row_key_schema
        if split_keys is not None:
            self._values["split_keys"] = split_keys
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
    def instance_name(self) -> builtins.str:
        '''The name of the Bigtable instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#instance_name BigtableTable#instance_name}
        '''
        result = self._values.get("instance_name")
        assert result is not None, "Required property 'instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the table. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#name BigtableTable#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automated_backup_policy(
        self,
    ) -> typing.Optional[BigtableTableAutomatedBackupPolicy]:
        '''automated_backup_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#automated_backup_policy BigtableTable#automated_backup_policy}
        '''
        result = self._values.get("automated_backup_policy")
        return typing.cast(typing.Optional[BigtableTableAutomatedBackupPolicy], result)

    @builtins.property
    def change_stream_retention(self) -> typing.Optional[builtins.str]:
        '''Duration to retain change stream data for the table.

        Set to 0 to disable. Must be between 1 and 7 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#change_stream_retention BigtableTable#change_stream_retention}
        '''
        result = self._values.get("change_stream_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column_family(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableTableColumnFamily]]]:
        '''column_family block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#column_family BigtableTable#column_family}
        '''
        result = self._values.get("column_family")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableTableColumnFamily]]], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.str]:
        '''A field to make the table protected against data loss i.e. when set to PROTECTED, deleting the table, the column families in the table, and the instance containing the table would be prohibited. If not provided, currently deletion protection will be set to UNPROTECTED as it is the API default value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#deletion_protection BigtableTable#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#id BigtableTable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#project BigtableTable#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def row_key_schema(self) -> typing.Optional[builtins.str]:
        '''Defines the row key schema of a table.

        To create or update a table with a row key schema, specify this argument.
        Note that in-place update is not supported, and any in-place modification to the schema will lead to failure.
        To update a schema, please clear it (by omitting the field), and update the resource again with a new schema.\\n Example::

           				The schema must be a valid JSON encoded string representing a Type's struct protobuf message. Note that for bytes sequence (like delimited_bytes.delimiter)
           				the delimiter must be base64 encoded. For example, if you want to set a delimiter to a single byte character "#", it should be set to "Iw==", which is the base64 encoding of the byte sequence "#".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#row_key_schema BigtableTable#row_key_schema}
        '''
        result = self._values.get("row_key_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def split_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of predefined keys to split the table on.

        !> Warning: Modifying the split_keys of an existing table will cause Terraform to delete/recreate the entire google_bigtable_table resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#split_keys BigtableTable#split_keys}
        '''
        result = self._values.get("split_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigtableTableTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#timeouts BigtableTable#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigtableTableTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class BigtableTableTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#create BigtableTable#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#update BigtableTable#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a2005c8eeb9b03661feb4670e8e1b5ec71bda69fb13e8aa8a5539b7e2fa825)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#create BigtableTable#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_table#update BigtableTable#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableTableTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableTableTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableTable.BigtableTableTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da532a67c0bc572d82c1a9f1be18f27e58ecbdb29716cf9aedeeb412de89489)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__00fd59a30b4373c5087a4df21e35f5232928e6e750d5be506fda09d73d8a8627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57a46695d6c5135a7e427f95c09f426d1f580c5242c8317404e8e9f5e75d517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca30939f1eff97620e054d761ce96648d146825724732412a1fb43813e6000f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigtableTable",
    "BigtableTableAutomatedBackupPolicy",
    "BigtableTableAutomatedBackupPolicyOutputReference",
    "BigtableTableColumnFamily",
    "BigtableTableColumnFamilyList",
    "BigtableTableColumnFamilyOutputReference",
    "BigtableTableConfig",
    "BigtableTableTimeouts",
    "BigtableTableTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1499603ea51c36ee146261312c1a2b754f3444eb1c55f94e75e75248a4ccff11(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_name: builtins.str,
    name: builtins.str,
    automated_backup_policy: typing.Optional[typing.Union[BigtableTableAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    change_stream_retention: typing.Optional[builtins.str] = None,
    column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableTableColumnFamily, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deletion_protection: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    row_key_schema: typing.Optional[builtins.str] = None,
    split_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BigtableTableTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__73336f724ee0dd498459fe9b3067ef3e0be1e4e66b9b8bbc2b235bdddaa9f07a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08227b5d571ff63b25c450a94bdafe9b6575b2d81252f4ef583377f3fb3f33d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableTableColumnFamily, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1e19c1572649142e47c40eb6d7a658b5879b90e91f466123ef0aadd58b9acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37980d768d82b4f0398d383c79344f87960671be3334a8c037bd8f956d2bab68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceea3882ac38e19378b2fddefd229040ac11e367c666a5d08be6ddf92eec8299(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1814af09b6dad96de17b05bdece2049ed52bcff3b00b57c95e9977a8b81a01fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225957254875e01f6756a01782eee82092c5b11b55d5403d1142108e7ffc27f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626cd0d6448d93e6b6722bb31730c4ac4389da0dcee9a25b0d120aa9345c399c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e05fedf7823a620bb15d7f8a19b7ae2ac7eb289f6acd34bcafbb9c2c390fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a223e1f84d835eab9247f558608d7443615b133d0ac6f6296c38b56b27f8bf17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f806529cb84fecde2d2a789f51b78d18fb5cd7f170be404d3a5fae17dd787b(
    *,
    frequency: typing.Optional[builtins.str] = None,
    retention_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d9dc49ceb4269300ed2999619d5ac026353703a2b54c7fc84acaac78482767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d651818b9f169b04386dc51836b26f4039f9a417e5825c3de4deaf762b4caf2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5d7e95399cd7b01e22a51fbf4e996e147e235c075d5adaf1f0613d68b6dc78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e8b409aab4c90984e74d4b60a0b0db8a5c7acb311a119937b53dfbe8b52a08(
    value: typing.Optional[BigtableTableAutomatedBackupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33841b6d6c3f8d1b070973c1960e4431b857c91f34a84bf6f32ed2b2b78001bc(
    *,
    family: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09046238c50fa48eb8c3301039c909588cd63b4981283647c46a7588738606e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7221fb213164f54396b6d4b7fd8c4edafca8357891728cc4d9ce494ebcb52bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9eff86a983d5b867497e991c36ea9974b7a6caf0c2943d99d44543ea14bec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8863f90c5bf8f04fb033bc13b505bbe82421b00c9a354afbe87fd02d14ecfb2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274a76f60cc622f37930806ceb722a26bc667d1e1e8ea27d4ed82b4e6975fbdb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dc91a4fe8acedbb7b537a624723eb82f0fb60048c657de3e41910ef050e7d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableTableColumnFamily]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edef5a78419a3c6c0b779afc74a7cb8d5819394885121706370439ab5c1c501b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b78c23066d868f273d409a5d426132aed1d2713d86c1e99c8c44a235224515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28751ad48dc6e24c3653b16f0c36a3d5400d788fb63ef0ae9199b67ce6778517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630af987512da16e68a2b6f079748c195cdf6c3e1c80a6679bdb77dd8f24a499(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableColumnFamily]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf1b3822b1a425036d795cf074693a0754e892bc1ba2a01009f088a1b2739e6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_name: builtins.str,
    name: builtins.str,
    automated_backup_policy: typing.Optional[typing.Union[BigtableTableAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    change_stream_retention: typing.Optional[builtins.str] = None,
    column_family: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableTableColumnFamily, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deletion_protection: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    row_key_schema: typing.Optional[builtins.str] = None,
    split_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BigtableTableTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a2005c8eeb9b03661feb4670e8e1b5ec71bda69fb13e8aa8a5539b7e2fa825(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da532a67c0bc572d82c1a9f1be18f27e58ecbdb29716cf9aedeeb412de89489(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fd59a30b4373c5087a4df21e35f5232928e6e750d5be506fda09d73d8a8627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57a46695d6c5135a7e427f95c09f426d1f580c5242c8317404e8e9f5e75d517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca30939f1eff97620e054d761ce96648d146825724732412a1fb43813e6000f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableTableTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
