import base64
import json
import typing as t


def pad(encoded: str) -> str:
    mod = len(encoded) % 4

    if mod == 2:
        return f"{encoded}=="
    if mod == 3:
        return f"{encoded}="
    return encoded


def jwt_b64decode(data: str) -> str:
    return base64.urlsafe_b64decode(pad(data)).decode("utf-8")


def parse_jwt(token: str) -> t.Tuple[t.Dict, t.Dict, str]:
    [encoded_header, encoded_body, sig] = token.split(".")

    header = jwt_b64decode(encoded_header)
    body = jwt_b64decode(encoded_body)

    return json.loads(header), json.loads(body), sig
