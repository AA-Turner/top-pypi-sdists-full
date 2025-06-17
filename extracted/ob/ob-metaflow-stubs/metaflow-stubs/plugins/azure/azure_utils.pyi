######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.933445                                                            #
######################################################################################################

from __future__ import annotations


from .azure_exceptions import MetaflowAzureAuthenticationError as MetaflowAzureAuthenticationError
from .azure_exceptions import MetaflowAzureResourceError as MetaflowAzureResourceError
from .azure_exceptions import MetaflowAzurePackageError as MetaflowAzurePackageError
from ...exception import MetaflowInternalError as MetaflowInternalError
from ...exception import MetaflowException as MetaflowException
from .azure_credential import create_cacheable_azure_credential as create_cacheable_azure_credential

def check_azure_deps(func):
    """
    The decorated function checks Azure dependencies (as needed for Azure storage backend). This includes
    various Azure SDK packages, as well as a Python version of >3.6
    
    We also tune some warning and logging configurations to reduce excessive log lines from Azure SDK.
    """
    ...

def parse_azure_full_path(blob_full_uri):
    """
    Parse an Azure Blob Storage path str into a tuple (container_name, blob).
    
    Expected format is: <container_name>/<blob>
    
    This is sometimes used to parse an Azure sys root, in which case:
    
    - <container_name> is the Azure Blob Storage container name
    - <blob> is effectively a blob_prefix, a subpath within the container in which blobs will live
    
    Blob may be None, if input looks like <container_name>. I.e. no slashes present.
    
    We take a strict validation approach, doing no implicit string manipulations on
    the user's behalf.  Path manipulations by themselves are complicated enough without
    adding magic.
    
    We provide clear error messages so the user knows exactly how to fix any validation error.
    """
    ...

def process_exception(*args, **kwargs):
    ...

def handle_exceptions(func):
    """
    This is a decorator leveraging the logic from process_exception()
    """
    ...

def create_static_token_credential(*args, **kwargs):
    ...

