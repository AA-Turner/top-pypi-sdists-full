r'''
# `opentelekomcloud_css_cluster_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_css_cluster_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1).
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


class CssClusterV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1 opentelekomcloud_css_cluster_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        node_config: typing.Union["CssClusterV1NodeConfig", typing.Dict[builtins.str, typing.Any]],
        admin_pass: typing.Optional[builtins.str] = None,
        backup_strategy: typing.Optional[typing.Union["CssClusterV1BackupStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        datastore: typing.Optional[typing.Union["CssClusterV1Datastore", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_authority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expect_node_num: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        public_access: typing.Optional[typing.Union["CssClusterV1PublicAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CssClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1 opentelekomcloud_css_cluster_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#name CssClusterV1#name}.
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#node_config CssClusterV1#node_config}
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#admin_pass CssClusterV1#admin_pass}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#backup_strategy CssClusterV1#backup_strategy}
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#datastore CssClusterV1#datastore}
        :param enable_authority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#enable_authority CssClusterV1#enable_authority}.
        :param enable_https: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#enable_https CssClusterV1#enable_https}.
        :param expect_node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#expect_node_num CssClusterV1#expect_node_num}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#id CssClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param public_access: public_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#public_access CssClusterV1#public_access}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#tags CssClusterV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#timeouts CssClusterV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b11d0ec1d22a84b6271e1074da81c2c795006935c0df14f37cd2ba0dbab4c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CssClusterV1Config(
            name=name,
            node_config=node_config,
            admin_pass=admin_pass,
            backup_strategy=backup_strategy,
            datastore=datastore,
            enable_authority=enable_authority,
            enable_https=enable_https,
            expect_node_num=expect_node_num,
            id=id,
            public_access=public_access,
            tags=tags,
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
        '''Generates CDKTF code for importing a CssClusterV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CssClusterV1 to import.
        :param import_from_id: The id of the existing CssClusterV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CssClusterV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4027551f20d3d1883735a69d23378e3066a9ca8022e51b19b7ff6f132d240dea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupStrategy")
    def put_backup_strategy(
        self,
        *,
        keep_days: jsii.Number,
        prefix: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#keep_days CssClusterV1#keep_days}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#prefix CssClusterV1#prefix}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#start_time CssClusterV1#start_time}.
        '''
        value = CssClusterV1BackupStrategy(
            keep_days=keep_days, prefix=prefix, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putBackupStrategy", [value]))

    @jsii.member(jsii_name="putDatastore")
    def put_datastore(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#type CssClusterV1#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#version CssClusterV1#version}.
        '''
        value = CssClusterV1Datastore(type=type, version=version)

        return typing.cast(None, jsii.invoke(self, "putDatastore", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        flavor: builtins.str,
        network_info: typing.Union["CssClusterV1NodeConfigNetworkInfo", typing.Dict[builtins.str, typing.Any]],
        volume: typing.Union["CssClusterV1NodeConfigVolume", typing.Dict[builtins.str, typing.Any]],
        availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#flavor CssClusterV1#flavor}.
        :param network_info: network_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#network_info CssClusterV1#network_info}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#volume CssClusterV1#volume}
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#availability_zone CssClusterV1#availability_zone}.
        '''
        value = CssClusterV1NodeConfig(
            flavor=flavor,
            network_info=network_info,
            volume=volume,
            availability_zone=availability_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putPublicAccess")
    def put_public_access(
        self,
        *,
        bandwidth: jsii.Number,
        whitelist_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        whitelist: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#bandwidth CssClusterV1#bandwidth}.
        :param whitelist_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#whitelist_enabled CssClusterV1#whitelist_enabled}.
        :param whitelist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#whitelist CssClusterV1#whitelist}.
        '''
        value = CssClusterV1PublicAccess(
            bandwidth=bandwidth,
            whitelist_enabled=whitelist_enabled,
            whitelist=whitelist,
        )

        return typing.cast(None, jsii.invoke(self, "putPublicAccess", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#create CssClusterV1#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#update CssClusterV1#update}.
        '''
        value = CssClusterV1Timeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminPass")
    def reset_admin_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPass", []))

    @jsii.member(jsii_name="resetBackupStrategy")
    def reset_backup_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupStrategy", []))

    @jsii.member(jsii_name="resetDatastore")
    def reset_datastore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatastore", []))

    @jsii.member(jsii_name="resetEnableAuthority")
    def reset_enable_authority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAuthority", []))

    @jsii.member(jsii_name="resetEnableHttps")
    def reset_enable_https(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHttps", []))

    @jsii.member(jsii_name="resetExpectNodeNum")
    def reset_expect_node_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectNodeNum", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPublicAccess")
    def reset_public_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicAccess", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="backupAvailable")
    def backup_available(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "backupAvailable"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategy")
    def backup_strategy(self) -> "CssClusterV1BackupStrategyOutputReference":
        return typing.cast("CssClusterV1BackupStrategyOutputReference", jsii.get(self, "backupStrategy"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> "CssClusterV1DatastoreOutputReference":
        return typing.cast("CssClusterV1DatastoreOutputReference", jsii.get(self, "datastore"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "CssClusterV1NodeConfigOutputReference":
        return typing.cast("CssClusterV1NodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> "CssClusterV1NodesList":
        return typing.cast("CssClusterV1NodesList", jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="publicAccess")
    def public_access(self) -> "CssClusterV1PublicAccessOutputReference":
        return typing.cast("CssClusterV1PublicAccessOutputReference", jsii.get(self, "publicAccess"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CssClusterV1TimeoutsOutputReference":
        return typing.cast("CssClusterV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="adminPassInput")
    def admin_pass_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPassInput"))

    @builtins.property
    @jsii.member(jsii_name="backupStrategyInput")
    def backup_strategy_input(self) -> typing.Optional["CssClusterV1BackupStrategy"]:
        return typing.cast(typing.Optional["CssClusterV1BackupStrategy"], jsii.get(self, "backupStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional["CssClusterV1Datastore"]:
        return typing.cast(typing.Optional["CssClusterV1Datastore"], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAuthorityInput")
    def enable_authority_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAuthorityInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpsInput")
    def enable_https_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttpsInput"))

    @builtins.property
    @jsii.member(jsii_name="expectNodeNumInput")
    def expect_node_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expectNodeNumInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(self) -> typing.Optional["CssClusterV1NodeConfig"]:
        return typing.cast(typing.Optional["CssClusterV1NodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="publicAccessInput")
    def public_access_input(self) -> typing.Optional["CssClusterV1PublicAccess"]:
        return typing.cast(typing.Optional["CssClusterV1PublicAccess"], jsii.get(self, "publicAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CssClusterV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CssClusterV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPass")
    def admin_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPass"))

    @admin_pass.setter
    def admin_pass(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d560d8ea87ffd4c7373b98efa57cb80083b9df5ded21018a0d54ba1631ac004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAuthority")
    def enable_authority(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAuthority"))

    @enable_authority.setter
    def enable_authority(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e5234e8a7a225cccb012c3c6f73fb3ba6084b7be54009aa721f2520aa6468b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAuthority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableHttps")
    def enable_https(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttps"))

    @enable_https.setter
    def enable_https(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3acc295b2548510dd138c6c2ff08c1ec30776ce08d365466c98edc982d6bc637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expectNodeNum")
    def expect_node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expectNodeNum"))

    @expect_node_num.setter
    def expect_node_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1fa517130c13abfaccf58147c8af2ece641c0478b7b15fd10d7996e3b8bf015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectNodeNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d50387399eb8e9bc21afb2dbf2bab8320992f40a86c4cbe9a2b80e5f7dfdf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21021f9ec4989962c8817efc4dd8adcb9027dc464c4da00eb4fae57d9293a4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e491de4d5e0c58035125675d9ad9c63b8b9731fdddfc5a04f8d9f7b4a911585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1BackupStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "keep_days": "keepDays",
        "prefix": "prefix",
        "start_time": "startTime",
    },
)
class CssClusterV1BackupStrategy:
    def __init__(
        self,
        *,
        keep_days: jsii.Number,
        prefix: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param keep_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#keep_days CssClusterV1#keep_days}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#prefix CssClusterV1#prefix}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#start_time CssClusterV1#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5059d4d8223e361d2b7dc68799e71fbe664f9a05aa53a26832ce580c141c8c2)
            check_type(argname="argument keep_days", value=keep_days, expected_type=type_hints["keep_days"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keep_days": keep_days,
            "prefix": prefix,
            "start_time": start_time,
        }

    @builtins.property
    def keep_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#keep_days CssClusterV1#keep_days}.'''
        result = self._values.get("keep_days")
        assert result is not None, "Required property 'keep_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#prefix CssClusterV1#prefix}.'''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#start_time CssClusterV1#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1BackupStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1BackupStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1BackupStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4008998ae88e81a56ba4c785f82308ce0b22fd9857a747e4d8907f65308ba04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keepDaysInput")
    def keep_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="keepDays")
    def keep_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepDays"))

    @keep_days.setter
    def keep_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316d9993c70ac575fca2255df2ebff51864555740e9dff7a29caf0aea1a74d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee569d2f1426b8e16693e588a4d0a617ce38b86988c0e8d8c8c8ca9358ad7338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cfe73af9d88dde415fbb5b121bb01e2652ebd71e392bd9f9e58322f3a02fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1BackupStrategy]:
        return typing.cast(typing.Optional[CssClusterV1BackupStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CssClusterV1BackupStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441b7dbf706489f102703886df434732b35fad3344cbbe501d85fc2b0b178e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "node_config": "nodeConfig",
        "admin_pass": "adminPass",
        "backup_strategy": "backupStrategy",
        "datastore": "datastore",
        "enable_authority": "enableAuthority",
        "enable_https": "enableHttps",
        "expect_node_num": "expectNodeNum",
        "id": "id",
        "public_access": "publicAccess",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class CssClusterV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        node_config: typing.Union["CssClusterV1NodeConfig", typing.Dict[builtins.str, typing.Any]],
        admin_pass: typing.Optional[builtins.str] = None,
        backup_strategy: typing.Optional[typing.Union[CssClusterV1BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
        datastore: typing.Optional[typing.Union["CssClusterV1Datastore", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_authority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expect_node_num: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        public_access: typing.Optional[typing.Union["CssClusterV1PublicAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CssClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#name CssClusterV1#name}.
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#node_config CssClusterV1#node_config}
        :param admin_pass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#admin_pass CssClusterV1#admin_pass}.
        :param backup_strategy: backup_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#backup_strategy CssClusterV1#backup_strategy}
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#datastore CssClusterV1#datastore}
        :param enable_authority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#enable_authority CssClusterV1#enable_authority}.
        :param enable_https: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#enable_https CssClusterV1#enable_https}.
        :param expect_node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#expect_node_num CssClusterV1#expect_node_num}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#id CssClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param public_access: public_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#public_access CssClusterV1#public_access}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#tags CssClusterV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#timeouts CssClusterV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(node_config, dict):
            node_config = CssClusterV1NodeConfig(**node_config)
        if isinstance(backup_strategy, dict):
            backup_strategy = CssClusterV1BackupStrategy(**backup_strategy)
        if isinstance(datastore, dict):
            datastore = CssClusterV1Datastore(**datastore)
        if isinstance(public_access, dict):
            public_access = CssClusterV1PublicAccess(**public_access)
        if isinstance(timeouts, dict):
            timeouts = CssClusterV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583ddacbcdd1dd84534bb1785d33e094a22d4071a3a33a3c4bdd71ea5bd9ff26)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument admin_pass", value=admin_pass, expected_type=type_hints["admin_pass"])
            check_type(argname="argument backup_strategy", value=backup_strategy, expected_type=type_hints["backup_strategy"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument enable_authority", value=enable_authority, expected_type=type_hints["enable_authority"])
            check_type(argname="argument enable_https", value=enable_https, expected_type=type_hints["enable_https"])
            check_type(argname="argument expect_node_num", value=expect_node_num, expected_type=type_hints["expect_node_num"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument public_access", value=public_access, expected_type=type_hints["public_access"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "node_config": node_config,
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
        if admin_pass is not None:
            self._values["admin_pass"] = admin_pass
        if backup_strategy is not None:
            self._values["backup_strategy"] = backup_strategy
        if datastore is not None:
            self._values["datastore"] = datastore
        if enable_authority is not None:
            self._values["enable_authority"] = enable_authority
        if enable_https is not None:
            self._values["enable_https"] = enable_https
        if expect_node_num is not None:
            self._values["expect_node_num"] = expect_node_num
        if id is not None:
            self._values["id"] = id
        if public_access is not None:
            self._values["public_access"] = public_access
        if tags is not None:
            self._values["tags"] = tags
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#name CssClusterV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_config(self) -> "CssClusterV1NodeConfig":
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#node_config CssClusterV1#node_config}
        '''
        result = self._values.get("node_config")
        assert result is not None, "Required property 'node_config' is missing"
        return typing.cast("CssClusterV1NodeConfig", result)

    @builtins.property
    def admin_pass(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#admin_pass CssClusterV1#admin_pass}.'''
        result = self._values.get("admin_pass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_strategy(self) -> typing.Optional[CssClusterV1BackupStrategy]:
        '''backup_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#backup_strategy CssClusterV1#backup_strategy}
        '''
        result = self._values.get("backup_strategy")
        return typing.cast(typing.Optional[CssClusterV1BackupStrategy], result)

    @builtins.property
    def datastore(self) -> typing.Optional["CssClusterV1Datastore"]:
        '''datastore block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#datastore CssClusterV1#datastore}
        '''
        result = self._values.get("datastore")
        return typing.cast(typing.Optional["CssClusterV1Datastore"], result)

    @builtins.property
    def enable_authority(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#enable_authority CssClusterV1#enable_authority}.'''
        result = self._values.get("enable_authority")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_https(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#enable_https CssClusterV1#enable_https}.'''
        result = self._values.get("enable_https")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expect_node_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#expect_node_num CssClusterV1#expect_node_num}.'''
        result = self._values.get("expect_node_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#id CssClusterV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_access(self) -> typing.Optional["CssClusterV1PublicAccess"]:
        '''public_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#public_access CssClusterV1#public_access}
        '''
        result = self._values.get("public_access")
        return typing.cast(typing.Optional["CssClusterV1PublicAccess"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#tags CssClusterV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CssClusterV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#timeouts CssClusterV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CssClusterV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1Datastore",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "version": "version"},
)
class CssClusterV1Datastore:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#type CssClusterV1#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#version CssClusterV1#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632c1ebcb58e234542fbb6f092a61341f5de0c8d072a08060bd3e45dc11cf35a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#type CssClusterV1#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#version CssClusterV1#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1Datastore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1DatastoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1DatastoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0013c70aac537e1a590e85e9ed26e96656c8ec6da94ec63786ef04b0f11ffcbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57dbfd2d85fafbc85ba57966b5c64040be85e586c335fe0309f4e130701e678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddd38fa4dffd56e16a565668c6bdff0a7429aab866dfe79903a6bc8c443dfaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1Datastore]:
        return typing.cast(typing.Optional[CssClusterV1Datastore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CssClusterV1Datastore]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4db2e08cc02c4d69acf3831561ba0efec80e3166889341c63d05410b21bdf6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "flavor": "flavor",
        "network_info": "networkInfo",
        "volume": "volume",
        "availability_zone": "availabilityZone",
    },
)
class CssClusterV1NodeConfig:
    def __init__(
        self,
        *,
        flavor: builtins.str,
        network_info: typing.Union["CssClusterV1NodeConfigNetworkInfo", typing.Dict[builtins.str, typing.Any]],
        volume: typing.Union["CssClusterV1NodeConfigVolume", typing.Dict[builtins.str, typing.Any]],
        availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#flavor CssClusterV1#flavor}.
        :param network_info: network_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#network_info CssClusterV1#network_info}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#volume CssClusterV1#volume}
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#availability_zone CssClusterV1#availability_zone}.
        '''
        if isinstance(network_info, dict):
            network_info = CssClusterV1NodeConfigNetworkInfo(**network_info)
        if isinstance(volume, dict):
            volume = CssClusterV1NodeConfigVolume(**volume)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed32b0e35e37bb714f29882bda971612e4117937fdb59708fc0981fdd9d015f0)
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument network_info", value=network_info, expected_type=type_hints["network_info"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flavor": flavor,
            "network_info": network_info,
            "volume": volume,
        }
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone

    @builtins.property
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#flavor CssClusterV1#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_info(self) -> "CssClusterV1NodeConfigNetworkInfo":
        '''network_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#network_info CssClusterV1#network_info}
        '''
        result = self._values.get("network_info")
        assert result is not None, "Required property 'network_info' is missing"
        return typing.cast("CssClusterV1NodeConfigNetworkInfo", result)

    @builtins.property
    def volume(self) -> "CssClusterV1NodeConfigVolume":
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#volume CssClusterV1#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("CssClusterV1NodeConfigVolume", result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#availability_zone CssClusterV1#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1NodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodeConfigNetworkInfo",
    jsii_struct_bases=[],
    name_mapping={
        "network_id": "networkId",
        "security_group_id": "securityGroupId",
        "vpc_id": "vpcId",
    },
)
class CssClusterV1NodeConfigNetworkInfo:
    def __init__(
        self,
        *,
        network_id: builtins.str,
        security_group_id: builtins.str,
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#network_id CssClusterV1#network_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#security_group_id CssClusterV1#security_group_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#vpc_id CssClusterV1#vpc_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08fe6755900468eee5cdf4afafafe283f4b3eef1506730f89f5a072260c5a05a)
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_id": network_id,
            "security_group_id": security_group_id,
            "vpc_id": vpc_id,
        }

    @builtins.property
    def network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#network_id CssClusterV1#network_id}.'''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#security_group_id CssClusterV1#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#vpc_id CssClusterV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1NodeConfigNetworkInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1NodeConfigNetworkInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodeConfigNetworkInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3df4ce3ab706db6741fbbf6ca30f0c8af2184509e99aa95e215409573d5174a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730cc6e37a7a033544dda13f63b62aa20a2839fe0ff16485de22ddebc5164674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7e301a61531b90c83483b40fa1b9e3b75c0ac8b1662b11d80145a3296dc47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f78c3cd972ce105e2a2cf055ce906e5f6dca76f9b93b687382108230ca659c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1NodeConfigNetworkInfo]:
        return typing.cast(typing.Optional[CssClusterV1NodeConfigNetworkInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CssClusterV1NodeConfigNetworkInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d370f5ca949d4acae338a61fc25161eab535cc07eade93f775aac2bd461bdf5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CssClusterV1NodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae2acf11c0721d808eb3e8005d97ee7f955d5d595a3006e35bc56e62ecfcc39b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInfo")
    def put_network_info(
        self,
        *,
        network_id: builtins.str,
        security_group_id: builtins.str,
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#network_id CssClusterV1#network_id}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#security_group_id CssClusterV1#security_group_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#vpc_id CssClusterV1#vpc_id}.
        '''
        value = CssClusterV1NodeConfigNetworkInfo(
            network_id=network_id, security_group_id=security_group_id, vpc_id=vpc_id
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkInfo", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        *,
        size: jsii.Number,
        volume_type: builtins.str,
        encryption_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#size CssClusterV1#size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#volume_type CssClusterV1#volume_type}.
        :param encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#encryption_key CssClusterV1#encryption_key}.
        '''
        value = CssClusterV1NodeConfigVolume(
            size=size, volume_type=volume_type, encryption_key=encryption_key
        )

        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @builtins.property
    @jsii.member(jsii_name="networkInfo")
    def network_info(self) -> CssClusterV1NodeConfigNetworkInfoOutputReference:
        return typing.cast(CssClusterV1NodeConfigNetworkInfoOutputReference, jsii.get(self, "networkInfo"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "CssClusterV1NodeConfigVolumeOutputReference":
        return typing.cast("CssClusterV1NodeConfigVolumeOutputReference", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInfoInput")
    def network_info_input(self) -> typing.Optional[CssClusterV1NodeConfigNetworkInfo]:
        return typing.cast(typing.Optional[CssClusterV1NodeConfigNetworkInfo], jsii.get(self, "networkInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional["CssClusterV1NodeConfigVolume"]:
        return typing.cast(typing.Optional["CssClusterV1NodeConfigVolume"], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2536b03f382f4c45e29f22759e12c1dbbdba98f37434242372c0a2e2a3f14714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496762065436de2edcabdb6de03e5af0b205910fa2c6bf584f2f07632c0552c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1NodeConfig]:
        return typing.cast(typing.Optional[CssClusterV1NodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CssClusterV1NodeConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbd35905cef904945fd4fc6c3a8862b61c034e0fc18b1a0b0ea28300e824388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodeConfigVolume",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volume_type": "volumeType",
        "encryption_key": "encryptionKey",
    },
)
class CssClusterV1NodeConfigVolume:
    def __init__(
        self,
        *,
        size: jsii.Number,
        volume_type: builtins.str,
        encryption_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#size CssClusterV1#size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#volume_type CssClusterV1#volume_type}.
        :param encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#encryption_key CssClusterV1#encryption_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b060a1b8c5358fdd8b6fde5afa981b3d479e7d74599d47e04f8919927f238ed6)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "volume_type": volume_type,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#size CssClusterV1#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#volume_type CssClusterV1#volume_type}.'''
        result = self._values.get("volume_type")
        assert result is not None, "Required property 'volume_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#encryption_key CssClusterV1#encryption_key}.'''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1NodeConfigVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1NodeConfigVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodeConfigVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4871f0638fa9cc6b1617657c7674754247c043868c4346a3505640543d34afa7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3b9f5640895fe7d79846f918541335ddb36e7b0ba2d147d341ac2f08ea3e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b835b006872486f37ea8f5748ad9e7e62745ce5d1449c5ae05d05e598317ccf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c15eb3d7ca54e1521554a9759cc478a533733dcd15421a8a2c211ca2f4f6e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1NodeConfigVolume]:
        return typing.cast(typing.Optional[CssClusterV1NodeConfigVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CssClusterV1NodeConfigVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3b33683b8bc40b608ca271114f5b6cb0d9764945f8d5885626e03779d0753a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1Nodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class CssClusterV1Nodes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1Nodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1NodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ff93429b12d6ed7244d829f06257527bfd30ebc6e2f26a9a1d3a1f413426fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CssClusterV1NodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4cc861b3922bf40e692b8baf2a7596968872f89fa421217850d66c75f34a0e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CssClusterV1NodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77dfaef6601250da9967839ea3f7714a1e2d163fcd857f1f4d4820a87e6e400)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06a2d7586e2cc2c02935b07f5c4ffc8fc41cae1be32933100e6e8d4052541fcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d52fdbc7a8a93b1d0900cd60c6d003b7d0953fb85a5539f320cdc792faf47be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CssClusterV1NodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1NodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94299056d39074877f7c8d896a338f840c3aff7a4776b24c576f1caa788b7306)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1Nodes]:
        return typing.cast(typing.Optional[CssClusterV1Nodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CssClusterV1Nodes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b44029ee7c296744c2d3b895d36fecce3e9ade8deea74457f544f6c4727724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1PublicAccess",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth": "bandwidth",
        "whitelist_enabled": "whitelistEnabled",
        "whitelist": "whitelist",
    },
)
class CssClusterV1PublicAccess:
    def __init__(
        self,
        *,
        bandwidth: jsii.Number,
        whitelist_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        whitelist: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#bandwidth CssClusterV1#bandwidth}.
        :param whitelist_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#whitelist_enabled CssClusterV1#whitelist_enabled}.
        :param whitelist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#whitelist CssClusterV1#whitelist}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae25358373247554aef0f7766128dc2083f9f326ce9f71f23413bcc3a848882d)
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument whitelist_enabled", value=whitelist_enabled, expected_type=type_hints["whitelist_enabled"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth": bandwidth,
            "whitelist_enabled": whitelist_enabled,
        }
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def bandwidth(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#bandwidth CssClusterV1#bandwidth}.'''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def whitelist_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#whitelist_enabled CssClusterV1#whitelist_enabled}.'''
        result = self._values.get("whitelist_enabled")
        assert result is not None, "Required property 'whitelist_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def whitelist(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#whitelist CssClusterV1#whitelist}.'''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1PublicAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1PublicAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1PublicAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__effaf7314347c142f081cc7d6087543998ba50322ec647763787747874f39d0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWhitelist")
    def reset_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhitelist", []))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInput")
    def bandwidth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelistEnabledInput")
    def whitelist_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "whitelistEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelistInput")
    def whitelist_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084209e2ad9c535cb0731ef5fe6acacda79b355c2977a68a2b8f841302c4549f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="whitelist")
    def whitelist(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "whitelist"))

    @whitelist.setter
    def whitelist(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b88b82654df02bce10090c8d7ae65b65253d40265f93ae6dbfb95fda426db65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="whitelistEnabled")
    def whitelist_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "whitelistEnabled"))

    @whitelist_enabled.setter
    def whitelist_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c43341e4159467ff48ca31ddc8aa99167dee6942d43aed7a385cb1c2348d92c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelistEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CssClusterV1PublicAccess]:
        return typing.cast(typing.Optional[CssClusterV1PublicAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CssClusterV1PublicAccess]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6894b0c296d464c5d50cccec2b09cfae26e62c8846ad829108cc14cf4b8a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class CssClusterV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#create CssClusterV1#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#update CssClusterV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74b6ff83668398d3416f481356a23f22d8fced291144b737fd1f188a4a7fad5)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#create CssClusterV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/css_cluster_v1#update CssClusterV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssClusterV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CssClusterV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cssClusterV1.CssClusterV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e527071bd0b301afd0294876a2d969f462bb12551e82f5527a75f2a5d40c9f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02f33ad3dcc68aca3423b647be7614f52475146a704509dd84878aa4e42b7e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38689a4035879c98a4c08fea42bf6723ef5c7b7c140a7777c3d059e901650e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssClusterV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssClusterV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssClusterV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b0f3f4ae031191484ceceaa19cb8ea715b03e777ed8a2c5837bd4f66136b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CssClusterV1",
    "CssClusterV1BackupStrategy",
    "CssClusterV1BackupStrategyOutputReference",
    "CssClusterV1Config",
    "CssClusterV1Datastore",
    "CssClusterV1DatastoreOutputReference",
    "CssClusterV1NodeConfig",
    "CssClusterV1NodeConfigNetworkInfo",
    "CssClusterV1NodeConfigNetworkInfoOutputReference",
    "CssClusterV1NodeConfigOutputReference",
    "CssClusterV1NodeConfigVolume",
    "CssClusterV1NodeConfigVolumeOutputReference",
    "CssClusterV1Nodes",
    "CssClusterV1NodesList",
    "CssClusterV1NodesOutputReference",
    "CssClusterV1PublicAccess",
    "CssClusterV1PublicAccessOutputReference",
    "CssClusterV1Timeouts",
    "CssClusterV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__78b11d0ec1d22a84b6271e1074da81c2c795006935c0df14f37cd2ba0dbab4c0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    node_config: typing.Union[CssClusterV1NodeConfig, typing.Dict[builtins.str, typing.Any]],
    admin_pass: typing.Optional[builtins.str] = None,
    backup_strategy: typing.Optional[typing.Union[CssClusterV1BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    datastore: typing.Optional[typing.Union[CssClusterV1Datastore, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_authority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expect_node_num: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    public_access: typing.Optional[typing.Union[CssClusterV1PublicAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CssClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4027551f20d3d1883735a69d23378e3066a9ca8022e51b19b7ff6f132d240dea(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d560d8ea87ffd4c7373b98efa57cb80083b9df5ded21018a0d54ba1631ac004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e5234e8a7a225cccb012c3c6f73fb3ba6084b7be54009aa721f2520aa6468b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acc295b2548510dd138c6c2ff08c1ec30776ce08d365466c98edc982d6bc637(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fa517130c13abfaccf58147c8af2ece641c0478b7b15fd10d7996e3b8bf015(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d50387399eb8e9bc21afb2dbf2bab8320992f40a86c4cbe9a2b80e5f7dfdf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21021f9ec4989962c8817efc4dd8adcb9027dc464c4da00eb4fae57d9293a4c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e491de4d5e0c58035125675d9ad9c63b8b9731fdddfc5a04f8d9f7b4a911585(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5059d4d8223e361d2b7dc68799e71fbe664f9a05aa53a26832ce580c141c8c2(
    *,
    keep_days: jsii.Number,
    prefix: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4008998ae88e81a56ba4c785f82308ce0b22fd9857a747e4d8907f65308ba04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316d9993c70ac575fca2255df2ebff51864555740e9dff7a29caf0aea1a74d01(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee569d2f1426b8e16693e588a4d0a617ce38b86988c0e8d8c8c8ca9358ad7338(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cfe73af9d88dde415fbb5b121bb01e2652ebd71e392bd9f9e58322f3a02fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441b7dbf706489f102703886df434732b35fad3344cbbe501d85fc2b0b178e89(
    value: typing.Optional[CssClusterV1BackupStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583ddacbcdd1dd84534bb1785d33e094a22d4071a3a33a3c4bdd71ea5bd9ff26(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    node_config: typing.Union[CssClusterV1NodeConfig, typing.Dict[builtins.str, typing.Any]],
    admin_pass: typing.Optional[builtins.str] = None,
    backup_strategy: typing.Optional[typing.Union[CssClusterV1BackupStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    datastore: typing.Optional[typing.Union[CssClusterV1Datastore, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_authority: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expect_node_num: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    public_access: typing.Optional[typing.Union[CssClusterV1PublicAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CssClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632c1ebcb58e234542fbb6f092a61341f5de0c8d072a08060bd3e45dc11cf35a(
    *,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0013c70aac537e1a590e85e9ed26e96656c8ec6da94ec63786ef04b0f11ffcbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57dbfd2d85fafbc85ba57966b5c64040be85e586c335fe0309f4e130701e678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddd38fa4dffd56e16a565668c6bdff0a7429aab866dfe79903a6bc8c443dfaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4db2e08cc02c4d69acf3831561ba0efec80e3166889341c63d05410b21bdf6f(
    value: typing.Optional[CssClusterV1Datastore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed32b0e35e37bb714f29882bda971612e4117937fdb59708fc0981fdd9d015f0(
    *,
    flavor: builtins.str,
    network_info: typing.Union[CssClusterV1NodeConfigNetworkInfo, typing.Dict[builtins.str, typing.Any]],
    volume: typing.Union[CssClusterV1NodeConfigVolume, typing.Dict[builtins.str, typing.Any]],
    availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fe6755900468eee5cdf4afafafe283f4b3eef1506730f89f5a072260c5a05a(
    *,
    network_id: builtins.str,
    security_group_id: builtins.str,
    vpc_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df4ce3ab706db6741fbbf6ca30f0c8af2184509e99aa95e215409573d5174a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730cc6e37a7a033544dda13f63b62aa20a2839fe0ff16485de22ddebc5164674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7e301a61531b90c83483b40fa1b9e3b75c0ac8b1662b11d80145a3296dc47d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f78c3cd972ce105e2a2cf055ce906e5f6dca76f9b93b687382108230ca659c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d370f5ca949d4acae338a61fc25161eab535cc07eade93f775aac2bd461bdf5a(
    value: typing.Optional[CssClusterV1NodeConfigNetworkInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2acf11c0721d808eb3e8005d97ee7f955d5d595a3006e35bc56e62ecfcc39b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2536b03f382f4c45e29f22759e12c1dbbdba98f37434242372c0a2e2a3f14714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496762065436de2edcabdb6de03e5af0b205910fa2c6bf584f2f07632c0552c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbd35905cef904945fd4fc6c3a8862b61c034e0fc18b1a0b0ea28300e824388(
    value: typing.Optional[CssClusterV1NodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b060a1b8c5358fdd8b6fde5afa981b3d479e7d74599d47e04f8919927f238ed6(
    *,
    size: jsii.Number,
    volume_type: builtins.str,
    encryption_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4871f0638fa9cc6b1617657c7674754247c043868c4346a3505640543d34afa7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3b9f5640895fe7d79846f918541335ddb36e7b0ba2d147d341ac2f08ea3e69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b835b006872486f37ea8f5748ad9e7e62745ce5d1449c5ae05d05e598317ccf9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c15eb3d7ca54e1521554a9759cc478a533733dcd15421a8a2c211ca2f4f6e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3b33683b8bc40b608ca271114f5b6cb0d9764945f8d5885626e03779d0753a(
    value: typing.Optional[CssClusterV1NodeConfigVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ff93429b12d6ed7244d829f06257527bfd30ebc6e2f26a9a1d3a1f413426fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cc861b3922bf40e692b8baf2a7596968872f89fa421217850d66c75f34a0e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77dfaef6601250da9967839ea3f7714a1e2d163fcd857f1f4d4820a87e6e400(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a2d7586e2cc2c02935b07f5c4ffc8fc41cae1be32933100e6e8d4052541fcc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d52fdbc7a8a93b1d0900cd60c6d003b7d0953fb85a5539f320cdc792faf47be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94299056d39074877f7c8d896a338f840c3aff7a4776b24c576f1caa788b7306(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b44029ee7c296744c2d3b895d36fecce3e9ade8deea74457f544f6c4727724(
    value: typing.Optional[CssClusterV1Nodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae25358373247554aef0f7766128dc2083f9f326ce9f71f23413bcc3a848882d(
    *,
    bandwidth: jsii.Number,
    whitelist_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    whitelist: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effaf7314347c142f081cc7d6087543998ba50322ec647763787747874f39d0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084209e2ad9c535cb0731ef5fe6acacda79b355c2977a68a2b8f841302c4549f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b88b82654df02bce10090c8d7ae65b65253d40265f93ae6dbfb95fda426db65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c43341e4159467ff48ca31ddc8aa99167dee6942d43aed7a385cb1c2348d92c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6894b0c296d464c5d50cccec2b09cfae26e62c8846ad829108cc14cf4b8a17(
    value: typing.Optional[CssClusterV1PublicAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74b6ff83668398d3416f481356a23f22d8fced291144b737fd1f188a4a7fad5(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e527071bd0b301afd0294876a2d969f462bb12551e82f5527a75f2a5d40c9f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f33ad3dcc68aca3423b647be7614f52475146a704509dd84878aa4e42b7e1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38689a4035879c98a4c08fea42bf6723ef5c7b7c140a7777c3d059e901650e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b0f3f4ae031191484ceceaa19cb8ea715b03e777ed8a2c5837bd4f66136b63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CssClusterV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
