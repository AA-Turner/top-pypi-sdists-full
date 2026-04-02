import datetime
import requests

from nsj_queue_lib.settings import (
    MULTI_DATABASE_USER,
    MULTI_DATABASE_PASSWORD,
    MULTI_DATABASE_CLIENT_ID,
    MULTI_DATABASE_API_CREDETIALS_URL,
    OAUTH_TOKEN_URL,
)


class TokenStore:
    instance: "TokenStore" = None

    tokens: dict[str, dict[str, any]]

    def __init__(self):
        self.tokens = {}

    @staticmethod
    def get_instance() -> "TokenStore":
        if not TokenStore.instance:
            TokenStore.instance = TokenStore()
        return TokenStore.instance


class MultiDatabaseClient:
    def __init__(self):
        self.url = MULTI_DATABASE_API_CREDETIALS_URL
        self.token = self.get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _call_oauth_api(self, auth_url, auth_payload, headers):
        try:
            response = requests.post(auth_url, data=auth_payload, headers=headers)
            response.raise_for_status()
            token = response.json()

            # Calcula a data de expiração do token (descontando 10 segundos para evitar problemas de sincronização)
            token[
                "expires_in_date_time"
            ] = datetime.datetime.now() + datetime.timedelta(
                seconds=(token["expires_in"] - 10)
            )

            # Calcula a data de expiração do refresh_token (descontando 10 segundos para evitar problemas de sincronização)
            token[
                "refresh_token_expires_in_date_time"
            ] = datetime.datetime.now() + datetime.timedelta(
                seconds=(token["refresh_expires_in"] - 10)
            )

            return token
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Erro ao recuperar o token para chamada à API multibanco: {e}"
            )

    def _retrieve_token(self):
        auth_url = OAUTH_TOKEN_URL
        auth_payload = {
            "username": MULTI_DATABASE_USER,
            "password": MULTI_DATABASE_PASSWORD,
            "client_id": MULTI_DATABASE_CLIENT_ID,
            "scope": "offline_access",
            "grant_type": "password",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self._call_oauth_api(auth_url, auth_payload, headers)

    def _renew_token(self, refresh_token: str):
        auth_url = OAUTH_TOKEN_URL
        auth_payload = {
            "refresh_token": refresh_token,
            "client_id": MULTI_DATABASE_CLIENT_ID,
            "scope": "offline_access",
            "grant_type": "refresh_token",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        return self._call_oauth_api(auth_url, auth_payload, headers)

    def get_token(self):
        if MULTI_DATABASE_USER in TokenStore.get_instance().tokens:
            token = TokenStore.get_instance().tokens[MULTI_DATABASE_USER]

            # Verifica se o token venceu
            if token["expires_in_date_time"] <= datetime.datetime.now():
                # Verifica se o refresh_token venceu
                if (
                    token["refresh_token_expires_in_date_time"]
                    <= datetime.datetime.now()
                ):
                    # Se venceu, refaz todo o processo
                    token = self._retrieve_token()
                else:
                    # Se não venceu, renova o token
                    token = self._renew_token(token["refresh_token"])
        else:
            # Se não achou o token, recupera um do zero
            token = self._retrieve_token()

        TokenStore.get_instance().tokens[MULTI_DATABASE_USER] = token
        return token["access_token"]

    def get_erp_credentials(self, tenant):
        payload = {"tenant": tenant}
        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()  # Levanta um erro para respostas com status 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao chamar a API: {e}")


if __name__ == "__main__":
    client = MultiDatabaseClient()
    credentials = client.get_erp_credentials(tenant=47)
    if credentials:
        print("Resposta da API:", credentials)

    print("------------")

    credentials = client.get_erp_credentials(tenant=47)
    if credentials:
        print("Resposta da API:", credentials)

    print("------------")

    token = client._renew_token(
        TokenStore.get_instance().tokens[MULTI_DATABASE_USER]["refresh_token"]
    )
    print("Token renovado:", token)
