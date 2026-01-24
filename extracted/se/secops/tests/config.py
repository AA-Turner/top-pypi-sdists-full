"""Test configurations."""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    # Load .env file from project root
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    # dotenv not installed, will use system environment variables
    pass

CHRONICLE_CONFIG = {
    "customer_id": os.getenv("CHRONICLE_CUSTOMER_ID", ""),
    "project_id": os.getenv("CHRONICLE_PROJECT_NUMBER", ""),
    "region": os.getenv("CHRONICLE_REGION", "us"),
}

# Optional - for service account testing
SERVICE_ACCOUNT_JSON = {
    "type": "service_account",
    "project_id": os.getenv("CHRONICLE_PROJECT_NAME", ""),
    "private_key_id": os.getenv("CHRONICLE_PRIVATE_KEY_ID", ""),
    "private_key": os.getenv("CHRONICLE_PRIVATE_KEY", "").replace(
        "\\n", "\n"
    ),  # Handle newlines in env vars
    "client_email": os.getenv("CHRONICLE_CLIENT_EMAIL", ""),
    "client_id": os.getenv("CHRONICLE_CLIENT_ID", ""),
    "auth_uri": os.getenv(
        "CHRONICLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"
    ),
    "token_uri": os.getenv(
        "CHRONICLE_TOKEN_URI", "https://oauth2.googleapis.com/token"
    ),
    "auth_provider_x509_cert_url": os.getenv(
        "CHRONICLE_AUTH_PROVIDER_CERT_URL",
        "https://www.googleapis.com/oauth2/v1/certs",
    ),
    "client_x509_cert_url": os.getenv("CHRONICLE_CLIENT_X509_CERT_URL", ""),
    "universe_domain": os.getenv("CHRONICLE_UNIVERSE_DOMAIN", "googleapis.com"),
}
