from typing import List
from typing import Optional

from typeguard import typechecked

from tecton import version as tecton_version
from tecton._internals import metadata_service
from tecton.framework import base_tecton_object
from tecton_core import errors
from tecton_core import id_helper
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


def format_validation_errors(
    primary_object: base_tecton_object.BaseTectonObject,
    dependent_objects: List[base_tecton_object.BaseTectonObject],
    validation_errors: List[state_update_pb2.ValidationMessage],
) -> str:
    id_to_dependent_object = {obj.id: obj for obj in dependent_objects}

    if len(validation_errors) == 1:
        # If there is a single error, print the entire exception on one line. This is better UX in notebooks, which
        # often only show the first line of an exception in a preview.
        msg = f"{primary_object.__class__.__name__} '{primary_object.info.name}' failed validation"
        error = validation_errors[0]
        error_object_id = id_helper.IdHelper.to_string(error.fco_refs[0].fco_id)
        if error_object_id != primary_object.id:
            # a dependent object failed validation
            dependent_object = id_to_dependent_object.get(error_object_id, None)
            if dependent_object:
                msg += f" due to dependent {dependent_object.__class__.__name__} '{dependent_object.info.name}'"
        return f"{msg}: {error.message}"

    else:
        error_strings = [
            f"{primary_object.__class__.__name__} '{primary_object.info.name}' failed validation with the following errors:"
        ]
        for error in validation_errors:
            error_object_id = id_helper.IdHelper.to_string(error.fco_refs[0].fco_id)
            prefix = ""
            if error_object_id != primary_object.id:
                dep_obj = id_to_dependent_object.get(error_object_id, None)
                if dep_obj:
                    prefix = f"[Dependent {dep_obj.__class__.__name__} '{dep_obj.info.name}'] "
            error_strings.append(f"  • {prefix}{error.message}")
        return "\n".join(error_strings)


def _check_errors_match_validation_objects(
    primary_object: base_tecton_object.BaseTectonObject,
    dependent_objects: List[base_tecton_object.BaseTectonObject],
    validation_errors: List[state_update_pb2.ValidationMessage],
) -> None:
    validation_object_ids = {primary_object.id}.union({obj.id for obj in dependent_objects})
    for error in validation_errors:
        error_object_id = id_helper.IdHelper.to_string(error.fco_refs[0].fco_id)
        if error_object_id not in validation_object_ids:
            expected_ids = ", ".join(sorted(validation_object_ids))
            msg = f"Backend validation error returned unexpected object id: {error_object_id}. Expected one of: {expected_ids}"
            raise errors.TectonInternalError(msg)


@typechecked
def run_backend_validation_and_assert_valid(
    primary_object: base_tecton_object.BaseTectonObject,
    validation_request: validator_pb2.ValidationRequest,
    dependent_objects: Optional[List[base_tecton_object.BaseTectonObject]] = None,
) -> None:
    """Run validation against the Tecton backend.

    Raises an exception if validation fails.
    :param primary_object: The primary object to validate.
    :param validation_request: The validation request to send to the backend.
    :param dependent_objects: A list of dependent objects to validate.
    """
    if dependent_objects is None:
        dependent_objects = []

    validation_local_fco_request = metadata_service_pb2.ValidateLocalFcoRequest(
        sdk_version=tecton_version.get_semantic_version(),
        validation_request=validation_request,
    )
    response = metadata_service.instance().ValidateLocalFco(validation_local_fco_request).response_proto

    if response.success:
        return

    # If there's a server side error, print that instead of the validation errors.
    if response.error:
        msg = f"{primary_object.__class__.__name__} '{primary_object.info.name}' failed validation: {response.error}"
        raise errors.TectonValidationError(msg)

    validation_errors = response.validation_result.errors
    _check_errors_match_validation_objects(primary_object, dependent_objects, validation_errors)
    raise errors.TectonValidationError(format_validation_errors(primary_object, dependent_objects, validation_errors))
