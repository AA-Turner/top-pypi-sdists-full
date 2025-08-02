r'''
# `data_opentelekomcloud_cce_addon_template_v3`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_cce_addon_template_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3).
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


class DataOpentelekomcloudCceAddonTemplateV3(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCceAddonTemplateV3.DataOpentelekomcloudCceAddonTemplateV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3 opentelekomcloud_cce_addon_template_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        addon_name: builtins.str,
        addon_version: builtins.str,
        cluster_ip: typing.Optional[builtins.str] = None,
        cluster_versions: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_version: typing.Optional[builtins.str] = None,
        swr_addr: typing.Optional[builtins.str] = None,
        swr_user: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3 opentelekomcloud_cce_addon_template_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param addon_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#addon_name DataOpentelekomcloudCceAddonTemplateV3#addon_name}.
        :param addon_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#addon_version DataOpentelekomcloudCceAddonTemplateV3#addon_version}.
        :param cluster_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#cluster_ip DataOpentelekomcloudCceAddonTemplateV3#cluster_ip}.
        :param cluster_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#cluster_versions DataOpentelekomcloudCceAddonTemplateV3#cluster_versions}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#id DataOpentelekomcloudCceAddonTemplateV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#image_version DataOpentelekomcloudCceAddonTemplateV3#image_version}.
        :param swr_addr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#swr_addr DataOpentelekomcloudCceAddonTemplateV3#swr_addr}.
        :param swr_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#swr_user DataOpentelekomcloudCceAddonTemplateV3#swr_user}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b9e06be76a4f5ef883e4930aae6c41528899bdf2d9bdae2823cf9d67b3b11c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudCceAddonTemplateV3Config(
            addon_name=addon_name,
            addon_version=addon_version,
            cluster_ip=cluster_ip,
            cluster_versions=cluster_versions,
            id=id,
            image_version=image_version,
            swr_addr=swr_addr,
            swr_user=swr_user,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudCceAddonTemplateV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudCceAddonTemplateV3 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudCceAddonTemplateV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudCceAddonTemplateV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1315bd7410a581221659654111a3d71170b5e73947d3e97bd02d7d4ce7465c52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetClusterIp")
    def reset_cluster_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIp", []))

    @jsii.member(jsii_name="resetClusterVersions")
    def reset_cluster_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterVersions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetSwrAddr")
    def reset_swr_addr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwrAddr", []))

    @jsii.member(jsii_name="resetSwrUser")
    def reset_swr_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwrUser", []))

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
    @jsii.member(jsii_name="addonNameInput")
    def addon_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="addonVersionInput")
    def addon_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addonVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpInput")
    def cluster_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIpInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionsInput")
    def cluster_versions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="swrAddrInput")
    def swr_addr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "swrAddrInput"))

    @builtins.property
    @jsii.member(jsii_name="swrUserInput")
    def swr_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "swrUserInput"))

    @builtins.property
    @jsii.member(jsii_name="addonName")
    def addon_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addonName"))

    @addon_name.setter
    def addon_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8ec87167608e4f8e9b95e64a704d1a34b889fc63c657168b4f9e837ed6e9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="addonVersion")
    def addon_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "addonVersion"))

    @addon_version.setter
    def addon_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1211840dc1026133c7a080a5ea94ef2a0937f5259aa4b56dcc5db91a78f3d961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addonVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterIp")
    def cluster_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIp"))

    @cluster_ip.setter
    def cluster_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0f67a17e6ae40f0e5eeff3ccf1b9a242bfd7a6b8999d0717847ea898d7c7bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterVersions")
    def cluster_versions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersions"))

    @cluster_versions.setter
    def cluster_versions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61603fea3c09dca7a54f285ac067d18bd4796671ca3182900360b89c9c3b526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ed31bc81b908c4d99d9a58143314d77208c33b43d80a1e246f96ee0ee8168a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772a5257d673b194ccdcd0dd27f84b56c8f3a97c2bc6d85fca302e929366f440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="swrAddr")
    def swr_addr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "swrAddr"))

    @swr_addr.setter
    def swr_addr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a346d12d7cef49ed788e7ce805fa3ad5faa60618de7fbae90ba0a6b272b6c361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swrAddr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="swrUser")
    def swr_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "swrUser"))

    @swr_user.setter
    def swr_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c019dde488d2bf4b3e5525a4ad93e17164d6251fe4087d8b7572fb15766cee9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "swrUser", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCceAddonTemplateV3.DataOpentelekomcloudCceAddonTemplateV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "addon_name": "addonName",
        "addon_version": "addonVersion",
        "cluster_ip": "clusterIp",
        "cluster_versions": "clusterVersions",
        "id": "id",
        "image_version": "imageVersion",
        "swr_addr": "swrAddr",
        "swr_user": "swrUser",
    },
)
class DataOpentelekomcloudCceAddonTemplateV3Config(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        addon_name: builtins.str,
        addon_version: builtins.str,
        cluster_ip: typing.Optional[builtins.str] = None,
        cluster_versions: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_version: typing.Optional[builtins.str] = None,
        swr_addr: typing.Optional[builtins.str] = None,
        swr_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param addon_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#addon_name DataOpentelekomcloudCceAddonTemplateV3#addon_name}.
        :param addon_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#addon_version DataOpentelekomcloudCceAddonTemplateV3#addon_version}.
        :param cluster_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#cluster_ip DataOpentelekomcloudCceAddonTemplateV3#cluster_ip}.
        :param cluster_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#cluster_versions DataOpentelekomcloudCceAddonTemplateV3#cluster_versions}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#id DataOpentelekomcloudCceAddonTemplateV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#image_version DataOpentelekomcloudCceAddonTemplateV3#image_version}.
        :param swr_addr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#swr_addr DataOpentelekomcloudCceAddonTemplateV3#swr_addr}.
        :param swr_user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#swr_user DataOpentelekomcloudCceAddonTemplateV3#swr_user}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6b94749cd6209559d0bb6c995229bc234fdc02ca94ec427be3b30addae507c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument addon_name", value=addon_name, expected_type=type_hints["addon_name"])
            check_type(argname="argument addon_version", value=addon_version, expected_type=type_hints["addon_version"])
            check_type(argname="argument cluster_ip", value=cluster_ip, expected_type=type_hints["cluster_ip"])
            check_type(argname="argument cluster_versions", value=cluster_versions, expected_type=type_hints["cluster_versions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument swr_addr", value=swr_addr, expected_type=type_hints["swr_addr"])
            check_type(argname="argument swr_user", value=swr_user, expected_type=type_hints["swr_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "addon_name": addon_name,
            "addon_version": addon_version,
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
        if cluster_ip is not None:
            self._values["cluster_ip"] = cluster_ip
        if cluster_versions is not None:
            self._values["cluster_versions"] = cluster_versions
        if id is not None:
            self._values["id"] = id
        if image_version is not None:
            self._values["image_version"] = image_version
        if swr_addr is not None:
            self._values["swr_addr"] = swr_addr
        if swr_user is not None:
            self._values["swr_user"] = swr_user

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
    def addon_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#addon_name DataOpentelekomcloudCceAddonTemplateV3#addon_name}.'''
        result = self._values.get("addon_name")
        assert result is not None, "Required property 'addon_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addon_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#addon_version DataOpentelekomcloudCceAddonTemplateV3#addon_version}.'''
        result = self._values.get("addon_version")
        assert result is not None, "Required property 'addon_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#cluster_ip DataOpentelekomcloudCceAddonTemplateV3#cluster_ip}.'''
        result = self._values.get("cluster_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_versions(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#cluster_versions DataOpentelekomcloudCceAddonTemplateV3#cluster_versions}.'''
        result = self._values.get("cluster_versions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#id DataOpentelekomcloudCceAddonTemplateV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#image_version DataOpentelekomcloudCceAddonTemplateV3#image_version}.'''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swr_addr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#swr_addr DataOpentelekomcloudCceAddonTemplateV3#swr_addr}.'''
        result = self._values.get("swr_addr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def swr_user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cce_addon_template_v3#swr_user DataOpentelekomcloudCceAddonTemplateV3#swr_user}.'''
        result = self._values.get("swr_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCceAddonTemplateV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudCceAddonTemplateV3",
    "DataOpentelekomcloudCceAddonTemplateV3Config",
]

publication.publish()

def _typecheckingstub__53b9e06be76a4f5ef883e4930aae6c41528899bdf2d9bdae2823cf9d67b3b11c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    addon_name: builtins.str,
    addon_version: builtins.str,
    cluster_ip: typing.Optional[builtins.str] = None,
    cluster_versions: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_version: typing.Optional[builtins.str] = None,
    swr_addr: typing.Optional[builtins.str] = None,
    swr_user: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1315bd7410a581221659654111a3d71170b5e73947d3e97bd02d7d4ce7465c52(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8ec87167608e4f8e9b95e64a704d1a34b889fc63c657168b4f9e837ed6e9cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1211840dc1026133c7a080a5ea94ef2a0937f5259aa4b56dcc5db91a78f3d961(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0f67a17e6ae40f0e5eeff3ccf1b9a242bfd7a6b8999d0717847ea898d7c7bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61603fea3c09dca7a54f285ac067d18bd4796671ca3182900360b89c9c3b526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ed31bc81b908c4d99d9a58143314d77208c33b43d80a1e246f96ee0ee8168a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772a5257d673b194ccdcd0dd27f84b56c8f3a97c2bc6d85fca302e929366f440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a346d12d7cef49ed788e7ce805fa3ad5faa60618de7fbae90ba0a6b272b6c361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c019dde488d2bf4b3e5525a4ad93e17164d6251fe4087d8b7572fb15766cee9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6b94749cd6209559d0bb6c995229bc234fdc02ca94ec427be3b30addae507c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    addon_name: builtins.str,
    addon_version: builtins.str,
    cluster_ip: typing.Optional[builtins.str] = None,
    cluster_versions: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_version: typing.Optional[builtins.str] = None,
    swr_addr: typing.Optional[builtins.str] = None,
    swr_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
