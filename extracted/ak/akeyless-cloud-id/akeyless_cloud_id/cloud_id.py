from __future__ import absolute_import

import base64
import datetime
import hashlib
import hmac
import json
import requests


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
        from google.auth import compute_engine
        import google.auth.transport.requests

        request = google.auth.transport.requests.Request()
        credentials = compute_engine.IDTokenCredentials(
            request=request, target_audience=audience, use_metadata_identity_endpoint=True)
        credentials.refresh(request)
        cloud_id = base64.b64encode(credentials.token.encode()).decode()
        return cloud_id

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
