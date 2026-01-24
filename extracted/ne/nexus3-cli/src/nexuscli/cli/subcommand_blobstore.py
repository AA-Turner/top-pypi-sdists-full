import json

from nexuscli import exception, NexusClient
from nexuscli.api.blobstore import Blobstore
from nexuscli.cli import util


def cmd_list(nexus_client: NexusClient, **kwargs):
    """Performs `nexus3 blobstore list`"""
    if kwargs.get('json'):
        print(json.dumps(nexus_client.blobstores.list))
    else:
        util.print_as_table(nexus_client.blobstores.list, ['name', 'type', 'totalSizeInBytes'])


def cmd_show(nexus_client: NexusClient, name):
    """Performs `nexus3 blobstore show`"""
    blobstore = nexus_client.blobstores.get_by_name(name)
    print(json.dumps(blobstore.configuration))


def cmd_delete(nexus_client: NexusClient, name):
    nexus_client.blobstores.delete(name)


def _cmd_create_params(blobstore_params: dict, kwargs: dict):
    if kwargs.get('quota_type') or kwargs.get('quota_limit'):  # let the API deal with validation
        blobstore_params['softQuota'] = {
            'limit': kwargs.get('quota_limit'),
            'type': kwargs.get('quota_type'),
        }


def _cmd_create_params_s3(blobstore_params: dict, kwargs: dict):
    s3_params = {
        'bucketConfiguration': {
            'bucket': {
                'region': kwargs['bucket_region'],
                'name': kwargs['bucket_name'],
                'prefix': kwargs.get('bucket_prefix'),
                'expiration': kwargs.get('bucket_expiration') or 0,
            },
            'encryption': {
                'encryptionType': kwargs.get('encryption_type') or Blobstore.ENCRYPTION_TYPES[0],
                'encryptionKey': kwargs.get('encryption_key'),
            },
            'bucketSecurity': {
                'accessKeyId': kwargs['key_id'],
                'secretAccessKey': kwargs['secret_key'],
                'role': kwargs.get('role'),
                'sessionToken': kwargs.get('session_token'),
            },
            # TODO:
            # 'advancedBucketConnection': {
            #     'endpoint': 'string',
            #     'signerType': 'string',
            #     'forcePathStyle': True
            # }
        }
    }
    blobstore_params.update(s3_params)


def cmd_create(nexus_client: NexusClient, blob_type, name, **kwargs):
    """Performs `nexus3 blobstore create`"""
    blobstore_params = {'name': name, 'type': blob_type}
    _cmd_create_params(blobstore_params, kwargs)

    if blob_type.lower() == 'file':
        blobstore_params['path'] = kwargs.get('path')
    elif blob_type.lower() == 's3':
        _cmd_create_params_s3(blobstore_params, kwargs)

    try:
        blobstore = Blobstore(nexus_http=nexus_client.http, **blobstore_params)
    except ValueError as e:
        raise exception.ConfigError(str(e))

    nexus_client.blobstores.create(blobstore)
