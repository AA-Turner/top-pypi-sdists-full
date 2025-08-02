r'''
# `opentelekomcloud_drs_task_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_drs_task_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3).
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


class DrsTaskV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3 opentelekomcloud_drs_task_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_db: typing.Union["DrsTaskV3DestinationDb", typing.Dict[builtins.str, typing.Any]],
        direction: builtins.str,
        engine_type: builtins.str,
        name: builtins.str,
        source_db: typing.Union["DrsTaskV3SourceDb", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        destination_db_readonly: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expired_days: typing.Optional[jsii.Number] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        limit_speed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DrsTaskV3LimitSpeed", typing.Dict[builtins.str, typing.Any]]]]] = None,
        migrate_definer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        migration_type: typing.Optional[builtins.str] = None,
        multi_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        net_type: typing.Optional[builtins.str] = None,
        node_num: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DrsTaskV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3 opentelekomcloud_drs_task_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_db: destination_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#destination_db DrsTaskV3#destination_db}
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#direction DrsTaskV3#direction}.
        :param engine_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.
        :param source_db: source_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#source_db DrsTaskV3#source_db}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#type DrsTaskV3#type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#description DrsTaskV3#description}.
        :param destination_db_readonly: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#destination_db_readonly DrsTaskV3#destination_db_readonly}.
        :param expired_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#expired_days DrsTaskV3#expired_days}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#force_destroy DrsTaskV3#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#id DrsTaskV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param limit_speed: limit_speed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#limit_speed DrsTaskV3#limit_speed}
        :param migrate_definer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#migrate_definer DrsTaskV3#migrate_definer}.
        :param migration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#migration_type DrsTaskV3#migration_type}.
        :param multi_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#multi_write DrsTaskV3#multi_write}.
        :param net_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#net_type DrsTaskV3#net_type}.
        :param node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#node_num DrsTaskV3#node_num}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#start_time DrsTaskV3#start_time}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#tags DrsTaskV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#timeouts DrsTaskV3#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7838c1c2b3d09ded0df16ac866cd3bc5cd118a7b7f71f619befa8bdc9987237e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DrsTaskV3Config(
            destination_db=destination_db,
            direction=direction,
            engine_type=engine_type,
            name=name,
            source_db=source_db,
            type=type,
            description=description,
            destination_db_readonly=destination_db_readonly,
            expired_days=expired_days,
            force_destroy=force_destroy,
            id=id,
            limit_speed=limit_speed,
            migrate_definer=migrate_definer,
            migration_type=migration_type,
            multi_write=multi_write,
            net_type=net_type,
            node_num=node_num,
            start_time=start_time,
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
        '''Generates CDKTF code for importing a DrsTaskV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DrsTaskV3 to import.
        :param import_from_id: The id of the existing DrsTaskV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DrsTaskV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420b9396da887424053432fb68fcda72c9554ce8b90f5c197c8364b4dbf7c874)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationDb")
    def put_destination_db(
        self,
        *,
        engine_type: builtins.str,
        ip: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        user: builtins.str,
        instance_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_cert_check_sum: typing.Optional[builtins.str] = None,
        ssl_cert_key: typing.Optional[builtins.str] = None,
        ssl_cert_name: typing.Optional[builtins.str] = None,
        ssl_cert_password: typing.Optional[builtins.str] = None,
        ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.
        :param ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ip DrsTaskV3#ip}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#password DrsTaskV3#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#port DrsTaskV3#port}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#user DrsTaskV3#user}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#instance_id DrsTaskV3#instance_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#region DrsTaskV3#region}.
        :param ssl_cert_check_sum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_check_sum DrsTaskV3#ssl_cert_check_sum}.
        :param ssl_cert_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_key DrsTaskV3#ssl_cert_key}.
        :param ssl_cert_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_name DrsTaskV3#ssl_cert_name}.
        :param ssl_cert_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_password DrsTaskV3#ssl_cert_password}.
        :param ssl_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_enabled DrsTaskV3#ssl_enabled}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#subnet_id DrsTaskV3#subnet_id}.
        '''
        value = DrsTaskV3DestinationDb(
            engine_type=engine_type,
            ip=ip,
            password=password,
            port=port,
            user=user,
            instance_id=instance_id,
            name=name,
            region=region,
            ssl_cert_check_sum=ssl_cert_check_sum,
            ssl_cert_key=ssl_cert_key,
            ssl_cert_name=ssl_cert_name,
            ssl_cert_password=ssl_cert_password,
            ssl_enabled=ssl_enabled,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationDb", [value]))

    @jsii.member(jsii_name="putLimitSpeed")
    def put_limit_speed(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DrsTaskV3LimitSpeed", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fdc677dc030fe5318b20f673502fa446574129c26536c46e91cda44dfb3f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLimitSpeed", [value]))

    @jsii.member(jsii_name="putSourceDb")
    def put_source_db(
        self,
        *,
        engine_type: builtins.str,
        ip: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        user: builtins.str,
        instance_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_cert_check_sum: typing.Optional[builtins.str] = None,
        ssl_cert_key: typing.Optional[builtins.str] = None,
        ssl_cert_name: typing.Optional[builtins.str] = None,
        ssl_cert_password: typing.Optional[builtins.str] = None,
        ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.
        :param ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ip DrsTaskV3#ip}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#password DrsTaskV3#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#port DrsTaskV3#port}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#user DrsTaskV3#user}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#instance_id DrsTaskV3#instance_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#region DrsTaskV3#region}.
        :param ssl_cert_check_sum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_check_sum DrsTaskV3#ssl_cert_check_sum}.
        :param ssl_cert_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_key DrsTaskV3#ssl_cert_key}.
        :param ssl_cert_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_name DrsTaskV3#ssl_cert_name}.
        :param ssl_cert_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_password DrsTaskV3#ssl_cert_password}.
        :param ssl_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_enabled DrsTaskV3#ssl_enabled}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#subnet_id DrsTaskV3#subnet_id}.
        '''
        value = DrsTaskV3SourceDb(
            engine_type=engine_type,
            ip=ip,
            password=password,
            port=port,
            user=user,
            instance_id=instance_id,
            name=name,
            region=region,
            ssl_cert_check_sum=ssl_cert_check_sum,
            ssl_cert_key=ssl_cert_key,
            ssl_cert_name=ssl_cert_name,
            ssl_cert_password=ssl_cert_password,
            ssl_enabled=ssl_enabled,
            subnet_id=subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceDb", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#create DrsTaskV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#delete DrsTaskV3#delete}.
        '''
        value = DrsTaskV3Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestinationDbReadonly")
    def reset_destination_db_readonly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationDbReadonly", []))

    @jsii.member(jsii_name="resetExpiredDays")
    def reset_expired_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiredDays", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLimitSpeed")
    def reset_limit_speed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimitSpeed", []))

    @jsii.member(jsii_name="resetMigrateDefiner")
    def reset_migrate_definer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMigrateDefiner", []))

    @jsii.member(jsii_name="resetMigrationType")
    def reset_migration_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMigrationType", []))

    @jsii.member(jsii_name="resetMultiWrite")
    def reset_multi_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiWrite", []))

    @jsii.member(jsii_name="resetNetType")
    def reset_net_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetType", []))

    @jsii.member(jsii_name="resetNodeNum")
    def reset_node_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeNum", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="destinationDb")
    def destination_db(self) -> "DrsTaskV3DestinationDbOutputReference":
        return typing.cast("DrsTaskV3DestinationDbOutputReference", jsii.get(self, "destinationDb"))

    @builtins.property
    @jsii.member(jsii_name="limitSpeed")
    def limit_speed(self) -> "DrsTaskV3LimitSpeedList":
        return typing.cast("DrsTaskV3LimitSpeedList", jsii.get(self, "limitSpeed"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="sourceDb")
    def source_db(self) -> "DrsTaskV3SourceDbOutputReference":
        return typing.cast("DrsTaskV3SourceDbOutputReference", jsii.get(self, "sourceDb"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DrsTaskV3TimeoutsOutputReference":
        return typing.cast("DrsTaskV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationDbInput")
    def destination_db_input(self) -> typing.Optional["DrsTaskV3DestinationDb"]:
        return typing.cast(typing.Optional["DrsTaskV3DestinationDb"], jsii.get(self, "destinationDbInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationDbReadonlyInput")
    def destination_db_readonly_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "destinationDbReadonlyInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="engineTypeInput")
    def engine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="expiredDaysInput")
    def expired_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expiredDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="limitSpeedInput")
    def limit_speed_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DrsTaskV3LimitSpeed"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DrsTaskV3LimitSpeed"]]], jsii.get(self, "limitSpeedInput"))

    @builtins.property
    @jsii.member(jsii_name="migrateDefinerInput")
    def migrate_definer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "migrateDefinerInput"))

    @builtins.property
    @jsii.member(jsii_name="migrationTypeInput")
    def migration_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "migrationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="multiWriteInput")
    def multi_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multiWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="netTypeInput")
    def net_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeNumInput")
    def node_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeNumInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDbInput")
    def source_db_input(self) -> typing.Optional["DrsTaskV3SourceDb"]:
        return typing.cast(typing.Optional["DrsTaskV3SourceDb"], jsii.get(self, "sourceDbInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DrsTaskV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DrsTaskV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785fbd11cb40b257616fdc6c6c6ddbe919a078a8f9d1f5751b4dd0cf1881d2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationDbReadonly")
    def destination_db_readonly(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "destinationDbReadonly"))

    @destination_db_readonly.setter
    def destination_db_readonly(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9993508a366d5a1c192fb8f53c1d9b284bb2020516c99cc5f0bc5664beae03d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationDbReadonly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b47082981ac603adb9a1de55758e17cf8f6740c225975c7d0c5fc321849a871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e35819a09f3eeb9229cf71c4ffb709634ee9e8dd531ae03c5f28be4deb8a731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiredDays")
    def expired_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expiredDays"))

    @expired_days.setter
    def expired_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a7c4f3f746e818ef06009d7a305af86fcba600503f60caf3fa4da6768c5b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiredDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46facd7fc4ee4e9043fdd09bc384b64832aa083e40973d89eee4527d240694d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b079aedfa53b71ad92b667a115a41ab5e1812fefb54263824b3534bda7210e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="migrateDefiner")
    def migrate_definer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "migrateDefiner"))

    @migrate_definer.setter
    def migrate_definer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bb506ee38455a23f354173c8e2042821d1a5d2c18e633d1c1fa2897e123683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migrateDefiner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="migrationType")
    def migration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "migrationType"))

    @migration_type.setter
    def migration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f77d1551ff4a4e52a18bccd85e53468c9ed273240a817be43b7d2dcd7f1abaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "migrationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiWrite")
    def multi_write(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multiWrite"))

    @multi_write.setter
    def multi_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4527edfe3424398bd9717beb5ff3644f925501bcd0c5adb26a2cff623e78f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a418dc5afc04eae945c7964b5cdd37f80a9a0ef58d0e61d2c81611f6865e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netType")
    def net_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netType"))

    @net_type.setter
    def net_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261e589bb49a92f203541c6a370365dd75a649c196e969625f31b59cfb550384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeNum")
    def node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeNum"))

    @node_num.setter
    def node_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63a35c78698ca56b94adbc0cc9db2e36ca7998067c091cf7e72d58c497f9c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab3405157a95f97a37d9989b3af2a52bf801a8d4ebb341f5730f49a42b654ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6383afe5a2f1722083c7c9930d0c424121cbf131ab0ac2327bb59372c86e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c87aebf6e2bb9aa06238bb63254c12f443b0bb5bd94917d77607fa08f19e0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_db": "destinationDb",
        "direction": "direction",
        "engine_type": "engineType",
        "name": "name",
        "source_db": "sourceDb",
        "type": "type",
        "description": "description",
        "destination_db_readonly": "destinationDbReadonly",
        "expired_days": "expiredDays",
        "force_destroy": "forceDestroy",
        "id": "id",
        "limit_speed": "limitSpeed",
        "migrate_definer": "migrateDefiner",
        "migration_type": "migrationType",
        "multi_write": "multiWrite",
        "net_type": "netType",
        "node_num": "nodeNum",
        "start_time": "startTime",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class DrsTaskV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_db: typing.Union["DrsTaskV3DestinationDb", typing.Dict[builtins.str, typing.Any]],
        direction: builtins.str,
        engine_type: builtins.str,
        name: builtins.str,
        source_db: typing.Union["DrsTaskV3SourceDb", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        destination_db_readonly: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expired_days: typing.Optional[jsii.Number] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        limit_speed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DrsTaskV3LimitSpeed", typing.Dict[builtins.str, typing.Any]]]]] = None,
        migrate_definer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        migration_type: typing.Optional[builtins.str] = None,
        multi_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        net_type: typing.Optional[builtins.str] = None,
        node_num: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DrsTaskV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination_db: destination_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#destination_db DrsTaskV3#destination_db}
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#direction DrsTaskV3#direction}.
        :param engine_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.
        :param source_db: source_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#source_db DrsTaskV3#source_db}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#type DrsTaskV3#type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#description DrsTaskV3#description}.
        :param destination_db_readonly: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#destination_db_readonly DrsTaskV3#destination_db_readonly}.
        :param expired_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#expired_days DrsTaskV3#expired_days}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#force_destroy DrsTaskV3#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#id DrsTaskV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param limit_speed: limit_speed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#limit_speed DrsTaskV3#limit_speed}
        :param migrate_definer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#migrate_definer DrsTaskV3#migrate_definer}.
        :param migration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#migration_type DrsTaskV3#migration_type}.
        :param multi_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#multi_write DrsTaskV3#multi_write}.
        :param net_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#net_type DrsTaskV3#net_type}.
        :param node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#node_num DrsTaskV3#node_num}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#start_time DrsTaskV3#start_time}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#tags DrsTaskV3#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#timeouts DrsTaskV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination_db, dict):
            destination_db = DrsTaskV3DestinationDb(**destination_db)
        if isinstance(source_db, dict):
            source_db = DrsTaskV3SourceDb(**source_db)
        if isinstance(timeouts, dict):
            timeouts = DrsTaskV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca50ae3156205d446c1ddeb0499808f302dd8e152ba203bb39c9baa5b173144)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_db", value=destination_db, expected_type=type_hints["destination_db"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_db", value=source_db, expected_type=type_hints["source_db"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_db_readonly", value=destination_db_readonly, expected_type=type_hints["destination_db_readonly"])
            check_type(argname="argument expired_days", value=expired_days, expected_type=type_hints["expired_days"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument limit_speed", value=limit_speed, expected_type=type_hints["limit_speed"])
            check_type(argname="argument migrate_definer", value=migrate_definer, expected_type=type_hints["migrate_definer"])
            check_type(argname="argument migration_type", value=migration_type, expected_type=type_hints["migration_type"])
            check_type(argname="argument multi_write", value=multi_write, expected_type=type_hints["multi_write"])
            check_type(argname="argument net_type", value=net_type, expected_type=type_hints["net_type"])
            check_type(argname="argument node_num", value=node_num, expected_type=type_hints["node_num"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_db": destination_db,
            "direction": direction,
            "engine_type": engine_type,
            "name": name,
            "source_db": source_db,
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
        if description is not None:
            self._values["description"] = description
        if destination_db_readonly is not None:
            self._values["destination_db_readonly"] = destination_db_readonly
        if expired_days is not None:
            self._values["expired_days"] = expired_days
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if id is not None:
            self._values["id"] = id
        if limit_speed is not None:
            self._values["limit_speed"] = limit_speed
        if migrate_definer is not None:
            self._values["migrate_definer"] = migrate_definer
        if migration_type is not None:
            self._values["migration_type"] = migration_type
        if multi_write is not None:
            self._values["multi_write"] = multi_write
        if net_type is not None:
            self._values["net_type"] = net_type
        if node_num is not None:
            self._values["node_num"] = node_num
        if start_time is not None:
            self._values["start_time"] = start_time
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
    def destination_db(self) -> "DrsTaskV3DestinationDb":
        '''destination_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#destination_db DrsTaskV3#destination_db}
        '''
        result = self._values.get("destination_db")
        assert result is not None, "Required property 'destination_db' is missing"
        return typing.cast("DrsTaskV3DestinationDb", result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#direction DrsTaskV3#direction}.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.'''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_db(self) -> "DrsTaskV3SourceDb":
        '''source_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#source_db DrsTaskV3#source_db}
        '''
        result = self._values.get("source_db")
        assert result is not None, "Required property 'source_db' is missing"
        return typing.cast("DrsTaskV3SourceDb", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#type DrsTaskV3#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#description DrsTaskV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_db_readonly(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#destination_db_readonly DrsTaskV3#destination_db_readonly}.'''
        result = self._values.get("destination_db_readonly")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expired_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#expired_days DrsTaskV3#expired_days}.'''
        result = self._values.get("expired_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#force_destroy DrsTaskV3#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#id DrsTaskV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_speed(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DrsTaskV3LimitSpeed"]]]:
        '''limit_speed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#limit_speed DrsTaskV3#limit_speed}
        '''
        result = self._values.get("limit_speed")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DrsTaskV3LimitSpeed"]]], result)

    @builtins.property
    def migrate_definer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#migrate_definer DrsTaskV3#migrate_definer}.'''
        result = self._values.get("migrate_definer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def migration_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#migration_type DrsTaskV3#migration_type}.'''
        result = self._values.get("migration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#multi_write DrsTaskV3#multi_write}.'''
        result = self._values.get("multi_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def net_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#net_type DrsTaskV3#net_type}.'''
        result = self._values.get("net_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#node_num DrsTaskV3#node_num}.'''
        result = self._values.get("node_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#start_time DrsTaskV3#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#tags DrsTaskV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DrsTaskV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#timeouts DrsTaskV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DrsTaskV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrsTaskV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3DestinationDb",
    jsii_struct_bases=[],
    name_mapping={
        "engine_type": "engineType",
        "ip": "ip",
        "password": "password",
        "port": "port",
        "user": "user",
        "instance_id": "instanceId",
        "name": "name",
        "region": "region",
        "ssl_cert_check_sum": "sslCertCheckSum",
        "ssl_cert_key": "sslCertKey",
        "ssl_cert_name": "sslCertName",
        "ssl_cert_password": "sslCertPassword",
        "ssl_enabled": "sslEnabled",
        "subnet_id": "subnetId",
    },
)
class DrsTaskV3DestinationDb:
    def __init__(
        self,
        *,
        engine_type: builtins.str,
        ip: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        user: builtins.str,
        instance_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_cert_check_sum: typing.Optional[builtins.str] = None,
        ssl_cert_key: typing.Optional[builtins.str] = None,
        ssl_cert_name: typing.Optional[builtins.str] = None,
        ssl_cert_password: typing.Optional[builtins.str] = None,
        ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.
        :param ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ip DrsTaskV3#ip}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#password DrsTaskV3#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#port DrsTaskV3#port}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#user DrsTaskV3#user}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#instance_id DrsTaskV3#instance_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#region DrsTaskV3#region}.
        :param ssl_cert_check_sum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_check_sum DrsTaskV3#ssl_cert_check_sum}.
        :param ssl_cert_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_key DrsTaskV3#ssl_cert_key}.
        :param ssl_cert_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_name DrsTaskV3#ssl_cert_name}.
        :param ssl_cert_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_password DrsTaskV3#ssl_cert_password}.
        :param ssl_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_enabled DrsTaskV3#ssl_enabled}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#subnet_id DrsTaskV3#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d62c4b688521d013d9303f2bef6269168ab81a30ae87770fb636a3a2f51bd8)
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ssl_cert_check_sum", value=ssl_cert_check_sum, expected_type=type_hints["ssl_cert_check_sum"])
            check_type(argname="argument ssl_cert_key", value=ssl_cert_key, expected_type=type_hints["ssl_cert_key"])
            check_type(argname="argument ssl_cert_name", value=ssl_cert_name, expected_type=type_hints["ssl_cert_name"])
            check_type(argname="argument ssl_cert_password", value=ssl_cert_password, expected_type=type_hints["ssl_cert_password"])
            check_type(argname="argument ssl_enabled", value=ssl_enabled, expected_type=type_hints["ssl_enabled"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine_type": engine_type,
            "ip": ip,
            "password": password,
            "port": port,
            "user": user,
        }
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if ssl_cert_check_sum is not None:
            self._values["ssl_cert_check_sum"] = ssl_cert_check_sum
        if ssl_cert_key is not None:
            self._values["ssl_cert_key"] = ssl_cert_key
        if ssl_cert_name is not None:
            self._values["ssl_cert_name"] = ssl_cert_name
        if ssl_cert_password is not None:
            self._values["ssl_cert_password"] = ssl_cert_password
        if ssl_enabled is not None:
            self._values["ssl_enabled"] = ssl_enabled
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.'''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ip DrsTaskV3#ip}.'''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#password DrsTaskV3#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#port DrsTaskV3#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#user DrsTaskV3#user}.'''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#instance_id DrsTaskV3#instance_id}.'''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#region DrsTaskV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_check_sum(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_check_sum DrsTaskV3#ssl_cert_check_sum}.'''
        result = self._values.get("ssl_cert_check_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_key DrsTaskV3#ssl_cert_key}.'''
        result = self._values.get("ssl_cert_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_name DrsTaskV3#ssl_cert_name}.'''
        result = self._values.get("ssl_cert_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_password DrsTaskV3#ssl_cert_password}.'''
        result = self._values.get("ssl_cert_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_enabled DrsTaskV3#ssl_enabled}.'''
        result = self._values.get("ssl_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#subnet_id DrsTaskV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrsTaskV3DestinationDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DrsTaskV3DestinationDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3DestinationDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ac58a9a5acd707c7a25032bd8c4f246de2c8b0f10c2a1f095db6179b57fae1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSslCertCheckSum")
    def reset_ssl_cert_check_sum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertCheckSum", []))

    @jsii.member(jsii_name="resetSslCertKey")
    def reset_ssl_cert_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertKey", []))

    @jsii.member(jsii_name="resetSslCertName")
    def reset_ssl_cert_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertName", []))

    @jsii.member(jsii_name="resetSslCertPassword")
    def reset_ssl_cert_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertPassword", []))

    @jsii.member(jsii_name="resetSslEnabled")
    def reset_ssl_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslEnabled", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="engineTypeInput")
    def engine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertCheckSumInput")
    def ssl_cert_check_sum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertCheckSumInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertKeyInput")
    def ssl_cert_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertNameInput")
    def ssl_cert_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertPasswordInput")
    def ssl_cert_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sslEnabledInput")
    def ssl_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32862d88350d9d60816dd39e49db50969b178da6fe083d7f1fde27c4729228cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dac5ea3204ac7bb115456c5eeb001d4e9775e31ee115703523d93935389dd2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae39879ddb0dd2f2fb36cd8bc2570eb6be2400cb534554a4555f46f648c5536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4696c901933c161e312cff398c620e78be5136d80a10068ba76bdacd42c471d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1692d675d1cfbc45fb43718ac92b66bb459762d0d0b51dc06b7cc1fc4f9245b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421b678a5c1e91dc7686c721acc9b9b25c82d1fc3a214c497c838013c1d03a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bbf403ba25b8d862d54db616b326c867d24edb014babfd274c5bdf32c01456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertCheckSum")
    def ssl_cert_check_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertCheckSum"))

    @ssl_cert_check_sum.setter
    def ssl_cert_check_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8d60f94fdd25088f78ed502a67ad950fccfa7daa4c088f19f950e71d142d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertCheckSum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertKey")
    def ssl_cert_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertKey"))

    @ssl_cert_key.setter
    def ssl_cert_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce038c6b4d3101f759f514b28380cfa13f1c8e5848250c53af62fdb7f0171390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertName")
    def ssl_cert_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertName"))

    @ssl_cert_name.setter
    def ssl_cert_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6612075b6820cecd1984eb36e9ef3748b2c49a1fd8b9fd488fecb6e03a80c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertPassword")
    def ssl_cert_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertPassword"))

    @ssl_cert_password.setter
    def ssl_cert_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38e3f0bba85620a8ae504cbe8910ccfde010efa99c90b6366493ce05f49cc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslEnabled")
    def ssl_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sslEnabled"))

    @ssl_enabled.setter
    def ssl_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e5c4c556b897fba1a1ca710dfb72467530f309b32e2ff088645e950e89598c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fd284d63748e655d7d71130c6fcfd4a71da54f5d94bfe1c6f6182c78960a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f31761f0f99a24707f462de07a5c61e9fc812fe866a8c620d5222de6f57da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DrsTaskV3DestinationDb]:
        return typing.cast(typing.Optional[DrsTaskV3DestinationDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DrsTaskV3DestinationDb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4dfe82ecb139ac77093c9cc94ce1d6fe666b6811f3451b4ec9f515028764db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3LimitSpeed",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "speed": "speed", "start_time": "startTime"},
)
class DrsTaskV3LimitSpeed:
    def __init__(
        self,
        *,
        end_time: builtins.str,
        speed: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#end_time DrsTaskV3#end_time}.
        :param speed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#speed DrsTaskV3#speed}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#start_time DrsTaskV3#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1480ef8745f5127588129ccab9ec02db38eeaefb7c17e7e87565ed2dab27ed1e)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument speed", value=speed, expected_type=type_hints["speed"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_time": end_time,
            "speed": speed,
            "start_time": start_time,
        }

    @builtins.property
    def end_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#end_time DrsTaskV3#end_time}.'''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def speed(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#speed DrsTaskV3#speed}.'''
        result = self._values.get("speed")
        assert result is not None, "Required property 'speed' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#start_time DrsTaskV3#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrsTaskV3LimitSpeed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DrsTaskV3LimitSpeedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3LimitSpeedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d71720dc9bf9fd0fa49e285d1b16c13c5def21c3d86a558ffc9d0feac6bbc027)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DrsTaskV3LimitSpeedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487bf2f212d3711e100161b35fd45f1bfec748ed54ad12a15ca856fe83362a3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DrsTaskV3LimitSpeedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2baa017abc3289df7d31097c8b82a896f38d6af5bc61555fae891239c75bfa08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d39f1184e18f29a90415d1628e69cdbee2a42cbab192010b4b044537bc199095)
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
            type_hints = typing.get_type_hints(_typecheckingstub__624bba32dd225c31b205478990d194dbb05c79def0afb10d34d2136d1a91ee39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DrsTaskV3LimitSpeed]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DrsTaskV3LimitSpeed]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DrsTaskV3LimitSpeed]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e91205c20aa85092d812deaf820d4e218ea42612ad179c397ab0cff61ed7b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DrsTaskV3LimitSpeedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3LimitSpeedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c32c698add6b072d5bb6b59983042993ca972890ee5b0bb2bfc82bd75754c948)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="speedInput")
    def speed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "speedInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5a0c792c6a81f3e4d7c3835a66993950403598ec8eb9f5e57f228e26f332af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speed")
    def speed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speed"))

    @speed.setter
    def speed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba9db71dce65776b70d49044645558ab567f0e373311b228abc0668a0fce85c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906e0fc35631a46b6c4ae3e2699ed5ba014d507a4fdf711c594f2b8323509cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3LimitSpeed]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3LimitSpeed]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3LimitSpeed]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9987140d9575793a9fe6300a4e76181865b620035d85819cf0d1814ab5800e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3SourceDb",
    jsii_struct_bases=[],
    name_mapping={
        "engine_type": "engineType",
        "ip": "ip",
        "password": "password",
        "port": "port",
        "user": "user",
        "instance_id": "instanceId",
        "name": "name",
        "region": "region",
        "ssl_cert_check_sum": "sslCertCheckSum",
        "ssl_cert_key": "sslCertKey",
        "ssl_cert_name": "sslCertName",
        "ssl_cert_password": "sslCertPassword",
        "ssl_enabled": "sslEnabled",
        "subnet_id": "subnetId",
    },
)
class DrsTaskV3SourceDb:
    def __init__(
        self,
        *,
        engine_type: builtins.str,
        ip: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        user: builtins.str,
        instance_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ssl_cert_check_sum: typing.Optional[builtins.str] = None,
        ssl_cert_key: typing.Optional[builtins.str] = None,
        ssl_cert_name: typing.Optional[builtins.str] = None,
        ssl_cert_password: typing.Optional[builtins.str] = None,
        ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param engine_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.
        :param ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ip DrsTaskV3#ip}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#password DrsTaskV3#password}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#port DrsTaskV3#port}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#user DrsTaskV3#user}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#instance_id DrsTaskV3#instance_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#region DrsTaskV3#region}.
        :param ssl_cert_check_sum: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_check_sum DrsTaskV3#ssl_cert_check_sum}.
        :param ssl_cert_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_key DrsTaskV3#ssl_cert_key}.
        :param ssl_cert_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_name DrsTaskV3#ssl_cert_name}.
        :param ssl_cert_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_password DrsTaskV3#ssl_cert_password}.
        :param ssl_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_enabled DrsTaskV3#ssl_enabled}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#subnet_id DrsTaskV3#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17268970270f3c295d220be7ce9444eb726803980147b63b6bb521d34ef4d87f)
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ssl_cert_check_sum", value=ssl_cert_check_sum, expected_type=type_hints["ssl_cert_check_sum"])
            check_type(argname="argument ssl_cert_key", value=ssl_cert_key, expected_type=type_hints["ssl_cert_key"])
            check_type(argname="argument ssl_cert_name", value=ssl_cert_name, expected_type=type_hints["ssl_cert_name"])
            check_type(argname="argument ssl_cert_password", value=ssl_cert_password, expected_type=type_hints["ssl_cert_password"])
            check_type(argname="argument ssl_enabled", value=ssl_enabled, expected_type=type_hints["ssl_enabled"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine_type": engine_type,
            "ip": ip,
            "password": password,
            "port": port,
            "user": user,
        }
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if ssl_cert_check_sum is not None:
            self._values["ssl_cert_check_sum"] = ssl_cert_check_sum
        if ssl_cert_key is not None:
            self._values["ssl_cert_key"] = ssl_cert_key
        if ssl_cert_name is not None:
            self._values["ssl_cert_name"] = ssl_cert_name
        if ssl_cert_password is not None:
            self._values["ssl_cert_password"] = ssl_cert_password
        if ssl_enabled is not None:
            self._values["ssl_enabled"] = ssl_enabled
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#engine_type DrsTaskV3#engine_type}.'''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ip DrsTaskV3#ip}.'''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#password DrsTaskV3#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#port DrsTaskV3#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#user DrsTaskV3#user}.'''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#instance_id DrsTaskV3#instance_id}.'''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#name DrsTaskV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#region DrsTaskV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_check_sum(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_check_sum DrsTaskV3#ssl_cert_check_sum}.'''
        result = self._values.get("ssl_cert_check_sum")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_key DrsTaskV3#ssl_cert_key}.'''
        result = self._values.get("ssl_cert_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_name DrsTaskV3#ssl_cert_name}.'''
        result = self._values.get("ssl_cert_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_cert_password DrsTaskV3#ssl_cert_password}.'''
        result = self._values.get("ssl_cert_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#ssl_enabled DrsTaskV3#ssl_enabled}.'''
        result = self._values.get("ssl_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#subnet_id DrsTaskV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrsTaskV3SourceDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DrsTaskV3SourceDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3SourceDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7fbcb6a1ae01ac0b3c8dfbe8af441cb2e2464258db02c63416f3ec931c236ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSslCertCheckSum")
    def reset_ssl_cert_check_sum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertCheckSum", []))

    @jsii.member(jsii_name="resetSslCertKey")
    def reset_ssl_cert_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertKey", []))

    @jsii.member(jsii_name="resetSslCertName")
    def reset_ssl_cert_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertName", []))

    @jsii.member(jsii_name="resetSslCertPassword")
    def reset_ssl_cert_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCertPassword", []))

    @jsii.member(jsii_name="resetSslEnabled")
    def reset_ssl_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslEnabled", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="engineTypeInput")
    def engine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertCheckSumInput")
    def ssl_cert_check_sum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertCheckSumInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertKeyInput")
    def ssl_cert_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertNameInput")
    def ssl_cert_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCertPasswordInput")
    def ssl_cert_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCertPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sslEnabledInput")
    def ssl_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1908a2f82d5f5b7acfbd1f87bb1e3e835932f67f5ae1e28a90cbed4c492a2453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d890ddd88b961696149d5072ec52af8a70404b9cebdfd7b8929d07de963a9902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5601b465d72a503073bd86d401bfc2e279e2f761393db82e383be1aa86f1978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74953575a7e0fd937f07006a2b4e07b314c0a0c83956055744a5b2cead59b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423b23701145573352782e9865bcfc5f82fd1b8f7caddd3cd40f101693ecfbbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d6db0d0b6c4495f045d1c28698bc5a1b03f6c0313fdac69034a38cf953e3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff32e64e71091c2df86bf660ec32e564fa45b12e54ab2e752a0c539cb7ac66a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertCheckSum")
    def ssl_cert_check_sum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertCheckSum"))

    @ssl_cert_check_sum.setter
    def ssl_cert_check_sum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59294a745af2a14f32b0630cc5e27ef7dd1811d3cfbd92a22d48cfbffac95b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertCheckSum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertKey")
    def ssl_cert_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertKey"))

    @ssl_cert_key.setter
    def ssl_cert_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f414cd739ef0bb3fac2717c5518b3e2d7ef1c8fb6fc358ae8ed782aeecc16f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertName")
    def ssl_cert_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertName"))

    @ssl_cert_name.setter
    def ssl_cert_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064a75b9199c9af2a53fa532d853001ff6b3112b8db5693f4338c5a92e31c6e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCertPassword")
    def ssl_cert_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCertPassword"))

    @ssl_cert_password.setter
    def ssl_cert_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cf36e29f3fb65662a9a914ce46d1096961077fdd5022a1c8e11d018ac3a647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCertPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslEnabled")
    def ssl_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sslEnabled"))

    @ssl_enabled.setter
    def ssl_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994fc2073b3b2f37631ce059bce236f6582e99250249f8e9a3dfd7b69331f9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a517fc6753d2aaa049db00f90f14023968414ce96a34e22bbbdbab307568e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11c18595be94c0c1b53940232991bf2e46fc7c79910ef2bd9cbd5e4216e0508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DrsTaskV3SourceDb]:
        return typing.cast(typing.Optional[DrsTaskV3SourceDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DrsTaskV3SourceDb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4c69d34afd6e08c9fde017b77f8d44a617795e69a24acead42e4389cf95c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DrsTaskV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#create DrsTaskV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#delete DrsTaskV3#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddea68c2485ced71a161eb8518ac928af53de2c35698ec6e6526df31e355706)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#create DrsTaskV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/drs_task_v3#delete DrsTaskV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DrsTaskV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DrsTaskV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.drsTaskV3.DrsTaskV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b42a3100f1510c122951ed4bc4a9761f6b1ed6f9f39337d31418fce808e00ebe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3fa8ae090dd634571331dd581cb8d5768b3ebcbc56a023c59956286b139451a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a2fa7221bda013e1912a9785f1f3a89538b379b716a14c43fcde4b4fb281a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1558f949b3b0c42fe41339a8dd81bc0f674b2f5298c07c35eec129eb82efa1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DrsTaskV3",
    "DrsTaskV3Config",
    "DrsTaskV3DestinationDb",
    "DrsTaskV3DestinationDbOutputReference",
    "DrsTaskV3LimitSpeed",
    "DrsTaskV3LimitSpeedList",
    "DrsTaskV3LimitSpeedOutputReference",
    "DrsTaskV3SourceDb",
    "DrsTaskV3SourceDbOutputReference",
    "DrsTaskV3Timeouts",
    "DrsTaskV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7838c1c2b3d09ded0df16ac866cd3bc5cd118a7b7f71f619befa8bdc9987237e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_db: typing.Union[DrsTaskV3DestinationDb, typing.Dict[builtins.str, typing.Any]],
    direction: builtins.str,
    engine_type: builtins.str,
    name: builtins.str,
    source_db: typing.Union[DrsTaskV3SourceDb, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    destination_db_readonly: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expired_days: typing.Optional[jsii.Number] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    limit_speed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DrsTaskV3LimitSpeed, typing.Dict[builtins.str, typing.Any]]]]] = None,
    migrate_definer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    migration_type: typing.Optional[builtins.str] = None,
    multi_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    net_type: typing.Optional[builtins.str] = None,
    node_num: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DrsTaskV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__420b9396da887424053432fb68fcda72c9554ce8b90f5c197c8364b4dbf7c874(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fdc677dc030fe5318b20f673502fa446574129c26536c46e91cda44dfb3f0c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DrsTaskV3LimitSpeed, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785fbd11cb40b257616fdc6c6c6ddbe919a078a8f9d1f5751b4dd0cf1881d2a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9993508a366d5a1c192fb8f53c1d9b284bb2020516c99cc5f0bc5664beae03d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b47082981ac603adb9a1de55758e17cf8f6740c225975c7d0c5fc321849a871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e35819a09f3eeb9229cf71c4ffb709634ee9e8dd531ae03c5f28be4deb8a731(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a7c4f3f746e818ef06009d7a305af86fcba600503f60caf3fa4da6768c5b6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46facd7fc4ee4e9043fdd09bc384b64832aa083e40973d89eee4527d240694d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b079aedfa53b71ad92b667a115a41ab5e1812fefb54263824b3534bda7210e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bb506ee38455a23f354173c8e2042821d1a5d2c18e633d1c1fa2897e123683(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f77d1551ff4a4e52a18bccd85e53468c9ed273240a817be43b7d2dcd7f1abaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4527edfe3424398bd9717beb5ff3644f925501bcd0c5adb26a2cff623e78f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a418dc5afc04eae945c7964b5cdd37f80a9a0ef58d0e61d2c81611f6865e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261e589bb49a92f203541c6a370365dd75a649c196e969625f31b59cfb550384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63a35c78698ca56b94adbc0cc9db2e36ca7998067c091cf7e72d58c497f9c69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab3405157a95f97a37d9989b3af2a52bf801a8d4ebb341f5730f49a42b654ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6383afe5a2f1722083c7c9930d0c424121cbf131ab0ac2327bb59372c86e84(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c87aebf6e2bb9aa06238bb63254c12f443b0bb5bd94917d77607fa08f19e0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca50ae3156205d446c1ddeb0499808f302dd8e152ba203bb39c9baa5b173144(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_db: typing.Union[DrsTaskV3DestinationDb, typing.Dict[builtins.str, typing.Any]],
    direction: builtins.str,
    engine_type: builtins.str,
    name: builtins.str,
    source_db: typing.Union[DrsTaskV3SourceDb, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    destination_db_readonly: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expired_days: typing.Optional[jsii.Number] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    limit_speed: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DrsTaskV3LimitSpeed, typing.Dict[builtins.str, typing.Any]]]]] = None,
    migrate_definer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    migration_type: typing.Optional[builtins.str] = None,
    multi_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    net_type: typing.Optional[builtins.str] = None,
    node_num: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DrsTaskV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d62c4b688521d013d9303f2bef6269168ab81a30ae87770fb636a3a2f51bd8(
    *,
    engine_type: builtins.str,
    ip: builtins.str,
    password: builtins.str,
    port: jsii.Number,
    user: builtins.str,
    instance_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_cert_check_sum: typing.Optional[builtins.str] = None,
    ssl_cert_key: typing.Optional[builtins.str] = None,
    ssl_cert_name: typing.Optional[builtins.str] = None,
    ssl_cert_password: typing.Optional[builtins.str] = None,
    ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ac58a9a5acd707c7a25032bd8c4f246de2c8b0f10c2a1f095db6179b57fae1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32862d88350d9d60816dd39e49db50969b178da6fe083d7f1fde27c4729228cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dac5ea3204ac7bb115456c5eeb001d4e9775e31ee115703523d93935389dd2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae39879ddb0dd2f2fb36cd8bc2570eb6be2400cb534554a4555f46f648c5536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4696c901933c161e312cff398c620e78be5136d80a10068ba76bdacd42c471d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1692d675d1cfbc45fb43718ac92b66bb459762d0d0b51dc06b7cc1fc4f9245b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421b678a5c1e91dc7686c721acc9b9b25c82d1fc3a214c497c838013c1d03a26(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bbf403ba25b8d862d54db616b326c867d24edb014babfd274c5bdf32c01456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8d60f94fdd25088f78ed502a67ad950fccfa7daa4c088f19f950e71d142d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce038c6b4d3101f759f514b28380cfa13f1c8e5848250c53af62fdb7f0171390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6612075b6820cecd1984eb36e9ef3748b2c49a1fd8b9fd488fecb6e03a80c66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38e3f0bba85620a8ae504cbe8910ccfde010efa99c90b6366493ce05f49cc6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5c4c556b897fba1a1ca710dfb72467530f309b32e2ff088645e950e89598c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fd284d63748e655d7d71130c6fcfd4a71da54f5d94bfe1c6f6182c78960a0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f31761f0f99a24707f462de07a5c61e9fc812fe866a8c620d5222de6f57da4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4dfe82ecb139ac77093c9cc94ce1d6fe666b6811f3451b4ec9f515028764db(
    value: typing.Optional[DrsTaskV3DestinationDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1480ef8745f5127588129ccab9ec02db38eeaefb7c17e7e87565ed2dab27ed1e(
    *,
    end_time: builtins.str,
    speed: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71720dc9bf9fd0fa49e285d1b16c13c5def21c3d86a558ffc9d0feac6bbc027(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487bf2f212d3711e100161b35fd45f1bfec748ed54ad12a15ca856fe83362a3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2baa017abc3289df7d31097c8b82a896f38d6af5bc61555fae891239c75bfa08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39f1184e18f29a90415d1628e69cdbee2a42cbab192010b4b044537bc199095(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624bba32dd225c31b205478990d194dbb05c79def0afb10d34d2136d1a91ee39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e91205c20aa85092d812deaf820d4e218ea42612ad179c397ab0cff61ed7b18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DrsTaskV3LimitSpeed]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32c698add6b072d5bb6b59983042993ca972890ee5b0bb2bfc82bd75754c948(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5a0c792c6a81f3e4d7c3835a66993950403598ec8eb9f5e57f228e26f332af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba9db71dce65776b70d49044645558ab567f0e373311b228abc0668a0fce85c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906e0fc35631a46b6c4ae3e2699ed5ba014d507a4fdf711c594f2b8323509cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9987140d9575793a9fe6300a4e76181865b620035d85819cf0d1814ab5800e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3LimitSpeed]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17268970270f3c295d220be7ce9444eb726803980147b63b6bb521d34ef4d87f(
    *,
    engine_type: builtins.str,
    ip: builtins.str,
    password: builtins.str,
    port: jsii.Number,
    user: builtins.str,
    instance_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ssl_cert_check_sum: typing.Optional[builtins.str] = None,
    ssl_cert_key: typing.Optional[builtins.str] = None,
    ssl_cert_name: typing.Optional[builtins.str] = None,
    ssl_cert_password: typing.Optional[builtins.str] = None,
    ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fbcb6a1ae01ac0b3c8dfbe8af441cb2e2464258db02c63416f3ec931c236ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1908a2f82d5f5b7acfbd1f87bb1e3e835932f67f5ae1e28a90cbed4c492a2453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d890ddd88b961696149d5072ec52af8a70404b9cebdfd7b8929d07de963a9902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5601b465d72a503073bd86d401bfc2e279e2f761393db82e383be1aa86f1978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74953575a7e0fd937f07006a2b4e07b314c0a0c83956055744a5b2cead59b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423b23701145573352782e9865bcfc5f82fd1b8f7caddd3cd40f101693ecfbbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d6db0d0b6c4495f045d1c28698bc5a1b03f6c0313fdac69034a38cf953e3ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff32e64e71091c2df86bf660ec32e564fa45b12e54ab2e752a0c539cb7ac66a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59294a745af2a14f32b0630cc5e27ef7dd1811d3cfbd92a22d48cfbffac95b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f414cd739ef0bb3fac2717c5518b3e2d7ef1c8fb6fc358ae8ed782aeecc16f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064a75b9199c9af2a53fa532d853001ff6b3112b8db5693f4338c5a92e31c6e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cf36e29f3fb65662a9a914ce46d1096961077fdd5022a1c8e11d018ac3a647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994fc2073b3b2f37631ce059bce236f6582e99250249f8e9a3dfd7b69331f9c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a517fc6753d2aaa049db00f90f14023968414ce96a34e22bbbdbab307568e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11c18595be94c0c1b53940232991bf2e46fc7c79910ef2bd9cbd5e4216e0508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4c69d34afd6e08c9fde017b77f8d44a617795e69a24acead42e4389cf95c5e(
    value: typing.Optional[DrsTaskV3SourceDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddea68c2485ced71a161eb8518ac928af53de2c35698ec6e6526df31e355706(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42a3100f1510c122951ed4bc4a9761f6b1ed6f9f39337d31418fce808e00ebe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fa8ae090dd634571331dd581cb8d5768b3ebcbc56a023c59956286b139451a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a2fa7221bda013e1912a9785f1f3a89538b379b716a14c43fcde4b4fb281a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1558f949b3b0c42fe41339a8dd81bc0f674b2f5298c07c35eec129eb82efa1f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DrsTaskV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
