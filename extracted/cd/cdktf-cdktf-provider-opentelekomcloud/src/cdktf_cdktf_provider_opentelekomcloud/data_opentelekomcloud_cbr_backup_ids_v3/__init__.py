r'''
# `data_opentelekomcloud_cbr_backup_ids_v3`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_cbr_backup_ids_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3).
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


class DataOpentelekomcloudCbrBackupIdsV3(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCbrBackupIdsV3.DataOpentelekomcloudCbrBackupIdsV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3 opentelekomcloud_cbr_backup_ids_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        checkpoint_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent_id: typing.Optional[builtins.str] = None,
        resource_az: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        vault_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3 opentelekomcloud_cbr_backup_ids_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param checkpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#checkpoint_id DataOpentelekomcloudCbrBackupIdsV3#checkpoint_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#id DataOpentelekomcloudCbrBackupIdsV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#image_type DataOpentelekomcloudCbrBackupIdsV3#image_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#name DataOpentelekomcloudCbrBackupIdsV3#name}.
        :param parent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#parent_id DataOpentelekomcloudCbrBackupIdsV3#parent_id}.
        :param resource_az: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_az DataOpentelekomcloudCbrBackupIdsV3#resource_az}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_id DataOpentelekomcloudCbrBackupIdsV3#resource_id}.
        :param resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_name DataOpentelekomcloudCbrBackupIdsV3#resource_name}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_type DataOpentelekomcloudCbrBackupIdsV3#resource_type}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#status DataOpentelekomcloudCbrBackupIdsV3#status}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#vault_id DataOpentelekomcloudCbrBackupIdsV3#vault_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59a8827972b695e2a4e19616df4ee185786fd38cfb38eb5635885b91d70f41a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudCbrBackupIdsV3Config(
            checkpoint_id=checkpoint_id,
            id=id,
            image_type=image_type,
            name=name,
            parent_id=parent_id,
            resource_az=resource_az,
            resource_id=resource_id,
            resource_name=resource_name,
            resource_type=resource_type,
            status=status,
            vault_id=vault_id,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudCbrBackupIdsV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudCbrBackupIdsV3 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudCbrBackupIdsV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudCbrBackupIdsV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdd832bc68ccee7a2794f4e8e5188fd2f1fbbbc09d6cee6ee27a55161d76e01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCheckpointId")
    def reset_checkpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckpointId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageType")
    def reset_image_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageType", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetParentId")
    def reset_parent_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentId", []))

    @jsii.member(jsii_name="resetResourceAz")
    def reset_resource_az(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceAz", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourceName")
    def reset_resource_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceName", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetVaultId")
    def reset_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVaultId", []))

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
    @jsii.member(jsii_name="ids")
    def ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ids"))

    @builtins.property
    @jsii.member(jsii_name="checkpointIdInput")
    def checkpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentIdInput")
    def parent_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAzInput")
    def resource_az_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceAzInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceNameInput")
    def resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="checkpointId")
    def checkpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkpointId"))

    @checkpoint_id.setter
    def checkpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd489be51b2a48f67fcd5b5f72c2765bfd26e1c4c3b05d67592cff0f6a8dc876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e4089fc549b3e6d353f935573c6beb546a9e70c3f56f8b07efe128b4c714bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5969b62655011afdb2ad9a3ee541ed58363721bf56f117591139c1f9c9e1184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55115ba8730cbdf0914e296c92050196d457a290aa3e262d8a508d6b9881e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentId")
    def parent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentId"))

    @parent_id.setter
    def parent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecf167433ccbe7835c6378f3b95fffac7c31a57baddd9e4e3504fe1c1631b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAz")
    def resource_az(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAz"))

    @resource_az.setter
    def resource_az(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8a6422f875cc4f88ec9917fbf1acf15b0b428b4f2087ff05075352e066a536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c31cff6ed061604496d9446899f00d8b1b4d6010d7c46168b1d22c31292faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceName")
    def resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceName"))

    @resource_name.setter
    def resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709bb5c95fe3063d10e701dbd7dad9543bfe28461bdb19fa9dadbf28803389cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e27db9b07c4c0496ef96ee950d692f610414d8d1d930817abbdf789e6c0d166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e8256912c209a0b1acd2fcdefc66c998a458b6753d145a4f04c7f1fac00c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438611d590dd489e7356b7b2f424054044a726904f5fd8ed130b95eb65191ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCbrBackupIdsV3.DataOpentelekomcloudCbrBackupIdsV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "checkpoint_id": "checkpointId",
        "id": "id",
        "image_type": "imageType",
        "name": "name",
        "parent_id": "parentId",
        "resource_az": "resourceAz",
        "resource_id": "resourceId",
        "resource_name": "resourceName",
        "resource_type": "resourceType",
        "status": "status",
        "vault_id": "vaultId",
    },
)
class DataOpentelekomcloudCbrBackupIdsV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        checkpoint_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent_id: typing.Optional[builtins.str] = None,
        resource_az: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        vault_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param checkpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#checkpoint_id DataOpentelekomcloudCbrBackupIdsV3#checkpoint_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#id DataOpentelekomcloudCbrBackupIdsV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#image_type DataOpentelekomcloudCbrBackupIdsV3#image_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#name DataOpentelekomcloudCbrBackupIdsV3#name}.
        :param parent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#parent_id DataOpentelekomcloudCbrBackupIdsV3#parent_id}.
        :param resource_az: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_az DataOpentelekomcloudCbrBackupIdsV3#resource_az}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_id DataOpentelekomcloudCbrBackupIdsV3#resource_id}.
        :param resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_name DataOpentelekomcloudCbrBackupIdsV3#resource_name}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_type DataOpentelekomcloudCbrBackupIdsV3#resource_type}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#status DataOpentelekomcloudCbrBackupIdsV3#status}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#vault_id DataOpentelekomcloudCbrBackupIdsV3#vault_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8499c9390aabbe8b5594a19a15626816b06c92e0c9b6b40e446976fca321e38d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument checkpoint_id", value=checkpoint_id, expected_type=type_hints["checkpoint_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_id", value=parent_id, expected_type=type_hints["parent_id"])
            check_type(argname="argument resource_az", value=resource_az, expected_type=type_hints["resource_az"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if checkpoint_id is not None:
            self._values["checkpoint_id"] = checkpoint_id
        if id is not None:
            self._values["id"] = id
        if image_type is not None:
            self._values["image_type"] = image_type
        if name is not None:
            self._values["name"] = name
        if parent_id is not None:
            self._values["parent_id"] = parent_id
        if resource_az is not None:
            self._values["resource_az"] = resource_az
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_name is not None:
            self._values["resource_name"] = resource_name
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if status is not None:
            self._values["status"] = status
        if vault_id is not None:
            self._values["vault_id"] = vault_id

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
    def checkpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#checkpoint_id DataOpentelekomcloudCbrBackupIdsV3#checkpoint_id}.'''
        result = self._values.get("checkpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#id DataOpentelekomcloudCbrBackupIdsV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#image_type DataOpentelekomcloudCbrBackupIdsV3#image_type}.'''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#name DataOpentelekomcloudCbrBackupIdsV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#parent_id DataOpentelekomcloudCbrBackupIdsV3#parent_id}.'''
        result = self._values.get("parent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_az(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_az DataOpentelekomcloudCbrBackupIdsV3#resource_az}.'''
        result = self._values.get("resource_az")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_id DataOpentelekomcloudCbrBackupIdsV3#resource_id}.'''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_name DataOpentelekomcloudCbrBackupIdsV3#resource_name}.'''
        result = self._values.get("resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#resource_type DataOpentelekomcloudCbrBackupIdsV3#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#status DataOpentelekomcloudCbrBackupIdsV3#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_ids_v3#vault_id DataOpentelekomcloudCbrBackupIdsV3#vault_id}.'''
        result = self._values.get("vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCbrBackupIdsV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudCbrBackupIdsV3",
    "DataOpentelekomcloudCbrBackupIdsV3Config",
]

publication.publish()

def _typecheckingstub__b59a8827972b695e2a4e19616df4ee185786fd38cfb38eb5635885b91d70f41a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    checkpoint_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_id: typing.Optional[builtins.str] = None,
    resource_az: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    vault_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5cdd832bc68ccee7a2794f4e8e5188fd2f1fbbbc09d6cee6ee27a55161d76e01(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd489be51b2a48f67fcd5b5f72c2765bfd26e1c4c3b05d67592cff0f6a8dc876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e4089fc549b3e6d353f935573c6beb546a9e70c3f56f8b07efe128b4c714bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5969b62655011afdb2ad9a3ee541ed58363721bf56f117591139c1f9c9e1184(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55115ba8730cbdf0914e296c92050196d457a290aa3e262d8a508d6b9881e3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecf167433ccbe7835c6378f3b95fffac7c31a57baddd9e4e3504fe1c1631b20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8a6422f875cc4f88ec9917fbf1acf15b0b428b4f2087ff05075352e066a536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c31cff6ed061604496d9446899f00d8b1b4d6010d7c46168b1d22c31292faf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709bb5c95fe3063d10e701dbd7dad9543bfe28461bdb19fa9dadbf28803389cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e27db9b07c4c0496ef96ee950d692f610414d8d1d930817abbdf789e6c0d166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e8256912c209a0b1acd2fcdefc66c998a458b6753d145a4f04c7f1fac00c60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438611d590dd489e7356b7b2f424054044a726904f5fd8ed130b95eb65191ca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8499c9390aabbe8b5594a19a15626816b06c92e0c9b6b40e446976fca321e38d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    checkpoint_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_id: typing.Optional[builtins.str] = None,
    resource_az: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    vault_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
