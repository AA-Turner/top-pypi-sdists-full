import boto3
import os
import datetime
import zipfile
import tempfile
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

def upload_file_to_s3(file_path, bucket_name, s3_key):
    # Load configuration from environment variables or a config file
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAZ7YFAWD6HLD47Z4O')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')
    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    logger.debug(f"Uploading file {file_path} to S3 bucket {bucket_name} with key {s3_key}")
    logger.debug(f"Using AWS region: {region_name}")

    # Create an S3 client with the configuration
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name)

    # Upload the file to S3
    s3.upload_file(file_path, bucket_name, s3_key)
    logger.debug(f"Successfully uploaded file to S3: s3://{bucket_name}/{s3_key}")

def deploy_zip_to_s3(local_directory):
    """
    Create a zip file from a local directory and upload it to S3.
    
    :param local_directory: Path to the local directory to be zipped and uploaded
    :return: S3 key of the uploaded zip file
    """
    bucket_name = 'zinley'
    s3_prefix = 'fsd/'
    ignore_files = ['.git', '.DS_Store', '.zinley', '.zinley.tags.cache.v3', '.gitignore']
    
    logger.debug(f"Starting deployment process for directory: {local_directory}")
    logger.debug(f"Using bucket: {bucket_name}, prefix: {s3_prefix}")
    logger.debug(f"Ignoring files: {ignore_files}")

    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(suffix='_web.zip', delete=False) as temp_zip:
        zip_filename = temp_zip.name
        logger.debug(f"Created temporary zip file: {zip_filename}")
        logger.debug(f"Creating zip archive at: {zip_filename}")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            logger.debug(local_directory)
            for root, dirs, files in os.walk(local_directory, topdown=True):
                # Convert local_directory to absolute path if it's not already
                local_directory = os.path.abspath(local_directory)
                
                # Ensure root is an absolute path
                root = os.path.abspath(root)
                
                # Skip if root is not within local_directory
                if not root.startswith(local_directory):
                    logger.debug(f"Skipping directory outside of local_directory: {root}")
                    continue

                # Remove ignored directories
                dirs[:] = [d for d in dirs if d not in ignore_files]
                logger.debug(f"Processing directory: {root}")
                for file in files:
                    if file not in ignore_files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, local_directory)
                        if os.path.isfile(file_path):  # Check if it's a file before adding
                            logger.debug(f"Adding file to zip: {arcname}")
                            zipf.write(file_path, arcname)
    
    # Check if the zip file is empty
    zip_size = os.path.getsize(zip_filename)
    logger.debug(f"Generated zip file size: {zip_size} bytes")
    if zip_size == 0:
        logger.error(f"Generated zip file {zip_filename} is empty")
        os.unlink(zip_filename)
        raise ValueError(f"Generated zip file {zip_filename} is empty. No files were added.")
    
    # Generate S3 key for the zip file
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    s3_key = f"{s3_prefix}{os.path.basename(local_directory)}_{timestamp}_web.zip"
    logger.debug(f"Generated S3 key: {s3_key}")
    
    # Upload the zip file to S3
    logger.debug("Starting upload to S3...")
    upload_file_to_s3(zip_filename, bucket_name, s3_key)
    logger.debug("Upload to S3 completed successfully")
    
    # Clean up the temporary zip file
    logger.debug(f"Cleaning up temporary zip file: {zip_filename}")
    os.unlink(zip_filename)
    
    return s3_key
