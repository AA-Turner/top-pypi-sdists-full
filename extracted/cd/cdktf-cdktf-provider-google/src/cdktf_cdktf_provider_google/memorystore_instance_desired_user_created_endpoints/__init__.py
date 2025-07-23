r'''
# `google_memorystore_instance_desired_user_created_endpoints`

Refer to the Terraform Registry for docs: [`google_memorystore_instance_desired_user_created_endpoints`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints).
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


class MemorystoreInstanceDesiredUserCreatedEndpoints(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpoints",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints google_memorystore_instance_desired_user_created_endpoints}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        region: builtins.str,
        desired_user_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints google_memorystore_instance_desired_user_created_endpoints} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the Memorystore instance these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#name MemorystoreInstanceDesiredUserCreatedEndpoints#name}
        :param region: The name of the region of the Memorystore instance these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#region MemorystoreInstanceDesiredUserCreatedEndpoints#region}
        :param desired_user_created_endpoints: desired_user_created_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#desired_user_created_endpoints MemorystoreInstanceDesiredUserCreatedEndpoints#desired_user_created_endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#id MemorystoreInstanceDesiredUserCreatedEndpoints#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#project MemorystoreInstanceDesiredUserCreatedEndpoints#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#timeouts MemorystoreInstanceDesiredUserCreatedEndpoints#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db013c3cbe0d02d9a1e4053b8dc61a58cc08019af96c4e89b7df676927861a8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MemorystoreInstanceDesiredUserCreatedEndpointsConfig(
            name=name,
            region=region,
            desired_user_created_endpoints=desired_user_created_endpoints,
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
        '''Generates CDKTF code for importing a MemorystoreInstanceDesiredUserCreatedEndpoints resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MemorystoreInstanceDesiredUserCreatedEndpoints to import.
        :param import_from_id: The id of the existing MemorystoreInstanceDesiredUserCreatedEndpoints that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MemorystoreInstanceDesiredUserCreatedEndpoints to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dff2871c5b2dbb97fd2722c117a74fd32660cf118a22ff4f19bedf67e997f6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDesiredUserCreatedEndpoints")
    def put_desired_user_created_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5d31c78406f2683fef50284036397b93a8aa42e73f844884a91fbefa748ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDesiredUserCreatedEndpoints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#create MemorystoreInstanceDesiredUserCreatedEndpoints#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#delete MemorystoreInstanceDesiredUserCreatedEndpoints#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#update MemorystoreInstanceDesiredUserCreatedEndpoints#update}.
        '''
        value = MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDesiredUserCreatedEndpoints")
    def reset_desired_user_created_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredUserCreatedEndpoints", []))

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
    @jsii.member(jsii_name="desiredUserCreatedEndpoints")
    def desired_user_created_endpoints(
        self,
    ) -> "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsList":
        return typing.cast("MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsList", jsii.get(self, "desiredUserCreatedEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "MemorystoreInstanceDesiredUserCreatedEndpointsTimeoutsOutputReference":
        return typing.cast("MemorystoreInstanceDesiredUserCreatedEndpointsTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="desiredUserCreatedEndpointsInput")
    def desired_user_created_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints"]]], jsii.get(self, "desiredUserCreatedEndpointsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ccf13025f9407124d0ede076d09226fd6ea3778a62b89f581413e286d773c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dabc97fb564d9bc7d7b3c645faba5751de598c8a09eb0cfe17f90db8da948ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dd7c481b50135be38fbe2f52219a6888728be0a1a2b619e4dcb80eb7fba987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5970aea8a6f2e62d26dbd2009d2b89030b33775a3bfdf821854bd2554f69566c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsConfig",
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
        "desired_user_created_endpoints": "desiredUserCreatedEndpoints",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class MemorystoreInstanceDesiredUserCreatedEndpointsConfig(
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
        name: builtins.str,
        region: builtins.str,
        desired_user_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the Memorystore instance these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#name MemorystoreInstanceDesiredUserCreatedEndpoints#name}
        :param region: The name of the region of the Memorystore instance these endpoints should be added to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#region MemorystoreInstanceDesiredUserCreatedEndpoints#region}
        :param desired_user_created_endpoints: desired_user_created_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#desired_user_created_endpoints MemorystoreInstanceDesiredUserCreatedEndpoints#desired_user_created_endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#id MemorystoreInstanceDesiredUserCreatedEndpoints#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#project MemorystoreInstanceDesiredUserCreatedEndpoints#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#timeouts MemorystoreInstanceDesiredUserCreatedEndpoints#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6a4effb4c97c03a2a7c84829746d0cb7973ee0d1ae05c377b21cf5f39fcef7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument desired_user_created_endpoints", value=desired_user_created_endpoints, expected_type=type_hints["desired_user_created_endpoints"])
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
        if desired_user_created_endpoints is not None:
            self._values["desired_user_created_endpoints"] = desired_user_created_endpoints
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
        '''The name of the Memorystore instance these endpoints should be added to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#name MemorystoreInstanceDesiredUserCreatedEndpoints#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''The name of the region of the Memorystore instance these endpoints should be added to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#region MemorystoreInstanceDesiredUserCreatedEndpoints#region}
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def desired_user_created_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints"]]]:
        '''desired_user_created_endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#desired_user_created_endpoints MemorystoreInstanceDesiredUserCreatedEndpoints#desired_user_created_endpoints}
        '''
        result = self._values.get("desired_user_created_endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#id MemorystoreInstanceDesiredUserCreatedEndpoints#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#project MemorystoreInstanceDesiredUserCreatedEndpoints#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#timeouts MemorystoreInstanceDesiredUserCreatedEndpoints#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredUserCreatedEndpointsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints",
    jsii_struct_bases=[],
    name_mapping={"connections": "connections"},
)
class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints:
    def __init__(
        self,
        *,
        connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connections: connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#connections MemorystoreInstanceDesiredUserCreatedEndpoints#connections}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325f974ae03291b479bcb56e779769885a9652ded4a6a4fbb3cc55b94b2047c6)
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connections is not None:
            self._values["connections"] = connections

    @builtins.property
    def connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections"]]]:
        '''connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#connections MemorystoreInstanceDesiredUserCreatedEndpoints#connections}
        '''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections",
    jsii_struct_bases=[],
    name_mapping={"psc_connection": "pscConnection"},
)
class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections:
    def __init__(
        self,
        *,
        psc_connection: typing.Optional[typing.Union["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param psc_connection: psc_connection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#psc_connection MemorystoreInstanceDesiredUserCreatedEndpoints#psc_connection}
        '''
        if isinstance(psc_connection, dict):
            psc_connection = MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection(**psc_connection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa22afcbe58b05954b6d1ed09984c14b660ec121d255d4d4f65f358807ddbac)
            check_type(argname="argument psc_connection", value=psc_connection, expected_type=type_hints["psc_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if psc_connection is not None:
            self._values["psc_connection"] = psc_connection

    @builtins.property
    def psc_connection(
        self,
    ) -> typing.Optional["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection"]:
        '''psc_connection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#psc_connection MemorystoreInstanceDesiredUserCreatedEndpoints#psc_connection}
        '''
        result = self._values.get("psc_connection")
        return typing.cast(typing.Optional["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c44410ba55b5e1a8174fbb51019115373703782cf9e7b563c0b675bfc5b00f56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c63bb8b5cd50aa4c6877a65b7653bba9252e5eb30da35bccbc081dd5ed33fe5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840a7de9d0cf195fa0b8ee1a720f7b9e06b640194758e9b6740dae9fc38d5d7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78b3c0fa20ffd6da6f272df1036d9f0dd8e808c9a87c201ecf0949e714c1a81d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9929e1d4fff6abd162cd7d6303d77c17f0c1c840dd84e83492f577d388ddc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d127177fa41dafd541e92287bb58170342490fc4957043527f211d61068da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb6e94f3447dc0a31d8ee2c8ed8fec901e895460abeb5f584ad60fc644641f42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPscConnection")
    def put_psc_connection(
        self,
        *,
        forwarding_rule: builtins.str,
        ip_address: builtins.str,
        network: builtins.str,
        psc_connection_id: builtins.str,
        service_attachment: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param forwarding_rule: The URI of the consumer side forwarding rule. Format: projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#forwarding_rule MemorystoreInstanceDesiredUserCreatedEndpoints#forwarding_rule}
        :param ip_address: The IP allocated on the consumer network for the PSC forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#ip_address MemorystoreInstanceDesiredUserCreatedEndpoints#ip_address}
        :param network: The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#network MemorystoreInstanceDesiredUserCreatedEndpoints#network}
        :param psc_connection_id: The PSC connection id of the forwarding rule connected to the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#psc_connection_id MemorystoreInstanceDesiredUserCreatedEndpoints#psc_connection_id}
        :param service_attachment: The service attachment which is the target of the PSC connection, in the form of projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#service_attachment MemorystoreInstanceDesiredUserCreatedEndpoints#service_attachment}
        :param project_id: The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#project_id MemorystoreInstanceDesiredUserCreatedEndpoints#project_id}
        '''
        value = MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection(
            forwarding_rule=forwarding_rule,
            ip_address=ip_address,
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
    ) -> "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnectionOutputReference":
        return typing.cast("MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnectionOutputReference", jsii.get(self, "pscConnection"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionInput")
    def psc_connection_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection"]:
        return typing.cast(typing.Optional["MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection"], jsii.get(self, "pscConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47b90716c2c05a3d84eb9e778037858261986cd426075609e5d96ac86a7a187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection",
    jsii_struct_bases=[],
    name_mapping={
        "forwarding_rule": "forwardingRule",
        "ip_address": "ipAddress",
        "network": "network",
        "psc_connection_id": "pscConnectionId",
        "service_attachment": "serviceAttachment",
        "project_id": "projectId",
    },
)
class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection:
    def __init__(
        self,
        *,
        forwarding_rule: builtins.str,
        ip_address: builtins.str,
        network: builtins.str,
        psc_connection_id: builtins.str,
        service_attachment: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param forwarding_rule: The URI of the consumer side forwarding rule. Format: projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#forwarding_rule MemorystoreInstanceDesiredUserCreatedEndpoints#forwarding_rule}
        :param ip_address: The IP allocated on the consumer network for the PSC forwarding rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#ip_address MemorystoreInstanceDesiredUserCreatedEndpoints#ip_address}
        :param network: The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#network MemorystoreInstanceDesiredUserCreatedEndpoints#network}
        :param psc_connection_id: The PSC connection id of the forwarding rule connected to the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#psc_connection_id MemorystoreInstanceDesiredUserCreatedEndpoints#psc_connection_id}
        :param service_attachment: The service attachment which is the target of the PSC connection, in the form of projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#service_attachment MemorystoreInstanceDesiredUserCreatedEndpoints#service_attachment}
        :param project_id: The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#project_id MemorystoreInstanceDesiredUserCreatedEndpoints#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b07d0ced40f18cdefe9251fc56f367520fb456fb58cd014dc4e27a22e4ccae1)
            check_type(argname="argument forwarding_rule", value=forwarding_rule, expected_type=type_hints["forwarding_rule"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument psc_connection_id", value=psc_connection_id, expected_type=type_hints["psc_connection_id"])
            check_type(argname="argument service_attachment", value=service_attachment, expected_type=type_hints["service_attachment"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "forwarding_rule": forwarding_rule,
            "ip_address": ip_address,
            "network": network,
            "psc_connection_id": psc_connection_id,
            "service_attachment": service_attachment,
        }
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def forwarding_rule(self) -> builtins.str:
        '''The URI of the consumer side forwarding rule. Format: projects/{project}/regions/{region}/forwardingRules/{forwarding_rule}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#forwarding_rule MemorystoreInstanceDesiredUserCreatedEndpoints#forwarding_rule}
        '''
        result = self._values.get("forwarding_rule")
        assert result is not None, "Required property 'forwarding_rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''The IP allocated on the consumer network for the PSC forwarding rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#ip_address MemorystoreInstanceDesiredUserCreatedEndpoints#ip_address}
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#network MemorystoreInstanceDesiredUserCreatedEndpoints#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def psc_connection_id(self) -> builtins.str:
        '''The PSC connection id of the forwarding rule connected to the service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#psc_connection_id MemorystoreInstanceDesiredUserCreatedEndpoints#psc_connection_id}
        '''
        result = self._values.get("psc_connection_id")
        assert result is not None, "Required property 'psc_connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_attachment(self) -> builtins.str:
        '''The service attachment which is the target of the PSC connection, in the form of projects/{project-id}/regions/{region}/serviceAttachments/{service-attachment-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#service_attachment MemorystoreInstanceDesiredUserCreatedEndpoints#service_attachment}
        '''
        result = self._values.get("service_attachment")
        assert result is not None, "Required property 'service_attachment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#project_id MemorystoreInstanceDesiredUserCreatedEndpoints#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ceb9a3c179cdc8689e2b8f477802e4172211ac1381c5a55baa90e5a7cfcb51d)
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
    @jsii.member(jsii_name="forwardingRuleInput")
    def forwarding_rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardingRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

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
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @forwarding_rule.setter
    def forwarding_rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb88f6d19f140ea8a9277dfdf7b8265888bae0ad0fc3dd9232f9450d82377da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardingRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1f077b66bb7366db1dfd2d7d925b8773e64edff0a7b35bddca2dfab1215b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c7916282b3fe3953ba6c5f68a428dc97919f6963e6ba42c97f21f4143716c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb42c74af71fd2f3d7ac8d8c31533ada828226c1a4503fda2b5bebf3940fb54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @psc_connection_id.setter
    def psc_connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3b9e121d94a00b8c65776e923ebbb1bd4a58da5780a74f11762cd8bd0054fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscConnectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @service_attachment.setter
    def service_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162d05a93c95a47f699b23de6d6e5c93188d98a480694e61ff25df6a86a1571b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection]:
        return typing.cast(typing.Optional[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c438005fa2d82c729df58dc0865fafcdc8ee6c60724fdfa3a77420c76fbb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30f941b06c9bc1f384047c68e25fbf36978effcc7a234cf47b2da5671f7d2ecf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9faac445c96137a4f7caae7874169fd0a624fee425652c145cc260727f9b8225)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2aacfe82d799f78e03f1c9134f1d5830c955b0f58b11bae25bdd2fa0393076)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4d39181b6d249d3395e2fc1401746cb1b90c05958b73aeb86d528dab598b335)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd2b5308e4ad3e9efab9832a4fc688593ada48ac02e4eed1b6ae44910901075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbf4ad878afb530bfe81b236a9e93ae5bb2137cb0023f6094495427e3306261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ab807acca2a574889fe4e3a8c0a179765e6f4b9b4a398aacf251753f3a57672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnections")
    def put_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60801db6c6b26d08ff0fade57e0f59c45e5017403bd54e6469de26a0968474ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnections", [value]))

    @jsii.member(jsii_name="resetConnections")
    def reset_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnections", []))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(
        self,
    ) -> MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsList:
        return typing.cast(MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsList, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="connectionsInput")
    def connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]], jsii.get(self, "connectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecea382df2fe8685f4c153aad35319d379cf4197791ca1a2aa81403ad8ef02f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#create MemorystoreInstanceDesiredUserCreatedEndpoints#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#delete MemorystoreInstanceDesiredUserCreatedEndpoints#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#update MemorystoreInstanceDesiredUserCreatedEndpoints#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8948c56b54101ba4c76c3348b8d0d12c683c5aa7081c13f9c1c5eeae7af7ef95)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#create MemorystoreInstanceDesiredUserCreatedEndpoints#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#delete MemorystoreInstanceDesiredUserCreatedEndpoints#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance_desired_user_created_endpoints#update MemorystoreInstanceDesiredUserCreatedEndpoints#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDesiredUserCreatedEndpointsTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstanceDesiredUserCreatedEndpoints.MemorystoreInstanceDesiredUserCreatedEndpointsTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3db02fa7eb5608f27f7c6ff737428e83741b6538417b7526d3b3fbc33a17bee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c1a982b0c7c85bfbb2602fa1124d39498efcb2c40164be5f725eb56a09099b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7f1e35d2d5c95c538a4bc573086059a7bf798ee6fe86c5a3d0d3779658358b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1492a4a8c3ec7e11395ac00f800e4a3a7dca593f2eb0debbf5b7481ff3ba47ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf57fdfac52f6016ee9621188070bc229e60f4f533af39d39a1e55f1d80cc33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MemorystoreInstanceDesiredUserCreatedEndpoints",
    "MemorystoreInstanceDesiredUserCreatedEndpointsConfig",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsList",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsOutputReference",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnectionOutputReference",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsList",
    "MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsOutputReference",
    "MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts",
    "MemorystoreInstanceDesiredUserCreatedEndpointsTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__db013c3cbe0d02d9a1e4053b8dc61a58cc08019af96c4e89b7df676927861a8e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    region: builtins.str,
    desired_user_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2dff2871c5b2dbb97fd2722c117a74fd32660cf118a22ff4f19bedf67e997f6f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5d31c78406f2683fef50284036397b93a8aa42e73f844884a91fbefa748ba3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ccf13025f9407124d0ede076d09226fd6ea3778a62b89f581413e286d773c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dabc97fb564d9bc7d7b3c645faba5751de598c8a09eb0cfe17f90db8da948ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dd7c481b50135be38fbe2f52219a6888728be0a1a2b619e4dcb80eb7fba987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5970aea8a6f2e62d26dbd2009d2b89030b33775a3bfdf821854bd2554f69566c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6a4effb4c97c03a2a7c84829746d0cb7973ee0d1ae05c377b21cf5f39fcef7(
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
    desired_user_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325f974ae03291b479bcb56e779769885a9652ded4a6a4fbb3cc55b94b2047c6(
    *,
    connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa22afcbe58b05954b6d1ed09984c14b660ec121d255d4d4f65f358807ddbac(
    *,
    psc_connection: typing.Optional[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44410ba55b5e1a8174fbb51019115373703782cf9e7b563c0b675bfc5b00f56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c63bb8b5cd50aa4c6877a65b7653bba9252e5eb30da35bccbc081dd5ed33fe5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840a7de9d0cf195fa0b8ee1a720f7b9e06b640194758e9b6740dae9fc38d5d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b3c0fa20ffd6da6f272df1036d9f0dd8e808c9a87c201ecf0949e714c1a81d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9929e1d4fff6abd162cd7d6303d77c17f0c1c840dd84e83492f577d388ddc01(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d127177fa41dafd541e92287bb58170342490fc4957043527f211d61068da0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6e94f3447dc0a31d8ee2c8ed8fec901e895460abeb5f584ad60fc644641f42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47b90716c2c05a3d84eb9e778037858261986cd426075609e5d96ac86a7a187(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b07d0ced40f18cdefe9251fc56f367520fb456fb58cd014dc4e27a22e4ccae1(
    *,
    forwarding_rule: builtins.str,
    ip_address: builtins.str,
    network: builtins.str,
    psc_connection_id: builtins.str,
    service_attachment: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ceb9a3c179cdc8689e2b8f477802e4172211ac1381c5a55baa90e5a7cfcb51d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb88f6d19f140ea8a9277dfdf7b8265888bae0ad0fc3dd9232f9450d82377da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1f077b66bb7366db1dfd2d7d925b8773e64edff0a7b35bddca2dfab1215b1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c7916282b3fe3953ba6c5f68a428dc97919f6963e6ba42c97f21f4143716c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb42c74af71fd2f3d7ac8d8c31533ada828226c1a4503fda2b5bebf3940fb54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3b9e121d94a00b8c65776e923ebbb1bd4a58da5780a74f11762cd8bd0054fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162d05a93c95a47f699b23de6d6e5c93188d98a480694e61ff25df6a86a1571b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c438005fa2d82c729df58dc0865fafcdc8ee6c60724fdfa3a77420c76fbb3b(
    value: typing.Optional[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnectionsPscConnection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f941b06c9bc1f384047c68e25fbf36978effcc7a234cf47b2da5671f7d2ecf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faac445c96137a4f7caae7874169fd0a624fee425652c145cc260727f9b8225(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2aacfe82d799f78e03f1c9134f1d5830c955b0f58b11bae25bdd2fa0393076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d39181b6d249d3395e2fc1401746cb1b90c05958b73aeb86d528dab598b335(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd2b5308e4ad3e9efab9832a4fc688593ada48ac02e4eed1b6ae44910901075(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbf4ad878afb530bfe81b236a9e93ae5bb2137cb0023f6094495427e3306261(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab807acca2a574889fe4e3a8c0a179765e6f4b9b4a398aacf251753f3a57672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60801db6c6b26d08ff0fade57e0f59c45e5017403bd54e6469de26a0968474ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpointsConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecea382df2fe8685f4c153aad35319d379cf4197791ca1a2aa81403ad8ef02f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsDesiredUserCreatedEndpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8948c56b54101ba4c76c3348b8d0d12c683c5aa7081c13f9c1c5eeae7af7ef95(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3db02fa7eb5608f27f7c6ff737428e83741b6538417b7526d3b3fbc33a17bee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1a982b0c7c85bfbb2602fa1124d39498efcb2c40164be5f725eb56a09099b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7f1e35d2d5c95c538a4bc573086059a7bf798ee6fe86c5a3d0d3779658358b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1492a4a8c3ec7e11395ac00f800e4a3a7dca593f2eb0debbf5b7481ff3ba47ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf57fdfac52f6016ee9621188070bc229e60f4f533af39d39a1e55f1d80cc33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredUserCreatedEndpointsTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
