import click

from nexuscli.api.blobstore import Blobstore

#############################################################################
# blobstore create options
COMMON = [
    click.argument('name'),
    click.option('--quota-type', '-q', help='Enable soft quota of the chosen type',
                 type=click.Choice(Blobstore.QUOTA_TYPES)),
    click.option('--quota-limit', '-l', help='Quota limit in bytes', type=click.INT),
]

S3 = [
    click.option('--bucket-region', '-r', help='AWS region', type=click.STRING, required=True),
    click.option('--bucket-name', '-n', help='S3 bucket name', type=click.STRING, required=True),
    click.option('--key-id', '-k', help='IAM access key ID', type=click.STRING, required=True),
    click.option('--secret-key', '-s', help='Secret for key ID', type=click.STRING, required=True),
    click.option('--bucket-prefix', type=click.STRING),
    click.option('--bucket-expiration', help='Days until deleted blobs are removed',
                 type=click.INT),
    click.option('--encryption-type', '-e', help='S3 encryption',
                 type=click.Choice(Blobstore.ENCRYPTION_TYPES)),
    click.option('--encryption-key', '-E', type=click.STRING),
    click.option('--role', help='IAM role to assume', type=click.STRING),
    click.option('--session-token', help='AWS STS session token for temporary credentials',
                 type=click.STRING),
]
