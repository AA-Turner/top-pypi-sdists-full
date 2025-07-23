r'''
# `google_redis_cluster_user_created_connections`

Refer to the Terraform Registry for docs: [`google_redis_cluster_user_created_connections`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections).
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


class RedisClusterUserCreatedConnections(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnections",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections google_redis_cluster_user_created_connections}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        region: builtins.str,
        cluster_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterUserCreatedConnectionsClusterEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["RedisClusterUserCreatedConnectionsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections google_redis_cluster_user_created_connections} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the Redis cluster these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#name RedisClusterUserCreatedConnections#name}
        :param region: The name of the region of the Redis cluster these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#region RedisClusterUserCreatedConnections#region}
        :param cluster_endpoints: cluster_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#cluster_endpoints RedisClusterUserCreatedConnections#cluster_endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#id RedisClusterUserCreatedConnections#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#project RedisClusterUserCreatedConnections#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#timeouts RedisClusterUserCreatedConnections#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc10f849dfba64ef58a5f9b9d85404d5a7c5e3b2ad2ff7ea6fde761c8b6ac6a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RedisClusterUserCreatedConnectionsConfig(
            name=name,
            region=region,
            cluster_endpoints=cluster_endpoints,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a RedisClusterUserCreatedConnections resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RedisClusterUserCreatedConnections to import.
        :param import_from_id: The id of the existing RedisClusterUserCreatedConnections that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RedisClusterUserCreatedConnections to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031a56bd32537ca4c794861dc6e11d1eda7eaa321a4759e80bc0004b5f040042)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClusterEndpoints")
    def put_cluster_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterUserCreatedConnectionsClusterEndpoints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb30bc4bb0c1f0f694437555cc102458b0d54015038c5097048c6568ffad04dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClusterEndpoints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#create RedisClusterUserCreatedConnections#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#delete RedisClusterUserCreatedConnections#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#update RedisClusterUserCreatedConnections#update}.
        '''
        value = RedisClusterUserCreatedConnectionsTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClusterEndpoints")
    def reset_cluster_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterEndpoints", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="clusterEndpoints")
    def cluster_endpoints(
        self,
    ) -> "RedisClusterUserCreatedConnectionsClusterEndpointsList":
        return typing.cast("RedisClusterUserCreatedConnectionsClusterEndpointsList", jsii.get(self, "clusterEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RedisClusterUserCreatedConnectionsTimeoutsOutputReference":
        return typing.cast("RedisClusterUserCreatedConnectionsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpointsInput")
    def cluster_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterUserCreatedConnectionsClusterEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterUserCreatedConnectionsClusterEndpoints"]]], jsii.get(self, "clusterEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisClusterUserCreatedConnectionsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisClusterUserCreatedConnectionsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdad996925818f32f18c8df6722fb2c4c2f41f5f27f9e99eea2d99593a73d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42a32d7bd74203da1493f8743596d4b9721feef7d4b88590e54867d10479f28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc211b233d01c846ce3f091d6adc5a5cca58362d974b89aec451929ae2e22fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9956d67b1837d42682195dcf84ef57f70e19ba8ac238caa87eefc0c7eee881d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpoints",
    jsii_struct_bases=[],
    name_mapping={"connections": "connections"},
)
class RedisClusterUserCreatedConnectionsClusterEndpoints:
    def __init__(
        self,
        *,
        connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterUserCreatedConnectionsClusterEndpointsConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connections: connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#connections RedisClusterUserCreatedConnections#connections}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71479862d461b4fa1b51d582654924b4c6553f52eea4ea71a656e4ec25ad031d)
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connections is not None:
            self._values["connections"] = connections

    @builtins.property
    def connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterUserCreatedConnectionsClusterEndpointsConnections"]]]:
        '''connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#connections RedisClusterUserCreatedConnections#connections}
        '''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterUserCreatedConnectionsClusterEndpointsConnections"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterUserCreatedConnectionsClusterEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsConnections",
    jsii_struct_bases=[],
    name_mapping={"psc_connection": "pscConnection"},
)
class RedisClusterUserCreatedConnectionsClusterEndpointsConnections:
    def __init__(
        self,
        *,
        psc_connection: typing.Optional[typing.Union["RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param psc_connection: psc_connection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#psc_connection RedisClusterUserCreatedConnections#psc_connection}
        '''
        if isinstance(psc_connection, dict):
            psc_connection = RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection(**psc_connection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7b8d63825e3dce7500e1e7208421c7530927b937a36bcf7f72b4eedaa35ed0)
            check_type(argname="argument psc_connection", value=psc_connection, expected_type=type_hints["psc_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if psc_connection is not None:
            self._values["psc_connection"] = psc_connection

    @builtins.property
    def psc_connection(
        self,
    ) -> typing.Optional["RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection"]:
        '''psc_connection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#psc_connection RedisClusterUserCreatedConnections#psc_connection}
        '''
        result = self._values.get("psc_connection")
        return typing.cast(typing.Optional["RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterUserCreatedConnectionsClusterEndpointsConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90e2fbe7ab4fded1a7350df081b5cd67672103bd63ac1807fd4c714795ea8a2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba670dd54fc624d45f22bbfff3f4dd3da9391ac2e4286ceacb423241e6999f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4f405676bef2c039a8d7750083c7071b7fd4e55aa03e80e5868f534239caba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e68124b2df0139dad2f603cad36c190613375ee743e11952979bbe5213600d76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382f85b5b6614442c1cc457747143de70f20a442f5bad7565336a00fab3aae92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bf3a4261812055dbffec04b8155ee6493c0715a5c893d1252fe75a614c3f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5320df97b9f0ee7b9c7420c22c849f40a208b7dba4824e3703912c727a0fa8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPscConnection")
    def put_psc_connection(
        self,
        *,
        address: builtins.str,
        forwarding_rule: builtins.str,
        network: builtins.str,
        psc_connection_id: builtins.str,
        service_attachment: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The IP allocated on the consumer network for the PSC forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#address RedisClusterUserCreatedConnections#address}
        :param forwarding_rule: The URI of the consumer side forwarding rule. Format: projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#forwarding_rule RedisClusterUserCreatedConnections#forwarding_rule}
        :param network: The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#network RedisClusterUserCreatedConnections#network}
        :param psc_connection_id: The PSC connection id of the forwarding rule connected to the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#psc_connection_id RedisClusterUserCreatedConnections#psc_connection_id}
        :param service_attachment: The service attachment which is the target of the PSC connection, in the form of projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#service_attachment RedisClusterUserCreatedConnections#service_attachment}
        :param project_id: The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#project_id RedisClusterUserCreatedConnections#project_id}
        '''
        value = RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection(
            address=address,
            forwarding_rule=forwarding_rule,
            network=network,
            psc_connection_id=psc_connection_id,
            service_attachment=service_attachment,
            project_id=project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putPscConnection", [value]))

    @jsii.member(jsii_name="resetPscConnection")
    def reset_psc_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConnection", []))

    @builtins.property
    @jsii.member(jsii_name="pscConnection")
    def psc_connection(
        self,
    ) -> "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnectionOutputReference":
        return typing.cast("RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnectionOutputReference", jsii.get(self, "pscConnection"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionInput")
    def psc_connection_input(
        self,
    ) -> typing.Optional["RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection"]:
        return typing.cast(typing.Optional["RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection"], jsii.get(self, "pscConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpointsConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpointsConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb62ccfda05da8c48f4759482e7a47fa33f18268cb3eb7fd15b47f5475a8050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "forwarding_rule": "forwardingRule",
        "network": "network",
        "psc_connection_id": "pscConnectionId",
        "service_attachment": "serviceAttachment",
        "project_id": "projectId",
    },
)
class RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection:
    def __init__(
        self,
        *,
        address: builtins.str,
        forwarding_rule: builtins.str,
        network: builtins.str,
        psc_connection_id: builtins.str,
        service_attachment: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The IP allocated on the consumer network for the PSC forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#address RedisClusterUserCreatedConnections#address}
        :param forwarding_rule: The URI of the consumer side forwarding rule. Format: projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#forwarding_rule RedisClusterUserCreatedConnections#forwarding_rule}
        :param network: The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#network RedisClusterUserCreatedConnections#network}
        :param psc_connection_id: The PSC connection id of the forwarding rule connected to the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#psc_connection_id RedisClusterUserCreatedConnections#psc_connection_id}
        :param service_attachment: The service attachment which is the target of the PSC connection, in the form of projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#service_attachment RedisClusterUserCreatedConnections#service_attachment}
        :param project_id: The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#project_id RedisClusterUserCreatedConnections#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72e25def97b8dd9575222296b736c81e5dc2e7cab18011da6dd56e2de56150a)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument forwarding_rule", value=forwarding_rule, expected_type=type_hints["forwarding_rule"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument psc_connection_id", value=psc_connection_id, expected_type=type_hints["psc_connection_id"])
            check_type(argname="argument service_attachment", value=service_attachment, expected_type=type_hints["service_attachment"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "forwarding_rule": forwarding_rule,
            "network": network,
            "psc_connection_id": psc_connection_id,
            "service_attachment": service_attachment,
        }
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def address(self) -> builtins.str:
        '''The IP allocated on the consumer network for the PSC forwarding rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#address RedisClusterUserCreatedConnections#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forwarding_rule(self) -> builtins.str:
        '''The URI of the consumer side forwarding rule. Format: projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#forwarding_rule RedisClusterUserCreatedConnections#forwarding_rule}
        '''
        result = self._values.get("forwarding_rule")
        assert result is not None, "Required property 'forwarding_rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#network RedisClusterUserCreatedConnections#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def psc_connection_id(self) -> builtins.str:
        '''The PSC connection id of the forwarding rule connected to the service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#psc_connection_id RedisClusterUserCreatedConnections#psc_connection_id}
        '''
        result = self._values.get("psc_connection_id")
        assert result is not None, "Required property 'psc_connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_attachment(self) -> builtins.str:
        '''The service attachment which is the target of the PSC connection, in the form of projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#service_attachment RedisClusterUserCreatedConnections#service_attachment}
        '''
        result = self._values.get("service_attachment")
        assert result is not None, "Required property 'service_attachment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#project_id RedisClusterUserCreatedConnections#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d716c34e8f253cc3c30676b162c1c3d0b3382ea9e1da8a9fadfdb2e65c5641b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionType"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionStatus")
    def psc_connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardingRuleInput")
    def forwarding_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionIdInput")
    def psc_connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pscConnectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachmentInput")
    def service_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c63f7eb6a7fe44c45b83900699cdecac06e2eab4a1e1ed05f79ae32bc240e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @forwarding_rule.setter
    def forwarding_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64627f630d83f33a6f6b8875c9d576c12934f4bbd7cffb537bf761912c895393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819045778cd2754307f1377d3381b74aaf9526cda3cc36092c5792b98f4d6c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b424f669267940603706c7d4f456532acf3152e2d3885bf9149d2fa32784889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @psc_connection_id.setter
    def psc_connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a686003bfa024c13b6651ed4407c3370fd82be06d4e7ed9329867f14d074b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscConnectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @service_attachment.setter
    def service_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1efeeae47fdb5392b6d9f239b3c7cd8eae8364605b02ebbe50ffd0947d2ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection]:
        return typing.cast(typing.Optional[RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827a575459270059fdf49c51f2555c4896f244dbfb2989e06addb7d10a5ccd08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterUserCreatedConnectionsClusterEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__118c4ef20b303bab9e6a6e17450340de6d1ff076ba2e321b210f92342faed273)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterUserCreatedConnectionsClusterEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fc186e7d5f0dd6ad1b1b0eb8b53699a22f7555c03a996443c1659e74f27931)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterUserCreatedConnectionsClusterEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5d5939969847e146106d76602c028cffd7d1b22a88fdc3e2bd5cbb66eb8c57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc220922b93561f8dec0f874ab36177077c9b52735ef36e868d211ac5e0507b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53af51a225e1874823f8171c1c3f30dae41117db770a5de887d47f62504d0271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81dd3fd795d53005daab9b20a732d021277f9bf96dab0ad9451441031861c8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterUserCreatedConnectionsClusterEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsClusterEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d4a73808d8448efac702f24e54bba00526dc3ab49a2996b7934bb5c7152bf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnections")
    def put_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpointsConnections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df08c146a77b586b9384ddbed0a5816cc214f0f27efa4e014b88479a95997a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnections", [value]))

    @jsii.member(jsii_name="resetConnections")
    def reset_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnections", []))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(
        self,
    ) -> RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsList:
        return typing.cast(RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsList, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="connectionsInput")
    def connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]], jsii.get(self, "connectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cba3e7043886e9ae41ee353f1db7f043e1bdd82131bc7518413496e6c8fefd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsConfig",
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
        "region": "region",
        "cluster_endpoints": "clusterEndpoints",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class RedisClusterUserCreatedConnectionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        region: builtins.str,
        cluster_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["RedisClusterUserCreatedConnectionsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the Redis cluster these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#name RedisClusterUserCreatedConnections#name}
        :param region: The name of the region of the Redis cluster these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#region RedisClusterUserCreatedConnections#region}
        :param cluster_endpoints: cluster_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#cluster_endpoints RedisClusterUserCreatedConnections#cluster_endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#id RedisClusterUserCreatedConnections#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#project RedisClusterUserCreatedConnections#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#timeouts RedisClusterUserCreatedConnections#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = RedisClusterUserCreatedConnectionsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00b1e48e3c68ecd87bcd37b41d87b6c85e13c02d791fe5c919dbc3fc5ea8892)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cluster_endpoints", value=cluster_endpoints, expected_type=type_hints["cluster_endpoints"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "region": region,
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
        if cluster_endpoints is not None:
            self._values["cluster_endpoints"] = cluster_endpoints
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
        '''The name of the Redis cluster these endpoints should be added to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#name RedisClusterUserCreatedConnections#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''The name of the region of the Redis cluster these endpoints should be added to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#region RedisClusterUserCreatedConnections#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpoints]]]:
        '''cluster_endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#cluster_endpoints RedisClusterUserCreatedConnections#cluster_endpoints}
        '''
        result = self._values.get("cluster_endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpoints]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#id RedisClusterUserCreatedConnections#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#project RedisClusterUserCreatedConnections#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RedisClusterUserCreatedConnectionsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#timeouts RedisClusterUserCreatedConnections#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RedisClusterUserCreatedConnectionsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterUserCreatedConnectionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RedisClusterUserCreatedConnectionsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#create RedisClusterUserCreatedConnections#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#delete RedisClusterUserCreatedConnections#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#update RedisClusterUserCreatedConnections#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571f7c35112b7f5a19d9371fc8e35454ec35c977f7b1e5aa472ebcaf4e25e5e7)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#create RedisClusterUserCreatedConnections#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#delete RedisClusterUserCreatedConnections#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster_user_created_connections#update RedisClusterUserCreatedConnections#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterUserCreatedConnectionsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterUserCreatedConnectionsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisClusterUserCreatedConnections.RedisClusterUserCreatedConnectionsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__689affe7ddff3600478e484f45250d4b243ef21eae5ffa2e3703970aef123533)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8079c34451baf5c62b113c281018ce47c8bca819000b37e1dd05253c30d90569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d084388266cba83aeacb191511b896fc361b1e5f48ab9b672ebe865cca5bcaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ac004f5e989ab333255298017dddf32051e80b838e56abf467cdb24025d9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61272d93a12c6d72b911c0f972e0bfda26f5d93da10f75cabe5b040958d7a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RedisClusterUserCreatedConnections",
    "RedisClusterUserCreatedConnectionsClusterEndpoints",
    "RedisClusterUserCreatedConnectionsClusterEndpointsConnections",
    "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsList",
    "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsOutputReference",
    "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection",
    "RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnectionOutputReference",
    "RedisClusterUserCreatedConnectionsClusterEndpointsList",
    "RedisClusterUserCreatedConnectionsClusterEndpointsOutputReference",
    "RedisClusterUserCreatedConnectionsConfig",
    "RedisClusterUserCreatedConnectionsTimeouts",
    "RedisClusterUserCreatedConnectionsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dc10f849dfba64ef58a5f9b9d85404d5a7c5e3b2ad2ff7ea6fde761c8b6ac6a2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    region: builtins.str,
    cluster_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[RedisClusterUserCreatedConnectionsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__031a56bd32537ca4c794861dc6e11d1eda7eaa321a4759e80bc0004b5f040042(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb30bc4bb0c1f0f694437555cc102458b0d54015038c5097048c6568ffad04dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdad996925818f32f18c8df6722fb2c4c2f41f5f27f9e99eea2d99593a73d13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42a32d7bd74203da1493f8743596d4b9721feef7d4b88590e54867d10479f28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc211b233d01c846ce3f091d6adc5a5cca58362d974b89aec451929ae2e22fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9956d67b1837d42682195dcf84ef57f70e19ba8ac238caa87eefc0c7eee881d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71479862d461b4fa1b51d582654924b4c6553f52eea4ea71a656e4ec25ad031d(
    *,
    connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpointsConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7b8d63825e3dce7500e1e7208421c7530927b937a36bcf7f72b4eedaa35ed0(
    *,
    psc_connection: typing.Optional[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e2fbe7ab4fded1a7350df081b5cd67672103bd63ac1807fd4c714795ea8a2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba670dd54fc624d45f22bbfff3f4dd3da9391ac2e4286ceacb423241e6999f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4f405676bef2c039a8d7750083c7071b7fd4e55aa03e80e5868f534239caba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68124b2df0139dad2f603cad36c190613375ee743e11952979bbe5213600d76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382f85b5b6614442c1cc457747143de70f20a442f5bad7565336a00fab3aae92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bf3a4261812055dbffec04b8155ee6493c0715a5c893d1252fe75a614c3f6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpointsConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5320df97b9f0ee7b9c7420c22c849f40a208b7dba4824e3703912c727a0fa8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb62ccfda05da8c48f4759482e7a47fa33f18268cb3eb7fd15b47f5475a8050(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpointsConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72e25def97b8dd9575222296b736c81e5dc2e7cab18011da6dd56e2de56150a(
    *,
    address: builtins.str,
    forwarding_rule: builtins.str,
    network: builtins.str,
    psc_connection_id: builtins.str,
    service_attachment: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d716c34e8f253cc3c30676b162c1c3d0b3382ea9e1da8a9fadfdb2e65c5641b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c63f7eb6a7fe44c45b83900699cdecac06e2eab4a1e1ed05f79ae32bc240e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64627f630d83f33a6f6b8875c9d576c12934f4bbd7cffb537bf761912c895393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819045778cd2754307f1377d3381b74aaf9526cda3cc36092c5792b98f4d6c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b424f669267940603706c7d4f456532acf3152e2d3885bf9149d2fa32784889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a686003bfa024c13b6651ed4407c3370fd82be06d4e7ed9329867f14d074b97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1efeeae47fdb5392b6d9f239b3c7cd8eae8364605b02ebbe50ffd0947d2ffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827a575459270059fdf49c51f2555c4896f244dbfb2989e06addb7d10a5ccd08(
    value: typing.Optional[RedisClusterUserCreatedConnectionsClusterEndpointsConnectionsPscConnection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118c4ef20b303bab9e6a6e17450340de6d1ff076ba2e321b210f92342faed273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fc186e7d5f0dd6ad1b1b0eb8b53699a22f7555c03a996443c1659e74f27931(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5d5939969847e146106d76602c028cffd7d1b22a88fdc3e2bd5cbb66eb8c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc220922b93561f8dec0f874ab36177077c9b52735ef36e868d211ac5e0507b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53af51a225e1874823f8171c1c3f30dae41117db770a5de887d47f62504d0271(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dd3fd795d53005daab9b20a732d021277f9bf96dab0ad9451441031861c8d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterUserCreatedConnectionsClusterEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d4a73808d8448efac702f24e54bba00526dc3ab49a2996b7934bb5c7152bf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df08c146a77b586b9384ddbed0a5816cc214f0f27efa4e014b88479a95997a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpointsConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cba3e7043886e9ae41ee353f1db7f043e1bdd82131bc7518413496e6c8fefd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsClusterEndpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00b1e48e3c68ecd87bcd37b41d87b6c85e13c02d791fe5c919dbc3fc5ea8892(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    region: builtins.str,
    cluster_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterUserCreatedConnectionsClusterEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[RedisClusterUserCreatedConnectionsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571f7c35112b7f5a19d9371fc8e35454ec35c977f7b1e5aa472ebcaf4e25e5e7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689affe7ddff3600478e484f45250d4b243ef21eae5ffa2e3703970aef123533(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8079c34451baf5c62b113c281018ce47c8bca819000b37e1dd05253c30d90569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d084388266cba83aeacb191511b896fc361b1e5f48ab9b672ebe865cca5bcaf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ac004f5e989ab333255298017dddf32051e80b838e56abf467cdb24025d9cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61272d93a12c6d72b911c0f972e0bfda26f5d93da10f75cabe5b040958d7a90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterUserCreatedConnectionsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
