import argparse
from google.cloud import storage


def _download(bucket=None, obj=None, output_file=None):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(obj)
    blob.download_to_filename(output_file)

def main():
    parser = argparse.ArgumentParser(description="Download an object from Google Cloud Storage, to a file.")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--object", required=True)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()
    _download(bucket=args.bucket, obj=args.object, output_file=args.output_file)
