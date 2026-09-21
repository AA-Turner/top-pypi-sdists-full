from __future__ import absolute_import

import base64
import datetime
import hashlib
import hmac
import json
import os
from urllib.error import URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


_ALIBABA_DEFAULT_REGION = "cn-hangzhou"
_ALIBABA_STS_DOMAIN = "sts.aliyuncs.com"
_ALIBABA_STS_API_VERSION = "2015-04-01"
_ALIBABA_STS_API_ACTION = "GetCallerIdentity"
_ALIBABA_STS_API_FORMAT = "JSON"
_ALIBABA_SIGNATURE_METHOD = "HMAC-SHA1"
_ALIBABA_ECS_METADATA_TOKEN_URL = "http://100.100.100.200/latest/api/token"
_ALIBABA_ECS_ROLE_URL = "http://100.100.100.200/latest/meta-data/ram/security-credentials/"
_ALIBABA_ECS_METADATA_TOKEN_TTL_SECONDS = "21600"
_ALIBABA_RAM_ROLE_NAME_ALLOWED = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+=,.@_-"
)


def _alibaba_query_escape(value):
    return (
        quote_plus(str(value), safe="-._~")
        .replace("+", "%20")
        .replace("*", "%2A")
        .replace("%7E", "~")
    )


def _alibaba_encode_query_params(params):
    return "&".join(
        "{}={}".format(_alibaba_query_escape(key), _alibaba_query_escape(params[key]))
        for key in sorted(params)
    )


def _alibaba_rpc_string_to_sign(method, query_params):
    encoded = _alibaba_encode_query_params(query_params)
    return method + "&%2F&" + _alibaba_query_escape(encoded)


def _alibaba_sha_hmac1(source, secret):
    digest = hmac.new(secret.encode("utf-8"), source.encode("utf-8"), hashlib.sha1).digest()
    return base64.b64encode(digest).decode()


def _resolve_alibaba_region():
    for key in ("ALIBABA_CLOUD_REGION_ID", "ALIBABA_CLOUD_REGION", "REGION_ID"):
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return ""


