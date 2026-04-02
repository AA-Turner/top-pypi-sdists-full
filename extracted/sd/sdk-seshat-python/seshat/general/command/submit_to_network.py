import hashlib
import os
import pathlib
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Optional, BinaryIO

import boto3
import typer
from botocore.exceptions import ClientError
from dotenv import dotenv_values

from seshat.general.command.base import BaseTyperCommand, ApiConfig, JobMetadata
from seshat.general.exceptions import RestClientException, EnvFileNotFound
from seshat.general.models import CodePackage
from seshat.utils.date_utils import format_datetime_for_api
from seshat.utils.file import is_binary_file
from seshat.utils.file_cryptography import AESCipher
from seshat.utils.jobignore import JobIgnoreHandler
from seshat.utils.logger import get_multi_logger
from seshat.utils.obfuscate import Obfuscator
from seshat.utils.package_utils import add_file_to_package
from seshat.utils.rest import RestClient
from seshat.utils.zip_utils import create_zip_from_files, extract_zip

MAX_PACKAGE_SIZE = 50 * 1024 * 1024
logger = get_multi_logger()


class CodeStorageBackend(ABC):
    @abstractmethod
    def store(self, package: CodePackage) -> str:
        """Store a code package and return its identifier"""
        pass

    @abstractmethod
    def retrieve(self, identifier: str) -> Optional[CodePackage]:
        """Retrieve a code package by its identifier"""
        pass

    @abstractmethod
    def exists(self, identifier: str) -> bool:
        """Check if a package exists"""
        pass


def _create_zip(package: CodePackage) -> BinaryIO:
    """Create a zip file from a CodePackage."""

    metadata = {
        "name": package.name,
        "version": package.version,
        "executor_image_tag": package.executor_image_tag,
        "metadata": package.metadata,
        "hash": package.hash,
    }

    return create_zip_from_files(package.files, package.binary_files, metadata)


def _extract_package(zip_data: BinaryIO) -> CodePackage:
    """Extract a CodePackage from a zip file."""
    extracted = extract_zip(zip_data)

    return CodePackage(
        name=extracted["metadata"]["name"],
        version=extracted["metadata"]["version"],
        executor_image_tag=extracted["metadata"].get("executor_image_tag", "latest"),
        files=extracted["files"],
        metadata=extracted["metadata"]["metadata"],
        hash=extracted["metadata"]["hash"],
        binary_files=extracted["binary_files"],
    )


class S3Backend(CodeStorageBackend):
    def __init__(
        self,
        bucket: str,
        prefix: str = "code",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_region: Optional[str] = None,
    ):
        session_kwargs = {}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs.update(
                {
                    "aws_access_key_id": aws_access_key_id,
                    "aws_secret_access_key": aws_secret_access_key,
                }
            )
        if aws_region:
            session_kwargs["region_name"] = aws_region

        session = boto3.Session(**session_kwargs)
        self.s3 = session.client("s3")
        self.bucket = bucket
        self.prefix = prefix

    def store(self, package: CodePackage) -> str:
        zip_data = _create_zip(package)

        key = f"{self.prefix}/{package.hash}.zip"
        try:
            self.s3.upload_fileobj(zip_data, self.bucket, key)
            return key
        except ClientError as e:
            logger.error(f"Failed to store in S3: {e}")
            raise

    def retrieve(self, identifier: str) -> Optional[CodePackage]:
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=identifier)
            return _extract_package(response["Body"])
        except ClientError as e:
            logger.error(f"Failed to retrieve from S3: {e}")
            return None

    def exists(self, identifier: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key=identifier)
            return True
        except ClientError:
            return False

    def generate_presigned_url(self, key: str, expiration: int = 86400) -> str:
        """Generate a pre-signed URL that expires in specified seconds (default 24 hours)"""
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expiration,
            )
            return url
        except Exception as e:
            logger.error(f"Failed to generate pre-signed URL: {e}")
            raise


