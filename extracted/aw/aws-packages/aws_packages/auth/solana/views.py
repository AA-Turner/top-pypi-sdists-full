from aws_packages.auth.solana.auth_backend import solana_auth_backend
from aws_packages.auth.views import process_authenticate_request


def process_solana_authenticate_request(request_body):
    return process_authenticate_request(request_body, solana_auth_backend)
