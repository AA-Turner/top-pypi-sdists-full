import json
import os

from functools import wraps
from flask import g, request

from nsj_gcf_utils.rest_error_util import format_json_error

from nsj_rest_lib.exception import NotFoundException

from nsj_flask_auth.exceptions import MissingAuthorizationHeader

from nsj_multi_database_lib.exception import ParameterNotFound
from nsj_multi_database_lib.settings import get_logger

from nsj_multi_database_lib.service.database_service import (
    DatabaseService,
    DatabaseValidationException,
)


def multi_database(service_account: str = None):
    """Decorator para resolver dinamicamente as credenciais do tenant.

    Se `service_account` for informado, resolve as credenciais usando esse e-mail
    no lugar do usuário do access token.
    """

    _access_token_header: str = "Authorization"
    _x_api_key_header: str = "X-API-Key"
    _api_key_header: str = "apikey"

    def __get_db_username(db_name: str, erp_login: str):
        return db_name.lower() + "_" + erp_login.lower()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.getenv("ENV") == "local":
                return func(*args, **kwargs)

            try:
                db_service = DatabaseService()

                token = None
                token_type = None

                if request.headers.get(_access_token_header):
                    token = request.headers.get(_access_token_header)
                    token_type = "Authorization"
                elif request.headers.get(_x_api_key_header):
                    token = request.headers.get(_x_api_key_header)
                    token_type = "X-API-Key"
                elif request.headers.get(_api_key_header):
                    token = request.headers.get(_api_key_header)
                    token_type = "X-API-Key"
                else:
                    raise MissingAuthorizationHeader(
                        f"Missing {_access_token_header}, X-API-Key or apikey header"
                    )

                if not token:
                    raise MissingAuthorizationHeader(
                        f"Missing {_access_token_header} header"
                    )

                if token_type == "Authorization" and "bearer " not in token.lower():
                    token = "Bearer " + token

                # Recuperando o tenant da query string, ou do corpo da requisição
                tenant = request.args.get("tenant")
                if tenant is None:
                    try:
                        body = request.get_data(as_text=True).strip()
                        body = json.loads(body)
                        tenant = body["tenant"]
                    except:
                        pass

                if tenant is None:
                    raise ParameterNotFound("tenant")

                tenant = int(tenant)

                # Recuperando os dados do banco pelo tenant
                database = db_service.get_by_tenant(
                    tenant,
                    token=token,
                    token_type=token_type,
                    service_account=service_account,
                )

                # Definindo dados de conexão com o DB no contexto da aplicação
                g.external_database = {
                    "host": database["hostname"],
                    "port": database["port"],
                    "name": database["db_name"],
                    "user": f"{database['user'].lower()}",
                    "password": database["password"],
                }

                return func(*args, **kwargs)
            except (ParameterNotFound, MissingAuthorizationHeader) as e:
                if request.method.upper() == "GET":
                    msg = f"Faltando parâmetro obrigatório na requisição: {e}."
                else:
                    msg = (
                        f"Faltando propriedade obrigatória no corpo da requisição: {e}."
                    )

                get_logger().warning(msg)
                return (
                    format_json_error(msg),
                    400,
                    {"Content-Type": "application/json; charset=utf-8"},
                )
            except DatabaseValidationException as e:
                get_logger().warning(e)
                return (
                    format_json_error(e.args[1]),
                    e.args[0],
                    {"Content-Type": "application/json; charset=utf-8"},
                )
            except NotFoundException as e:
                msg = f"Dados Faltando: {e}."
                get_logger().warning(msg)
                return (
                    format_json_error(msg),
                    412,
                    {"Content-Type": "application/json; charset=utf-8"},
                )
            except Exception as e:
                msg = f"Erro desconhecido: {e}."
                get_logger().exception(msg, e)
                return (
                    format_json_error(msg),
                    500,
                    {"Content-Type": "application/json; charset=utf-8"},
                )

        return wrapper

    return decorator
