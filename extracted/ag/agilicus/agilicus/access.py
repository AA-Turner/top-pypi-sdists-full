import json
from datetime import datetime
from datetime import timedelta

import jwt
import requests
from oauth2client.client import Credentials

from . import context, credentials, response, tokens


def is_token_expired(token, expiry_threshold_min=2):
    try:
        payload = jwt.decode(
            token,
            algorithms=["ES256"],
            options={"verify_signature": False},
            leeway=60,
        )
    except jwt.ExpiredSignatureError:
        return True

    if "exp" not in payload:
        return True

    expiry = datetime.utcfromtimestamp(payload.get("exp"))
    return (expiry - datetime.utcnow()) < timedelta(minutes=expiry_threshold_min)


class TokenStore(Credentials):
    def __init__(self, data=None):
        self.valid = True
        if data:
            self.data = data
        else:
            self.data = {}
            self.data["_module"] = "agilicus.access"
            self.data["_class"] = "TokenStore"
        self.token_cache = {}

    def set_store(self, store):
        self.store = store

    def set_ctx(self, ctx):
        self.ctx = ctx

    def set_id_token(self, id_token):
        self.id_token = id_token

    def set_root_token(self, root_token):
        self.root_token = root_token

    @classmethod
    def from_json(self, json_data):
        data = json.loads(json_data)
        return self(data)

    def _to_json(self, strip, to_serialize=None):
        return json.dumps(self.data)

    def add(self, org_id, token):
        self.data[org_id] = token
        self.store.put(self)

    def get(self, org_id, force=False, original_token=None):
        token = self.token_cache.get(org_id, None)
        if token:
            return token

        token = self.data.get(org_id, None)

        if token and is_token_expired(token):
            # expired, get a new token
            token = None

        if original_token is None:
            raise Exception("cannot switch orgs without root token")

        if token is None:
            token = self.request_token(org_id)
            self.add(org_id, token)
            self.token_cache[org_id] = token
            return token
        return token

    def request_token(self, org_id):
        headers = {}
        headers["Content-type"] = "application/json"
        post_data = {}
        post_data["id_token"] = self.id_token
        post_data["org_id"] = org_id

        return tokens.reissue_token(self.ctx, org_id, self.root_token)


class AccessToken:
    def __init__(self, ctx, crd):
        self.valid = True
        self.data = json.loads(crd.to_json())
        self.ctx = ctx
        self.store = credentials.get_store_from_ctx(self.ctx, token=True)
        self.token_store = self.store.get()
        if not self.token_store:
            self.token_store = TokenStore()
        self.token_store.set_store(self.store)
        self.token_store.set_ctx(ctx)
        self.token_store.set_id_token(self.data["token_response"]["id_token"])
        access_token = self.data["access_token"]
        self.token_store.set_root_token(access_token)

        try:
            self.token_payload = jwt.decode(
                access_token,
                algorithms=["ES256"],
                options={"verify_signature": False},
                leeway=60,
            )
        except jwt.ExpiredSignatureError:
            self.token_payload = {}

    def get_token_for_org(self, org_id):
        if org_id is None or org_id == self.token_payload.get("org", None):
            return self.data["access_token"]

        return self.token_store.get(org_id, original_token=self.data.get("access_token"))

    def get(self, org_id=None):
        if org_id is not None:
            self.get_token_for_org(org_id)

        org_id = context.get_org_id(self.ctx)
        return self.get_token_for_org(org_id)

    def get_id_token(self):
        return self.data["token_response"]["id_token"]

    def scopes(self):
        resp = self.introspect_token()
        if not resp:
            return []
        return resp.get("scopes", [])

    def introspect_token(self):
        access_token = self.data.get("access_token")
        if not access_token:
            return None

        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"bearer {access_token}"

        resp = requests.get(
            context.get_api(self.ctx) + "/v1/tokens/introspect_self",
            headers=headers,
            verify=context.get_cacert(self.ctx),
        )
        response.validate(resp)
        return resp.json()


def get_access_token(ctx, org_id=None, refresh=None):
    token = AccessToken(ctx, credentials.get_credentials_from_ctx(ctx, refresh))
    if _need_new_token(ctx, token):
        credentials.delete_credentials_with_ctx(ctx)
        token = AccessToken(ctx, credentials.get_credentials_from_ctx(ctx, refresh))

    return token


def _need_new_token(ctx, token):
    try:
        current_scopes = _get_agilicus_scopes(token.scopes())
    except Exception as exc:
        print(f"failed to retreive scopes {exc}. Using existing set")
        return False

    new_scopes = _get_agilicus_scopes(context.get_scopes(ctx))
    diff = new_scopes.symmetric_difference(current_scopes)
    if diff:
        # scopes have changed. Need a new one
        return True

    return False


def _get_agilicus_scopes(scopes):
    return {scope for scope in scopes if scope.startswith("urn:agilicus")}
