r'''
# `google_tpu_v2_queued_resource`

Refer to the Terraform Registry for docs: [`google_tpu_v2_queued_resource`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource).
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


class GoogleTpuV2QueuedResource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource google_tpu_v2_queued_resource}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleTpuV2QueuedResourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tpu: typing.Optional[typing.Union["GoogleTpuV2QueuedResourceTpu", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource google_tpu_v2_queued_resource} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The immutable name of the Queued Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#name GoogleTpuV2QueuedResource#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#id GoogleTpuV2QueuedResource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#project GoogleTpuV2QueuedResource#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#timeouts GoogleTpuV2QueuedResource#timeouts}
        :param tpu: tpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#tpu GoogleTpuV2QueuedResource#tpu}
        :param zone: The GCP location for the Queued Resource. If it is not provided, the provider zone is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#zone GoogleTpuV2QueuedResource#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c2dcfcdfb37792f77a5322b323b54d5e62d77207189c98b3f58bfdb6dd6953)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleTpuV2QueuedResourceConfig(
            name=name,
            id=id,
            project=project,
            timeouts=timeouts,
            tpu=tpu,
            zone=zone,
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
        '''Generates CDKTF code for importing a GoogleTpuV2QueuedResource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleTpuV2QueuedResource to import.
        :param import_from_id: The id of the existing GoogleTpuV2QueuedResource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleTpuV2QueuedResource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33dc4ef8ca9baf6382a01649da60a68b3059f6ea1452c449c37698c7fdc53210)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#create GoogleTpuV2QueuedResource#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#delete GoogleTpuV2QueuedResource#delete}.
        '''
        value = GoogleTpuV2QueuedResourceTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTpu")
    def put_tpu(
        self,
        *,
        node_spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTpuV2QueuedResourceTpuNodeSpec", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param node_spec: node_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node_spec GoogleTpuV2QueuedResource#node_spec}
        '''
        value = GoogleTpuV2QueuedResourceTpu(node_spec=node_spec)

        return typing.cast(None, jsii.invoke(self, "putTpu", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTpu")
    def reset_tpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpu", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleTpuV2QueuedResourceTimeoutsOutputReference":
        return typing.cast("GoogleTpuV2QueuedResourceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="tpu")
    def tpu(self) -> "GoogleTpuV2QueuedResourceTpuOutputReference":
        return typing.cast("GoogleTpuV2QueuedResourceTpuOutputReference", jsii.get(self, "tpu"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleTpuV2QueuedResourceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleTpuV2QueuedResourceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="tpuInput")
    def tpu_input(self) -> typing.Optional["GoogleTpuV2QueuedResourceTpu"]:
        return typing.cast(typing.Optional["GoogleTpuV2QueuedResourceTpu"], jsii.get(self, "tpuInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83124ca4bd9c9b6c7d582c038cfefb7076c9487f680c7cdcb60cf784d71d1968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9bf127f7a9b597840479753d27301c019090dc15d02924f5a5037c4c4f11f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4db3bdaf58fb8365d0f9550be2f5a1f09ff1114252ba331b7cc7cc17818277e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6545fa9971cd14d70333f6518fd770acf88720e618facc0f1fa0aad593f7499e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceConfig",
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
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
        "tpu": "tpu",
        "zone": "zone",
    },
)
class GoogleTpuV2QueuedResourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleTpuV2QueuedResourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        tpu: typing.Optional[typing.Union["GoogleTpuV2QueuedResourceTpu", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The immutable name of the Queued Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#name GoogleTpuV2QueuedResource#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#id GoogleTpuV2QueuedResource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#project GoogleTpuV2QueuedResource#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#timeouts GoogleTpuV2QueuedResource#timeouts}
        :param tpu: tpu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#tpu GoogleTpuV2QueuedResource#tpu}
        :param zone: The GCP location for the Queued Resource. If it is not provided, the provider zone is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#zone GoogleTpuV2QueuedResource#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleTpuV2QueuedResourceTimeouts(**timeouts)
        if isinstance(tpu, dict):
            tpu = GoogleTpuV2QueuedResourceTpu(**tpu)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d2b09d2426cf6a93c24fbe5feab7a2639521c1289e275271fd6ed3d6432f0a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument tpu", value=tpu, expected_type=type_hints["tpu"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if tpu is not None:
            self._values["tpu"] = tpu
        if zone is not None:
            self._values["zone"] = zone

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
        '''The immutable name of the Queued Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#name GoogleTpuV2QueuedResource#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#id GoogleTpuV2QueuedResource#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#project GoogleTpuV2QueuedResource#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleTpuV2QueuedResourceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#timeouts GoogleTpuV2QueuedResource#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleTpuV2QueuedResourceTimeouts"], result)

    @builtins.property
    def tpu(self) -> typing.Optional["GoogleTpuV2QueuedResourceTpu"]:
        '''tpu block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#tpu GoogleTpuV2QueuedResource#tpu}
        '''
        result = self._values.get("tpu")
        return typing.cast(typing.Optional["GoogleTpuV2QueuedResourceTpu"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The GCP location for the Queued Resource. If it is not provided, the provider zone is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#zone GoogleTpuV2QueuedResource#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTpuV2QueuedResourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleTpuV2QueuedResourceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#create GoogleTpuV2QueuedResource#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#delete GoogleTpuV2QueuedResource#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e18206be6430ffc8a83fede9fd1f00c9ff734f9ef5aa2ec789af25741765ee)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#create GoogleTpuV2QueuedResource#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#delete GoogleTpuV2QueuedResource#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTpuV2QueuedResourceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTpuV2QueuedResourceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c7f1e95233cfa5b3f6cd793ba0844dc548f05972ef245161b7a2c49ee53cebf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccd10c34a70933c60523ac67f36305d6bda44120af34bba6cfd9919277faf605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0f5c0ba0305e5457c90d1968cb73f7e3ffccfe493404ffd10162893d6f11c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c7945e56cae2e900da64b71bb89915d6f9473e86ede8dce8ddd8e03e9a23db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpu",
    jsii_struct_bases=[],
    name_mapping={"node_spec": "nodeSpec"},
)
class GoogleTpuV2QueuedResourceTpu:
    def __init__(
        self,
        *,
        node_spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleTpuV2QueuedResourceTpuNodeSpec", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param node_spec: node_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node_spec GoogleTpuV2QueuedResource#node_spec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b7f50fbc55e22085165ee0187ef9b97caf716c59594460bb52f4f8c4a2defb)
            check_type(argname="argument node_spec", value=node_spec, expected_type=type_hints["node_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_spec is not None:
            self._values["node_spec"] = node_spec

    @builtins.property
    def node_spec(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTpuV2QueuedResourceTpuNodeSpec"]]]:
        '''node_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node_spec GoogleTpuV2QueuedResource#node_spec}
        '''
        result = self._values.get("node_spec")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleTpuV2QueuedResourceTpuNodeSpec"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTpuV2QueuedResourceTpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpec",
    jsii_struct_bases=[],
    name_mapping={
        "node_attribute": "nodeAttribute",
        "parent": "parent",
        "node_id": "nodeId",
    },
)
class GoogleTpuV2QueuedResourceTpuNodeSpec:
    def __init__(
        self,
        *,
        node_attribute: typing.Union["GoogleTpuV2QueuedResourceTpuNodeSpecNode", typing.Dict[builtins.str, typing.Any]],
        parent: builtins.str,
        node_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param node_attribute: node block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node GoogleTpuV2QueuedResource#node}
        :param parent: The parent resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#parent GoogleTpuV2QueuedResource#parent}
        :param node_id: Unqualified node identifier used to identify the node in the project once provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node_id GoogleTpuV2QueuedResource#node_id}
        '''
        if isinstance(node_attribute, dict):
            node_attribute = GoogleTpuV2QueuedResourceTpuNodeSpecNode(**node_attribute)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d60d0c3b14c68010df4cb24e0e82d9851daabde7ae9e648598f50e90a63a03b)
            check_type(argname="argument node_attribute", value=node_attribute, expected_type=type_hints["node_attribute"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument node_id", value=node_id, expected_type=type_hints["node_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_attribute": node_attribute,
            "parent": parent,
        }
        if node_id is not None:
            self._values["node_id"] = node_id

    @builtins.property
    def node_attribute(self) -> "GoogleTpuV2QueuedResourceTpuNodeSpecNode":
        '''node block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node GoogleTpuV2QueuedResource#node}
        '''
        result = self._values.get("node_attribute")
        assert result is not None, "Required property 'node_attribute' is missing"
        return typing.cast("GoogleTpuV2QueuedResourceTpuNodeSpecNode", result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''The parent resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#parent GoogleTpuV2QueuedResource#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_id(self) -> typing.Optional[builtins.str]:
        '''Unqualified node identifier used to identify the node in the project once provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#node_id GoogleTpuV2QueuedResource#node_id}
        '''
        result = self._values.get("node_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTpuV2QueuedResourceTpuNodeSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTpuV2QueuedResourceTpuNodeSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b4c22e35e7e0b9f6975838ea71a5ddadb6d43973445fd2c9b4f638d517f3854)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleTpuV2QueuedResourceTpuNodeSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952babd4fe7dbf2ad8327dd167e73a768dbe591be06483ca2649befd19d2713b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleTpuV2QueuedResourceTpuNodeSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88296fe6c597709fa96ff037c13ba3e0fac1acf044c5b4998bfb25cb6efb98ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8542291308f0b06d7eadb86c259f797f68bf3ef68a45de45c19180677b955a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9cab410544d2fd46abe1cc3fb2bb8ae9ea2b851dfc21f8fcba9c972fd8ac70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTpuV2QueuedResourceTpuNodeSpec]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTpuV2QueuedResourceTpuNodeSpec]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTpuV2QueuedResourceTpuNodeSpec]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d9038c9afc8d6f90ac6c59fec4f9216ccbe9ff0fb9caf3ca52f0e40fbb0ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpecNode",
    jsii_struct_bases=[],
    name_mapping={
        "runtime_version": "runtimeVersion",
        "accelerator_type": "acceleratorType",
        "description": "description",
        "network_config": "networkConfig",
    },
)
class GoogleTpuV2QueuedResourceTpuNodeSpecNode:
    def __init__(
        self,
        *,
        runtime_version: builtins.str,
        accelerator_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union["GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param runtime_version: Runtime version for the TPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#runtime_version GoogleTpuV2QueuedResource#runtime_version}
        :param accelerator_type: TPU accelerator type for the TPU. If not specified, this defaults to 'v2-8'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#accelerator_type GoogleTpuV2QueuedResource#accelerator_type}
        :param description: Text description of the TPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#description GoogleTpuV2QueuedResource#description}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#network_config GoogleTpuV2QueuedResource#network_config}
        '''
        if isinstance(network_config, dict):
            network_config = GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig(**network_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bf7bff85939a3226cf3e9549bed903c220604fb4bd65031c930367dba6824a)
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "runtime_version": runtime_version,
        }
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if description is not None:
            self._values["description"] = description
        if network_config is not None:
            self._values["network_config"] = network_config

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''Runtime version for the TPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#runtime_version GoogleTpuV2QueuedResource#runtime_version}
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''TPU accelerator type for the TPU. If not specified, this defaults to 'v2-8'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#accelerator_type GoogleTpuV2QueuedResource#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Text description of the TPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#description GoogleTpuV2QueuedResource#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_config(
        self,
    ) -> typing.Optional["GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#network_config GoogleTpuV2QueuedResource#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTpuV2QueuedResourceTpuNodeSpecNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "can_ip_forward": "canIpForward",
        "enable_external_ips": "enableExternalIps",
        "network": "network",
        "queue_count": "queueCount",
        "subnetwork": "subnetwork",
    },
)
class GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig:
    def __init__(
        self,
        *,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_external_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network: typing.Optional[builtins.str] = None,
        queue_count: typing.Optional[jsii.Number] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param can_ip_forward: Allows the TPU node to send and receive packets with non-matching destination or source IPs. This is required if you plan to use the TPU workers to forward routes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#can_ip_forward GoogleTpuV2QueuedResource#can_ip_forward}
        :param enable_external_ips: Indicates that external IP addresses would be associated with the TPU workers. If set to false, the specified subnetwork or network should have Private Google Access enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#enable_external_ips GoogleTpuV2QueuedResource#enable_external_ips}
        :param network: The name of the network for the TPU node. It must be a preexisting Google Compute Engine network. If none is provided, "default" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#network GoogleTpuV2QueuedResource#network}
        :param queue_count: Specifies networking queue count for TPU VM instance's network interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#queue_count GoogleTpuV2QueuedResource#queue_count}
        :param subnetwork: The name of the subnetwork for the TPU node. It must be a preexisting Google Compute Engine subnetwork. If none is provided, "default" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#subnetwork GoogleTpuV2QueuedResource#subnetwork}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad00f7bde3607fe6b853048c6fcf3a71307de169dee2240e1c86d6d29c2fe85)
            check_type(argname="argument can_ip_forward", value=can_ip_forward, expected_type=type_hints["can_ip_forward"])
            check_type(argname="argument enable_external_ips", value=enable_external_ips, expected_type=type_hints["enable_external_ips"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument queue_count", value=queue_count, expected_type=type_hints["queue_count"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if can_ip_forward is not None:
            self._values["can_ip_forward"] = can_ip_forward
        if enable_external_ips is not None:
            self._values["enable_external_ips"] = enable_external_ips
        if network is not None:
            self._values["network"] = network
        if queue_count is not None:
            self._values["queue_count"] = queue_count
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork

    @builtins.property
    def can_ip_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows the TPU node to send and receive packets with non-matching destination or source IPs.

        This is required if you plan to use the TPU workers to forward routes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#can_ip_forward GoogleTpuV2QueuedResource#can_ip_forward}
        '''
        result = self._values.get("can_ip_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_external_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that external IP addresses would be associated with the TPU workers.

        If set to
        false, the specified subnetwork or network should have Private Google Access enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#enable_external_ips GoogleTpuV2QueuedResource#enable_external_ips}
        '''
        result = self._values.get("enable_external_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name of the network for the TPU node.

        It must be a preexisting Google Compute Engine
        network. If none is provided, "default" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#network GoogleTpuV2QueuedResource#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies networking queue count for TPU VM instance's network interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#queue_count GoogleTpuV2QueuedResource#queue_count}
        '''
        result = self._values.get("queue_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name of the subnetwork for the TPU node.

        It must be a preexisting Google Compute
        Engine subnetwork. If none is provided, "default" will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#subnetwork GoogleTpuV2QueuedResource#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a03d32eedeb725b460fa6b89d1f013277cb8f04d83ea7acc4086252fd4b37ebd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCanIpForward")
    def reset_can_ip_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanIpForward", []))

    @jsii.member(jsii_name="resetEnableExternalIps")
    def reset_enable_external_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableExternalIps", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetQueueCount")
    def reset_queue_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueCount", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @builtins.property
    @jsii.member(jsii_name="canIpForwardInput")
    def can_ip_forward_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canIpForwardInput"))

    @builtins.property
    @jsii.member(jsii_name="enableExternalIpsInput")
    def enable_external_ips_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableExternalIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="queueCountInput")
    def queue_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queueCountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="canIpForward")
    def can_ip_forward(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canIpForward"))

    @can_ip_forward.setter
    def can_ip_forward(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d64e79d9e3fbf60767dea41b904578c4c4670ccb9efaa5e33d24605ee3de044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canIpForward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableExternalIps")
    def enable_external_ips(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableExternalIps"))

    @enable_external_ips.setter
    def enable_external_ips(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e087fe8053e44d8b58c01f43881cb8c8d5042741052f1bfc4a863de6c31b0acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableExternalIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cf07c38efe1ecaba4530a9d0827854f9e708e981d79602a69851e4ec60f6a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueCount")
    def queue_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueCount"))

    @queue_count.setter
    def queue_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257359153a2c935b5897140c3416ba55cbe81dfbf6b219561a427281cd2f9922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b0b0dcc6ab3e45a60d9a98419c5c6e540743681d3858d91980a6e7cdf3d96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig]:
        return typing.cast(typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f813aaa303a02f3bc58645f911380ff146bab26df34fec3e35095a15bf6b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTpuV2QueuedResourceTpuNodeSpecNodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpecNodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8383756612a12579cb432bffd5d16d6cc6038886d62c03355aa091ff62cffd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_external_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network: typing.Optional[builtins.str] = None,
        queue_count: typing.Optional[jsii.Number] = None,
        subnetwork: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param can_ip_forward: Allows the TPU node to send and receive packets with non-matching destination or source IPs. This is required if you plan to use the TPU workers to forward routes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#can_ip_forward GoogleTpuV2QueuedResource#can_ip_forward}
        :param enable_external_ips: Indicates that external IP addresses would be associated with the TPU workers. If set to false, the specified subnetwork or network should have Private Google Access enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#enable_external_ips GoogleTpuV2QueuedResource#enable_external_ips}
        :param network: The name of the network for the TPU node. It must be a preexisting Google Compute Engine network. If none is provided, "default" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#network GoogleTpuV2QueuedResource#network}
        :param queue_count: Specifies networking queue count for TPU VM instance's network interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#queue_count GoogleTpuV2QueuedResource#queue_count}
        :param subnetwork: The name of the subnetwork for the TPU node. It must be a preexisting Google Compute Engine subnetwork. If none is provided, "default" will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#subnetwork GoogleTpuV2QueuedResource#subnetwork}
        '''
        value = GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig(
            can_ip_forward=can_ip_forward,
            enable_external_ips=enable_external_ips,
            network=network,
            queue_count=queue_count,
            subnetwork=subnetwork,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(
        self,
    ) -> GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfigOutputReference:
        return typing.cast(GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfigOutputReference, jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig]:
        return typing.cast(typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123934c33ae96f2e2cc76b9246fcbfede68a26c0650925e6013de8abec5db55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08118afe7362b09afb8de87a06d9ef3f662d420483e9e4e6d52a66e556be444e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762b20ddbe993496b9352abd0b3098314835dd2c568a3b566863f122e424c31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNode]:
        return typing.cast(typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328c5525756032fdb6836918c7ac1c8ceec3ed9b79330dd71870101affc170b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTpuV2QueuedResourceTpuNodeSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuNodeSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b7cd2418fe95869f7bb70b7e3548de3b1650a72293acfc2fd2495a297423fab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNodeAttribute")
    def put_node_attribute(
        self,
        *,
        runtime_version: builtins.str,
        accelerator_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        network_config: typing.Optional[typing.Union[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param runtime_version: Runtime version for the TPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#runtime_version GoogleTpuV2QueuedResource#runtime_version}
        :param accelerator_type: TPU accelerator type for the TPU. If not specified, this defaults to 'v2-8'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#accelerator_type GoogleTpuV2QueuedResource#accelerator_type}
        :param description: Text description of the TPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#description GoogleTpuV2QueuedResource#description}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_tpu_v2_queued_resource#network_config GoogleTpuV2QueuedResource#network_config}
        '''
        value = GoogleTpuV2QueuedResourceTpuNodeSpecNode(
            runtime_version=runtime_version,
            accelerator_type=accelerator_type,
            description=description,
            network_config=network_config,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeAttribute", [value]))

    @jsii.member(jsii_name="resetNodeId")
    def reset_node_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeId", []))

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> GoogleTpuV2QueuedResourceTpuNodeSpecNodeOutputReference:
        return typing.cast(GoogleTpuV2QueuedResourceTpuNodeSpecNodeOutputReference, jsii.get(self, "nodeAttribute"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttributeInput")
    def node_attribute_input(
        self,
    ) -> typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNode]:
        return typing.cast(typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNode], jsii.get(self, "nodeAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeIdInput")
    def node_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @node_id.setter
    def node_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4595f790d6bd006583563a3a8eec60132df527e0a1d47aaa389275ec5a33eaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d5af04440c13f32fa4531218c23a9cd5991d6a283213d8722a9b3468a1c97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTpuNodeSpec]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTpuNodeSpec]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTpuNodeSpec]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d115b8a543d01030a3b3ac9809c80c7f2710b4d09f747ac42d407a1a838c5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleTpuV2QueuedResourceTpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleTpuV2QueuedResource.GoogleTpuV2QueuedResourceTpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13d11a4c51782e26a40f26321ae961ac4454ec38176d2a8be0f6c8971da85ce6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeSpec")
    def put_node_spec(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTpuV2QueuedResourceTpuNodeSpec, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d2b1a9bde1b4a5da6e59e79f8a03c014c5543b18f8c565fd53b2644e4b7e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeSpec", [value]))

    @jsii.member(jsii_name="resetNodeSpec")
    def reset_node_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSpec", []))

    @builtins.property
    @jsii.member(jsii_name="nodeSpec")
    def node_spec(self) -> GoogleTpuV2QueuedResourceTpuNodeSpecList:
        return typing.cast(GoogleTpuV2QueuedResourceTpuNodeSpecList, jsii.get(self, "nodeSpec"))

    @builtins.property
    @jsii.member(jsii_name="nodeSpecInput")
    def node_spec_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTpuV2QueuedResourceTpuNodeSpec]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTpuV2QueuedResourceTpuNodeSpec]]], jsii.get(self, "nodeSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleTpuV2QueuedResourceTpu]:
        return typing.cast(typing.Optional[GoogleTpuV2QueuedResourceTpu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleTpuV2QueuedResourceTpu],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5fac241acc227e543d5267d05c5a085b443e3f1ccc48c49bd4a6cb74866a48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleTpuV2QueuedResource",
    "GoogleTpuV2QueuedResourceConfig",
    "GoogleTpuV2QueuedResourceTimeouts",
    "GoogleTpuV2QueuedResourceTimeoutsOutputReference",
    "GoogleTpuV2QueuedResourceTpu",
    "GoogleTpuV2QueuedResourceTpuNodeSpec",
    "GoogleTpuV2QueuedResourceTpuNodeSpecList",
    "GoogleTpuV2QueuedResourceTpuNodeSpecNode",
    "GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig",
    "GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfigOutputReference",
    "GoogleTpuV2QueuedResourceTpuNodeSpecNodeOutputReference",
    "GoogleTpuV2QueuedResourceTpuNodeSpecOutputReference",
    "GoogleTpuV2QueuedResourceTpuOutputReference",
]

publication.publish()

def _typecheckingstub__20c2dcfcdfb37792f77a5322b323b54d5e62d77207189c98b3f58bfdb6dd6953(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleTpuV2QueuedResourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tpu: typing.Optional[typing.Union[GoogleTpuV2QueuedResourceTpu, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__33dc4ef8ca9baf6382a01649da60a68b3059f6ea1452c449c37698c7fdc53210(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83124ca4bd9c9b6c7d582c038cfefb7076c9487f680c7cdcb60cf784d71d1968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9bf127f7a9b597840479753d27301c019090dc15d02924f5a5037c4c4f11f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4db3bdaf58fb8365d0f9550be2f5a1f09ff1114252ba331b7cc7cc17818277e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6545fa9971cd14d70333f6518fd770acf88720e618facc0f1fa0aad593f7499e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d2b09d2426cf6a93c24fbe5feab7a2639521c1289e275271fd6ed3d6432f0a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleTpuV2QueuedResourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    tpu: typing.Optional[typing.Union[GoogleTpuV2QueuedResourceTpu, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e18206be6430ffc8a83fede9fd1f00c9ff734f9ef5aa2ec789af25741765ee(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7f1e95233cfa5b3f6cd793ba0844dc548f05972ef245161b7a2c49ee53cebf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd10c34a70933c60523ac67f36305d6bda44120af34bba6cfd9919277faf605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0f5c0ba0305e5457c90d1968cb73f7e3ffccfe493404ffd10162893d6f11c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c7945e56cae2e900da64b71bb89915d6f9473e86ede8dce8ddd8e03e9a23db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b7f50fbc55e22085165ee0187ef9b97caf716c59594460bb52f4f8c4a2defb(
    *,
    node_spec: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTpuV2QueuedResourceTpuNodeSpec, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d60d0c3b14c68010df4cb24e0e82d9851daabde7ae9e648598f50e90a63a03b(
    *,
    node_attribute: typing.Union[GoogleTpuV2QueuedResourceTpuNodeSpecNode, typing.Dict[builtins.str, typing.Any]],
    parent: builtins.str,
    node_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4c22e35e7e0b9f6975838ea71a5ddadb6d43973445fd2c9b4f638d517f3854(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952babd4fe7dbf2ad8327dd167e73a768dbe591be06483ca2649befd19d2713b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88296fe6c597709fa96ff037c13ba3e0fac1acf044c5b4998bfb25cb6efb98ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8542291308f0b06d7eadb86c259f797f68bf3ef68a45de45c19180677b955a6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cab410544d2fd46abe1cc3fb2bb8ae9ea2b851dfc21f8fcba9c972fd8ac70d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d9038c9afc8d6f90ac6c59fec4f9216ccbe9ff0fb9caf3ca52f0e40fbb0ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleTpuV2QueuedResourceTpuNodeSpec]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bf7bff85939a3226cf3e9549bed903c220604fb4bd65031c930367dba6824a(
    *,
    runtime_version: builtins.str,
    accelerator_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    network_config: typing.Optional[typing.Union[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad00f7bde3607fe6b853048c6fcf3a71307de169dee2240e1c86d6d29c2fe85(
    *,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_external_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network: typing.Optional[builtins.str] = None,
    queue_count: typing.Optional[jsii.Number] = None,
    subnetwork: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03d32eedeb725b460fa6b89d1f013277cb8f04d83ea7acc4086252fd4b37ebd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d64e79d9e3fbf60767dea41b904578c4c4670ccb9efaa5e33d24605ee3de044(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e087fe8053e44d8b58c01f43881cb8c8d5042741052f1bfc4a863de6c31b0acb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cf07c38efe1ecaba4530a9d0827854f9e708e981d79602a69851e4ec60f6a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257359153a2c935b5897140c3416ba55cbe81dfbf6b219561a427281cd2f9922(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b0b0dcc6ab3e45a60d9a98419c5c6e540743681d3858d91980a6e7cdf3d96f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f813aaa303a02f3bc58645f911380ff146bab26df34fec3e35095a15bf6b22(
    value: typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNodeNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8383756612a12579cb432bffd5d16d6cc6038886d62c03355aa091ff62cffd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123934c33ae96f2e2cc76b9246fcbfede68a26c0650925e6013de8abec5db55c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08118afe7362b09afb8de87a06d9ef3f662d420483e9e4e6d52a66e556be444e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762b20ddbe993496b9352abd0b3098314835dd2c568a3b566863f122e424c31b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328c5525756032fdb6836918c7ac1c8ceec3ed9b79330dd71870101affc170b9(
    value: typing.Optional[GoogleTpuV2QueuedResourceTpuNodeSpecNode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7cd2418fe95869f7bb70b7e3548de3b1650a72293acfc2fd2495a297423fab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4595f790d6bd006583563a3a8eec60132df527e0a1d47aaa389275ec5a33eaef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d5af04440c13f32fa4531218c23a9cd5991d6a283213d8722a9b3468a1c97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d115b8a543d01030a3b3ac9809c80c7f2710b4d09f747ac42d407a1a838c5e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleTpuV2QueuedResourceTpuNodeSpec]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d11a4c51782e26a40f26321ae961ac4454ec38176d2a8be0f6c8971da85ce6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d2b1a9bde1b4a5da6e59e79f8a03c014c5543b18f8c565fd53b2644e4b7e93(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleTpuV2QueuedResourceTpuNodeSpec, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fac241acc227e543d5267d05c5a085b443e3f1ccc48c49bd4a6cb74866a48a(
    value: typing.Optional[GoogleTpuV2QueuedResourceTpu],
) -> None:
    """Type checking stubs"""
    pass
