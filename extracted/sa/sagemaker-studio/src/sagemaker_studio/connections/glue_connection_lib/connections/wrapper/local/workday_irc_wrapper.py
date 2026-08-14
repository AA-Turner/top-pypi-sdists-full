"""
Workday IRC Connection Wrapper Implementation.
"""

import time
import uuid
from typing import Any, Dict

import requests  # type: ignore[import-untyped]

from .native_wrapper import NativeConnectionWrapper


class WorkdayIcebergRestCatalogConnectionWrapper(NativeConnectionWrapper):
    """
    Workday Iceberg REST catalog connection wrapper that extends native wrapper functionality.
    """

    def get_catalog_configs(self) -> Dict[str, Any]:
        """Get connection with resolved workday IRC spark properties."""
        # Get the base resolved connection
        options = {}
        options["INSTANCE_URL"] = self._connection["ConnectionProperties"]["INSTANCE_URL"]
        options["SOURCE_CATALOG_LIST"] = self._connection["ConnectionProperties"][
            "SOURCE_CATALOG_LIST"
        ]
        options["TENANT_ID"] = self._connection["ConnectionProperties"]["TENANT_ID"]
        options["CLIENT_ID"] = self._connection["AuthenticationConfiguration"]["OAuth2Properties"][
            "OAuth2ClientApplication"
        ]["UserManagedClientApplicationClientId"]
        options["TOKEN_URL"] = self._connection["AuthenticationConfiguration"]["OAuth2Properties"][
            "TokenUrl"
        ]
        options["SCOPE"] = self._connection["AuthenticationConfiguration"]["OAuth2Properties"].get(
            "Scope", "PRINCIPAL_ROLE:ALL"
        )
        secretId = self._connection["AuthenticationConfiguration"]["SecretArn"]
        secret_options = self._get_secret_options_from_secret_manager(secretId)
        options["USERNAME"] = secret_options["USERNAME"]
        options["PRIVATE_KEY_PEM"] = secret_options["PRIVATE_KEY_PEM"]

        options = self._get_access_token(options)

        return options

    def _get_access_token(self, options_map: Dict[str, Any]) -> Dict[str, Any]:
        """Obtain access token from Workday via JWT Bearer grant."""
        # Imported here so that consumers of other connection types don't pay the
        # cost of loading PyJWT's `cryptography` backend just to build a wrapper.
        import jwt

        now = int(time.time())
        claims = {
            "iss": options_map["CLIENT_ID"],
            "sub": options_map["USERNAME"],
            "aud": options_map["TENANT_ID"],
            "exp": now + 300,
            "iat": now,
            "jti": str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(claims, options_map["PRIVATE_KEY_PEM"], algorithm="RS256")

        resp = requests.post(
            options_map["TOKEN_URL"],
            headers={
                "Authorization": "PLACE_HOLDER_FOR_NOW",
                "Polaris-Realm": options_map["TENANT_ID"],
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                "subject_token": jwt_token,
                "client_id": options_map["CLIENT_ID"],
                "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
                "scope": options_map["SCOPE"],
            },
        )
        if resp.status_code != 200:
            raise Exception(f"Token request failed: {resp.status_code} {resp.text}")

        options_map["ACCESS_TOKEN"] = resp.json()["access_token"]
        return options_map
