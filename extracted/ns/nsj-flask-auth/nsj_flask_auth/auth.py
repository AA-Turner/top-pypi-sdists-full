# pylint: disable=C0301, C0114, C0115, W0718, W0719, W1203, W3101, C0415, W102, C0411
import os
import logging
import requests

from typing import List
from enum import Enum
from functools import wraps
from urllib.parse import urljoin

from flask import request, abort, jsonify, g

from nsj_flask_auth.caching import Caching
from nsj_flask_auth.exceptions import Forbidden, MissingAuthorizationHeader, Unauthorized, InternalUnauthorized, UnknowAuthorizationException
from nsj_flask_auth.settings import log_time


class Scope(Enum):
    TENANT = 0
    GRUPO_EMPRESARIAL = 1
    EMPRESA = 2
    ESTABELECIMENTO = 3

class ProfileVendor(Enum):
    DIRETORIO = 1
    NSJ_AUTH_API = 2


class Auth:
    """Esta classe é responsável por disponibilizar um fluxo básico de autenticação através
    dos métodos decoradores requires_api_key, requires_access_token e requires_api_or_access_token.

    Para seu funcionamento mínimo é necessário que você defina os seguintes parâmetros:

    diretorio_base_uri: raiz da url do diretório.

    profile_uri: url do endpoint que retorna o perfil do usuário.

    diretorio_api_key: chave de acesso da sua aplicação.

    profile_vendor: Determina qual a api de profile utilizar, Diretório ou nsj-authorization-api.

    nsj_auth_api_url: Url base da nsj-authorization-api.

    nsj_auth_api_token: Token  da nsj-authorization-api.

    Recomenda-se instanciar a classe em um arquivo próprio e importar sua instância a partir dele.

    Caso tenha sido implementado um serviço de caching na aplicação é possível fornecer uma
    instância do objeto como parametro de inicialização. Até o momento este recurso só foi
    validado com instancias do módulo flask_caching.

    A inicialização também permite configurar as permissões de acesso necessárias
    (user_internal_permissions, user_tenant_permissions, app_required_permissions). Porém caso
    seja configurado na sua iniciliazação, não será possível utilizar o método decorador com
    permissões menores do que a configurada.
    """

    _cache = None

    def __init__(
        self,
        diretorio_base_uri: str = None,
        profile_uri: str = None,
        diretorio_api_key: str = None,
        api_key_header: str = "X-API-Key",
        api_instalacao_header: str = "X-API-Key",
        access_token_header: str = "Authorization",
        user_internal_permissions: list = [],
        user_tenant_permissions: list = [],
        app_required_permissions: list = [],
        caching_service=None,
        scope: Scope = Scope.GRUPO_EMPRESARIAL,
        user_scope_permissions: List = [],
        app_name="app",
        profile_vendor: ProfileVendor = ProfileVendor.DIRETORIO,
        nsj_auth_api_url: str = None,
        nsj_auth_api_token: str = None,
        introspect_url: str = None,
        introspect_token: str = None
        
    ):
        self._diretorio_base_uri = diretorio_base_uri
        self._profile_uri = profile_uri
        self._diretorio_api_key = diretorio_api_key
        self._api_key_header = api_key_header
        self._api_instalacao_header = api_instalacao_header
        self._access_token_header = access_token_header
        self._user_internal_permissions = user_internal_permissions
        self._scope: Scope = scope
        self._user_scope_permissions = user_scope_permissions
        self._app_required_permissions = app_required_permissions
        self._user_tenant_permissions = user_tenant_permissions
        self._profile_vendor = profile_vendor
        self._nsj_auth_api_url = nsj_auth_api_url
        self._nsj_auth_api_token = nsj_auth_api_token
        self._introspect_url = introspect_url
        self._introspect_token = introspect_token

        if caching_service:
            self._cache = Caching(caching_service)

        if "APP_NAME" in os.environ:
            self._logger = logging.getLogger(os.environ["APP_NAME"])
        else:
            self._logger = logging.getLogger(app_name)

    def _verify_api_key(self, app_required_permissions: List = None):
        api_key = request.headers.get(self._api_key_header)

        if not api_key:
            self._verify_system_api_key(app_required_permissions)
            return

        app_profile = self._get_app_profile(api_key)

        g.profile = self._create_profile_from_app_profile(app_profile)

    def _verify_instalacao_key(self, app_required_permissions: List = None):
        instalacao_key = request.headers.get(self._api_instalacao_header)

        if not instalacao_key:
            raise MissingAuthorizationHeader(
                f"Missing {self._api_instalacao_header} header")

        app_profile = self._get_app_profile_by_instalacao(instalacao_key)

        if app_profile.get("tipo") == "instalacao":
            g.profile = {
                "nome": "Instalação",
                "email": "",
                "authentication_type": "instalacao",
            }
            return

        raise Unauthorized("Instalações não são válidas")

    def _verify_access_token(
        self,
        user_internal_permissions: List = None,
        scope: Scope = Scope.GRUPO_EMPRESARIAL,
        user_scope_permissions: List = None,
    ):

        access_token = request.headers.get(self._access_token_header)

        if not access_token:
            raise MissingAuthorizationHeader(
                f"Missing {self._access_token_header} header"
            )

        user_profile = self._get_user_profile(access_token)

        email = user_profile.get("email")

        if not email:
            raise Unauthorized("O token do usuário não é válido")

        if user_internal_permissions:
            profile = self._verify_user_permissions(
                user_internal_permissions, email)

        if self._user_internal_permissions:
            profile = self._verify_user_permissions(
                self._user_internal_permissions, email)

        else:
            profile = self._verify_user_permissions(None, email)

        g.profile = {
            "nome": user_profile.get("name"),
            "email": user_profile.get("email"),
            "user_profile": profile,
            "authentication_type": "access_token",
        }

        if user_scope_permissions:
            self._verify_permission_by_scope(
                user_scope_permissions, email, scope=scope)
            return

        if self._user_scope_permissions:
            self._verify_permission_by_scope(
                self._user_scope_permissions, email, scope=self._scope
            )
            return

        return

    def _verify_system_api_key(self, app_required_permissions: List = None):
        authorization_token = request.headers.get(self._access_token_header)

        # Não possui header 'Authorization'
        if not authorization_token:
            raise MissingAuthorizationHeader(
                f"Missing {self._access_token_header} header"
            )
        
        # Se token não possui 'Basic', a autenticação será gerida pelo validador de access token
        if "Basic " not in authorization_token:
            raise MissingAuthorizationHeader(
                f"Missing {self._access_token_header} header with Basic prefix"
            )

        headers = {"Authorization": authorization_token}

        url = urljoin(self._nsj_auth_api_url, f"/authorization/api/validate")

        response = requests.get(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            raise InternalUnauthorized("A chave recebida na autenticação basic (header Authorization) não é válida")
        elif response.status_code != 200:
            raise UnknowAuthorizationException(f"Erro desconhecido na validação do profile: {response.status_code}. Mensagem: {response.content.decode()}")

        g.profile = self._create_profile_from_app_profile(response.json())


    @log_time('Pegar profile do diretório')
    def _get_user_profile_diretorio(self, email):
        user_profile = None

        if self._cache:
            user_profile = self._cache.get(email)
            if user_profile:
                return user_profile

        url = urljoin(self._diretorio_base_uri, f"/v2/api/profile/{email}")
        headers = {"apikey": self._diretorio_api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            raise InternalUnauthorized("A api-key do sistema não é válida")
        elif response.status_code != 200:
            raise Exception(f"Erro desconhecido na recuperação do profile: {response.status_code}. Mensagem: {response.content.decode()}. URL: {url}")

        user_profile = response.json()

        if self._cache:
            self._cache.set(email, user_profile)

        return user_profile

    @log_time('Pegar profile do nsj auth api')
    def _get_user_profile_auth_api(self, email):
        user_profile = None

        if self._cache:
            user_profile = self._cache.get(email)
            if user_profile:
                return user_profile

        if self._nsj_auth_api_url is None:
            raise Exception("Url da api de profile não foi definida.")

        if self._nsj_auth_api_token is None:
            raise Exception("Token da api de profile não foi definido.")

        access_token_basic = self._nsj_auth_api_token
        if "Basic " not in access_token_basic:
            access_token_basic = "Basic " + access_token_basic

        headers = {"Authorization": access_token_basic}

        url = urljoin(self._nsj_auth_api_url, f"/authorization/api/profile/{email}")

        response = requests.get(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            raise InternalUnauthorized("O token de autenticação não é válido.")
        elif response.status_code != 200:
            raise Exception(f"Erro desconhecido na recuperação do profile: {response.status_code}. Mensagem: {response.content.decode()}. URL: {url}")

        user_profile = response.json()

        if self._cache:
            self._cache.set(email, user_profile)

        return user_profile

    def _get_user_profile_vendor(self, email):

        match self._profile_vendor:
            case ProfileVendor.DIRETORIO:
                return self._get_user_profile_diretorio(email)
            case ProfileVendor.NSJ_AUTH_API:
                return self._get_user_profile_auth_api(email)
            case _:
                raise Exception(f"Profile inválido: {str(self._profile_vendor)}.")

    def _create_profile_from_app_profile(self, app_profile: dict):
        """ Cria objeto de profile da aplicação a partir do profile retornado pelo diretório ou nsj-authorization-api"""

        if app_profile.get("tipo") == "sistema":
            return {
                "nome": app_profile["sistema"].get("nome"),
                "email": "",
                "authentication_type": "api_key",
            }
    
        if app_profile.get("tipo") == "tenant":
            return {
                "nome": app_profile["codigo"],
                "email": "",
                "tenant": app_profile["tenant"].get("id"),
                "authentication_type": "api_key",
            }
    
        raise Unauthorized("Somente api-keys de sistema/tenant são válidas")

    def _verify_user_permissions(self, user_internal_permissions: List, email: str):

        user_profile = self._get_user_profile_vendor(email)

        if not user_internal_permissions:
            return user_profile

        if list(
            set(user_profile.get("permissao", [])) & set(
                user_internal_permissions)
        ):
            return user_profile

        raise Forbidden(
            "O usuário não possui permissão para acessar este recurso.")

    def _verify_permission_by_scope(
        self, permissions: List, email: str, scope: Scope = Scope.GRUPO_EMPRESARIAL
    ):
        user_profile = self._get_user_profile_vendor(email)

        entity_scope_id = self._get_entity_scope_id_from_request(scope)

        functions = self._get_functions_by_entity_scope_id(
            user_profile, scope, entity_scope_id
        )

        all_permissions = []

        for function in functions:
            all_permissions += self._get_permissions_by_function(
                function["id"])

        if list(set(all_permissions) & set(permissions)):
            return

        raise Forbidden(
            "O usuário não possui permissão para acessar este recurso.")

    def _get_entity_scope_id_from_request(self, scope: Scope = Scope.GRUPO_EMPRESARIAL):
        data = {}
        if request.method in ["GET", "DELETE"]:
            data = request.args
        elif request.method in ["POST", "PUT", "PATCH"]:
            data = request.get_json()
        else:
            data = request.args

        if scope == Scope.TENANT:
            return data.get("tenant")
        elif scope == Scope.GRUPO_EMPRESARIAL:
            return data.get("grupo_empresarial")
        elif scope == Scope.EMPRESA:
            return data.get("empresa")
        elif scope == Scope.ESTABELECIMENTO:
            return data.get("estabelecimento")

    def _get_functions_by_entity_scope_id(
        self, user_profile, scope: Scope, entity_scope_id
    ):
        # Loop through tenants
        for tenant in user_profile.get("tenants"):
            if scope == Scope.TENANT and tenant.get("id") == entity_scope_id:
                return tenant.get("funcoes")
            # Loop through gruposempresariais
            for grupoempresarial in tenant.get("gruposempresariais"):
                if (
                    scope == Scope.GRUPO_EMPRESARIAL
                    and grupoempresarial.get("id") == entity_scope_id
                ):
                    return grupoempresarial.get("funcoes")
                # Loop through empresas
                for empresa in grupoempresarial.get("empresas"):
                    if scope == Scope.EMPRESA and empresa.get("id") == entity_scope_id:
                        return empresa.get("funcoes")
                    # Loop through estabelecimentos
                    for estabelecimento in empresa.get("estabelecimentos"):
                        if (
                            scope == Scope.ESTABELECIMENTO
                            and estabelecimento.get("id") == entity_scope_id
                        ):
                            return estabelecimento.get("funcoes")

        return []

    def _verify_api_key_or_access_token(
        self,
        app_required_permissions: list = None,
        user_internal_permissions: list = None,
        scope: Scope = Scope.GRUPO_EMPRESARIAL,
        user_scope_permissions: list = None,
    ):
        try:
            self._verify_api_key(app_required_permissions)
            return
        except MissingAuthorizationHeader:
            pass
        except Unauthorized:
            pass

        self._verify_access_token(
            user_internal_permissions, scope, user_scope_permissions
        )

    def _verify_api_key_or_instalacao_key(
        self,
        app_required_permissions: list = None
    ):
        try:
            self._verify_api_key(app_required_permissions)
            return
        except MissingAuthorizationHeader:
            pass
        except Unauthorized:
            pass

        self._verify_instalacao_key(
            app_required_permissions
        )

    @log_time('Pegar profile a partir do access token')
    def _get_user_profile(self, access_token):

        if self._cache:
            user_profile = self._cache.get(access_token)
            if user_profile:
                return user_profile

        access_token_bearer = access_token

        if "Bearer " not in access_token:

            # Se token possui 'Basic', a tentativa de validação já foi feita via apikey de sistema
            if "Basic " in access_token:
                raise UnknowAuthorizationException(
                    f"Basic auth should be handled as API Key, not as access token"
                )

            access_token_bearer = "Bearer " + access_token

        headers = {"Authorization": access_token_bearer}
        response = requests.get(self._profile_uri, headers=headers)

        if response.status_code != 200:
            raise Unauthorized("O token do usuário não é válido")

        if self._cache:
            self._cache.set(access_token, response.json())

        return response.json()

    @log_time('Pegar profile a partir da apikey')
    def _get_app_profile(self, api_key):

        if self._cache:
            app_profile = self._cache.get(api_key)
            if app_profile:
                return app_profile

        data = f"apikey={api_key}"

        headers = {
            "apikey": self._diretorio_api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        url = urljoin(self._diretorio_base_uri, "v2/api/validate")

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            raise InternalUnauthorized("A api-key do sistema não é válida")
        elif response.status_code != 200:
            raise Exception(f"Erro desconhecido na validação do profile: {response.status_code}. Mensagem: {response.content.decode()}")

        if self._cache:
            self._cache.set(api_key, response.json())

        return response.json()

    @log_time('Pegar profile a partir da instalação')
    def _get_app_profile_by_instalacao(self, instalacao):

        if self._cache:
            app_profile = self._cache.get(instalacao)
            if app_profile:
                return app_profile

        data = f"apikey={instalacao}"

        headers = {
            "apikey": self._diretorio_api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        url = urljoin(self._diretorio_base_uri, "v2/api/validate")

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            raise InternalUnauthorized("A instalação do sistema não é válida")
        elif response.status_code != 200:
            raise Exception(f"Erro desconhecido na validação do profile: {response.status_code}. Mensagem: {response.content.decode()}")

        if self._cache:
            self._cache.set(instalacao, response.json())

        return response.json()

    @log_time('Pegar permissões por funções')
    def _get_permissions_by_function(self, function_id):

        permissions = None

        if self._cache:
            permissions = self._cache.get(function_id)
            if permissions:
                return permissions

        if not permissions:
            url = urljoin(
                self._diretorio_base_uri, f"v2/api/funcoes/{function_id}/permissoes"
            )
            headers = {"apikey": self._diretorio_api_key}
            response = requests.get(url, headers=headers)

            if response.status_code == 401 or response.status_code == 403:
                raise InternalUnauthorized("A api-key do sistema não é válida")
            elif response.status_code != 200:
                raise Exception(f"Erro desconhecido na recuperação das permissões do profile: {response.status_code}. Mensagem: {response.content.decode()}")

            permissions = response.json()

            if self._cache:
                self._cache.set(function_id, permissions)

        return permissions

    def _format_erro(self, status_code: int, message: str):
        import json

        error_body = {
            'code': status_code,
            'message': message
        }

        headers = {
            "Content-type": "application/json"
        }

        return (json.dumps(error_body), status_code, headers)

    def requires_api_key(self, app_required_permissions: List = None):
        """Decorador que garante o envio de uma api-key válida. Caso não seja enviada ou seja
        enviado uma api-key inválida, a chamada será automaticamente abortada. A parametrização
        da mensagem de erro ainda não está disponível. O decorador também aceita como parametro
        uma lista de permissões que o sistema deve ter para acessar o recurso. Esta lista trabalha
        em adição a lista fornceida na inicialização da classe.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self._verify_api_key(app_required_permissions)
                    return func(*args, **kwargs)
                except Forbidden as e:
                    return self._format_erro(403, f"{e}")
                except MissingAuthorizationHeader as e:
                    return self._format_erro(401, f"{e}")
                except Unauthorized as e:
                    return self._format_erro(401, f"{e}")
                except InternalUnauthorized as e:
                    return self._format_erro(500, f"{e}")
                except Exception as e:
                    self._logger.exception(
                        f"Erro na autenticação/autorização. Mensagem: {e}")
                    return self._format_erro(500, f"{e}")

            return wrapper

        return decorator

    def requires_instalacao_key(self, app_required_permissions: List = None):
        """Decorador que garante o envio de uma instalacao-key válida. Caso não seja enviada ou seja
        enviado uma instalacao-key inválida, a chamada será automaticamente abortada. A parametrização
        da mensagem de erro ainda não está disponível. O decorador também aceita como parametro
        uma lista de permissões que o sistema deve ter para acessar o recurso. Esta lista trabalha
        em adição a lista fornceida na inicialização da classe.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self._verify_instalacao_key(app_required_permissions)
                    return func(*args, **kwargs)
                except Forbidden as e:
                    return self._format_erro(403, f"{e}")
                except MissingAuthorizationHeader as e:
                    return self._format_erro(401, f"{e}")
                except Unauthorized as e:
                    return self._format_erro(401, f"{e}")
                except InternalUnauthorized as e:
                    return self._format_erro(500, f"{e}")
                except Exception as e:
                    self._logger.exception(
                        f"Erro na autenticação/autorização. Mensagem: {e}")
                    return self._format_erro(500, f"{e}")

            return wrapper

        return decorator

    def requires_api_key_or_instalacao_key(self, app_required_permissions: List = None):
        """Fluxo que implementa os decoradores requires_instalacao_key e requires_api_key.
        Neste fluxo, caso seja enviado na mesma requisição um instalacao key e uma api key,
        primeiro é validado o api-key e se for válido, o access token é ignorado.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self._verify_api_key_or_instalacao_key(app_required_permissions)
                    return func(*args, **kwargs)
                except Forbidden as e:
                    return self._format_erro(403, f"{e}")
                except MissingAuthorizationHeader as e:
                    return self._format_erro(401, f"{e}")
                except Unauthorized as e:
                    return self._format_erro(401, f"{e}")
                except InternalUnauthorized as e:
                    return self._format_erro(500, f"{e}")
                except Exception as e:
                    self._logger.exception(
                        f"Erro na autenticação/autorização. Mensagem: {e}")
                    return self._format_erro(500, f"{e}")

            return wrapper

        return decorator

    def requires_access_token(
        self,
        user_internal_permissions: List = None,
        scope: Scope = Scope.GRUPO_EMPRESARIAL,
        user_scope_permissions: List = None,
    ):
        """Decorador que garante o envio de um access token válido. Caso não seja enviado ou seja
        enviado um access token inválido, a chamada será automaticamente abortada. A parametrização
        da mensagem de erro ainda não está disponível. O decorador também aceita como parametro
        uma lista de permissões internas que o usuário deve ter para acessar o recurso.
        Esta lista trabalha em adição a lista fornceida na inicialização da classe. Também é
        possível fornecer uma lista de permissões por tenant, porém esta funcionalidade ainda
        não está disponível.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self._verify_access_token(
                        user_internal_permissions, scope, user_scope_permissions
                    )
                    return func(*args, **kwargs)
                except Forbidden as e:
                    return self._format_erro(403, f"{e}")
                except MissingAuthorizationHeader as e:
                    return self._format_erro(401, f"{e}")
                except Unauthorized as e:
                    return self._format_erro(401, f"{e}")
                except InternalUnauthorized as e:
                    return self._format_erro(500, f"{e}")
                except Exception as e:
                    self._logger.exception(
                        f"Erro na autenticação/autorização. Mensagem: {e}")
                    return self._format_erro(500, f"{e}")

            return wrapper

        return decorator

    def requires_api_key_or_access_token(
        self,
        app_required_permissions: List = None,
        user_internal_permissions: List = None,
        scope: Scope = Scope.GRUPO_EMPRESARIAL,
        user_scope_permissions: List = None,
    ):
        """Fluxo que implementa os decoradores requires_access_token e requires_api_key.
        Neste fluxo, caso seja enviado na mesma requisição um access token e uma api key,
        primeiro é validado o api-key e se for válido, o access token é ignorado.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self._verify_api_key_or_access_token(
                        app_required_permissions,
                        user_internal_permissions,
                        scope,
                        user_scope_permissions,
                    )
                    return func(*args, **kwargs)
                except Forbidden as e:
                    return self._format_erro(403, f"{e}")
                except MissingAuthorizationHeader as e:
                    return self._format_erro(401, f"{e}")
                except Unauthorized as e:
                    return self._format_erro(401, f"{e}")
                except InternalUnauthorized as e:
                    return self._format_erro(500, f"{e}")
                except Exception as e:
                    self._logger.exception(
                        f"Erro na autenticação/autorização. Mensagem: {e}")
                    return self._format_erro(500, f"{e}")

            return wrapper

        return decorator
    
    def _fast_access_token_or_apikey(self, access_token: str, apikey: str):

        if access_token:
            # Validação com access_token
            headers = {
                "Authorization": f"Basic {self._introspect_token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            url = self._introspect_url

            data = {
                "token": access_token.replace("Bearer ", ""),
                "token_type_hint": "access_token"
            }

        elif apikey:
            # Validação com apikey
            headers = {"apikey": apikey}
            url = urljoin(self._diretorio_base_uri, "v2/api/validate")
            data = {
                "apikey": apikey
            }

        else:
            raise MissingAuthorizationHeader("Missing authorization headers")
        
        response = requests.post(url, headers=headers, data=data)        

        if response.status_code != 200:
            raise Unauthorized("A api-key do sistema ou access token não é válido")
        
        response = response.json()

        if response.get("active") is False:
            raise Unauthorized("A api-key do sistema ou access token não é válido")

        g.user_data = {
            "name": response.get("name") if access_token else "unknown",
            "email": response.get("email") if access_token else "unknown",
            "type": "access_token" if access_token else "apikey"
        }

        return
    
    def fast_access_token_or_apikey(self):
        """
        Decorador para validar apenas o access token ou API Key, sem verificar permissões adicionais.
        O access token é validado pela url do introspect
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                
                try:
                    
                    access_token = request.headers.get(self._access_token_header)
                    apikey = request.headers.get(self._api_key_header)

                    if not access_token and not apikey:
                        raise MissingAuthorizationHeader("Missing authorization or X-API-KEY header")

                    # Chama o método de validação que agora lida com ambos
                    self._fast_access_token_or_apikey(access_token=access_token, apikey=apikey)

                    return func(*args, **kwargs)
                
                except Forbidden as e:
                    return self._format_erro(403, f"{e}")
                except MissingAuthorizationHeader as e:
                    return self._format_erro(401, f"{e}")
                except Unauthorized as e:
                    return self._format_erro(401, f"{e}")
                except Exception as e:
                    self._logger.exception(
                        f"Erro na autenticação/autorização. Mensagem: {e}")
                    return self._format_erro(500, f"{e}")

            return wrapper
        
        return decorator
