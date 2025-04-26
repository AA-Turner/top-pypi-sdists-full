from tecton._internals import metadata_service
from tecton_core.errors import TectonValidationError
from tecton_core.id_helper import IdHelper
from tecton_proto.metadataservice.metadata_service__client_pb2 import CreateApiKeyRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import DeleteApiKeyRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import IntrospectApiKeyRequest
from tecton_proto.metadataservice.metadata_service__client_pb2 import ListApiKeysRequest


def create(description, is_admin):
    """Create a new API key."""
    request = CreateApiKeyRequest()
    request.description = description
    request.is_admin = is_admin
    return metadata_service.instance().CreateApiKey(request)


def introspect(api_key):
    """Get information about the API key."""
    request = IntrospectApiKeyRequest()
    request.api_key = api_key
    return metadata_service.instance().IntrospectApiKey(request)


def delete(id):
    """Delete an API key by its ID."""
    request = DeleteApiKeyRequest()
    try:
        id_proto = IdHelper.from_string(id)
    except Exception:
        msg = "Invalid format for ID"
        raise TectonValidationError(msg)
    request.id.CopyFrom(id_proto)
    return metadata_service.instance().DeleteApiKey(request)


def list():
    """List active API keys."""
    request = ListApiKeysRequest()
    return metadata_service.instance().ListApiKeys(request)
