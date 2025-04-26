r'''
# `data_github_repository_pull_requests`

Refer to the Terraform Registry for docs: [`data_github_repository_pull_requests`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests).
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


class DataGithubRepositoryPullRequests(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.dataGithubRepositoryPullRequests.DataGithubRepositoryPullRequests",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests github_repository_pull_requests}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        base_repository: builtins.str,
        base_ref: typing.Optional[builtins.str] = None,
        head_ref: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_direction: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests github_repository_pull_requests} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param base_repository: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#base_repository DataGithubRepositoryPullRequests#base_repository}.
        :param base_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#base_ref DataGithubRepositoryPullRequests#base_ref}.
        :param head_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#head_ref DataGithubRepositoryPullRequests#head_ref}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#id DataGithubRepositoryPullRequests#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#owner DataGithubRepositoryPullRequests#owner}.
        :param sort_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#sort_by DataGithubRepositoryPullRequests#sort_by}.
        :param sort_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#sort_direction DataGithubRepositoryPullRequests#sort_direction}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#state DataGithubRepositoryPullRequests#state}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c858bc6d8c4a606ea654eae2167a1c0769c1e9e39c582c1306304d61ce89ba2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGithubRepositoryPullRequestsConfig(
            base_repository=base_repository,
            base_ref=base_ref,
            head_ref=head_ref,
            id=id,
            owner=owner,
            sort_by=sort_by,
            sort_direction=sort_direction,
            state=state,
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
        '''Generates CDKTF code for importing a DataGithubRepositoryPullRequests resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGithubRepositoryPullRequests to import.
        :param import_from_id: The id of the existing DataGithubRepositoryPullRequests that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGithubRepositoryPullRequests to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7398efc7a8efd53a690bb9db0ed9d94e3da1755c53c5da642c421812e1af4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetBaseRef")
    def reset_base_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseRef", []))

    @jsii.member(jsii_name="resetHeadRef")
    def reset_head_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadRef", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetSortBy")
    def reset_sort_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortBy", []))

    @jsii.member(jsii_name="resetSortDirection")
    def reset_sort_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSortDirection", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

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
    @jsii.member(jsii_name="results")
    def results(self) -> "DataGithubRepositoryPullRequestsResultsList":
        return typing.cast("DataGithubRepositoryPullRequestsResultsList", jsii.get(self, "results"))

    @builtins.property
    @jsii.member(jsii_name="baseRefInput")
    def base_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseRefInput"))

    @builtins.property
    @jsii.member(jsii_name="baseRepositoryInput")
    def base_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="headRefInput")
    def head_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headRefInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="sortByInput")
    def sort_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortByInput"))

    @builtins.property
    @jsii.member(jsii_name="sortDirectionInput")
    def sort_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="baseRef")
    def base_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseRef"))

    @base_ref.setter
    def base_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c30e6157acd90182f98680ddb60c5d9bf601f2639f34146ca9811965fa0bec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseRepository")
    def base_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseRepository"))

    @base_repository.setter
    def base_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f8b11383074e3584a85aab64a49b8206e4197cf50ce37cdb214fb4922b699b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headRef")
    def head_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headRef"))

    @head_ref.setter
    def head_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257d05d73e54d57de26ee5de033fb3a8722fd4063d7c1138ca0866790403292a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headRef", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95da15d923c03e200d3e19a1362b19593459a54293a0e1887f199ee76163d711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796a87800657180161c7dcb53ec9bb70bc18e01cd346a2ccdfb5d23d0f8e3854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortBy")
    def sort_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortBy"))

    @sort_by.setter
    def sort_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01688fe87b45b8dd305e4491148eafa09a96a6d6214a27ae6501ee44738e4dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sortDirection")
    def sort_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sortDirection"))

    @sort_direction.setter
    def sort_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e76934c698a3b6d43cabf3a8b7eb529ad693e84ad9556e2d663ef9239284bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sortDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55820c97f03a392348d1210a21cf4926f7329fdf6d630c23db2d1e3835ad981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.dataGithubRepositoryPullRequests.DataGithubRepositoryPullRequestsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "base_repository": "baseRepository",
        "base_ref": "baseRef",
        "head_ref": "headRef",
        "id": "id",
        "owner": "owner",
        "sort_by": "sortBy",
        "sort_direction": "sortDirection",
        "state": "state",
    },
)
class DataGithubRepositoryPullRequestsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        base_repository: builtins.str,
        base_ref: typing.Optional[builtins.str] = None,
        head_ref: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_direction: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param base_repository: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#base_repository DataGithubRepositoryPullRequests#base_repository}.
        :param base_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#base_ref DataGithubRepositoryPullRequests#base_ref}.
        :param head_ref: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#head_ref DataGithubRepositoryPullRequests#head_ref}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#id DataGithubRepositoryPullRequests#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#owner DataGithubRepositoryPullRequests#owner}.
        :param sort_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#sort_by DataGithubRepositoryPullRequests#sort_by}.
        :param sort_direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#sort_direction DataGithubRepositoryPullRequests#sort_direction}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#state DataGithubRepositoryPullRequests#state}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092182f2b8dd98dbb1a092e8070b76b6493c3966988634ba28fb99a5a1835da1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument base_repository", value=base_repository, expected_type=type_hints["base_repository"])
            check_type(argname="argument base_ref", value=base_ref, expected_type=type_hints["base_ref"])
            check_type(argname="argument head_ref", value=head_ref, expected_type=type_hints["head_ref"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument sort_by", value=sort_by, expected_type=type_hints["sort_by"])
            check_type(argname="argument sort_direction", value=sort_direction, expected_type=type_hints["sort_direction"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_repository": base_repository,
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
        if base_ref is not None:
            self._values["base_ref"] = base_ref
        if head_ref is not None:
            self._values["head_ref"] = head_ref
        if id is not None:
            self._values["id"] = id
        if owner is not None:
            self._values["owner"] = owner
        if sort_by is not None:
            self._values["sort_by"] = sort_by
        if sort_direction is not None:
            self._values["sort_direction"] = sort_direction
        if state is not None:
            self._values["state"] = state

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
    def base_repository(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#base_repository DataGithubRepositoryPullRequests#base_repository}.'''
        result = self._values.get("base_repository")
        assert result is not None, "Required property 'base_repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#base_ref DataGithubRepositoryPullRequests#base_ref}.'''
        result = self._values.get("base_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def head_ref(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#head_ref DataGithubRepositoryPullRequests#head_ref}.'''
        result = self._values.get("head_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#id DataGithubRepositoryPullRequests#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#owner DataGithubRepositoryPullRequests#owner}.'''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_by(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#sort_by DataGithubRepositoryPullRequests#sort_by}.'''
        result = self._values.get("sort_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#sort_direction DataGithubRepositoryPullRequests#sort_direction}.'''
        result = self._values.get("sort_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/data-sources/repository_pull_requests#state DataGithubRepositoryPullRequests#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubRepositoryPullRequestsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.dataGithubRepositoryPullRequests.DataGithubRepositoryPullRequestsResults",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGithubRepositoryPullRequestsResults:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGithubRepositoryPullRequestsResults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGithubRepositoryPullRequestsResultsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.dataGithubRepositoryPullRequests.DataGithubRepositoryPullRequestsResultsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b42460cabdf3e8fb7e11e25e97d9f6dea7bc91f9cf7001550c7b71f95ce1f44b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGithubRepositoryPullRequestsResultsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4359603bfbbdb0341d157936c9044c397208cea3ac0ad6d8df7976f3232de942)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGithubRepositoryPullRequestsResultsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105eb8537e31195ca9043c967f06ae37929a0663267f29a67c67324b2cbec1c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52237aac1fee4aaa7e2243b7e900371b9bfbc5821a1c8ad4b489a02762da765c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22b32064f50ae84e254a47e0068cf24cbe3e27c3f110f03e70ec8cdbf257f6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGithubRepositoryPullRequestsResultsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.dataGithubRepositoryPullRequests.DataGithubRepositoryPullRequestsResultsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5e7ee1df81cfa0f85254ea5669c0f8a0209d0f32f3d726cefecabb31e1d0d12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="baseRef")
    def base_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseRef"))

    @builtins.property
    @jsii.member(jsii_name="baseSha")
    def base_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseSha"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="draft")
    def draft(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "draft"))

    @builtins.property
    @jsii.member(jsii_name="headOwner")
    def head_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headOwner"))

    @builtins.property
    @jsii.member(jsii_name="headRef")
    def head_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headRef"))

    @builtins.property
    @jsii.member(jsii_name="headRepository")
    def head_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headRepository"))

    @builtins.property
    @jsii.member(jsii_name="headSha")
    def head_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headSha"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="maintainerCanModify")
    def maintainer_can_modify(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "maintainerCanModify"))

    @builtins.property
    @jsii.member(jsii_name="number")
    def number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "number"))

    @builtins.property
    @jsii.member(jsii_name="openedAt")
    def opened_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "openedAt"))

    @builtins.property
    @jsii.member(jsii_name="openedBy")
    def opened_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openedBy"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGithubRepositoryPullRequestsResults]:
        return typing.cast(typing.Optional[DataGithubRepositoryPullRequestsResults], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGithubRepositoryPullRequestsResults],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27082182388215f6cc1f738dda47e9b79a0b828de025b7a250816084864d231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataGithubRepositoryPullRequests",
    "DataGithubRepositoryPullRequestsConfig",
    "DataGithubRepositoryPullRequestsResults",
    "DataGithubRepositoryPullRequestsResultsList",
    "DataGithubRepositoryPullRequestsResultsOutputReference",
]

