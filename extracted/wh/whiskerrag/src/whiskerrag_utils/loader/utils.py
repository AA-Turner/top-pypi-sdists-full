import os
import tempfile
from typing import Tuple

import boto3  # type: ignore
import requests  # type: ignore
from botocore.client import Config  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from whiskerrag_types.model.knowledge_source import S3SourceConfig

_MAX_FILE_SIZE = 250 * 1024 * 1024


def download_from_s3_to_local(config: S3SourceConfig) -> Tuple[str, dict]:
    """download s3 to tempdir"""
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"s3_{os.urandom(8).hex()}")

    try:
        s3_client = boto3.client(
            "s3",
            region_name=config.region,
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            aws_session_token=config.auth_info,
            config=Config(signature_version="s3v4"),
        )

        kwargs = {"Bucket": config.bucket, "Key": config.key}
        if config.version_id:
            kwargs["VersionId"] = config.version_id

        head_response = s3_client.head_object(**kwargs)
        file_size = head_response["ContentLength"]

        if file_size > _MAX_FILE_SIZE:
            raise Exception(f"File size exceeds limit of {_MAX_FILE_SIZE} bytes")

        with open(temp_file, "wb") as f:
            response = s3_client.get_object(**kwargs)
            for chunk in response["Body"].iter_chunks(chunk_size=8192):
                f.write(chunk)

        file_info = {
            "content_type": head_response.get("ContentType"),
            "content_length": file_size,
            "last_modified": head_response["LastModified"].isoformat(),
            "etag": head_response["ETag"],
        }
        return temp_file, file_info

    except ClientError as e:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        raise Exception(f"Failed to download from S3: {str(e)}")
    except Exception as e:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        raise Exception(f"Error processing S3 file: {str(e)}")


def download_from_url_to_local(url: str) -> Tuple[str, dict]:
    """
    下载文件到本地临时目录
    增加从响应头中获取文件信息
    """
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"download_{os.urandom(8).hex()}")

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            # 从响应头获取文件信息
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) > _MAX_FILE_SIZE:
                raise Exception(f"File size exceeds limit of {_MAX_FILE_SIZE} bytes")
            content_disposition = response.headers.get("content-disposition")
            original_filename = None
            if content_disposition:
                import re

                matches = re.findall(
                    r"filename\*?=['\"]*([^'\";\n]*)", content_disposition
                )
                if matches:
                    original_filename = matches[0]

            with open(temp_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            file_size = os.path.getsize(temp_file)

            file_metadata = {
                "content_type": response.headers.get("content-type"),
                "content_length": file_size,
                "last_modified": response.headers.get("last-modified"),
                "etag": response.headers.get("etag"),
                "original_filename": original_filename,
                "content_encoding": response.headers.get("content-encoding"),
            }

            file_metadata = {k: v for k, v in file_metadata.items() if v is not None}

            return temp_file, file_metadata

    except Exception as e:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        raise Exception(f"Failed to download file from URL: {str(e)}")
