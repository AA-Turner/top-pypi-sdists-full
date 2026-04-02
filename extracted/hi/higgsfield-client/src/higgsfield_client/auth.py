import os

from higgsfield_client.exceptions import CredentialsMissedError


def get_credential_key() -> str:
    key = os.getenv('HF_KEY')

    if key:
        return key

    api_key = os.getenv('HF_API_KEY')
    api_secret = os.getenv('HF_API_SECRET')

    if api_key and api_secret:
        return f'{api_key}:{api_secret}'

    raise CredentialsMissedError(
        'Higgsfield API credentials missing. Please set HF_KEY, or '
        'alternatively set HF_API_KEY and HF_API_SECRET.'
    )
