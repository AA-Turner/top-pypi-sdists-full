r'''
# `google_vertex_ai_rag_engine_config`

Refer to the Terraform Registry for docs: [`google_vertex_ai_rag_engine_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config).
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


class GoogleVertexAiRagEngineConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config google_vertex_ai_rag_engine_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        rag_managed_db_config: typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfig", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config google_vertex_ai_rag_engine_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param rag_managed_db_config: rag_managed_db_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#rag_managed_db_config GoogleVertexAiRagEngineConfig#rag_managed_db_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#id GoogleVertexAiRagEngineConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#project GoogleVertexAiRagEngineConfig#project}.
        :param region: The region of the RagEngineConfig. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#region GoogleVertexAiRagEngineConfig#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#timeouts GoogleVertexAiRagEngineConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a846f8fa1d3c7d345acd79e93869d7a0977b69c7d944c3447c8f1d62e7591609)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiRagEngineConfigConfig(
            rag_managed_db_config=rag_managed_db_config,
            id=id,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a GoogleVertexAiRagEngineConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiRagEngineConfig to import.
        :param import_from_id: The id of the existing GoogleVertexAiRagEngineConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiRagEngineConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd482522181d033da46d4dde65f0de4ae3caf434a6bce39bc83804dd1722216)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRagManagedDbConfig")
    def put_rag_managed_db_config(
        self,
        *,
        basic: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        scaled: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled", typing.Dict[builtins.str, typing.Any]]] = None,
        unprovisioned: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#basic GoogleVertexAiRagEngineConfig#basic}
        :param scaled: scaled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#scaled GoogleVertexAiRagEngineConfig#scaled}
        :param unprovisioned: unprovisioned block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#unprovisioned GoogleVertexAiRagEngineConfig#unprovisioned}
        '''
        value = GoogleVertexAiRagEngineConfigRagManagedDbConfig(
            basic=basic, scaled=scaled, unprovisioned=unprovisioned
        )

        return typing.cast(None, jsii.invoke(self, "putRagManagedDbConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#create GoogleVertexAiRagEngineConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#delete GoogleVertexAiRagEngineConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#update GoogleVertexAiRagEngineConfig#update}.
        '''
        value = GoogleVertexAiRagEngineConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="ragManagedDbConfig")
    def rag_managed_db_config(
        self,
    ) -> "GoogleVertexAiRagEngineConfigRagManagedDbConfigOutputReference":
        return typing.cast("GoogleVertexAiRagEngineConfigRagManagedDbConfigOutputReference", jsii.get(self, "ragManagedDbConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVertexAiRagEngineConfigTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiRagEngineConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="ragManagedDbConfigInput")
    def rag_managed_db_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfig"], jsii.get(self, "ragManagedDbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiRagEngineConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiRagEngineConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1768a70e47986f50ffc926d9db0b2a8f3f5efdf8afae122981630b0dc2035608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c614316376f4115d23827d5f99c9bb5c7fbcfb687e5f51be8cb43cf63cb37d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc5ef286cda7ae0d539aaf0b763a33ea1f83c643cad47bbc9d963c362e168b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "rag_managed_db_config": "ragManagedDbConfig",
        "id": "id",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class GoogleVertexAiRagEngineConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rag_managed_db_config: typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfig", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param rag_managed_db_config: rag_managed_db_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#rag_managed_db_config GoogleVertexAiRagEngineConfig#rag_managed_db_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#id GoogleVertexAiRagEngineConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#project GoogleVertexAiRagEngineConfig#project}.
        :param region: The region of the RagEngineConfig. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#region GoogleVertexAiRagEngineConfig#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#timeouts GoogleVertexAiRagEngineConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rag_managed_db_config, dict):
            rag_managed_db_config = GoogleVertexAiRagEngineConfigRagManagedDbConfig(**rag_managed_db_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiRagEngineConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433e2e4418939b109721e80307bd718406cc94a9c8e9e995c376f6efc8fa4356)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument rag_managed_db_config", value=rag_managed_db_config, expected_type=type_hints["rag_managed_db_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rag_managed_db_config": rag_managed_db_config,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def rag_managed_db_config(
        self,
    ) -> "GoogleVertexAiRagEngineConfigRagManagedDbConfig":
        '''rag_managed_db_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#rag_managed_db_config GoogleVertexAiRagEngineConfig#rag_managed_db_config}
        '''
        result = self._values.get("rag_managed_db_config")
        assert result is not None, "Required property 'rag_managed_db_config' is missing"
        return typing.cast("GoogleVertexAiRagEngineConfigRagManagedDbConfig", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#id GoogleVertexAiRagEngineConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#project GoogleVertexAiRagEngineConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the RagEngineConfig. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#region GoogleVertexAiRagEngineConfig#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleVertexAiRagEngineConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#timeouts GoogleVertexAiRagEngineConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiRagEngineConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "basic": "basic",
        "scaled": "scaled",
        "unprovisioned": "unprovisioned",
    },
)
class GoogleVertexAiRagEngineConfigRagManagedDbConfig:
    def __init__(
        self,
        *,
        basic: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        scaled: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled", typing.Dict[builtins.str, typing.Any]]] = None,
        unprovisioned: typing.Optional[typing.Union["GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#basic GoogleVertexAiRagEngineConfig#basic}
        :param scaled: scaled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#scaled GoogleVertexAiRagEngineConfig#scaled}
        :param unprovisioned: unprovisioned block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#unprovisioned GoogleVertexAiRagEngineConfig#unprovisioned}
        '''
        if isinstance(basic, dict):
            basic = GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic(**basic)
        if isinstance(scaled, dict):
            scaled = GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled(**scaled)
        if isinstance(unprovisioned, dict):
            unprovisioned = GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned(**unprovisioned)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fbf9eecb9a679c8f831a8ce4d5407719ea279996500a824627aa655cd83b03)
            check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
            check_type(argname="argument scaled", value=scaled, expected_type=type_hints["scaled"])
            check_type(argname="argument unprovisioned", value=unprovisioned, expected_type=type_hints["unprovisioned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic is not None:
            self._values["basic"] = basic
        if scaled is not None:
            self._values["scaled"] = scaled
        if unprovisioned is not None:
            self._values["unprovisioned"] = unprovisioned

    @builtins.property
    def basic(
        self,
    ) -> typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic"]:
        '''basic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#basic GoogleVertexAiRagEngineConfig#basic}
        '''
        result = self._values.get("basic")
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic"], result)

    @builtins.property
    def scaled(
        self,
    ) -> typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled"]:
        '''scaled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#scaled GoogleVertexAiRagEngineConfig#scaled}
        '''
        result = self._values.get("scaled")
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled"], result)

    @builtins.property
    def unprovisioned(
        self,
    ) -> typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned"]:
        '''unprovisioned block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#unprovisioned GoogleVertexAiRagEngineConfig#unprovisioned}
        '''
        result = self._values.get("unprovisioned")
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiRagEngineConfigRagManagedDbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiRagEngineConfigRagManagedDbConfigBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f6dc4b7246aecc56ac5e554e8583366edde13ca49736cdcbc3dcaecf42b9a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic]:
        return typing.cast(typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c8591d15c0762f75fb2e8df87755d412f6fd3331fd19f73a93659602b2df8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiRagEngineConfigRagManagedDbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af0606bcce9f47ceb60fbdb8e3c0ba3060ec535264b364e3430fde66e3be738)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasic")
    def put_basic(self) -> None:
        value = GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic()

        return typing.cast(None, jsii.invoke(self, "putBasic", [value]))

    @jsii.member(jsii_name="putScaled")
    def put_scaled(self) -> None:
        value = GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled()

        return typing.cast(None, jsii.invoke(self, "putScaled", [value]))

    @jsii.member(jsii_name="putUnprovisioned")
    def put_unprovisioned(self) -> None:
        value = GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned()

        return typing.cast(None, jsii.invoke(self, "putUnprovisioned", [value]))

    @jsii.member(jsii_name="resetBasic")
    def reset_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasic", []))

    @jsii.member(jsii_name="resetScaled")
    def reset_scaled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaled", []))

    @jsii.member(jsii_name="resetUnprovisioned")
    def reset_unprovisioned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnprovisioned", []))

    @builtins.property
    @jsii.member(jsii_name="basic")
    def basic(
        self,
    ) -> GoogleVertexAiRagEngineConfigRagManagedDbConfigBasicOutputReference:
        return typing.cast(GoogleVertexAiRagEngineConfigRagManagedDbConfigBasicOutputReference, jsii.get(self, "basic"))

    @builtins.property
    @jsii.member(jsii_name="scaled")
    def scaled(
        self,
    ) -> "GoogleVertexAiRagEngineConfigRagManagedDbConfigScaledOutputReference":
        return typing.cast("GoogleVertexAiRagEngineConfigRagManagedDbConfigScaledOutputReference", jsii.get(self, "scaled"))

    @builtins.property
    @jsii.member(jsii_name="unprovisioned")
    def unprovisioned(
        self,
    ) -> "GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisionedOutputReference":
        return typing.cast("GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisionedOutputReference", jsii.get(self, "unprovisioned"))

    @builtins.property
    @jsii.member(jsii_name="basicInput")
    def basic_input(
        self,
    ) -> typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic]:
        return typing.cast(typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic], jsii.get(self, "basicInput"))

    @builtins.property
    @jsii.member(jsii_name="scaledInput")
    def scaled_input(
        self,
    ) -> typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled"]:
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled"], jsii.get(self, "scaledInput"))

    @builtins.property
    @jsii.member(jsii_name="unprovisionedInput")
    def unprovisioned_input(
        self,
    ) -> typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned"]:
        return typing.cast(typing.Optional["GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned"], jsii.get(self, "unprovisionedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8197fc1c6072b9dd1bb8aa3a40fd418c6ad9d626a1e207aa1038088fb5420621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiRagEngineConfigRagManagedDbConfigScaledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigScaledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e7577453fe345be01c38cdd6f831a74a5fe346d073dd6cdc9466a89ac5e4a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled]:
        return typing.cast(typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfbaa248237a0724db4811e17bbc80bb4cabc7aabf84e551aa702203abe441d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisionedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisionedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b41702b4d358e9aff800b9c87544a2789e374f16e7a6731c29f5ca06b51725a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned]:
        return typing.cast(typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3529e49acba2a017f97c441e5044f31fee67b5311f5fa8d012758985c4e9893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiRagEngineConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#create GoogleVertexAiRagEngineConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#delete GoogleVertexAiRagEngineConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#update GoogleVertexAiRagEngineConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86952c407984fdbf0a8a02059d661cad6838d268888ef41a69ca700841b316e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#create GoogleVertexAiRagEngineConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#delete GoogleVertexAiRagEngineConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_rag_engine_config#update GoogleVertexAiRagEngineConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiRagEngineConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiRagEngineConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiRagEngineConfig.GoogleVertexAiRagEngineConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d75dbcbf99a7145810ca4f8188f52f85afd102c2c4cc5d6ada5d167140a898aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b378fc0aa4ba4122bd5b2c559d4a85c859737eef777e76c259a0fad3dd49c8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9103f3048202dc3d90d87f4763d5cdc367510238c496ae6ae281a3cb167bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4cb64255a1bd2983c6ef22a328aaae5ebd71c153575805a6e8f511fe5e3cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiRagEngineConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiRagEngineConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiRagEngineConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc91bcff16e2fbd15908bef30f00a34a5bc8f3c0d075782d2ac0255929e4d33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiRagEngineConfig",
    "GoogleVertexAiRagEngineConfigConfig",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfig",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigBasicOutputReference",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigOutputReference",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigScaledOutputReference",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned",
    "GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisionedOutputReference",
    "GoogleVertexAiRagEngineConfigTimeouts",
    "GoogleVertexAiRagEngineConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a846f8fa1d3c7d345acd79e93869d7a0977b69c7d944c3447c8f1d62e7591609(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    rag_managed_db_config: typing.Union[GoogleVertexAiRagEngineConfigRagManagedDbConfig, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiRagEngineConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7cd482522181d033da46d4dde65f0de4ae3caf434a6bce39bc83804dd1722216(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1768a70e47986f50ffc926d9db0b2a8f3f5efdf8afae122981630b0dc2035608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c614316376f4115d23827d5f99c9bb5c7fbcfb687e5f51be8cb43cf63cb37d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc5ef286cda7ae0d539aaf0b763a33ea1f83c643cad47bbc9d963c362e168b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433e2e4418939b109721e80307bd718406cc94a9c8e9e995c376f6efc8fa4356(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rag_managed_db_config: typing.Union[GoogleVertexAiRagEngineConfigRagManagedDbConfig, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiRagEngineConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fbf9eecb9a679c8f831a8ce4d5407719ea279996500a824627aa655cd83b03(
    *,
    basic: typing.Optional[typing.Union[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    scaled: typing.Optional[typing.Union[GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled, typing.Dict[builtins.str, typing.Any]]] = None,
    unprovisioned: typing.Optional[typing.Union[GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f6dc4b7246aecc56ac5e554e8583366edde13ca49736cdcbc3dcaecf42b9a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c8591d15c0762f75fb2e8df87755d412f6fd3331fd19f73a93659602b2df8c(
    value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af0606bcce9f47ceb60fbdb8e3c0ba3060ec535264b364e3430fde66e3be738(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8197fc1c6072b9dd1bb8aa3a40fd418c6ad9d626a1e207aa1038088fb5420621(
    value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e7577453fe345be01c38cdd6f831a74a5fe346d073dd6cdc9466a89ac5e4a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfbaa248237a0724db4811e17bbc80bb4cabc7aabf84e551aa702203abe441d(
    value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigScaled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b41702b4d358e9aff800b9c87544a2789e374f16e7a6731c29f5ca06b51725a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3529e49acba2a017f97c441e5044f31fee67b5311f5fa8d012758985c4e9893(
    value: typing.Optional[GoogleVertexAiRagEngineConfigRagManagedDbConfigUnprovisioned],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86952c407984fdbf0a8a02059d661cad6838d268888ef41a69ca700841b316e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75dbcbf99a7145810ca4f8188f52f85afd102c2c4cc5d6ada5d167140a898aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b378fc0aa4ba4122bd5b2c559d4a85c859737eef777e76c259a0fad3dd49c8ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9103f3048202dc3d90d87f4763d5cdc367510238c496ae6ae281a3cb167bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4cb64255a1bd2983c6ef22a328aaae5ebd71c153575805a6e8f511fe5e3cad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc91bcff16e2fbd15908bef30f00a34a5bc8f3c0d075782d2ac0255929e4d33f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiRagEngineConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