class SubmitCommand(BaseTyperCommand):
    ctx: dict

    def __init__(self, config, report=True):
        super().__init__(report)

        self.config = config
        self.report = report

        self.ignore_file = config.get("code", {}).get("ignore_file", ".jobignore")

        self.backend = S3Backend(
            config["aws"]["bucket"],
            config["aws"]["prefix"],
            config["aws"]["access_key_id"],
            config["aws"]["secret_access_key"],
            config["aws"]["region"],
        )

        try:
            self.job_config = ApiConfig(
                base_url=config.get("api", {}).get("base_url"),
                auth_token=config.get("api", {}).get("auth_token"),
            )
        except ValueError as e:
            typer.echo(
                "❌ base_url and auth_token parameters must be set in the config file"
            )
            raise ValueError(str(e))

        self.rest_client = RestClient(
            base_url=self.job_config.base_url,
            timeout=30,
            max_retries=5,
            retry_delay=1,
            headers={
                "Authorization": f"Bearer {self.job_config.auth_token}",
                "Content-Type": "application/json",
            },
        )

        self.obfuscator = Obfuscator(echo_func=self.echo)

    @staticmethod
    def _hash_package(public_files):
        content_hash = hashlib.sha256()
        for filename in sorted(public_files.keys()):
            content_hash.update(public_files[filename].encode())
        return content_hash

    def handle(
        self,
        directory: str,
        name: str,
        version: str,
        metadata: JobMetadata,
        executor_image_tag: str = None,
        requirements_file: Optional[str] = None,
        secret_env: bool = False,
    ) -> CodePackage:
        self.echo(f"📦 Packaging code from {directory}")
        env_file, env_data = None, None
        try:
            env_data, key, iv, env_file = self.handle_env_file(directory, secret_env)
            if not secret_env:
                metadata.env_vars = env_data
            metadata.secret_key = key
            metadata.iv = iv
        except EnvFileNotFound:
            self.echo("No env file found, continuing ...")

        job_ignore_handler = JobIgnoreHandler(
            ignore_file=(
                os.path.join(directory, self.ignore_file)
                if os.path.exists(os.path.join(directory, self.ignore_file))
                else None
            )
        )

        total_size = 0

        all_files = {}
        public_files = {}

        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                total_size += os.path.getsize(filepath)
                relative_path = os.path.relpath(filepath, directory)

                if job_ignore_handler.match_gitignore_like_path(relative_path):
                    continue

                if (
                    secret_env
                    and env_file
                    and (pathlib.Path(filepath) == pathlib.Path(env_file))
                ):
                    with open(filepath, "r", encoding="utf-8") as _:
                        all_files[relative_path] = env_data
                        # metadata.env_file_path = env_file
                        self.echo(f"📄 Added {relative_path}")
                    continue

                total_size = self._add_public_file_to_package(
                    all_files, filepath, public_files, relative_path, total_size
                )

        metadata.code_size = total_size

        content_hash = self._hash_package(public_files)

        package = CodePackage(
            name=name,
            version=version,
            executor_image_tag=executor_image_tag,
            files=all_files,
            metadata=asdict(metadata),
            hash=content_hash.hexdigest(),
            binary_files=set(),
        )

        for file_path in all_files.keys():
            if is_binary_file(file_path):
                package.binary_files.add(file_path)

        return package

    def _add_public_file_to_package(
        self, all_files, filepath, public_files, relative_path, total_size
    ):
        """Add a file to the package, handling binary files appropriately."""

        new_total_size, _ = add_file_to_package(
            filepath=filepath,
            relative_path=relative_path,
            all_files=all_files,
            public_files=public_files,
            total_size=total_size,
            echo_func=self.echo,
        )

        return new_total_size

    def handle_env_file(self, directory: str, secret_env: bool):
        env_file_path = self.config.get("code").get("env_file")
        if not env_file_path:
            self.echo("No env file found in config")
            raise EnvFileNotFound

        possible_env_path = [
            os.path.join(directory, env_file_path),
            os.path.join(directory, os.path.basename(env_file_path)),
        ]
        env_file = next(
            (env_path for env_path in possible_env_path if os.path.exists(env_path)),
            None,
        )

        if not env_file:
            self.echo("No env file found to encrypt")
            raise EnvFileNotFound

        key, iv = None, None
        if secret_env:
            encryption_result = AESCipher().encrypt_file(env_file)
            env_data = encryption_result["encrypted_data"]
            key = encryption_result["key"]
            iv = encryption_result["iv"]
        else:
            env_data = dotenv_values(env_file)
        return env_data, key, iv, env_file

    def store_code(self, package: CodePackage) -> str:
        self.echo("☁️  Uploading to S3...")
        return self.backend.store(package)

    def retrieve_code(self, identifier: str) -> Optional[CodePackage]:
        return self.backend.retrieve(identifier)

    def obfuscate_code(self, package: CodePackage) -> CodePackage:
        """Obfuscate code using pyarmor."""
        return self.obfuscator.obfuscate_code(package)

    def submit_job(
        self,
        s3_key: str,
        name: str,
        version: str,
        metadata: JobMetadata,
        executor_image_tag: str = None,
        expiration=86400,
    ) -> dict:
        """Submit job to API after successful upload"""
        if not self.job_config.base_url or not self.job_config.auth_token:
            raise ValueError(
                "API configuration missing. Please set base_url and auth_token"
            )

        presigned_url = self.backend.generate_presigned_url(s3_key, expiration)
        executor_label = self.config.get("executor", {}).get("label")

        payload = {
            "name": name,
            "version": version,
            "executor_image_tag": executor_image_tag,
            "directory": {"url": presigned_url, "type": "s3"},
            "execution_plan": (
                asdict(metadata.execution_plan)
                if metadata.execution_plan is not None
                else None
            ),
            "meta_data": {
                "pipeline_hash": metadata.pipeline_hash,
                "confidential_level": metadata.confidential_level,
                "execution_mode": metadata.execution_mode,
                "main_file_path": metadata.main_file_path,
                "env_file_path": metadata.env_file_path,
                "data_size": metadata.data_size,
                "complexity_factor": metadata.complexity_factor,
                "encryption_credentials": {
                    "secret_key": metadata.secret_key,
                    "iv": metadata.iv,
                },
            },
        }
        if executor_label:
            payload.update({"executor_label": executor_label})

        try:
            self.echo("🚀 Submitting job...")
            response_data = self.rest_client.post("jobs/submit", json=payload)
            self.echo("✅ Job submitted successfully!")
            return response_data
        except RestClientException as e:
            self.echo(f"❌ Failed to submit job: {str(e)}")
            raise

    def publish_job(
        self,
        s3_key: str,
        name: str,
        version: str,
        metadata: JobMetadata,
        expiration=86400,
    ) -> dict:
        """Submit job to API after successful upload"""
        if not self.job_config.base_url or not self.job_config.auth_token:
            raise ValueError(
                "API configuration missing. Please set base_url and auth_token"
            )

        presigned_url = self.backend.generate_presigned_url(s3_key, expiration)
        executor_label = self.config.get("executor", {}).get("label")

        payload = {
            "name": name,
            "label": name,
            "public": False,
            "pipeline": {
                "configs": metadata.env_vars,
                "schedule": (
                    {
                        "type": metadata.execution_plan.schedule_mode,
                        "expression": metadata.execution_plan.cron_expression,
                        "interval": metadata.execution_plan.interval,
                        "timezone": metadata.execution_plan.timezone,
                        "start_time": format_datetime_for_api(
                            metadata.execution_plan.start_time
                        ),
                        "end_time": format_datetime_for_api(
                            metadata.execution_plan.until
                        ),
                        "initial_run": metadata.execution_plan.initial_run,
                        "run_overlap": metadata.execution_plan.run_overlap,
                    }
                    if metadata.execution_plan is not None
                    else {"type": "once"}
                ),
                "job_template": {
                    "name": f"{name}-job",
                    "label": f"{name}-job",
                    "description": "",
                    "version": str(version),
                    "execution_priority": "default",
                    "validation_priority": "default",
                    "directory": {"url": presigned_url, "type": "s3"},
                    "retry_policy": {
                        "retry_on_error": False,
                        "interval": "0",
                        "retry_count": 0,
                        "action_on_failure": "none",
                    },
                    "meta_data": {
                        "code_size": metadata.code_size,
                        "pipeline_hash": metadata.pipeline_hash,
                        "confidential_level": metadata.confidential_level,
                        "execution_mode": metadata.execution_mode,
                        "main_file_path": metadata.main_file_path,
                        "env_file_path": metadata.env_file_path,
                        "complexity_factor": metadata.complexity_factor,
                        "data_size": metadata.data_size,
                    },
                    "executor_label": executor_label,
                },
                "config_handler": "store_accounts",
                "active": True,
            },
        }

        if metadata.secret_key:
            payload["pipeline"]["job_template"]["meta_data"].update(
                {
                    "encryption_secret_key": metadata.secret_key,
                    "encryption_iv": metadata.iv,
                }
            )

        try:
            self.echo("🚀 Publishing job to cook...")
            response_data = self.rest_client.post(
                "agent-launchers/data-agents/submit", json=payload
            )
            self.echo("✅ Job published to cook successfully!")
            return response_data
        except RestClientException as e:
            self.echo(f"❌ Failed to publish job: {str(e)}")
            raise