publication.publish()

def _typecheckingstub__0c858bc6d8c4a606ea654eae2167a1c0769c1e9e39c582c1306304d61ce89ba2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    base_repository: builtins.str,
    base_ref: typing.Optional[builtins.str] = None,
    head_ref: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_direction: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9b7398efc7a8efd53a690bb9db0ed9d94e3da1755c53c5da642c421812e1af4e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c30e6157acd90182f98680ddb60c5d9bf601f2639f34146ca9811965fa0bec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f8b11383074e3584a85aab64a49b8206e4197cf50ce37cdb214fb4922b699b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257d05d73e54d57de26ee5de033fb3a8722fd4063d7c1138ca0866790403292a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95da15d923c03e200d3e19a1362b19593459a54293a0e1887f199ee76163d711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796a87800657180161c7dcb53ec9bb70bc18e01cd346a2ccdfb5d23d0f8e3854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01688fe87b45b8dd305e4491148eafa09a96a6d6214a27ae6501ee44738e4dfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e76934c698a3b6d43cabf3a8b7eb529ad693e84ad9556e2d663ef9239284bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55820c97f03a392348d1210a21cf4926f7329fdf6d630c23db2d1e3835ad981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092182f2b8dd98dbb1a092e8070b76b6493c3966988634ba28fb99a5a1835da1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    base_repository: builtins.str,
    base_ref: typing.Optional[builtins.str] = None,
    head_ref: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_direction: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42460cabdf3e8fb7e11e25e97d9f6dea7bc91f9cf7001550c7b71f95ce1f44b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4359603bfbbdb0341d157936c9044c397208cea3ac0ad6d8df7976f3232de942(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105eb8537e31195ca9043c967f06ae37929a0663267f29a67c67324b2cbec1c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52237aac1fee4aaa7e2243b7e900371b9bfbc5821a1c8ad4b489a02762da765c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b32064f50ae84e254a47e0068cf24cbe3e27c3f110f03e70ec8cdbf257f6b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e7ee1df81cfa0f85254ea5669c0f8a0209d0f32f3d726cefecabb31e1d0d12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27082182388215f6cc1f738dda47e9b79a0b828de025b7a250816084864d231(
    value: typing.Optional[DataGithubRepositoryPullRequestsResults],
) -> None:
    """Type checking stubs"""
    pass
