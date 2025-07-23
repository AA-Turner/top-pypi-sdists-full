r'''
# `google_integration_connectors_connection`

Refer to the Terraform Registry for docs: [`google_integration_connectors_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection).
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


class IntegrationConnectorsConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection google_integration_connectors_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connector_version: builtins.str,
        location: builtins.str,
        name: builtins.str,
        auth_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionConfigVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionDestinationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        eventing_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        eventing_enablement_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lock_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionLockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["IntegrationConnectorsConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection google_integration_connectors_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connector_version: connectorVersion of the Connector. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#connector_version IntegrationConnectorsConnection#connector_version}
        :param location: Location in which Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#location IntegrationConnectorsConnection#location}
        :param name: Name of Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#name IntegrationConnectorsConnection#name}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_config IntegrationConnectorsConnection#auth_config}
        :param config_variable: config_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#config_variable IntegrationConnectorsConnection#config_variable}
        :param description: An arbitrary description for the Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#description IntegrationConnectorsConnection#description}
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination_config IntegrationConnectorsConnection#destination_config}
        :param eventing_config: eventing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#eventing_config IntegrationConnectorsConnection#eventing_config}
        :param eventing_enablement_type: Eventing enablement type. Will be nil if eventing is not enabled. Possible values: ["EVENTING_AND_CONNECTION", "ONLY_EVENTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#eventing_enablement_type IntegrationConnectorsConnection#eventing_enablement_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#id IntegrationConnectorsConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#labels IntegrationConnectorsConnection#labels}
        :param lock_config: lock_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#lock_config IntegrationConnectorsConnection#lock_config}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#log_config IntegrationConnectorsConnection#log_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#node_config IntegrationConnectorsConnection#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#project IntegrationConnectorsConnection#project}.
        :param service_account: Service account needed for runtime plane to access Google Cloud resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_account IntegrationConnectorsConnection#service_account}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssl_config IntegrationConnectorsConnection#ssl_config}
        :param suspended: Suspended indicates if a user has suspended a connection or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#suspended IntegrationConnectorsConnection#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#timeouts IntegrationConnectorsConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ed424ced18e1b0129b97a14ca05975280338b1a83a03daa820213d1ae60c8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IntegrationConnectorsConnectionConfig(
            connector_version=connector_version,
            location=location,
            name=name,
            auth_config=auth_config,
            config_variable=config_variable,
            description=description,
            destination_config=destination_config,
            eventing_config=eventing_config,
            eventing_enablement_type=eventing_enablement_type,
            id=id,
            labels=labels,
            lock_config=lock_config,
            log_config=log_config,
            node_config=node_config,
            project=project,
            service_account=service_account,
            ssl_config=ssl_config,
            suspended=suspended,
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
        '''Generates CDKTF code for importing a IntegrationConnectorsConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationConnectorsConnection to import.
        :param import_from_id: The id of the existing IntegrationConnectorsConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationConnectorsConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a00317b891b3174b3a93c18a4c1dfde6e8b3c31d3df02c803bab57db16246a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        *,
        auth_type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionAuthConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
        oauth2_auth_code_flow: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_jwt_bearer: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_key: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigSshPublicKey", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigUserPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["AUTH_TYPE_UNSPECIFIED", "USER_PASSWORD", "OAUTH2_JWT_BEARER", "OAUTH2_CLIENT_CREDENTIALS", "SSH_PUBLIC_KEY", "OAUTH2_AUTH_CODE_FLOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_type IntegrationConnectorsConnection#auth_type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_key IntegrationConnectorsConnection#auth_key}
        :param oauth2_auth_code_flow: oauth2_auth_code_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_auth_code_flow IntegrationConnectorsConnection#oauth2_auth_code_flow}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_client_credentials IntegrationConnectorsConnection#oauth2_client_credentials}
        :param oauth2_jwt_bearer: oauth2_jwt_bearer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_jwt_bearer IntegrationConnectorsConnection#oauth2_jwt_bearer}
        :param ssh_public_key: ssh_public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_public_key IntegrationConnectorsConnection#ssh_public_key}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#user_password IntegrationConnectorsConnection#user_password}
        '''
        value = IntegrationConnectorsConnectionAuthConfig(
            auth_type=auth_type,
            additional_variable=additional_variable,
            auth_key=auth_key,
            oauth2_auth_code_flow=oauth2_auth_code_flow,
            oauth2_client_credentials=oauth2_client_credentials,
            oauth2_jwt_bearer=oauth2_jwt_bearer,
            ssh_public_key=ssh_public_key,
            user_password=user_password,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthConfig", [value]))

    @jsii.member(jsii_name="putConfigVariable")
    def put_config_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionConfigVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84273e97476965f18853eca727fa9dfe089320562e30e199c31eee1f6ede7c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfigVariable", [value]))

    @jsii.member(jsii_name="putDestinationConfig")
    def put_destination_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionDestinationConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e227c9e340f2ca5b811c412d1a363f2afa555a779a7d75d3a6fa8ac208a3262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationConfig", [value]))

    @jsii.member(jsii_name="putEventingConfig")
    def put_eventing_config(
        self,
        *,
        registration_destination_config: typing.Union["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionEventingConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enrichment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registration_destination_config: registration_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#registration_destination_config IntegrationConnectorsConnection#registration_destination_config}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_config IntegrationConnectorsConnection#auth_config}
        :param enrichment_enabled: Enrichment Enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enrichment_enabled IntegrationConnectorsConnection#enrichment_enabled}
        '''
        value = IntegrationConnectorsConnectionEventingConfig(
            registration_destination_config=registration_destination_config,
            additional_variable=additional_variable,
            auth_config=auth_config,
            enrichment_enabled=enrichment_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putEventingConfig", [value]))

    @jsii.member(jsii_name="putLockConfig")
    def put_lock_config(
        self,
        *,
        locked: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param locked: Indicates whether or not the connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#locked IntegrationConnectorsConnection#locked}
        :param reason: Describes why a connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#reason IntegrationConnectorsConnection#reason}
        '''
        value = IntegrationConnectorsConnectionLockConfig(locked=locked, reason=reason)

        return typing.cast(None, jsii.invoke(self, "putLockConfig", [value]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enabled represents whether logging is enabled or not for a connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enabled IntegrationConnectorsConnection#enabled}
        :param level: Log configuration level. Possible values: ["LOG_LEVEL_UNSPECIFIED", "ERROR", "INFO", "DEBUG"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#level IntegrationConnectorsConnection#level}
        '''
        value = IntegrationConnectorsConnectionLogConfig(enabled=enabled, level=level)

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#max_node_count IntegrationConnectorsConnection#max_node_count}
        :param min_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#min_node_count IntegrationConnectorsConnection#min_node_count}
        '''
        value = IntegrationConnectorsConnectionNodeConfig(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putSslConfig")
    def put_ssl_config(
        self,
        *,
        type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionSslConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        client_cert_type: typing.Optional[builtins.str] = None,
        client_private_key: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigClientPrivateKey", typing.Dict[builtins.str, typing.Any]]] = None,
        client_private_key_pass: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass", typing.Dict[builtins.str, typing.Any]]] = None,
        private_server_certificate: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigPrivateServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        server_cert_type: typing.Optional[builtins.str] = None,
        trust_model: typing.Optional[builtins.str] = None,
        use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Enum for controlling the SSL Type (TLS/MTLS) Possible values: ["TLS", "MTLS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_certificate IntegrationConnectorsConnection#client_certificate}
        :param client_cert_type: Type of Client Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_cert_type IntegrationConnectorsConnection#client_cert_type}
        :param client_private_key: client_private_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_private_key IntegrationConnectorsConnection#client_private_key}
        :param client_private_key_pass: client_private_key_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_private_key_pass IntegrationConnectorsConnection#client_private_key_pass}
        :param private_server_certificate: private_server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#private_server_certificate IntegrationConnectorsConnection#private_server_certificate}
        :param server_cert_type: Type of Server Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#server_cert_type IntegrationConnectorsConnection#server_cert_type}
        :param trust_model: Enum for Trust Model Possible values: ["PUBLIC", "PRIVATE", "INSECURE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#trust_model IntegrationConnectorsConnection#trust_model}
        :param use_ssl: Bool for enabling SSL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#use_ssl IntegrationConnectorsConnection#use_ssl}
        '''
        value = IntegrationConnectorsConnectionSslConfig(
            type=type,
            additional_variable=additional_variable,
            client_certificate=client_certificate,
            client_cert_type=client_cert_type,
            client_private_key=client_private_key,
            client_private_key_pass=client_private_key_pass,
            private_server_certificate=private_server_certificate,
            server_cert_type=server_cert_type,
            trust_model=trust_model,
            use_ssl=use_ssl,
        )

        return typing.cast(None, jsii.invoke(self, "putSslConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#create IntegrationConnectorsConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#delete IntegrationConnectorsConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#update IntegrationConnectorsConnection#update}.
        '''
        value = IntegrationConnectorsConnectionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthConfig")
    def reset_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfig", []))

    @jsii.member(jsii_name="resetConfigVariable")
    def reset_config_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigVariable", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDestinationConfig")
    def reset_destination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationConfig", []))

    @jsii.member(jsii_name="resetEventingConfig")
    def reset_eventing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventingConfig", []))

    @jsii.member(jsii_name="resetEventingEnablementType")
    def reset_eventing_enablement_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventingEnablementType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLockConfig")
    def reset_lock_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockConfig", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetNodeConfig")
    def reset_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSslConfig")
    def reset_ssl_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslConfig", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

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
    @jsii.member(jsii_name="authConfig")
    def auth_config(self) -> "IntegrationConnectorsConnectionAuthConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigOutputReference", jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="configVariable")
    def config_variable(self) -> "IntegrationConnectorsConnectionConfigVariableList":
        return typing.cast("IntegrationConnectorsConnectionConfigVariableList", jsii.get(self, "configVariable"))

    @builtins.property
    @jsii.member(jsii_name="connectionRevision")
    def connection_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionRevision"))

    @builtins.property
    @jsii.member(jsii_name="connectorVersionInfraConfig")
    def connector_version_infra_config(
        self,
    ) -> "IntegrationConnectorsConnectionConnectorVersionInfraConfigList":
        return typing.cast("IntegrationConnectorsConnectionConnectorVersionInfraConfigList", jsii.get(self, "connectorVersionInfraConfig"))

    @builtins.property
    @jsii.member(jsii_name="connectorVersionLaunchStage")
    def connector_version_launch_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorVersionLaunchStage"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(
        self,
    ) -> "IntegrationConnectorsConnectionDestinationConfigList":
        return typing.cast("IntegrationConnectorsConnectionDestinationConfigList", jsii.get(self, "destinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="eventingConfig")
    def eventing_config(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionEventingConfigOutputReference", jsii.get(self, "eventingConfig"))

    @builtins.property
    @jsii.member(jsii_name="eventingRuntimeData")
    def eventing_runtime_data(
        self,
    ) -> "IntegrationConnectorsConnectionEventingRuntimeDataList":
        return typing.cast("IntegrationConnectorsConnectionEventingRuntimeDataList", jsii.get(self, "eventingRuntimeData"))

    @builtins.property
    @jsii.member(jsii_name="lockConfig")
    def lock_config(self) -> "IntegrationConnectorsConnectionLockConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionLockConfigOutputReference", jsii.get(self, "lockConfig"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "IntegrationConnectorsConnectionLogConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "IntegrationConnectorsConnectionNodeConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectory")
    def service_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceDirectory"))

    @builtins.property
    @jsii.member(jsii_name="sslConfig")
    def ssl_config(self) -> "IntegrationConnectorsConnectionSslConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionSslConfigOutputReference", jsii.get(self, "sslConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "IntegrationConnectorsConnectionStatusList":
        return typing.cast("IntegrationConnectorsConnectionStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionType")
    def subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionType"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IntegrationConnectorsConnectionTimeoutsOutputReference":
        return typing.cast("IntegrationConnectorsConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfig"], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="configVariableInput")
    def config_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionConfigVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionConfigVariable"]]], jsii.get(self, "configVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorVersionInput")
    def connector_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfigInput")
    def destination_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionDestinationConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionDestinationConfig"]]], jsii.get(self, "destinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventingConfigInput")
    def eventing_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfig"], jsii.get(self, "eventingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventingEnablementTypeInput")
    def eventing_enablement_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventingEnablementTypeInput"))

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
    @jsii.member(jsii_name="lockConfigInput")
    def lock_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionLockConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionLockConfig"], jsii.get(self, "lockConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionLogConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionNodeConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sslConfigInput")
    def ssl_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfig"], jsii.get(self, "sslConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationConnectorsConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationConnectorsConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorVersion")
    def connector_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorVersion"))

    @connector_version.setter
    def connector_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011e39a1b1f2d85ee191305d2530ae3c4fdcc4502ee819fd35087e4f20e8f03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9ef744f1753acb333a7d1456aaff823bc1e4bd48e1caf5c30b571dd42a833b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventingEnablementType")
    def eventing_enablement_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventingEnablementType"))

    @eventing_enablement_type.setter
    def eventing_enablement_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5bce9ef80de159f25eb2f8784146fa4da1a8e7fb1624f25b008ec218a5632f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventingEnablementType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c2fe7a9a5284c03816a925e4ea6b649d33167504294abd783e07348bc7573f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a52958684399fa0a584638f4ba39e6d7f4ca67e6779362957461493d3cee04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4621dab763df729a546a4f03577014271bd2321caf37e979b4daa0a16845eafe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db3d81fb9d602f8ba41146dba80262eefff7c2924525aa6de1bb8d426ecbeaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a5b13de17dedc70a6bf2a37d4931a4c082442f0e5f9036677f27b2f9f8c67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701852376e1734059b42ce6510eda7ceb701a6cbbd205919d81cef967ed15dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd662386050a6c5bc7a7f7493c31e699dc5699a357de9b809a715e4b6d6b27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "additional_variable": "additionalVariable",
        "auth_key": "authKey",
        "oauth2_auth_code_flow": "oauth2AuthCodeFlow",
        "oauth2_client_credentials": "oauth2ClientCredentials",
        "oauth2_jwt_bearer": "oauth2JwtBearer",
        "ssh_public_key": "sshPublicKey",
        "user_password": "userPassword",
    },
)
class IntegrationConnectorsConnectionAuthConfig:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionAuthConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
        oauth2_auth_code_flow: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_jwt_bearer: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_key: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigSshPublicKey", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigUserPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["AUTH_TYPE_UNSPECIFIED", "USER_PASSWORD", "OAUTH2_JWT_BEARER", "OAUTH2_CLIENT_CREDENTIALS", "SSH_PUBLIC_KEY", "OAUTH2_AUTH_CODE_FLOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_type IntegrationConnectorsConnection#auth_type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_key IntegrationConnectorsConnection#auth_key}
        :param oauth2_auth_code_flow: oauth2_auth_code_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_auth_code_flow IntegrationConnectorsConnection#oauth2_auth_code_flow}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_client_credentials IntegrationConnectorsConnection#oauth2_client_credentials}
        :param oauth2_jwt_bearer: oauth2_jwt_bearer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_jwt_bearer IntegrationConnectorsConnection#oauth2_jwt_bearer}
        :param ssh_public_key: ssh_public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_public_key IntegrationConnectorsConnection#ssh_public_key}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#user_password IntegrationConnectorsConnection#user_password}
        '''
        if isinstance(oauth2_auth_code_flow, dict):
            oauth2_auth_code_flow = IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow(**oauth2_auth_code_flow)
        if isinstance(oauth2_client_credentials, dict):
            oauth2_client_credentials = IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials(**oauth2_client_credentials)
        if isinstance(oauth2_jwt_bearer, dict):
            oauth2_jwt_bearer = IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer(**oauth2_jwt_bearer)
        if isinstance(ssh_public_key, dict):
            ssh_public_key = IntegrationConnectorsConnectionAuthConfigSshPublicKey(**ssh_public_key)
        if isinstance(user_password, dict):
            user_password = IntegrationConnectorsConnectionAuthConfigUserPassword(**user_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784e43ea4ab00211fa80ed218e310b1f3bf1aa8e807d4f3d35b28fa853d9c40f)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument additional_variable", value=additional_variable, expected_type=type_hints["additional_variable"])
            check_type(argname="argument auth_key", value=auth_key, expected_type=type_hints["auth_key"])
            check_type(argname="argument oauth2_auth_code_flow", value=oauth2_auth_code_flow, expected_type=type_hints["oauth2_auth_code_flow"])
            check_type(argname="argument oauth2_client_credentials", value=oauth2_client_credentials, expected_type=type_hints["oauth2_client_credentials"])
            check_type(argname="argument oauth2_jwt_bearer", value=oauth2_jwt_bearer, expected_type=type_hints["oauth2_jwt_bearer"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
            check_type(argname="argument user_password", value=user_password, expected_type=type_hints["user_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }
        if additional_variable is not None:
            self._values["additional_variable"] = additional_variable
        if auth_key is not None:
            self._values["auth_key"] = auth_key
        if oauth2_auth_code_flow is not None:
            self._values["oauth2_auth_code_flow"] = oauth2_auth_code_flow
        if oauth2_client_credentials is not None:
            self._values["oauth2_client_credentials"] = oauth2_client_credentials
        if oauth2_jwt_bearer is not None:
            self._values["oauth2_jwt_bearer"] = oauth2_jwt_bearer
        if ssh_public_key is not None:
            self._values["ssh_public_key"] = ssh_public_key
        if user_password is not None:
            self._values["user_password"] = user_password

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''authType of the Connection Possible values: ["AUTH_TYPE_UNSPECIFIED", "USER_PASSWORD", "OAUTH2_JWT_BEARER", "OAUTH2_CLIENT_CREDENTIALS", "SSH_PUBLIC_KEY", "OAUTH2_AUTH_CODE_FLOW"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_type IntegrationConnectorsConnection#auth_type}
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionAuthConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionAuthConfigAdditionalVariable"]]], result)

    @builtins.property
    def auth_key(self) -> typing.Optional[builtins.str]:
        '''The type of authentication configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_key IntegrationConnectorsConnection#auth_key}
        '''
        result = self._values.get("auth_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_auth_code_flow(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow"]:
        '''oauth2_auth_code_flow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_auth_code_flow IntegrationConnectorsConnection#oauth2_auth_code_flow}
        '''
        result = self._values.get("oauth2_auth_code_flow")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow"], result)

    @builtins.property
    def oauth2_client_credentials(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials"]:
        '''oauth2_client_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_client_credentials IntegrationConnectorsConnection#oauth2_client_credentials}
        '''
        result = self._values.get("oauth2_client_credentials")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials"], result)

    @builtins.property
    def oauth2_jwt_bearer(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer"]:
        '''oauth2_jwt_bearer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#oauth2_jwt_bearer IntegrationConnectorsConnection#oauth2_jwt_bearer}
        '''
        result = self._values.get("oauth2_jwt_bearer")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer"], result)

    @builtins.property
    def ssh_public_key(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKey"]:
        '''ssh_public_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_public_key IntegrationConnectorsConnection#ssh_public_key}
        '''
        result = self._values.get("ssh_public_key")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKey"], result)

    @builtins.property
    def user_password(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPassword"]:
        '''user_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#user_password IntegrationConnectorsConnection#user_password}
        '''
        result = self._values.get("user_password")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPassword"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariable",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "boolean_value": "booleanValue",
        "encryption_key_value": "encryptionKeyValue",
        "integer_value": "integerValue",
        "secret_value": "secretValue",
        "string_value": "stringValue",
    },
)
class IntegrationConnectorsConnectionAuthConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad852eb4a85850bdb1dcdfabe6ca77c863a1b56ee7064eab1d34a366d59e6ef5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
            check_type(argname="argument encryption_key_value", value=encryption_key_value, expected_type=type_hints["encryption_key_value"])
            check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if boolean_value is not None:
            self._values["boolean_value"] = boolean_value
        if encryption_key_value is not None:
            self._values["encryption_key_value"] = encryption_key_value
        if integer_value is not None:
            self._values["integer_value"] = integer_value
        if secret_value is not None:
            self._values["secret_value"] = secret_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "kms_key_name": "kmsKeyName"},
)
class IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cac7353988c945adb1ccad90ec8370291accde639805d0148e7e4e0bfe2a8f3)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The [KMS key name] with which the content of the Operation is encrypted.

        The
        expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*.
        Will be empty string if google managed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d42bb49dd07bd34b58c814fb9dc63b61e6a11e02cf11af39f4b263175833244)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bc6f028dc670f3f8e7273f8e41bcfff1b68aa9848735d4b08995928ab97c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e057682f59cebef43654809b96e524fe015930a8a295e3417b753fd884525144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7149291fa5c044da5cf48d9bb6b08984bb640cf133776c102924596b988b3798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionAuthConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__662be42e95855c79d323de57fe355f91bb807a66b0caf32ff4bc9f269616eb6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5662ad4db4f9ad4816ae149b9ed3492972e61ff27f5cae0f31a4b51246f434f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f244590e71adfed8c59ecc9209c5beb1556583c5d37e3e9d25480b6a5ff167)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8f22312e03ff886af12b0c691f2bde39a756e061b8c60bb70c43e62e8dd2b95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0256b910c770e2363a591f73313842fd1abf44d451c29bd3d516832ea858169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ade69a634c001f2a4b67e826992ffb7115bf9617fe451785c116b091be8e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3143f95409ccbdfaea1449ee38c70d419ac277aad660acdb3269eb5865f7d02f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKeyValue")
    def put_encryption_key_value(
        self,
        *,
        type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue(
            type=type, kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretValue", [value]))

    @jsii.member(jsii_name="resetBooleanValue")
    def reset_boolean_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanValue", []))

    @jsii.member(jsii_name="resetEncryptionKeyValue")
    def reset_encryption_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyValue", []))

    @jsii.member(jsii_name="resetIntegerValue")
    def reset_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerValue", []))

    @jsii.member(jsii_name="resetSecretValue")
    def reset_secret_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValue")
    def encryption_key_value(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="booleanValueInput")
    def boolean_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "booleanValueInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValueInput")
    def encryption_key_value_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="integerValueInput")
    def integer_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValueInput")
    def secret_value_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "booleanValue"))

    @boolean_value.setter
    def boolean_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343c38f73982243545debaa90e19cb038a026cd5a3ea397b310c169f531eee21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e3efc39c132f840bfad35574c3a3b39b6599a1be163c9d6190ab9da8fafbf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fc770a600aa85d86eb91da48b4004dc1fc6f56722051ecc10e3bd843957796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7029cf313dc754473a4c67bad19a3f498fb4750ecdfdc4c7ea1e3033855e8de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionAuthConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionAuthConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e6ee263a6ac9f7e745ce998c727ad241d38f35ca333ff4636bc65146e31207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c040f19174e193c815b422a1bf23802ab9147b84f009e7a98c6be469ad5b298)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__448c6703331298500c67a87a9209ff52bb82604679aef5943639dcd28f35a871)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de399d3f845f36534e79855043f320ce6160f2ea8dbc00506b1beb26ef0b72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c726b8d2477437dda972dc10bb35083cd7fedc176b5ada54528b761af7d0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow",
    jsii_struct_bases=[],
    name_mapping={
        "auth_uri": "authUri",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enable_pkce": "enablePkce",
        "scopes": "scopes",
    },
)
class IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow:
    def __init__(
        self,
        *,
        auth_uri: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_pkce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param auth_uri: Auth URL for Authorization Code Flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_uri IntegrationConnectorsConnection#auth_uri}
        :param client_id: Client ID for user-provided OAuth app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_id IntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_secret IntegrationConnectorsConnection#client_secret}
        :param enable_pkce: Whether to enable PKCE when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enable_pkce IntegrationConnectorsConnection#enable_pkce}
        :param scopes: Scopes the connection will request when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#scopes IntegrationConnectorsConnection#scopes}
        '''
        if isinstance(client_secret, dict):
            client_secret = IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret(**client_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a3e824fd69e5644b951dc09e4ac028ac6c8764ad1edfcd9f17ca37ed510f45)
            check_type(argname="argument auth_uri", value=auth_uri, expected_type=type_hints["auth_uri"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument enable_pkce", value=enable_pkce, expected_type=type_hints["enable_pkce"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_uri is not None:
            self._values["auth_uri"] = auth_uri
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if enable_pkce is not None:
            self._values["enable_pkce"] = enable_pkce
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def auth_uri(self) -> typing.Optional[builtins.str]:
        '''Auth URL for Authorization Code Flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_uri IntegrationConnectorsConnection#auth_uri}
        '''
        result = self._values.get("auth_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID for user-provided OAuth app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_id IntegrationConnectorsConnection#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret"]:
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_secret IntegrationConnectorsConnection#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret"], result)

    @builtins.property
    def enable_pkce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable PKCE when the user performs the auth code flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enable_pkce IntegrationConnectorsConnection#enable_pkce}
        '''
        result = self._values.get("enable_pkce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Scopes the connection will request when the user performs the auth code flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#scopes IntegrationConnectorsConnection#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3659af668cce19ed566ebcb7ab9d4a5d11e0e455137cc092f7a342394dd3f3a2)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c00906b01652edcf1e55631a13ccfe8c92a82043ea41d091f71cca8426c5d7f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880b72f1eae9b7da205303c5a9041f19bfaf7141bcb45635e1fbbe24cf41f6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5ff28718b44518ef65177543ce6855369dd8f576a81f755195570c92b3a090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1212b1e76965464186c7474c9ef83b3e0a2afb997c029c5e6ddc67dea1eff129)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientSecret", [value]))

    @jsii.member(jsii_name="resetAuthUri")
    def reset_auth_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUri", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetEnablePkce")
    def reset_enable_pkce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePkce", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="authUriInput")
    def auth_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUriInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePkceInput")
    def enable_pkce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePkceInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="authUri")
    def auth_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authUri"))

    @auth_uri.setter
    def auth_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6eb694122fefad1107aed1630e73aee827084c7b9c10fecd30ffeec3ee7844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c446562b99928eb5af4a43d744d0ca276c0535e54e1dfcfea1e23178b85763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePkce")
    def enable_pkce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePkce"))

    @enable_pkce.setter
    def enable_pkce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60acf325ec07ed2fa9132726f454ab728472f297e94796a13543be18e30cd4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePkce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7437455f218efa3c5ab4e41496c325f9278f466d96ddce7d551cb58aa1b58675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1605fa2e576fabe03013678569f7ae54cc6b68988f8b5a502f5dd1188014eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Secret version of Password for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_id IntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_secret IntegrationConnectorsConnection#client_secret}
        '''
        if isinstance(client_secret, dict):
            client_secret = IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret(**client_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5a7a2112d59af611f4dfa360f3962c3620496786c313182f935fcce6f1f5ac)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Secret version of Password for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_id IntegrationConnectorsConnection#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret"]:
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_secret IntegrationConnectorsConnection#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b5561dbc28528ac2d0865e9a836ea3974ad432999522ef5c8895d0b9cac62c)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6263f7018336d6515f7e9671fcc83b60485adc71e6cc2d0788dc6b90108bcc5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a718830e2a8756f3527e6d95822b2c942a75ed2722c6a7fb791e7f628d62b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd8387be9b223f4426bc6f85b8bd8b64ad6a6f6bd412481bdce9b941b5bc01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__990b17338703eac47557ce0e10a87d6a34d495fe31e623228ce6a96368e35771)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientSecret", [value]))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c902e473b4731e59105593ce8c1e5e0bdf23281564caae0e1e1de4ca73e1102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07dc6455dadf80f85a2312bbcbda6b6d5a435203311e0b59923867607f6fb685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer",
    jsii_struct_bases=[],
    name_mapping={"client_key": "clientKey", "jwt_claims": "jwtClaims"},
)
class IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer:
    def __init__(
        self,
        *,
        client_key: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_claims: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_key: client_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_key IntegrationConnectorsConnection#client_key}
        :param jwt_claims: jwt_claims block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#jwt_claims IntegrationConnectorsConnection#jwt_claims}
        '''
        if isinstance(client_key, dict):
            client_key = IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey(**client_key)
        if isinstance(jwt_claims, dict):
            jwt_claims = IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims(**jwt_claims)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1134d1bf31a2a72cac1ed9bca86aba587208e19e9d25a5a0f5a18a0ad988cf23)
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument jwt_claims", value=jwt_claims, expected_type=type_hints["jwt_claims"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_key is not None:
            self._values["client_key"] = client_key
        if jwt_claims is not None:
            self._values["jwt_claims"] = jwt_claims

    @builtins.property
    def client_key(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey"]:
        '''client_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_key IntegrationConnectorsConnection#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey"], result)

    @builtins.property
    def jwt_claims(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims"]:
        '''jwt_claims block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#jwt_claims IntegrationConnectorsConnection#jwt_claims}
        '''
        result = self._values.get("jwt_claims")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435739f68d806f919644cd5bc59532128511408b6e5dac6d56e6ea240ddbc022)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38623a645a4fb24776eaf085c22ee0d62e9ae715edb10b39b51d4c00f915cb6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec65651930ba4215d584f4c44dd8d4ad34c42bf7b70680783b16c51a5f024bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a5a369ceafe1ceff68d07f39f7a2659fa877c1a4b7bdbf0eaf2842211367fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims",
    jsii_struct_bases=[],
    name_mapping={"audience": "audience", "issuer": "issuer", "subject": "subject"},
)
class IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims:
    def __init__(
        self,
        *,
        audience: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audience: Value for the "aud" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#audience IntegrationConnectorsConnection#audience}
        :param issuer: Value for the "iss" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#issuer IntegrationConnectorsConnection#issuer}
        :param subject: Value for the "sub" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#subject IntegrationConnectorsConnection#subject}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fa20f27fac590a12d7aa45dd24adf4e2064d0f78f9c8a9776f29b5eae279b1)
            check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audience is not None:
            self._values["audience"] = audience
        if issuer is not None:
            self._values["issuer"] = issuer
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def audience(self) -> typing.Optional[builtins.str]:
        '''Value for the "aud" claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#audience IntegrationConnectorsConnection#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''Value for the "iss" claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#issuer IntegrationConnectorsConnection#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''Value for the "sub" claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#subject IntegrationConnectorsConnection#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66469e25ff5b387773e599072d4be345297e993bf1220c8515388d1f0944a226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudience")
    def reset_audience(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudience", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @builtins.property
    @jsii.member(jsii_name="audienceInput")
    def audience_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audienceInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773ca9638c2b64aff8e5e17b0735828485d7d8861ef73e5915997569d7d84b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32984e58df442956da76256241a4c295f050e8a99f0c1d67c04b177b29914352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5047e8e4b01bec19586fc2cfc1aa55fb4f30b2e593bcf78555f2f96e5c9fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51641881b9473fb77beb67a9bdf38bd5fc8466a13f81e1f58f926d30221b2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a36387a63c6de7379176a008d9774f6a60ac0d7b0538a88ac4672dca7ac069)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientKey")
    def put_client_key(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientKey", [value]))

    @jsii.member(jsii_name="putJwtClaims")
    def put_jwt_claims(
        self,
        *,
        audience: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audience: Value for the "aud" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#audience IntegrationConnectorsConnection#audience}
        :param issuer: Value for the "iss" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#issuer IntegrationConnectorsConnection#issuer}
        :param subject: Value for the "sub" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#subject IntegrationConnectorsConnection#subject}
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims(
            audience=audience, issuer=issuer, subject=subject
        )

        return typing.cast(None, jsii.invoke(self, "putJwtClaims", [value]))

    @jsii.member(jsii_name="resetClientKey")
    def reset_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKey", []))

    @jsii.member(jsii_name="resetJwtClaims")
    def reset_jwt_claims(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtClaims", []))

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference, jsii.get(self, "clientKey"))

    @builtins.property
    @jsii.member(jsii_name="jwtClaims")
    def jwt_claims(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference, jsii.get(self, "jwtClaims"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtClaimsInput")
    def jwt_claims_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims], jsii.get(self, "jwtClaimsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35ae054dc09f2a6382992d4c4b055ff4da9a7b386f458bacf51c3c15c408cce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0498631f945041a4e83c819633b0384a90750e8bfb5ae3180014e3cc059ea15c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab60f2ab93607affbe048028fa7f13d1fdd597e46a3ebdedae447f1c69cdb25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putOauth2AuthCodeFlow")
    def put_oauth2_auth_code_flow(
        self,
        *,
        auth_uri: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_pkce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param auth_uri: Auth URL for Authorization Code Flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_uri IntegrationConnectorsConnection#auth_uri}
        :param client_id: Client ID for user-provided OAuth app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_id IntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_secret IntegrationConnectorsConnection#client_secret}
        :param enable_pkce: Whether to enable PKCE when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enable_pkce IntegrationConnectorsConnection#enable_pkce}
        :param scopes: Scopes the connection will request when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#scopes IntegrationConnectorsConnection#scopes}
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow(
            auth_uri=auth_uri,
            client_id=client_id,
            client_secret=client_secret,
            enable_pkce=enable_pkce,
            scopes=scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2AuthCodeFlow", [value]))

    @jsii.member(jsii_name="putOauth2ClientCredentials")
    def put_oauth2_client_credentials(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Secret version of Password for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_id IntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_secret IntegrationConnectorsConnection#client_secret}
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2ClientCredentials", [value]))

    @jsii.member(jsii_name="putOauth2JwtBearer")
    def put_oauth2_jwt_bearer(
        self,
        *,
        client_key: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey, typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_claims: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_key: client_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_key IntegrationConnectorsConnection#client_key}
        :param jwt_claims: jwt_claims block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#jwt_claims IntegrationConnectorsConnection#jwt_claims}
        '''
        value = IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer(
            client_key=client_key, jwt_claims=jwt_claims
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2JwtBearer", [value]))

    @jsii.member(jsii_name="putSshPublicKey")
    def put_ssh_public_key(
        self,
        *,
        username: builtins.str,
        cert_type: typing.Optional[builtins.str] = None,
        ssh_client_cert: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_client_cert_pass: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: The user account used to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        :param cert_type: Format of SSH Client cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#cert_type IntegrationConnectorsConnection#cert_type}
        :param ssh_client_cert: ssh_client_cert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_client_cert IntegrationConnectorsConnection#ssh_client_cert}
        :param ssh_client_cert_pass: ssh_client_cert_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_client_cert_pass IntegrationConnectorsConnection#ssh_client_cert_pass}
        '''
        value = IntegrationConnectorsConnectionAuthConfigSshPublicKey(
            username=username,
            cert_type=cert_type,
            ssh_client_cert=ssh_client_cert,
            ssh_client_cert_pass=ssh_client_cert_pass,
        )

        return typing.cast(None, jsii.invoke(self, "putSshPublicKey", [value]))

    @jsii.member(jsii_name="putUserPassword")
    def put_user_password(
        self,
        *,
        username: builtins.str,
        password: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#password IntegrationConnectorsConnection#password}
        '''
        value = IntegrationConnectorsConnectionAuthConfigUserPassword(
            username=username, password=password
        )

        return typing.cast(None, jsii.invoke(self, "putUserPassword", [value]))

    @jsii.member(jsii_name="resetAdditionalVariable")
    def reset_additional_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalVariable", []))

    @jsii.member(jsii_name="resetAuthKey")
    def reset_auth_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthKey", []))

    @jsii.member(jsii_name="resetOauth2AuthCodeFlow")
    def reset_oauth2_auth_code_flow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2AuthCodeFlow", []))

    @jsii.member(jsii_name="resetOauth2ClientCredentials")
    def reset_oauth2_client_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2ClientCredentials", []))

    @jsii.member(jsii_name="resetOauth2JwtBearer")
    def reset_oauth2_jwt_bearer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2JwtBearer", []))

    @jsii.member(jsii_name="resetSshPublicKey")
    def reset_ssh_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicKey", []))

    @jsii.member(jsii_name="resetUserPassword")
    def reset_user_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPassword", []))

    @builtins.property
    @jsii.member(jsii_name="additionalVariable")
    def additional_variable(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigAdditionalVariableList:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthCodeFlow")
    def oauth2_auth_code_flow(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference, jsii.get(self, "oauth2AuthCodeFlow"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentials")
    def oauth2_client_credentials(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference, jsii.get(self, "oauth2ClientCredentials"))

    @builtins.property
    @jsii.member(jsii_name="oauth2JwtBearer")
    def oauth2_jwt_bearer(
        self,
    ) -> IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference:
        return typing.cast(IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference, jsii.get(self, "oauth2JwtBearer"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(
        self,
    ) -> "IntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference", jsii.get(self, "sshPublicKey"))

    @builtins.property
    @jsii.member(jsii_name="userPassword")
    def user_password(
        self,
    ) -> "IntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference", jsii.get(self, "userPassword"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="authKeyInput")
    def auth_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthCodeFlowInput")
    def oauth2_auth_code_flow_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow], jsii.get(self, "oauth2AuthCodeFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsInput")
    def oauth2_client_credentials_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials], jsii.get(self, "oauth2ClientCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2JwtBearerInput")
    def oauth2_jwt_bearer_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer], jsii.get(self, "oauth2JwtBearerInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKey"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKey"], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordInput")
    def user_password_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPassword"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPassword"], jsii.get(self, "userPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authKey")
    def auth_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authKey"))

    @auth_key.setter
    def auth_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a447f8c756418a42daf254d9f7e0037b6e0c47650e74e00995084c0b8075b17f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab731dcb72d933fd34ee98543eb7aff041843daa848a3e6c6eb83cb1614bb5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8aa4fc2af2e16df5c0dad27f7caca1604b7ab27f5fc1d742331d3d242586319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigSshPublicKey",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "cert_type": "certType",
        "ssh_client_cert": "sshClientCert",
        "ssh_client_cert_pass": "sshClientCertPass",
    },
)
class IntegrationConnectorsConnectionAuthConfigSshPublicKey:
    def __init__(
        self,
        *,
        username: builtins.str,
        cert_type: typing.Optional[builtins.str] = None,
        ssh_client_cert: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_client_cert_pass: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: The user account used to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        :param cert_type: Format of SSH Client cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#cert_type IntegrationConnectorsConnection#cert_type}
        :param ssh_client_cert: ssh_client_cert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_client_cert IntegrationConnectorsConnection#ssh_client_cert}
        :param ssh_client_cert_pass: ssh_client_cert_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_client_cert_pass IntegrationConnectorsConnection#ssh_client_cert_pass}
        '''
        if isinstance(ssh_client_cert, dict):
            ssh_client_cert = IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert(**ssh_client_cert)
        if isinstance(ssh_client_cert_pass, dict):
            ssh_client_cert_pass = IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass(**ssh_client_cert_pass)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c3b42e94ccd57b919a1b9aa98101a9f2c6eba765d752e118806cf273c7a4f8)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument cert_type", value=cert_type, expected_type=type_hints["cert_type"])
            check_type(argname="argument ssh_client_cert", value=ssh_client_cert, expected_type=type_hints["ssh_client_cert"])
            check_type(argname="argument ssh_client_cert_pass", value=ssh_client_cert_pass, expected_type=type_hints["ssh_client_cert_pass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if cert_type is not None:
            self._values["cert_type"] = cert_type
        if ssh_client_cert is not None:
            self._values["ssh_client_cert"] = ssh_client_cert
        if ssh_client_cert_pass is not None:
            self._values["ssh_client_cert_pass"] = ssh_client_cert_pass

    @builtins.property
    def username(self) -> builtins.str:
        '''The user account used to authenticate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cert_type(self) -> typing.Optional[builtins.str]:
        '''Format of SSH Client cert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#cert_type IntegrationConnectorsConnection#cert_type}
        '''
        result = self._values.get("cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_client_cert(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"]:
        '''ssh_client_cert block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_client_cert IntegrationConnectorsConnection#ssh_client_cert}
        '''
        result = self._values.get("ssh_client_cert")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"], result)

    @builtins.property
    def ssh_client_cert_pass(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"]:
        '''ssh_client_cert_pass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssh_client_cert_pass IntegrationConnectorsConnection#ssh_client_cert_pass}
        '''
        result = self._values.get("ssh_client_cert_pass")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigSshPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__875de16295b8bb218274524698334146f771316c92d880ea513fa64eb8534393)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSshClientCert")
    def put_ssh_client_cert(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSshClientCert", [value]))

    @jsii.member(jsii_name="putSshClientCertPass")
    def put_ssh_client_cert_pass(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSshClientCertPass", [value]))

    @jsii.member(jsii_name="resetCertType")
    def reset_cert_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertType", []))

    @jsii.member(jsii_name="resetSshClientCert")
    def reset_ssh_client_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshClientCert", []))

    @jsii.member(jsii_name="resetSshClientCertPass")
    def reset_ssh_client_cert_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshClientCertPass", []))

    @builtins.property
    @jsii.member(jsii_name="sshClientCert")
    def ssh_client_cert(
        self,
    ) -> "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference", jsii.get(self, "sshClientCert"))

    @builtins.property
    @jsii.member(jsii_name="sshClientCertPass")
    def ssh_client_cert_pass(
        self,
    ) -> "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference", jsii.get(self, "sshClientCertPass"))

    @builtins.property
    @jsii.member(jsii_name="certTypeInput")
    def cert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sshClientCertInput")
    def ssh_client_cert_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"], jsii.get(self, "sshClientCertInput"))

    @builtins.property
    @jsii.member(jsii_name="sshClientCertPassInput")
    def ssh_client_cert_pass_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"], jsii.get(self, "sshClientCertPassInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="certType")
    def cert_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certType"))

    @cert_type.setter
    def cert_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc906f1334c2a54156bf92ead2b808bf0be53559fd7abef5c706924840e1ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2464ae0689f286d2968bf1065263463c056b90216c03978963c03c2991aa795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKey]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be62cddfef9127429277e1e5b5299280aa7fa9282a8453b72f5954a35dc4bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36756f83dffc7f35b4696099ffd39b831c963322a17ed6bf9fd57a669d5e930a)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0403215a7c1db16d07861f2c50b6acee0b8124e98b89ef2f85713b844442833e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6dd6d310e7ae051196c1cfcbd2a64cf3fef0b6e0531c90bb92903efc319d745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ec8c73ca20e33767e5de2105b9a95686bbb74a9287cfabd68c9e91bd51f100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2440f9943abdf84643a484466f000d0e676a6083d516d20a536bc5054de75b40)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d6bb0b62325f87d0f615d9d8822d5ec06b1010e08fe374383c73323655d9b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e05a63a64ccc2ee8899927c8521cc9c6c65fb247fd603ef4ca39c8c03984ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec955341fb0791f692977c3505ee2ae9a51d261b05f1d1edbd8ef00b1b0d918e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigUserPassword",
    jsii_struct_bases=[],
    name_mapping={"username": "username", "password": "password"},
)
class IntegrationConnectorsConnectionAuthConfigUserPassword:
    def __init__(
        self,
        *,
        username: builtins.str,
        password: typing.Optional[typing.Union["IntegrationConnectorsConnectionAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#password IntegrationConnectorsConnection#password}
        '''
        if isinstance(password, dict):
            password = IntegrationConnectorsConnectionAuthConfigUserPasswordPassword(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23a9118569e9f15d606ccb0c5426ad81c8a028d8210e106613a14beb3f30c1d)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPasswordPassword"]:
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#password IntegrationConnectorsConnection#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPasswordPassword"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigUserPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78344d79b5cfb9e23263e8cb6f5809f1c87d8b7dbe6636e1ad853e1ee9c4cbc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPassword")
    def put_password(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionAuthConfigUserPasswordPassword(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putPassword", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(
        self,
    ) -> "IntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference":
        return typing.cast("IntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPasswordPassword"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionAuthConfigUserPasswordPassword"], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c1caa7157704361f44f3c3df7ced1aacb24c691c0880542ae47ef093f99de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPassword]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0ce275fcda12bcf22c49101ab929100248feabd782dbfe1abd0d0f5fabf612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigUserPasswordPassword",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionAuthConfigUserPasswordPassword:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2db0ebbe5fdac3c686e663151dc44a498d6516c79cb24577316fcf5e7adbaa)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionAuthConfigUserPasswordPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24ae7f003e6dd523dd55e24026c1c7a6fffc09182222c30c07bf8c2edd48f9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c005c01403a1a538f7d95651ead03f2f8d06cd2e5f656a2923ffd370751b0a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPasswordPassword]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPasswordPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPasswordPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a92b4d3fd757de4cf3e88342cb40ec9c45a820c62d4f7a89ea56e761d9f455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connector_version": "connectorVersion",
        "location": "location",
        "name": "name",
        "auth_config": "authConfig",
        "config_variable": "configVariable",
        "description": "description",
        "destination_config": "destinationConfig",
        "eventing_config": "eventingConfig",
        "eventing_enablement_type": "eventingEnablementType",
        "id": "id",
        "labels": "labels",
        "lock_config": "lockConfig",
        "log_config": "logConfig",
        "node_config": "nodeConfig",
        "project": "project",
        "service_account": "serviceAccount",
        "ssl_config": "sslConfig",
        "suspended": "suspended",
        "timeouts": "timeouts",
    },
)
class IntegrationConnectorsConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connector_version: builtins.str,
        location: builtins.str,
        name: builtins.str,
        auth_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionConfigVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionDestinationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        eventing_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        eventing_enablement_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lock_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionLockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["IntegrationConnectorsConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connector_version: connectorVersion of the Connector. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#connector_version IntegrationConnectorsConnection#connector_version}
        :param location: Location in which Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#location IntegrationConnectorsConnection#location}
        :param name: Name of Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#name IntegrationConnectorsConnection#name}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_config IntegrationConnectorsConnection#auth_config}
        :param config_variable: config_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#config_variable IntegrationConnectorsConnection#config_variable}
        :param description: An arbitrary description for the Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#description IntegrationConnectorsConnection#description}
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination_config IntegrationConnectorsConnection#destination_config}
        :param eventing_config: eventing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#eventing_config IntegrationConnectorsConnection#eventing_config}
        :param eventing_enablement_type: Eventing enablement type. Will be nil if eventing is not enabled. Possible values: ["EVENTING_AND_CONNECTION", "ONLY_EVENTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#eventing_enablement_type IntegrationConnectorsConnection#eventing_enablement_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#id IntegrationConnectorsConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#labels IntegrationConnectorsConnection#labels}
        :param lock_config: lock_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#lock_config IntegrationConnectorsConnection#lock_config}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#log_config IntegrationConnectorsConnection#log_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#node_config IntegrationConnectorsConnection#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#project IntegrationConnectorsConnection#project}.
        :param service_account: Service account needed for runtime plane to access Google Cloud resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_account IntegrationConnectorsConnection#service_account}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssl_config IntegrationConnectorsConnection#ssl_config}
        :param suspended: Suspended indicates if a user has suspended a connection or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#suspended IntegrationConnectorsConnection#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#timeouts IntegrationConnectorsConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_config, dict):
            auth_config = IntegrationConnectorsConnectionAuthConfig(**auth_config)
        if isinstance(eventing_config, dict):
            eventing_config = IntegrationConnectorsConnectionEventingConfig(**eventing_config)
        if isinstance(lock_config, dict):
            lock_config = IntegrationConnectorsConnectionLockConfig(**lock_config)
        if isinstance(log_config, dict):
            log_config = IntegrationConnectorsConnectionLogConfig(**log_config)
        if isinstance(node_config, dict):
            node_config = IntegrationConnectorsConnectionNodeConfig(**node_config)
        if isinstance(ssl_config, dict):
            ssl_config = IntegrationConnectorsConnectionSslConfig(**ssl_config)
        if isinstance(timeouts, dict):
            timeouts = IntegrationConnectorsConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21924e6f83e1659bd056c72af7df8c23e7c8462f592d413b2a1346bf5cec424)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connector_version", value=connector_version, expected_type=type_hints["connector_version"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auth_config", value=auth_config, expected_type=type_hints["auth_config"])
            check_type(argname="argument config_variable", value=config_variable, expected_type=type_hints["config_variable"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument eventing_config", value=eventing_config, expected_type=type_hints["eventing_config"])
            check_type(argname="argument eventing_enablement_type", value=eventing_enablement_type, expected_type=type_hints["eventing_enablement_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument lock_config", value=lock_config, expected_type=type_hints["lock_config"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument ssl_config", value=ssl_config, expected_type=type_hints["ssl_config"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_version": connector_version,
            "location": location,
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
        if auth_config is not None:
            self._values["auth_config"] = auth_config
        if config_variable is not None:
            self._values["config_variable"] = config_variable
        if description is not None:
            self._values["description"] = description
        if destination_config is not None:
            self._values["destination_config"] = destination_config
        if eventing_config is not None:
            self._values["eventing_config"] = eventing_config
        if eventing_enablement_type is not None:
            self._values["eventing_enablement_type"] = eventing_enablement_type
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if lock_config is not None:
            self._values["lock_config"] = lock_config
        if log_config is not None:
            self._values["log_config"] = log_config
        if node_config is not None:
            self._values["node_config"] = node_config
        if project is not None:
            self._values["project"] = project
        if service_account is not None:
            self._values["service_account"] = service_account
        if ssl_config is not None:
            self._values["ssl_config"] = ssl_config
        if suspended is not None:
            self._values["suspended"] = suspended
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
    def connector_version(self) -> builtins.str:
        '''connectorVersion of the Connector.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#connector_version IntegrationConnectorsConnection#connector_version}
        '''
        result = self._values.get("connector_version")
        assert result is not None, "Required property 'connector_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location in which Connection needs to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#location IntegrationConnectorsConnection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of Connection needs to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#name IntegrationConnectorsConnection#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_config(self) -> typing.Optional[IntegrationConnectorsConnectionAuthConfig]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_config IntegrationConnectorsConnection#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionAuthConfig], result)

    @builtins.property
    def config_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionConfigVariable"]]]:
        '''config_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#config_variable IntegrationConnectorsConnection#config_variable}
        '''
        result = self._values.get("config_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionConfigVariable"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An arbitrary description for the Connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#description IntegrationConnectorsConnection#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionDestinationConfig"]]]:
        '''destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination_config IntegrationConnectorsConnection#destination_config}
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionDestinationConfig"]]], result)

    @builtins.property
    def eventing_config(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfig"]:
        '''eventing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#eventing_config IntegrationConnectorsConnection#eventing_config}
        '''
        result = self._values.get("eventing_config")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfig"], result)

    @builtins.property
    def eventing_enablement_type(self) -> typing.Optional[builtins.str]:
        '''Eventing enablement type. Will be nil if eventing is not enabled. Possible values: ["EVENTING_AND_CONNECTION", "ONLY_EVENTING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#eventing_enablement_type IntegrationConnectorsConnection#eventing_enablement_type}
        '''
        result = self._values.get("eventing_enablement_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#id IntegrationConnectorsConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#labels IntegrationConnectorsConnection#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lock_config(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionLockConfig"]:
        '''lock_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#lock_config IntegrationConnectorsConnection#lock_config}
        '''
        result = self._values.get("lock_config")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionLockConfig"], result)

    @builtins.property
    def log_config(self) -> typing.Optional["IntegrationConnectorsConnectionLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#log_config IntegrationConnectorsConnection#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionLogConfig"], result)

    @builtins.property
    def node_config(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#node_config IntegrationConnectorsConnection#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionNodeConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#project IntegrationConnectorsConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account needed for runtime plane to access Google Cloud resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_account IntegrationConnectorsConnection#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_config(self) -> typing.Optional["IntegrationConnectorsConnectionSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#ssl_config IntegrationConnectorsConnection#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfig"], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Suspended indicates if a user has suspended a connection or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#suspended IntegrationConnectorsConnection#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IntegrationConnectorsConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#timeouts IntegrationConnectorsConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariable",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "boolean_value": "booleanValue",
        "encryption_key_value": "encryptionKeyValue",
        "integer_value": "integerValue",
        "secret_value": "secretValue",
        "string_value": "stringValue",
    },
)
class IntegrationConnectorsConnectionConfigVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionConfigVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = IntegrationConnectorsConnectionConfigVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b16dea51d1aa468986fb801cc0dc053919676ee29c627496ab3f493a897281)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
            check_type(argname="argument encryption_key_value", value=encryption_key_value, expected_type=type_hints["encryption_key_value"])
            check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if boolean_value is not None:
            self._values["boolean_value"] = boolean_value
        if encryption_key_value is not None:
            self._values["encryption_key_value"] = encryption_key_value
        if integer_value is not None:
            self._values["integer_value"] = integer_value
        if secret_value is not None:
            self._values["secret_value"] = secret_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionConfigVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionConfigVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionConfigVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "kms_key_name": "kmsKeyName"},
)
class IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5ed5b76d3a450d63344b6bfa58ce7f917d3e183c4869a707db7dc7d203410f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The [KMS key name] with which the content of the Operation is encrypted.

        The
        expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*.
        Will be empty string if google managed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b3d5e98d9b31a2fc62c654b872822c5faa77fc52e9edd058b343f3c4bccebf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335bdd2f2a7ea410d8107120b883e2a2618b6112fcdb3373523c7a9947bd7d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481872c987275b771d7a6bdcacaae907cbc134b26131765dc295c756738a597d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97153987c9473d42989eee5a772d87721ce15145b4918c24964c42b00134bdb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionConfigVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9959da3773d3d7b9c8017b8c04a1883482cd38a91197a7349407c45932656f11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionConfigVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d8d7a63764f62f173a2b77af5199a2308adb855ccec0344fc0c4a1b519db81)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionConfigVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547fd4612a571870fbbf1511aff0431318d2b13410e32a9510a4fb9f321ce5bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec693580c3479c286b6cf68ab2879a5b995b05f0b9c9a832cd5ebc20c34b838a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a226a481c6ffe40e631656764057a0d7d4572e162fc7553daeaca09c8a038bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionConfigVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionConfigVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionConfigVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3f99656c0d625ce6b35d4e2acd41799cc448e0591e81a20d09b60bb58a1820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionConfigVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f09db8d1182257d29ea95cfc841aece3cb4092dbc865b0d961c4b1dcf21fc8fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKeyValue")
    def put_encryption_key_value(
        self,
        *,
        type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue(
            type=type, kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionConfigVariableSecretValue(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretValue", [value]))

    @jsii.member(jsii_name="resetBooleanValue")
    def reset_boolean_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanValue", []))

    @jsii.member(jsii_name="resetEncryptionKeyValue")
    def reset_encryption_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyValue", []))

    @jsii.member(jsii_name="resetIntegerValue")
    def reset_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerValue", []))

    @jsii.member(jsii_name="resetSecretValue")
    def reset_secret_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValue")
    def encryption_key_value(
        self,
    ) -> IntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference:
        return typing.cast(IntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "IntegrationConnectorsConnectionConfigVariableSecretValueOutputReference":
        return typing.cast("IntegrationConnectorsConnectionConfigVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="booleanValueInput")
    def boolean_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "booleanValueInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValueInput")
    def encryption_key_value_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="integerValueInput")
    def integer_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValueInput")
    def secret_value_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionConfigVariableSecretValue"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionConfigVariableSecretValue"], jsii.get(self, "secretValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "booleanValue"))

    @boolean_value.setter
    def boolean_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a12478e56458c64c2a551d8438fdd408b79de008c669afcb1dbba46c7d6e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1317ca2bbc7f9f92f0e74e088d75fbc1d84b4d15748e1061e2a7ce3649fdf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d87fd66d3424129e91cb22ebe41131b8790b20612131c7f1395332c59ddc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5189422edee0d4b60533490626c339d61acd4fda91d962b9875f572d6a1aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionConfigVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionConfigVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionConfigVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2308f61b37052b197efb725807d3f3902d46b7f4ebb8f02c6fe478a497b0c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionConfigVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f11312db5a590b8dabaac8dd3ebfd45f2da5667666f5fecb8b5773c4aa5e9f)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionConfigVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionConfigVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConfigVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7b502eb1e818d11ece6fcfecb7919ba0ae29f56c44e6d62fbf74971fe65900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b034265e0a079a9feba63d7d698d8dc0d8fa907e29b83d3780e773aeebf1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionConfigVariableSecretValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionConfigVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionConfigVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fa7a7e058ba893700d0ff47da58890dd3addf04287cd0d367ed19a4687f900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConnectorVersionInfraConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class IntegrationConnectorsConnectionConnectorVersionInfraConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionConnectorVersionInfraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionConnectorVersionInfraConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConnectorVersionInfraConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c369fa62736bc207acd9a8a36851f342e36f3b53ebb3dbfd9f04986d881f40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653089efe450ba8f3f6f2c7c3f70b09914fe15893dadbf140d0c83742b923615)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229a55644bdaec61361db40b9dea74e73a6a30dd1978bdb4529f7001666fea2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cd25ff0334860149dad1e907f5a68e94e981e36c20b1728223ad081673f993d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c34a05869baeafa41458bfe5e66120e787be2d60614f0d5e28cd26015129020e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b63ce40cf0ec8cd1dc45aa828ec2d3f5ef137a4f9afefad8de732ccf1a5b45a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ratelimitThreshold")
    def ratelimit_threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ratelimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionConnectorVersionInfraConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionConnectorVersionInfraConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionConnectorVersionInfraConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373be81b761bd4ff9b745b481565dd64b13b36f9bf46a46a9dab5582a2c86c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "destination": "destination"},
)
class IntegrationConnectorsConnectionDestinationConfig:
    def __init__(
        self,
        *,
        key: builtins.str,
        destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionDestinationConfigDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param key: The key is the destination identifier that is supported by the Connector. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination IntegrationConnectorsConnection#destination}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff9859246bb637bdafe4157ece9214258e9a348467e9f901b38dee2d90225a0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def key(self) -> builtins.str:
        '''The key is the destination identifier that is supported by the Connector.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionDestinationConfigDestination"]]]:
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination IntegrationConnectorsConnection#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionDestinationConfigDestination"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionDestinationConfigDestination",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "service_attachment": "serviceAttachment",
    },
)
class IntegrationConnectorsConnectionDestinationConfigDestination:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: For publicly routable host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#host IntegrationConnectorsConnection#host}
        :param port: The port is the target port number that is accepted by the destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#port IntegrationConnectorsConnection#port}
        :param service_attachment: PSC service attachments. Format: projects/* /regions/* /serviceAttachments/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_attachment IntegrationConnectorsConnection#service_attachment} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82921b34946b1f9a697b136da9beb4960df08c8efcccdf3b507a1332ff4f36e2)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service_attachment", value=service_attachment, expected_type=type_hints["service_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port
        if service_attachment is not None:
            self._values["service_attachment"] = service_attachment

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''For publicly routable host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#host IntegrationConnectorsConnection#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port is the target port number that is accepted by the destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#port IntegrationConnectorsConnection#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_attachment(self) -> typing.Optional[builtins.str]:
        '''PSC service attachments. Format: projects/* /regions/* /serviceAttachments/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_attachment IntegrationConnectorsConnection#service_attachment}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("service_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionDestinationConfigDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionDestinationConfigDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionDestinationConfigDestinationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4502cf2f0a9e9ab5fa1f48c725a2ec7a7ff3e8a0a7f101273d2af795e13d4b6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionDestinationConfigDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37df733460f51aaa553cafede5a5d7995ce01fc95bee6b1da113940eede0dcf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionDestinationConfigDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8104f03970ed4f446b35223dfe8d28fda18d21abe4265b236ddc4eadfb4f4736)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b7fe9a625df7dec7a380162f06a11f3e183d6dac07d6a389ffa38adf3a0355d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f495b08403c79a15a96f45a42924e7a1882179f23fc7dc91e3fc815a2dcd5b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfigDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfigDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0e5dbd41e788a0a7d3658a392ffd3ce8e5b8006e8d1c5e6442cdb0989216e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionDestinationConfigDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionDestinationConfigDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0ba8bc42178338beececee46d6125fa5148a916e960e912cf4d02761a13587e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetServiceAttachment")
    def reset_service_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAttachment", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachmentInput")
    def service_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04d18ed71779ba6cf0da1169b404ee8825115e33b921534218dacccee1bf712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1173e860adab330d59ee3a8540a9a422c94fe4b4c154f2b4985f75b416dee401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @service_attachment.setter
    def service_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043361124c7cfb71d21cc86255a5229f20453af2f2997795518894a522b0c67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfigDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfigDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfigDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3e2b844f48bc5e6dea517acc1ee423f4e432e3204a1b1ab7c48e59e52b576a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionDestinationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionDestinationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85510c6a0712a5d6a13dc6de690dc1f30bf312924c8b6ff29ad12fcc22e31e9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionDestinationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b8112f423f6cec7de179bc90288fdee4bf4c24bc9293b3329a1393117b5576)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionDestinationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e105bfdba81ed6f639775aa3d047b524cab21216cb1b480368b0909d8b43da19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a35f4e09f138aca33952d1732f74e8755123cd5d684cb49a62ed9a2d970307)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79dea1f14f7aa020f16c41be2751a072993ee9a365d433e6e73d0d40a4ba0676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98c4732a7405e43f08de4d1b0318ecc5a57e5a32adce0f43886bd55360863ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6f642f90251773f8621c4e9c701c6480f79b7ab512d8336966abbc8c7e688eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce0df16522d133826d7289b8f158d3240d4fd18e297d9f7326be6cbf256965d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(
        self,
    ) -> IntegrationConnectorsConnectionDestinationConfigDestinationList:
        return typing.cast(IntegrationConnectorsConnectionDestinationConfigDestinationList, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfigDestination]]], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a042472b120c2b9e100a1656301890858a55e7f78ffc42a17644dd134eeee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46607c9696caf7935c193d011470c89e5a9586aa492632d64bd662dfcd6a9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "registration_destination_config": "registrationDestinationConfig",
        "additional_variable": "additionalVariable",
        "auth_config": "authConfig",
        "enrichment_enabled": "enrichmentEnabled",
    },
)
class IntegrationConnectorsConnectionEventingConfig:
    def __init__(
        self,
        *,
        registration_destination_config: typing.Union["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionEventingConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enrichment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registration_destination_config: registration_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#registration_destination_config IntegrationConnectorsConnection#registration_destination_config}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_config IntegrationConnectorsConnection#auth_config}
        :param enrichment_enabled: Enrichment Enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enrichment_enabled IntegrationConnectorsConnection#enrichment_enabled}
        '''
        if isinstance(registration_destination_config, dict):
            registration_destination_config = IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig(**registration_destination_config)
        if isinstance(auth_config, dict):
            auth_config = IntegrationConnectorsConnectionEventingConfigAuthConfig(**auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8517027c90d3bf7e8529e2f469a05c2536d1c83309605809ee671deccc2a753b)
            check_type(argname="argument registration_destination_config", value=registration_destination_config, expected_type=type_hints["registration_destination_config"])
            check_type(argname="argument additional_variable", value=additional_variable, expected_type=type_hints["additional_variable"])
            check_type(argname="argument auth_config", value=auth_config, expected_type=type_hints["auth_config"])
            check_type(argname="argument enrichment_enabled", value=enrichment_enabled, expected_type=type_hints["enrichment_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "registration_destination_config": registration_destination_config,
        }
        if additional_variable is not None:
            self._values["additional_variable"] = additional_variable
        if auth_config is not None:
            self._values["auth_config"] = auth_config
        if enrichment_enabled is not None:
            self._values["enrichment_enabled"] = enrichment_enabled

    @builtins.property
    def registration_destination_config(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig":
        '''registration_destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#registration_destination_config IntegrationConnectorsConnection#registration_destination_config}
        '''
        result = self._values.get("registration_destination_config")
        assert result is not None, "Required property 'registration_destination_config' is missing"
        return typing.cast("IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig", result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionEventingConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionEventingConfigAdditionalVariable"]]], result)

    @builtins.property
    def auth_config(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfig"]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_config IntegrationConnectorsConnection#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfig"], result)

    @builtins.property
    def enrichment_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enrichment Enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enrichment_enabled IntegrationConnectorsConnection#enrichment_enabled}
        '''
        result = self._values.get("enrichment_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariable",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "boolean_value": "booleanValue",
        "encryption_key_value": "encryptionKeyValue",
        "integer_value": "integerValue",
        "secret_value": "secretValue",
        "string_value": "stringValue",
    },
)
class IntegrationConnectorsConnectionEventingConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61842c3e3dfa13ca809a4f99fa0b5774a81f2e8fc0eda934bb381513f33c681c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
            check_type(argname="argument encryption_key_value", value=encryption_key_value, expected_type=type_hints["encryption_key_value"])
            check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if boolean_value is not None:
            self._values["boolean_value"] = boolean_value
        if encryption_key_value is not None:
            self._values["encryption_key_value"] = encryption_key_value
        if integer_value is not None:
            self._values["integer_value"] = integer_value
        if secret_value is not None:
            self._values["secret_value"] = secret_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "type": "type"},
)
class IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7578fb67081ff8bf1dd9db6efb13b81e4dd0da1292f88852943e0245a7b5f95)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The [KMS key name] with which the content of the Operation is encrypted.

        The
        expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*.
        Will be empty string if google managed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f9c9e72ce5d3d5d2123938e68196c81644e2d9c1b75f41d9a5a06f98e69766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67eb8cb4f6ea48e5fb59a0dbd19550a403d96823d63533bd6a0fab78842c162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4179aabda6a84c810b341ae25cda567d4fccb26518865d049245ab7a291b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc2f1356ad0cfa5d5ce330d879be52c61f315aba1626ca980f1643f049852f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ba9b60947f155d37b1e318476d949c2ba0fdb43977d0bd09e1d0ce0044b3786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b74017e3f2b359f59983d27b58c45257ec32ddb795e44a1c706e3b240982325)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883cb532afb2b37209b45cca9925739a3345495af8b03ee11eb8ad07d1530f52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81eded52972033888d8821c7e988224b244842792b761e0d2d21003fb432088e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cadbfbaa555d320715aa26831386eab34d0b923bfaa3e9a817156106de17e12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314ea5875c225fc7275d91e204ccaf4977de70bb323a1900d532de410947cb9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5128fd9cdb7e99cba6729fdff9813a612b527f826c73550eafb48ba6dc41506d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKeyValue")
    def put_encryption_key_value(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        value = IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue(
            kms_key_name=kms_key_name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretValue", [value]))

    @jsii.member(jsii_name="resetBooleanValue")
    def reset_boolean_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanValue", []))

    @jsii.member(jsii_name="resetEncryptionKeyValue")
    def reset_encryption_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyValue", []))

    @jsii.member(jsii_name="resetIntegerValue")
    def reset_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerValue", []))

    @jsii.member(jsii_name="resetSecretValue")
    def reset_secret_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValue")
    def encryption_key_value(
        self,
    ) -> IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="booleanValueInput")
    def boolean_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "booleanValueInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValueInput")
    def encryption_key_value_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="integerValueInput")
    def integer_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValueInput")
    def secret_value_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "booleanValue"))

    @boolean_value.setter
    def boolean_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f479f7cb467d42bc68f31f29fa64637016e8931cc76e0ce56fecfd3bf6ca989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2cfffd696aa3e6fcc864f44f4c711b07028b862573c0b1a231338448c94bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ae7273b56cbf3bda93299cf6e7cef8219695830ed35618fde3c06939611ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d097d1cd0d346b81c7359ed18286b2db04966d31f83bbad2d67ad03497225ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aaf1b6ba3af48ce39afe395863e40b7f4793ec9492c405d12605ddf8d524501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8847f1e0b52123381f2d8b12b87181c09c24e7ea56a845f960cdf60c77cd42b)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffa5ada0a31e48c7ff94e91d648f18baf75f9c425c0514dc15bb83679d01f2ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9e7f8f584c0c618b700c7c4ef40f2125a169b7be47a877aa8a66f4ab97b14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611a051101f8b8c0495dc2217d3d8b01765df0ddbe013227a0f012c29a3146c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "user_password": "userPassword",
        "additional_variable": "additionalVariable",
        "auth_key": "authKey",
    },
)
class IntegrationConnectorsConnectionEventingConfigAuthConfig:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        user_password: typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword", typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["USER_PASSWORD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_type IntegrationConnectorsConnection#auth_type}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#user_password IntegrationConnectorsConnection#user_password}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_key IntegrationConnectorsConnection#auth_key}
        '''
        if isinstance(user_password, dict):
            user_password = IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword(**user_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698eb846aa157336fa307aa9676e5bc98d0b95d41b7fb7978ee9bf4587e93068)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument user_password", value=user_password, expected_type=type_hints["user_password"])
            check_type(argname="argument additional_variable", value=additional_variable, expected_type=type_hints["additional_variable"])
            check_type(argname="argument auth_key", value=auth_key, expected_type=type_hints["auth_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
            "user_password": user_password,
        }
        if additional_variable is not None:
            self._values["additional_variable"] = additional_variable
        if auth_key is not None:
            self._values["auth_key"] = auth_key

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''authType of the Connection Possible values: ["USER_PASSWORD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_type IntegrationConnectorsConnection#auth_type}
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_password(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword":
        '''user_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#user_password IntegrationConnectorsConnection#user_password}
        '''
        result = self._values.get("user_password")
        assert result is not None, "Required property 'user_password' is missing"
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword", result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable"]]], result)

    @builtins.property
    def auth_key(self) -> typing.Optional[builtins.str]:
        '''The type of authentication configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_key IntegrationConnectorsConnection#auth_key}
        '''
        result = self._values.get("auth_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "boolean_value": "booleanValue",
        "encryption_key_value": "encryptionKeyValue",
        "integer_value": "integerValue",
        "secret_value": "secretValue",
        "string_value": "stringValue",
    },
)
class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806f3a858a574eff78ab4908e5c7dd4e17cafd043300a4ae39494295849e1db5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
            check_type(argname="argument encryption_key_value", value=encryption_key_value, expected_type=type_hints["encryption_key_value"])
            check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if boolean_value is not None:
            self._values["boolean_value"] = boolean_value
        if encryption_key_value is not None:
            self._values["encryption_key_value"] = encryption_key_value
        if integer_value is not None:
            self._values["integer_value"] = integer_value
        if secret_value is not None:
            self._values["secret_value"] = secret_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "type": "type"},
)
class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d71816293fb20a913dfa3b0bfa377b5e900f895d28f0e08fc35a789175d67b2)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The [KMS key name] with which the content of the Operation is encrypted.

        The
        expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*.
        Will be empty string if google managed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9304305c41a8478e21aac4d7b74e4270f7340c13ce594c7c00f0897e2511a8a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfe3bafc4d3d0d2f4b402236b07929cba2748a742569d58d6d0bb1615c3dea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d617c73abea336468ca70920ac6800b50f5337d75d52c8366c678c0044b9a248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1153c31e27350cbe552e7633e27b69047040456ec8afe2805fe30060549f210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2942e29e8f17edee2266b872e3cf3ec13708622f2af11a6912f662c8025b5a11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2573d9cbbd1b24141fbf512bab7c9bf50438f4e677d5ee9e2aeff77a2898a210)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946643e54f5eb5d7c946ca06cbed28fd69d4ef1e75bf7fd59f81061c6372c9d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec7e20c717d588e960e6272495ca399792dcd5a76e78c8c910396a21a0164893)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfdaaa6440b20a3792d3ba3302b47c76975f5c7a046b427ffa7114fc18111061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1a36939e7ba5ef5b0376f9c59149302f20f17a9475e4dada07854b30fd3e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e33197bf0f720d457d4eba3a066b7a672094ec70b8f4dca8b83de473e9af4e80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKeyValue")
    def put_encryption_key_value(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        value = IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue(
            kms_key_name=kms_key_name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretValue", [value]))

    @jsii.member(jsii_name="resetBooleanValue")
    def reset_boolean_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanValue", []))

    @jsii.member(jsii_name="resetEncryptionKeyValue")
    def reset_encryption_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyValue", []))

    @jsii.member(jsii_name="resetIntegerValue")
    def reset_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerValue", []))

    @jsii.member(jsii_name="resetSecretValue")
    def reset_secret_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValue")
    def encryption_key_value(
        self,
    ) -> IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="booleanValueInput")
    def boolean_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "booleanValueInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValueInput")
    def encryption_key_value_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="integerValueInput")
    def integer_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValueInput")
    def secret_value_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "booleanValue"))

    @boolean_value.setter
    def boolean_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3dd88acbedd3c7ac1d875acd35a83d1ae26daea1132352f807e30c9a23b768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a2c7630127c8e02025c1e760dfe32f5073eb93d5df1e2834c7b26d8cf732fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342f7e5c26bf4dc7abd60f8ffae69c1e06d3e106100562a6ab7f3d2ff33b732c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143c66d9c6420749a27ccf6addfd6491c9902e307bf4b9f90bec4c8d0b3e3178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68d54640c2ab339895f51eed1213521d636a4d6872762d7f5ee2c5f9d55a2b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0136c4a5abba67772b4b0ec120e69cd16fb4a9e70409b433a2330770447b5b25)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90546002f128d679d73c23320c99aed5a19e5f48974e2c7f6e9dd33af7aff9ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab910ba5c3c5324744fb07c9a473b4d1ef4c7b125eb110cee4b9a73fc1ddbd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d084603317c1590ce6bfcfd4b8ff30456a7d103d834dfa1d86acb1a8a4c5460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cd52082b6d5d376aab67e2b3123983e6c69d2c8c9b74ae6f9173cf3593fb901)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70ab7bf161894d0363adfb3d97a329388499d021b8a4f14540dd538da83011d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putUserPassword")
    def put_user_password(
        self,
        *,
        password: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#password IntegrationConnectorsConnection#password}
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        '''
        value = IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putUserPassword", [value]))

    @jsii.member(jsii_name="resetAdditionalVariable")
    def reset_additional_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalVariable", []))

    @jsii.member(jsii_name="resetAuthKey")
    def reset_auth_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthKey", []))

    @builtins.property
    @jsii.member(jsii_name="additionalVariable")
    def additional_variable(
        self,
    ) -> IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList:
        return typing.cast(IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="userPassword")
    def user_password(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference":
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference", jsii.get(self, "userPassword"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="authKeyInput")
    def auth_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordInput")
    def user_password_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword"], jsii.get(self, "userPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authKey")
    def auth_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authKey"))

    @auth_key.setter
    def auth_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36270d5f4b9766da67458a4e8c251a4d2e1d47aa0c59b9fff4e63c8a0d18663f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d8257ee9429a60828dc23aed63b6293af4cc8a14d9e3d133f83b77cfcddcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43525b6f630644d866ece39b0597195692abede7086aa60fd51d60b5f5db025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword:
    def __init__(
        self,
        *,
        password: typing.Optional[typing.Union["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#password IntegrationConnectorsConnection#password}
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        '''
        if isinstance(password, dict):
            password = IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd33fc1e9b1e1783f85ca1b6d41f6ef857de2a24a49a89224e07f67d77908b39)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"]:
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#password IntegrationConnectorsConnection#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#username IntegrationConnectorsConnection#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98606598e02bdb786896da5fba5ca6aec82d70ef7067ed250f4cc2741746104e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPassword")
    def put_password(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putPassword", [value]))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference":
        return typing.cast("IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a56b236f7b1fbec51e54906454543f98bf23ccff33695aaed23743dcafab51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae95539a6269154ac576caa237e6bb0c61a0c1a0308422797efb40358fa5162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53c8e0efe597dd6fdf00d8ce1e64202012a3a1738796e77ddd7925c682e2290)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9375e8a2c9562a6e563c0910cbdf7fe0225bb31a2fe6f6ee7de8db0462066730)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4a55808f63aa9cf6c075641a236a5cf4d3607c26bc21b00960b7faa5fb9119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adeec5861c6febb420bb40b5e60da4fc9295ef79af9bff9b3f26e8be6c86b565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__102bd75de3bc9a05d7bef70e1ec280ff4ddede93f147acade6fc564290bcd542)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f28a5c90bdcd5e3e9b18128133c94703d86296e7dbb8383d77a78078a47d68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        *,
        auth_type: builtins.str,
        user_password: typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword, typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["USER_PASSWORD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_type IntegrationConnectorsConnection#auth_type}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#user_password IntegrationConnectorsConnection#user_password}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#auth_key IntegrationConnectorsConnection#auth_key}
        '''
        value = IntegrationConnectorsConnectionEventingConfigAuthConfig(
            auth_type=auth_type,
            user_password=user_password,
            additional_variable=additional_variable,
            auth_key=auth_key,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthConfig", [value]))

    @jsii.member(jsii_name="putRegistrationDestinationConfig")
    def put_registration_destination_config(
        self,
        *,
        destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination IntegrationConnectorsConnection#destination}
        :param key: Key for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        value = IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig(
            destination=destination, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putRegistrationDestinationConfig", [value]))

    @jsii.member(jsii_name="resetAdditionalVariable")
    def reset_additional_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalVariable", []))

    @jsii.member(jsii_name="resetAuthConfig")
    def reset_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfig", []))

    @jsii.member(jsii_name="resetEnrichmentEnabled")
    def reset_enrichment_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnrichmentEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="additionalVariable")
    def additional_variable(
        self,
    ) -> IntegrationConnectorsConnectionEventingConfigAdditionalVariableList:
        return typing.cast(IntegrationConnectorsConnectionEventingConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="authConfig")
    def auth_config(
        self,
    ) -> IntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference:
        return typing.cast(IntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference, jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="registrationDestinationConfig")
    def registration_destination_config(
        self,
    ) -> "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference":
        return typing.cast("IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference", jsii.get(self, "registrationDestinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfig], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enrichmentEnabledInput")
    def enrichment_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enrichmentEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="registrationDestinationConfigInput")
    def registration_destination_config_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig"], jsii.get(self, "registrationDestinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enrichmentEnabled")
    def enrichment_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enrichmentEnabled"))

    @enrichment_enabled.setter
    def enrichment_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0245710bf5ac7253d6aacce5a49d42e6ea87ceacfa957e066eadd887e9d69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrichmentEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d7177792266c8eae9a8440d89a93a49f1b217a859e18ea6d1c7820e3c95a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "key": "key"},
)
class IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig:
    def __init__(
        self,
        *,
        destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination IntegrationConnectorsConnection#destination}
        :param key: Key for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7949c521601a7b718cb39770c3a518ddf3fed849c1f0a5085c5dbf474f8f530d)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination"]]]:
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#destination IntegrationConnectorsConnection#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination"]]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key for the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "service_attachment": "serviceAttachment",
    },
)
class IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#host IntegrationConnectorsConnection#host}
        :param port: port number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#port IntegrationConnectorsConnection#port}
        :param service_attachment: Service Attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_attachment IntegrationConnectorsConnection#service_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ceffd4ac6f38da16b6b92378dee9f5195b866042ceb550b6fd8aff3f6ac01c)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service_attachment", value=service_attachment, expected_type=type_hints["service_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port
        if service_attachment is not None:
            self._values["service_attachment"] = service_attachment

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#host IntegrationConnectorsConnection#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''port number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#port IntegrationConnectorsConnection#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_attachment(self) -> typing.Optional[builtins.str]:
        '''Service Attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#service_attachment IntegrationConnectorsConnection#service_attachment}
        '''
        result = self._values.get("service_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc7910b304fe6563b61250e7a89f5db4296e3cb1612f23acd3ba7a2235004e16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9878b2d4a98dc0b2806d6532129405c76ce37dd4ddefd62f26a9f51d302cff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb6e10f6ffb25256b24c9953f410e9b8039a2e72465d81e922dcf3e12c56747)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f19e6db4811e21e36421f156d947befd5a54e8cca0aa3f306f5582a8c89864)
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
            type_hints = typing.get_type_hints(_typecheckingstub__795dd86ee117793c88a50e2378714e089776e2f2298917df2890051011a7e2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8faa4f0bd9b57db9acc38999693bddc2fd7aa22147e4115d9c418cd7633f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8642a748ae2eb8505be1f159dbdc1e0ebace025f4639a1481b2291e4f7cdf73c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetServiceAttachment")
    def reset_service_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAttachment", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachmentInput")
    def service_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ec8b740bb30a5159b40922e97122efdf53f28ddc68a7d5768d133c4e1912b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f29d17a5b6902b91ec937c6d62ea260dc92676d1bb4a4c5e514e190dc0e83d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @service_attachment.setter
    def service_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13841eee73cc37a14aab69e9045196d1ea81324390820fcab61261c13dca60f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c341c60352f61c5bc9510f24d03510805bd4300f4cf6caa1057edb78fa04cc1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8b8f5845202a432707538e791d47f12596db32acadd8ad695eaa52c6c842150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a6e5d6d7addb6173a81ae75df299d742592c60c17c07027cbb204076fdd567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(
        self,
    ) -> IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList:
        return typing.cast(IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43451a228049d3b68f3b7f9f0ee1c6d618b0f4404f9d01e21fc171a8ce81c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eed9eaecfbe8dbe625672e64a2531f0fc355aba8da2fec4fb250b1c8ca891a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingRuntimeData",
    jsii_struct_bases=[],
    name_mapping={},
)
class IntegrationConnectorsConnectionEventingRuntimeData:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingRuntimeData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingRuntimeDataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingRuntimeDataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab9e44a20a724fc5cf27e6b0f1df44164d78ab6c36eb0d7b59685adc3fc92b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionEventingRuntimeDataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e74ca94ac0706b541e02185823d15210ebab789f43b3a88b609c992076fe775)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionEventingRuntimeDataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127b88a9cb3d37aa21d36ed310b6f27559d3a5f16f0411956c84584d276c6d35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c848e2a6f3f35ea5a88cff2382eb8677481f1d87d278850df162bba960e2ff28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69426fb5ddf185a3655f11ffae3ff87563a72ba30af206d1e5355cf56667cc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingRuntimeDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingRuntimeDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaf35863461f471f30887957db1715fc4ba3b7c72eaaa499ca88a925f53aa7c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="eventsListenerEndpoint")
    def events_listener_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventsListenerEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "IntegrationConnectorsConnectionEventingRuntimeDataStatusList":
        return typing.cast("IntegrationConnectorsConnectionEventingRuntimeDataStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingRuntimeData]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingRuntimeData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingRuntimeData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7ae592e1847a03f19ea48f15ffe9a27ed4f0734213eb893f13d4746db15640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingRuntimeDataStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class IntegrationConnectorsConnectionEventingRuntimeDataStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionEventingRuntimeDataStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionEventingRuntimeDataStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingRuntimeDataStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be2ab17e36500bfe64d1b7a65ba58e9cba109c5c108865a2e5448619ea6d9f18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962ccd34a792a0eedec25cd6621f97207a430124243052cbb021b3ae8527e633)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82df24423f72d2e7e9b15b67c00523e39c813cc34e24efaa35498f66f7c9d34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc618b3203f0329954381a50bdfdef2713c84e38fe24ac54ad2c9f1acf7048d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__634a07cd7b47f9969230f7f848abcf4cf1a5279e4fec0db02944de1d5f2282a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88e4ee770f2eb18b95754896f7600bf87e859f72fc87bac13c797423083979a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionEventingRuntimeDataStatus]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionEventingRuntimeDataStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionEventingRuntimeDataStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4dfd5733de3d915cceb0d37878b9e8dcb4e50532140922171e4b7868e398522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionLockConfig",
    jsii_struct_bases=[],
    name_mapping={"locked": "locked", "reason": "reason"},
)
class IntegrationConnectorsConnectionLockConfig:
    def __init__(
        self,
        *,
        locked: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param locked: Indicates whether or not the connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#locked IntegrationConnectorsConnection#locked}
        :param reason: Describes why a connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#reason IntegrationConnectorsConnection#reason}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea2d467459f46d826ea9713d3f1d36f0265d7cceb11dc7a55996187f0f367da)
            check_type(argname="argument locked", value=locked, expected_type=type_hints["locked"])
            check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locked": locked,
        }
        if reason is not None:
            self._values["reason"] = reason

    @builtins.property
    def locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not the connection is locked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#locked IntegrationConnectorsConnection#locked}
        '''
        result = self._values.get("locked")
        assert result is not None, "Required property 'locked' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def reason(self) -> typing.Optional[builtins.str]:
        '''Describes why a connection is locked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#reason IntegrationConnectorsConnection#reason}
        '''
        result = self._values.get("reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionLockConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionLockConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionLockConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d18b6a45dfaec3787a764e990d49d48c55285ced43193c6f55ec292ae270f7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReason")
    def reset_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReason", []))

    @builtins.property
    @jsii.member(jsii_name="lockedInput")
    def locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockedInput"))

    @builtins.property
    @jsii.member(jsii_name="reasonInput")
    def reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reasonInput"))

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "locked"))

    @locked.setter
    def locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373b781f8c9799ec1be9b4bcd309373e23f28e79217e68a3660add0b9337d9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @reason.setter
    def reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4749349a39b322a6949fc9cddb6cf6f9afd30694cec26c7edc49b0738bb2e198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionLockConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionLockConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionLockConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3da4cdb1cf08f3e51489b0042449fe1263f8dfc7d798d612c9e103689178700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "level": "level"},
)
class IntegrationConnectorsConnectionLogConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enabled represents whether logging is enabled or not for a connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enabled IntegrationConnectorsConnection#enabled}
        :param level: Log configuration level. Possible values: ["LOG_LEVEL_UNSPECIFIED", "ERROR", "INFO", "DEBUG"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#level IntegrationConnectorsConnection#level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a109a339fe595cada2d515c57d9fba5c7d0b6a68831e977adba0cb08a2bd6e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if level is not None:
            self._values["level"] = level

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enabled represents whether logging is enabled or not for a connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#enabled IntegrationConnectorsConnection#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''Log configuration level. Possible values: ["LOG_LEVEL_UNSPECIFIED", "ERROR", "INFO", "DEBUG"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#level IntegrationConnectorsConnection#level}
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2df2699f4ab792a55690904d74d69c638097ff539d9c5f4ca354c2106860e0a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc4382f89254df87590b38f53a4c7b9ceec625df978039d770906017d49ea79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ad71dbbfaae7ee017196eb0b4c8c21f78ef1de282011b0a53914d7d335e861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionLogConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1022220984fd0e980857968dd97a9f8b7ab436450263f93a2d1e610ab62407fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class IntegrationConnectorsConnectionNodeConfig:
    def __init__(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#max_node_count IntegrationConnectorsConnection#max_node_count}
        :param min_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#min_node_count IntegrationConnectorsConnection#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2338ea037eecca7605513daa561de7fa28822f8ec195ed86b122e8bed1007737)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_node_count is not None:
            self._values["max_node_count"] = max_node_count
        if min_node_count is not None:
            self._values["min_node_count"] = min_node_count

    @builtins.property
    def max_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes in the runtime nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#max_node_count IntegrationConnectorsConnection#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes in the runtime nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#min_node_count IntegrationConnectorsConnection#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__191c8d807581a8dae297f14a17b16dede5e2c0aadb096cbbb6e66df87d3264e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNodeCount")
    def reset_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeCount", []))

    @jsii.member(jsii_name="resetMinNodeCount")
    def reset_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3b113de4eb9fdfed781f4e02cf510ccb9a38387b93f298117d34c6a11a8a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0250bc667b4283bed3f706bba0c35e079d41c56d43c3bdc443671d9021cb16e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionNodeConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599ad20c3ebb656850ac79a42ce761884b969108d7bc0af6b3865c43ec8c6210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfig",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "additional_variable": "additionalVariable",
        "client_certificate": "clientCertificate",
        "client_cert_type": "clientCertType",
        "client_private_key": "clientPrivateKey",
        "client_private_key_pass": "clientPrivateKeyPass",
        "private_server_certificate": "privateServerCertificate",
        "server_cert_type": "serverCertType",
        "trust_model": "trustModel",
        "use_ssl": "useSsl",
    },
)
class IntegrationConnectorsConnectionSslConfig:
    def __init__(
        self,
        *,
        type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationConnectorsConnectionSslConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        client_cert_type: typing.Optional[builtins.str] = None,
        client_private_key: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigClientPrivateKey", typing.Dict[builtins.str, typing.Any]]] = None,
        client_private_key_pass: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass", typing.Dict[builtins.str, typing.Any]]] = None,
        private_server_certificate: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigPrivateServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        server_cert_type: typing.Optional[builtins.str] = None,
        trust_model: typing.Optional[builtins.str] = None,
        use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Enum for controlling the SSL Type (TLS/MTLS) Possible values: ["TLS", "MTLS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_certificate IntegrationConnectorsConnection#client_certificate}
        :param client_cert_type: Type of Client Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_cert_type IntegrationConnectorsConnection#client_cert_type}
        :param client_private_key: client_private_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_private_key IntegrationConnectorsConnection#client_private_key}
        :param client_private_key_pass: client_private_key_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_private_key_pass IntegrationConnectorsConnection#client_private_key_pass}
        :param private_server_certificate: private_server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#private_server_certificate IntegrationConnectorsConnection#private_server_certificate}
        :param server_cert_type: Type of Server Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#server_cert_type IntegrationConnectorsConnection#server_cert_type}
        :param trust_model: Enum for Trust Model Possible values: ["PUBLIC", "PRIVATE", "INSECURE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#trust_model IntegrationConnectorsConnection#trust_model}
        :param use_ssl: Bool for enabling SSL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#use_ssl IntegrationConnectorsConnection#use_ssl}
        '''
        if isinstance(client_certificate, dict):
            client_certificate = IntegrationConnectorsConnectionSslConfigClientCertificate(**client_certificate)
        if isinstance(client_private_key, dict):
            client_private_key = IntegrationConnectorsConnectionSslConfigClientPrivateKey(**client_private_key)
        if isinstance(client_private_key_pass, dict):
            client_private_key_pass = IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass(**client_private_key_pass)
        if isinstance(private_server_certificate, dict):
            private_server_certificate = IntegrationConnectorsConnectionSslConfigPrivateServerCertificate(**private_server_certificate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f84003442bb2f17f2449e577b2b4f4ee4fd1bef363d97c16635039e7da0b39)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument additional_variable", value=additional_variable, expected_type=type_hints["additional_variable"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_cert_type", value=client_cert_type, expected_type=type_hints["client_cert_type"])
            check_type(argname="argument client_private_key", value=client_private_key, expected_type=type_hints["client_private_key"])
            check_type(argname="argument client_private_key_pass", value=client_private_key_pass, expected_type=type_hints["client_private_key_pass"])
            check_type(argname="argument private_server_certificate", value=private_server_certificate, expected_type=type_hints["private_server_certificate"])
            check_type(argname="argument server_cert_type", value=server_cert_type, expected_type=type_hints["server_cert_type"])
            check_type(argname="argument trust_model", value=trust_model, expected_type=type_hints["trust_model"])
            check_type(argname="argument use_ssl", value=use_ssl, expected_type=type_hints["use_ssl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if additional_variable is not None:
            self._values["additional_variable"] = additional_variable
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_cert_type is not None:
            self._values["client_cert_type"] = client_cert_type
        if client_private_key is not None:
            self._values["client_private_key"] = client_private_key
        if client_private_key_pass is not None:
            self._values["client_private_key_pass"] = client_private_key_pass
        if private_server_certificate is not None:
            self._values["private_server_certificate"] = private_server_certificate
        if server_cert_type is not None:
            self._values["server_cert_type"] = server_cert_type
        if trust_model is not None:
            self._values["trust_model"] = trust_model
        if use_ssl is not None:
            self._values["use_ssl"] = use_ssl

    @builtins.property
    def type(self) -> builtins.str:
        '''Enum for controlling the SSL Type (TLS/MTLS) Possible values: ["TLS", "MTLS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionSslConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#additional_variable IntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationConnectorsConnectionSslConfigAdditionalVariable"]]], result)

    @builtins.property
    def client_certificate(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigClientCertificate"]:
        '''client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_certificate IntegrationConnectorsConnection#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigClientCertificate"], result)

    @builtins.property
    def client_cert_type(self) -> typing.Optional[builtins.str]:
        '''Type of Client Cert (PEM/JKS/.. etc.) Possible values: ["PEM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_cert_type IntegrationConnectorsConnection#client_cert_type}
        '''
        result = self._values.get("client_cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_private_key(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigClientPrivateKey"]:
        '''client_private_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_private_key IntegrationConnectorsConnection#client_private_key}
        '''
        result = self._values.get("client_private_key")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigClientPrivateKey"], result)

    @builtins.property
    def client_private_key_pass(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass"]:
        '''client_private_key_pass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#client_private_key_pass IntegrationConnectorsConnection#client_private_key_pass}
        '''
        result = self._values.get("client_private_key_pass")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass"], result)

    @builtins.property
    def private_server_certificate(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigPrivateServerCertificate"]:
        '''private_server_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#private_server_certificate IntegrationConnectorsConnection#private_server_certificate}
        '''
        result = self._values.get("private_server_certificate")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigPrivateServerCertificate"], result)

    @builtins.property
    def server_cert_type(self) -> typing.Optional[builtins.str]:
        '''Type of Server Cert (PEM/JKS/.. etc.) Possible values: ["PEM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#server_cert_type IntegrationConnectorsConnection#server_cert_type}
        '''
        result = self._values.get("server_cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trust_model(self) -> typing.Optional[builtins.str]:
        '''Enum for Trust Model Possible values: ["PUBLIC", "PRIVATE", "INSECURE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#trust_model IntegrationConnectorsConnection#trust_model}
        '''
        result = self._values.get("trust_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Bool for enabling SSL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#use_ssl IntegrationConnectorsConnection#use_ssl}
        '''
        result = self._values.get("use_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariable",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "boolean_value": "booleanValue",
        "encryption_key_value": "encryptionKeyValue",
        "integer_value": "integerValue",
        "secret_value": "secretValue",
        "string_value": "stringValue",
    },
)
class IntegrationConnectorsConnectionSslConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c663feb12c8390cf4efaa5a955ed8ba6c42953c4dda5126e4384ba589c1f77)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
            check_type(argname="argument encryption_key_value", value=encryption_key_value, expected_type=type_hints["encryption_key_value"])
            check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
            check_type(argname="argument secret_value", value=secret_value, expected_type=type_hints["secret_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if boolean_value is not None:
            self._values["boolean_value"] = boolean_value
        if encryption_key_value is not None:
            self._values["encryption_key_value"] = encryption_key_value
        if integer_value is not None:
            self._values["integer_value"] = integer_value
        if secret_value is not None:
            self._values["secret_value"] = secret_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def key(self) -> builtins.str:
        '''Key for the configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#key IntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#boolean_value IntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#encryption_key_value IntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#integer_value IntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_value IntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#string_value IntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "type": "type"},
)
class IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93216645811c53ea7f047086f8dfcaa9e6cedfc9ca2c8b26f609bd79e7ec4092)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The [KMS key name] with which the content of the Operation is encrypted.

        The
        expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*.
        Will be empty string if google managed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8a786e0ecc0cd6cbdd36c8506ebaa16878e908ed757380b08bf58a8728ab5ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072909afaf9f4a98fba64039eccc9860851120808d8b438a340d951e46091609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2811528cfe600f6414af8f73c8c5ecbe81d68b6d5b819b58bbe2bdb62c04f3b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e1b4f77dfad5f10b508f670688ecf219c286a29a9ce54f299f7711d9827052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionSslConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f9d7eec61c7e997ebf0232318577f82885a9536a423a52e0253d0c5daa9f6e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85e81acf597eb917efc64f5eaeb1d3c054feea79fc93d822e1bcd5bb9e5e555)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4248032990e7a6da93bf1986885c7163264cc9fad3c8bb5e6b8e90fb03c9f9fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82062f0ba71bf6b9bebf7712b36e0c7d638cc1b8333cf84c831bb2d49090f1f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__567b5e2aba93b8973326038d68f9262aade5a4ba1dddc2424dbaf53014ff9f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionSslConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionSslConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionSslConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9fa48c59a75dc31da8bea5a4bc69beff479aee39d0d114f8c96e1daad257a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f5564e66df51648ac596836a72eef4b06b3e1ab7915136bf36a39a5bf7dd49c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKeyValue")
    def put_encryption_key_value(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#kms_key_name IntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#type IntegrationConnectorsConnection#type}
        '''
        value = IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue(
            kms_key_name=kms_key_name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretValue", [value]))

    @jsii.member(jsii_name="resetBooleanValue")
    def reset_boolean_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBooleanValue", []))

    @jsii.member(jsii_name="resetEncryptionKeyValue")
    def reset_encryption_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyValue", []))

    @jsii.member(jsii_name="resetIntegerValue")
    def reset_integer_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerValue", []))

    @jsii.member(jsii_name="resetSecretValue")
    def reset_secret_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValue")
    def encryption_key_value(
        self,
    ) -> IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="booleanValueInput")
    def boolean_value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "booleanValueInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyValueInput")
    def encryption_key_value_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="integerValueInput")
    def integer_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretValueInput")
    def secret_value_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="booleanValue")
    def boolean_value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "booleanValue"))

    @boolean_value.setter
    def boolean_value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e186832667c69fe8cd91d95cc0dbd3a62a0ca90dc5b1caa331c059818a413e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f689ae666b7e2eeda166d635f6760ce0d18e819418f7a0e2f94bc99bfc03a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd97a3664b11542918d17ec12acf8a1a1cfc31e991024d3281fda08556212317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc30deb868101ad791decbc7a6fec1d54e722bd4f52f4e983aca3cbba449f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionSslConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionSslConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionSslConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c4d6b6847df106033d463c9d4d2e73b853b469d3cd1957a1385ce469d26e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a098e37405933a001829f1b171e9d9c1d048ccc594e0845fe38e2a9e2a9155a)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__779119a255522620d0d60c749ecc0108791028925f9fdf4fa3f00de812155091)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a290a20e4a2e935145358a688b99a8b4795af7ebf8eb20b6ef22e6694729097c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efee0656acb675a191bf39230632162c04b84dff9557cc72072199beb740d1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigClientCertificate",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionSslConfigClientCertificate:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebda8cc556302d5c9a9ca0c0c226dfe4ed3f1f5c7fae93e08ce022579916a65)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionSslConfigClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc331baec911743e8a587650659276090ab00e6ae968ee0e3f2850a0d7e52701)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2518a01d67a18d5629831e95932011d26404ed6a938ea68bde2a1e9b0f9995c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigClientCertificate]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfigClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fb15deeedaa338f36148d82b34834f102db758ea5701b7359128360d1fd5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigClientPrivateKey",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionSslConfigClientPrivateKey:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5362f5d86fec9831a6d16ab93f39265c541de45c8574278a2810f51c0f6d5aa1)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigClientPrivateKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d88090ad11f470b38b770f8f314154b3424aaccac2addb68204b933d4faa564)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59ff8af8a676d4297c0a5e1e182fee851dc3379a72f7e068f2061a4b849c923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKey]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3412ba66b15677ba92fd8a131492cf5142179a70cdda6fd6d9db9131fbfd6d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1302620ff7359db642c8af507a43185dcbbf846a73493cc9da689747fb339b1d)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fec89ef1bdac4d06655c1c43e1e6d8a512ac21a55b205d5bc91bf9c8b23d4cb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5854c63a2d808b215fc47ed835d4463dd77076f3310d833a1811453bfd0005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b30744be7e145a2a7548e28684498b9c75e7888a919171f0d277e535b092db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionSslConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__713b26756602aad44575b2015ccc80f1b3b88e8f2b18d95e0c3fc06c41a2adec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionSslConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc833e1ca12ad78f69ed4144f3010060fb8e11d377fb3a5b212c53256b433006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putClientCertificate")
    def put_client_certificate(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionSslConfigClientCertificate(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientCertificate", [value]))

    @jsii.member(jsii_name="putClientPrivateKey")
    def put_client_private_key(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionSslConfigClientPrivateKey(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientPrivateKey", [value]))

    @jsii.member(jsii_name="putClientPrivateKeyPass")
    def put_client_private_key_pass(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientPrivateKeyPass", [value]))

    @jsii.member(jsii_name="putPrivateServerCertificate")
    def put_private_server_certificate(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        value = IntegrationConnectorsConnectionSslConfigPrivateServerCertificate(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateServerCertificate", [value]))

    @jsii.member(jsii_name="resetAdditionalVariable")
    def reset_additional_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalVariable", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientCertType")
    def reset_client_cert_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertType", []))

    @jsii.member(jsii_name="resetClientPrivateKey")
    def reset_client_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientPrivateKey", []))

    @jsii.member(jsii_name="resetClientPrivateKeyPass")
    def reset_client_private_key_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientPrivateKeyPass", []))

    @jsii.member(jsii_name="resetPrivateServerCertificate")
    def reset_private_server_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateServerCertificate", []))

    @jsii.member(jsii_name="resetServerCertType")
    def reset_server_cert_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerCertType", []))

    @jsii.member(jsii_name="resetTrustModel")
    def reset_trust_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustModel", []))

    @jsii.member(jsii_name="resetUseSsl")
    def reset_use_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseSsl", []))

    @builtins.property
    @jsii.member(jsii_name="additionalVariable")
    def additional_variable(
        self,
    ) -> IntegrationConnectorsConnectionSslConfigAdditionalVariableList:
        return typing.cast(IntegrationConnectorsConnectionSslConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(
        self,
    ) -> IntegrationConnectorsConnectionSslConfigClientCertificateOutputReference:
        return typing.cast(IntegrationConnectorsConnectionSslConfigClientCertificateOutputReference, jsii.get(self, "clientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKey")
    def client_private_key(
        self,
    ) -> IntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference:
        return typing.cast(IntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference, jsii.get(self, "clientPrivateKey"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKeyPass")
    def client_private_key_pass(
        self,
    ) -> IntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference:
        return typing.cast(IntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference, jsii.get(self, "clientPrivateKeyPass"))

    @builtins.property
    @jsii.member(jsii_name="privateServerCertificate")
    def private_server_certificate(
        self,
    ) -> "IntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference":
        return typing.cast("IntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference", jsii.get(self, "privateServerCertificate"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionSslConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionSslConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigClientCertificate]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigClientCertificate], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertTypeInput")
    def client_cert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKeyInput")
    def client_private_key_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKey]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKey], jsii.get(self, "clientPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKeyPassInput")
    def client_private_key_pass_input(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass], jsii.get(self, "clientPrivateKeyPassInput"))

    @builtins.property
    @jsii.member(jsii_name="privateServerCertificateInput")
    def private_server_certificate_input(
        self,
    ) -> typing.Optional["IntegrationConnectorsConnectionSslConfigPrivateServerCertificate"]:
        return typing.cast(typing.Optional["IntegrationConnectorsConnectionSslConfigPrivateServerCertificate"], jsii.get(self, "privateServerCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCertTypeInput")
    def server_cert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCertTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="trustModelInput")
    def trust_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustModelInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="useSslInput")
    def use_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useSslInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertType")
    def client_cert_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertType"))

    @client_cert_type.setter
    def client_cert_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6b5f3fde28e36a0d9148ab2084ffbf1f17470c9e863833a483726b13d6e6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCertType")
    def server_cert_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCertType"))

    @server_cert_type.setter
    def server_cert_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4573763a7b5631e705d361e5c565f8afccd4193ce7de69577eb502e7236149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustModel")
    def trust_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustModel"))

    @trust_model.setter
    def trust_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4715d70181fa2f1b1fd37feccf8662df3bd58753964e9cda34b6defdcfba02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4907ee12ac4b9972824739708d50be31a7dde63f6a4774e8233af29a76a8a73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSsl")
    def use_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useSsl"))

    @use_ssl.setter
    def use_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e307c464374fd134c486dac8f015e28702ac8d675d41a3d9a6860c9864f4e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfig]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50adfd58dfb93dff1a9a58c3bed3da38ac9f639cda743c4f7894e5eec591708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigPrivateServerCertificate",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class IntegrationConnectorsConnectionSslConfigPrivateServerCertificate:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f98f0f1175752ab8ca4355d80ca02cb3218996acba9a3305572381611cf5cf)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#secret_version IntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionSslConfigPrivateServerCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf11a925bcd83ae01949bd659882538d2abc2cbbad292075fb9500cab30464f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555ddcf4b895366a9aeec2ec7c5d88e636c17381253c112a1e154653b909c11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IntegrationConnectorsConnectionSslConfigPrivateServerCertificate]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionSslConfigPrivateServerCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionSslConfigPrivateServerCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3daeadd46525241fa52386b2f4e609731beba0915c5bac00904b11c6aa4c5d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class IntegrationConnectorsConnectionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__330f6f33eb4e4b470ae39fc9c5f00326ad394a6594412fedb37f0092378c7a6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationConnectorsConnectionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455c083b13c765fcd0f9042122c895705269df08f757f68a59d008f719dd261f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationConnectorsConnectionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c31b8ad280a91439452b7d5b4f3451d7a300cf10e98a61e159b2979aba650ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c079f1ab0277b90b016447d1e8e6b020b33cb8dacff9651055b4d8df51f14c6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ba83a37baafd5b22ad4e3aebe99e77705014d5d41faac96469235632fecb76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class IntegrationConnectorsConnectionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aad8286e6c4ea654c27809b53859572720750c9348a47016768e01b2f9165a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IntegrationConnectorsConnectionStatus]:
        return typing.cast(typing.Optional[IntegrationConnectorsConnectionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IntegrationConnectorsConnectionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc627c0b30a07e747e5a9ba85467424bb831ae37ea4c8e72c83496354043a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class IntegrationConnectorsConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#create IntegrationConnectorsConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#delete IntegrationConnectorsConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#update IntegrationConnectorsConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f884edec2a25cbab5894e1cc4f1be76d2885ed99984ab4bffbdeefd4a7d2d511)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#create IntegrationConnectorsConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#delete IntegrationConnectorsConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/integration_connectors_connection#update IntegrationConnectorsConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationConnectorsConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationConnectorsConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.integrationConnectorsConnection.IntegrationConnectorsConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17397827d6be345bf4535ef72d5fd46cc298e6c9793317fa637623b435027dfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43efb7a9e57bd12799a20696d70d175e6906146516dc126dd9c74f045b94c333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6a9a98d3911d94ba2270a2266dc349c9fa2c877764c755ff3dd0397c667202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8b2ce2331df4de6efeed832d97a448d64173702444f160c06dba38f7dc2194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c592f2d8469372b2c38d6dcb69c522f3ea8cbed64501bfc19495336dc7989f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IntegrationConnectorsConnection",
    "IntegrationConnectorsConnectionAuthConfig",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariable",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariableList",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue",
    "IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow",
    "IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret",
    "IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials",
    "IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret",
    "IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer",
    "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey",
    "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims",
    "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference",
    "IntegrationConnectorsConnectionAuthConfigOutputReference",
    "IntegrationConnectorsConnectionAuthConfigSshPublicKey",
    "IntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference",
    "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert",
    "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference",
    "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass",
    "IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference",
    "IntegrationConnectorsConnectionAuthConfigUserPassword",
    "IntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference",
    "IntegrationConnectorsConnectionAuthConfigUserPasswordPassword",
    "IntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference",
    "IntegrationConnectorsConnectionConfig",
    "IntegrationConnectorsConnectionConfigVariable",
    "IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue",
    "IntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference",
    "IntegrationConnectorsConnectionConfigVariableList",
    "IntegrationConnectorsConnectionConfigVariableOutputReference",
    "IntegrationConnectorsConnectionConfigVariableSecretValue",
    "IntegrationConnectorsConnectionConfigVariableSecretValueOutputReference",
    "IntegrationConnectorsConnectionConnectorVersionInfraConfig",
    "IntegrationConnectorsConnectionConnectorVersionInfraConfigList",
    "IntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference",
    "IntegrationConnectorsConnectionDestinationConfig",
    "IntegrationConnectorsConnectionDestinationConfigDestination",
    "IntegrationConnectorsConnectionDestinationConfigDestinationList",
    "IntegrationConnectorsConnectionDestinationConfigDestinationOutputReference",
    "IntegrationConnectorsConnectionDestinationConfigList",
    "IntegrationConnectorsConnectionDestinationConfigOutputReference",
    "IntegrationConnectorsConnectionEventingConfig",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariable",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariableList",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue",
    "IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAuthConfig",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword",
    "IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference",
    "IntegrationConnectorsConnectionEventingConfigOutputReference",
    "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig",
    "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination",
    "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList",
    "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference",
    "IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference",
    "IntegrationConnectorsConnectionEventingRuntimeData",
    "IntegrationConnectorsConnectionEventingRuntimeDataList",
    "IntegrationConnectorsConnectionEventingRuntimeDataOutputReference",
    "IntegrationConnectorsConnectionEventingRuntimeDataStatus",
    "IntegrationConnectorsConnectionEventingRuntimeDataStatusList",
    "IntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference",
    "IntegrationConnectorsConnectionLockConfig",
    "IntegrationConnectorsConnectionLockConfigOutputReference",
    "IntegrationConnectorsConnectionLogConfig",
    "IntegrationConnectorsConnectionLogConfigOutputReference",
    "IntegrationConnectorsConnectionNodeConfig",
    "IntegrationConnectorsConnectionNodeConfigOutputReference",
    "IntegrationConnectorsConnectionSslConfig",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariable",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariableList",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue",
    "IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference",
    "IntegrationConnectorsConnectionSslConfigClientCertificate",
    "IntegrationConnectorsConnectionSslConfigClientCertificateOutputReference",
    "IntegrationConnectorsConnectionSslConfigClientPrivateKey",
    "IntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference",
    "IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass",
    "IntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference",
    "IntegrationConnectorsConnectionSslConfigOutputReference",
    "IntegrationConnectorsConnectionSslConfigPrivateServerCertificate",
    "IntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference",
    "IntegrationConnectorsConnectionStatus",
    "IntegrationConnectorsConnectionStatusList",
    "IntegrationConnectorsConnectionStatusOutputReference",
    "IntegrationConnectorsConnectionTimeouts",
    "IntegrationConnectorsConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b1ed424ced18e1b0129b97a14ca05975280338b1a83a03daa820213d1ae60c8e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connector_version: builtins.str,
    location: builtins.str,
    name: builtins.str,
    auth_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionConfigVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionDestinationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    eventing_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    eventing_enablement_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lock_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionLockConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    ssl_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[IntegrationConnectorsConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6a00317b891b3174b3a93c18a4c1dfde6e8b3c31d3df02c803bab57db16246a4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84273e97476965f18853eca727fa9dfe089320562e30e199c31eee1f6ede7c2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionConfigVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e227c9e340f2ca5b811c412d1a363f2afa555a779a7d75d3a6fa8ac208a3262(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionDestinationConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011e39a1b1f2d85ee191305d2530ae3c4fdcc4502ee819fd35087e4f20e8f03c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9ef744f1753acb333a7d1456aaff823bc1e4bd48e1caf5c30b571dd42a833b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5bce9ef80de159f25eb2f8784146fa4da1a8e7fb1624f25b008ec218a5632f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c2fe7a9a5284c03816a925e4ea6b649d33167504294abd783e07348bc7573f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a52958684399fa0a584638f4ba39e6d7f4ca67e6779362957461493d3cee04(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4621dab763df729a546a4f03577014271bd2321caf37e979b4daa0a16845eafe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db3d81fb9d602f8ba41146dba80262eefff7c2924525aa6de1bb8d426ecbeaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a5b13de17dedc70a6bf2a37d4931a4c082442f0e5f9036677f27b2f9f8c67b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701852376e1734059b42ce6510eda7ceb701a6cbbd205919d81cef967ed15dc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd662386050a6c5bc7a7f7493c31e699dc5699a357de9b809a715e4b6d6b27a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784e43ea4ab00211fa80ed218e310b1f3bf1aa8e807d4f3d35b28fa853d9c40f(
    *,
    auth_type: builtins.str,
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_key: typing.Optional[builtins.str] = None,
    oauth2_auth_code_flow: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_client_credentials: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_jwt_bearer: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_public_key: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigSshPublicKey, typing.Dict[builtins.str, typing.Any]]] = None,
    user_password: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigUserPassword, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad852eb4a85850bdb1dcdfabe6ca77c863a1b56ee7064eab1d34a366d59e6ef5(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cac7353988c945adb1ccad90ec8370291accde639805d0148e7e4e0bfe2a8f3(
    *,
    type: builtins.str,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d42bb49dd07bd34b58c814fb9dc63b61e6a11e02cf11af39f4b263175833244(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bc6f028dc670f3f8e7273f8e41bcfff1b68aa9848735d4b08995928ab97c13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e057682f59cebef43654809b96e524fe015930a8a295e3417b753fd884525144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7149291fa5c044da5cf48d9bb6b08984bb640cf133776c102924596b988b3798(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662be42e95855c79d323de57fe355f91bb807a66b0caf32ff4bc9f269616eb6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5662ad4db4f9ad4816ae149b9ed3492972e61ff27f5cae0f31a4b51246f434f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f244590e71adfed8c59ecc9209c5beb1556583c5d37e3e9d25480b6a5ff167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f22312e03ff886af12b0c691f2bde39a756e061b8c60bb70c43e62e8dd2b95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0256b910c770e2363a591f73313842fd1abf44d451c29bd3d516832ea858169(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ade69a634c001f2a4b67e826992ffb7115bf9617fe451785c116b091be8e11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionAuthConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3143f95409ccbdfaea1449ee38c70d419ac277aad660acdb3269eb5865f7d02f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343c38f73982243545debaa90e19cb038a026cd5a3ea397b310c169f531eee21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e3efc39c132f840bfad35574c3a3b39b6599a1be163c9d6190ab9da8fafbf7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fc770a600aa85d86eb91da48b4004dc1fc6f56722051ecc10e3bd843957796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7029cf313dc754473a4c67bad19a3f498fb4750ecdfdc4c7ea1e3033855e8de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e6ee263a6ac9f7e745ce998c727ad241d38f35ca333ff4636bc65146e31207(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionAuthConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c040f19174e193c815b422a1bf23802ab9147b84f009e7a98c6be469ad5b298(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448c6703331298500c67a87a9209ff52bb82604679aef5943639dcd28f35a871(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de399d3f845f36534e79855043f320ce6160f2ea8dbc00506b1beb26ef0b72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c726b8d2477437dda972dc10bb35083cd7fedc176b5ada54528b761af7d0e0(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a3e824fd69e5644b951dc09e4ac028ac6c8764ad1edfcd9f17ca37ed510f45(
    *,
    auth_uri: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_pkce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3659af668cce19ed566ebcb7ab9d4a5d11e0e455137cc092f7a342394dd3f3a2(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00906b01652edcf1e55631a13ccfe8c92a82043ea41d091f71cca8426c5d7f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880b72f1eae9b7da205303c5a9041f19bfaf7141bcb45635e1fbbe24cf41f6d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5ff28718b44518ef65177543ce6855369dd8f576a81f755195570c92b3a090(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1212b1e76965464186c7474c9ef83b3e0a2afb997c029c5e6ddc67dea1eff129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6eb694122fefad1107aed1630e73aee827084c7b9c10fecd30ffeec3ee7844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c446562b99928eb5af4a43d744d0ca276c0535e54e1dfcfea1e23178b85763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60acf325ec07ed2fa9132726f454ab728472f297e94796a13543be18e30cd4b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7437455f218efa3c5ab4e41496c325f9278f466d96ddce7d551cb58aa1b58675(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1605fa2e576fabe03013678569f7ae54cc6b68988f8b5a502f5dd1188014eaa(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5a7a2112d59af611f4dfa360f3962c3620496786c313182f935fcce6f1f5ac(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b5561dbc28528ac2d0865e9a836ea3974ad432999522ef5c8895d0b9cac62c(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6263f7018336d6515f7e9671fcc83b60485adc71e6cc2d0788dc6b90108bcc5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a718830e2a8756f3527e6d95822b2c942a75ed2722c6a7fb791e7f628d62b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd8387be9b223f4426bc6f85b8bd8b64ad6a6f6bd412481bdce9b941b5bc01d(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990b17338703eac47557ce0e10a87d6a34d495fe31e623228ce6a96368e35771(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c902e473b4731e59105593ce8c1e5e0bdf23281564caae0e1e1de4ca73e1102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07dc6455dadf80f85a2312bbcbda6b6d5a435203311e0b59923867607f6fb685(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1134d1bf31a2a72cac1ed9bca86aba587208e19e9d25a5a0f5a18a0ad988cf23(
    *,
    client_key: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt_claims: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435739f68d806f919644cd5bc59532128511408b6e5dac6d56e6ea240ddbc022(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38623a645a4fb24776eaf085c22ee0d62e9ae715edb10b39b51d4c00f915cb6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec65651930ba4215d584f4c44dd8d4ad34c42bf7b70680783b16c51a5f024bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a5a369ceafe1ceff68d07f39f7a2659fa877c1a4b7bdbf0eaf2842211367fa(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fa20f27fac590a12d7aa45dd24adf4e2064d0f78f9c8a9776f29b5eae279b1(
    *,
    audience: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66469e25ff5b387773e599072d4be345297e993bf1220c8515388d1f0944a226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773ca9638c2b64aff8e5e17b0735828485d7d8861ef73e5915997569d7d84b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32984e58df442956da76256241a4c295f050e8a99f0c1d67c04b177b29914352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5047e8e4b01bec19586fc2cfc1aa55fb4f30b2e593bcf78555f2f96e5c9fc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51641881b9473fb77beb67a9bdf38bd5fc8466a13f81e1f58f926d30221b2bc(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a36387a63c6de7379176a008d9774f6a60ac0d7b0538a88ac4672dca7ac069(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35ae054dc09f2a6382992d4c4b055ff4da9a7b386f458bacf51c3c15c408cce(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigOauth2JwtBearer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0498631f945041a4e83c819633b0384a90750e8bfb5ae3180014e3cc059ea15c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab60f2ab93607affbe048028fa7f13d1fdd597e46a3ebdedae447f1c69cdb25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a447f8c756418a42daf254d9f7e0037b6e0c47650e74e00995084c0b8075b17f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab731dcb72d933fd34ee98543eb7aff041843daa848a3e6c6eb83cb1614bb5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8aa4fc2af2e16df5c0dad27f7caca1604b7ab27f5fc1d742331d3d242586319(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c3b42e94ccd57b919a1b9aa98101a9f2c6eba765d752e118806cf273c7a4f8(
    *,
    username: builtins.str,
    cert_type: typing.Optional[builtins.str] = None,
    ssh_client_cert: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_client_cert_pass: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875de16295b8bb218274524698334146f771316c92d880ea513fa64eb8534393(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc906f1334c2a54156bf92ead2b808bf0be53559fd7abef5c706924840e1ce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2464ae0689f286d2968bf1065263463c056b90216c03978963c03c2991aa795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be62cddfef9127429277e1e5b5299280aa7fa9282a8453b72f5954a35dc4bfa(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36756f83dffc7f35b4696099ffd39b831c963322a17ed6bf9fd57a669d5e930a(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0403215a7c1db16d07861f2c50b6acee0b8124e98b89ef2f85713b844442833e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dd6d310e7ae051196c1cfcbd2a64cf3fef0b6e0531c90bb92903efc319d745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ec8c73ca20e33767e5de2105b9a95686bbb74a9287cfabd68c9e91bd51f100(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2440f9943abdf84643a484466f000d0e676a6083d516d20a536bc5054de75b40(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d6bb0b62325f87d0f615d9d8822d5ec06b1010e08fe374383c73323655d9b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e05a63a64ccc2ee8899927c8521cc9c6c65fb247fd603ef4ca39c8c03984ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec955341fb0791f692977c3505ee2ae9a51d261b05f1d1edbd8ef00b1b0d918e(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23a9118569e9f15d606ccb0c5426ad81c8a028d8210e106613a14beb3f30c1d(
    *,
    username: builtins.str,
    password: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfigUserPasswordPassword, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78344d79b5cfb9e23263e8cb6f5809f1c87d8b7dbe6636e1ad853e1ee9c4cbc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c1caa7157704361f44f3c3df7ced1aacb24c691c0880542ae47ef093f99de4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0ce275fcda12bcf22c49101ab929100248feabd782dbfe1abd0d0f5fabf612(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2db0ebbe5fdac3c686e663151dc44a498d6516c79cb24577316fcf5e7adbaa(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24ae7f003e6dd523dd55e24026c1c7a6fffc09182222c30c07bf8c2edd48f9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c005c01403a1a538f7d95651ead03f2f8d06cd2e5f656a2923ffd370751b0a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a92b4d3fd757de4cf3e88342cb40ec9c45a820c62d4f7a89ea56e761d9f455(
    value: typing.Optional[IntegrationConnectorsConnectionAuthConfigUserPasswordPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21924e6f83e1659bd056c72af7df8c23e7c8462f592d413b2a1346bf5cec424(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connector_version: builtins.str,
    location: builtins.str,
    name: builtins.str,
    auth_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionConfigVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionDestinationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    eventing_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    eventing_enablement_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lock_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionLockConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    ssl_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[IntegrationConnectorsConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b16dea51d1aa468986fb801cc0dc053919676ee29c627496ab3f493a897281(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionConfigVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5ed5b76d3a450d63344b6bfa58ce7f917d3e183c4869a707db7dc7d203410f(
    *,
    type: builtins.str,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3d5e98d9b31a2fc62c654b872822c5faa77fc52e9edd058b343f3c4bccebf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335bdd2f2a7ea410d8107120b883e2a2618b6112fcdb3373523c7a9947bd7d41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481872c987275b771d7a6bdcacaae907cbc134b26131765dc295c756738a597d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97153987c9473d42989eee5a772d87721ce15145b4918c24964c42b00134bdb3(
    value: typing.Optional[IntegrationConnectorsConnectionConfigVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9959da3773d3d7b9c8017b8c04a1883482cd38a91197a7349407c45932656f11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d8d7a63764f62f173a2b77af5199a2308adb855ccec0344fc0c4a1b519db81(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547fd4612a571870fbbf1511aff0431318d2b13410e32a9510a4fb9f321ce5bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec693580c3479c286b6cf68ab2879a5b995b05f0b9c9a832cd5ebc20c34b838a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a226a481c6ffe40e631656764057a0d7d4572e162fc7553daeaca09c8a038bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3f99656c0d625ce6b35d4e2acd41799cc448e0591e81a20d09b60bb58a1820(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionConfigVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09db8d1182257d29ea95cfc841aece3cb4092dbc865b0d961c4b1dcf21fc8fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a12478e56458c64c2a551d8438fdd408b79de008c669afcb1dbba46c7d6e28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1317ca2bbc7f9f92f0e74e088d75fbc1d84b4d15748e1061e2a7ce3649fdf4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d87fd66d3424129e91cb22ebe41131b8790b20612131c7f1395332c59ddc20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5189422edee0d4b60533490626c339d61acd4fda91d962b9875f572d6a1aac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2308f61b37052b197efb725807d3f3902d46b7f4ebb8f02c6fe478a497b0c11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionConfigVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f11312db5a590b8dabaac8dd3ebfd45f2da5667666f5fecb8b5773c4aa5e9f(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7b502eb1e818d11ece6fcfecb7919ba0ae29f56c44e6d62fbf74971fe65900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b034265e0a079a9feba63d7d698d8dc0d8fa907e29b83d3780e773aeebf1ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fa7a7e058ba893700d0ff47da58890dd3addf04287cd0d367ed19a4687f900(
    value: typing.Optional[IntegrationConnectorsConnectionConfigVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c369fa62736bc207acd9a8a36851f342e36f3b53ebb3dbfd9f04986d881f40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653089efe450ba8f3f6f2c7c3f70b09914fe15893dadbf140d0c83742b923615(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229a55644bdaec61361db40b9dea74e73a6a30dd1978bdb4529f7001666fea2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd25ff0334860149dad1e907f5a68e94e981e36c20b1728223ad081673f993d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34a05869baeafa41458bfe5e66120e787be2d60614f0d5e28cd26015129020e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63ce40cf0ec8cd1dc45aa828ec2d3f5ef137a4f9afefad8de732ccf1a5b45a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373be81b761bd4ff9b745b481565dd64b13b36f9bf46a46a9dab5582a2c86c93(
    value: typing.Optional[IntegrationConnectorsConnectionConnectorVersionInfraConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff9859246bb637bdafe4157ece9214258e9a348467e9f901b38dee2d90225a0(
    *,
    key: builtins.str,
    destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82921b34946b1f9a697b136da9beb4960df08c8efcccdf3b507a1332ff4f36e2(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_attachment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4502cf2f0a9e9ab5fa1f48c725a2ec7a7ff3e8a0a7f101273d2af795e13d4b6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37df733460f51aaa553cafede5a5d7995ce01fc95bee6b1da113940eede0dcf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8104f03970ed4f446b35223dfe8d28fda18d21abe4265b236ddc4eadfb4f4736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7fe9a625df7dec7a380162f06a11f3e183d6dac07d6a389ffa38adf3a0355d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f495b08403c79a15a96f45a42924e7a1882179f23fc7dc91e3fc815a2dcd5b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0e5dbd41e788a0a7d3658a392ffd3ce8e5b8006e8d1c5e6442cdb0989216e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfigDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ba8bc42178338beececee46d6125fa5148a916e960e912cf4d02761a13587e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04d18ed71779ba6cf0da1169b404ee8825115e33b921534218dacccee1bf712(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1173e860adab330d59ee3a8540a9a422c94fe4b4c154f2b4985f75b416dee401(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043361124c7cfb71d21cc86255a5229f20453af2f2997795518894a522b0c67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3e2b844f48bc5e6dea517acc1ee423f4e432e3204a1b1ab7c48e59e52b576a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfigDestination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85510c6a0712a5d6a13dc6de690dc1f30bf312924c8b6ff29ad12fcc22e31e9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b8112f423f6cec7de179bc90288fdee4bf4c24bc9293b3329a1393117b5576(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e105bfdba81ed6f639775aa3d047b524cab21216cb1b480368b0909d8b43da19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a35f4e09f138aca33952d1732f74e8755123cd5d684cb49a62ed9a2d970307(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79dea1f14f7aa020f16c41be2751a072993ee9a365d433e6e73d0d40a4ba0676(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98c4732a7405e43f08de4d1b0318ecc5a57e5a32adce0f43886bd55360863ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionDestinationConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f642f90251773f8621c4e9c701c6480f79b7ab512d8336966abbc8c7e688eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce0df16522d133826d7289b8f158d3240d4fd18e297d9f7326be6cbf256965d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a042472b120c2b9e100a1656301890858a55e7f78ffc42a17644dd134eeee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46607c9696caf7935c193d011470c89e5a9586aa492632d64bd662dfcd6a9d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionDestinationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8517027c90d3bf7e8529e2f469a05c2536d1c83309605809ee671deccc2a753b(
    *,
    registration_destination_config: typing.Union[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig, typing.Dict[builtins.str, typing.Any]],
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enrichment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61842c3e3dfa13ca809a4f99fa0b5774a81f2e8fc0eda934bb381513f33c681c(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7578fb67081ff8bf1dd9db6efb13b81e4dd0da1292f88852943e0245a7b5f95(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f9c9e72ce5d3d5d2123938e68196c81644e2d9c1b75f41d9a5a06f98e69766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67eb8cb4f6ea48e5fb59a0dbd19550a403d96823d63533bd6a0fab78842c162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4179aabda6a84c810b341ae25cda567d4fccb26518865d049245ab7a291b62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc2f1356ad0cfa5d5ce330d879be52c61f315aba1626ca980f1643f049852f9(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba9b60947f155d37b1e318476d949c2ba0fdb43977d0bd09e1d0ce0044b3786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b74017e3f2b359f59983d27b58c45257ec32ddb795e44a1c706e3b240982325(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883cb532afb2b37209b45cca9925739a3345495af8b03ee11eb8ad07d1530f52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81eded52972033888d8821c7e988224b244842792b761e0d2d21003fb432088e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadbfbaa555d320715aa26831386eab34d0b923bfaa3e9a817156106de17e12a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314ea5875c225fc7275d91e204ccaf4977de70bb323a1900d532de410947cb9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5128fd9cdb7e99cba6729fdff9813a612b527f826c73550eafb48ba6dc41506d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f479f7cb467d42bc68f31f29fa64637016e8931cc76e0ce56fecfd3bf6ca989(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2cfffd696aa3e6fcc864f44f4c711b07028b862573c0b1a231338448c94bbd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ae7273b56cbf3bda93299cf6e7cef8219695830ed35618fde3c06939611ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d097d1cd0d346b81c7359ed18286b2db04966d31f83bbad2d67ad03497225ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aaf1b6ba3af48ce39afe395863e40b7f4793ec9492c405d12605ddf8d524501(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8847f1e0b52123381f2d8b12b87181c09c24e7ea56a845f960cdf60c77cd42b(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa5ada0a31e48c7ff94e91d648f18baf75f9c425c0514dc15bb83679d01f2ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9e7f8f584c0c618b700c7c4ef40f2125a169b7be47a877aa8a66f4ab97b14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611a051101f8b8c0495dc2217d3d8b01765df0ddbe013227a0f012c29a3146c9(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698eb846aa157336fa307aa9676e5bc98d0b95d41b7fb7978ee9bf4587e93068(
    *,
    auth_type: builtins.str,
    user_password: typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword, typing.Dict[builtins.str, typing.Any]],
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806f3a858a574eff78ab4908e5c7dd4e17cafd043300a4ae39494295849e1db5(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d71816293fb20a913dfa3b0bfa377b5e900f895d28f0e08fc35a789175d67b2(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9304305c41a8478e21aac4d7b74e4270f7340c13ce594c7c00f0897e2511a8a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfe3bafc4d3d0d2f4b402236b07929cba2748a742569d58d6d0bb1615c3dea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d617c73abea336468ca70920ac6800b50f5337d75d52c8366c678c0044b9a248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1153c31e27350cbe552e7633e27b69047040456ec8afe2805fe30060549f210(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2942e29e8f17edee2266b872e3cf3ec13708622f2af11a6912f662c8025b5a11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2573d9cbbd1b24141fbf512bab7c9bf50438f4e677d5ee9e2aeff77a2898a210(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946643e54f5eb5d7c946ca06cbed28fd69d4ef1e75bf7fd59f81061c6372c9d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7e20c717d588e960e6272495ca399792dcd5a76e78c8c910396a21a0164893(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdaaa6440b20a3792d3ba3302b47c76975f5c7a046b427ffa7114fc18111061(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1a36939e7ba5ef5b0376f9c59149302f20f17a9475e4dada07854b30fd3e56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33197bf0f720d457d4eba3a066b7a672094ec70b8f4dca8b83de473e9af4e80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3dd88acbedd3c7ac1d875acd35a83d1ae26daea1132352f807e30c9a23b768(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a2c7630127c8e02025c1e760dfe32f5073eb93d5df1e2834c7b26d8cf732fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342f7e5c26bf4dc7abd60f8ffae69c1e06d3e106100562a6ab7f3d2ff33b732c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143c66d9c6420749a27ccf6addfd6491c9902e307bf4b9f90bec4c8d0b3e3178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68d54640c2ab339895f51eed1213521d636a4d6872762d7f5ee2c5f9d55a2b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0136c4a5abba67772b4b0ec120e69cd16fb4a9e70409b433a2330770447b5b25(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90546002f128d679d73c23320c99aed5a19e5f48974e2c7f6e9dd33af7aff9ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab910ba5c3c5324744fb07c9a473b4d1ef4c7b125eb110cee4b9a73fc1ddbd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d084603317c1590ce6bfcfd4b8ff30456a7d103d834dfa1d86acb1a8a4c5460(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd52082b6d5d376aab67e2b3123983e6c69d2c8c9b74ae6f9173cf3593fb901(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70ab7bf161894d0363adfb3d97a329388499d021b8a4f14540dd538da83011d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36270d5f4b9766da67458a4e8c251a4d2e1d47aa0c59b9fff4e63c8a0d18663f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d8257ee9429a60828dc23aed63b6293af4cc8a14d9e3d133f83b77cfcddcc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43525b6f630644d866ece39b0597195692abede7086aa60fd51d60b5f5db025(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd33fc1e9b1e1783f85ca1b6d41f6ef857de2a24a49a89224e07f67d77908b39(
    *,
    password: typing.Optional[typing.Union[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98606598e02bdb786896da5fba5ca6aec82d70ef7067ed250f4cc2741746104e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a56b236f7b1fbec51e54906454543f98bf23ccff33695aaed23743dcafab51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae95539a6269154ac576caa237e6bb0c61a0c1a0308422797efb40358fa5162(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53c8e0efe597dd6fdf00d8ce1e64202012a3a1738796e77ddd7925c682e2290(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9375e8a2c9562a6e563c0910cbdf7fe0225bb31a2fe6f6ee7de8db0462066730(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4a55808f63aa9cf6c075641a236a5cf4d3607c26bc21b00960b7faa5fb9119(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adeec5861c6febb420bb40b5e60da4fc9295ef79af9bff9b3f26e8be6c86b565(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102bd75de3bc9a05d7bef70e1ec280ff4ddede93f147acade6fc564290bcd542(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f28a5c90bdcd5e3e9b18128133c94703d86296e7dbb8383d77a78078a47d68d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0245710bf5ac7253d6aacce5a49d42e6ea87ceacfa957e066eadd887e9d69b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d7177792266c8eae9a8440d89a93a49f1b217a859e18ea6d1c7820e3c95a5b(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7949c521601a7b718cb39770c3a518ddf3fed849c1f0a5085c5dbf474f8f530d(
    *,
    destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ceffd4ac6f38da16b6b92378dee9f5195b866042ceb550b6fd8aff3f6ac01c(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_attachment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7910b304fe6563b61250e7a89f5db4296e3cb1612f23acd3ba7a2235004e16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9878b2d4a98dc0b2806d6532129405c76ce37dd4ddefd62f26a9f51d302cff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb6e10f6ffb25256b24c9953f410e9b8039a2e72465d81e922dcf3e12c56747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f19e6db4811e21e36421f156d947befd5a54e8cca0aa3f306f5582a8c89864(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795dd86ee117793c88a50e2378714e089776e2f2298917df2890051011a7e2f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8faa4f0bd9b57db9acc38999693bddc2fd7aa22147e4115d9c418cd7633f6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8642a748ae2eb8505be1f159dbdc1e0ebace025f4639a1481b2291e4f7cdf73c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ec8b740bb30a5159b40922e97122efdf53f28ddc68a7d5768d133c4e1912b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f29d17a5b6902b91ec937c6d62ea260dc92676d1bb4a4c5e514e190dc0e83d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13841eee73cc37a14aab69e9045196d1ea81324390820fcab61261c13dca60f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c341c60352f61c5bc9510f24d03510805bd4300f4cf6caa1057edb78fa04cc1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b8f5845202a432707538e791d47f12596db32acadd8ad695eaa52c6c842150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a6e5d6d7addb6173a81ae75df299d742592c60c17c07027cbb204076fdd567(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43451a228049d3b68f3b7f9f0ee1c6d618b0f4404f9d01e21fc171a8ce81c05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eed9eaecfbe8dbe625672e64a2531f0fc355aba8da2fec4fb250b1c8ca891a4(
    value: typing.Optional[IntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab9e44a20a724fc5cf27e6b0f1df44164d78ab6c36eb0d7b59685adc3fc92b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e74ca94ac0706b541e02185823d15210ebab789f43b3a88b609c992076fe775(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127b88a9cb3d37aa21d36ed310b6f27559d3a5f16f0411956c84584d276c6d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c848e2a6f3f35ea5a88cff2382eb8677481f1d87d278850df162bba960e2ff28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69426fb5ddf185a3655f11ffae3ff87563a72ba30af206d1e5355cf56667cc34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf35863461f471f30887957db1715fc4ba3b7c72eaaa499ca88a925f53aa7c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7ae592e1847a03f19ea48f15ffe9a27ed4f0734213eb893f13d4746db15640(
    value: typing.Optional[IntegrationConnectorsConnectionEventingRuntimeData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2ab17e36500bfe64d1b7a65ba58e9cba109c5c108865a2e5448619ea6d9f18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962ccd34a792a0eedec25cd6621f97207a430124243052cbb021b3ae8527e633(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82df24423f72d2e7e9b15b67c00523e39c813cc34e24efaa35498f66f7c9d34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc618b3203f0329954381a50bdfdef2713c84e38fe24ac54ad2c9f1acf7048d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634a07cd7b47f9969230f7f848abcf4cf1a5279e4fec0db02944de1d5f2282a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e4ee770f2eb18b95754896f7600bf87e859f72fc87bac13c797423083979a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4dfd5733de3d915cceb0d37878b9e8dcb4e50532140922171e4b7868e398522(
    value: typing.Optional[IntegrationConnectorsConnectionEventingRuntimeDataStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea2d467459f46d826ea9713d3f1d36f0265d7cceb11dc7a55996187f0f367da(
    *,
    locked: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d18b6a45dfaec3787a764e990d49d48c55285ced43193c6f55ec292ae270f7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373b781f8c9799ec1be9b4bcd309373e23f28e79217e68a3660add0b9337d9e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4749349a39b322a6949fc9cddb6cf6f9afd30694cec26c7edc49b0738bb2e198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3da4cdb1cf08f3e51489b0042449fe1263f8dfc7d798d612c9e103689178700(
    value: typing.Optional[IntegrationConnectorsConnectionLockConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a109a339fe595cada2d515c57d9fba5c7d0b6a68831e977adba0cb08a2bd6e(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df2699f4ab792a55690904d74d69c638097ff539d9c5f4ca354c2106860e0a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc4382f89254df87590b38f53a4c7b9ceec625df978039d770906017d49ea79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ad71dbbfaae7ee017196eb0b4c8c21f78ef1de282011b0a53914d7d335e861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1022220984fd0e980857968dd97a9f8b7ab436450263f93a2d1e610ab62407fe(
    value: typing.Optional[IntegrationConnectorsConnectionLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2338ea037eecca7605513daa561de7fa28822f8ec195ed86b122e8bed1007737(
    *,
    max_node_count: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191c8d807581a8dae297f14a17b16dede5e2c0aadb096cbbb6e66df87d3264e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3b113de4eb9fdfed781f4e02cf510ccb9a38387b93f298117d34c6a11a8a25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0250bc667b4283bed3f706bba0c35e079d41c56d43c3bdc443671d9021cb16e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599ad20c3ebb656850ac79a42ce761884b969108d7bc0af6b3865c43ec8c6210(
    value: typing.Optional[IntegrationConnectorsConnectionNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f84003442bb2f17f2449e577b2b4f4ee4fd1bef363d97c16635039e7da0b39(
    *,
    type: builtins.str,
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionSslConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_certificate: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    client_cert_type: typing.Optional[builtins.str] = None,
    client_private_key: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfigClientPrivateKey, typing.Dict[builtins.str, typing.Any]]] = None,
    client_private_key_pass: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass, typing.Dict[builtins.str, typing.Any]]] = None,
    private_server_certificate: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfigPrivateServerCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    server_cert_type: typing.Optional[builtins.str] = None,
    trust_model: typing.Optional[builtins.str] = None,
    use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c663feb12c8390cf4efaa5a955ed8ba6c42953c4dda5126e4384ba589c1f77(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93216645811c53ea7f047086f8dfcaa9e6cedfc9ca2c8b26f609bd79e7ec4092(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a786e0ecc0cd6cbdd36c8506ebaa16878e908ed757380b08bf58a8728ab5ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072909afaf9f4a98fba64039eccc9860851120808d8b438a340d951e46091609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2811528cfe600f6414af8f73c8c5ecbe81d68b6d5b819b58bbe2bdb62c04f3b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e1b4f77dfad5f10b508f670688ecf219c286a29a9ce54f299f7711d9827052(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9d7eec61c7e997ebf0232318577f82885a9536a423a52e0253d0c5daa9f6e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85e81acf597eb917efc64f5eaeb1d3c054feea79fc93d822e1bcd5bb9e5e555(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4248032990e7a6da93bf1986885c7163264cc9fad3c8bb5e6b8e90fb03c9f9fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82062f0ba71bf6b9bebf7712b36e0c7d638cc1b8333cf84c831bb2d49090f1f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b5e2aba93b8973326038d68f9262aade5a4ba1dddc2424dbaf53014ff9f52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9fa48c59a75dc31da8bea5a4bc69beff479aee39d0d114f8c96e1daad257a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationConnectorsConnectionSslConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5564e66df51648ac596836a72eef4b06b3e1ab7915136bf36a39a5bf7dd49c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e186832667c69fe8cd91d95cc0dbd3a62a0ca90dc5b1caa331c059818a413e89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f689ae666b7e2eeda166d635f6760ce0d18e819418f7a0e2f94bc99bfc03a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd97a3664b11542918d17ec12acf8a1a1cfc31e991024d3281fda08556212317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc30deb868101ad791decbc7a6fec1d54e722bd4f52f4e983aca3cbba449f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c4d6b6847df106033d463c9d4d2e73b853b469d3cd1957a1385ce469d26e9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionSslConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a098e37405933a001829f1b171e9d9c1d048ccc594e0845fe38e2a9e2a9155a(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779119a255522620d0d60c749ecc0108791028925f9fdf4fa3f00de812155091(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a290a20e4a2e935145358a688b99a8b4795af7ebf8eb20b6ef22e6694729097c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efee0656acb675a191bf39230632162c04b84dff9557cc72072199beb740d1f7(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebda8cc556302d5c9a9ca0c0c226dfe4ed3f1f5c7fae93e08ce022579916a65(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc331baec911743e8a587650659276090ab00e6ae968ee0e3f2850a0d7e52701(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2518a01d67a18d5629831e95932011d26404ed6a938ea68bde2a1e9b0f9995c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fb15deeedaa338f36148d82b34834f102db758ea5701b7359128360d1fd5ad(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfigClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5362f5d86fec9831a6d16ab93f39265c541de45c8574278a2810f51c0f6d5aa1(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d88090ad11f470b38b770f8f314154b3424aaccac2addb68204b933d4faa564(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59ff8af8a676d4297c0a5e1e182fee851dc3379a72f7e068f2061a4b849c923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3412ba66b15677ba92fd8a131492cf5142179a70cdda6fd6d9db9131fbfd6d5a(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1302620ff7359db642c8af507a43185dcbbf846a73493cc9da689747fb339b1d(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec89ef1bdac4d06655c1c43e1e6d8a512ac21a55b205d5bc91bf9c8b23d4cb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5854c63a2d808b215fc47ed835d4463dd77076f3310d833a1811453bfd0005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b30744be7e145a2a7548e28684498b9c75e7888a919171f0d277e535b092db(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfigClientPrivateKeyPass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713b26756602aad44575b2015ccc80f1b3b88e8f2b18d95e0c3fc06c41a2adec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc833e1ca12ad78f69ed4144f3010060fb8e11d377fb3a5b212c53256b433006(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationConnectorsConnectionSslConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6b5f3fde28e36a0d9148ab2084ffbf1f17470c9e863833a483726b13d6e6e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4573763a7b5631e705d361e5c565f8afccd4193ce7de69577eb502e7236149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4715d70181fa2f1b1fd37feccf8662df3bd58753964e9cda34b6defdcfba02c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4907ee12ac4b9972824739708d50be31a7dde63f6a4774e8233af29a76a8a73d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e307c464374fd134c486dac8f015e28702ac8d675d41a3d9a6860c9864f4e3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50adfd58dfb93dff1a9a58c3bed3da38ac9f639cda743c4f7894e5eec591708(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f98f0f1175752ab8ca4355d80ca02cb3218996acba9a3305572381611cf5cf(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf11a925bcd83ae01949bd659882538d2abc2cbbad292075fb9500cab30464f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555ddcf4b895366a9aeec2ec7c5d88e636c17381253c112a1e154653b909c11c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3daeadd46525241fa52386b2f4e609731beba0915c5bac00904b11c6aa4c5d2a(
    value: typing.Optional[IntegrationConnectorsConnectionSslConfigPrivateServerCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330f6f33eb4e4b470ae39fc9c5f00326ad394a6594412fedb37f0092378c7a6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455c083b13c765fcd0f9042122c895705269df08f757f68a59d008f719dd261f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c31b8ad280a91439452b7d5b4f3451d7a300cf10e98a61e159b2979aba650ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c079f1ab0277b90b016447d1e8e6b020b33cb8dacff9651055b4d8df51f14c6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba83a37baafd5b22ad4e3aebe99e77705014d5d41faac96469235632fecb76f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aad8286e6c4ea654c27809b53859572720750c9348a47016768e01b2f9165a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc627c0b30a07e747e5a9ba85467424bb831ae37ea4c8e72c83496354043a51(
    value: typing.Optional[IntegrationConnectorsConnectionStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f884edec2a25cbab5894e1cc4f1be76d2885ed99984ab4bffbdeefd4a7d2d511(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17397827d6be345bf4535ef72d5fd46cc298e6c9793317fa637623b435027dfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43efb7a9e57bd12799a20696d70d175e6906146516dc126dd9c74f045b94c333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6a9a98d3911d94ba2270a2266dc349c9fa2c877764c755ff3dd0397c667202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8b2ce2331df4de6efeed832d97a448d64173702444f160c06dba38f7dc2194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c592f2d8469372b2c38d6dcb69c522f3ea8cbed64501bfc19495336dc7989f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationConnectorsConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
