r'''
# `google_firebase_app_hosting_domain`

Refer to the Terraform Registry for docs: [`google_firebase_app_hosting_domain`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain).
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


class FirebaseAppHostingDomain(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomain",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain google_firebase_app_hosting_domain}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backend: builtins.str,
        domain_id: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        serve: typing.Optional[typing.Union["FirebaseAppHostingDomainServe", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FirebaseAppHostingDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain google_firebase_app_hosting_domain} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backend: The ID of the Backend that this Domain is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#backend FirebaseAppHostingDomain#backend}
        :param domain_id: Id of the domain to create. Must be a valid domain name, such as "foo.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#domain_id FirebaseAppHostingDomain#domain_id}
        :param location: The location of the Backend that this Domain is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#location FirebaseAppHostingDomain#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#id FirebaseAppHostingDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#project FirebaseAppHostingDomain#project}.
        :param serve: serve block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#serve FirebaseAppHostingDomain#serve}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#timeouts FirebaseAppHostingDomain#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de86a9c3085a22321613c4d1ae9ffb1cb735c212f6adb8d2b275bcedc8b7df68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FirebaseAppHostingDomainConfig(
            backend=backend,
            domain_id=domain_id,
            location=location,
            id=id,
            project=project,
            serve=serve,
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
        '''Generates CDKTF code for importing a FirebaseAppHostingDomain resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FirebaseAppHostingDomain to import.
        :param import_from_id: The id of the existing FirebaseAppHostingDomain that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FirebaseAppHostingDomain to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b12a48d04cc9f870843aa071a37b1ae123e13b2d3dd0ab3e76af9cee7e2f8a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServe")
    def put_serve(
        self,
        *,
        redirect: typing.Optional[typing.Union["FirebaseAppHostingDomainServeRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#redirect FirebaseAppHostingDomain#redirect}
        '''
        value = FirebaseAppHostingDomainServe(redirect=redirect)

        return typing.cast(None, jsii.invoke(self, "putServe", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#create FirebaseAppHostingDomain#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#delete FirebaseAppHostingDomain#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#update FirebaseAppHostingDomain#update}.
        '''
        value = FirebaseAppHostingDomainTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServe")
    def reset_serve(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServe", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="customDomainStatus")
    def custom_domain_status(self) -> "FirebaseAppHostingDomainCustomDomainStatusList":
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusList", jsii.get(self, "customDomainStatus"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="purgeTime")
    def purge_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purgeTime"))

    @builtins.property
    @jsii.member(jsii_name="serve")
    def serve(self) -> "FirebaseAppHostingDomainServeOutputReference":
        return typing.cast("FirebaseAppHostingDomainServeOutputReference", jsii.get(self, "serve"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FirebaseAppHostingDomainTimeoutsOutputReference":
        return typing.cast("FirebaseAppHostingDomainTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="backendInput")
    def backend_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backendInput"))

    @builtins.property
    @jsii.member(jsii_name="domainIdInput")
    def domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serveInput")
    def serve_input(self) -> typing.Optional["FirebaseAppHostingDomainServe"]:
        return typing.cast(typing.Optional["FirebaseAppHostingDomainServe"], jsii.get(self, "serveInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirebaseAppHostingDomainTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirebaseAppHostingDomainTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backend")
    def backend(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backend"))

    @backend.setter
    def backend(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26487bf7d430edee8dc52f2f8adba010b8d8df2d567a9dc0eff11fdcb9a9c23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @domain_id.setter
    def domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e82911f509fbab24ca640a8fc04330a3e3182b7ba631e631c42a6ce8fd42b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ce7a92dd767ac9652ae9753f244df61d7b39cfc1451c06aaabba8dd5982be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73709549da2dcf3feb276c5e734c9b3c288b94ef8bcc6d3758a4faea832ef111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbdbdb2bb341f58b391d021dda6f95e7cd6ff4c6040e0b0e5faad075b8af5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backend": "backend",
        "domain_id": "domainId",
        "location": "location",
        "id": "id",
        "project": "project",
        "serve": "serve",
        "timeouts": "timeouts",
    },
)
class FirebaseAppHostingDomainConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backend: builtins.str,
        domain_id: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        serve: typing.Optional[typing.Union["FirebaseAppHostingDomainServe", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FirebaseAppHostingDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backend: The ID of the Backend that this Domain is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#backend FirebaseAppHostingDomain#backend}
        :param domain_id: Id of the domain to create. Must be a valid domain name, such as "foo.com". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#domain_id FirebaseAppHostingDomain#domain_id}
        :param location: The location of the Backend that this Domain is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#location FirebaseAppHostingDomain#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#id FirebaseAppHostingDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#project FirebaseAppHostingDomain#project}.
        :param serve: serve block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#serve FirebaseAppHostingDomain#serve}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#timeouts FirebaseAppHostingDomain#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(serve, dict):
            serve = FirebaseAppHostingDomainServe(**serve)
        if isinstance(timeouts, dict):
            timeouts = FirebaseAppHostingDomainTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9492ec781d67247a7c46a207474af15662f41d6a38228f2d8734c89aa27bc763)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument serve", value=serve, expected_type=type_hints["serve"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend": backend,
            "domain_id": domain_id,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if serve is not None:
            self._values["serve"] = serve
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
    def backend(self) -> builtins.str:
        '''The ID of the Backend that this Domain is associated with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#backend FirebaseAppHostingDomain#backend}
        '''
        result = self._values.get("backend")
        assert result is not None, "Required property 'backend' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_id(self) -> builtins.str:
        '''Id of the domain to create. Must be a valid domain name, such as "foo.com".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#domain_id FirebaseAppHostingDomain#domain_id}
        '''
        result = self._values.get("domain_id")
        assert result is not None, "Required property 'domain_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the Backend that this Domain is associated with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#location FirebaseAppHostingDomain#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#id FirebaseAppHostingDomain#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#project FirebaseAppHostingDomain#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serve(self) -> typing.Optional["FirebaseAppHostingDomainServe"]:
        '''serve block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#serve FirebaseAppHostingDomain#serve}
        '''
        result = self._values.get("serve")
        return typing.cast(typing.Optional["FirebaseAppHostingDomainServe"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FirebaseAppHostingDomainTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#timeouts FirebaseAppHostingDomain#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FirebaseAppHostingDomainTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusIssues",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusIssues:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusIssues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainCustomDomainStatusIssuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusIssuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9ba0671ce2be16ef5d6a67a30454960f2910962b954d742470985cf47de71c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusIssuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f0817d91d8c0a716bbc3258f4a22bd9b7f332265896743c150b22923ef982a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusIssuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04dc03480b4aee21a2e738edc1ea4a913c939dae4b2e268b15a906446b3c1d09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c56dc385f13fe93b54f290f20c70350e145d678ea13a2bbfbd9c98a9acafbfb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1032b079e886821eb21b6e7a4fd1fa237f0ed014bc2b80c83cc4529147ad022a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusIssuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusIssuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec32108a59f089c241db212c0490a9e63df458ecf6aba695d82de852b7cfc64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusIssues]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusIssues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusIssues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e93f1dff9013a65b86fbf554dc478d59d61412d76ad697a47748ca1e20f3668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__695da130f64beda062ece833d7c19325a1f3f8ea89deeea0502aa1c66fe0b964)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014f7a516b7f0daa319479b0646e881d46fc8691c04cebb6c9171348f9e013a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071f73d29293fad30d2d7e5b632f166c5ae723b97d619aade50ead5304ea4d9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae6b91f5218fa1740b9f02408b0d01b9739dd07710e9814d00f571020807505a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9df3677b9c1a8b05eab0e7128881c321ca6e63198b9edfb295ced9f307c4cc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1578573c5fe0e2ce97ab684bd9bbdb69a63043e41735c477ae9178d8ffcd69f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certState")
    def cert_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certState"))

    @builtins.property
    @jsii.member(jsii_name="hostState")
    def host_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostState"))

    @builtins.property
    @jsii.member(jsii_name="issues")
    def issues(self) -> FirebaseAppHostingDomainCustomDomainStatusIssuesList:
        return typing.cast(FirebaseAppHostingDomainCustomDomainStatusIssuesList, jsii.get(self, "issues"))

    @builtins.property
    @jsii.member(jsii_name="ownershipState")
    def ownership_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownershipState"))

    @builtins.property
    @jsii.member(jsii_name="requiredDnsUpdates")
    def required_dns_updates(
        self,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesList":
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesList", jsii.get(self, "requiredDnsUpdates"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatus]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a4968f9c4e9e7ee9c7d0461b448e81fba1362cb9c9ff8f0383b79fab30a9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a873fa922233826888cc9a3c79e7d65005fc104f875b3d5219cc06c46f2c68ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8f4455fcdb224f412416596382a03dfc59abc473c20db45de930533a53eab5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61faf93e0e33698030845e049966af66717296ef8f1fb5566198d08345e354f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e813438fffc7e754f4a252baf3817a5f54941c7c88d804bf34fd049f7c764703)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6207852b67b203fe58e416fbcc15a2396537b9739872b8d63001135dce70a7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99a186d8ce1f5295cd19355ad10c9c3794799246039c4f7c7191e9349ce99a68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7fe6d415353a37b1469c4dd2afdbcd7971a6eb5cc8b2261a7bcfd964ec878d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9005b42c6a6e207d140d06e3492246f56c4ecd744d7c9e135cfceac31a269ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5964a08392c90712e634864f3b653f9dbb7a595bb2bbceb5dacf0123b72641)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0267fb1c0f7181c7d5a0624e8700bedf57864d41c277df31996192a55166a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__521bcacad543e012e1c7669680f064b2fec1715a4c01087579fd032d05cbea41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3bf5daa607ba192877c5792ee8d12c3aa34cba86c6d84d674c3eef5cc47d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32b62f437426ea930230d711282408e12807f7d37ca0532758cef9514760c55f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="checkError")
    def check_error(
        self,
    ) -> FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorList:
        return typing.cast(FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorList, jsii.get(self, "checkError"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="records")
    def records(
        self,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsList":
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsList", jsii.get(self, "records"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bada13b51df1ea56496710eabc988eda87bb02ac0eeacd2c8ee016ca596c3f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e586deccbce1013d4842d7237feadf1bc8d8f1a3522929061c95f6b1ed6eba1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fc4c279a3e51c7cc055bd12fc2433e150a15e292b2b97b5df60d4c37e8609c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc326477145b675dfdf0ececce664c2074d78da61ed5d3a67e4c3c36a1bd937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f84e9c61f8b5350f37f5852894b6805aa64cafc79b954f5ae84fff57295dc272)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23238e5b165fdab98cf537ca39bdba69dd408e2e8910ece51ca34efe0b80da00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__896242bdc69df3cbba6a7e60b704f7ed357aa4b14c65263bb420f3ee139dea1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="rdata")
    def rdata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdata"))

    @builtins.property
    @jsii.member(jsii_name="relevantState")
    def relevant_state(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relevantState"))

    @builtins.property
    @jsii.member(jsii_name="requiredAction")
    def required_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requiredAction"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74daede64032cde2bb5edb35493e062c4d413590226a91d478dd84a1fd738a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0928386a0ca3c7f22f789c255c9729deac026443c15b98f36824f76da07f492)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1f6f6241594d810e72e4f5abd41f216b6ea7dd81a2a7899e811369c5f9166c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e6df97617803e62c3a2f75f0ba83c7ebb866602659b32ef859d25bdb22a048)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86cf8683a2bba1ef48b8952f06ccb6cf8731231f2afebeba5f8b2cc4f8e5ea20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e82ee6ecd7cfc95681671f3e87474e4b006e1c0ef32a5686bf52ee9d136ea16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__661595d571da8218110d62b60103f5df68a5a603e031e42d2b4b9a41392e0029)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7dfb42699e5aa97047e69d98e960b445e72fa656c0adca6ca2c3d33903fe26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a969a77a2a0430df93008dc6a363bcdd1cdf7e48dcf9bac5932b755c7f705c9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bbda74698e76c46d1f9305a0612c0b0e6bec0c5fef899afe9438b1c25ae0eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb49997f787ac918d812e569811b758327973b5ecac3cf3c4208d67b048b0232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b998797704e397dccdb63edbe7301aeb84fc2d6a32d47d70e1aaa34ffebe3a72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b64542a22cbdc658a75b15b8c2db96f6ce1a15d77a33b8894fa2c614d932005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f54242f54abbd7f5cc1ad714bda491d5eaa523a5f390446a6bbd276b5541bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="checkError")
    def check_error(
        self,
    ) -> FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorList:
        return typing.cast(FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorList, jsii.get(self, "checkError"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="records")
    def records(
        self,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsList":
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsList", jsii.get(self, "records"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c285d5e6bc715ee01ad6d6c6f4a31cb80a450e4b01b493d2ce6f78e19167a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d26f42ce35ca1efeadcf5f2d8804ebdc118649d5ef659dc994dd8f81919472a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9856a6647a305f1c88da72e9e1310c380babf80c22b6dc779ea04e8c499c40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7297e3e8c3b454c7097fb798d6d102dc46d7069cb27c9caad4d61104fc1048)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5a2347ba22a251315f5ce0cb63c3ca6d1dcd7f07bcf0144c6443e2ea050251d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8088296d20663358468b38ef3e1ec151ffe179736e345bc94d6f0326db03db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29c8cfff84c01abf40fb0c7b29872251b5bbd09cd562543cc650e470c75c7d4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="rdata")
    def rdata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdata"))

    @builtins.property
    @jsii.member(jsii_name="relevantState")
    def relevant_state(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relevantState"))

    @builtins.property
    @jsii.member(jsii_name="requiredAction")
    def required_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requiredAction"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c014b39c5d94dfa2d533b36d325d293a59f8ec1581f3b218e459a32182ae53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3025255894e1c06268edb336b00f0dc63537e54fcc577081f300a857c0e94fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b00a7442d3d1ea303e5c398700fbf694eb913838e3882557c4c13ac51fa03c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48d27f88dd22ad89bdd42fbfa447186b5dff404ee79b2a718caa87aa811edda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed02cb2c8100da57dbf8f9353f83bf040fcd2833d7e0bda744435bad37b8165)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dfee04e1eaeed1381fdd2638bf9b34a7b7b030d2188191231e539f028cbd5c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__313c3c57b4f774891b7340bae43db543b6e7ad71353c840b6c6fddb2afb5f05c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="checkTime")
    def check_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkTime"))

    @builtins.property
    @jsii.member(jsii_name="desired")
    def desired(
        self,
    ) -> FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredList:
        return typing.cast(FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredList, jsii.get(self, "desired"))

    @builtins.property
    @jsii.member(jsii_name="discovered")
    def discovered(
        self,
    ) -> FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredList:
        return typing.cast(FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredList, jsii.get(self, "discovered"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d92a36199c0d21d2ec4f3b92f187bf667fb46d9550ae1acde57b007f666ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainServe",
    jsii_struct_bases=[],
    name_mapping={"redirect": "redirect"},
)
class FirebaseAppHostingDomainServe:
    def __init__(
        self,
        *,
        redirect: typing.Optional[typing.Union["FirebaseAppHostingDomainServeRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#redirect FirebaseAppHostingDomain#redirect}
        '''
        if isinstance(redirect, dict):
            redirect = FirebaseAppHostingDomainServeRedirect(**redirect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a314612700b9b144f68fede16f94bf01a630642c2785fb7735f0c3d66b7395d)
            check_type(argname="argument redirect", value=redirect, expected_type=type_hints["redirect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if redirect is not None:
            self._values["redirect"] = redirect

    @builtins.property
    def redirect(self) -> typing.Optional["FirebaseAppHostingDomainServeRedirect"]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#redirect FirebaseAppHostingDomain#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional["FirebaseAppHostingDomainServeRedirect"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainServe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainServeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainServeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41750406e7914ce16cc66249afd6bbd6687892da0dfb16379f80e4bb2afc0ee8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRedirect")
    def put_redirect(
        self,
        *,
        uri: builtins.str,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the redirect's intended destination. This URI will be prepended to the original request path. URI without a scheme are assumed to be HTTPS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#uri FirebaseAppHostingDomain#uri}
        :param status: The status code to use in a redirect response. Must be a valid HTTP 3XX status code. Defaults to 302 if not present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#status FirebaseAppHostingDomain#status}
        '''
        value = FirebaseAppHostingDomainServeRedirect(uri=uri, status=status)

        return typing.cast(None, jsii.invoke(self, "putRedirect", [value]))

    @jsii.member(jsii_name="resetRedirect")
    def reset_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirect", []))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(self) -> "FirebaseAppHostingDomainServeRedirectOutputReference":
        return typing.cast("FirebaseAppHostingDomainServeRedirectOutputReference", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(
        self,
    ) -> typing.Optional["FirebaseAppHostingDomainServeRedirect"]:
        return typing.cast(typing.Optional["FirebaseAppHostingDomainServeRedirect"], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirebaseAppHostingDomainServe]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainServe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainServe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90fb20fbad84436829657ff004ef4bb5feb39250e9c7a6a5b6e26d73e9a6b7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainServeRedirect",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "status": "status"},
)
class FirebaseAppHostingDomainServeRedirect:
    def __init__(
        self,
        *,
        uri: builtins.str,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the redirect's intended destination. This URI will be prepended to the original request path. URI without a scheme are assumed to be HTTPS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#uri FirebaseAppHostingDomain#uri}
        :param status: The status code to use in a redirect response. Must be a valid HTTP 3XX status code. Defaults to 302 if not present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#status FirebaseAppHostingDomain#status}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b5d08b6e3873a90a268b1e55cfa9459544ca667bd4bd818f99cf4f8be32993)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def uri(self) -> builtins.str:
        '''The URI of the redirect's intended destination.

        This URI will be
        prepended to the original request path. URI without a scheme are
        assumed to be HTTPS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#uri FirebaseAppHostingDomain#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status code to use in a redirect response.

        Must be a valid HTTP 3XX
        status code. Defaults to 302 if not present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#status FirebaseAppHostingDomain#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainServeRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainServeRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainServeRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29491d28c9575c8e7ec3743a39771a9785053a2167fc54cf820ca87e722c547f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1036d7cac4c663ec2e5a272db490becd5c6ddef31b4117611c9107e6740ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6d4a127fe14bb11eb0db277b3d6cec702b742a58c4211be20d1c51d1f7bb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirebaseAppHostingDomainServeRedirect]:
        return typing.cast(typing.Optional[FirebaseAppHostingDomainServeRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirebaseAppHostingDomainServeRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47442dbb26132199afb245c637b44610f20000d61eea0d32b43fa731d514fcc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FirebaseAppHostingDomainTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#create FirebaseAppHostingDomain#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#delete FirebaseAppHostingDomain#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#update FirebaseAppHostingDomain#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1060814127e0ca6604486568ba1a6223080abe1691ce6f052d110d8f239973)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#create FirebaseAppHostingDomain#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#delete FirebaseAppHostingDomain#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firebase_app_hosting_domain#update FirebaseAppHostingDomain#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirebaseAppHostingDomainTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirebaseAppHostingDomainTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firebaseAppHostingDomain.FirebaseAppHostingDomainTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0660c62848b47f7d82493c387df8f1dcbf9e0dd5ceac235042f36906f13f49b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__674ed549322b4fa2ae58af467b6d4d8f395b4a0dc9596fd5a1348c032d76636d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407b047724bbdddf7e5cebcd75402bf36c6a4eaa3da468d6f26f61275311bbbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d7bcc1de0ee67ea3180bb63872b87063872d8db41a548cb08f1df3b216d046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingDomainTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingDomainTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingDomainTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fb1b507784071310a5c9db20f5fa2ed33b68aae2817038102adf6271c57246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FirebaseAppHostingDomain",
    "FirebaseAppHostingDomainConfig",
    "FirebaseAppHostingDomainCustomDomainStatus",
    "FirebaseAppHostingDomainCustomDomainStatusIssues",
    "FirebaseAppHostingDomainCustomDomainStatusIssuesList",
    "FirebaseAppHostingDomainCustomDomainStatusIssuesOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusList",
    "FirebaseAppHostingDomainCustomDomainStatusOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckErrorOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecordsOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckErrorOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecordsOutputReference",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesList",
    "FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesOutputReference",
    "FirebaseAppHostingDomainServe",
    "FirebaseAppHostingDomainServeOutputReference",
    "FirebaseAppHostingDomainServeRedirect",
    "FirebaseAppHostingDomainServeRedirectOutputReference",
    "FirebaseAppHostingDomainTimeouts",
    "FirebaseAppHostingDomainTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__de86a9c3085a22321613c4d1ae9ffb1cb735c212f6adb8d2b275bcedc8b7df68(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backend: builtins.str,
    domain_id: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    serve: typing.Optional[typing.Union[FirebaseAppHostingDomainServe, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FirebaseAppHostingDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7b12a48d04cc9f870843aa071a37b1ae123e13b2d3dd0ab3e76af9cee7e2f8a5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26487bf7d430edee8dc52f2f8adba010b8d8df2d567a9dc0eff11fdcb9a9c23a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e82911f509fbab24ca640a8fc04330a3e3182b7ba631e631c42a6ce8fd42b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ce7a92dd767ac9652ae9753f244df61d7b39cfc1451c06aaabba8dd5982be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73709549da2dcf3feb276c5e734c9b3c288b94ef8bcc6d3758a4faea832ef111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbdbdb2bb341f58b391d021dda6f95e7cd6ff4c6040e0b0e5faad075b8af5b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9492ec781d67247a7c46a207474af15662f41d6a38228f2d8734c89aa27bc763(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backend: builtins.str,
    domain_id: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    serve: typing.Optional[typing.Union[FirebaseAppHostingDomainServe, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FirebaseAppHostingDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9ba0671ce2be16ef5d6a67a30454960f2910962b954d742470985cf47de71c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f0817d91d8c0a716bbc3258f4a22bd9b7f332265896743c150b22923ef982a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dc03480b4aee21a2e738edc1ea4a913c939dae4b2e268b15a906446b3c1d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56dc385f13fe93b54f290f20c70350e145d678ea13a2bbfbd9c98a9acafbfb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1032b079e886821eb21b6e7a4fd1fa237f0ed014bc2b80c83cc4529147ad022a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec32108a59f089c241db212c0490a9e63df458ecf6aba695d82de852b7cfc64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e93f1dff9013a65b86fbf554dc478d59d61412d76ad697a47748ca1e20f3668(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusIssues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695da130f64beda062ece833d7c19325a1f3f8ea89deeea0502aa1c66fe0b964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014f7a516b7f0daa319479b0646e881d46fc8691c04cebb6c9171348f9e013a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071f73d29293fad30d2d7e5b632f166c5ae723b97d619aade50ead5304ea4d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6b91f5218fa1740b9f02408b0d01b9739dd07710e9814d00f571020807505a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df3677b9c1a8b05eab0e7128881c321ca6e63198b9edfb295ced9f307c4cc37(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1578573c5fe0e2ce97ab684bd9bbdb69a63043e41735c477ae9178d8ffcd69f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a4968f9c4e9e7ee9c7d0461b448e81fba1362cb9c9ff8f0383b79fab30a9fd(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a873fa922233826888cc9a3c79e7d65005fc104f875b3d5219cc06c46f2c68ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8f4455fcdb224f412416596382a03dfc59abc473c20db45de930533a53eab5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61faf93e0e33698030845e049966af66717296ef8f1fb5566198d08345e354f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e813438fffc7e754f4a252baf3817a5f54941c7c88d804bf34fd049f7c764703(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6207852b67b203fe58e416fbcc15a2396537b9739872b8d63001135dce70a7e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a186d8ce1f5295cd19355ad10c9c3794799246039c4f7c7191e9349ce99a68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7fe6d415353a37b1469c4dd2afdbcd7971a6eb5cc8b2261a7bcfd964ec878d(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredCheckError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9005b42c6a6e207d140d06e3492246f56c4ecd744d7c9e135cfceac31a269ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5964a08392c90712e634864f3b653f9dbb7a595bb2bbceb5dacf0123b72641(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0267fb1c0f7181c7d5a0624e8700bedf57864d41c277df31996192a55166a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521bcacad543e012e1c7669680f064b2fec1715a4c01087579fd032d05cbea41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3bf5daa607ba192877c5792ee8d12c3aa34cba86c6d84d674c3eef5cc47d6f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b62f437426ea930230d711282408e12807f7d37ca0532758cef9514760c55f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bada13b51df1ea56496710eabc988eda87bb02ac0eeacd2c8ee016ca596c3f03(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesired],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e586deccbce1013d4842d7237feadf1bc8d8f1a3522929061c95f6b1ed6eba1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fc4c279a3e51c7cc055bd12fc2433e150a15e292b2b97b5df60d4c37e8609c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc326477145b675dfdf0ececce664c2074d78da61ed5d3a67e4c3c36a1bd937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84e9c61f8b5350f37f5852894b6805aa64cafc79b954f5ae84fff57295dc272(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23238e5b165fdab98cf537ca39bdba69dd408e2e8910ece51ca34efe0b80da00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896242bdc69df3cbba6a7e60b704f7ed357aa4b14c65263bb420f3ee139dea1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74daede64032cde2bb5edb35493e062c4d413590226a91d478dd84a1fd738a37(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDesiredRecords],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0928386a0ca3c7f22f789c255c9729deac026443c15b98f36824f76da07f492(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1f6f6241594d810e72e4f5abd41f216b6ea7dd81a2a7899e811369c5f9166c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e6df97617803e62c3a2f75f0ba83c7ebb866602659b32ef859d25bdb22a048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cf8683a2bba1ef48b8952f06ccb6cf8731231f2afebeba5f8b2cc4f8e5ea20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e82ee6ecd7cfc95681671f3e87474e4b006e1c0ef32a5686bf52ee9d136ea16(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661595d571da8218110d62b60103f5df68a5a603e031e42d2b4b9a41392e0029(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7dfb42699e5aa97047e69d98e960b445e72fa656c0adca6ca2c3d33903fe26(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredCheckError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a969a77a2a0430df93008dc6a363bcdd1cdf7e48dcf9bac5932b755c7f705c9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bbda74698e76c46d1f9305a0612c0b0e6bec0c5fef899afe9438b1c25ae0eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb49997f787ac918d812e569811b758327973b5ecac3cf3c4208d67b048b0232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b998797704e397dccdb63edbe7301aeb84fc2d6a32d47d70e1aaa34ffebe3a72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b64542a22cbdc658a75b15b8c2db96f6ce1a15d77a33b8894fa2c614d932005(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f54242f54abbd7f5cc1ad714bda491d5eaa523a5f390446a6bbd276b5541bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c285d5e6bc715ee01ad6d6c6f4a31cb80a450e4b01b493d2ce6f78e19167a3(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscovered],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d26f42ce35ca1efeadcf5f2d8804ebdc118649d5ef659dc994dd8f81919472a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9856a6647a305f1c88da72e9e1310c380babf80c22b6dc779ea04e8c499c40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7297e3e8c3b454c7097fb798d6d102dc46d7069cb27c9caad4d61104fc1048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a2347ba22a251315f5ce0cb63c3ca6d1dcd7f07bcf0144c6443e2ea050251d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8088296d20663358468b38ef3e1ec151ffe179736e345bc94d6f0326db03db2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c8cfff84c01abf40fb0c7b29872251b5bbd09cd562543cc650e470c75c7d4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c014b39c5d94dfa2d533b36d325d293a59f8ec1581f3b218e459a32182ae53(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdatesDiscoveredRecords],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3025255894e1c06268edb336b00f0dc63537e54fcc577081f300a857c0e94fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b00a7442d3d1ea303e5c398700fbf694eb913838e3882557c4c13ac51fa03c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48d27f88dd22ad89bdd42fbfa447186b5dff404ee79b2a718caa87aa811edda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed02cb2c8100da57dbf8f9353f83bf040fcd2833d7e0bda744435bad37b8165(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfee04e1eaeed1381fdd2638bf9b34a7b7b030d2188191231e539f028cbd5c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313c3c57b4f774891b7340bae43db543b6e7ad71353c840b6c6fddb2afb5f05c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d92a36199c0d21d2ec4f3b92f187bf667fb46d9550ae1acde57b007f666ba0(
    value: typing.Optional[FirebaseAppHostingDomainCustomDomainStatusRequiredDnsUpdates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a314612700b9b144f68fede16f94bf01a630642c2785fb7735f0c3d66b7395d(
    *,
    redirect: typing.Optional[typing.Union[FirebaseAppHostingDomainServeRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41750406e7914ce16cc66249afd6bbd6687892da0dfb16379f80e4bb2afc0ee8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90fb20fbad84436829657ff004ef4bb5feb39250e9c7a6a5b6e26d73e9a6b7b(
    value: typing.Optional[FirebaseAppHostingDomainServe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b5d08b6e3873a90a268b1e55cfa9459544ca667bd4bd818f99cf4f8be32993(
    *,
    uri: builtins.str,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29491d28c9575c8e7ec3743a39771a9785053a2167fc54cf820ca87e722c547f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1036d7cac4c663ec2e5a272db490becd5c6ddef31b4117611c9107e6740ad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6d4a127fe14bb11eb0db277b3d6cec702b742a58c4211be20d1c51d1f7bb7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47442dbb26132199afb245c637b44610f20000d61eea0d32b43fa731d514fcc4(
    value: typing.Optional[FirebaseAppHostingDomainServeRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1060814127e0ca6604486568ba1a6223080abe1691ce6f052d110d8f239973(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0660c62848b47f7d82493c387df8f1dcbf9e0dd5ceac235042f36906f13f49b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674ed549322b4fa2ae58af467b6d4d8f395b4a0dc9596fd5a1348c032d76636d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407b047724bbdddf7e5cebcd75402bf36c6a4eaa3da468d6f26f61275311bbbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d7bcc1de0ee67ea3180bb63872b87063872d8db41a548cb08f1df3b216d046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fb1b507784071310a5c9db20f5fa2ed33b68aae2817038102adf6271c57246(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirebaseAppHostingDomainTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
