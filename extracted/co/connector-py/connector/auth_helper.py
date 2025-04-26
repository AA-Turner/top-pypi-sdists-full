from urllib.parse import parse_qs, urljoin, urlparse

from connector.generated.models.handle_authorization_callback_request import (
    HandleAuthorizationCallbackRequest,
)


def parse_auth_code_and_redirect_uri(args: HandleAuthorizationCallbackRequest):
    redirect_uri_with_code = args.request.redirect_uri_with_code
    parsed_uri = urlparse(redirect_uri_with_code)
    base_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
    path = parsed_uri.path
    original_redirect_uri = urljoin(base_url, path)
    query_params = parse_qs(parsed_uri.query)
    authorization_code = query_params.get("code", [None])[0]

    return authorization_code, original_redirect_uri
