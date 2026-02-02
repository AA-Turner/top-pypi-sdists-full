from aws_packages.auth.icp.auth_backend import icp_auth_backend
from aws_packages.auth.views import process_authenticate_request


def process_icp_authenticate_request(request_body):
    return process_authenticate_request(request_body, icp_auth_backend)