def _resolve_alibaba_credentials():
    access_key_id = (os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID") or os.environ.get("ALICLOUD_ACCESS_KEY") or "").strip()
    access_key_secret = (os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET") or os.environ.get("ALICLOUD_SECRET_KEY") or "").strip()
    security_token = (os.environ.get("ALIBABA_CLOUD_SECURITY_TOKEN") or os.environ.get("ALICLOUD_SECURITY_TOKEN") or "").strip()
    if access_key_id and access_key_secret:
        return access_key_id, access_key_secret, security_token
    return _resolve_alibaba_ecs_ram_role()


def _alibaba_imdsv1_disabled():
    return os.environ.get("ALIBABA_CLOUD_IMDSV1_DISABLED", "").strip().lower() in ("1", "true", "yes")


def _alibaba_ecs_open(url, method="GET", headers=None):
    request = Request(url, method=method, headers=headers or {})
    return urlopen(request, timeout=2).read().decode("utf-8")


def _alibaba_ecs_metadata_token():
    token = _alibaba_ecs_open(
        _ALIBABA_ECS_METADATA_TOKEN_URL,
        method="PUT",
        headers={"X-aliyun-ecs-metadata-token-ttl-seconds": _ALIBABA_ECS_METADATA_TOKEN_TTL_SECONDS},
    ).strip()
    if not token:
        raise ValueError("alibaba ecs metadata token is empty")
    return token


def _alibaba_ecs_get(url, token=""):
    headers = {}
    if token:
        headers["X-aliyun-ecs-metadata-token"] = token
    return _alibaba_ecs_open(url, headers=headers)


def _alibaba_valid_ram_role_name(role_name):
    return bool(role_name) and all(ch in _ALIBABA_RAM_ROLE_NAME_ALLOWED for ch in role_name)


def _resolve_alibaba_ecs_ram_role():
    token = ""
    try:
        token = _alibaba_ecs_metadata_token()
    except (URLError, OSError, ValueError):
        if _alibaba_imdsv1_disabled():
            raise
    role_name = _alibaba_ecs_get(_ALIBABA_ECS_ROLE_URL, token).strip()
    if not _alibaba_valid_ram_role_name(role_name):
        raise ValueError("alibaba credentials are missing access key id or secret")
    creds = json.loads(_alibaba_ecs_get(_ALIBABA_ECS_ROLE_URL + role_name, token))
    return creds.get("AccessKeyId", ""), creds.get("AccessKeySecret", ""), creds.get("SecurityToken", "")


# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


class CloudId:
    def generateAzure(self, object_id=""):
        from azure.identity import DefaultAzureCredential
            
        credential = DefaultAzureCredential()
            
        scope = "https://management.azure.com/.default"
        token = credential.get_token(scope)
        
        cloud_id = base64.b64encode(token.token.encode()).decode()
        return cloud_id

    def generateGcp(self, audience="akeyless.io"):
        import google.auth.transport.requests
        from google.oauth2 import id_token

        request = google.auth.transport.requests.Request()
        
        # Fetch ID token using default credentials
        # This automatically handles service accounts and compute engine
        token = id_token.fetch_id_token(request, audience)
        
        cloud_id = base64.b64encode(token.encode()).decode()
        return cloud_id

    def generateAlibaba(self, access_key_id="", access_key_secret="", security_token="", region="",
                        timestamp="", nonce=""):
        if not access_key_id or not access_key_secret:
            access_key_id, access_key_secret, security_token = _resolve_alibaba_credentials()
        if not region:
            region = _resolve_alibaba_region() or _ALIBABA_DEFAULT_REGION
        if not timestamp:
            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        if not nonce:
            nonce = hashlib.sha1(os.urandom(16)).hexdigest()

        if not access_key_id or not access_key_secret:
            raise ValueError("alibaba credentials are missing access key id or secret")

        query_params = {
            "AccessKeyId": access_key_id,
            "Action": _ALIBABA_STS_API_ACTION,
            "Format": _ALIBABA_STS_API_FORMAT,
            "RegionId": region,
            "SignatureMethod": _ALIBABA_SIGNATURE_METHOD,
            "SignatureNonce": nonce,
            "SignatureType": "",
            "SignatureVersion": "1.0",
            "Timestamp": timestamp,
            "Version": _ALIBABA_STS_API_VERSION,
        }
        if security_token:
            query_params["SecurityToken"] = security_token

        string_to_sign = _alibaba_rpc_string_to_sign("POST", query_params)
        query_params["Signature"] = _alibaba_sha_hmac1(string_to_sign, access_key_secret + "&")

        request_url = "https://{}/?{}".format(_ALIBABA_STS_DOMAIN, _alibaba_encode_query_params(query_params))
        headers = {
            "Content-Type": ["application/x-www-form-urlencoded"],
            "X-Acs-Action": [_ALIBABA_STS_API_ACTION],
            "X-Acs-Version": [_ALIBABA_STS_API_VERSION],
        }
        alibaba_data = {
            "sts_request_method": "POST",
            "sts_request_url": base64.b64encode(request_url.encode("utf-8")).decode(),
            "sts_request_body": base64.b64encode(b"").decode(),
            "sts_request_headers": base64.b64encode(json.dumps(headers).encode()).decode(),
        }
        return base64.b64encode(json.dumps(alibaba_data).encode()).decode()

    def generate(self, aws_access_id="", aws_secret_access_key="", security_token=""):
        import boto3

        algorithm = 'AWS4-HMAC-SHA256'
        service = "sts"
        region = "us-east-1"
        method = 'POST'
        host = 'sts.amazonaws.com'
        content_type = 'application/x-www-form-urlencoded; charset=utf-8'
        body = 'Action=GetCallerIdentity&Version=2011-06-15'

        if not aws_access_id or not aws_secret_access_key or not security_token:
            session = boto3.session.Session()
            credentials = session.get_credentials()
            aws_access_id = credentials.access_key
            aws_secret_access_key = credentials.secret_key
            security_token = credentials.token

        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')
        raw_query = ''

        credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'

        canonical_uri = '/'
        signed_headers = 'content-length;content-type;host;x-amz-date;x-amz-security-token'

        body_digest = hashlib.sha256((body).encode('utf-8')).hexdigest()
        canonical_headers = 'content-length:{}\ncontent-type:{}\nhost:{}\nx-amz-date:{}\nx-amz-security-token:{}\n'.format(
            len(body), content_type, host, amzdate, security_token)
        canonical_request = method + '\n' + canonical_uri + '\n' + raw_query + \
            '\n' + canonical_headers + '\n' + signed_headers + '\n' + body_digest
        canonical_header_hash = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + \
            '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        # Create the signing key using the function defined above.
        signing_key = getSignatureKey(aws_secret_access_key, datestamp, region, service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode(
            'utf-8'), hashlib.sha256).hexdigest()

        auth = '{} Credential={}/{},  SignedHeaders={}, Signature={}'.format(
            algorithm, aws_access_id, credential_scope, signed_headers, signature)
        headers = {}
        headers['Authorization'] = [auth]
        headers['Content-Length'] = [str(len(body))]
        headers['Content-Type'] = [content_type]
        headers['User-Agent'] = ['aws-sdk-python']
        headers['X-Amz-Date'] = [amzdate]
        headers['X-Amz-Security-Token'] = [security_token]

        headersJson = json.dumps(headers)
        awsData = {}
        awsData['sts_request_method'] = method
        awsData['sts_request_url'] = base64.b64encode(
            b'https://sts.amazonaws.com/').decode()  # string representation of base64
        awsData['sts_request_body'] = base64.b64encode(
            body.encode('utf-8')).decode()  # string representation of base64
        awsData['sts_request_headers'] = base64.b64encode(
            headersJson.encode()).decode()  # string representation of base64

        awsDump = json.dumps(awsData)
        cloud_id = base64.b64encode(awsDump.encode()).decode()  # string representation of base64

        return cloud_id
