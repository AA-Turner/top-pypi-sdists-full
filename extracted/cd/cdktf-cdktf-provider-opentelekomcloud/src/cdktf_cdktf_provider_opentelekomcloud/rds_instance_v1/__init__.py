r'''
# `opentelekomcloud_rds_instance_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_rds_instance_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1).
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


class RdsInstanceV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1 opentelekomcloud_rds_instance_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availabilityzone: builtins.str,
        datastore: typing.Union["RdsInstanceV1Datastore", typing.Dict[builtins.str, typing.Any]],
        dbrtpd: builtins.str,
        flavorref: builtins.str,
        nics: typing.Union["RdsInstanceV1Nics", typing.Dict[builtins.str, typing.Any]],
        securitygroup: typing.Union["RdsInstanceV1Securitygroup", typing.Dict[builtins.str, typing.Any]],
        volume: typing.Union["RdsInstanceV1Volume", typing.Dict[builtins.str, typing.Any]],
        vpc: builtins.str,
        backupstrategy: typing.Optional[typing.Union["RdsInstanceV1Backupstrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        dbport: typing.Optional[builtins.str] = None,
        ha: typing.Optional[typing.Union["RdsInstanceV1Ha", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1 opentelekomcloud_rds_instance_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availabilityzone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#availabilityzone RdsInstanceV1#availabilityzone}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#datastore RdsInstanceV1#datastore}
        :param dbrtpd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#dbrtpd RdsInstanceV1#dbrtpd}.
        :param flavorref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#flavorref RdsInstanceV1#flavorref}.
        :param nics: nics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#nics RdsInstanceV1#nics}
        :param securitygroup: securitygroup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#securitygroup RdsInstanceV1#securitygroup}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#volume RdsInstanceV1#volume}
        :param vpc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#vpc RdsInstanceV1#vpc}.
        :param backupstrategy: backupstrategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#backupstrategy RdsInstanceV1#backupstrategy}
        :param dbport: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#dbport RdsInstanceV1#dbport}.
        :param ha: ha block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#ha RdsInstanceV1#ha}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#name RdsInstanceV1#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#region RdsInstanceV1#region}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#tag RdsInstanceV1#tag}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#timeouts RdsInstanceV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4311046b325f0c79281784863e5363866ca88990bd861a1fe1b620d426d7fcde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RdsInstanceV1Config(
            availabilityzone=availabilityzone,
            datastore=datastore,
            dbrtpd=dbrtpd,
            flavorref=flavorref,
            nics=nics,
            securitygroup=securitygroup,
            volume=volume,
            vpc=vpc,
            backupstrategy=backupstrategy,
            dbport=dbport,
            ha=ha,
            id=id,
            name=name,
            region=region,
            tag=tag,
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
        '''Generates CDKTF code for importing a RdsInstanceV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RdsInstanceV1 to import.
        :param import_from_id: The id of the existing RdsInstanceV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RdsInstanceV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea36474560124a1f7e71a79a4b17af0fe133e3b4847aec85319aacbed78e594e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupstrategy")
    def put_backupstrategy(
        self,
        *,
        keepdays: typing.Optional[jsii.Number] = None,
        starttime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keepdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#keepdays RdsInstanceV1#keepdays}.
        :param starttime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#starttime RdsInstanceV1#starttime}.
        '''
        value = RdsInstanceV1Backupstrategy(keepdays=keepdays, starttime=starttime)

        return typing.cast(None, jsii.invoke(self, "putBackupstrategy", [value]))

    @jsii.member(jsii_name="putDatastore")
    def put_datastore(self, *, type: builtins.str, version: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#type RdsInstanceV1#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#version RdsInstanceV1#version}.
        '''
        value = RdsInstanceV1Datastore(type=type, version=version)

        return typing.cast(None, jsii.invoke(self, "putDatastore", [value]))

    @jsii.member(jsii_name="putHa")
    def put_ha(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replicationmode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#enable RdsInstanceV1#enable}.
        :param replicationmode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#replicationmode RdsInstanceV1#replicationmode}.
        '''
        value = RdsInstanceV1Ha(enable=enable, replicationmode=replicationmode)

        return typing.cast(None, jsii.invoke(self, "putHa", [value]))

    @jsii.member(jsii_name="putNics")
    def put_nics(self, *, subnetid: builtins.str) -> None:
        '''
        :param subnetid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#subnetid RdsInstanceV1#subnetid}.
        '''
        value = RdsInstanceV1Nics(subnetid=subnetid)

        return typing.cast(None, jsii.invoke(self, "putNics", [value]))

    @jsii.member(jsii_name="putSecuritygroup")
    def put_securitygroup(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = RdsInstanceV1Securitygroup(id=id)

        return typing.cast(None, jsii.invoke(self, "putSecuritygroup", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#create RdsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#delete RdsInstanceV1#delete}.
        '''
        value = RdsInstanceV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(self, *, size: jsii.Number, type: builtins.str) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#size RdsInstanceV1#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#type RdsInstanceV1#type}.
        '''
        value = RdsInstanceV1Volume(size=size, type=type)

        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetBackupstrategy")
    def reset_backupstrategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupstrategy", []))

    @jsii.member(jsii_name="resetDbport")
    def reset_dbport(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbport", []))

    @jsii.member(jsii_name="resetHa")
    def reset_ha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHa", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="backupstrategy")
    def backupstrategy(self) -> "RdsInstanceV1BackupstrategyOutputReference":
        return typing.cast("RdsInstanceV1BackupstrategyOutputReference", jsii.get(self, "backupstrategy"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="datastore")
    def datastore(self) -> "RdsInstanceV1DatastoreOutputReference":
        return typing.cast("RdsInstanceV1DatastoreOutputReference", jsii.get(self, "datastore"))

    @builtins.property
    @jsii.member(jsii_name="ha")
    def ha(self) -> "RdsInstanceV1HaOutputReference":
        return typing.cast("RdsInstanceV1HaOutputReference", jsii.get(self, "ha"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="nics")
    def nics(self) -> "RdsInstanceV1NicsOutputReference":
        return typing.cast("RdsInstanceV1NicsOutputReference", jsii.get(self, "nics"))

    @builtins.property
    @jsii.member(jsii_name="securitygroup")
    def securitygroup(self) -> "RdsInstanceV1SecuritygroupOutputReference":
        return typing.cast("RdsInstanceV1SecuritygroupOutputReference", jsii.get(self, "securitygroup"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RdsInstanceV1TimeoutsOutputReference":
        return typing.cast("RdsInstanceV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "RdsInstanceV1VolumeOutputReference":
        return typing.cast("RdsInstanceV1VolumeOutputReference", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="availabilityzoneInput")
    def availabilityzone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityzoneInput"))

    @builtins.property
    @jsii.member(jsii_name="backupstrategyInput")
    def backupstrategy_input(self) -> typing.Optional["RdsInstanceV1Backupstrategy"]:
        return typing.cast(typing.Optional["RdsInstanceV1Backupstrategy"], jsii.get(self, "backupstrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreInput")
    def datastore_input(self) -> typing.Optional["RdsInstanceV1Datastore"]:
        return typing.cast(typing.Optional["RdsInstanceV1Datastore"], jsii.get(self, "datastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="dbportInput")
    def dbport_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbportInput"))

    @builtins.property
    @jsii.member(jsii_name="dbrtpdInput")
    def dbrtpd_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbrtpdInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorrefInput")
    def flavorref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorrefInput"))

    @builtins.property
    @jsii.member(jsii_name="haInput")
    def ha_input(self) -> typing.Optional["RdsInstanceV1Ha"]:
        return typing.cast(typing.Optional["RdsInstanceV1Ha"], jsii.get(self, "haInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nicsInput")
    def nics_input(self) -> typing.Optional["RdsInstanceV1Nics"]:
        return typing.cast(typing.Optional["RdsInstanceV1Nics"], jsii.get(self, "nicsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securitygroupInput")
    def securitygroup_input(self) -> typing.Optional["RdsInstanceV1Securitygroup"]:
        return typing.cast(typing.Optional["RdsInstanceV1Securitygroup"], jsii.get(self, "securitygroupInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RdsInstanceV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RdsInstanceV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional["RdsInstanceV1Volume"]:
        return typing.cast(typing.Optional["RdsInstanceV1Volume"], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityzone")
    def availabilityzone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityzone"))

    @availabilityzone.setter
    def availabilityzone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cafc85ffca7480712ebb66263b7e1e23991d2a6f078e6ae62728caa69d2d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityzone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbport")
    def dbport(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbport"))

    @dbport.setter
    def dbport(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846f516bdbfecf6365957e46aaa25f634d1bdcca7c620c82ca149e324285e445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbrtpd")
    def dbrtpd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbrtpd"))

    @dbrtpd.setter
    def dbrtpd(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ae700a41dcbc5a2893b34083c5f35cd90711eb1b629d7bc97c0bd7da540f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbrtpd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorref")
    def flavorref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorref"))

    @flavorref.setter
    def flavorref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0865a537776a06c655bdc2973c41e4c10736c23b3722fe0db7eea58aef91c4a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc92082ed82e598f2fe6a9679e6fd3636a0df4954c1077d3a7d01d6793b7172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abad893934d837cf0e2c21471a07674aa6cd21b3517318cd97213db453e2770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87553d1a17fb00e2495595e0b5a0fe4fd481b55109a188f23a770113f81ed7d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492ecf8363f955b00d23a88d64691169058919248f5e87ae28c9b356a30ab7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f2d26a878964faf4bfc1734c26159d63f08a30c48a35fad77453135c926e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Backupstrategy",
    jsii_struct_bases=[],
    name_mapping={"keepdays": "keepdays", "starttime": "starttime"},
)
class RdsInstanceV1Backupstrategy:
    def __init__(
        self,
        *,
        keepdays: typing.Optional[jsii.Number] = None,
        starttime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keepdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#keepdays RdsInstanceV1#keepdays}.
        :param starttime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#starttime RdsInstanceV1#starttime}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c32d505c6fb41426c42336493df852c1ae093f15bf812785801b2f23f3ca13)
            check_type(argname="argument keepdays", value=keepdays, expected_type=type_hints["keepdays"])
            check_type(argname="argument starttime", value=starttime, expected_type=type_hints["starttime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if keepdays is not None:
            self._values["keepdays"] = keepdays
        if starttime is not None:
            self._values["starttime"] = starttime

    @builtins.property
    def keepdays(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#keepdays RdsInstanceV1#keepdays}.'''
        result = self._values.get("keepdays")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starttime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#starttime RdsInstanceV1#starttime}.'''
        result = self._values.get("starttime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Backupstrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1BackupstrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1BackupstrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab4b00f92f087b3e84bfd5eb8aec464161b554202aa7dd316074c6b18d550a9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepdays")
    def reset_keepdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepdays", []))

    @jsii.member(jsii_name="resetStarttime")
    def reset_starttime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStarttime", []))

    @builtins.property
    @jsii.member(jsii_name="keepdaysInput")
    def keepdays_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="starttimeInput")
    def starttime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "starttimeInput"))

    @builtins.property
    @jsii.member(jsii_name="keepdays")
    def keepdays(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepdays"))

    @keepdays.setter
    def keepdays(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39110a37f8a2f8a2856ee5f6a55878367f394adee698ec34dbe836acb017137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="starttime")
    def starttime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "starttime"))

    @starttime.setter
    def starttime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060babdd444e303dc63891f0ae93a7763a96ade570239aeacd4045ab6d4e9329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "starttime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Backupstrategy]:
        return typing.cast(typing.Optional[RdsInstanceV1Backupstrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV1Backupstrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a640ce105ef935bca5dcc750f6b67c514113c303d0110ee4c95de8cc12710398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availabilityzone": "availabilityzone",
        "datastore": "datastore",
        "dbrtpd": "dbrtpd",
        "flavorref": "flavorref",
        "nics": "nics",
        "securitygroup": "securitygroup",
        "volume": "volume",
        "vpc": "vpc",
        "backupstrategy": "backupstrategy",
        "dbport": "dbport",
        "ha": "ha",
        "id": "id",
        "name": "name",
        "region": "region",
        "tag": "tag",
        "timeouts": "timeouts",
    },
)
class RdsInstanceV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availabilityzone: builtins.str,
        datastore: typing.Union["RdsInstanceV1Datastore", typing.Dict[builtins.str, typing.Any]],
        dbrtpd: builtins.str,
        flavorref: builtins.str,
        nics: typing.Union["RdsInstanceV1Nics", typing.Dict[builtins.str, typing.Any]],
        securitygroup: typing.Union["RdsInstanceV1Securitygroup", typing.Dict[builtins.str, typing.Any]],
        volume: typing.Union["RdsInstanceV1Volume", typing.Dict[builtins.str, typing.Any]],
        vpc: builtins.str,
        backupstrategy: typing.Optional[typing.Union[RdsInstanceV1Backupstrategy, typing.Dict[builtins.str, typing.Any]]] = None,
        dbport: typing.Optional[builtins.str] = None,
        ha: typing.Optional[typing.Union["RdsInstanceV1Ha", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RdsInstanceV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availabilityzone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#availabilityzone RdsInstanceV1#availabilityzone}.
        :param datastore: datastore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#datastore RdsInstanceV1#datastore}
        :param dbrtpd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#dbrtpd RdsInstanceV1#dbrtpd}.
        :param flavorref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#flavorref RdsInstanceV1#flavorref}.
        :param nics: nics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#nics RdsInstanceV1#nics}
        :param securitygroup: securitygroup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#securitygroup RdsInstanceV1#securitygroup}
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#volume RdsInstanceV1#volume}
        :param vpc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#vpc RdsInstanceV1#vpc}.
        :param backupstrategy: backupstrategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#backupstrategy RdsInstanceV1#backupstrategy}
        :param dbport: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#dbport RdsInstanceV1#dbport}.
        :param ha: ha block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#ha RdsInstanceV1#ha}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#name RdsInstanceV1#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#region RdsInstanceV1#region}.
        :param tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#tag RdsInstanceV1#tag}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#timeouts RdsInstanceV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(datastore, dict):
            datastore = RdsInstanceV1Datastore(**datastore)
        if isinstance(nics, dict):
            nics = RdsInstanceV1Nics(**nics)
        if isinstance(securitygroup, dict):
            securitygroup = RdsInstanceV1Securitygroup(**securitygroup)
        if isinstance(volume, dict):
            volume = RdsInstanceV1Volume(**volume)
        if isinstance(backupstrategy, dict):
            backupstrategy = RdsInstanceV1Backupstrategy(**backupstrategy)
        if isinstance(ha, dict):
            ha = RdsInstanceV1Ha(**ha)
        if isinstance(timeouts, dict):
            timeouts = RdsInstanceV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05085112b58997bf742f1c626f4649163a5017eeef35a55f728c9c1ab2b3c726)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availabilityzone", value=availabilityzone, expected_type=type_hints["availabilityzone"])
            check_type(argname="argument datastore", value=datastore, expected_type=type_hints["datastore"])
            check_type(argname="argument dbrtpd", value=dbrtpd, expected_type=type_hints["dbrtpd"])
            check_type(argname="argument flavorref", value=flavorref, expected_type=type_hints["flavorref"])
            check_type(argname="argument nics", value=nics, expected_type=type_hints["nics"])
            check_type(argname="argument securitygroup", value=securitygroup, expected_type=type_hints["securitygroup"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument backupstrategy", value=backupstrategy, expected_type=type_hints["backupstrategy"])
            check_type(argname="argument dbport", value=dbport, expected_type=type_hints["dbport"])
            check_type(argname="argument ha", value=ha, expected_type=type_hints["ha"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availabilityzone": availabilityzone,
            "datastore": datastore,
            "dbrtpd": dbrtpd,
            "flavorref": flavorref,
            "nics": nics,
            "securitygroup": securitygroup,
            "volume": volume,
            "vpc": vpc,
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
        if backupstrategy is not None:
            self._values["backupstrategy"] = backupstrategy
        if dbport is not None:
            self._values["dbport"] = dbport
        if ha is not None:
            self._values["ha"] = ha
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region
        if tag is not None:
            self._values["tag"] = tag
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
    def availabilityzone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#availabilityzone RdsInstanceV1#availabilityzone}.'''
        result = self._values.get("availabilityzone")
        assert result is not None, "Required property 'availabilityzone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore(self) -> "RdsInstanceV1Datastore":
        '''datastore block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#datastore RdsInstanceV1#datastore}
        '''
        result = self._values.get("datastore")
        assert result is not None, "Required property 'datastore' is missing"
        return typing.cast("RdsInstanceV1Datastore", result)

    @builtins.property
    def dbrtpd(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#dbrtpd RdsInstanceV1#dbrtpd}.'''
        result = self._values.get("dbrtpd")
        assert result is not None, "Required property 'dbrtpd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flavorref(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#flavorref RdsInstanceV1#flavorref}.'''
        result = self._values.get("flavorref")
        assert result is not None, "Required property 'flavorref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nics(self) -> "RdsInstanceV1Nics":
        '''nics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#nics RdsInstanceV1#nics}
        '''
        result = self._values.get("nics")
        assert result is not None, "Required property 'nics' is missing"
        return typing.cast("RdsInstanceV1Nics", result)

    @builtins.property
    def securitygroup(self) -> "RdsInstanceV1Securitygroup":
        '''securitygroup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#securitygroup RdsInstanceV1#securitygroup}
        '''
        result = self._values.get("securitygroup")
        assert result is not None, "Required property 'securitygroup' is missing"
        return typing.cast("RdsInstanceV1Securitygroup", result)

    @builtins.property
    def volume(self) -> "RdsInstanceV1Volume":
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#volume RdsInstanceV1#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast("RdsInstanceV1Volume", result)

    @builtins.property
    def vpc(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#vpc RdsInstanceV1#vpc}.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backupstrategy(self) -> typing.Optional[RdsInstanceV1Backupstrategy]:
        '''backupstrategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#backupstrategy RdsInstanceV1#backupstrategy}
        '''
        result = self._values.get("backupstrategy")
        return typing.cast(typing.Optional[RdsInstanceV1Backupstrategy], result)

    @builtins.property
    def dbport(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#dbport RdsInstanceV1#dbport}.'''
        result = self._values.get("dbport")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha(self) -> typing.Optional["RdsInstanceV1Ha"]:
        '''ha block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#ha RdsInstanceV1#ha}
        '''
        result = self._values.get("ha")
        return typing.cast(typing.Optional["RdsInstanceV1Ha"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#id RdsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#name RdsInstanceV1#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#region RdsInstanceV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#tag RdsInstanceV1#tag}.'''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RdsInstanceV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#timeouts RdsInstanceV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RdsInstanceV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Datastore",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "version": "version"},
)
class RdsInstanceV1Datastore:
    def __init__(self, *, type: builtins.str, version: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#type RdsInstanceV1#type}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#version RdsInstanceV1#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee7fc71130c8a7c078adb32308a261b1f08a16d0733cf65d83ab48b66459185)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "version": version,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#type RdsInstanceV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#version RdsInstanceV1#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Datastore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1DatastoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1DatastoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__686bf4fdb4eec3eec0246603afac65c88e39f4a1c3a661bcbdf60da10fa8901d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__08c990c04ab538201f9497bf97e2acdaa3ec23e4d35ca156b6c9ec5adb9afa39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8224f243d9ea0e10e59b587c04c1f68170baa6ed87cf424d5cbd0272cd804e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Datastore]:
        return typing.cast(typing.Optional[RdsInstanceV1Datastore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Datastore]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32af91af00d22a7b1d6f9507be735a01f4222b9d3c91c0cf569d4a7ce8666f65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Ha",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable", "replicationmode": "replicationmode"},
)
class RdsInstanceV1Ha:
    def __init__(
        self,
        *,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replicationmode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#enable RdsInstanceV1#enable}.
        :param replicationmode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#replicationmode RdsInstanceV1#replicationmode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a576f2a42ed5c308bd5a3aa15e8fbb7d10ad9d69a6bf3ca9c72f8fa97f01618)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument replicationmode", value=replicationmode, expected_type=type_hints["replicationmode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable is not None:
            self._values["enable"] = enable
        if replicationmode is not None:
            self._values["replicationmode"] = replicationmode

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#enable RdsInstanceV1#enable}.'''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replicationmode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#replicationmode RdsInstanceV1#replicationmode}.'''
        result = self._values.get("replicationmode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Ha(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1HaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1HaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__123b78ae559b9c69282912823d5b72f4d514b374a5eb6c4ac46d91c9d1080c71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetReplicationmode")
    def reset_replicationmode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationmode", []))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationmodeInput")
    def replicationmode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationmodeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3fbe481c2e11e8b987d0e879b7935a8ff9a31e8940e68c6af3f8d5db41d76e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationmode")
    def replicationmode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationmode"))

    @replicationmode.setter
    def replicationmode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b93d8ed5e8f63f1c6e60ea989bfcfaf43e9096f7ef60f9478e299167d185de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationmode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Ha]:
        return typing.cast(typing.Optional[RdsInstanceV1Ha], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Ha]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a0e4150666c727aa4cce0189b7f3db5fe15f23510a63982674086866a114cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Nics",
    jsii_struct_bases=[],
    name_mapping={"subnetid": "subnetid"},
)
class RdsInstanceV1Nics:
    def __init__(self, *, subnetid: builtins.str) -> None:
        '''
        :param subnetid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#subnetid RdsInstanceV1#subnetid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ece4f4ccddb42550abf0749fd96c84646b2e1982dceb039d560599d6b2a589d)
            check_type(argname="argument subnetid", value=subnetid, expected_type=type_hints["subnetid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnetid": subnetid,
        }

    @builtins.property
    def subnetid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#subnetid RdsInstanceV1#subnetid}.'''
        result = self._values.get("subnetid")
        assert result is not None, "Required property 'subnetid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Nics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1NicsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1NicsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b85efcb9a7778f6a21d249bcf476d48e6cd32b54baab963bdbe68f60a18c601)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetidInput")
    def subnetid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetidInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetid")
    def subnetid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetid"))

    @subnetid.setter
    def subnetid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f3a8214789a42340b840a68928ef7a54cf2b72eed63c630619cb7348070c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Nics]:
        return typing.cast(typing.Optional[RdsInstanceV1Nics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Nics]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bc0c39362eeb5c89739846faeba89ce6913e10d4c3ba145e6f043de57fdc0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Securitygroup",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class RdsInstanceV1Securitygroup:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#id RdsInstanceV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca01ec32aa82b9c98d426a62ef64925fcf31fcd9d48795f2e390fae275eccf6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#id RdsInstanceV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Securitygroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1SecuritygroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1SecuritygroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4c561673ef3fbddbc463a191e1f5380433aeccaa50e6107a6e375d7b4cfa61e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43aafe35aef98de2fb2fb2da6b8b7b112b014dabe55b8b49a4afaeda1d8a2d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Securitygroup]:
        return typing.cast(typing.Optional[RdsInstanceV1Securitygroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RdsInstanceV1Securitygroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2cf176362557c354bee16ae9d3d778408a569218c8802e1b97832a15d9718f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class RdsInstanceV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#create RdsInstanceV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#delete RdsInstanceV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba59a59112b91452c9b2460981ff7da9b6a7e5b5fc01d613c695474697ed0966)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#create RdsInstanceV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#delete RdsInstanceV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__555f8408651935b3c0651114f378142cbbb93cff2511ea45b70bc0faf632b932)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4641a5b3dc2741c92fe2b5f39558bd150430e083bfa7feaf3d0f495ff66811cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0802f991bf8a3de0b8d84a3ac0f6185aa546ddf9e17284f0575b9e4fda334a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e4cfd129aabf2f9f37e912e9d28d00ccdd1fed27896e18bb94b6ced1b87e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1Volume",
    jsii_struct_bases=[],
    name_mapping={"size": "size", "type": "type"},
)
class RdsInstanceV1Volume:
    def __init__(self, *, size: jsii.Number, type: builtins.str) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#size RdsInstanceV1#size}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#type RdsInstanceV1#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36097fb2c7bf7aa24328508efbcc6959d7a36da58c2126fbd2142af86537b7ab)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "type": type,
        }

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#size RdsInstanceV1#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/rds_instance_v1#type RdsInstanceV1#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsInstanceV1Volume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsInstanceV1VolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.rdsInstanceV1.RdsInstanceV1VolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7651ca53d0c396fc9aee45e498d8995bddfcffe05c206495a5325538fe79b5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1413c4892aa7fdca2d02dccb98b63a956df9311ba7049fa345af6ce1bcb5725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc78ea21d702b67054e37420c2053b918dc4879dcd887f77874b8a949eabab90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RdsInstanceV1Volume]:
        return typing.cast(typing.Optional[RdsInstanceV1Volume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RdsInstanceV1Volume]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c5421a34e7a5a126d6eb80a041bcdc78a5cb2e156a57c0d86ca3e2a4db9f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RdsInstanceV1",
    "RdsInstanceV1Backupstrategy",
    "RdsInstanceV1BackupstrategyOutputReference",
    "RdsInstanceV1Config",
    "RdsInstanceV1Datastore",
    "RdsInstanceV1DatastoreOutputReference",
    "RdsInstanceV1Ha",
    "RdsInstanceV1HaOutputReference",
    "RdsInstanceV1Nics",
    "RdsInstanceV1NicsOutputReference",
    "RdsInstanceV1Securitygroup",
    "RdsInstanceV1SecuritygroupOutputReference",
    "RdsInstanceV1Timeouts",
    "RdsInstanceV1TimeoutsOutputReference",
    "RdsInstanceV1Volume",
    "RdsInstanceV1VolumeOutputReference",
]

publication.publish()

def _typecheckingstub__4311046b325f0c79281784863e5363866ca88990bd861a1fe1b620d426d7fcde(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availabilityzone: builtins.str,
    datastore: typing.Union[RdsInstanceV1Datastore, typing.Dict[builtins.str, typing.Any]],
    dbrtpd: builtins.str,
    flavorref: builtins.str,
    nics: typing.Union[RdsInstanceV1Nics, typing.Dict[builtins.str, typing.Any]],
    securitygroup: typing.Union[RdsInstanceV1Securitygroup, typing.Dict[builtins.str, typing.Any]],
    volume: typing.Union[RdsInstanceV1Volume, typing.Dict[builtins.str, typing.Any]],
    vpc: builtins.str,
    backupstrategy: typing.Optional[typing.Union[RdsInstanceV1Backupstrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    dbport: typing.Optional[builtins.str] = None,
    ha: typing.Optional[typing.Union[RdsInstanceV1Ha, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RdsInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ea36474560124a1f7e71a79a4b17af0fe133e3b4847aec85319aacbed78e594e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cafc85ffca7480712ebb66263b7e1e23991d2a6f078e6ae62728caa69d2d17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846f516bdbfecf6365957e46aaa25f634d1bdcca7c620c82ca149e324285e445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ae700a41dcbc5a2893b34083c5f35cd90711eb1b629d7bc97c0bd7da540f3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0865a537776a06c655bdc2973c41e4c10736c23b3722fe0db7eea58aef91c4a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc92082ed82e598f2fe6a9679e6fd3636a0df4954c1077d3a7d01d6793b7172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abad893934d837cf0e2c21471a07674aa6cd21b3517318cd97213db453e2770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87553d1a17fb00e2495595e0b5a0fe4fd481b55109a188f23a770113f81ed7d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492ecf8363f955b00d23a88d64691169058919248f5e87ae28c9b356a30ab7de(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f2d26a878964faf4bfc1734c26159d63f08a30c48a35fad77453135c926e34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c32d505c6fb41426c42336493df852c1ae093f15bf812785801b2f23f3ca13(
    *,
    keepdays: typing.Optional[jsii.Number] = None,
    starttime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4b00f92f087b3e84bfd5eb8aec464161b554202aa7dd316074c6b18d550a9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39110a37f8a2f8a2856ee5f6a55878367f394adee698ec34dbe836acb017137(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060babdd444e303dc63891f0ae93a7763a96ade570239aeacd4045ab6d4e9329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a640ce105ef935bca5dcc750f6b67c514113c303d0110ee4c95de8cc12710398(
    value: typing.Optional[RdsInstanceV1Backupstrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05085112b58997bf742f1c626f4649163a5017eeef35a55f728c9c1ab2b3c726(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availabilityzone: builtins.str,
    datastore: typing.Union[RdsInstanceV1Datastore, typing.Dict[builtins.str, typing.Any]],
    dbrtpd: builtins.str,
    flavorref: builtins.str,
    nics: typing.Union[RdsInstanceV1Nics, typing.Dict[builtins.str, typing.Any]],
    securitygroup: typing.Union[RdsInstanceV1Securitygroup, typing.Dict[builtins.str, typing.Any]],
    volume: typing.Union[RdsInstanceV1Volume, typing.Dict[builtins.str, typing.Any]],
    vpc: builtins.str,
    backupstrategy: typing.Optional[typing.Union[RdsInstanceV1Backupstrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    dbport: typing.Optional[builtins.str] = None,
    ha: typing.Optional[typing.Union[RdsInstanceV1Ha, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tag: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RdsInstanceV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee7fc71130c8a7c078adb32308a261b1f08a16d0733cf65d83ab48b66459185(
    *,
    type: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686bf4fdb4eec3eec0246603afac65c88e39f4a1c3a661bcbdf60da10fa8901d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c990c04ab538201f9497bf97e2acdaa3ec23e4d35ca156b6c9ec5adb9afa39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8224f243d9ea0e10e59b587c04c1f68170baa6ed87cf424d5cbd0272cd804e99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32af91af00d22a7b1d6f9507be735a01f4222b9d3c91c0cf569d4a7ce8666f65(
    value: typing.Optional[RdsInstanceV1Datastore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a576f2a42ed5c308bd5a3aa15e8fbb7d10ad9d69a6bf3ca9c72f8fa97f01618(
    *,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replicationmode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123b78ae559b9c69282912823d5b72f4d514b374a5eb6c4ac46d91c9d1080c71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbe481c2e11e8b987d0e879b7935a8ff9a31e8940e68c6af3f8d5db41d76e1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b93d8ed5e8f63f1c6e60ea989bfcfaf43e9096f7ef60f9478e299167d185de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a0e4150666c727aa4cce0189b7f3db5fe15f23510a63982674086866a114cc(
    value: typing.Optional[RdsInstanceV1Ha],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ece4f4ccddb42550abf0749fd96c84646b2e1982dceb039d560599d6b2a589d(
    *,
    subnetid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b85efcb9a7778f6a21d249bcf476d48e6cd32b54baab963bdbe68f60a18c601(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f3a8214789a42340b840a68928ef7a54cf2b72eed63c630619cb7348070c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bc0c39362eeb5c89739846faeba89ce6913e10d4c3ba145e6f043de57fdc0f(
    value: typing.Optional[RdsInstanceV1Nics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca01ec32aa82b9c98d426a62ef64925fcf31fcd9d48795f2e390fae275eccf6(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c561673ef3fbddbc463a191e1f5380433aeccaa50e6107a6e375d7b4cfa61e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43aafe35aef98de2fb2fb2da6b8b7b112b014dabe55b8b49a4afaeda1d8a2d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2cf176362557c354bee16ae9d3d778408a569218c8802e1b97832a15d9718f(
    value: typing.Optional[RdsInstanceV1Securitygroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba59a59112b91452c9b2460981ff7da9b6a7e5b5fc01d613c695474697ed0966(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555f8408651935b3c0651114f378142cbbb93cff2511ea45b70bc0faf632b932(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4641a5b3dc2741c92fe2b5f39558bd150430e083bfa7feaf3d0f495ff66811cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0802f991bf8a3de0b8d84a3ac0f6185aa546ddf9e17284f0575b9e4fda334a4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e4cfd129aabf2f9f37e912e9d28d00ccdd1fed27896e18bb94b6ced1b87e34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RdsInstanceV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36097fb2c7bf7aa24328508efbcc6959d7a36da58c2126fbd2142af86537b7ab(
    *,
    size: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7651ca53d0c396fc9aee45e498d8995bddfcffe05c206495a5325538fe79b5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1413c4892aa7fdca2d02dccb98b63a956df9311ba7049fa345af6ce1bcb5725(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc78ea21d702b67054e37420c2053b918dc4879dcd887f77874b8a949eabab90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c5421a34e7a5a126d6eb80a041bcdc78a5cb2e156a57c0d86ca3e2a4db9f91(
    value: typing.Optional[RdsInstanceV1Volume],
) -> None:
    """Type checking stubs"""
    pass
