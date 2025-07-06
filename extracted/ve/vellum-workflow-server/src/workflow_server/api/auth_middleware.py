import json
from typing import Any, Dict

from flask import Flask, Request, Response
import jwt
from jwt import ExpiredSignatureError

from workflow_server.config import IS_VPC, NAMESPACE, VEMBDA_PUBLIC_KEY, is_development


class AuthMiddleware:
    def __init__(self, app: Flask) -> None:
        self.app = app

    def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
        try:
            request = Request(environ)
            if not request.path.startswith("/healthz") and not is_development() and not IS_VPC:
                token = request.headers.get("X-Vembda-Signature")
                if token:
                    decoded = jwt.decode(token, VEMBDA_PUBLIC_KEY, algorithms=["RS256"])

                    # Validate that the signature's namespace matches our services namespace. We need to do
                    # this because otherwise you could simply use your signature on someone else's service
                    # if you manage to get past the networking policies.
                    token_namespace = decoded.get("namespace")

                    if decoded.get("namespace") != NAMESPACE:
                        res = Response(
                            json.dumps(
                                {
                                    "detail": f"Token namespace '{token_namespace}' "
                                    f"does not match service namespace '{NAMESPACE}'"
                                }
                            ),
                            mimetype="application/json",
                            status=401,
                        )
                        return res(environ, start_response)
                else:
                    res = Response(json.dumps({"detail": "Signature missing"}), mimetype="application/json", status=401)
                    return res(environ, start_response)

        except ExpiredSignatureError:
            res = Response(
                json.dumps({"detail": "Signature token has expired. Please obtain a new token."}),
                mimetype="application/json",
                status=401,
            )
            return res(environ, start_response)
        except Exception as e:
            res = Response(
                json.dumps({"detail": f"Invalid signature token {str(e)}"}), mimetype="application/json", status=401
            )
            return res(environ, start_response)

        return self.app(environ, start_response)
