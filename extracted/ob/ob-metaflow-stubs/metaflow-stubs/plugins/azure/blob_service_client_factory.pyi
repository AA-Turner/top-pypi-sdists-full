######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.933722                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import MetaflowException as MetaflowException
from .azure_utils import check_azure_deps as check_azure_deps
from .azure_credential import create_cacheable_azure_credential as create_cacheable_azure_credential

AZURE_STORAGE_BLOB_SERVICE_ENDPOINT: None

AZURE_CLIENT_CONNECTION_DATA_BLOCK_SIZE: int

AZURE_CLIENT_MAX_SINGLE_GET_SIZE_MB: int

AZURE_CLIENT_MAX_SINGLE_PUT_SIZE_MB: int

AZURE_CLIENT_MAX_CHUNK_GET_SIZE_MB: int

BYTES_IN_MB: int

def get_azure_blob_service_client(credential = None, credential_is_cacheable = False, max_single_get_size = 33554432, max_single_put_size = 67108864, max_chunk_get_size = 16777216, connection_data_block_size = 262144):
    """
    Returns a azure.storage.blob.BlobServiceClient.
    
    The value adds are:
    - connection caching (see _ClientCache)
    - auto storage account URL detection
    - auto credential handling (pull SAS token from environment, OR DefaultAzureCredential)
    - sensible default values for Azure SDK tunables
    """
    ...

