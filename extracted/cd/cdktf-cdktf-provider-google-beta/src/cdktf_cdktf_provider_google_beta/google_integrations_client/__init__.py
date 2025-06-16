r'''
# `google_integrations_client`

Refer to the Terraform Registry for docs: [`google_integrations_client`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client).
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


class GoogleIntegrationsClient(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsClient.GoogleIntegrationsClient",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client google_integrations_client}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        cloud_kms_config: typing.Optional[typing.Union["GoogleIntegrationsClientCloudKmsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        create_sample_integrations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        run_as_service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIntegrationsClientTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client google_integrations_client} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Location in which client needs to be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#location GoogleIntegrationsClient#location}
        :param cloud_kms_config: cloud_kms_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#cloud_kms_config GoogleIntegrationsClient#cloud_kms_config}
        :param create_sample_integrations: Indicates if sample integrations should be created along with provisioning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#create_sample_integrations GoogleIntegrationsClient#create_sample_integrations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#id GoogleIntegrationsClient#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#project GoogleIntegrationsClient#project}.
        :param run_as_service_account: User input run-as service account, if empty, will bring up a new default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#run_as_service_account GoogleIntegrationsClient#run_as_service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#timeouts GoogleIntegrationsClient#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e717233bc36f5b0ecf2aee6e1a5a9ba10eca52b53e762bb87d6921955cd6ecf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIntegrationsClientConfig(
            location=location,
            cloud_kms_config=cloud_kms_config,
            create_sample_integrations=create_sample_integrations,
            id=id,
            project=project,
            run_as_service_account=run_as_service_account,
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
        '''Generates CDKTF code for importing a GoogleIntegrationsClient resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIntegrationsClient to import.
        :param import_from_id: The id of the existing GoogleIntegrationsClient that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIntegrationsClient to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03eb3a7539e3da682aad8afee96a419ef19ac7afbf43b5f9e2b7be7df532b014)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudKmsConfig")
    def put_cloud_kms_config(
        self,
        *,
        key: builtins.str,
        kms_location: builtins.str,
        kms_ring: builtins.str,
        key_version: typing.Optional[builtins.str] = None,
        kms_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: A Cloud KMS key is a named object containing one or more key versions, along with metadata for the key. A key exists on exactly one key ring tied to a specific location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#key GoogleIntegrationsClient#key}
        :param kms_location: Location name of the key ring, e.g. "us-west1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_location GoogleIntegrationsClient#kms_location}
        :param kms_ring: A key ring organizes keys in a specific Google Cloud location and allows you to manage access control on groups of keys. A key ring's name does not need to be unique across a Google Cloud project, but must be unique within a given location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_ring GoogleIntegrationsClient#kms_ring}
        :param key_version: Each version of a key contains key material used for encryption or signing. A key's version is represented by an integer, starting at 1. To decrypt data or verify a signature, you must use the same key version that was used to encrypt or sign the data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#key_version GoogleIntegrationsClient#key_version}
        :param kms_project_id: The Google Cloud project id of the project where the kms key stored. If empty, the kms key is stored at the same project as customer's project and ecrypted with CMEK, otherwise, the kms key is stored in the tenant project and encrypted with GMEK. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_project_id GoogleIntegrationsClient#kms_project_id}
        '''
        value = GoogleIntegrationsClientCloudKmsConfig(
            key=key,
            kms_location=kms_location,
            kms_ring=kms_ring,
            key_version=key_version,
            kms_project_id=kms_project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudKmsConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#create GoogleIntegrationsClient#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#delete GoogleIntegrationsClient#delete}.
        '''
        value = GoogleIntegrationsClientTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCloudKmsConfig")
    def reset_cloud_kms_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudKmsConfig", []))

    @jsii.member(jsii_name="resetCreateSampleIntegrations")
    def reset_create_sample_integrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateSampleIntegrations", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRunAsServiceAccount")
    def reset_run_as_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunAsServiceAccount", []))

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
    @jsii.member(jsii_name="cloudKmsConfig")
    def cloud_kms_config(
        self,
    ) -> "GoogleIntegrationsClientCloudKmsConfigOutputReference":
        return typing.cast("GoogleIntegrationsClientCloudKmsConfigOutputReference", jsii.get(self, "cloudKmsConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleIntegrationsClientTimeoutsOutputReference":
        return typing.cast("GoogleIntegrationsClientTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cloudKmsConfigInput")
    def cloud_kms_config_input(
        self,
    ) -> typing.Optional["GoogleIntegrationsClientCloudKmsConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationsClientCloudKmsConfig"], jsii.get(self, "cloudKmsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="createSampleIntegrationsInput")
    def create_sample_integrations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createSampleIntegrationsInput"))

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
    @jsii.member(jsii_name="runAsServiceAccountInput")
    def run_as_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runAsServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIntegrationsClientTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIntegrationsClientTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="createSampleIntegrations")
    def create_sample_integrations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createSampleIntegrations"))

    @create_sample_integrations.setter
    def create_sample_integrations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66dac5bca84254d171d40bd985d44add623dd6a4eafabd9c43e5e52ea1851f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSampleIntegrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f801d9ec5cdd9a369a29f9c53d672fd85ee0df4c5908abb33419fcf03e88da85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60bf0d01b6fd684b137c8971955f02f7c95be96d6a899935397349f3243b2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0242f0f00e0fc778f5031b3927fc3d9cf711f58e39cc0b659e0c12940ade91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runAsServiceAccount")
    def run_as_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runAsServiceAccount"))

    @run_as_service_account.setter
    def run_as_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7ad73d33241c4b885bed65f080231265a539fe2206dc508c2bfd81797dc4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runAsServiceAccount", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsClient.GoogleIntegrationsClientCloudKmsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "kms_location": "kmsLocation",
        "kms_ring": "kmsRing",
        "key_version": "keyVersion",
        "kms_project_id": "kmsProjectId",
    },
)
class GoogleIntegrationsClientCloudKmsConfig:
    def __init__(
        self,
        *,
        key: builtins.str,
        kms_location: builtins.str,
        kms_ring: builtins.str,
        key_version: typing.Optional[builtins.str] = None,
        kms_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: A Cloud KMS key is a named object containing one or more key versions, along with metadata for the key. A key exists on exactly one key ring tied to a specific location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#key GoogleIntegrationsClient#key}
        :param kms_location: Location name of the key ring, e.g. "us-west1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_location GoogleIntegrationsClient#kms_location}
        :param kms_ring: A key ring organizes keys in a specific Google Cloud location and allows you to manage access control on groups of keys. A key ring's name does not need to be unique across a Google Cloud project, but must be unique within a given location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_ring GoogleIntegrationsClient#kms_ring}
        :param key_version: Each version of a key contains key material used for encryption or signing. A key's version is represented by an integer, starting at 1. To decrypt data or verify a signature, you must use the same key version that was used to encrypt or sign the data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#key_version GoogleIntegrationsClient#key_version}
        :param kms_project_id: The Google Cloud project id of the project where the kms key stored. If empty, the kms key is stored at the same project as customer's project and ecrypted with CMEK, otherwise, the kms key is stored in the tenant project and encrypted with GMEK. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_project_id GoogleIntegrationsClient#kms_project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0625e884b24139d0a41f707eb36292784a509c1840990424d4b9b2ad7277fec)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument kms_location", value=kms_location, expected_type=type_hints["kms_location"])
            check_type(argname="argument kms_ring", value=kms_ring, expected_type=type_hints["kms_ring"])
            check_type(argname="argument key_version", value=key_version, expected_type=type_hints["key_version"])
            check_type(argname="argument kms_project_id", value=kms_project_id, expected_type=type_hints["kms_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "kms_location": kms_location,
            "kms_ring": kms_ring,
        }
        if key_version is not None:
            self._values["key_version"] = key_version
        if kms_project_id is not None:
            self._values["kms_project_id"] = kms_project_id

    @builtins.property
    def key(self) -> builtins.str:
        '''A Cloud KMS key is a named object containing one or more key versions, along with metadata for the key.

        A key exists on exactly one key ring tied to a
        specific location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#key GoogleIntegrationsClient#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_location(self) -> builtins.str:
        '''Location name of the key ring, e.g. "us-west1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_location GoogleIntegrationsClient#kms_location}
        '''
        result = self._values.get("kms_location")
        assert result is not None, "Required property 'kms_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_ring(self) -> builtins.str:
        '''A key ring organizes keys in a specific Google Cloud location and allows you to manage access control on groups of keys.

        A key ring's name does not need to be
        unique across a Google Cloud project, but must be unique within a given location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_ring GoogleIntegrationsClient#kms_ring}
        '''
        result = self._values.get("kms_ring")
        assert result is not None, "Required property 'kms_ring' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_version(self) -> typing.Optional[builtins.str]:
        '''Each version of a key contains key material used for encryption or signing.

        A key's version is represented by an integer, starting at 1. To decrypt data
        or verify a signature, you must use the same key version that was used to
        encrypt or sign the data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#key_version GoogleIntegrationsClient#key_version}
        '''
        result = self._values.get("key_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_project_id(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud project id of the project where the kms key stored.

        If empty,
        the kms key is stored at the same project as customer's project and ecrypted
        with CMEK, otherwise, the kms key is stored in the tenant project and
        encrypted with GMEK.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#kms_project_id GoogleIntegrationsClient#kms_project_id}
        '''
        result = self._values.get("kms_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsClientCloudKmsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsClientCloudKmsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsClient.GoogleIntegrationsClientCloudKmsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c674814608f3945da0e30007138a844011aad27330900884f8d3e1955e5d997)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyVersion")
    def reset_key_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVersion", []))

    @jsii.member(jsii_name="resetKmsProjectId")
    def reset_kms_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVersionInput")
    def key_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsLocationInput")
    def kms_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsProjectIdInput")
    def kms_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsRingInput")
    def kms_ring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsRingInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe26255f9589ba20852dc0d57c5db738168130049507abee09cbb864adc6934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVersion")
    def key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVersion"))

    @key_version.setter
    def key_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d109de47e08ca0c444c95647465a978554bba624b9df04760b2e6c6e8fc2b253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsLocation")
    def kms_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsLocation"))

    @kms_location.setter
    def kms_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1fbaaffb9a5c55b2f020b4df470418b1832dc684bc76f40200f970bf884757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsProjectId")
    def kms_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsProjectId"))

    @kms_project_id.setter
    def kms_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd7fcd8e169df58ad17f1afe5843af3f130b63bd474e63e9fc2a6aec80c47a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsRing")
    def kms_ring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsRing"))

    @kms_ring.setter
    def kms_ring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db81668a7b165d17570ce728f7a9b385e5acf00f8ed7e82089d3717ba6623daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsRing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleIntegrationsClientCloudKmsConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationsClientCloudKmsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationsClientCloudKmsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad6b16ef8ed4a599d2f8dd0ecd8180b781c3dafd10803e11569e4b5a8a8ee3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsClient.GoogleIntegrationsClientConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "cloud_kms_config": "cloudKmsConfig",
        "create_sample_integrations": "createSampleIntegrations",
        "id": "id",
        "project": "project",
        "run_as_service_account": "runAsServiceAccount",
        "timeouts": "timeouts",
    },
)
class GoogleIntegrationsClientConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        cloud_kms_config: typing.Optional[typing.Union[GoogleIntegrationsClientCloudKmsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        create_sample_integrations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        run_as_service_account: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleIntegrationsClientTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Location in which client needs to be provisioned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#location GoogleIntegrationsClient#location}
        :param cloud_kms_config: cloud_kms_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#cloud_kms_config GoogleIntegrationsClient#cloud_kms_config}
        :param create_sample_integrations: Indicates if sample integrations should be created along with provisioning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#create_sample_integrations GoogleIntegrationsClient#create_sample_integrations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#id GoogleIntegrationsClient#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#project GoogleIntegrationsClient#project}.
        :param run_as_service_account: User input run-as service account, if empty, will bring up a new default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#run_as_service_account GoogleIntegrationsClient#run_as_service_account}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#timeouts GoogleIntegrationsClient#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloud_kms_config, dict):
            cloud_kms_config = GoogleIntegrationsClientCloudKmsConfig(**cloud_kms_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleIntegrationsClientTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a65089243ceb8659e6dc592efec12e6f4f1226e715da3ff2cd2afc57168ca5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument cloud_kms_config", value=cloud_kms_config, expected_type=type_hints["cloud_kms_config"])
            check_type(argname="argument create_sample_integrations", value=create_sample_integrations, expected_type=type_hints["create_sample_integrations"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument run_as_service_account", value=run_as_service_account, expected_type=type_hints["run_as_service_account"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if cloud_kms_config is not None:
            self._values["cloud_kms_config"] = cloud_kms_config
        if create_sample_integrations is not None:
            self._values["create_sample_integrations"] = create_sample_integrations
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if run_as_service_account is not None:
            self._values["run_as_service_account"] = run_as_service_account
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
    def location(self) -> builtins.str:
        '''Location in which client needs to be provisioned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#location GoogleIntegrationsClient#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_kms_config(
        self,
    ) -> typing.Optional[GoogleIntegrationsClientCloudKmsConfig]:
        '''cloud_kms_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#cloud_kms_config GoogleIntegrationsClient#cloud_kms_config}
        '''
        result = self._values.get("cloud_kms_config")
        return typing.cast(typing.Optional[GoogleIntegrationsClientCloudKmsConfig], result)

    @builtins.property
    def create_sample_integrations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if sample integrations should be created along with provisioning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#create_sample_integrations GoogleIntegrationsClient#create_sample_integrations}
        '''
        result = self._values.get("create_sample_integrations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#id GoogleIntegrationsClient#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#project GoogleIntegrationsClient#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_as_service_account(self) -> typing.Optional[builtins.str]:
        '''User input run-as service account, if empty, will bring up a new default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#run_as_service_account GoogleIntegrationsClient#run_as_service_account}
        '''
        result = self._values.get("run_as_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleIntegrationsClientTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#timeouts GoogleIntegrationsClient#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIntegrationsClientTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsClientConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsClient.GoogleIntegrationsClientTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleIntegrationsClientTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#create GoogleIntegrationsClient#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#delete GoogleIntegrationsClient#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828cf609216e96e0af00989d30624ac76571c2c3f26b11a6ffcbf0f7c80a4da9)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#create GoogleIntegrationsClient#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integrations_client#delete GoogleIntegrationsClient#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationsClientTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationsClientTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationsClient.GoogleIntegrationsClientTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33061926b0391e946214650c6fef55f3b01a64a5c1377895a19d49d8ab0f0443)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c269ae355234aa0df1c83868446c7ad8a3e6f74a9094b3720e70a62b31d4f63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87c02cad90cfb59cf577c91b6d0c63fe760871e2ea965555229aef90df44227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsClientTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsClientTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsClientTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28769d9be5c466d9b82876ee59341530fa92ec2f8d534148224f2e0abc661d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIntegrationsClient",
    "GoogleIntegrationsClientCloudKmsConfig",
    "GoogleIntegrationsClientCloudKmsConfigOutputReference",
    "GoogleIntegrationsClientConfig",
    "GoogleIntegrationsClientTimeouts",
    "GoogleIntegrationsClientTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9e717233bc36f5b0ecf2aee6e1a5a9ba10eca52b53e762bb87d6921955cd6ecf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    cloud_kms_config: typing.Optional[typing.Union[GoogleIntegrationsClientCloudKmsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    create_sample_integrations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    run_as_service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIntegrationsClientTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__03eb3a7539e3da682aad8afee96a419ef19ac7afbf43b5f9e2b7be7df532b014(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66dac5bca84254d171d40bd985d44add623dd6a4eafabd9c43e5e52ea1851f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f801d9ec5cdd9a369a29f9c53d672fd85ee0df4c5908abb33419fcf03e88da85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60bf0d01b6fd684b137c8971955f02f7c95be96d6a899935397349f3243b2e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0242f0f00e0fc778f5031b3927fc3d9cf711f58e39cc0b659e0c12940ade91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7ad73d33241c4b885bed65f080231265a539fe2206dc508c2bfd81797dc4c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0625e884b24139d0a41f707eb36292784a509c1840990424d4b9b2ad7277fec(
    *,
    key: builtins.str,
    kms_location: builtins.str,
    kms_ring: builtins.str,
    key_version: typing.Optional[builtins.str] = None,
    kms_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c674814608f3945da0e30007138a844011aad27330900884f8d3e1955e5d997(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe26255f9589ba20852dc0d57c5db738168130049507abee09cbb864adc6934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d109de47e08ca0c444c95647465a978554bba624b9df04760b2e6c6e8fc2b253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1fbaaffb9a5c55b2f020b4df470418b1832dc684bc76f40200f970bf884757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd7fcd8e169df58ad17f1afe5843af3f130b63bd474e63e9fc2a6aec80c47a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db81668a7b165d17570ce728f7a9b385e5acf00f8ed7e82089d3717ba6623daf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad6b16ef8ed4a599d2f8dd0ecd8180b781c3dafd10803e11569e4b5a8a8ee3a(
    value: typing.Optional[GoogleIntegrationsClientCloudKmsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a65089243ceb8659e6dc592efec12e6f4f1226e715da3ff2cd2afc57168ca5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    cloud_kms_config: typing.Optional[typing.Union[GoogleIntegrationsClientCloudKmsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    create_sample_integrations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    run_as_service_account: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleIntegrationsClientTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828cf609216e96e0af00989d30624ac76571c2c3f26b11a6ffcbf0f7c80a4da9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33061926b0391e946214650c6fef55f3b01a64a5c1377895a19d49d8ab0f0443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c269ae355234aa0df1c83868446c7ad8a3e6f74a9094b3720e70a62b31d4f63c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87c02cad90cfb59cf577c91b6d0c63fe760871e2ea965555229aef90df44227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28769d9be5c466d9b82876ee59341530fa92ec2f8d534148224f2e0abc661d7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationsClientTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
