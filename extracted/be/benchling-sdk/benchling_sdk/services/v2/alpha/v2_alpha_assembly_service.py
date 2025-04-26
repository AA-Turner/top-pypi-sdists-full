from benchling_api_client.v2.alpha.api.assemblies import (
    create_and_finalize_assembly,
    get_assembly,
    validate_assembly,
)
from benchling_api_client.v2.alpha.models.assembly import Assembly
from benchling_api_client.v2.alpha.models.assembly_spec_shared import AssemblySpecShared
from benchling_api_client.v2.alpha.models.create_and_finalize_assembly_json_body import (
    CreateAndFinalizeAssemblyJsonBody,
)

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import AsyncTaskLink
from benchling_sdk.services.v2.base_service import BaseService


class V2AlphaAssemblyService(BaseService):
    """
    V2-Alpha Assemblies.

    In Benchling, Assemblies are records of a process in which many fragment sequences are
    assembled in silico to create new construct sequences.

    https://benchling.com/api/v2-alpha/reference#/Assemblies
    """

    @api_method
    def get_by_id(self, bulk_assembly_id: str) -> Assembly:
        """
        Get a bulk assembly by its API identifier.

        See https://benchling.com/api/v2-alpha/reference#/Assemblies/GetAssembly
        """
        response = get_assembly.sync_detailed(client=self.client, bulk_assembly_id=bulk_assembly_id)
        return model_from_detailed(response)

    @api_method
    def create_and_finalize(self, create: CreateAndFinalizeAssemblyJsonBody) -> TaskHelper[Assembly]:
        """
        Create and finalize a new bulk assembly in a single step.

        This endpoint launches a long-running task and returns a
        :py:class:`benchling_sdk.helpers.task_helpers.TaskHelper` for waiting on the task.
        On success, the task's response will be an :py:class:`.Assembly`.

        See https://benchling.com/api/v2-alpha/reference#/Assemblies/CreateAndFinalizeAssembly
        """
        response = create_and_finalize_assembly.sync_detailed(client=self.client, json_body=create)
        return self._task_helper_from_response(response, Assembly)

    @api_method
    def validate(self, assembly: AssemblySpecShared) -> AsyncTaskLink:
        """
        Validate an assembly prior to finalization to see if it will succeed.

        This endpoint launches a long-running task and returns the Task ID of the launched task.
        The task response contains a set of validation results.

        See https://benchling.com/api/v2-alpha/reference#/Assemblies/ValidateAssembly
        """
        response = validate_assembly.sync_detailed(client=self.client, json_body=assembly)
        return model_from_detailed(response)
