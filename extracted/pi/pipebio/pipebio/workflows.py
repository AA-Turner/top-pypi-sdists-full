"""Run PipeBio workflows.

A *workflow* is a saved, reusable sequence of jobs. This module resolves a saved
workflow definition, applies caller-supplied parameters, and submits it as a
``WorkflowJob``. It is exposed as :attr:`PipebioClient.workflows`.
"""

from typing import List, Any, Dict, Optional

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.jobs import Jobs
from pipebio.organization_lists import OrganizationLists
from pipebio.util import Util


class Workflows:
    """Wraps workflow execution on top of the ``jobs`` API.

    Obtain an instance via :attr:`PipebioClient.workflows` rather than
    constructing it directly.
    """

    _session: BaseUrlSession
    _url: str
    _user: Any
    _organization_lists: OrganizationLists
    _jobs: Jobs

    def __init__(self, session: BaseUrlSession, organization_lists: OrganizationLists, user: Any, jobs: Jobs) -> None:
        """Initialise the service.

        Args:
            session: An authenticated base-url session from the client.
            organization_lists: Service used to resolve workflow and scaffold
                definitions.
            user: The authenticated user object.
            jobs: Service used to poll the submitted workflow job.
        """
        self._url = 'jobs'
        self._session = Util.mount_standard_session(session)
        self._organization_lists = organization_lists
        self._user = user
        self._jobs = jobs

    def run_workflow(self,
                     project_id: str,
                     workflow_id: str,
                     name: str,
                     input_entity_ids: List[str],
                     organization_id: Optional[str] = None,
                     target_folder_id: Optional[str] = None,
                     params: Optional[Dict[str, Any]] = None,
                     poll_job: bool = False
                     ) -> Dict[str, Any]:
        """Resolve and run a saved workflow.

        Args:
            project_id: Id of the project (shareable) to run the workflow in.
            workflow_id: Id of the saved workflow definition.
            name: User-facing name for the resulting workflow job.
            input_entity_ids: Ids of the input documents/entities.
            organization_id: Organization id. Defaults to the user's default org.
            target_folder_id: Optional id of the folder to write outputs to.
            params: Values for the workflow's settable parameters, keyed by
                parameter name.
            poll_job: If ``True``, block until the workflow job completes.

        Returns:
            The workflow job object (completed when ``poll_job`` is set).

        .. API reference (generated - do not edit) ::

        **POST** ``/jobs``

        Create

        Create a new job

        API parameters:
            * ``allowDeletedEntities`` (query) -- If true, allow referencing entities that have been soft-deleted.

        API request body:
            * ``name`` -- Give the job a friendly name that is meaningful to the end user
            * ``clientSide`` (optional) -- Set true if you want to run the job locally yourself and not on PipeBio servers
            * ``shareableId`` -- Copy your project id from the project settings page
            * ``params`` -- Parameters the job can use
            * ``type`` -- What type of job is this
            * ``messages`` -- Update the user with details about what the job is currently doing
            * ``inputEntities`` -- Entity ids of entities that should be fed into this job
            * ``status`` -- Initial status of the job.

        .. end API reference ::
        """
        if params is None:
            params = dict()

        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        scaffolds = self._organization_lists.get_scaffolds()['data']

        response = self._organization_lists.get_workflow(workflow_id=workflow_id)
        workflow = response['options']['workflow']
        workflow_name = response['name']
        workflow_description = workflow['description'] if 'description' in workflow else ''

        param_names = list(params.keys())

        jobs = workflow['jobs']

        self._process_jobs(jobs, param_names, params, workflow_id, scaffolds)

        workflow_params = dict(name=name,
                               params=dict(jobs=jobs,
                                           name=workflow_name,
                                           description=workflow_description),
                               shareableId=project_id,
                               ownerId=_organization_id,
                               inputEntities=input_entity_ids,
                               type='WorkflowJob')
        if target_folder_id is not None:
            workflow_params['params']['targetFolderId'] = target_folder_id

        workflow_response = self._session.post('jobs', json=workflow_params)

        Util.raise_detailed_error(workflow_response)

        job = workflow_response.json()

        if poll_job:
            return self._jobs.poll_job(job['id'])
        else:
            return job

    def _process_jobs(self, jobs: List[Dict],
                      param_names: List[str],
                      params: Dict[str, Any],
                      workflow_id: str,
                      scaffolds: List[Dict]) -> None:
        """
        Iterates over all the jobs, replacing params if they are settable.
        If a settableParam has a required validator - it checks that either:
            - it is included in the params
            - has a default value already set in the workflow
        :param jobs:
        :param param_names:
        :param params:
        :param workflow_id:
        :param scaffolds:
        :return:
        """
        # iterate over each job
        for job in jobs:
            if 'jobs' in job:
                # Recursion!
                self._process_jobs(job['jobs'], param_names, params, workflow_id, scaffolds)
            else:
                if 'params' in job:
                    job_params = list(job['params'].items())
                    for key, value in job_params:
                        # iterate over each param for a job
                        if 'settableParams' in job:
                            settable_param = next(filter(lambda p: p['name'] == key, job['settableParams']), None)
                            # if its a settable param, use supplied value or validate
                            if settable_param is not None:
                                if key in param_names:
                                    # TODO validate options['allowedValues']?
                                    # set the job param to the supplied value
                                    job['params'][key] = params[key]
                                else:
                                    if 'validators' in settable_param:
                                        self._validate_required(workflow_id, key, value, settable_param)
                                del job['settableParams']

                        if key == 'scaffold':
                            scaffold = next(filter(lambda s: s['name'] == value, scaffolds), None)
                            if scaffold is not None:
                                job['params'][key] = dict(id=scaffold['id'], name=value)
                            else:
                                names = ', '.join(f'"{s["name"]}"' for s in scaffolds)
                                raise ValueError(
                                    f'No scaffold with the name specified in the workflow ({value}) was found. '
                                    f'Available scaffolds are: {names}'
                            )

    @staticmethod
    def _validate_required(workflow_id: str, key: str, value: Any, settable_param: Dict) -> None:
        is_required = next(
            filter(lambda p: p['name'] == 'required', settable_param['validators']),
            {'value': False}
        )['value']
        default_value_is_none = (value is None or value == 'None' or
                                 (isinstance(value, list) and len(value) == 0))
        if is_required and default_value_is_none:
            raise ValueError(f'Parameter {key} is required for workflow {workflow_id}')
