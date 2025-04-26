from typeguard import typechecked

from tecton import version as tecton_version
from tecton._internals import metadata_service
from tecton.framework import base_tecton_object
from tecton_core import errors
from tecton_core import id_helper
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


def format_server_errors(
    tecton_object: base_tecton_object.BaseTectonObject, response: metadata_service_pb2.ValidateLocalFcoResponse
) -> str:
    # If there's a server side error, print that instead of the validation errors.
    if response.error:
        return f"{tecton_object.__class__.__name__} '{tecton_object.info.name}' failed validation: {response.error}"

    validation_errors = response.validation_result.errors
    if len(validation_errors) == 1:
        # If there is a single error, print the entire exception on one line. This is better UX in notebooks, which
        # often only show the first line of an exception in a preview.
        error = validation_errors[0]
        _check_error_matches_tecton_object(tecton_object, error)
        return f"{tecton_object.__class__.__name__} '{tecton_object.info.name}' failed validation: {error.message}"
    else:
        error_strings = [
            f"{tecton_object.__class__.__name__} '{tecton_object.info.name}' failed validation with the following errors:"
        ]
        for error in validation_errors:
            _check_error_matches_tecton_object(tecton_object, error)
            error_strings.append(error.message)
        return "\n".join(error_strings)


def _check_error_matches_tecton_object(
    tecton_object: base_tecton_object.BaseTectonObject, error: state_update_pb2.ValidationMessage
) -> None:
    error_object_id = id_helper.IdHelper.to_string(error.fco_refs[0].fco_id)

    if error_object_id != tecton_object.id:
        msg = f"Backend validation error returned wrong object id: {error_object_id}. Expected {tecton_object.id}"
        raise errors.TectonInternalError(msg)


@typechecked
def run_backend_validation_and_assert_valid(
    tecton_object: base_tecton_object.BaseTectonObject,
    validation_request: validator_pb2.ValidationRequest,
) -> None:
    """Run validation against the Tecton backend.

    Raises an exception if validation fails. Prints message if successful.
    """
    validation_local_fco_request = metadata_service_pb2.ValidateLocalFcoRequest(
        sdk_version=tecton_version.get_semantic_version(),
        validation_request=validation_request,
    )
    response = metadata_service.instance().ValidateLocalFco(validation_local_fco_request).response_proto
    if not response.success:
        raise errors.TectonValidationError(format_server_errors(tecton_object, response))
