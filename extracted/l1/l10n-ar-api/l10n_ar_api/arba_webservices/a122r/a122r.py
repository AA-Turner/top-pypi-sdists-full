# coding=utf-8

import requests
from . import config


class A122RApiClient:
    """Cliente stateless para la API A122R de ARBA."""

    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

    @staticmethod
    def get_base_url(environment):
        return config.BASE_URLS.get(environment, config.BASE_URLS['test'])

    @staticmethod
    def get_oauth_token(cuit, cit, environment='prod'):
        """Obtiene access token via OAuth 2.0 Password Grant.

        Returns:
            dict con 'access_token' y 'expires_in' (segundos).
        """
        token_url = config.TOKEN_URLS.get(environment, config.TOKEN_URLS['prod'])
        client_id = config.CLIENT_IDS.get(environment, config.CLIENT_IDS['prod'])
        client_secret = config.CLIENT_SECRETS.get(environment, config.CLIENT_SECRETS['prod'])
        data = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': cuit,
            'password': cit,
            'scope': 'openid',
        }
        response = requests.post(
            token_url, data=data, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def create_ddjj(self, cuit, quincena, actividad_id, anio, mes):
        """POST /external/declaracionJurada - Iniciar DDJJ.

        Returns:
            dict con datos de la DJ creada (incluyendo ID).
        """
        url = f"{self.base_url}/external/declaracionJurada"
        payload = {
            'cuitAgente': cuit,
            'quincena': int(quincena),
            'actividadId': int(actividad_id),
            'anio': int(anio),
            'mes': int(mes),
        }
        response = requests.post(
            url, json=payload, headers=self.headers, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def add_comprobante(self, payload):
        """POST /external/comprobante - Alta de comprobante de retención.

        Args:
            payload: dict con campos del comprobante.

        Returns:
            dict con datos del comprobante creado (incluyendo ID).
        """
        url = f"{self.base_url}/external/comprobante"
        response = requests.post(
            url, json=payload, headers=self.headers, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def delete_comprobante(self, comprobante_id):
        """DELETE /external/comprobante/{id} - Baja de comprobante."""
        url = f"{self.base_url}/external/comprobante/{comprobante_id}"
        response = requests.delete(
            url, headers=self.headers, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.json() if response.content else {}

    def get_comprobante_pdf(self, comprobante_id):
        """GET /external/comprobantePdf - Descargar PDF del comprobante.

        Returns:
            bytes con el contenido del PDF.
        """
        url = f"{self.base_url}/external/comprobantePdf"
        params = {'id': int(comprobante_id)}
        headers = {
            'Authorization': self.headers['Authorization'],
            'Accept': 'application/pdf',
        }
        response = requests.get(
            url, params=params, headers=headers, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.content

    def query_ddjj(self, **filters):
        """GET /external/declaracionJurada - Consultar DJ.

        Args:
            **filters: idDj, cuitAgente, actividadId, anio, mes, quincena.
        """
        url = f"{self.base_url}/external/declaracionJurada"
        response = requests.get(
            url, params=filters, headers=self.headers, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.json()
