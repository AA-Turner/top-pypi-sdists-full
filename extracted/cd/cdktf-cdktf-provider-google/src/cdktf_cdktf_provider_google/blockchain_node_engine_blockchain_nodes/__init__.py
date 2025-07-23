r'''
# `google_blockchain_node_engine_blockchain_nodes`

Refer to the Terraform Registry for docs: [`google_blockchain_node_engine_blockchain_nodes`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes).
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


class BlockchainNodeEngineBlockchainNodes(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodes",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes google_blockchain_node_engine_blockchain_nodes}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        blockchain_node_id: builtins.str,
        location: builtins.str,
        blockchain_type: typing.Optional[builtins.str] = None,
        ethereum_details: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesEthereumDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes google_blockchain_node_engine_blockchain_nodes} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param blockchain_node_id: ID of the requesting object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#blockchain_node_id BlockchainNodeEngineBlockchainNodes#blockchain_node_id}
        :param location: Location of Blockchain Node being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#location BlockchainNodeEngineBlockchainNodes#location}
        :param blockchain_type: User-provided key-value pairs Possible values: ["ETHEREUM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#blockchain_type BlockchainNodeEngineBlockchainNodes#blockchain_type}
        :param ethereum_details: ethereum_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#ethereum_details BlockchainNodeEngineBlockchainNodes#ethereum_details}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#id BlockchainNodeEngineBlockchainNodes#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-provided key-value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#labels BlockchainNodeEngineBlockchainNodes#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#project BlockchainNodeEngineBlockchainNodes#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#timeouts BlockchainNodeEngineBlockchainNodes#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5640a637bbc7c5d810b501b2246dbc86a758f303af35ec75d47e9d22d6e29394)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BlockchainNodeEngineBlockchainNodesConfig(
            blockchain_node_id=blockchain_node_id,
            location=location,
            blockchain_type=blockchain_type,
            ethereum_details=ethereum_details,
            id=id,
            labels=labels,
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
        '''Generates CDKTF code for importing a BlockchainNodeEngineBlockchainNodes resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BlockchainNodeEngineBlockchainNodes to import.
        :param import_from_id: The id of the existing BlockchainNodeEngineBlockchainNodes that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BlockchainNodeEngineBlockchainNodes to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcea21c290b92e6a2c90ea8fc6938e18d378d6179116860b53b3e83a89fcee9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEthereumDetails")
    def put_ethereum_details(
        self,
        *,
        api_enable_admin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_enable_debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        consensus_client: typing.Optional[builtins.str] = None,
        execution_client: typing.Optional[builtins.str] = None,
        fetchh_details: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        validator_config: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_enable_admin: Enables JSON-RPC access to functions in the admin namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#api_enable_admin BlockchainNodeEngineBlockchainNodes#api_enable_admin}
        :param api_enable_debug: Enables JSON-RPC access to functions in the debug namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#api_enable_debug BlockchainNodeEngineBlockchainNodes#api_enable_debug}
        :param consensus_client: The consensus client Possible values: ["CONSENSUS_CLIENT_UNSPECIFIED", "LIGHTHOUSE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#consensus_client BlockchainNodeEngineBlockchainNodes#consensus_client}
        :param execution_client: The execution client Possible values: ["EXECUTION_CLIENT_UNSPECIFIED", "GETH", "ERIGON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#execution_client BlockchainNodeEngineBlockchainNodes#execution_client}
        :param fetchh_details: geth_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#geth_details BlockchainNodeEngineBlockchainNodes#geth_details}
        :param network: The Ethereum environment being accessed. Possible values: ["MAINNET", "TESTNET_GOERLI_PRATER", "TESTNET_SEPOLIA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#network BlockchainNodeEngineBlockchainNodes#network}
        :param node_type: The type of Ethereum node. Possible values: ["LIGHT", "FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#node_type BlockchainNodeEngineBlockchainNodes#node_type}
        :param validator_config: validator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#validator_config BlockchainNodeEngineBlockchainNodes#validator_config}
        '''
        value = BlockchainNodeEngineBlockchainNodesEthereumDetails(
            api_enable_admin=api_enable_admin,
            api_enable_debug=api_enable_debug,
            consensus_client=consensus_client,
            execution_client=execution_client,
            fetchh_details=fetchh_details,
            network=network,
            node_type=node_type,
            validator_config=validator_config,
        )

        return typing.cast(None, jsii.invoke(self, "putEthereumDetails", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#create BlockchainNodeEngineBlockchainNodes#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#delete BlockchainNodeEngineBlockchainNodes#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#update BlockchainNodeEngineBlockchainNodes#update}.
        '''
        value = BlockchainNodeEngineBlockchainNodesTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlockchainType")
    def reset_blockchain_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockchainType", []))

    @jsii.member(jsii_name="resetEthereumDetails")
    def reset_ethereum_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEthereumDetails", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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
    @jsii.member(jsii_name="connectionInfo")
    def connection_info(
        self,
    ) -> "BlockchainNodeEngineBlockchainNodesConnectionInfoList":
        return typing.cast("BlockchainNodeEngineBlockchainNodesConnectionInfoList", jsii.get(self, "connectionInfo"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="ethereumDetails")
    def ethereum_details(
        self,
    ) -> "BlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference":
        return typing.cast("BlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference", jsii.get(self, "ethereumDetails"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BlockchainNodeEngineBlockchainNodesTimeoutsOutputReference":
        return typing.cast("BlockchainNodeEngineBlockchainNodesTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="blockchainNodeIdInput")
    def blockchain_node_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockchainNodeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="blockchainTypeInput")
    def blockchain_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockchainTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ethereumDetailsInput")
    def ethereum_details_input(
        self,
    ) -> typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetails"]:
        return typing.cast(typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetails"], jsii.get(self, "ethereumDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BlockchainNodeEngineBlockchainNodesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BlockchainNodeEngineBlockchainNodesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="blockchainNodeId")
    def blockchain_node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockchainNodeId"))

    @blockchain_node_id.setter
    def blockchain_node_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f17a617407d523d6f1d11a1147b59406c0ce086698cfad381d2ebe974cc70b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockchainNodeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockchainType")
    def blockchain_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockchainType"))

    @blockchain_type.setter
    def blockchain_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2742dcc4a11f3f80c9886b499344d89654275235e2cccdc9750617fa444516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockchainType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fb00e499700b0659167243324a7c6a6c8a0083156ebaa5f151a97f7fd3e5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828dd354bf157bdc72a9a5e1d5e0e7dba971d79d509d694ff51036aa6e1e89d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d30d56cc5ea5b1a009394198aab4621fd5ea3fffbcaea8fa5ba704c379f06c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5cbee8961287b0458e5ef29253a10038df28f20834245c1a142b74f7629ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "blockchain_node_id": "blockchainNodeId",
        "location": "location",
        "blockchain_type": "blockchainType",
        "ethereum_details": "ethereumDetails",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class BlockchainNodeEngineBlockchainNodesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        blockchain_node_id: builtins.str,
        location: builtins.str,
        blockchain_type: typing.Optional[builtins.str] = None,
        ethereum_details: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesEthereumDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param blockchain_node_id: ID of the requesting object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#blockchain_node_id BlockchainNodeEngineBlockchainNodes#blockchain_node_id}
        :param location: Location of Blockchain Node being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#location BlockchainNodeEngineBlockchainNodes#location}
        :param blockchain_type: User-provided key-value pairs Possible values: ["ETHEREUM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#blockchain_type BlockchainNodeEngineBlockchainNodes#blockchain_type}
        :param ethereum_details: ethereum_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#ethereum_details BlockchainNodeEngineBlockchainNodes#ethereum_details}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#id BlockchainNodeEngineBlockchainNodes#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-provided key-value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#labels BlockchainNodeEngineBlockchainNodes#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#project BlockchainNodeEngineBlockchainNodes#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#timeouts BlockchainNodeEngineBlockchainNodes#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ethereum_details, dict):
            ethereum_details = BlockchainNodeEngineBlockchainNodesEthereumDetails(**ethereum_details)
        if isinstance(timeouts, dict):
            timeouts = BlockchainNodeEngineBlockchainNodesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb086546add46925e6126ccf1189ee61ced61b4b81df5f4d8d35e14d923d14b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument blockchain_node_id", value=blockchain_node_id, expected_type=type_hints["blockchain_node_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument blockchain_type", value=blockchain_type, expected_type=type_hints["blockchain_type"])
            check_type(argname="argument ethereum_details", value=ethereum_details, expected_type=type_hints["ethereum_details"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blockchain_node_id": blockchain_node_id,
            "location": location,
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
        if blockchain_type is not None:
            self._values["blockchain_type"] = blockchain_type
        if ethereum_details is not None:
            self._values["ethereum_details"] = ethereum_details
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
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
    def blockchain_node_id(self) -> builtins.str:
        '''ID of the requesting object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#blockchain_node_id BlockchainNodeEngineBlockchainNodes#blockchain_node_id}
        '''
        result = self._values.get("blockchain_node_id")
        assert result is not None, "Required property 'blockchain_node_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location of Blockchain Node being created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#location BlockchainNodeEngineBlockchainNodes#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blockchain_type(self) -> typing.Optional[builtins.str]:
        '''User-provided key-value pairs Possible values: ["ETHEREUM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#blockchain_type BlockchainNodeEngineBlockchainNodes#blockchain_type}
        '''
        result = self._values.get("blockchain_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ethereum_details(
        self,
    ) -> typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetails"]:
        '''ethereum_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#ethereum_details BlockchainNodeEngineBlockchainNodes#ethereum_details}
        '''
        result = self._values.get("ethereum_details")
        return typing.cast(typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetails"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#id BlockchainNodeEngineBlockchainNodes#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided key-value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#labels BlockchainNodeEngineBlockchainNodes#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#project BlockchainNodeEngineBlockchainNodes#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["BlockchainNodeEngineBlockchainNodesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#timeouts BlockchainNodeEngineBlockchainNodes#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BlockchainNodeEngineBlockchainNodesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConnectionInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class BlockchainNodeEngineBlockchainNodesConnectionInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesConnectionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f65f59dfa0acb6ea08f9475dd895af84c173b2939d876e424e00b040fdd15b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1056cc081209542e6ec8ec19564bd2ae8f14ce41adadf10c48a837edb05dcc4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a15d5a22e257ef1d24a22461b47091201871d0bd93a131a7e020cff39cd7e70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb5ed35356f9224c7e24930a6d54f724e9570c3379ccda6c078db2864dbb5880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11096005f7fde77563d650f394a23c6abcf17194e52443b1cad5cd3fd7fcb4fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c66a41da7c8f6b6b550efcc9dc9bda545b2cff12bdecca4fcf556a18133df502)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="jsonRpcApiEndpoint")
    def json_rpc_api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonRpcApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="websocketsApiEndpoint")
    def websockets_api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "websocketsApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f757c2e9402bdb490b336fde0b16b20e30615a64019328fd9167fef68696716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BlockchainNodeEngineBlockchainNodesConnectionInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConnectionInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b63d7a26b7c840fc3c69d7cf857aae2bdf8196200ea3d9e338408f29cd2d7e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc17d6b127da421a248a323055d622a4323ac36b15729a458bd63a8faa0b1394)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6202634e173af43a9ef22bdc258ae9a789e4c8861a2c1accaec419dc82076c2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6e4bccc2c6cfe2f3b129359288833d4b82f9928be1cbe7d49a8dce1e16a925a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7acac41fa8913377f283f99cdf3427170df03c2103fe1b62e258ec06cd79261e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class BlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e1d78073fbcfd767b07c0d144d26f8d006fc924ba100c5d76314f87ad2894c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointInfo")
    def endpoint_info(
        self,
    ) -> BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList:
        return typing.cast(BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList, jsii.get(self, "endpointInfo"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfo]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8a1adf4f9d2491d66b1e6281f2e31b099c7e55b2083d31521ebc97bd140c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetails",
    jsii_struct_bases=[],
    name_mapping={
        "api_enable_admin": "apiEnableAdmin",
        "api_enable_debug": "apiEnableDebug",
        "consensus_client": "consensusClient",
        "execution_client": "executionClient",
        "fetchh_details": "fetchhDetails",
        "network": "network",
        "node_type": "nodeType",
        "validator_config": "validatorConfig",
    },
)
class BlockchainNodeEngineBlockchainNodesEthereumDetails:
    def __init__(
        self,
        *,
        api_enable_admin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_enable_debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        consensus_client: typing.Optional[builtins.str] = None,
        execution_client: typing.Optional[builtins.str] = None,
        fetchh_details: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        validator_config: typing.Optional[typing.Union["BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_enable_admin: Enables JSON-RPC access to functions in the admin namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#api_enable_admin BlockchainNodeEngineBlockchainNodes#api_enable_admin}
        :param api_enable_debug: Enables JSON-RPC access to functions in the debug namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#api_enable_debug BlockchainNodeEngineBlockchainNodes#api_enable_debug}
        :param consensus_client: The consensus client Possible values: ["CONSENSUS_CLIENT_UNSPECIFIED", "LIGHTHOUSE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#consensus_client BlockchainNodeEngineBlockchainNodes#consensus_client}
        :param execution_client: The execution client Possible values: ["EXECUTION_CLIENT_UNSPECIFIED", "GETH", "ERIGON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#execution_client BlockchainNodeEngineBlockchainNodes#execution_client}
        :param fetchh_details: geth_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#geth_details BlockchainNodeEngineBlockchainNodes#geth_details}
        :param network: The Ethereum environment being accessed. Possible values: ["MAINNET", "TESTNET_GOERLI_PRATER", "TESTNET_SEPOLIA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#network BlockchainNodeEngineBlockchainNodes#network}
        :param node_type: The type of Ethereum node. Possible values: ["LIGHT", "FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#node_type BlockchainNodeEngineBlockchainNodes#node_type}
        :param validator_config: validator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#validator_config BlockchainNodeEngineBlockchainNodes#validator_config}
        '''
        if isinstance(fetchh_details, dict):
            fetchh_details = BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails(**fetchh_details)
        if isinstance(validator_config, dict):
            validator_config = BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig(**validator_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a858b5714ba84864d5cc75681e9fe1b9c0e2c73140177d527e58b221c123519)
            check_type(argname="argument api_enable_admin", value=api_enable_admin, expected_type=type_hints["api_enable_admin"])
            check_type(argname="argument api_enable_debug", value=api_enable_debug, expected_type=type_hints["api_enable_debug"])
            check_type(argname="argument consensus_client", value=consensus_client, expected_type=type_hints["consensus_client"])
            check_type(argname="argument execution_client", value=execution_client, expected_type=type_hints["execution_client"])
            check_type(argname="argument fetchh_details", value=fetchh_details, expected_type=type_hints["fetchh_details"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument validator_config", value=validator_config, expected_type=type_hints["validator_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_enable_admin is not None:
            self._values["api_enable_admin"] = api_enable_admin
        if api_enable_debug is not None:
            self._values["api_enable_debug"] = api_enable_debug
        if consensus_client is not None:
            self._values["consensus_client"] = consensus_client
        if execution_client is not None:
            self._values["execution_client"] = execution_client
        if fetchh_details is not None:
            self._values["fetchh_details"] = fetchh_details
        if network is not None:
            self._values["network"] = network
        if node_type is not None:
            self._values["node_type"] = node_type
        if validator_config is not None:
            self._values["validator_config"] = validator_config

    @builtins.property
    def api_enable_admin(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables JSON-RPC access to functions in the admin namespace. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#api_enable_admin BlockchainNodeEngineBlockchainNodes#api_enable_admin}
        '''
        result = self._values.get("api_enable_admin")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def api_enable_debug(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables JSON-RPC access to functions in the debug namespace. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#api_enable_debug BlockchainNodeEngineBlockchainNodes#api_enable_debug}
        '''
        result = self._values.get("api_enable_debug")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def consensus_client(self) -> typing.Optional[builtins.str]:
        '''The consensus client Possible values: ["CONSENSUS_CLIENT_UNSPECIFIED", "LIGHTHOUSE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#consensus_client BlockchainNodeEngineBlockchainNodes#consensus_client}
        '''
        result = self._values.get("consensus_client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_client(self) -> typing.Optional[builtins.str]:
        '''The execution client Possible values: ["EXECUTION_CLIENT_UNSPECIFIED", "GETH", "ERIGON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#execution_client BlockchainNodeEngineBlockchainNodes#execution_client}
        '''
        result = self._values.get("execution_client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fetchh_details(
        self,
    ) -> typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails"]:
        '''geth_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#geth_details BlockchainNodeEngineBlockchainNodes#geth_details}
        '''
        result = self._values.get("fetchh_details")
        return typing.cast(typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails"], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Ethereum environment being accessed. Possible values: ["MAINNET", "TESTNET_GOERLI_PRATER", "TESTNET_SEPOLIA"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#network BlockchainNodeEngineBlockchainNodes#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The type of Ethereum node. Possible values: ["LIGHT", "FULL", "ARCHIVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#node_type BlockchainNodeEngineBlockchainNodes#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validator_config(
        self,
    ) -> typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"]:
        '''validator_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#validator_config BlockchainNodeEngineBlockchainNodes#validator_config}
        '''
        result = self._values.get("validator_config")
        return typing.cast(typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesEthereumDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c5908fb61c916650c23fe4f0cc9899142ccdcde58cc4bc1c2917da4a0365915)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ba433b716e3a2d24e36b85a51233548c492ef0df2ee58a4d972fef888230b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc0c56253066bc0273387108f5d0e3af45a6dbe7f6118e49164cc9098258ca8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5121df3869770876bd70e2829a0f8d5a356f6950b26931afabf3a9aa68c141ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__021320e90f99dbf409598c3def7b7aa305ab851c276e2347cc1eca4073d0854c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23c9813e7f506bcc425cd2bc1ab68b9ae5abe441f28494e027ecdae3c6f5893c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="beaconApiEndpoint")
    def beacon_api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beaconApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="beaconPrometheusMetricsApiEndpoint")
    def beacon_prometheus_metrics_api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "beaconPrometheusMetricsApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="executionClientPrometheusMetricsApiEndpoint")
    def execution_client_prometheus_metrics_api_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionClientPrometheusMetricsApiEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba728ed5fb07bfd9358642912a222e75cc3f011e8ca35a8201c7a424464a0f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails",
    jsii_struct_bases=[],
    name_mapping={"garbage_collection_mode": "garbageCollectionMode"},
)
class BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails:
    def __init__(
        self,
        *,
        garbage_collection_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param garbage_collection_mode: Blockchain garbage collection modes. Only applicable when NodeType is FULL or ARCHIVE. Possible values: ["FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#garbage_collection_mode BlockchainNodeEngineBlockchainNodes#garbage_collection_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77a86d92acbdf2c5242f98c15cf5e37beee9bfc304435b031759a64b1f48347)
            check_type(argname="argument garbage_collection_mode", value=garbage_collection_mode, expected_type=type_hints["garbage_collection_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if garbage_collection_mode is not None:
            self._values["garbage_collection_mode"] = garbage_collection_mode

    @builtins.property
    def garbage_collection_mode(self) -> typing.Optional[builtins.str]:
        '''Blockchain garbage collection modes. Only applicable when NodeType is FULL or ARCHIVE. Possible values: ["FULL", "ARCHIVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#garbage_collection_mode BlockchainNodeEngineBlockchainNodes#garbage_collection_mode}
        '''
        result = self._values.get("garbage_collection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1aec5eb575a54076abd2318da9ce2dc972f976ec13b96c50dfeadcb749cf76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGarbageCollectionMode")
    def reset_garbage_collection_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGarbageCollectionMode", []))

    @builtins.property
    @jsii.member(jsii_name="garbageCollectionModeInput")
    def garbage_collection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "garbageCollectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="garbageCollectionMode")
    def garbage_collection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "garbageCollectionMode"))

    @garbage_collection_mode.setter
    def garbage_collection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e984c2d510609441ed17d1797771038bfdc459eb998a69827fee14685f774f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "garbageCollectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b2f1dfa5eb3fa7fb4e790636f4efc93b1e6f060a6176dba1be6c451bf692ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56291b6851be9b4bb8362ba6a021f735cdf4cd26f0282540aec3ed09ee3f2c6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFetchhDetails")
    def put_fetchh_details(
        self,
        *,
        garbage_collection_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param garbage_collection_mode: Blockchain garbage collection modes. Only applicable when NodeType is FULL or ARCHIVE. Possible values: ["FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#garbage_collection_mode BlockchainNodeEngineBlockchainNodes#garbage_collection_mode}
        '''
        value = BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails(
            garbage_collection_mode=garbage_collection_mode
        )

        return typing.cast(None, jsii.invoke(self, "putFetchhDetails", [value]))

    @jsii.member(jsii_name="putValidatorConfig")
    def put_validator_config(
        self,
        *,
        mev_relay_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param mev_relay_urls: URLs for MEV-relay services to use for block building. When set, a managed MEV-boost service is configured on the beacon client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#mev_relay_urls BlockchainNodeEngineBlockchainNodes#mev_relay_urls}
        '''
        value = BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig(
            mev_relay_urls=mev_relay_urls
        )

        return typing.cast(None, jsii.invoke(self, "putValidatorConfig", [value]))

    @jsii.member(jsii_name="resetApiEnableAdmin")
    def reset_api_enable_admin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiEnableAdmin", []))

    @jsii.member(jsii_name="resetApiEnableDebug")
    def reset_api_enable_debug(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiEnableDebug", []))

    @jsii.member(jsii_name="resetConsensusClient")
    def reset_consensus_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsensusClient", []))

    @jsii.member(jsii_name="resetExecutionClient")
    def reset_execution_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionClient", []))

    @jsii.member(jsii_name="resetFetchhDetails")
    def reset_fetchh_details(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchhDetails", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetValidatorConfig")
    def reset_validator_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidatorConfig", []))

    @builtins.property
    @jsii.member(jsii_name="additionalEndpoints")
    def additional_endpoints(
        self,
    ) -> BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList:
        return typing.cast(BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList, jsii.get(self, "additionalEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="fetchhDetails")
    def fetchh_details(
        self,
    ) -> BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference:
        return typing.cast(BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference, jsii.get(self, "fetchhDetails"))

    @builtins.property
    @jsii.member(jsii_name="validatorConfig")
    def validator_config(
        self,
    ) -> "BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference":
        return typing.cast("BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference", jsii.get(self, "validatorConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiEnableAdminInput")
    def api_enable_admin_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "apiEnableAdminInput"))

    @builtins.property
    @jsii.member(jsii_name="apiEnableDebugInput")
    def api_enable_debug_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "apiEnableDebugInput"))

    @builtins.property
    @jsii.member(jsii_name="consensusClientInput")
    def consensus_client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consensusClientInput"))

    @builtins.property
    @jsii.member(jsii_name="executionClientInput")
    def execution_client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionClientInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchhDetailsInput")
    def fetchh_details_input(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails], jsii.get(self, "fetchhDetailsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="validatorConfigInput")
    def validator_config_input(
        self,
    ) -> typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"]:
        return typing.cast(typing.Optional["BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"], jsii.get(self, "validatorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="apiEnableAdmin")
    def api_enable_admin(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "apiEnableAdmin"))

    @api_enable_admin.setter
    def api_enable_admin(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66604c8c931bafe0cac99bc80460118ad10061ed20967ebc528a174f8f36bade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiEnableAdmin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiEnableDebug")
    def api_enable_debug(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "apiEnableDebug"))

    @api_enable_debug.setter
    def api_enable_debug(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e942474727e6fd9f4e598d55e63a56321edbbc8c4bd5e9b3faa5e57d20f26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiEnableDebug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consensusClient")
    def consensus_client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consensusClient"))

    @consensus_client.setter
    def consensus_client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3990564f825d8ee31fd819b1ec2d07967abb98d28c3b9a386c79a56a066500c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consensusClient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionClient")
    def execution_client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionClient"))

    @execution_client.setter
    def execution_client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006d97d1c0a30b2c4243bcfc87543df7f8ec7ef5647017b4215f6cae111e2f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionClient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdac7e13d0e7634675a304b0868471be7ed7faf9c84af0d3d1960f2fc3208180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9737d873b64d0c42866965a3af57ee198f6e384894db9a0dec57dac75c9ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetails]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6766960ba80990d492ea1279fd5773871f6c160ee0f9542877a9daf21b7a75cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig",
    jsii_struct_bases=[],
    name_mapping={"mev_relay_urls": "mevRelayUrls"},
)
class BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig:
    def __init__(
        self,
        *,
        mev_relay_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param mev_relay_urls: URLs for MEV-relay services to use for block building. When set, a managed MEV-boost service is configured on the beacon client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#mev_relay_urls BlockchainNodeEngineBlockchainNodes#mev_relay_urls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9daf2e410b137f43953c4ab2ee29995e9d0e4a79c52e6d8f4fe2a7e09257945)
            check_type(argname="argument mev_relay_urls", value=mev_relay_urls, expected_type=type_hints["mev_relay_urls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mev_relay_urls is not None:
            self._values["mev_relay_urls"] = mev_relay_urls

    @builtins.property
    def mev_relay_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URLs for MEV-relay services to use for block building.

        When set, a managed MEV-boost service is configured on the beacon client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#mev_relay_urls BlockchainNodeEngineBlockchainNodes#mev_relay_urls}
        '''
        result = self._values.get("mev_relay_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88c0138984c21b03a3e6d88fc2aee02bb441c60a2cd4cb7ba32915071235f796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMevRelayUrls")
    def reset_mev_relay_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMevRelayUrls", []))

    @builtins.property
    @jsii.member(jsii_name="mevRelayUrlsInput")
    def mev_relay_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "mevRelayUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="mevRelayUrls")
    def mev_relay_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mevRelayUrls"))

    @mev_relay_urls.setter
    def mev_relay_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425be25c84d6dc354a9c9fad13eca64c764e74e16102fe22f605b6c5b8c41a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mevRelayUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig]:
        return typing.cast(typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c1739255e9f381746ab24aca6afb9c47ad2d5df083c10f52163be0298038b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BlockchainNodeEngineBlockchainNodesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#create BlockchainNodeEngineBlockchainNodes#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#delete BlockchainNodeEngineBlockchainNodes#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#update BlockchainNodeEngineBlockchainNodes#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cd5a66415c45bfe952b2324b7db1c64e2d9673c287557023fe1e7cb0fb460e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#create BlockchainNodeEngineBlockchainNodes#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#delete BlockchainNodeEngineBlockchainNodes#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/blockchain_node_engine_blockchain_nodes#update BlockchainNodeEngineBlockchainNodes#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockchainNodeEngineBlockchainNodesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BlockchainNodeEngineBlockchainNodesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.blockchainNodeEngineBlockchainNodes.BlockchainNodeEngineBlockchainNodesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bb954e17aba89114b782b89a97bd8f13ca59081ec5db005e22012504dd126c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bc42bc0086c478b59354d583261c1b2b5f370b36b30b34f4f8e15a53277afc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521aecd540268086bea11388f99b6753ac0b10a0a5f92b69ce90bfccd2fd587c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11d572ddf7d52f4fe101b4688fd44946f8406b8b762b14f3c99f0b7e1a375fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockchainNodeEngineBlockchainNodesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockchainNodeEngineBlockchainNodesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockchainNodeEngineBlockchainNodesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f079e17364f0dfcbd19b09a796e144838758f79723b13d18af84eb2c705a3d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BlockchainNodeEngineBlockchainNodes",
    "BlockchainNodeEngineBlockchainNodesConfig",
    "BlockchainNodeEngineBlockchainNodesConnectionInfo",
    "BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo",
    "BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList",
    "BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference",
    "BlockchainNodeEngineBlockchainNodesConnectionInfoList",
    "BlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference",
    "BlockchainNodeEngineBlockchainNodesEthereumDetails",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig",
    "BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference",
    "BlockchainNodeEngineBlockchainNodesTimeouts",
    "BlockchainNodeEngineBlockchainNodesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5640a637bbc7c5d810b501b2246dbc86a758f303af35ec75d47e9d22d6e29394(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    blockchain_node_id: builtins.str,
    location: builtins.str,
    blockchain_type: typing.Optional[builtins.str] = None,
    ethereum_details: typing.Optional[typing.Union[BlockchainNodeEngineBlockchainNodesEthereumDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BlockchainNodeEngineBlockchainNodesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6fcea21c290b92e6a2c90ea8fc6938e18d378d6179116860b53b3e83a89fcee9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f17a617407d523d6f1d11a1147b59406c0ce086698cfad381d2ebe974cc70b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2742dcc4a11f3f80c9886b499344d89654275235e2cccdc9750617fa444516(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fb00e499700b0659167243324a7c6a6c8a0083156ebaa5f151a97f7fd3e5e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828dd354bf157bdc72a9a5e1d5e0e7dba971d79d509d694ff51036aa6e1e89d5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d30d56cc5ea5b1a009394198aab4621fd5ea3fffbcaea8fa5ba704c379f06c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5cbee8961287b0458e5ef29253a10038df28f20834245c1a142b74f7629ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb086546add46925e6126ccf1189ee61ced61b4b81df5f4d8d35e14d923d14b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    blockchain_node_id: builtins.str,
    location: builtins.str,
    blockchain_type: typing.Optional[builtins.str] = None,
    ethereum_details: typing.Optional[typing.Union[BlockchainNodeEngineBlockchainNodesEthereumDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BlockchainNodeEngineBlockchainNodesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f65f59dfa0acb6ea08f9475dd895af84c173b2939d876e424e00b040fdd15b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1056cc081209542e6ec8ec19564bd2ae8f14ce41adadf10c48a837edb05dcc4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a15d5a22e257ef1d24a22461b47091201871d0bd93a131a7e020cff39cd7e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5ed35356f9224c7e24930a6d54f724e9570c3379ccda6c078db2864dbb5880(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11096005f7fde77563d650f394a23c6abcf17194e52443b1cad5cd3fd7fcb4fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66a41da7c8f6b6b550efcc9dc9bda545b2cff12bdecca4fcf556a18133df502(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f757c2e9402bdb490b336fde0b16b20e30615a64019328fd9167fef68696716(
    value: typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b63d7a26b7c840fc3c69d7cf857aae2bdf8196200ea3d9e338408f29cd2d7e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc17d6b127da421a248a323055d622a4323ac36b15729a458bd63a8faa0b1394(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6202634e173af43a9ef22bdc258ae9a789e4c8861a2c1accaec419dc82076c2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e4bccc2c6cfe2f3b129359288833d4b82f9928be1cbe7d49a8dce1e16a925a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acac41fa8913377f283f99cdf3427170df03c2103fe1b62e258ec06cd79261e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e1d78073fbcfd767b07c0d144d26f8d006fc924ba100c5d76314f87ad2894c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8a1adf4f9d2491d66b1e6281f2e31b099c7e55b2083d31521ebc97bd140c8c(
    value: typing.Optional[BlockchainNodeEngineBlockchainNodesConnectionInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a858b5714ba84864d5cc75681e9fe1b9c0e2c73140177d527e58b221c123519(
    *,
    api_enable_admin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    api_enable_debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    consensus_client: typing.Optional[builtins.str] = None,
    execution_client: typing.Optional[builtins.str] = None,
    fetchh_details: typing.Optional[typing.Union[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    validator_config: typing.Optional[typing.Union[BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5908fb61c916650c23fe4f0cc9899142ccdcde58cc4bc1c2917da4a0365915(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ba433b716e3a2d24e36b85a51233548c492ef0df2ee58a4d972fef888230b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc0c56253066bc0273387108f5d0e3af45a6dbe7f6118e49164cc9098258ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5121df3869770876bd70e2829a0f8d5a356f6950b26931afabf3a9aa68c141ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021320e90f99dbf409598c3def7b7aa305ab851c276e2347cc1eca4073d0854c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c9813e7f506bcc425cd2bc1ab68b9ae5abe441f28494e027ecdae3c6f5893c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba728ed5fb07bfd9358642912a222e75cc3f011e8ca35a8201c7a424464a0f7a(
    value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77a86d92acbdf2c5242f98c15cf5e37beee9bfc304435b031759a64b1f48347(
    *,
    garbage_collection_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1aec5eb575a54076abd2318da9ce2dc972f976ec13b96c50dfeadcb749cf76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e984c2d510609441ed17d1797771038bfdc459eb998a69827fee14685f774f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b2f1dfa5eb3fa7fb4e790636f4efc93b1e6f060a6176dba1be6c451bf692ad(
    value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56291b6851be9b4bb8362ba6a021f735cdf4cd26f0282540aec3ed09ee3f2c6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66604c8c931bafe0cac99bc80460118ad10061ed20967ebc528a174f8f36bade(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e942474727e6fd9f4e598d55e63a56321edbbc8c4bd5e9b3faa5e57d20f26b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3990564f825d8ee31fd819b1ec2d07967abb98d28c3b9a386c79a56a066500c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006d97d1c0a30b2c4243bcfc87543df7f8ec7ef5647017b4215f6cae111e2f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdac7e13d0e7634675a304b0868471be7ed7faf9c84af0d3d1960f2fc3208180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9737d873b64d0c42866965a3af57ee198f6e384894db9a0dec57dac75c9ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6766960ba80990d492ea1279fd5773871f6c160ee0f9542877a9daf21b7a75cc(
    value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9daf2e410b137f43953c4ab2ee29995e9d0e4a79c52e6d8f4fe2a7e09257945(
    *,
    mev_relay_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c0138984c21b03a3e6d88fc2aee02bb441c60a2cd4cb7ba32915071235f796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425be25c84d6dc354a9c9fad13eca64c764e74e16102fe22f605b6c5b8c41a6f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c1739255e9f381746ab24aca6afb9c47ad2d5df083c10f52163be0298038b8(
    value: typing.Optional[BlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cd5a66415c45bfe952b2324b7db1c64e2d9673c287557023fe1e7cb0fb460e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb954e17aba89114b782b89a97bd8f13ca59081ec5db005e22012504dd126c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc42bc0086c478b59354d583261c1b2b5f370b36b30b34f4f8e15a53277afc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521aecd540268086bea11388f99b6753ac0b10a0a5f92b69ce90bfccd2fd587c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11d572ddf7d52f4fe101b4688fd44946f8406b8b762b14f3c99f0b7e1a375fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f079e17364f0dfcbd19b09a796e144838758f79723b13d18af84eb2c705a3d62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BlockchainNodeEngineBlockchainNodesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
