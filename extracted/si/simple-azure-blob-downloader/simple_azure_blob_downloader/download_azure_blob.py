import argparse
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential


def _download(blob_endpoint=None, container=None, blob=None, output_file=None):
    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=blob_endpoint, credential=credential)
    blob = service.get_blob_client(container, blob)
    with open(output_file, 'wb') as f:
        blob.download_blob().readinto(f)


def main():
    parser = argparse.ArgumentParser(description="Download a blob from Azure, to a file.")
    parser.add_argument("--blob-endpoint", required=True)
    parser.add_argument("--container", required=True)
    parser.add_argument("--blob", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()
    _download(blob_endpoint=args.blob_endpoint, container=args.container, blob=args.blob, output_file=args.output_file)
