r'''
# `google_integration_connectors_connection`

Refer to the Terraform Registry for docs: [`google_integration_connectors_connection`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection).
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


class GoogleIntegrationConnectorsConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection google_integration_connectors_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connector_version: builtins.str,
        location: builtins.str,
        name: builtins.str,
        auth_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionConfigVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionDestinationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        eventing_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        eventing_enablement_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lock_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionLockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection google_integration_connectors_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connector_version: connectorVersion of the Connector. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#connector_version GoogleIntegrationConnectorsConnection#connector_version}
        :param location: Location in which Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#location GoogleIntegrationConnectorsConnection#location}
        :param name: Name of Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#name GoogleIntegrationConnectorsConnection#name}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_config GoogleIntegrationConnectorsConnection#auth_config}
        :param config_variable: config_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#config_variable GoogleIntegrationConnectorsConnection#config_variable}
        :param description: An arbitrary description for the Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#description GoogleIntegrationConnectorsConnection#description}
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination_config GoogleIntegrationConnectorsConnection#destination_config}
        :param eventing_config: eventing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#eventing_config GoogleIntegrationConnectorsConnection#eventing_config}
        :param eventing_enablement_type: Eventing enablement type. Will be nil if eventing is not enabled. Possible values: ["EVENTING_AND_CONNECTION", "ONLY_EVENTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#eventing_enablement_type GoogleIntegrationConnectorsConnection#eventing_enablement_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#id GoogleIntegrationConnectorsConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#labels GoogleIntegrationConnectorsConnection#labels}
        :param lock_config: lock_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#lock_config GoogleIntegrationConnectorsConnection#lock_config}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#log_config GoogleIntegrationConnectorsConnection#log_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#node_config GoogleIntegrationConnectorsConnection#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#project GoogleIntegrationConnectorsConnection#project}.
        :param service_account: Service account needed for runtime plane to access Google Cloud resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_account GoogleIntegrationConnectorsConnection#service_account}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssl_config GoogleIntegrationConnectorsConnection#ssl_config}
        :param suspended: Suspended indicates if a user has suspended a connection or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#suspended GoogleIntegrationConnectorsConnection#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#timeouts GoogleIntegrationConnectorsConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3846c11b0728e49d19a9fe4b0c09d71b7c755209781db53f91dd5ba27e619d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIntegrationConnectorsConnectionConfig(
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
        '''Generates CDKTF code for importing a GoogleIntegrationConnectorsConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleIntegrationConnectorsConnection to import.
        :param import_from_id: The id of the existing GoogleIntegrationConnectorsConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleIntegrationConnectorsConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92e27dd8b512a3c3c9a87b36d859be7e18db83d01cffc0451fad277eeb4e962)
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
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
        oauth2_auth_code_flow: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_jwt_bearer: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_key: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigUserPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["AUTH_TYPE_UNSPECIFIED", "USER_PASSWORD", "OAUTH2_JWT_BEARER", "OAUTH2_CLIENT_CREDENTIALS", "SSH_PUBLIC_KEY", "OAUTH2_AUTH_CODE_FLOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_type GoogleIntegrationConnectorsConnection#auth_type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_key GoogleIntegrationConnectorsConnection#auth_key}
        :param oauth2_auth_code_flow: oauth2_auth_code_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_auth_code_flow GoogleIntegrationConnectorsConnection#oauth2_auth_code_flow}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_client_credentials GoogleIntegrationConnectorsConnection#oauth2_client_credentials}
        :param oauth2_jwt_bearer: oauth2_jwt_bearer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_jwt_bearer GoogleIntegrationConnectorsConnection#oauth2_jwt_bearer}
        :param ssh_public_key: ssh_public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_public_key GoogleIntegrationConnectorsConnection#ssh_public_key}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#user_password GoogleIntegrationConnectorsConnection#user_password}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfig(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionConfigVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c01ab1751a35eb9e83fba1e59f511472ee97a14bc0311a9aa654b42637b4694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfigVariable", [value]))

    @jsii.member(jsii_name="putDestinationConfig")
    def put_destination_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionDestinationConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee966f3960c7d234d87c4d243da63ced2918fc4d3cfbdfc72a6c84df1678a8ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationConfig", [value]))

    @jsii.member(jsii_name="putEventingConfig")
    def put_eventing_config(
        self,
        *,
        registration_destination_config: typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enrichment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registration_destination_config: registration_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#registration_destination_config GoogleIntegrationConnectorsConnection#registration_destination_config}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_config GoogleIntegrationConnectorsConnection#auth_config}
        :param enrichment_enabled: Enrichment Enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enrichment_enabled GoogleIntegrationConnectorsConnection#enrichment_enabled}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfig(
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
        :param locked: Indicates whether or not the connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#locked GoogleIntegrationConnectorsConnection#locked}
        :param reason: Describes why a connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#reason GoogleIntegrationConnectorsConnection#reason}
        '''
        value = GoogleIntegrationConnectorsConnectionLockConfig(
            locked=locked, reason=reason
        )

        return typing.cast(None, jsii.invoke(self, "putLockConfig", [value]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enabled represents whether logging is enabled or not for a connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enabled GoogleIntegrationConnectorsConnection#enabled}
        '''
        value = GoogleIntegrationConnectorsConnectionLogConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#max_node_count GoogleIntegrationConnectorsConnection#max_node_count}
        :param min_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#min_node_count GoogleIntegrationConnectorsConnection#min_node_count}
        '''
        value = GoogleIntegrationConnectorsConnectionNodeConfig(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putSslConfig")
    def put_ssl_config(
        self,
        *,
        type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        client_cert_type: typing.Optional[builtins.str] = None,
        client_private_key: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey", typing.Dict[builtins.str, typing.Any]]] = None,
        client_private_key_pass: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass", typing.Dict[builtins.str, typing.Any]]] = None,
        private_server_certificate: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        server_cert_type: typing.Optional[builtins.str] = None,
        trust_model: typing.Optional[builtins.str] = None,
        use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Enum for controlling the SSL Type (TLS/MTLS) Possible values: ["TLS", "MTLS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_certificate GoogleIntegrationConnectorsConnection#client_certificate}
        :param client_cert_type: Type of Client Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_cert_type GoogleIntegrationConnectorsConnection#client_cert_type}
        :param client_private_key: client_private_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_private_key GoogleIntegrationConnectorsConnection#client_private_key}
        :param client_private_key_pass: client_private_key_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_private_key_pass GoogleIntegrationConnectorsConnection#client_private_key_pass}
        :param private_server_certificate: private_server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#private_server_certificate GoogleIntegrationConnectorsConnection#private_server_certificate}
        :param server_cert_type: Type of Server Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#server_cert_type GoogleIntegrationConnectorsConnection#server_cert_type}
        :param trust_model: Enum for Trust Model Possible values: ["PUBLIC", "PRIVATE", "INSECURE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#trust_model GoogleIntegrationConnectorsConnection#trust_model}
        :param use_ssl: Bool for enabling SSL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#use_ssl GoogleIntegrationConnectorsConnection#use_ssl}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#create GoogleIntegrationConnectorsConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#delete GoogleIntegrationConnectorsConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#update GoogleIntegrationConnectorsConnection#update}.
        '''
        value = GoogleIntegrationConnectorsConnectionTimeouts(
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
    def auth_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigOutputReference", jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="configVariable")
    def config_variable(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionConfigVariableList":
        return typing.cast("GoogleIntegrationConnectorsConnectionConfigVariableList", jsii.get(self, "configVariable"))

    @builtins.property
    @jsii.member(jsii_name="connectionRevision")
    def connection_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionRevision"))

    @builtins.property
    @jsii.member(jsii_name="connectorVersionInfraConfig")
    def connector_version_infra_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigList":
        return typing.cast("GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigList", jsii.get(self, "connectorVersionInfraConfig"))

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
    ) -> "GoogleIntegrationConnectorsConnectionDestinationConfigList":
        return typing.cast("GoogleIntegrationConnectorsConnectionDestinationConfigList", jsii.get(self, "destinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="eventingConfig")
    def eventing_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigOutputReference", jsii.get(self, "eventingConfig"))

    @builtins.property
    @jsii.member(jsii_name="eventingRuntimeData")
    def eventing_runtime_data(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingRuntimeDataList":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingRuntimeDataList", jsii.get(self, "eventingRuntimeData"))

    @builtins.property
    @jsii.member(jsii_name="lockConfig")
    def lock_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionLockConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionLockConfigOutputReference", jsii.get(self, "lockConfig"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionLogConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionNodeConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectory")
    def service_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceDirectory"))

    @builtins.property
    @jsii.member(jsii_name="sslConfig")
    def ssl_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionSslConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionSslConfigOutputReference", jsii.get(self, "sslConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GoogleIntegrationConnectorsConnectionStatusList":
        return typing.cast("GoogleIntegrationConnectorsConnectionStatusList", jsii.get(self, "status"))

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
    def timeouts(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionTimeoutsOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfig"], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="configVariableInput")
    def config_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionConfigVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionConfigVariable"]]], jsii.get(self, "configVariableInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionDestinationConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionDestinationConfig"]]], jsii.get(self, "destinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventingConfigInput")
    def eventing_config_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfig"], jsii.get(self, "eventingConfigInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionLockConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionLockConfig"], jsii.get(self, "lockConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionLogConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionNodeConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionNodeConfig"], jsii.get(self, "nodeConfigInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfig"], jsii.get(self, "sslConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIntegrationConnectorsConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIntegrationConnectorsConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorVersion")
    def connector_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorVersion"))

    @connector_version.setter
    def connector_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01fb223abbc8d598528d9f8fdbbdbfb1b0d5147af5fa71f64846d9892e588a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967b26b00f8d47e755b2ac42b689f6585c96b3d31eb8435374d276754c7f9870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventingEnablementType")
    def eventing_enablement_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventingEnablementType"))

    @eventing_enablement_type.setter
    def eventing_enablement_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d89434b5b586d501ee413944ef519eaff232a908783055309ec1e9e3fe02e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventingEnablementType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2274b71a80efcf35aff696e147b61b8df7b6a79470e4a0e62d846ec7407b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9003a9012d7d68a08ce54c6a270d648a5f1617d2305210676d27fa6fbc7e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa45363279e1bd5e3832a1682af00fdb7000a2b27a0dd39d7dc11b957b8a605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb804713bed2b786770f922c4887ada3fcfe4b373fb9dcd1c50250054aa99b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969cfbac133ca15acc0b2aebff6592f1718a034f1596e0bd528e0a9a2c75ad2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470e3d0026e3b4ec3fc7ca5e726c68801ea555086e65f5a1ab3bccfe75c80720)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5acfe87518a0178b935df7eea7f8de8f2181ffd6f4d48c8acc83fe15eaae5df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfig",
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
class GoogleIntegrationConnectorsConnectionAuthConfig:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
        oauth2_auth_code_flow: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_jwt_bearer: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_key: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigUserPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["AUTH_TYPE_UNSPECIFIED", "USER_PASSWORD", "OAUTH2_JWT_BEARER", "OAUTH2_CLIENT_CREDENTIALS", "SSH_PUBLIC_KEY", "OAUTH2_AUTH_CODE_FLOW"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_type GoogleIntegrationConnectorsConnection#auth_type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_key GoogleIntegrationConnectorsConnection#auth_key}
        :param oauth2_auth_code_flow: oauth2_auth_code_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_auth_code_flow GoogleIntegrationConnectorsConnection#oauth2_auth_code_flow}
        :param oauth2_client_credentials: oauth2_client_credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_client_credentials GoogleIntegrationConnectorsConnection#oauth2_client_credentials}
        :param oauth2_jwt_bearer: oauth2_jwt_bearer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_jwt_bearer GoogleIntegrationConnectorsConnection#oauth2_jwt_bearer}
        :param ssh_public_key: ssh_public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_public_key GoogleIntegrationConnectorsConnection#ssh_public_key}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#user_password GoogleIntegrationConnectorsConnection#user_password}
        '''
        if isinstance(oauth2_auth_code_flow, dict):
            oauth2_auth_code_flow = GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow(**oauth2_auth_code_flow)
        if isinstance(oauth2_client_credentials, dict):
            oauth2_client_credentials = GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials(**oauth2_client_credentials)
        if isinstance(oauth2_jwt_bearer, dict):
            oauth2_jwt_bearer = GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer(**oauth2_jwt_bearer)
        if isinstance(ssh_public_key, dict):
            ssh_public_key = GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey(**ssh_public_key)
        if isinstance(user_password, dict):
            user_password = GoogleIntegrationConnectorsConnectionAuthConfigUserPassword(**user_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c80dda8c91f8e95ff493b48d147e78a8e4706740426c282adfdd1975eb4e9e2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_type GoogleIntegrationConnectorsConnection#auth_type}
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable"]]], result)

    @builtins.property
    def auth_key(self) -> typing.Optional[builtins.str]:
        '''The type of authentication configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_key GoogleIntegrationConnectorsConnection#auth_key}
        '''
        result = self._values.get("auth_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth2_auth_code_flow(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow"]:
        '''oauth2_auth_code_flow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_auth_code_flow GoogleIntegrationConnectorsConnection#oauth2_auth_code_flow}
        '''
        result = self._values.get("oauth2_auth_code_flow")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow"], result)

    @builtins.property
    def oauth2_client_credentials(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials"]:
        '''oauth2_client_credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_client_credentials GoogleIntegrationConnectorsConnection#oauth2_client_credentials}
        '''
        result = self._values.get("oauth2_client_credentials")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials"], result)

    @builtins.property
    def oauth2_jwt_bearer(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer"]:
        '''oauth2_jwt_bearer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#oauth2_jwt_bearer GoogleIntegrationConnectorsConnection#oauth2_jwt_bearer}
        '''
        result = self._values.get("oauth2_jwt_bearer")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer"], result)

    @builtins.property
    def ssh_public_key(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey"]:
        '''ssh_public_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_public_key GoogleIntegrationConnectorsConnection#ssh_public_key}
        '''
        result = self._values.get("ssh_public_key")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey"], result)

    @builtins.property
    def user_password(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPassword"]:
        '''user_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#user_password GoogleIntegrationConnectorsConnection#user_password}
        '''
        result = self._values.get("user_password")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPassword"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable",
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
class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244aacb073e53ed4089f9ffb376d0a60eae8dd2b159cf5ab4d34a34a63345bea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "kms_key_name": "kmsKeyName"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9c74e3e6848da09a4f3e6ec0f6b9cad7cad231434230207cc06b690b153215)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0365003c5e2ea3c1b94c4371312831c0703a0217b8bd09356ec4781f46229e3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e87a3b2afab80f93eb42c29c020b0eeda9537e0baf06cbfaf6c4563e4e41387d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a128ffcb8db3e6a748529afb3d149c6fb4ee3b2fe088574e75e8705cd75ea47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af00146a6d0ef98b5ef9e6f9bf5da371a3d504131db565c2e4a68b799ec08d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fd28ae52ffd5d234732e97d61ab6bead92556b6026ae44b901f6fcb59b80f48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66aa0bfe9754616094e0ee8a6d8db9ee898d01ea33f23dc774a6f31bb06c76f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e45e6fd96ad3f47f366fa559979c80f533e5125d99cfc662f9152cd48bec4b85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb9ab960beca42b6dd6838c40a5d0aefaf1b635ba32cdd335ea399f693fb6542)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6baebaefeeefce2c769c6c0c92b6f01369a8b81a46e544a952ab5c5ebb135665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb67b8f06dd3b1a02abaeb1f665f5915ed0121785430687d0fa4c2a5cb4df55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3df540d63422bceb701e73dc8b413e35951cb80342872c16c18ef045e029d6a9)
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
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue(
            type=type, kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue(
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
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2433d8f8ba7129820417d33298f7751eb6aedce4fc1b5eda57b47416e8bf92dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2284c868faaa8014a2fb39c18d211fcc46184a823bfbe25294b8e23b6f459fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44040db9456725894f91d2051dd8bce5c5c5a5208346c02abc2ad871a0d001c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb940bdb1797152631ed9e2be923db5d5841cab1df56973321933f43868cfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af67614cc3ecb866d8e51e585148fd30c15895c730add9e94d46d3df90d5646a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e028a64a21b0310c6caa1d720864bfa084ff1964f10647c68c2d8c1fd51d6de)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52eb4b6d2d2ec11d33d6a0a62980cf9207cfa6826674927411bc0abedd151a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__383e1f7a21de2bdaf0770ea9ddb482029f088db6099cce36ca0c5a670fd030e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6ea31518181d1529ac7fec5f4f28f1ced6b5a5192a9893352589e440792dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow",
    jsii_struct_bases=[],
    name_mapping={
        "auth_uri": "authUri",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enable_pkce": "enablePkce",
        "scopes": "scopes",
    },
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow:
    def __init__(
        self,
        *,
        auth_uri: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_pkce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param auth_uri: Auth URL for Authorization Code Flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_uri GoogleIntegrationConnectorsConnection#auth_uri}
        :param client_id: Client ID for user-provided OAuth app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_id GoogleIntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_secret GoogleIntegrationConnectorsConnection#client_secret}
        :param enable_pkce: Whether to enable PKCE when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enable_pkce GoogleIntegrationConnectorsConnection#enable_pkce}
        :param scopes: Scopes the connection will request when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#scopes GoogleIntegrationConnectorsConnection#scopes}
        '''
        if isinstance(client_secret, dict):
            client_secret = GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret(**client_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1135aed472915a69ddb4fed52c058ddb3378f8d108966d69194495b8dffa1dbe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_uri GoogleIntegrationConnectorsConnection#auth_uri}
        '''
        result = self._values.get("auth_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID for user-provided OAuth app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_id GoogleIntegrationConnectorsConnection#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret"]:
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_secret GoogleIntegrationConnectorsConnection#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret"], result)

    @builtins.property
    def enable_pkce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable PKCE when the user performs the auth code flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enable_pkce GoogleIntegrationConnectorsConnection#enable_pkce}
        '''
        result = self._values.get("enable_pkce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Scopes the connection will request when the user performs the auth code flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#scopes GoogleIntegrationConnectorsConnection#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47cdb57c1c62cdf2d5f33641750ae01b74b6f6cfab9064c795a59de09d7688f2)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb7d86988350de854a9512dd478b08836d0ce6a42aff9d7e3ceeabb98acee025)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b16dca7b685b542536bb6e982634b1988f589b7187461e514e7d2f603036c97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5f366f6d811738fd59d050c2ea5bdb85c3e5469f951b800bcecd4e0cd3d898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38fa35792e3cb68c04619fe966d033b00cb43476d0106f1ad45e085489152a2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret(
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
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference, jsii.get(self, "clientSecret"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret], jsii.get(self, "clientSecretInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4a92b091bb84e0d3020946015d8679474ee0c953c40a6133e74c821537f1b9fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8ec8a508ae2b878bca6348f58a052c059d657196f1e58e9733f816da23a7bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7381efd9ead774ab865c42bf3e2fadaff6f0afffda394748291d29972496bd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePkce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2abf1d6c8dbf1e9db11419100664c816e9c3ed274a7824e7c25fd4e7a93ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e20195114374b758152c78d3ce65bb32aeff04b029f0afb1a214ee30d45a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Secret version of Password for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_id GoogleIntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_secret GoogleIntegrationConnectorsConnection#client_secret}
        '''
        if isinstance(client_secret, dict):
            client_secret = GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret(**client_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b9804cb887b58788d7d3a8afe9063834030727d1419704053d93bc9b67d38a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_id GoogleIntegrationConnectorsConnection#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret"]:
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_secret GoogleIntegrationConnectorsConnection#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d69f7400e9237bc84502154731aaac008479c79df56749894c45bf05142d91e)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7934052aeee45db5df26f50fce8f8cea404d3d1551eb38fa1edebd9122be5380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__351ea48d679f9514b0e543eb2765a98b6eb70c59b1be74356cff0ee1794126a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bd9cd240fa651b6135416b93d71a68f9816cbab8dd9b2bdcb44b366d5f2094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4085222c240748d2ce76cc28477a2dc4ca1317af426c80243e997e832fa27efe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret(
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
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668024fa531aab97bc84ee12d0200c5c4ccfd80258781c032df6acfe65217ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2dd569cfb7f8c7ebb4bbce134657d68caa03bd79aa50aca687870ac95f8bc53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer",
    jsii_struct_bases=[],
    name_mapping={"client_key": "clientKey", "jwt_claims": "jwtClaims"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer:
    def __init__(
        self,
        *,
        client_key: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey", typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_claims: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_key: client_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_key GoogleIntegrationConnectorsConnection#client_key}
        :param jwt_claims: jwt_claims block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#jwt_claims GoogleIntegrationConnectorsConnection#jwt_claims}
        '''
        if isinstance(client_key, dict):
            client_key = GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey(**client_key)
        if isinstance(jwt_claims, dict):
            jwt_claims = GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims(**jwt_claims)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867d3e5058f6988ebe3014056d1df51c7086f75fb952561cb4c875dd3634e4b9)
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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey"]:
        '''client_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_key GoogleIntegrationConnectorsConnection#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey"], result)

    @builtins.property
    def jwt_claims(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims"]:
        '''jwt_claims block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#jwt_claims GoogleIntegrationConnectorsConnection#jwt_claims}
        '''
        result = self._values.get("jwt_claims")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439ef09587073eb7ba79b0381b091fe3e4ce78c52b37402be87e91be1a979236)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea6465364fc607ddcc15b62786482a949cfc4f1fa0fd429991d3bd8602e1222f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c7b92896effb570688fcdb2b814e276069052ed3ae32a0e549592c01cfe1f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5e4eaef4dd47dcbd532d4b5ebd916337c65a888ad00826e03062a16d6f359d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims",
    jsii_struct_bases=[],
    name_mapping={"audience": "audience", "issuer": "issuer", "subject": "subject"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims:
    def __init__(
        self,
        *,
        audience: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param audience: Value for the "aud" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#audience GoogleIntegrationConnectorsConnection#audience}
        :param issuer: Value for the "iss" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#issuer GoogleIntegrationConnectorsConnection#issuer}
        :param subject: Value for the "sub" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#subject GoogleIntegrationConnectorsConnection#subject}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c497fac4fc9d3bbb3f65be10c2b9c47de53b5df2d72ba362f2d9088820aa267a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#audience GoogleIntegrationConnectorsConnection#audience}
        '''
        result = self._values.get("audience")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''Value for the "iss" claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#issuer GoogleIntegrationConnectorsConnection#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''Value for the "sub" claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#subject GoogleIntegrationConnectorsConnection#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca8921961ac23b70c359b6d18d4bcd16290ceafc0fa69720eecd52c58a729547)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ae8eda786379cf461f762369f5cac2ea5e3a79a2355b19537892ee2a98fe75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc351571b00c45373d513e345742164ca5ac9dc397200ac049c4233531a9efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7a7a8b1ce67737b71dc28a4a0a9d38bd159b2e63130c43418896473c05818f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5696ccb3fc26763fc1d7e858150ff060fab646880b0132305bc751691601d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba868470dd758296817f4611c526db2032c1d8fb529577f2050cdaf59ede5d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientKey")
    def put_client_key(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey(
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
        :param audience: Value for the "aud" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#audience GoogleIntegrationConnectorsConnection#audience}
        :param issuer: Value for the "iss" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#issuer GoogleIntegrationConnectorsConnection#issuer}
        :param subject: Value for the "sub" claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#subject GoogleIntegrationConnectorsConnection#subject}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims(
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
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference, jsii.get(self, "clientKey"))

    @builtins.property
    @jsii.member(jsii_name="jwtClaims")
    def jwt_claims(
        self,
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference, jsii.get(self, "jwtClaims"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtClaimsInput")
    def jwt_claims_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims], jsii.get(self, "jwtClaimsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6587da0100b671fb3391572e31fe74c001adb202c4e969896fba5205c209fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbddc38487defdb2ced6129c49c9bd7ff3782ae49c3d5650b2130698116a5d2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494c79eeb78cc97a210503e98eea5f1bc9d4a6d23a14bca192c1b7e0a61f4765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putOauth2AuthCodeFlow")
    def put_oauth2_auth_code_flow(
        self,
        *,
        auth_uri: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_pkce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param auth_uri: Auth URL for Authorization Code Flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_uri GoogleIntegrationConnectorsConnection#auth_uri}
        :param client_id: Client ID for user-provided OAuth app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_id GoogleIntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_secret GoogleIntegrationConnectorsConnection#client_secret}
        :param enable_pkce: Whether to enable PKCE when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enable_pkce GoogleIntegrationConnectorsConnection#enable_pkce}
        :param scopes: Scopes the connection will request when the user performs the auth code flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#scopes GoogleIntegrationConnectorsConnection#scopes}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow(
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
        client_secret: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_id: Secret version of Password for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_id GoogleIntegrationConnectorsConnection#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_secret GoogleIntegrationConnectorsConnection#client_secret}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2ClientCredentials", [value]))

    @jsii.member(jsii_name="putOauth2JwtBearer")
    def put_oauth2_jwt_bearer(
        self,
        *,
        client_key: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey, typing.Dict[builtins.str, typing.Any]]] = None,
        jwt_claims: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_key: client_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_key GoogleIntegrationConnectorsConnection#client_key}
        :param jwt_claims: jwt_claims block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#jwt_claims GoogleIntegrationConnectorsConnection#jwt_claims}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer(
            client_key=client_key, jwt_claims=jwt_claims
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2JwtBearer", [value]))

    @jsii.member(jsii_name="putSshPublicKey")
    def put_ssh_public_key(
        self,
        *,
        username: builtins.str,
        cert_type: typing.Optional[builtins.str] = None,
        ssh_client_cert: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_client_cert_pass: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: The user account used to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        :param cert_type: Format of SSH Client cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#cert_type GoogleIntegrationConnectorsConnection#cert_type}
        :param ssh_client_cert: ssh_client_cert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_client_cert GoogleIntegrationConnectorsConnection#ssh_client_cert}
        :param ssh_client_cert_pass: ssh_client_cert_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_client_cert_pass GoogleIntegrationConnectorsConnection#ssh_client_cert_pass}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey(
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
        password: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#password GoogleIntegrationConnectorsConnection#password}
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigUserPassword(
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
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableList:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthCodeFlow")
    def oauth2_auth_code_flow(
        self,
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference, jsii.get(self, "oauth2AuthCodeFlow"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentials")
    def oauth2_client_credentials(
        self,
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference, jsii.get(self, "oauth2ClientCredentials"))

    @builtins.property
    @jsii.member(jsii_name="oauth2JwtBearer")
    def oauth2_jwt_bearer(
        self,
    ) -> GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference, jsii.get(self, "oauth2JwtBearer"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference", jsii.get(self, "sshPublicKey"))

    @builtins.property
    @jsii.member(jsii_name="userPassword")
    def user_password(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference", jsii.get(self, "userPassword"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow], jsii.get(self, "oauth2AuthCodeFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsInput")
    def oauth2_client_credentials_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials], jsii.get(self, "oauth2ClientCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2JwtBearerInput")
    def oauth2_jwt_bearer_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer], jsii.get(self, "oauth2JwtBearerInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey"], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordInput")
    def user_password_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPassword"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPassword"], jsii.get(self, "userPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authKey")
    def auth_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authKey"))

    @auth_key.setter
    def auth_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62e44927776b5666915c89d05fc2353851e42de6b8c1bbb2b2c3055511f1c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3538206f1effdf9af92f1f8fd3941be891666a1a69583eeab55bbe467d0e5f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e828df8af6739b9a5c76e8e4101f055eeeccfff70d484712bbfbb945e5d907e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "cert_type": "certType",
        "ssh_client_cert": "sshClientCert",
        "ssh_client_cert_pass": "sshClientCertPass",
    },
)
class GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey:
    def __init__(
        self,
        *,
        username: builtins.str,
        cert_type: typing.Optional[builtins.str] = None,
        ssh_client_cert: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_client_cert_pass: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: The user account used to authenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        :param cert_type: Format of SSH Client cert. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#cert_type GoogleIntegrationConnectorsConnection#cert_type}
        :param ssh_client_cert: ssh_client_cert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_client_cert GoogleIntegrationConnectorsConnection#ssh_client_cert}
        :param ssh_client_cert_pass: ssh_client_cert_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_client_cert_pass GoogleIntegrationConnectorsConnection#ssh_client_cert_pass}
        '''
        if isinstance(ssh_client_cert, dict):
            ssh_client_cert = GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert(**ssh_client_cert)
        if isinstance(ssh_client_cert_pass, dict):
            ssh_client_cert_pass = GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass(**ssh_client_cert_pass)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902d5dc5d9d27737cbb80faa91a5784953a6a69bf4468761ca27f9bf0fc4c925)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cert_type(self) -> typing.Optional[builtins.str]:
        '''Format of SSH Client cert.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#cert_type GoogleIntegrationConnectorsConnection#cert_type}
        '''
        result = self._values.get("cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_client_cert(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"]:
        '''ssh_client_cert block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_client_cert GoogleIntegrationConnectorsConnection#ssh_client_cert}
        '''
        result = self._values.get("ssh_client_cert")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"], result)

    @builtins.property
    def ssh_client_cert_pass(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"]:
        '''ssh_client_cert_pass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssh_client_cert_pass GoogleIntegrationConnectorsConnection#ssh_client_cert_pass}
        '''
        result = self._values.get("ssh_client_cert_pass")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26d7be3be5c5bbc8911ce2212202ede204287ae53a0be964e5b28b7b2daaae42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSshClientCert")
    def put_ssh_client_cert(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putSshClientCert", [value]))

    @jsii.member(jsii_name="putSshClientCertPass")
    def put_ssh_client_cert_pass(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass(
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
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference", jsii.get(self, "sshClientCert"))

    @builtins.property
    @jsii.member(jsii_name="sshClientCertPass")
    def ssh_client_cert_pass(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference", jsii.get(self, "sshClientCertPass"))

    @builtins.property
    @jsii.member(jsii_name="certTypeInput")
    def cert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sshClientCertInput")
    def ssh_client_cert_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert"], jsii.get(self, "sshClientCertInput"))

    @builtins.property
    @jsii.member(jsii_name="sshClientCertPassInput")
    def ssh_client_cert_pass_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass"], jsii.get(self, "sshClientCertPassInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__eb21bec1e861518f4073211b1fb6d79b8a30096b0137f782fb222cf5e9b1fcf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820db1dfe025bd03555e9ee69aa336153a4386f3ab2cb50dcc74ee0319fcfdb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ee11aa161c322a5ee6bea70a5a74b40812c8ed5f5ed80fb88dea80e5f01a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dc21172183de2a1c99d90c290b8db8754c6b4406949d3d829dc91fa2f0baf0a)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57b25c405f59c5245549e0443d67d0135b90971ab9b01af8b29672c99d96b254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03ab5185390aefb014320e6dd5c7238e2f8d757fe335a2ab93b0a1ce359f1391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631ac18c489a52113704908aee7a0c66e8f892cb421029a261cbd8c4a04a5dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c6cee8f9826d221a9374f79f8625b777daf81ca23272dc0906591e0c9cb664)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32558227a00bd009a93650ebebe2d5f79ae11d63f7d43d33deb30b6b2b88f087)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ee33b363438bc05c0733307e7ee613213c2929373a9e1fc14956b2283d2705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a333efad38e0b614560015cb11ebe1f2ae7725336b629a27550b586e1cea2d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigUserPassword",
    jsii_struct_bases=[],
    name_mapping={"username": "username", "password": "password"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigUserPassword:
    def __init__(
        self,
        *,
        username: builtins.str,
        password: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#password GoogleIntegrationConnectorsConnection#password}
        '''
        if isinstance(password, dict):
            password = GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66eb6f3527aa66f301f6cc17892f5f531741c18d84fbad8a33364b055aa62fa2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword"]:
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#password GoogleIntegrationConnectorsConnection#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionAuthConfigUserPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d6a91b803bad5e02664c7030ebbd3ed3f6b508bcf47c889f30b5cf27ee47018)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPassword")
    def put_password(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword(
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
    ) -> "GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword"], jsii.get(self, "passwordInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__633f4df6846162f9c9da79f99c13491c556ead98c6ce668aae59b0a36cb7a23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPassword]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ebd1e2d79bedccfc23b625e6dba4c9340d6e7564f20023d5fb158a844a315a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b64e7c5678ead8b1c72eebff3a49c7c08efc0ffbfa1cde3997f47724619d81a)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a954c356e583b0eb66b620e9dc7caffd0719a54d11528385ead605a6ab5e627)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d288456f48603aab838f02c18b81fec30c4101c8a87f3f83dbb8bf6c0201a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b4d67d911ef417565454aa3805667fa57b907bd2bdcd4dfefed1774c5ff3e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfig",
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
class GoogleIntegrationConnectorsConnectionConfig(
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
        connector_version: builtins.str,
        location: builtins.str,
        name: builtins.str,
        auth_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionConfigVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionDestinationConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        eventing_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        eventing_enablement_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lock_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionLockConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        ssl_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connector_version: connectorVersion of the Connector. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#connector_version GoogleIntegrationConnectorsConnection#connector_version}
        :param location: Location in which Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#location GoogleIntegrationConnectorsConnection#location}
        :param name: Name of Connection needs to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#name GoogleIntegrationConnectorsConnection#name}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_config GoogleIntegrationConnectorsConnection#auth_config}
        :param config_variable: config_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#config_variable GoogleIntegrationConnectorsConnection#config_variable}
        :param description: An arbitrary description for the Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#description GoogleIntegrationConnectorsConnection#description}
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination_config GoogleIntegrationConnectorsConnection#destination_config}
        :param eventing_config: eventing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#eventing_config GoogleIntegrationConnectorsConnection#eventing_config}
        :param eventing_enablement_type: Eventing enablement type. Will be nil if eventing is not enabled. Possible values: ["EVENTING_AND_CONNECTION", "ONLY_EVENTING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#eventing_enablement_type GoogleIntegrationConnectorsConnection#eventing_enablement_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#id GoogleIntegrationConnectorsConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#labels GoogleIntegrationConnectorsConnection#labels}
        :param lock_config: lock_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#lock_config GoogleIntegrationConnectorsConnection#lock_config}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#log_config GoogleIntegrationConnectorsConnection#log_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#node_config GoogleIntegrationConnectorsConnection#node_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#project GoogleIntegrationConnectorsConnection#project}.
        :param service_account: Service account needed for runtime plane to access Google Cloud resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_account GoogleIntegrationConnectorsConnection#service_account}
        :param ssl_config: ssl_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssl_config GoogleIntegrationConnectorsConnection#ssl_config}
        :param suspended: Suspended indicates if a user has suspended a connection or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#suspended GoogleIntegrationConnectorsConnection#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#timeouts GoogleIntegrationConnectorsConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_config, dict):
            auth_config = GoogleIntegrationConnectorsConnectionAuthConfig(**auth_config)
        if isinstance(eventing_config, dict):
            eventing_config = GoogleIntegrationConnectorsConnectionEventingConfig(**eventing_config)
        if isinstance(lock_config, dict):
            lock_config = GoogleIntegrationConnectorsConnectionLockConfig(**lock_config)
        if isinstance(log_config, dict):
            log_config = GoogleIntegrationConnectorsConnectionLogConfig(**log_config)
        if isinstance(node_config, dict):
            node_config = GoogleIntegrationConnectorsConnectionNodeConfig(**node_config)
        if isinstance(ssl_config, dict):
            ssl_config = GoogleIntegrationConnectorsConnectionSslConfig(**ssl_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleIntegrationConnectorsConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd42eea643201dfcec57a669932cd990618a7263e3badc6e1da9dc82016cd2a0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#connector_version GoogleIntegrationConnectorsConnection#connector_version}
        '''
        result = self._values.get("connector_version")
        assert result is not None, "Required property 'connector_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Location in which Connection needs to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#location GoogleIntegrationConnectorsConnection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of Connection needs to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#name GoogleIntegrationConnectorsConnection#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_config(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfig]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_config GoogleIntegrationConnectorsConnection#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfig], result)

    @builtins.property
    def config_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionConfigVariable"]]]:
        '''config_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#config_variable GoogleIntegrationConnectorsConnection#config_variable}
        '''
        result = self._values.get("config_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionConfigVariable"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An arbitrary description for the Connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#description GoogleIntegrationConnectorsConnection#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionDestinationConfig"]]]:
        '''destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination_config GoogleIntegrationConnectorsConnection#destination_config}
        '''
        result = self._values.get("destination_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionDestinationConfig"]]], result)

    @builtins.property
    def eventing_config(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfig"]:
        '''eventing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#eventing_config GoogleIntegrationConnectorsConnection#eventing_config}
        '''
        result = self._values.get("eventing_config")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfig"], result)

    @builtins.property
    def eventing_enablement_type(self) -> typing.Optional[builtins.str]:
        '''Eventing enablement type. Will be nil if eventing is not enabled. Possible values: ["EVENTING_AND_CONNECTION", "ONLY_EVENTING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#eventing_enablement_type GoogleIntegrationConnectorsConnection#eventing_enablement_type}
        '''
        result = self._values.get("eventing_enablement_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#id GoogleIntegrationConnectorsConnection#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#labels GoogleIntegrationConnectorsConnection#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lock_config(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionLockConfig"]:
        '''lock_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#lock_config GoogleIntegrationConnectorsConnection#lock_config}
        '''
        result = self._values.get("lock_config")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionLockConfig"], result)

    @builtins.property
    def log_config(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#log_config GoogleIntegrationConnectorsConnection#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionLogConfig"], result)

    @builtins.property
    def node_config(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#node_config GoogleIntegrationConnectorsConnection#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionNodeConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#project GoogleIntegrationConnectorsConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account needed for runtime plane to access Google Cloud resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_account GoogleIntegrationConnectorsConnection#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_config(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfig"]:
        '''ssl_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#ssl_config GoogleIntegrationConnectorsConnection#ssl_config}
        '''
        result = self._values.get("ssl_config")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfig"], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Suspended indicates if a user has suspended a connection or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#suspended GoogleIntegrationConnectorsConnection#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#timeouts GoogleIntegrationConnectorsConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariable",
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
class GoogleIntegrationConnectorsConnectionConfigVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionConfigVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = GoogleIntegrationConnectorsConnectionConfigVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e413761710edebfcce19cc338437025ebb351faa7005010c82db96495b841141)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionConfigVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionConfigVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionConfigVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "kms_key_name": "kmsKeyName"},
)
class GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        type: builtins.str,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3490c652ef0de051b994ef4b20a06ca53e4a0ddffdeacfa1e2f13064f31b38a0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85e39343dba42970cdfa9c2cb85d5ebaf6bc6c48edcc77fd7c40b145f3aaff40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b77b9b1e3ec1594469b420a84b595cbb9445b544e536d5aaa2efe21afe9d7e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb85ec5667b953c83382a84dde55a988013080a26f72df5b8f425f36198acb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a914ee5d52a61e6dcbfdfe9f1cc3ff4f4883a699d6517e6389051bffb21f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionConfigVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__189ca11fc932d97e8f8ac801b40109b2065bb77404480aad634cf6da7c8aef97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionConfigVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3f2db28906ca00f964e08486d74b570b9241dc54c14bd22d090b84f5dccbb4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionConfigVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72399a29d6938eef6059530c0ecd64f6996c883cf899ae5d360ed7d71f228b23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__066daba24b1b8612feadfe4825d8fe7aa7c2812272376e8ea295c0b39292f89e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02cf9d7b9fe3fa7ab4839c4db2f5da29e5824eaa9ab8670e891887c2352d35c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionConfigVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionConfigVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionConfigVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1826f58e6488372da8743dd568a8b67e619e3fb628d7e8e62e12d65a50222c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionConfigVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__750449c72259b5eab223c5aaa9024ba3731b4b2d1d04be592edd51c80dc59323)
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
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue(
            type=type, kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionConfigVariableSecretValue(
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
    ) -> GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionConfigVariableSecretValueOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionConfigVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionConfigVariableSecretValue"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionConfigVariableSecretValue"], jsii.get(self, "secretValueInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9c440fc7adb75ab3f22fe016f39322444d5bf8940428c49b3fa72a8e0e94d263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1fd0bd17947517d04bc37b1444999f984ad054368528c1a08e2fe46b97682f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc086e19182a9f2c1a6b8e19f5e64e48aa60a3d9fdac0af8f20840165bb6f3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b71d7f95e37e72fc0305b63620fcaaf6cd0c662fc0de9968c4f0832f09a453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionConfigVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionConfigVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionConfigVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee3bfb6c85740e45637e0f9333d7f78fcab76fa85a35035067f2bf3510a2971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionConfigVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0183543818a08bea4a8e007da3f6029b9bc146dbcd786fe193861a0965e9e96f)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionConfigVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionConfigVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConfigVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__106e7a30aa708f9deff5ab97fade0b53e4d72e0f7ab30d29645ce42a479e43bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30b0c04a0c17d31b98b1140dbb345763af0ea35c5891930f06d03fa699e9a041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableSecretValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da26b8da0794f9ecd491635be156ed01309af11559c23cdf77baa71a3c3f35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39adcf7b8cbd054d621797bc88c6a8c5b29732f1fc295c9e624eb963c106a99b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc97567be26f355d7f18b08db5994716f5c38b7cc6c994e28fb3156da0696d4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a9a5578171b02fa000c552bad65d67a2028455b76a4e368e40b77c18095cc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5da99c057677614f7da442198e7caa38433140319d20c2e11555496368157183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40ea2b7da6ef66771d763a62b231df433a5f0dd565c675ae7af45f05c0f26210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9afd71ab2068a604f256686f7e5c776cbaa79ae0c5c9588a962c5f9f5e885300)
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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa5dd9e1ee527ea2a0fea7ab0867f817c0b142616fde4afa354274d83a5c650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "destination": "destination"},
)
class GoogleIntegrationConnectorsConnectionDestinationConfig:
    def __init__(
        self,
        *,
        key: builtins.str,
        destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionDestinationConfigDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param key: The key is the destination identifier that is supported by the Connector. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination GoogleIntegrationConnectorsConnection#destination}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56c15bffafc414873a964d22e0f8cc31779d16aa0b50942c91995f7f8bdcc45)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionDestinationConfigDestination"]]]:
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination GoogleIntegrationConnectorsConnection#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionDestinationConfigDestination"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionDestinationConfigDestination",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "service_attachment": "serviceAttachment",
    },
)
class GoogleIntegrationConnectorsConnectionDestinationConfigDestination:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: For publicly routable host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#host GoogleIntegrationConnectorsConnection#host}
        :param port: The port is the target port number that is accepted by the destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#port GoogleIntegrationConnectorsConnection#port}
        :param service_attachment: PSC service attachments. Format: projects/* /regions/* /serviceAttachments/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_attachment GoogleIntegrationConnectorsConnection#service_attachment} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1f8d618904950a1fe1a6aad0c454efe58547e8953674145ae31d7def9494ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#host GoogleIntegrationConnectorsConnection#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port is the target port number that is accepted by the destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#port GoogleIntegrationConnectorsConnection#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_attachment(self) -> typing.Optional[builtins.str]:
        '''PSC service attachments. Format: projects/* /regions/* /serviceAttachments/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_attachment GoogleIntegrationConnectorsConnection#service_attachment}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("service_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionDestinationConfigDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionDestinationConfigDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionDestinationConfigDestinationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97d8dd5dee1b5c74e36a8f81fbdfa2a1cc9adf6bd8a8eaae6648ce634cc550ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionDestinationConfigDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb6c64c79bc85074bd88e2bcb53d160958782facc947dc998e0367eb83cf10a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionDestinationConfigDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee75c5ee330a5b89d7a0107e93dfa27ce168b183e6eab766d3c59007348a3801)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3903f7cfd98dd80582f5465a457916e22ce5215c822d31a1afff8f1558ffd6ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30be18e3e8d4c5821b5b66acd1c5380e9c43d6869e4832de974db0c1e61b4c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c074efa35c7106828339a1febd92bce4cb6eccba22600d34717c4cfbaa81c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionDestinationConfigDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionDestinationConfigDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74dfbb0434b8b97da17a750e90e5cccb4aea56e904901a48073759c1b71f61ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9763c2ca8e9b393e5da65aaed1fd285eafd466cfb537168dc77bb089e61c8c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a01dd58cf4c884a314a1fb2989faec7eebaf6300584cf7d44b464458c2cdbae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @service_attachment.setter
    def service_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b6475795c2d3ab2f2daea93e4cf3c672643d6d5557301832d6ba5f6d9f7a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfigDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfigDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aed9c8ce3868bb7042beaa6787df175708875f61faa87ee402901a9fe9648e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionDestinationConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionDestinationConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0656e302108b376b4daacc5531de3699811ba6176fc32a3bab3f77f7fd55ff6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionDestinationConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7fa6ddd1b1fdf552fab09a0f88058cc9b25ffafd0cf36fd80826b43549ef4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionDestinationConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844691dcc9f4be6dfd6b57a093a9edd80bf511a2b858e696ec56cd8b07186e60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b213d96f8df90449778bbe58d5418e7a689ecc2081059584280b5cba37a1d603)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34f2de98cb794aeca5b6315aaf2b176a533bee95c20c137e36aed44889798d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a72083c9d53ad2ab68f3d015a72e9d2e158c2fe6d08ea9283fac81ed04ea109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9745b06b64b917407c3f36f8bb6c24263bc4720d9782cf57b35cd773812008)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44959a5faa8631c1d11160d2f4a91966bcb4118e4acaf4762746a00945a4e35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(
        self,
    ) -> GoogleIntegrationConnectorsConnectionDestinationConfigDestinationList:
        return typing.cast(GoogleIntegrationConnectorsConnectionDestinationConfigDestinationList, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]], jsii.get(self, "destinationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9b0caeb8e9a8f9e8a4e1b5ae2b9974d12f66cabd209fb76df19cb146d9e5ea4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de86a1a957e2617fb8bdf3d18202d5848c6e00c5263df97a26e74855d46ef863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "registration_destination_config": "registrationDestinationConfig",
        "additional_variable": "additionalVariable",
        "auth_config": "authConfig",
        "enrichment_enabled": "enrichmentEnabled",
    },
)
class GoogleIntegrationConnectorsConnectionEventingConfig:
    def __init__(
        self,
        *,
        registration_destination_config: typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig", typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enrichment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param registration_destination_config: registration_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#registration_destination_config GoogleIntegrationConnectorsConnection#registration_destination_config}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_config GoogleIntegrationConnectorsConnection#auth_config}
        :param enrichment_enabled: Enrichment Enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enrichment_enabled GoogleIntegrationConnectorsConnection#enrichment_enabled}
        '''
        if isinstance(registration_destination_config, dict):
            registration_destination_config = GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig(**registration_destination_config)
        if isinstance(auth_config, dict):
            auth_config = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig(**auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb36dd86335f91b17a68f4bd7803605f71cf0935a89c385b351769d5b50d86e)
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
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig":
        '''registration_destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#registration_destination_config GoogleIntegrationConnectorsConnection#registration_destination_config}
        '''
        result = self._values.get("registration_destination_config")
        assert result is not None, "Required property 'registration_destination_config' is missing"
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig", result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable"]]], result)

    @builtins.property
    def auth_config(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig"]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_config GoogleIntegrationConnectorsConnection#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig"], result)

    @builtins.property
    def enrichment_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enrichment Enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enrichment_enabled GoogleIntegrationConnectorsConnection#enrichment_enabled}
        '''
        result = self._values.get("enrichment_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable",
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
class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e2aceaa12aa12c5d75f6930cd21ed523a9312ae7fc498a7a06f5a10ed28f11)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "type": "type"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63713d8301fb3e91f32963aa85f3936ebca05af6b2e1f43ea0b4c96288277f8f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79b555dae13d49af8265b1b602b5762bba6a54cc1f92e44029347269fdcfbda8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ddbd549a93ba56f20e5708e20caeb1ffb093aee8a9fe964e22b8f4971d51da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f05fb0b6d4528e061230950dda8ff1683b308639bb62e4b933f5eac6883164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4ee80ddda1011a9c09ee744164f931b87f22cd86fdf4b1dc95439ed9eee615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5884622ed2b351cd2360a60d0291f402780bf9e17736affd313984782fc88d07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6102708df54dab51872192286a512ba49d1a46c23fdfdfc39cf669a9a9799ff9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f2fe939cc8c9ee4a4e7f4c6f49dd0ca7f7ce568247f49be4fdf767cf9fa5b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1174c538380a2a5114cb7c277e97a426ab6d61c5f347bb413c0192d38dbdac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85e5c5f72d57b03ddc9f6b0a4603910055aa0e875b2beb21de8e4e656f29c289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b32f61d035368db02f5f3f15427cd12b5d754655f5c9e18533e6d0a5d58131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a884c6343d53f4f3015b49453fa48d8b604826f132beb62c4be1377a51fad4b)
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
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue(
            kms_key_name=kms_key_name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue(
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
    ) -> GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6df6523c2beb8c95605382a8b747c4533bc79c635619af7b91e329f374eef182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2399ae0bce659b2082571be071740de7fbf44ca99d0b35d0318d9f35910c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aef9c274ef519b20fd6ef1d13892ae9e34156aa49200cc53cab927631240b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bc8b01791cddaacbf0dc9693a066492b72a632053ac5e07dbe34338fae0389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a51b8a10e6a48e6011b26ad6ae5551a9070f29d199521f14aab4a14f1931d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33450fedd5f829acbcce4cfcf0d0c727143c4fee9d83b019952a3bd4794d2f76)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdafceb80669ab6051badf0ebb5085b3ed5ea4225d4edbd7633ae63857a3236e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74271f86467e59cb72d5b68171014eeef24b4f85a48bb43b00a80bb989f96c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c45aada97633184cd590c96d211eed28391123b915f0066f38586ee644695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "user_password": "userPassword",
        "additional_variable": "additionalVariable",
        "auth_key": "authKey",
    },
)
class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        user_password: typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword", typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["USER_PASSWORD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_type GoogleIntegrationConnectorsConnection#auth_type}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#user_password GoogleIntegrationConnectorsConnection#user_password}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_key GoogleIntegrationConnectorsConnection#auth_key}
        '''
        if isinstance(user_password, dict):
            user_password = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword(**user_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9c6c7426675aaeb3e29c4ebbca800ee38355fedd16b228e05f86847148da84)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_type GoogleIntegrationConnectorsConnection#auth_type}
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_password(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword":
        '''user_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#user_password GoogleIntegrationConnectorsConnection#user_password}
        '''
        result = self._values.get("user_password")
        assert result is not None, "Required property 'user_password' is missing"
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword", result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable"]]], result)

    @builtins.property
    def auth_key(self) -> typing.Optional[builtins.str]:
        '''The type of authentication configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_key GoogleIntegrationConnectorsConnection#auth_key}
        '''
        result = self._values.get("auth_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable",
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
class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b474daf4bcfeee324b67ef180bc75508ed9a87250e1d53d60beb9bb1e47a8236)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "type": "type"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db53f7c6ecf8d06b8992b403fc81f5296cc6e5827c9a29cbfec629962f176cb2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f0088053452224f174f8b6169e2a1eec80c9430411d849a90ca7b51293a3485)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed5624233df690c2e5d158b1ee8be3e50d5de3ee1a1df0761ff62af612dfbc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7510dcdc54a34254b9df7449ae942719ae687ac1d3e8ebecd34d02c7a925f1e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938141e9b779a581a514bdc9c1b17b692dd377255f384298bbe809e3a4b0b7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06366101cf72174efdfc93884350a9f7b507bd497513ad1a2cc620691be684e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbae6dbba8438f0c37ace1c7f451796e591a20d9b351ba12a140b928416299be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa87bf33895d23c419984640c99a1e304e88c09a35877f451c011cc232d65d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cf6ec9ecdb49ee27ff6150985fa95d18d886361731b8c80684a7cebbb220777)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3dd927eb378152f7b9e88054eb5bccd51f814e0634e86091c5c39b935d342b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce62edd36cadca6990c9e7e2ec453c65920f04c315971c0f6a5a6120b64f5af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa8986f88a81170150c614a3df2990b29f8eb811373bc632b55635543cfb1f83)
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
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue(
            kms_key_name=kms_key_name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue(
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
    ) -> GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b41951160c0b1f2fa207f9579fff92a8ccf5568ebdcf1a461a23a69f4aae7cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13978ca99ecd33845da44a8be0bb73cfb0a50b292b7e457c76e8bb56361a95e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7283bf6a2871de6df2f55c67787a2bfe1409e096fb7b05f839978038769b6529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631b3da6255a4fe12b69b72d2a11445cc336b2e079d3dacbf7cc36b395cfa4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa48c820cacbf647abc19bb3f0e27efbed4306e687b340f21b66d8c78762134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca727823027acfe04bfcb5b4ced9034d40cd2ea8cbbd736777f0e4de44d89ff)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6977274293c2914736c1c4e0b0b79e7f5d7cca7b4547e10b9365601f55d07a92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1132bae1a0a4c3e852e5274cfaecd9c682d5c30f9ad6d73a0408ebf2c1c84600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860bf661691706c30d6e096da1c692d657ec7fe0af5532018d9c863c3411959e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a435d9ac3dd7aaf09e7702db67b7ecfb278fd0abab280e8b9448175503f6eec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccef8aa791e4a9ffde185c8d641027b53e752b111e5e52ce566b0922f8b039a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putUserPassword")
    def put_user_password(
        self,
        *,
        password: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#password GoogleIntegrationConnectorsConnection#password}
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword(
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
    ) -> GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList:
        return typing.cast(GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="userPassword")
    def user_password(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference", jsii.get(self, "userPassword"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword"], jsii.get(self, "userPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authKey")
    def auth_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authKey"))

    @auth_key.setter
    def auth_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c929923e30b926f666122bd3e6391b45bc9503b38713a85ee8641cc249fd44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5352058c3e844d74f682ffd309363d78a8c014556954e37bdcce8a77addd3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aeaa709ca1d8c26a7935426d7b811da0fed4f18013443341b362b77e5194f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword:
    def __init__(
        self,
        *,
        password: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#password GoogleIntegrationConnectorsConnection#password}
        :param username: Username for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        '''
        if isinstance(password, dict):
            password = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8ef587e461ae6d239e673e981ea8814b7ed76184822f71064b8217720cf7fc)
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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"]:
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#password GoogleIntegrationConnectorsConnection#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#username GoogleIntegrationConnectorsConnection#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1045ce85ba519a5ff21332040181756246476704af8a5a5172961287d0bab807)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPassword")
    def put_password(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword(
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
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword"], jsii.get(self, "passwordInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__70c2c15dc007038d28bd5c3bf87e6e5bcb34cb5312827736174e9bc87254b27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db002f2c68278dff1d72bfc161f855fceb2f6e933bd8620ab7fee83aaca576a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a383743cece1b679382cb5a727121224227c445d655dc851109f5295cb8d28)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}

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
        return "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aa35ad6a837e1adedcc7dc5367156e80ffeca64daebacb585abe58dad12a2e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7f4a8dedf038860222dd8ade3c2d175ff24cac6926647ec2c053a55495cb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81dc9f61e8c5ecb54107f6595365a1df458d4909ea5215876f98df0eb3039d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a910bfa32a7c120b1ccf90db69285f5c08958947bd604aa8a55b3eaf0fcfd831)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deb28e3375bc9a06cf0570373b56c67c556fc8711fb6d057e0cd89bbd650cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        *,
        auth_type: builtins.str,
        user_password: typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword, typing.Dict[builtins.str, typing.Any]],
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_type: authType of the Connection Possible values: ["USER_PASSWORD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_type GoogleIntegrationConnectorsConnection#auth_type}
        :param user_password: user_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#user_password GoogleIntegrationConnectorsConnection#user_password}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param auth_key: The type of authentication configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#auth_key GoogleIntegrationConnectorsConnection#auth_key}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig(
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
        destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination GoogleIntegrationConnectorsConnection#destination}
        :param key: Key for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        value = GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig(
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
    ) -> GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableList:
        return typing.cast(GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="authConfig")
    def auth_config(
        self,
    ) -> GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference, jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="registrationDestinationConfig")
    def registration_destination_config(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference", jsii.get(self, "registrationDestinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig], jsii.get(self, "authConfigInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig"], jsii.get(self, "registrationDestinationConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5975b9a1f85826f91f021811272818ece82b89160a7e76ebe929ec9e27baea76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enrichmentEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63ee403cd604fa4278e5a73d77be432a438e1d0f3e78bca1271bdc70c756d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "key": "key"},
)
class GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig:
    def __init__(
        self,
        *,
        destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination GoogleIntegrationConnectorsConnection#destination}
        :param key: Key for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872fb709e653825be4e623c802cb345d32cfe267ff8060d423ceca32906dc997)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination"]]]:
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#destination GoogleIntegrationConnectorsConnection#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination"]]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key for the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "service_attachment": "serviceAttachment",
    },
)
class GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_attachment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#host GoogleIntegrationConnectorsConnection#host}
        :param port: port number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#port GoogleIntegrationConnectorsConnection#port}
        :param service_attachment: Service Attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_attachment GoogleIntegrationConnectorsConnection#service_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d1530fad6a7e0ff510983fa053fa1f9538d784aa58e323cb23fbf6e220dc5c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#host GoogleIntegrationConnectorsConnection#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''port number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#port GoogleIntegrationConnectorsConnection#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_attachment(self) -> typing.Optional[builtins.str]:
        '''Service Attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#service_attachment GoogleIntegrationConnectorsConnection#service_attachment}
        '''
        result = self._values.get("service_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d8ec93df02a5a279eb8b54ab81be0f6dd1e9811946ada5597a39f1f05c336f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ce878aead28208ae3b1afd2d1db9938bc2deb4fc84982bc0ec80de6021ddda)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9807cfb91a8c63dcaf6d4cf2d7518e8aab0b9df237c99a086458bbac2cac476)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7153c4b5f98e9af85d95b40d42de942d829f784748a6808202990466652c4b42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__020737d5b855c9dbb429b0065d8cf0554322cb340a6793aad412084fb743308a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c588fed34cd10ad051a656b92edecc122e07c6c48d0ee362bbbac4bc367d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__711fa75148dea414f250f4dcab2f7e6e455adf18966d6463914c268073c90009)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10dd63870ee74e133302de811dac2a7ac8e4bd66f4af679e25b4362de416e003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff935ec53df77519be6db32cbe9d9d3d54121a4f78a311505792bb57c6391982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @service_attachment.setter
    def service_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779933ff4d98d4abf824395f7f08f31fcbf094003c31b119cb9db5cf71f724c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2310e455038c803f7935adcd1718a13ce297ba47f31f1d5b966d5050a092a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c17067378f626ce0ec96ca039a5929869e081e7fe5cd78bb634b45032fe39fee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728107577b108b65c60d21fa148ae342b70926b2d3c457e30c40ee0c5394a305)
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
    ) -> GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList:
        return typing.cast(GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]], jsii.get(self, "destinationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e4fe4a03ca3224e4fe895fc7dab5165600cd7890d875e80fe87a321746f4c602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a82b6ee8b8993fe97df25bd0428487406d6e947b160c64fc557ba9989dffe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingRuntimeData",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIntegrationConnectorsConnectionEventingRuntimeData:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingRuntimeData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingRuntimeDataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingRuntimeDataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d87e0b019f88d3a98544e76372befee87668c69f1e1b1a152eaf16698664521)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionEventingRuntimeDataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16b8de417c27eb47de4708ae55e9ada78c4fbc585913f82e5ceb3ed3f2fe0c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingRuntimeDataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2315acdecf2e9d5d87cbf691d5563d5434808992c65d799e865151c94b7e0095)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59762a2f656816a2f7eddd044410334409e0e7d3d58151ef9039a20ce98d13bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32ef68aaa25d89a46193e771d94e19e7d75d8a25080355bc65c06a46b11af988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingRuntimeDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingRuntimeDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb29a8e76deaf9e46d754beb8cf0c4602aa3b1b6323179617ed86b3255382a01)
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
    def status(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusList":
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeData]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00509d34093c6541551749cf03f9e382b730238d44a6b26b2a95f2de63dbec63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a6e677b97cb8ee27dfe493a8b9b0492759b324b7a3cfd1b5ca43a1496373f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a504b6f315a678387753860acb1b483e7a214d9ae5b1ac635eda581190ad0c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960f842877d22ea23375324fcff3784360a748e0743d431a960d3ba3ff93ef7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bed70c48ce19565df8c7e4a9dcf266ad723a9ca6fe1c8c007e2397a0fe1d956)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92734a5993f0813e597bbd0f500046d6621ef09bf49d49ef6d91052ec4bf4861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22f7fd1faafe394d37bcb41296b02d40acbdb91a3b025aa471202642dd4f44ae)
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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5e2fa7326cf6763e942fb87b4aabf9fab9bac83e0086a1dcf6af51ca8ccb8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionLockConfig",
    jsii_struct_bases=[],
    name_mapping={"locked": "locked", "reason": "reason"},
)
class GoogleIntegrationConnectorsConnectionLockConfig:
    def __init__(
        self,
        *,
        locked: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param locked: Indicates whether or not the connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#locked GoogleIntegrationConnectorsConnection#locked}
        :param reason: Describes why a connection is locked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#reason GoogleIntegrationConnectorsConnection#reason}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d4e23b4fbd96d04999cc28c29eb0af455dc5c70514f2e437e16afa6453cf1c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#locked GoogleIntegrationConnectorsConnection#locked}
        '''
        result = self._values.get("locked")
        assert result is not None, "Required property 'locked' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def reason(self) -> typing.Optional[builtins.str]:
        '''Describes why a connection is locked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#reason GoogleIntegrationConnectorsConnection#reason}
        '''
        result = self._values.get("reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionLockConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionLockConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionLockConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed7d268397f37b04f295852a3dce4cb36ee9acc5291b6a2e86e66d842ec38f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__108acabf4335f656f54fc2ed9ac73209be3a0ffaa3431b3df1da3b2aa13a594c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @reason.setter
    def reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa1c5fa9963ba5be26c813288387a628652ff0e9bc75508ab04f54ff270c122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionLockConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionLockConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionLockConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4988cc997d0fc85be6ebd544b976a26cf2662f3029b6d05dfec4ea6836fc3150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleIntegrationConnectorsConnectionLogConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enabled represents whether logging is enabled or not for a connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enabled GoogleIntegrationConnectorsConnection#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4f9cb809ddf067c75ca41e1955b3a1b154b2a0d1936eee339abf11fab06105)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enabled represents whether logging is enabled or not for a connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#enabled GoogleIntegrationConnectorsConnection#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bd2c51911e47d9fe7d767c28e8114f0e8f0e56dc1fc3df1657261d4955407fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5dbc5384d9a6c63a3c21ef83108f237733fe249d412c09fc354a488f5d5c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionLogConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6c770da343af1cb0e34b4c5931b6a76b88afdf0ade0ec4c71a4d621dfac3ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class GoogleIntegrationConnectorsConnectionNodeConfig:
    def __init__(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#max_node_count GoogleIntegrationConnectorsConnection#max_node_count}
        :param min_node_count: Minimum number of nodes in the runtime nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#min_node_count GoogleIntegrationConnectorsConnection#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afb22892c95577b853c5d3c635236a00fe467363254f1913f71571c22518e82)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#max_node_count GoogleIntegrationConnectorsConnection#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of nodes in the runtime nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#min_node_count GoogleIntegrationConnectorsConnection#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d7da18d431a438ced37eb767d34f341d2f407b016a27a3bed1c3917215eee8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aeb2379ae67e91cf9fdcc7802bad40c59248b2dae1a2c7db1026e37a5e7d4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c463e32741832f6758dc6d950ef2717d4c156b4a21a4656e1f5b3cacdc337d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionNodeConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa817851136529b736ea0c7fd452c4fae04f73ab84a570967cccdf6783c4687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfig",
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
class GoogleIntegrationConnectorsConnectionSslConfig:
    def __init__(
        self,
        *,
        type: builtins.str,
        additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        client_certificate: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigClientCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        client_cert_type: typing.Optional[builtins.str] = None,
        client_private_key: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey", typing.Dict[builtins.str, typing.Any]]] = None,
        client_private_key_pass: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass", typing.Dict[builtins.str, typing.Any]]] = None,
        private_server_certificate: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        server_cert_type: typing.Optional[builtins.str] = None,
        trust_model: typing.Optional[builtins.str] = None,
        use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: Enum for controlling the SSL Type (TLS/MTLS) Possible values: ["TLS", "MTLS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        :param additional_variable: additional_variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        :param client_certificate: client_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_certificate GoogleIntegrationConnectorsConnection#client_certificate}
        :param client_cert_type: Type of Client Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_cert_type GoogleIntegrationConnectorsConnection#client_cert_type}
        :param client_private_key: client_private_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_private_key GoogleIntegrationConnectorsConnection#client_private_key}
        :param client_private_key_pass: client_private_key_pass block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_private_key_pass GoogleIntegrationConnectorsConnection#client_private_key_pass}
        :param private_server_certificate: private_server_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#private_server_certificate GoogleIntegrationConnectorsConnection#private_server_certificate}
        :param server_cert_type: Type of Server Cert (PEM/JKS/.. etc.) Possible values: ["PEM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#server_cert_type GoogleIntegrationConnectorsConnection#server_cert_type}
        :param trust_model: Enum for Trust Model Possible values: ["PUBLIC", "PRIVATE", "INSECURE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#trust_model GoogleIntegrationConnectorsConnection#trust_model}
        :param use_ssl: Bool for enabling SSL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#use_ssl GoogleIntegrationConnectorsConnection#use_ssl}
        '''
        if isinstance(client_certificate, dict):
            client_certificate = GoogleIntegrationConnectorsConnectionSslConfigClientCertificate(**client_certificate)
        if isinstance(client_private_key, dict):
            client_private_key = GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey(**client_private_key)
        if isinstance(client_private_key_pass, dict):
            client_private_key_pass = GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass(**client_private_key_pass)
        if isinstance(private_server_certificate, dict):
            private_server_certificate = GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate(**private_server_certificate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88073145527602431423adf81af858d385ef46376a5aec85d13f730b0e9b6a9e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable"]]]:
        '''additional_variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#additional_variable GoogleIntegrationConnectorsConnection#additional_variable}
        '''
        result = self._values.get("additional_variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable"]]], result)

    @builtins.property
    def client_certificate(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigClientCertificate"]:
        '''client_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_certificate GoogleIntegrationConnectorsConnection#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigClientCertificate"], result)

    @builtins.property
    def client_cert_type(self) -> typing.Optional[builtins.str]:
        '''Type of Client Cert (PEM/JKS/.. etc.) Possible values: ["PEM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_cert_type GoogleIntegrationConnectorsConnection#client_cert_type}
        '''
        result = self._values.get("client_cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_private_key(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey"]:
        '''client_private_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_private_key GoogleIntegrationConnectorsConnection#client_private_key}
        '''
        result = self._values.get("client_private_key")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey"], result)

    @builtins.property
    def client_private_key_pass(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass"]:
        '''client_private_key_pass block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#client_private_key_pass GoogleIntegrationConnectorsConnection#client_private_key_pass}
        '''
        result = self._values.get("client_private_key_pass")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass"], result)

    @builtins.property
    def private_server_certificate(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate"]:
        '''private_server_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#private_server_certificate GoogleIntegrationConnectorsConnection#private_server_certificate}
        '''
        result = self._values.get("private_server_certificate")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate"], result)

    @builtins.property
    def server_cert_type(self) -> typing.Optional[builtins.str]:
        '''Type of Server Cert (PEM/JKS/.. etc.) Possible values: ["PEM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#server_cert_type GoogleIntegrationConnectorsConnection#server_cert_type}
        '''
        result = self._values.get("server_cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trust_model(self) -> typing.Optional[builtins.str]:
        '''Enum for Trust Model Possible values: ["PUBLIC", "PRIVATE", "INSECURE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#trust_model GoogleIntegrationConnectorsConnection#trust_model}
        '''
        result = self._values.get("trust_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Bool for enabling SSL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#use_ssl GoogleIntegrationConnectorsConnection#use_ssl}
        '''
        result = self._values.get("use_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable",
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
class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable:
    def __init__(
        self,
        *,
        key: builtins.str,
        boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_value: typing.Optional[jsii.Number] = None,
        secret_value: typing.Optional[typing.Union["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue", typing.Dict[builtins.str, typing.Any]]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Key for the configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        :param boolean_value: Boolean Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        :param encryption_key_value: encryption_key_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        :param integer_value: Integer Value of configVariable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        :param secret_value: secret_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        :param string_value: String Value of configVariabley. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        if isinstance(encryption_key_value, dict):
            encryption_key_value = GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue(**encryption_key_value)
        if isinstance(secret_value, dict):
            secret_value = GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue(**secret_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b080f47f7f1bc20574e9dee85a870f92317830b0a0959653660c7d59c7690404)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#key GoogleIntegrationConnectorsConnection#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boolean_value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#boolean_value GoogleIntegrationConnectorsConnection#boolean_value}
        '''
        result = self._values.get("boolean_value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue"]:
        '''encryption_key_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#encryption_key_value GoogleIntegrationConnectorsConnection#encryption_key_value}
        '''
        result = self._values.get("encryption_key_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue"], result)

    @builtins.property
    def integer_value(self) -> typing.Optional[jsii.Number]:
        '''Integer Value of configVariable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#integer_value GoogleIntegrationConnectorsConnection#integer_value}
        '''
        result = self._values.get("integer_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret_value(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"]:
        '''secret_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_value GoogleIntegrationConnectorsConnection#secret_value}
        '''
        result = self._values.get("secret_value")
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''String Value of configVariabley.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#string_value GoogleIntegrationConnectorsConnection#string_value}
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName", "type": "type"},
)
class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7b0c4e45d4cd41e31d297cc33723c7cc442298e6846342f1bc2564df185280)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd453c8e0a747164ff9f99f045dfb6f20958521b068bca46ba431517fd1a64dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__813eb2727df3882007c37c228b2557b242a12856cdf73eb87b731b61ec5553c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69c55130108f67655ab1b1d5cae73907bcaa3409ee5b76f54ce27d00d4120ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd063306ab990780887a1953b53a54f57d497d728eac77a61352c5de926d2a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca8c5a1b5a7e3c621b01949a3868981c5b315929546388ca56a7afaf1d22d00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd49924f2d5ddfcb8c999896a267dba2c3007c60b2548794756438c9462f9b8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf017f0408cf6ea9cdd36b0b498d5b47eb55245b139dc463d5f5c9f0815d9db9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62fb525a989649268f8bdf0f6cd215a6fffeac9b5b4f5e5d1b72833a16d250fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f23c5a6072b430b1f38f3e5d01798913ea2e00b39cba5c574212e7f180a031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ee9b56eea79aa168b6b5a2e68ce7e6c44c4ca3ea74863c493765c5a0887681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2255f3b702345672df81dc439c394b6395e0d5187d3cb3c3426eca41dcadeb36)
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
        :param kms_key_name: The [KMS key name] with which the content of the Operation is encrypted. The expected format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Will be empty string if google managed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#kms_key_name GoogleIntegrationConnectorsConnection#kms_key_name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param type: Type of Encryption Key Possible values: ["GOOGLE_MANAGED", "CUSTOMER_MANAGED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#type GoogleIntegrationConnectorsConnection#type}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue(
            kms_key_name=kms_key_name, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKeyValue", [value]))

    @jsii.member(jsii_name="putSecretValue")
    def put_secret_value(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue(
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
    ) -> GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference, jsii.get(self, "encryptionKeyValue"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference", jsii.get(self, "secretValue"))

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
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue], jsii.get(self, "encryptionKeyValueInput"))

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
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue"], jsii.get(self, "secretValueInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__182ee9afcee5f23f99fb6b1b17b94c3364cb7b4008abccda7309fb8c9cb22d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "booleanValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integerValue")
    def integer_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integerValue"))

    @integer_value.setter
    def integer_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d608472ba68174769a7a2056ae00810c40d9d593977aa95d386a34f30ab8cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431157508b34e42ab6fe23dd25dc4d920d2e1c77a466dd23d79f2b89d4ba0f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14abcfe040dc92834c93e2e450e0034dea0bcc987c5caf6b3043388d25d6336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5f00bd39eb7f5c616af9a4a8e68844bccd77d12ed93256c7cc385ec17b7a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a91d587eec1842e8459bb49a0d3ce4c7f5df37cc2bab29d195a9352dc43f77f)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0589f76656346bd37ee3cc8eb3af588f5b81fb0bc84d438294f59de455fab3a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4649c09eb4a7a4ac19d85134ff6b32a924360e7fbb318546108083001a29353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671da39f3f891991cab2506bbf380355dd9e2f0aebf148d7c3a9182efe92fbd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigClientCertificate",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionSslConfigClientCertificate:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93613594ab5a3c56278988e6f8387002184ef527210daa8b64ccfcbb233e966)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigClientCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionSslConfigClientCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigClientCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8febc21fbf1412fe14f2a16b51fb6ed628b151af0ba8d01b6e778b96560f5057)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d7f8f03e0f08e195e8ee57f317ca0996ac8476697577f31c99dfcab6813293a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71bee84d22f1b5b1442b9bee43c8bb2ec314c639516c9d0bdc86159a8ec7d5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82074909f074e96dfc4c31c8b8435e7e4c8d9d8d813e3599d4999bd4b4b02c70)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e7a7dec8462d5a829376dbd951ebbad1492932ad133655aff4f9ab8036318e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e68fa560ab184f0222be55eb3d7a3c6a66e682809f094eb6180ba95d8535b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c450e14ee52df6fd6469d31340a5dec80a0803bce94384064b90f4a14ac00ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f174b07e703c7f8487d2dd379b7ca6664ad836661074ef09db5396dcfa1bc36b)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1bf7bfbb750304eeb4bfa5ddc7a767db43e3744e86cc6b5ef88cc0d49fb0d26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fede34b5b4e6c81f77ebd44aaef9462e442d8b97a44a3c160fa21a7ef0b1fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52329b896e7db056c6829466b9f1f5d117cef89d617235633b85c34540a0425d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionSslConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99a72b80365ca66b11ff133d4fa8591bac00565a51c25239b86b6d15726a044e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalVariable")
    def put_additional_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7b9713d0a84c263664f118451bb04dea4ccfc5c63ad2eea906629ce1bf5ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalVariable", [value]))

    @jsii.member(jsii_name="putClientCertificate")
    def put_client_certificate(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfigClientCertificate(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientCertificate", [value]))

    @jsii.member(jsii_name="putClientPrivateKey")
    def put_client_private_key(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientPrivateKey", [value]))

    @jsii.member(jsii_name="putClientPrivateKeyPass")
    def put_client_private_key_pass(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientPrivateKeyPass", [value]))

    @jsii.member(jsii_name="putPrivateServerCertificate")
    def put_private_server_certificate(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        value = GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate(
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
    ) -> GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableList:
        return typing.cast(GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableList, jsii.get(self, "additionalVariable"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(
        self,
    ) -> GoogleIntegrationConnectorsConnectionSslConfigClientCertificateOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionSslConfigClientCertificateOutputReference, jsii.get(self, "clientCertificate"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKey")
    def client_private_key(
        self,
    ) -> GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference, jsii.get(self, "clientPrivateKey"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKeyPass")
    def client_private_key_pass(
        self,
    ) -> GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference:
        return typing.cast(GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference, jsii.get(self, "clientPrivateKeyPass"))

    @builtins.property
    @jsii.member(jsii_name="privateServerCertificate")
    def private_server_certificate(
        self,
    ) -> "GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference":
        return typing.cast("GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference", jsii.get(self, "privateServerCertificate"))

    @builtins.property
    @jsii.member(jsii_name="additionalVariableInput")
    def additional_variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]], jsii.get(self, "additionalVariableInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertTypeInput")
    def client_cert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKeyInput")
    def client_private_key_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey], jsii.get(self, "clientPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientPrivateKeyPassInput")
    def client_private_key_pass_input(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass], jsii.get(self, "clientPrivateKeyPassInput"))

    @builtins.property
    @jsii.member(jsii_name="privateServerCertificateInput")
    def private_server_certificate_input(
        self,
    ) -> typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate"]:
        return typing.cast(typing.Optional["GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate"], jsii.get(self, "privateServerCertificateInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b29f8503f3b5a8c05195ae0d52861481db5ff418924553e92b1ed00a164dec86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCertType")
    def server_cert_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCertType"))

    @server_cert_type.setter
    def server_cert_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4575c86332578d5b49bd8936c05f0f82fc40aaafd6cf94357e3da967aa7a8fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustModel")
    def trust_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustModel"))

    @trust_model.setter
    def trust_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240f7c5007c32d3b796bd6d05244b7ca607c18544451e7086c51159c568b76aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034ed1472bff0ecab8d7f2415462de2d054c9699216287d16ade5f87ce6fc39c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9724141d1bbab6d13e4271167cfcad2efc9fc752d691959fac549c1bef9b1789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfig]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aaf2c19a0b21d6c45c602cfef181ac9efd9a21ae9df73019f346bf0a8e1e5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: Secret version of Secret Value for Config variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe7f58cbc3a71d569ac1617bbc384cfd91f4c3ee30810fd162ba8520bd7336e)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''Secret version of Secret Value for Config variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#secret_version GoogleIntegrationConnectorsConnection#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4de8918ab8dd6977ac5d77138800d577f8100523e58fd7ed62083ae18ecf18ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dcfe685bbb982dc7ceeeff988bcc8d49ceec336f6185ef432df41d37bdaa26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0206e335bd57838ec0975d079c529a1efbe83fab184c241b9d46786aa2c88fee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIntegrationConnectorsConnectionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8944378adc175a90dd7fefd1862016344072696ad6ca16289062cfcd50457042)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIntegrationConnectorsConnectionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dac355565f3894ebff752f70bc938d1b50e339e5cefeea9fd9cd847d1eee132)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIntegrationConnectorsConnectionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307520d189b98548e660106ddb143742fc6d278a44a63405aae6e757f5604b96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd1cf5d3652be9fdaaee8eca1bdba1d1c1d5f4a9fb57f1efc280a6c2bd8a48a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40f0fcbf74a972bf99e272854c703c85cf5d0ea64c2cb82734f2d0fdab398dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleIntegrationConnectorsConnectionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcb04cb5f456410b9da82ecc1eb8db086a1d72343b768b58fd2193f7900e4c52)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIntegrationConnectorsConnectionStatus]:
        return typing.cast(typing.Optional[GoogleIntegrationConnectorsConnectionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIntegrationConnectorsConnectionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb04283b4bc0b65d1b7388c34a266bf22a434b69ec37fe7d17b38090c44cf2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIntegrationConnectorsConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#create GoogleIntegrationConnectorsConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#delete GoogleIntegrationConnectorsConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#update GoogleIntegrationConnectorsConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eaf27154e3d64f853eb3f580a52ec56afedaa4d43c6cbc64e487e00d17a14c1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#create GoogleIntegrationConnectorsConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#delete GoogleIntegrationConnectorsConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_integration_connectors_connection#update GoogleIntegrationConnectorsConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIntegrationConnectorsConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIntegrationConnectorsConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIntegrationConnectorsConnection.GoogleIntegrationConnectorsConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0465b696c6f3b665da83d8f5be97bfcef6fd4f1798202e278b2b72e7ab4e4d39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2e291d55359fbd50562abfe2c4e12d045ae6ecee32dbdd2764d3494da54aad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f193ca04ea8adec1a480f443da58224700b70850d2d827d75a456b3ed3fa3e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f90b8d19e8e8bda0524cd2069d2c702d183d1ee4a841e364d63cefb3700489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67a7fd7794008ca0c29595d609a07996d2fdd7a2fb5583cf6b678bb3dc5f6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleIntegrationConnectorsConnection",
    "GoogleIntegrationConnectorsConnectionAuthConfig",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableList",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue",
    "GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValueOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecretOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecretOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKeyOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaimsOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey",
    "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeyOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert",
    "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass",
    "GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPassOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigUserPassword",
    "GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordOutputReference",
    "GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword",
    "GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPasswordOutputReference",
    "GoogleIntegrationConnectorsConnectionConfig",
    "GoogleIntegrationConnectorsConnectionConfigVariable",
    "GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue",
    "GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValueOutputReference",
    "GoogleIntegrationConnectorsConnectionConfigVariableList",
    "GoogleIntegrationConnectorsConnectionConfigVariableOutputReference",
    "GoogleIntegrationConnectorsConnectionConfigVariableSecretValue",
    "GoogleIntegrationConnectorsConnectionConfigVariableSecretValueOutputReference",
    "GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig",
    "GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigList",
    "GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionDestinationConfig",
    "GoogleIntegrationConnectorsConnectionDestinationConfigDestination",
    "GoogleIntegrationConnectorsConnectionDestinationConfigDestinationList",
    "GoogleIntegrationConnectorsConnectionDestinationConfigDestinationOutputReference",
    "GoogleIntegrationConnectorsConnectionDestinationConfigList",
    "GoogleIntegrationConnectorsConnectionDestinationConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfig",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableList",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue",
    "GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValueOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableList",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValueOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword",
    "GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPasswordOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig",
    "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination",
    "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationList",
    "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestinationOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingRuntimeData",
    "GoogleIntegrationConnectorsConnectionEventingRuntimeDataList",
    "GoogleIntegrationConnectorsConnectionEventingRuntimeDataOutputReference",
    "GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus",
    "GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusList",
    "GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatusOutputReference",
    "GoogleIntegrationConnectorsConnectionLockConfig",
    "GoogleIntegrationConnectorsConnectionLockConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionLogConfig",
    "GoogleIntegrationConnectorsConnectionLogConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionNodeConfig",
    "GoogleIntegrationConnectorsConnectionNodeConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfig",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValueOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableList",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue",
    "GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValueOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigClientCertificate",
    "GoogleIntegrationConnectorsConnectionSslConfigClientCertificateOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey",
    "GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass",
    "GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPassOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigOutputReference",
    "GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate",
    "GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificateOutputReference",
    "GoogleIntegrationConnectorsConnectionStatus",
    "GoogleIntegrationConnectorsConnectionStatusList",
    "GoogleIntegrationConnectorsConnectionStatusOutputReference",
    "GoogleIntegrationConnectorsConnectionTimeouts",
    "GoogleIntegrationConnectorsConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ed3846c11b0728e49d19a9fe4b0c09d71b7c755209781db53f91dd5ba27e619d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connector_version: builtins.str,
    location: builtins.str,
    name: builtins.str,
    auth_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionConfigVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionDestinationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    eventing_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    eventing_enablement_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lock_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionLockConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    ssl_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e92e27dd8b512a3c3c9a87b36d859be7e18db83d01cffc0451fad277eeb4e962(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c01ab1751a35eb9e83fba1e59f511472ee97a14bc0311a9aa654b42637b4694(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionConfigVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee966f3960c7d234d87c4d243da63ced2918fc4d3cfbdfc72a6c84df1678a8ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionDestinationConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01fb223abbc8d598528d9f8fdbbdbfb1b0d5147af5fa71f64846d9892e588a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967b26b00f8d47e755b2ac42b689f6585c96b3d31eb8435374d276754c7f9870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d89434b5b586d501ee413944ef519eaff232a908783055309ec1e9e3fe02e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2274b71a80efcf35aff696e147b61b8df7b6a79470e4a0e62d846ec7407b6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9003a9012d7d68a08ce54c6a270d648a5f1617d2305210676d27fa6fbc7e32(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa45363279e1bd5e3832a1682af00fdb7000a2b27a0dd39d7dc11b957b8a605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb804713bed2b786770f922c4887ada3fcfe4b373fb9dcd1c50250054aa99b78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969cfbac133ca15acc0b2aebff6592f1718a034f1596e0bd528e0a9a2c75ad2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470e3d0026e3b4ec3fc7ca5e726c68801ea555086e65f5a1ab3bccfe75c80720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acfe87518a0178b935df7eea7f8de8f2181ffd6f4d48c8acc83fe15eaae5df3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c80dda8c91f8e95ff493b48d147e78a8e4706740426c282adfdd1975eb4e9e2(
    *,
    auth_type: builtins.str,
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_key: typing.Optional[builtins.str] = None,
    oauth2_auth_code_flow: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_client_credentials: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_jwt_bearer: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_public_key: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey, typing.Dict[builtins.str, typing.Any]]] = None,
    user_password: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigUserPassword, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244aacb073e53ed4089f9ffb376d0a60eae8dd2b159cf5ab4d34a34a63345bea(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9c74e3e6848da09a4f3e6ec0f6b9cad7cad231434230207cc06b690b153215(
    *,
    type: builtins.str,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0365003c5e2ea3c1b94c4371312831c0703a0217b8bd09356ec4781f46229e3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87a3b2afab80f93eb42c29c020b0eeda9537e0baf06cbfaf6c4563e4e41387d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a128ffcb8db3e6a748529afb3d149c6fb4ee3b2fe088574e75e8705cd75ea47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af00146a6d0ef98b5ef9e6f9bf5da371a3d504131db565c2e4a68b799ec08d8(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd28ae52ffd5d234732e97d61ab6bead92556b6026ae44b901f6fcb59b80f48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66aa0bfe9754616094e0ee8a6d8db9ee898d01ea33f23dc774a6f31bb06c76f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45e6fd96ad3f47f366fa559979c80f533e5125d99cfc662f9152cd48bec4b85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9ab960beca42b6dd6838c40a5d0aefaf1b635ba32cdd335ea399f693fb6542(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baebaefeeefce2c769c6c0c92b6f01369a8b81a46e544a952ab5c5ebb135665(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb67b8f06dd3b1a02abaeb1f665f5915ed0121785430687d0fa4c2a5cb4df55f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df540d63422bceb701e73dc8b413e35951cb80342872c16c18ef045e029d6a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2433d8f8ba7129820417d33298f7751eb6aedce4fc1b5eda57b47416e8bf92dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2284c868faaa8014a2fb39c18d211fcc46184a823bfbe25294b8e23b6f459fb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44040db9456725894f91d2051dd8bce5c5c5a5208346c02abc2ad871a0d001c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb940bdb1797152631ed9e2be923db5d5841cab1df56973321933f43868cfa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af67614cc3ecb866d8e51e585148fd30c15895c730add9e94d46d3df90d5646a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e028a64a21b0310c6caa1d720864bfa084ff1964f10647c68c2d8c1fd51d6de(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52eb4b6d2d2ec11d33d6a0a62980cf9207cfa6826674927411bc0abedd151a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383e1f7a21de2bdaf0770ea9ddb482029f088db6099cce36ca0c5a670fd030e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6ea31518181d1529ac7fec5f4f28f1ced6b5a5192a9893352589e440792dd1(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1135aed472915a69ddb4fed52c058ddb3378f8d108966d69194495b8dffa1dbe(
    *,
    auth_uri: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_pkce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cdb57c1c62cdf2d5f33641750ae01b74b6f6cfab9064c795a59de09d7688f2(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7d86988350de854a9512dd478b08836d0ce6a42aff9d7e3ceeabb98acee025(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b16dca7b685b542536bb6e982634b1988f589b7187461e514e7d2f603036c97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5f366f6d811738fd59d050c2ea5bdb85c3e5469f951b800bcecd4e0cd3d898(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlowClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fa35792e3cb68c04619fe966d033b00cb43476d0106f1ad45e085489152a2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a92b091bb84e0d3020946015d8679474ee0c953c40a6133e74c821537f1b9fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8ec8a508ae2b878bca6348f58a052c059d657196f1e58e9733f816da23a7bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7381efd9ead774ab865c42bf3e2fadaff6f0afffda394748291d29972496bd25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2abf1d6c8dbf1e9db11419100664c816e9c3ed274a7824e7c25fd4e7a93ad8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e20195114374b758152c78d3ce65bb32aeff04b029f0afb1a214ee30d45a06(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2AuthCodeFlow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b9804cb887b58788d7d3a8afe9063834030727d1419704053d93bc9b67d38a(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d69f7400e9237bc84502154731aaac008479c79df56749894c45bf05142d91e(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7934052aeee45db5df26f50fce8f8cea404d3d1551eb38fa1edebd9122be5380(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351ea48d679f9514b0e543eb2765a98b6eb70c59b1be74356cff0ee1794126a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bd9cd240fa651b6135416b93d71a68f9816cbab8dd9b2bdcb44b366d5f2094(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentialsClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4085222c240748d2ce76cc28477a2dc4ca1317af426c80243e997e832fa27efe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668024fa531aab97bc84ee12d0200c5c4ccfd80258781c032df6acfe65217ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dd569cfb7f8c7ebb4bbce134657d68caa03bd79aa50aca687870ac95f8bc53(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2ClientCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867d3e5058f6988ebe3014056d1df51c7086f75fb952561cb4c875dd3634e4b9(
    *,
    client_key: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey, typing.Dict[builtins.str, typing.Any]]] = None,
    jwt_claims: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439ef09587073eb7ba79b0381b091fe3e4ce78c52b37402be87e91be1a979236(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6465364fc607ddcc15b62786482a949cfc4f1fa0fd429991d3bd8602e1222f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7b92896effb570688fcdb2b814e276069052ed3ae32a0e549592c01cfe1f81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5e4eaef4dd47dcbd532d4b5ebd916337c65a888ad00826e03062a16d6f359d(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerClientKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c497fac4fc9d3bbb3f65be10c2b9c47de53b5df2d72ba362f2d9088820aa267a(
    *,
    audience: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8921961ac23b70c359b6d18d4bcd16290ceafc0fa69720eecd52c58a729547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ae8eda786379cf461f762369f5cac2ea5e3a79a2355b19537892ee2a98fe75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc351571b00c45373d513e345742164ca5ac9dc397200ac049c4233531a9efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7a7a8b1ce67737b71dc28a4a0a9d38bd159b2e63130c43418896473c05818f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5696ccb3fc26763fc1d7e858150ff060fab646880b0132305bc751691601d4(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearerJwtClaims],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba868470dd758296817f4611c526db2032c1d8fb529577f2050cdaf59ede5d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6587da0100b671fb3391572e31fe74c001adb202c4e969896fba5205c209fd2(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigOauth2JwtBearer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbddc38487defdb2ced6129c49c9bd7ff3782ae49c3d5650b2130698116a5d2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494c79eeb78cc97a210503e98eea5f1bc9d4a6d23a14bca192c1b7e0a61f4765(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62e44927776b5666915c89d05fc2353851e42de6b8c1bbb2b2c3055511f1c86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3538206f1effdf9af92f1f8fd3941be891666a1a69583eeab55bbe467d0e5f1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e828df8af6739b9a5c76e8e4101f055eeeccfff70d484712bbfbb945e5d907e(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902d5dc5d9d27737cbb80faa91a5784953a6a69bf4468761ca27f9bf0fc4c925(
    *,
    username: builtins.str,
    cert_type: typing.Optional[builtins.str] = None,
    ssh_client_cert: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_client_cert_pass: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d7be3be5c5bbc8911ce2212202ede204287ae53a0be964e5b28b7b2daaae42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb21bec1e861518f4073211b1fb6d79b8a30096b0137f782fb222cf5e9b1fcf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820db1dfe025bd03555e9ee69aa336153a4386f3ab2cb50dcc74ee0319fcfdb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ee11aa161c322a5ee6bea70a5a74b40812c8ed5f5ed80fb88dea80e5f01a64(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc21172183de2a1c99d90c290b8db8754c6b4406949d3d829dc91fa2f0baf0a(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b25c405f59c5245549e0443d67d0135b90971ab9b01af8b29672c99d96b254(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ab5185390aefb014320e6dd5c7238e2f8d757fe335a2ab93b0a1ce359f1391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631ac18c489a52113704908aee7a0c66e8f892cb421029a261cbd8c4a04a5dc1(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c6cee8f9826d221a9374f79f8625b777daf81ca23272dc0906591e0c9cb664(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32558227a00bd009a93650ebebe2d5f79ae11d63f7d43d33deb30b6b2b88f087(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ee33b363438bc05c0733307e7ee613213c2929373a9e1fc14956b2283d2705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a333efad38e0b614560015cb11ebe1f2ae7725336b629a27550b586e1cea2d27(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigSshPublicKeySshClientCertPass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66eb6f3527aa66f301f6cc17892f5f531741c18d84fbad8a33364b055aa62fa2(
    *,
    username: builtins.str,
    password: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6a91b803bad5e02664c7030ebbd3ed3f6b508bcf47c889f30b5cf27ee47018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633f4df6846162f9c9da79f99c13491c556ead98c6ce668aae59b0a36cb7a23a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ebd1e2d79bedccfc23b625e6dba4c9340d6e7564f20023d5fb158a844a315a(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b64e7c5678ead8b1c72eebff3a49c7c08efc0ffbfa1cde3997f47724619d81a(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a954c356e583b0eb66b620e9dc7caffd0719a54d11528385ead605a6ab5e627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d288456f48603aab838f02c18b81fec30c4101c8a87f3f83dbb8bf6c0201a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b4d67d911ef417565454aa3805667fa57b907bd2bdcd4dfefed1774c5ff3e8(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionAuthConfigUserPasswordPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd42eea643201dfcec57a669932cd990618a7263e3badc6e1da9dc82016cd2a0(
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
    auth_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionConfigVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionDestinationConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    eventing_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    eventing_enablement_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lock_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionLockConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    ssl_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e413761710edebfcce19cc338437025ebb351faa7005010c82db96495b841141(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionConfigVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3490c652ef0de051b994ef4b20a06ca53e4a0ddffdeacfa1e2f13064f31b38a0(
    *,
    type: builtins.str,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e39343dba42970cdfa9c2cb85d5ebaf6bc6c48edcc77fd7c40b145f3aaff40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77b9b1e3ec1594469b420a84b595cbb9445b544e536d5aaa2efe21afe9d7e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb85ec5667b953c83382a84dde55a988013080a26f72df5b8f425f36198acb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a914ee5d52a61e6dcbfdfe9f1cc3ff4f4883a699d6517e6389051bffb21f80(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189ca11fc932d97e8f8ac801b40109b2065bb77404480aad634cf6da7c8aef97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3f2db28906ca00f964e08486d74b570b9241dc54c14bd22d090b84f5dccbb4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72399a29d6938eef6059530c0ecd64f6996c883cf899ae5d360ed7d71f228b23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066daba24b1b8612feadfe4825d8fe7aa7c2812272376e8ea295c0b39292f89e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cf9d7b9fe3fa7ab4839c4db2f5da29e5824eaa9ab8670e891887c2352d35c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1826f58e6488372da8743dd568a8b67e619e3fb628d7e8e62e12d65a50222c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionConfigVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750449c72259b5eab223c5aaa9024ba3731b4b2d1d04be592edd51c80dc59323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c440fc7adb75ab3f22fe016f39322444d5bf8940428c49b3fa72a8e0e94d263(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1fd0bd17947517d04bc37b1444999f984ad054368528c1a08e2fe46b97682f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc086e19182a9f2c1a6b8e19f5e64e48aa60a3d9fdac0af8f20840165bb6f3d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b71d7f95e37e72fc0305b63620fcaaf6cd0c662fc0de9968c4f0832f09a453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee3bfb6c85740e45637e0f9333d7f78fcab76fa85a35035067f2bf3510a2971(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionConfigVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0183543818a08bea4a8e007da3f6029b9bc146dbcd786fe193861a0965e9e96f(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106e7a30aa708f9deff5ab97fade0b53e4d72e0f7ab30d29645ce42a479e43bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b0c04a0c17d31b98b1140dbb345763af0ea35c5891930f06d03fa699e9a041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da26b8da0794f9ecd491635be156ed01309af11559c23cdf77baa71a3c3f35c(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionConfigVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39adcf7b8cbd054d621797bc88c6a8c5b29732f1fc295c9e624eb963c106a99b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc97567be26f355d7f18b08db5994716f5c38b7cc6c994e28fb3156da0696d4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a9a5578171b02fa000c552bad65d67a2028455b76a4e368e40b77c18095cc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da99c057677614f7da442198e7caa38433140319d20c2e11555496368157183(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ea2b7da6ef66771d763a62b231df433a5f0dd565c675ae7af45f05c0f26210(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afd71ab2068a604f256686f7e5c776cbaa79ae0c5c9588a962c5f9f5e885300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa5dd9e1ee527ea2a0fea7ab0867f817c0b142616fde4afa354274d83a5c650(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionConnectorVersionInfraConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56c15bffafc414873a964d22e0f8cc31779d16aa0b50942c91995f7f8bdcc45(
    *,
    key: builtins.str,
    destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1f8d618904950a1fe1a6aad0c454efe58547e8953674145ae31d7def9494ff(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_attachment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d8dd5dee1b5c74e36a8f81fbdfa2a1cc9adf6bd8a8eaae6648ce634cc550ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb6c64c79bc85074bd88e2bcb53d160958782facc947dc998e0367eb83cf10a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee75c5ee330a5b89d7a0107e93dfa27ce168b183e6eab766d3c59007348a3801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3903f7cfd98dd80582f5465a457916e22ce5215c822d31a1afff8f1558ffd6ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30be18e3e8d4c5821b5b66acd1c5380e9c43d6869e4832de974db0c1e61b4c7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c074efa35c7106828339a1febd92bce4cb6eccba22600d34717c4cfbaa81c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfigDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74dfbb0434b8b97da17a750e90e5cccb4aea56e904901a48073759c1b71f61ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9763c2ca8e9b393e5da65aaed1fd285eafd466cfb537168dc77bb089e61c8c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a01dd58cf4c884a314a1fb2989faec7eebaf6300584cf7d44b464458c2cdbae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b6475795c2d3ab2f2daea93e4cf3c672643d6d5557301832d6ba5f6d9f7a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aed9c8ce3868bb7042beaa6787df175708875f61faa87ee402901a9fe9648e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfigDestination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0656e302108b376b4daacc5531de3699811ba6176fc32a3bab3f77f7fd55ff6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7fa6ddd1b1fdf552fab09a0f88058cc9b25ffafd0cf36fd80826b43549ef4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844691dcc9f4be6dfd6b57a093a9edd80bf511a2b858e696ec56cd8b07186e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b213d96f8df90449778bbe58d5418e7a689ecc2081059584280b5cba37a1d603(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34f2de98cb794aeca5b6315aaf2b176a533bee95c20c137e36aed44889798d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a72083c9d53ad2ab68f3d015a72e9d2e158c2fe6d08ea9283fac81ed04ea109(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionDestinationConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9745b06b64b917407c3f36f8bb6c24263bc4720d9782cf57b35cd773812008(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44959a5faa8631c1d11160d2f4a91966bcb4118e4acaf4762746a00945a4e35a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0caeb8e9a8f9e8a4e1b5ae2b9974d12f66cabd209fb76df19cb146d9e5ea4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de86a1a957e2617fb8bdf3d18202d5848c6e00c5263df97a26e74855d46ef863(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionDestinationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb36dd86335f91b17a68f4bd7803605f71cf0935a89c385b351769d5b50d86e(
    *,
    registration_destination_config: typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig, typing.Dict[builtins.str, typing.Any]],
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enrichment_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e2aceaa12aa12c5d75f6930cd21ed523a9312ae7fc498a7a06f5a10ed28f11(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63713d8301fb3e91f32963aa85f3936ebca05af6b2e1f43ea0b4c96288277f8f(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b555dae13d49af8265b1b602b5762bba6a54cc1f92e44029347269fdcfbda8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ddbd549a93ba56f20e5708e20caeb1ffb093aee8a9fe964e22b8f4971d51da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f05fb0b6d4528e061230950dda8ff1683b308639bb62e4b933f5eac6883164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4ee80ddda1011a9c09ee744164f931b87f22cd86fdf4b1dc95439ed9eee615(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5884622ed2b351cd2360a60d0291f402780bf9e17736affd313984782fc88d07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6102708df54dab51872192286a512ba49d1a46c23fdfdfc39cf669a9a9799ff9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f2fe939cc8c9ee4a4e7f4c6f49dd0ca7f7ce568247f49be4fdf767cf9fa5b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1174c538380a2a5114cb7c277e97a426ab6d61c5f347bb413c0192d38dbdac8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e5c5f72d57b03ddc9f6b0a4603910055aa0e875b2beb21de8e4e656f29c289(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b32f61d035368db02f5f3f15427cd12b5d754655f5c9e18533e6d0a5d58131(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a884c6343d53f4f3015b49453fa48d8b604826f132beb62c4be1377a51fad4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df6523c2beb8c95605382a8b747c4533bc79c635619af7b91e329f374eef182(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2399ae0bce659b2082571be071740de7fbf44ca99d0b35d0318d9f35910c56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aef9c274ef519b20fd6ef1d13892ae9e34156aa49200cc53cab927631240b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bc8b01791cddaacbf0dc9693a066492b72a632053ac5e07dbe34338fae0389(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a51b8a10e6a48e6011b26ad6ae5551a9070f29d199521f14aab4a14f1931d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33450fedd5f829acbcce4cfcf0d0c727143c4fee9d83b019952a3bd4794d2f76(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdafceb80669ab6051badf0ebb5085b3ed5ea4225d4edbd7633ae63857a3236e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74271f86467e59cb72d5b68171014eeef24b4f85a48bb43b00a80bb989f96c69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c45aada97633184cd590c96d211eed28391123b915f0066f38586ee644695(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9c6c7426675aaeb3e29c4ebbca800ee38355fedd16b228e05f86847148da84(
    *,
    auth_type: builtins.str,
    user_password: typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword, typing.Dict[builtins.str, typing.Any]],
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b474daf4bcfeee324b67ef180bc75508ed9a87250e1d53d60beb9bb1e47a8236(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db53f7c6ecf8d06b8992b403fc81f5296cc6e5827c9a29cbfec629962f176cb2(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0088053452224f174f8b6169e2a1eec80c9430411d849a90ca7b51293a3485(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed5624233df690c2e5d158b1ee8be3e50d5de3ee1a1df0761ff62af612dfbc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7510dcdc54a34254b9df7449ae942719ae687ac1d3e8ebecd34d02c7a925f1e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938141e9b779a581a514bdc9c1b17b692dd377255f384298bbe809e3a4b0b7ba(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06366101cf72174efdfc93884350a9f7b507bd497513ad1a2cc620691be684e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbae6dbba8438f0c37ace1c7f451796e591a20d9b351ba12a140b928416299be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa87bf33895d23c419984640c99a1e304e88c09a35877f451c011cc232d65d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf6ec9ecdb49ee27ff6150985fa95d18d886361731b8c80684a7cebbb220777(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dd927eb378152f7b9e88054eb5bccd51f814e0634e86091c5c39b935d342b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce62edd36cadca6990c9e7e2ec453c65920f04c315971c0f6a5a6120b64f5af4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8986f88a81170150c614a3df2990b29f8eb811373bc632b55635543cfb1f83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41951160c0b1f2fa207f9579fff92a8ccf5568ebdcf1a461a23a69f4aae7cb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13978ca99ecd33845da44a8be0bb73cfb0a50b292b7e457c76e8bb56361a95e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7283bf6a2871de6df2f55c67787a2bfe1409e096fb7b05f839978038769b6529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631b3da6255a4fe12b69b72d2a11445cc336b2e079d3dacbf7cc36b395cfa4ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa48c820cacbf647abc19bb3f0e27efbed4306e687b340f21b66d8c78762134(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca727823027acfe04bfcb5b4ced9034d40cd2ea8cbbd736777f0e4de44d89ff(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6977274293c2914736c1c4e0b0b79e7f5d7cca7b4547e10b9365601f55d07a92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1132bae1a0a4c3e852e5274cfaecd9c682d5c30f9ad6d73a0408ebf2c1c84600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860bf661691706c30d6e096da1c692d657ec7fe0af5532018d9c863c3411959e(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a435d9ac3dd7aaf09e7702db67b7ecfb278fd0abab280e8b9448175503f6eec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccef8aa791e4a9ffde185c8d641027b53e752b111e5e52ce566b0922f8b039a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c929923e30b926f666122bd3e6391b45bc9503b38713a85ee8641cc249fd44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5352058c3e844d74f682ffd309363d78a8c014556954e37bdcce8a77addd3f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aeaa709ca1d8c26a7935426d7b811da0fed4f18013443341b362b77e5194f49(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8ef587e461ae6d239e673e981ea8814b7ed76184822f71064b8217720cf7fc(
    *,
    password: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1045ce85ba519a5ff21332040181756246476704af8a5a5172961287d0bab807(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c2c15dc007038d28bd5c3bf87e6e5bcb34cb5312827736174e9bc87254b27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db002f2c68278dff1d72bfc161f855fceb2f6e933bd8620ab7fee83aaca576a1(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a383743cece1b679382cb5a727121224227c445d655dc851109f5295cb8d28(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa35ad6a837e1adedcc7dc5367156e80ffeca64daebacb585abe58dad12a2e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7f4a8dedf038860222dd8ade3c2d175ff24cac6926647ec2c053a55495cb90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dc9f61e8c5ecb54107f6595365a1df458d4909ea5215876f98df0eb3039d5a(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigAuthConfigUserPasswordPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a910bfa32a7c120b1ccf90db69285f5c08958947bd604aa8a55b3eaf0fcfd831(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deb28e3375bc9a06cf0570373b56c67c556fc8711fb6d057e0cd89bbd650cb4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5975b9a1f85826f91f021811272818ece82b89160a7e76ebe929ec9e27baea76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63ee403cd604fa4278e5a73d77be432a438e1d0f3e78bca1271bdc70c756d2c(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872fb709e653825be4e623c802cb345d32cfe267ff8060d423ceca32906dc997(
    *,
    destination: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d1530fad6a7e0ff510983fa053fa1f9538d784aa58e323cb23fbf6e220dc5c(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_attachment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d8ec93df02a5a279eb8b54ab81be0f6dd1e9811946ada5597a39f1f05c336f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ce878aead28208ae3b1afd2d1db9938bc2deb4fc84982bc0ec80de6021ddda(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9807cfb91a8c63dcaf6d4cf2d7518e8aab0b9df237c99a086458bbac2cac476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7153c4b5f98e9af85d95b40d42de942d829f784748a6808202990466652c4b42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020737d5b855c9dbb429b0065d8cf0554322cb340a6793aad412084fb743308a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c588fed34cd10ad051a656b92edecc122e07c6c48d0ee362bbbac4bc367d55(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711fa75148dea414f250f4dcab2f7e6e455adf18966d6463914c268073c90009(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dd63870ee74e133302de811dac2a7ac8e4bd66f4af679e25b4362de416e003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff935ec53df77519be6db32cbe9d9d3d54121a4f78a311505792bb57c6391982(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779933ff4d98d4abf824395f7f08f31fcbf094003c31b119cb9db5cf71f724c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2310e455038c803f7935adcd1718a13ce297ba47f31f1d5b966d5050a092a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17067378f626ce0ec96ca039a5929869e081e7fe5cd78bb634b45032fe39fee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728107577b108b65c60d21fa148ae342b70926b2d3c457e30c40ee0c5394a305(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfigDestination, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fe4a03ca3224e4fe895fc7dab5165600cd7890d875e80fe87a321746f4c602(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a82b6ee8b8993fe97df25bd0428487406d6e947b160c64fc557ba9989dffe8(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingConfigRegistrationDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d87e0b019f88d3a98544e76372befee87668c69f1e1b1a152eaf16698664521(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16b8de417c27eb47de4708ae55e9ada78c4fbc585913f82e5ceb3ed3f2fe0c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2315acdecf2e9d5d87cbf691d5563d5434808992c65d799e865151c94b7e0095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59762a2f656816a2f7eddd044410334409e0e7d3d58151ef9039a20ce98d13bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ef68aaa25d89a46193e771d94e19e7d75d8a25080355bc65c06a46b11af988(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb29a8e76deaf9e46d754beb8cf0c4602aa3b1b6323179617ed86b3255382a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00509d34093c6541551749cf03f9e382b730238d44a6b26b2a95f2de63dbec63(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a6e677b97cb8ee27dfe493a8b9b0492759b324b7a3cfd1b5ca43a1496373f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a504b6f315a678387753860acb1b483e7a214d9ae5b1ac635eda581190ad0c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960f842877d22ea23375324fcff3784360a748e0743d431a960d3ba3ff93ef7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bed70c48ce19565df8c7e4a9dcf266ad723a9ca6fe1c8c007e2397a0fe1d956(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92734a5993f0813e597bbd0f500046d6621ef09bf49d49ef6d91052ec4bf4861(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f7fd1faafe394d37bcb41296b02d40acbdb91a3b025aa471202642dd4f44ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5e2fa7326cf6763e942fb87b4aabf9fab9bac83e0086a1dcf6af51ca8ccb8c(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionEventingRuntimeDataStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d4e23b4fbd96d04999cc28c29eb0af455dc5c70514f2e437e16afa6453cf1c(
    *,
    locked: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed7d268397f37b04f295852a3dce4cb36ee9acc5291b6a2e86e66d842ec38f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108acabf4335f656f54fc2ed9ac73209be3a0ffaa3431b3df1da3b2aa13a594c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa1c5fa9963ba5be26c813288387a628652ff0e9bc75508ab04f54ff270c122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4988cc997d0fc85be6ebd544b976a26cf2662f3029b6d05dfec4ea6836fc3150(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionLockConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4f9cb809ddf067c75ca41e1955b3a1b154b2a0d1936eee339abf11fab06105(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd2c51911e47d9fe7d767c28e8114f0e8f0e56dc1fc3df1657261d4955407fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5dbc5384d9a6c63a3c21ef83108f237733fe249d412c09fc354a488f5d5c63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6c770da343af1cb0e34b4c5931b6a76b88afdf0ade0ec4c71a4d621dfac3ef(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afb22892c95577b853c5d3c635236a00fe467363254f1913f71571c22518e82(
    *,
    max_node_count: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7da18d431a438ced37eb767d34f341d2f407b016a27a3bed1c3917215eee8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeb2379ae67e91cf9fdcc7802bad40c59248b2dae1a2c7db1026e37a5e7d4d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c463e32741832f6758dc6d950ef2717d4c156b4a21a4656e1f5b3cacdc337d51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa817851136529b736ea0c7fd452c4fae04f73ab84a570967cccdf6783c4687(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88073145527602431423adf81af858d385ef46376a5aec85d13f730b0e9b6a9e(
    *,
    type: builtins.str,
    additional_variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_certificate: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    client_cert_type: typing.Optional[builtins.str] = None,
    client_private_key: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey, typing.Dict[builtins.str, typing.Any]]] = None,
    client_private_key_pass: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass, typing.Dict[builtins.str, typing.Any]]] = None,
    private_server_certificate: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    server_cert_type: typing.Optional[builtins.str] = None,
    trust_model: typing.Optional[builtins.str] = None,
    use_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b080f47f7f1bc20574e9dee85a870f92317830b0a0959653660c7d59c7690404(
    *,
    key: builtins.str,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    secret_value: typing.Optional[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue, typing.Dict[builtins.str, typing.Any]]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7b0c4e45d4cd41e31d297cc33723c7cc442298e6846342f1bc2564df185280(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd453c8e0a747164ff9f99f045dfb6f20958521b068bca46ba431517fd1a64dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813eb2727df3882007c37c228b2557b242a12856cdf73eb87b731b61ec5553c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69c55130108f67655ab1b1d5cae73907bcaa3409ee5b76f54ce27d00d4120ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd063306ab990780887a1953b53a54f57d497d728eac77a61352c5de926d2a7d(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableEncryptionKeyValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca8c5a1b5a7e3c621b01949a3868981c5b315929546388ca56a7afaf1d22d00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd49924f2d5ddfcb8c999896a267dba2c3007c60b2548794756438c9462f9b8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf017f0408cf6ea9cdd36b0b498d5b47eb55245b139dc463d5f5c9f0815d9db9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fb525a989649268f8bdf0f6cd215a6fffeac9b5b4f5e5d1b72833a16d250fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f23c5a6072b430b1f38f3e5d01798913ea2e00b39cba5c574212e7f180a031(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ee9b56eea79aa168b6b5a2e68ce7e6c44c4ca3ea74863c493765c5a0887681(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2255f3b702345672df81dc439c394b6395e0d5187d3cb3c3426eca41dcadeb36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182ee9afcee5f23f99fb6b1b17b94c3364cb7b4008abccda7309fb8c9cb22d74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d608472ba68174769a7a2056ae00810c40d9d593977aa95d386a34f30ab8cc5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431157508b34e42ab6fe23dd25dc4d920d2e1c77a466dd23d79f2b89d4ba0f96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14abcfe040dc92834c93e2e450e0034dea0bcc987c5caf6b3043388d25d6336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5f00bd39eb7f5c616af9a4a8e68844bccd77d12ed93256c7cc385ec17b7a06(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a91d587eec1842e8459bb49a0d3ce4c7f5df37cc2bab29d195a9352dc43f77f(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0589f76656346bd37ee3cc8eb3af588f5b81fb0bc84d438294f59de455fab3a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4649c09eb4a7a4ac19d85134ff6b32a924360e7fbb318546108083001a29353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671da39f3f891991cab2506bbf380355dd9e2f0aebf148d7c3a9182efe92fbd9(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariableSecretValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93613594ab5a3c56278988e6f8387002184ef527210daa8b64ccfcbb233e966(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8febc21fbf1412fe14f2a16b51fb6ed628b151af0ba8d01b6e778b96560f5057(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7f8f03e0f08e195e8ee57f317ca0996ac8476697577f31c99dfcab6813293a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71bee84d22f1b5b1442b9bee43c8bb2ec314c639516c9d0bdc86159a8ec7d5f8(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82074909f074e96dfc4c31c8b8435e7e4c8d9d8d813e3599d4999bd4b4b02c70(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e7a7dec8462d5a829376dbd951ebbad1492932ad133655aff4f9ab8036318e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e68fa560ab184f0222be55eb3d7a3c6a66e682809f094eb6180ba95d8535b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c450e14ee52df6fd6469d31340a5dec80a0803bce94384064b90f4a14ac00ff5(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f174b07e703c7f8487d2dd379b7ca6664ad836661074ef09db5396dcfa1bc36b(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bf7bfbb750304eeb4bfa5ddc7a767db43e3744e86cc6b5ef88cc0d49fb0d26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fede34b5b4e6c81f77ebd44aaef9462e442d8b97a44a3c160fa21a7ef0b1fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52329b896e7db056c6829466b9f1f5d117cef89d617235633b85c34540a0425d(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigClientPrivateKeyPass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a72b80365ca66b11ff133d4fa8591bac00565a51c25239b86b6d15726a044e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7b9713d0a84c263664f118451bb04dea4ccfc5c63ad2eea906629ce1bf5ae1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleIntegrationConnectorsConnectionSslConfigAdditionalVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29f8503f3b5a8c05195ae0d52861481db5ff418924553e92b1ed00a164dec86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4575c86332578d5b49bd8936c05f0f82fc40aaafd6cf94357e3da967aa7a8fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240f7c5007c32d3b796bd6d05244b7ca607c18544451e7086c51159c568b76aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034ed1472bff0ecab8d7f2415462de2d054c9699216287d16ade5f87ce6fc39c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9724141d1bbab6d13e4271167cfcad2efc9fc752d691959fac549c1bef9b1789(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aaf2c19a0b21d6c45c602cfef181ac9efd9a21ae9df73019f346bf0a8e1e5e7(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe7f58cbc3a71d569ac1617bbc384cfd91f4c3ee30810fd162ba8520bd7336e(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de8918ab8dd6977ac5d77138800d577f8100523e58fd7ed62083ae18ecf18ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dcfe685bbb982dc7ceeeff988bcc8d49ceec336f6185ef432df41d37bdaa26d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0206e335bd57838ec0975d079c529a1efbe83fab184c241b9d46786aa2c88fee(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionSslConfigPrivateServerCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8944378adc175a90dd7fefd1862016344072696ad6ca16289062cfcd50457042(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dac355565f3894ebff752f70bc938d1b50e339e5cefeea9fd9cd847d1eee132(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307520d189b98548e660106ddb143742fc6d278a44a63405aae6e757f5604b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd1cf5d3652be9fdaaee8eca1bdba1d1c1d5f4a9fb57f1efc280a6c2bd8a48a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f0fcbf74a972bf99e272854c703c85cf5d0ea64c2cb82734f2d0fdab398dfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb04cb5f456410b9da82ecc1eb8db086a1d72343b768b58fd2193f7900e4c52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb04283b4bc0b65d1b7388c34a266bf22a434b69ec37fe7d17b38090c44cf2c(
    value: typing.Optional[GoogleIntegrationConnectorsConnectionStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eaf27154e3d64f853eb3f580a52ec56afedaa4d43c6cbc64e487e00d17a14c1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0465b696c6f3b665da83d8f5be97bfcef6fd4f1798202e278b2b72e7ab4e4d39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e291d55359fbd50562abfe2c4e12d045ae6ecee32dbdd2764d3494da54aad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f193ca04ea8adec1a480f443da58224700b70850d2d827d75a456b3ed3fa3e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f90b8d19e8e8bda0524cd2069d2c702d183d1ee4a841e364d63cefb3700489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67a7fd7794008ca0c29595d609a07996d2fdd7a2fb5583cf6b678bb3dc5f6b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIntegrationConnectorsConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
