r'''
# `data_datadog_software_catalog`

Refer to the Terraform Registry for docs: [`data_datadog_software_catalog`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog).
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


class DataDatadogSoftwareCatalog(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogSoftwareCatalog.DataDatadogSoftwareCatalog",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog datadog_software_catalog}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filter_exclude_snapshot: typing.Optional[builtins.str] = None,
        filter_id: typing.Optional[builtins.str] = None,
        filter_kind: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        filter_owner: typing.Optional[builtins.str] = None,
        filter_ref: typing.Optional[builtins.str] = None,
        filter_relation_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog datadog_software_catalog} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter_exclude_snapshot: Filter entities by excluding snapshotted entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_exclude_snapshot DataDatadogSoftwareCatalog#filter_exclude_snapshot}
        :param filter_id: Filter entities by UUID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_id DataDatadogSoftwareCatalog#filter_id}
        :param filter_kind: Filter entities by kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_kind DataDatadogSoftwareCatalog#filter_kind}
        :param filter_name: Filter entities by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_name DataDatadogSoftwareCatalog#filter_name}
        :param filter_owner: Filter entities by owner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_owner DataDatadogSoftwareCatalog#filter_owner}
        :param filter_ref: Filter entities by reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_ref DataDatadogSoftwareCatalog#filter_ref}
        :param filter_relation_type: Filter entities by relation type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_relation_type DataDatadogSoftwareCatalog#filter_relation_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d112d23c610c3b4f9111e1032b65b66239de5505fcd38ddf9a968823c49e0b08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataDatadogSoftwareCatalogConfig(
            filter_exclude_snapshot=filter_exclude_snapshot,
            filter_id=filter_id,
            filter_kind=filter_kind,
            filter_name=filter_name,
            filter_owner=filter_owner,
            filter_ref=filter_ref,
            filter_relation_type=filter_relation_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatadogSoftwareCatalog resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatadogSoftwareCatalog to import.
        :param import_from_id: The id of the existing DataDatadogSoftwareCatalog that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatadogSoftwareCatalog to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12db630d0176d8672eb737153220749e2e5dd9ab811069b93356938f98181500)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetFilterExcludeSnapshot")
    def reset_filter_exclude_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterExcludeSnapshot", []))

    @jsii.member(jsii_name="resetFilterId")
    def reset_filter_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterId", []))

    @jsii.member(jsii_name="resetFilterKind")
    def reset_filter_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterKind", []))

    @jsii.member(jsii_name="resetFilterName")
    def reset_filter_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterName", []))

    @jsii.member(jsii_name="resetFilterOwner")
    def reset_filter_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterOwner", []))

    @jsii.member(jsii_name="resetFilterRef")
    def reset_filter_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterRef", []))

    @jsii.member(jsii_name="resetFilterRelationType")
    def reset_filter_relation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterRelationType", []))

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
    @jsii.member(jsii_name="entities")
    def entities(self) -> "DataDatadogSoftwareCatalogEntitiesList":
        return typing.cast("DataDatadogSoftwareCatalogEntitiesList", jsii.get(self, "entities"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="filterExcludeSnapshotInput")
    def filter_exclude_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterExcludeSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="filterIdInput")
    def filter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="filterKindInput")
    def filter_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterKindInput"))

    @builtins.property
    @jsii.member(jsii_name="filterNameInput")
    def filter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="filterOwnerInput")
    def filter_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="filterRefInput")
    def filter_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterRefInput"))

    @builtins.property
    @jsii.member(jsii_name="filterRelationTypeInput")
    def filter_relation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterRelationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="filterExcludeSnapshot")
    def filter_exclude_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterExcludeSnapshot"))

    @filter_exclude_snapshot.setter
    def filter_exclude_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026e6dec7f3914b5e9fa31eccb313b39ba2a43e0436dc7d06b4dbc3ca22c9c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterExcludeSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterId")
    def filter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterId"))

    @filter_id.setter
    def filter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9ae96142be5a860bf3d988aca10afb3e40eb3c1ba0ebd5b7ed6c115b8939ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterKind")
    def filter_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterKind"))

    @filter_kind.setter
    def filter_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02db1cd48741fa49ab177a6546e8fdb91fe9254dc427893984121e242ada1abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterName"))

    @filter_name.setter
    def filter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ec8e322d21b7e5fbe0b58a802ae0e11c8119c77216f9764b353af936b565cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterOwner")
    def filter_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterOwner"))

    @filter_owner.setter
    def filter_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f30677fe92c7b3a54967c5d166813facb14e726cd2761118e8dc97dda7a444b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterRef")
    def filter_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterRef"))

    @filter_ref.setter
    def filter_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8335e4c6e7efeff7e8bf0975de7ae2655eef1cb676d77d06e2616c0cbdfe31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterRelationType")
    def filter_relation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterRelationType"))

    @filter_relation_type.setter
    def filter_relation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f5566285ef22494e8b2916802c87be23ccfa476a7e1f9cb6e4b1e7ba79f851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterRelationType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogSoftwareCatalog.DataDatadogSoftwareCatalogConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter_exclude_snapshot": "filterExcludeSnapshot",
        "filter_id": "filterId",
        "filter_kind": "filterKind",
        "filter_name": "filterName",
        "filter_owner": "filterOwner",
        "filter_ref": "filterRef",
        "filter_relation_type": "filterRelationType",
    },
)
class DataDatadogSoftwareCatalogConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter_exclude_snapshot: typing.Optional[builtins.str] = None,
        filter_id: typing.Optional[builtins.str] = None,
        filter_kind: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        filter_owner: typing.Optional[builtins.str] = None,
        filter_ref: typing.Optional[builtins.str] = None,
        filter_relation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter_exclude_snapshot: Filter entities by excluding snapshotted entities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_exclude_snapshot DataDatadogSoftwareCatalog#filter_exclude_snapshot}
        :param filter_id: Filter entities by UUID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_id DataDatadogSoftwareCatalog#filter_id}
        :param filter_kind: Filter entities by kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_kind DataDatadogSoftwareCatalog#filter_kind}
        :param filter_name: Filter entities by name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_name DataDatadogSoftwareCatalog#filter_name}
        :param filter_owner: Filter entities by owner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_owner DataDatadogSoftwareCatalog#filter_owner}
        :param filter_ref: Filter entities by reference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_ref DataDatadogSoftwareCatalog#filter_ref}
        :param filter_relation_type: Filter entities by relation type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_relation_type DataDatadogSoftwareCatalog#filter_relation_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbe5ba0e4c6c5f2f9b980b3ee09b8d48100cfdae8dc3c65d3686014d074bdbf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter_exclude_snapshot", value=filter_exclude_snapshot, expected_type=type_hints["filter_exclude_snapshot"])
            check_type(argname="argument filter_id", value=filter_id, expected_type=type_hints["filter_id"])
            check_type(argname="argument filter_kind", value=filter_kind, expected_type=type_hints["filter_kind"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
            check_type(argname="argument filter_owner", value=filter_owner, expected_type=type_hints["filter_owner"])
            check_type(argname="argument filter_ref", value=filter_ref, expected_type=type_hints["filter_ref"])
            check_type(argname="argument filter_relation_type", value=filter_relation_type, expected_type=type_hints["filter_relation_type"])
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
        if filter_exclude_snapshot is not None:
            self._values["filter_exclude_snapshot"] = filter_exclude_snapshot
        if filter_id is not None:
            self._values["filter_id"] = filter_id
        if filter_kind is not None:
            self._values["filter_kind"] = filter_kind
        if filter_name is not None:
            self._values["filter_name"] = filter_name
        if filter_owner is not None:
            self._values["filter_owner"] = filter_owner
        if filter_ref is not None:
            self._values["filter_ref"] = filter_ref
        if filter_relation_type is not None:
            self._values["filter_relation_type"] = filter_relation_type

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
    def filter_exclude_snapshot(self) -> typing.Optional[builtins.str]:
        '''Filter entities by excluding snapshotted entities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_exclude_snapshot DataDatadogSoftwareCatalog#filter_exclude_snapshot}
        '''
        result = self._values.get("filter_exclude_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_id(self) -> typing.Optional[builtins.str]:
        '''Filter entities by UUID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_id DataDatadogSoftwareCatalog#filter_id}
        '''
        result = self._values.get("filter_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_kind(self) -> typing.Optional[builtins.str]:
        '''Filter entities by kind.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_kind DataDatadogSoftwareCatalog#filter_kind}
        '''
        result = self._values.get("filter_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''Filter entities by name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_name DataDatadogSoftwareCatalog#filter_name}
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_owner(self) -> typing.Optional[builtins.str]:
        '''Filter entities by owner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_owner DataDatadogSoftwareCatalog#filter_owner}
        '''
        result = self._values.get("filter_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_ref(self) -> typing.Optional[builtins.str]:
        '''Filter entities by reference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_ref DataDatadogSoftwareCatalog#filter_ref}
        '''
        result = self._values.get("filter_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_relation_type(self) -> typing.Optional[builtins.str]:
        '''Filter entities by relation type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/data-sources/software_catalog#filter_relation_type DataDatadogSoftwareCatalog#filter_relation_type}
        '''
        result = self._values.get("filter_relation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogSoftwareCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogSoftwareCatalog.DataDatadogSoftwareCatalogEntities",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataDatadogSoftwareCatalogEntities:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogSoftwareCatalogEntities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatadogSoftwareCatalogEntitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogSoftwareCatalog.DataDatadogSoftwareCatalogEntitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08df1f98ff3b36672f9ee1600f3a8dddaafdda03690e85cebc56c8e4d928c408)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatadogSoftwareCatalogEntitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de641d55ba6f3c04c0aef73c81422a8ede540b50266d0890bfe400f4d23c901)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatadogSoftwareCatalogEntitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33804ee9afc4d36227a22ecb405835dcbcdbc1cd8946ef870892d8a39cbd708a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b92bd7a173c5e53e0438fa9f02b719bdd13b785dbcee666b8307b476381524)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c668726c72e633b9f306e11948b88cb837ce98597a1774a0028cabc621a6200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataDatadogSoftwareCatalogEntitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogSoftwareCatalog.DataDatadogSoftwareCatalogEntitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cdd0da460372bdad6fd794f005ea82b67e93bac2dc17725505c08e211d9f407)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataDatadogSoftwareCatalogEntities]:
        return typing.cast(typing.Optional[DataDatadogSoftwareCatalogEntities], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatadogSoftwareCatalogEntities],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a200cfbd652c8cf7e704e21eff6f2f6f0139a41090353aed1bb885670c34f86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataDatadogSoftwareCatalog",
    "DataDatadogSoftwareCatalogConfig",
    "DataDatadogSoftwareCatalogEntities",
    "DataDatadogSoftwareCatalogEntitiesList",
    "DataDatadogSoftwareCatalogEntitiesOutputReference",
]

publication.publish()

def _typecheckingstub__d112d23c610c3b4f9111e1032b65b66239de5505fcd38ddf9a968823c49e0b08(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filter_exclude_snapshot: typing.Optional[builtins.str] = None,
    filter_id: typing.Optional[builtins.str] = None,
    filter_kind: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    filter_owner: typing.Optional[builtins.str] = None,
    filter_ref: typing.Optional[builtins.str] = None,
    filter_relation_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__12db630d0176d8672eb737153220749e2e5dd9ab811069b93356938f98181500(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026e6dec7f3914b5e9fa31eccb313b39ba2a43e0436dc7d06b4dbc3ca22c9c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9ae96142be5a860bf3d988aca10afb3e40eb3c1ba0ebd5b7ed6c115b8939ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02db1cd48741fa49ab177a6546e8fdb91fe9254dc427893984121e242ada1abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ec8e322d21b7e5fbe0b58a802ae0e11c8119c77216f9764b353af936b565cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f30677fe92c7b3a54967c5d166813facb14e726cd2761118e8dc97dda7a444b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8335e4c6e7efeff7e8bf0975de7ae2655eef1cb676d77d06e2616c0cbdfe31d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f5566285ef22494e8b2916802c87be23ccfa476a7e1f9cb6e4b1e7ba79f851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbe5ba0e4c6c5f2f9b980b3ee09b8d48100cfdae8dc3c65d3686014d074bdbf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter_exclude_snapshot: typing.Optional[builtins.str] = None,
    filter_id: typing.Optional[builtins.str] = None,
    filter_kind: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    filter_owner: typing.Optional[builtins.str] = None,
    filter_ref: typing.Optional[builtins.str] = None,
    filter_relation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08df1f98ff3b36672f9ee1600f3a8dddaafdda03690e85cebc56c8e4d928c408(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de641d55ba6f3c04c0aef73c81422a8ede540b50266d0890bfe400f4d23c901(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33804ee9afc4d36227a22ecb405835dcbcdbc1cd8946ef870892d8a39cbd708a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b92bd7a173c5e53e0438fa9f02b719bdd13b785dbcee666b8307b476381524(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c668726c72e633b9f306e11948b88cb837ce98597a1774a0028cabc621a6200(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdd0da460372bdad6fd794f005ea82b67e93bac2dc17725505c08e211d9f407(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a200cfbd652c8cf7e704e21eff6f2f6f0139a41090353aed1bb885670c34f86d(
    value: typing.Optional[DataDatadogSoftwareCatalogEntities],
) -> None:
    """Type checking stubs"""
    pass
