r'''
# `google_blockchain_node_engine_blockchain_nodes`

Refer to the Terraform Registry for docs: [`google_blockchain_node_engine_blockchain_nodes`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes).
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


class GoogleBlockchainNodeEngineBlockchainNodes(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodes",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes google_blockchain_node_engine_blockchain_nodes}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        blockchain_node_id: builtins.str,
        location: builtins.str,
        blockchain_type: typing.Optional[builtins.str] = None,
        ethereum_details: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes google_blockchain_node_engine_blockchain_nodes} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param blockchain_node_id: ID of the requesting object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#blockchain_node_id GoogleBlockchainNodeEngineBlockchainNodes#blockchain_node_id}
        :param location: Location of Blockchain Node being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#location GoogleBlockchainNodeEngineBlockchainNodes#location}
        :param blockchain_type: User-provided key-value pairs Possible values: ["ETHEREUM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#blockchain_type GoogleBlockchainNodeEngineBlockchainNodes#blockchain_type}
        :param ethereum_details: ethereum_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#ethereum_details GoogleBlockchainNodeEngineBlockchainNodes#ethereum_details}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#id GoogleBlockchainNodeEngineBlockchainNodes#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-provided key-value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#labels GoogleBlockchainNodeEngineBlockchainNodes#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#project GoogleBlockchainNodeEngineBlockchainNodes#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#timeouts GoogleBlockchainNodeEngineBlockchainNodes#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3016d3ebf8050f3fa8626c599ab4213c19d41d7b08efa26afde8aab1a5651cf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBlockchainNodeEngineBlockchainNodesConfig(
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
        '''Generates CDKTF code for importing a GoogleBlockchainNodeEngineBlockchainNodes resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBlockchainNodeEngineBlockchainNodes to import.
        :param import_from_id: The id of the existing GoogleBlockchainNodeEngineBlockchainNodes that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBlockchainNodeEngineBlockchainNodes to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbedd3e518c50dc2da1090720203ea97d2ebb69282ba32df67a94d3c20e202dd)
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
        fetchh_details: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        validator_config: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_enable_admin: Enables JSON-RPC access to functions in the admin namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#api_enable_admin GoogleBlockchainNodeEngineBlockchainNodes#api_enable_admin}
        :param api_enable_debug: Enables JSON-RPC access to functions in the debug namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#api_enable_debug GoogleBlockchainNodeEngineBlockchainNodes#api_enable_debug}
        :param consensus_client: The consensus client Possible values: ["CONSENSUS_CLIENT_UNSPECIFIED", "LIGHTHOUSE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#consensus_client GoogleBlockchainNodeEngineBlockchainNodes#consensus_client}
        :param execution_client: The execution client Possible values: ["EXECUTION_CLIENT_UNSPECIFIED", "GETH", "ERIGON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#execution_client GoogleBlockchainNodeEngineBlockchainNodes#execution_client}
        :param fetchh_details: geth_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#geth_details GoogleBlockchainNodeEngineBlockchainNodes#geth_details}
        :param network: The Ethereum environment being accessed. Possible values: ["MAINNET", "TESTNET_GOERLI_PRATER", "TESTNET_SEPOLIA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#network GoogleBlockchainNodeEngineBlockchainNodes#network}
        :param node_type: The type of Ethereum node. Possible values: ["LIGHT", "FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#node_type GoogleBlockchainNodeEngineBlockchainNodes#node_type}
        :param validator_config: validator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#validator_config GoogleBlockchainNodeEngineBlockchainNodes#validator_config}
        '''
        value = GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#create GoogleBlockchainNodeEngineBlockchainNodes#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#delete GoogleBlockchainNodeEngineBlockchainNodes#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#update GoogleBlockchainNodeEngineBlockchainNodes#update}.
        '''
        value = GoogleBlockchainNodeEngineBlockchainNodesTimeouts(
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
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoList":
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoList", jsii.get(self, "connectionInfo"))

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
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference":
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference", jsii.get(self, "ethereumDetails"))

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
    def timeouts(
        self,
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesTimeoutsOutputReference":
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails"]:
        return typing.cast(typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails"], jsii.get(self, "ethereumDetailsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBlockchainNodeEngineBlockchainNodesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBlockchainNodeEngineBlockchainNodesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="blockchainNodeId")
    def blockchain_node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockchainNodeId"))

    @blockchain_node_id.setter
    def blockchain_node_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6f86a7da9871ef12390d0af2e5dc9ff51856e12ffd83591aaa6e554e7ad2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockchainNodeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockchainType")
    def blockchain_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockchainType"))

    @blockchain_type.setter
    def blockchain_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b5d079a01d2500f3f8566adad9fc97758552af7443e8561abb527bd9ccfae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockchainType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca88d2748a9798a0c187f2af4e49b6f00f64e7dbd0fbfbeab53e962dc7c754b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fdab1435acc5d59b7375a821d4c755d9759f56a07cfc8703821acd717d05120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891159072c338833db0287f5931bc8c6bf5ec5f018de114af19b45a6d3935b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18195b4fd96acb9ec94793ea20d4d5b7dfcd3f3190a3f4036832fdee2b507e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConfig",
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
class GoogleBlockchainNodeEngineBlockchainNodesConfig(
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
        blockchain_node_id: builtins.str,
        location: builtins.str,
        blockchain_type: typing.Optional[builtins.str] = None,
        ethereum_details: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param blockchain_node_id: ID of the requesting object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#blockchain_node_id GoogleBlockchainNodeEngineBlockchainNodes#blockchain_node_id}
        :param location: Location of Blockchain Node being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#location GoogleBlockchainNodeEngineBlockchainNodes#location}
        :param blockchain_type: User-provided key-value pairs Possible values: ["ETHEREUM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#blockchain_type GoogleBlockchainNodeEngineBlockchainNodes#blockchain_type}
        :param ethereum_details: ethereum_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#ethereum_details GoogleBlockchainNodeEngineBlockchainNodes#ethereum_details}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#id GoogleBlockchainNodeEngineBlockchainNodes#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-provided key-value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#labels GoogleBlockchainNodeEngineBlockchainNodes#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#project GoogleBlockchainNodeEngineBlockchainNodes#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#timeouts GoogleBlockchainNodeEngineBlockchainNodes#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ethereum_details, dict):
            ethereum_details = GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails(**ethereum_details)
        if isinstance(timeouts, dict):
            timeouts = GoogleBlockchainNodeEngineBlockchainNodesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb938b622e8aa36c215f14387d92bbab521f52b87914bfd010f506ebfcceb0d4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#blockchain_node_id GoogleBlockchainNodeEngineBlockchainNodes#blockchain_node_id}
        '''
        result = self._values.get("blockchain_node_id")
        assert result is not None, "Required property 'blockchain_node_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location of Blockchain Node being created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#location GoogleBlockchainNodeEngineBlockchainNodes#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blockchain_type(self) -> typing.Optional[builtins.str]:
        '''User-provided key-value pairs Possible values: ["ETHEREUM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#blockchain_type GoogleBlockchainNodeEngineBlockchainNodes#blockchain_type}
        '''
        result = self._values.get("blockchain_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ethereum_details(
        self,
    ) -> typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails"]:
        '''ethereum_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#ethereum_details GoogleBlockchainNodeEngineBlockchainNodes#ethereum_details}
        '''
        result = self._values.get("ethereum_details")
        return typing.cast(typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#id GoogleBlockchainNodeEngineBlockchainNodes#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#labels GoogleBlockchainNodeEngineBlockchainNodes#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#project GoogleBlockchainNodeEngineBlockchainNodes#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#timeouts GoogleBlockchainNodeEngineBlockchainNodes#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af7539790b0eeb19f625f6ee290cea3f8921f6d0ff31722a7fd199283ba3e5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816944ccedba5a8dda139c75211efbe7eb517718f6a7d18d527d9f9b76d8a27b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1fc3cbb0d66bbcf7a735fad6134e252dd567b882a912c4e36db615a7a52667)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09ba97a4dbf69b72cde0b712f624b8c746dc0167ca9d3b8a27612b23f822e392)
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
            type_hints = typing.get_type_hints(_typecheckingstub__516bcfa2553b18089bd11baf0b87b19d96a444410c116043e8c7d1672194ee3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3f724176ea5128d7738c828cf9895d2b71ff7b58010147eb4b77b21dfa68b28)
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
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0950f37d96e33991b75bd7379d174947ed03a4bc6156642887362b084330c564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63463c1b2feb2de46e9b4e153ae2255191c813304defdcd054936238f9afc1ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b465b96bd92bafe653af01fa8d42100142c5c682c26f4abe1e0a550bb69c3b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5a5d9b2d041ffce3fac13d37fbdd17e27884a9bbff9606e08f23d5ac85b689)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1552e7b797d830dc8f8bf80e8d8a21d5756e0160f4ae95f49e7e248db0b25cd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4708f0e8a7c384495c45943bb42d1cd7459d3ed1e6503918372aba5c55646626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cbfbfbbd942b161912e4727c919fb671ec853bb8f29f52c56e843132aa8f214)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointInfo")
    def endpoint_info(
        self,
    ) -> GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList:
        return typing.cast(GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList, jsii.get(self, "endpointInfo"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0362cc38aafa3fd875ae1a11456dcb636d0c151ce5ac6675dfa790c88da15bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails",
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
class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails:
    def __init__(
        self,
        *,
        api_enable_admin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_enable_debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        consensus_client: typing.Optional[builtins.str] = None,
        execution_client: typing.Optional[builtins.str] = None,
        fetchh_details: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        validator_config: typing.Optional[typing.Union["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_enable_admin: Enables JSON-RPC access to functions in the admin namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#api_enable_admin GoogleBlockchainNodeEngineBlockchainNodes#api_enable_admin}
        :param api_enable_debug: Enables JSON-RPC access to functions in the debug namespace. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#api_enable_debug GoogleBlockchainNodeEngineBlockchainNodes#api_enable_debug}
        :param consensus_client: The consensus client Possible values: ["CONSENSUS_CLIENT_UNSPECIFIED", "LIGHTHOUSE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#consensus_client GoogleBlockchainNodeEngineBlockchainNodes#consensus_client}
        :param execution_client: The execution client Possible values: ["EXECUTION_CLIENT_UNSPECIFIED", "GETH", "ERIGON"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#execution_client GoogleBlockchainNodeEngineBlockchainNodes#execution_client}
        :param fetchh_details: geth_details block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#geth_details GoogleBlockchainNodeEngineBlockchainNodes#geth_details}
        :param network: The Ethereum environment being accessed. Possible values: ["MAINNET", "TESTNET_GOERLI_PRATER", "TESTNET_SEPOLIA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#network GoogleBlockchainNodeEngineBlockchainNodes#network}
        :param node_type: The type of Ethereum node. Possible values: ["LIGHT", "FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#node_type GoogleBlockchainNodeEngineBlockchainNodes#node_type}
        :param validator_config: validator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#validator_config GoogleBlockchainNodeEngineBlockchainNodes#validator_config}
        '''
        if isinstance(fetchh_details, dict):
            fetchh_details = GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails(**fetchh_details)
        if isinstance(validator_config, dict):
            validator_config = GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig(**validator_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f469723c71ba0e4d866588f7c2da7abcc36c8fbf6749ccf08fd1586a25231b0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#api_enable_admin GoogleBlockchainNodeEngineBlockchainNodes#api_enable_admin}
        '''
        result = self._values.get("api_enable_admin")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def api_enable_debug(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables JSON-RPC access to functions in the debug namespace. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#api_enable_debug GoogleBlockchainNodeEngineBlockchainNodes#api_enable_debug}
        '''
        result = self._values.get("api_enable_debug")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def consensus_client(self) -> typing.Optional[builtins.str]:
        '''The consensus client Possible values: ["CONSENSUS_CLIENT_UNSPECIFIED", "LIGHTHOUSE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#consensus_client GoogleBlockchainNodeEngineBlockchainNodes#consensus_client}
        '''
        result = self._values.get("consensus_client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_client(self) -> typing.Optional[builtins.str]:
        '''The execution client Possible values: ["EXECUTION_CLIENT_UNSPECIFIED", "GETH", "ERIGON"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#execution_client GoogleBlockchainNodeEngineBlockchainNodes#execution_client}
        '''
        result = self._values.get("execution_client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fetchh_details(
        self,
    ) -> typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails"]:
        '''geth_details block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#geth_details GoogleBlockchainNodeEngineBlockchainNodes#geth_details}
        '''
        result = self._values.get("fetchh_details")
        return typing.cast(typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails"], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Ethereum environment being accessed. Possible values: ["MAINNET", "TESTNET_GOERLI_PRATER", "TESTNET_SEPOLIA"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#network GoogleBlockchainNodeEngineBlockchainNodes#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The type of Ethereum node. Possible values: ["LIGHT", "FULL", "ARCHIVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#node_type GoogleBlockchainNodeEngineBlockchainNodes#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validator_config(
        self,
    ) -> typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"]:
        '''validator_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#validator_config GoogleBlockchainNodeEngineBlockchainNodes#validator_config}
        '''
        result = self._values.get("validator_config")
        return typing.cast(typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed192e47f917a5e08b66a5297b92a05c412b6f65597c1b6724b11face8cd70d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639a736249f003b4329ac99ea0ffc38e477acdf39c113fa5ebf6fa2874c5ea30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37df4dea5b8e3d33449ca09d8eb7b516569659bdeae33455ae5ff29ae11ebf38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00df6fa18a03701434e987a5b9710a184e02ba28ddb707072528c82201da2530)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f2a67e707b7f91c284890d0623ee74ccc1a6414d3db8bce19848f4fe5694b71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8211b2e948af382af32970cebf7507d5d921df1f66f97d34d92ee0b88bcb7b18)
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
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f162e79d609917c2ceae2045c5346624ee1ba0c961c2aa7da1f8aa56096974b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails",
    jsii_struct_bases=[],
    name_mapping={"garbage_collection_mode": "garbageCollectionMode"},
)
class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails:
    def __init__(
        self,
        *,
        garbage_collection_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param garbage_collection_mode: Blockchain garbage collection modes. Only applicable when NodeType is FULL or ARCHIVE. Possible values: ["FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#garbage_collection_mode GoogleBlockchainNodeEngineBlockchainNodes#garbage_collection_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c22e0492aad79084f11769c97db4499fe7e661cdcc4e4ac18e9ab3ea32ba651)
            check_type(argname="argument garbage_collection_mode", value=garbage_collection_mode, expected_type=type_hints["garbage_collection_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if garbage_collection_mode is not None:
            self._values["garbage_collection_mode"] = garbage_collection_mode

    @builtins.property
    def garbage_collection_mode(self) -> typing.Optional[builtins.str]:
        '''Blockchain garbage collection modes. Only applicable when NodeType is FULL or ARCHIVE. Possible values: ["FULL", "ARCHIVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#garbage_collection_mode GoogleBlockchainNodeEngineBlockchainNodes#garbage_collection_mode}
        '''
        result = self._values.get("garbage_collection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af3c5df98c2f5ca2477abe23dc7673c797f32a93d647137e6a260514a52da0dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68aae9d32ae36921cb322a4644c5dc1fd9a44d38b1227a3b9ad7d536f22c738c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "garbageCollectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ecde8b55cb40fbd92fb2617591f9e5b1ded0d478fc714e4626b3f084189b489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bccc819f4fdaa2c55f86856704e94d0f1788179e1100e88aa2f9d8f8a4dba6ce)
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
        :param garbage_collection_mode: Blockchain garbage collection modes. Only applicable when NodeType is FULL or ARCHIVE. Possible values: ["FULL", "ARCHIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#garbage_collection_mode GoogleBlockchainNodeEngineBlockchainNodes#garbage_collection_mode}
        '''
        value = GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails(
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
        :param mev_relay_urls: URLs for MEV-relay services to use for block building. When set, a managed MEV-boost service is configured on the beacon client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#mev_relay_urls GoogleBlockchainNodeEngineBlockchainNodes#mev_relay_urls}
        '''
        value = GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig(
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
    ) -> GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList:
        return typing.cast(GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList, jsii.get(self, "additionalEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="fetchhDetails")
    def fetchh_details(
        self,
    ) -> GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference:
        return typing.cast(GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference, jsii.get(self, "fetchhDetails"))

    @builtins.property
    @jsii.member(jsii_name="validatorConfig")
    def validator_config(
        self,
    ) -> "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference":
        return typing.cast("GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference", jsii.get(self, "validatorConfig"))

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
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails], jsii.get(self, "fetchhDetailsInput"))

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
    ) -> typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"]:
        return typing.cast(typing.Optional["GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig"], jsii.get(self, "validatorConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2a92c3bcce4a6eadac92d6a287af6ed29a41af81f953b6d9fe86e38309798466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__461e5d954c2161188d250f64d71f7012420035d6c916c336546f16ec8cd22a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiEnableDebug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consensusClient")
    def consensus_client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consensusClient"))

    @consensus_client.setter
    def consensus_client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2db790f9fc4e505d0d51f11acbe48b94c689dce380388b774eabc07f9c0463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consensusClient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionClient")
    def execution_client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionClient"))

    @execution_client.setter
    def execution_client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3f70a592ac4a824293289d0eccb2a30f2852c33c0f179fa81ce8bc5bde44b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionClient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e739b4df555cd351bb8d49d12d8d1ba18c96ef2f46ad42d1c16a67646c70df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933e7847f1b93b8afd0f02a5cd224aad32a71c1d11c7c530b5efdb794448aefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43aadbc0533c41b57df92523afd4786c96d3a91e2e07b5d07ad6718192cc7cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig",
    jsii_struct_bases=[],
    name_mapping={"mev_relay_urls": "mevRelayUrls"},
)
class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig:
    def __init__(
        self,
        *,
        mev_relay_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param mev_relay_urls: URLs for MEV-relay services to use for block building. When set, a managed MEV-boost service is configured on the beacon client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#mev_relay_urls GoogleBlockchainNodeEngineBlockchainNodes#mev_relay_urls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b9d72f3d2e6182d0b0aa3d52427fccb44d3f5a80985f0ba8e57a70b56a422f)
            check_type(argname="argument mev_relay_urls", value=mev_relay_urls, expected_type=type_hints["mev_relay_urls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mev_relay_urls is not None:
            self._values["mev_relay_urls"] = mev_relay_urls

    @builtins.property
    def mev_relay_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URLs for MEV-relay services to use for block building.

        When set, a managed MEV-boost service is configured on the beacon client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#mev_relay_urls GoogleBlockchainNodeEngineBlockchainNodes#mev_relay_urls}
        '''
        result = self._values.get("mev_relay_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ba94177897bef02ae7fde38d59769d9e036304b4dc722f92abd8cf47ab0e089)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a36d5497a8aae5946802925bbee5c9ff3940a8a1296763e7f4491feecea3d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mevRelayUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig]:
        return typing.cast(typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb858c8e089044d22ac159e9bec2950cf13b5e0b64b9bed07f5a3fef0ae7d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBlockchainNodeEngineBlockchainNodesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#create GoogleBlockchainNodeEngineBlockchainNodes#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#delete GoogleBlockchainNodeEngineBlockchainNodes#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#update GoogleBlockchainNodeEngineBlockchainNodes#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddc5bbf4bbda84b263af2799c56984d181ec875b2987457935b24d774ae352e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#create GoogleBlockchainNodeEngineBlockchainNodes#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#delete GoogleBlockchainNodeEngineBlockchainNodes#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_blockchain_node_engine_blockchain_nodes#update GoogleBlockchainNodeEngineBlockchainNodes#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBlockchainNodeEngineBlockchainNodesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBlockchainNodeEngineBlockchainNodesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBlockchainNodeEngineBlockchainNodes.GoogleBlockchainNodeEngineBlockchainNodesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05876fa5a17ef613855583132cd3833d030ba49f4db493f8cd77ee135a2ce6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57f96fb47112aac214752639ec7f0132b5deefe95fa6379a673c2ec96fe3acd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013bd3996b0010380bca055b0eebd8f788a5fda147cee6f19030e3dc4e76ec36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea7c715fdc82051f3129e33f7b72c46b3bfac3d0ebfb542453fac49c0499b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBlockchainNodeEngineBlockchainNodesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBlockchainNodeEngineBlockchainNodesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBlockchainNodeEngineBlockchainNodesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce487e3bd005f99750ee54204645baaeed60e1562125d0df6381e84ea082ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBlockchainNodeEngineBlockchainNodes",
    "GoogleBlockchainNodeEngineBlockchainNodesConfig",
    "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo",
    "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo",
    "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoList",
    "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfoOutputReference",
    "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoList",
    "GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoOutputReference",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsList",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpointsOutputReference",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetailsOutputReference",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsOutputReference",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig",
    "GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfigOutputReference",
    "GoogleBlockchainNodeEngineBlockchainNodesTimeouts",
    "GoogleBlockchainNodeEngineBlockchainNodesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3016d3ebf8050f3fa8626c599ab4213c19d41d7b08efa26afde8aab1a5651cf9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    blockchain_node_id: builtins.str,
    location: builtins.str,
    blockchain_type: typing.Optional[builtins.str] = None,
    ethereum_details: typing.Optional[typing.Union[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBlockchainNodeEngineBlockchainNodesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dbedd3e518c50dc2da1090720203ea97d2ebb69282ba32df67a94d3c20e202dd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6f86a7da9871ef12390d0af2e5dc9ff51856e12ffd83591aaa6e554e7ad2cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b5d079a01d2500f3f8566adad9fc97758552af7443e8561abb527bd9ccfae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca88d2748a9798a0c187f2af4e49b6f00f64e7dbd0fbfbeab53e962dc7c754b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fdab1435acc5d59b7375a821d4c755d9759f56a07cfc8703821acd717d05120(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891159072c338833db0287f5931bc8c6bf5ec5f018de114af19b45a6d3935b3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18195b4fd96acb9ec94793ea20d4d5b7dfcd3f3190a3f4036832fdee2b507e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb938b622e8aa36c215f14387d92bbab521f52b87914bfd010f506ebfcceb0d4(
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
    ethereum_details: typing.Optional[typing.Union[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBlockchainNodeEngineBlockchainNodesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af7539790b0eeb19f625f6ee290cea3f8921f6d0ff31722a7fd199283ba3e5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816944ccedba5a8dda139c75211efbe7eb517718f6a7d18d527d9f9b76d8a27b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1fc3cbb0d66bbcf7a735fad6134e252dd567b882a912c4e36db615a7a52667(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ba97a4dbf69b72cde0b712f624b8c746dc0167ca9d3b8a27612b23f822e392(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516bcfa2553b18089bd11baf0b87b19d96a444410c116043e8c7d1672194ee3f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f724176ea5128d7738c828cf9895d2b71ff7b58010147eb4b77b21dfa68b28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0950f37d96e33991b75bd7379d174947ed03a4bc6156642887362b084330c564(
    value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfoEndpointInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63463c1b2feb2de46e9b4e153ae2255191c813304defdcd054936238f9afc1ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b465b96bd92bafe653af01fa8d42100142c5c682c26f4abe1e0a550bb69c3b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5a5d9b2d041ffce3fac13d37fbdd17e27884a9bbff9606e08f23d5ac85b689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1552e7b797d830dc8f8bf80e8d8a21d5756e0160f4ae95f49e7e248db0b25cd5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4708f0e8a7c384495c45943bb42d1cd7459d3ed1e6503918372aba5c55646626(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbfbfbbd942b161912e4727c919fb671ec853bb8f29f52c56e843132aa8f214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0362cc38aafa3fd875ae1a11456dcb636d0c151ce5ac6675dfa790c88da15bcb(
    value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesConnectionInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f469723c71ba0e4d866588f7c2da7abcc36c8fbf6749ccf08fd1586a25231b0(
    *,
    api_enable_admin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    api_enable_debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    consensus_client: typing.Optional[builtins.str] = None,
    execution_client: typing.Optional[builtins.str] = None,
    fetchh_details: typing.Optional[typing.Union[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    validator_config: typing.Optional[typing.Union[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed192e47f917a5e08b66a5297b92a05c412b6f65597c1b6724b11face8cd70d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639a736249f003b4329ac99ea0ffc38e477acdf39c113fa5ebf6fa2874c5ea30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37df4dea5b8e3d33449ca09d8eb7b516569659bdeae33455ae5ff29ae11ebf38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00df6fa18a03701434e987a5b9710a184e02ba28ddb707072528c82201da2530(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2a67e707b7f91c284890d0623ee74ccc1a6414d3db8bce19848f4fe5694b71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8211b2e948af382af32970cebf7507d5d921df1f66f97d34d92ee0b88bcb7b18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f162e79d609917c2ceae2045c5346624ee1ba0c961c2aa7da1f8aa56096974b(
    value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsAdditionalEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c22e0492aad79084f11769c97db4499fe7e661cdcc4e4ac18e9ab3ea32ba651(
    *,
    garbage_collection_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3c5df98c2f5ca2477abe23dc7673c797f32a93d647137e6a260514a52da0dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68aae9d32ae36921cb322a4644c5dc1fd9a44d38b1227a3b9ad7d536f22c738c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecde8b55cb40fbd92fb2617591f9e5b1ded0d478fc714e4626b3f084189b489(
    value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsGethDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bccc819f4fdaa2c55f86856704e94d0f1788179e1100e88aa2f9d8f8a4dba6ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a92c3bcce4a6eadac92d6a287af6ed29a41af81f953b6d9fe86e38309798466(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461e5d954c2161188d250f64d71f7012420035d6c916c336546f16ec8cd22a23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2db790f9fc4e505d0d51f11acbe48b94c689dce380388b774eabc07f9c0463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3f70a592ac4a824293289d0eccb2a30f2852c33c0f179fa81ce8bc5bde44b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e739b4df555cd351bb8d49d12d8d1ba18c96ef2f46ad42d1c16a67646c70df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933e7847f1b93b8afd0f02a5cd224aad32a71c1d11c7c530b5efdb794448aefb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43aadbc0533c41b57df92523afd4786c96d3a91e2e07b5d07ad6718192cc7cfc(
    value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b9d72f3d2e6182d0b0aa3d52427fccb44d3f5a80985f0ba8e57a70b56a422f(
    *,
    mev_relay_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba94177897bef02ae7fde38d59769d9e036304b4dc722f92abd8cf47ab0e089(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a36d5497a8aae5946802925bbee5c9ff3940a8a1296763e7f4491feecea3d01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb858c8e089044d22ac159e9bec2950cf13b5e0b64b9bed07f5a3fef0ae7d6d(
    value: typing.Optional[GoogleBlockchainNodeEngineBlockchainNodesEthereumDetailsValidatorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddc5bbf4bbda84b263af2799c56984d181ec875b2987457935b24d774ae352e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05876fa5a17ef613855583132cd3833d030ba49f4db493f8cd77ee135a2ce6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f96fb47112aac214752639ec7f0132b5deefe95fa6379a673c2ec96fe3acd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013bd3996b0010380bca055b0eebd8f788a5fda147cee6f19030e3dc4e76ec36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea7c715fdc82051f3129e33f7b72c46b3bfac3d0ebfb542453fac49c0499b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce487e3bd005f99750ee54204645baaeed60e1562125d0df6381e84ea082ac3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBlockchainNodeEngineBlockchainNodesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
