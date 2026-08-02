import boto3
from botocore.exceptions import (
    ClientError,
    ConnectionError,
    ConnectTimeoutError,
    EndpointConnectionError,
    NoCredentialsError,
    PartialCredentialsError,
    ReadTimeoutError,
)


class SecretsManager:
    def __init__(self, fallback_region=None):
        """
        Initialize SecretsManager with optional fallback region.

        Args:
            fallback_region: Optional fallback region. If provided, will attempt
                            to fetch from this region when primary fails.
        """
        self.primary_client = boto3.client("secretsmanager")
        self.fallback_client = None
        self.fallback_region = fallback_region
        if fallback_region:
            self.fallback_client = boto3.client(
                "secretsmanager", region_name=self.fallback_region
            )

    def get_secret(self, secret_name):
        # Try primary region first
        try:
            response = self.primary_client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]
        except (
            ClientError,
            EndpointConnectionError,
            ConnectionError,
            ConnectTimeoutError,
            ReadTimeoutError,
        ) as e:
            # Only attempt fallback if fallback_region is configured
            if self.fallback_client:
                print(f"Primary region failed for {secret_name}: {e}")
                try:
                    response = self.fallback_client.get_secret_value(
                        SecretId=secret_name
                    )
                    print(
                        f"Successfully fetched {secret_name} from fallback region {self.fallback_region}"
                    )
                    return response["SecretString"]
                except Exception as fallback_error:
                    print(
                        f"Fallback region {self.fallback_region} also failed: {fallback_error}"
                    )
                    return None
            else:
                print(f"Error retrieving secret {secret_name}: {e}")
                return None
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
            return None
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None

    def upload_secret(self, secret_name, secret_value):
        # Upload to primary region. If fallback is enabled, replication is configured.
        try:
            self.primary_client.describe_secret(SecretId=secret_name)
            print(f"Secret {secret_name} already exists.")
            self.primary_client.update_secret(
                SecretId=secret_name,
                SecretString=secret_value,
            )
            print(f"Secret {secret_name} updated successfully.")
        except self.primary_client.exceptions.ResourceNotFoundException:
            print(f"Secret {secret_name} does not exist. Creating secret.")
            create_params = {
                "Name": secret_name,
                "SecretString": secret_value,
            }
            # If fallback region is enabled, set up replication during creation
            if self.fallback_region:
                create_params["AddReplicaRegions"] = [
                    {"Region": self.fallback_region}
                ]
                print(
                    f"Creating secret with replication to {self.fallback_region}"
                )
            self.primary_client.create_secret(**create_params)
            print(f"Secret {secret_name} created successfully.")
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
        except Exception as e:
            print(f"Error uploading secret {secret_name}: {e}")
