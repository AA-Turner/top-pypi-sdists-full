import json
import logging
from .api_helpers import _build_slot_sequence_name_dict, _build_param_dict
from .data_quality.utils import resolve_object_from_json_dict
from .exceptions import DataQualityException

log = logging.getLogger(__name__)

class Submission:
    """
    This Submission class is associated with the v2 submission structure.

    Submission level functionality is handled through this class. Instances of this
    class are created using the LucoApi.get_submission() or LucoApi.create_submission() methods.
    """

    def __init__(self, slot_id, submission_id, core):
        self.slot_id = slot_id
        self.id = submission_id
        self.core = core
        self.__definitionJSON = None

    # Check if GET /slots/{slot_id}/submissions/{submission_id} has been called to 
    # get the submission JSON object.
    def __check_definition_exists(self):
        if not self.__definitionJSON:
            self.__update_definition()

    # Update JSON definition
    def __update_definition(self):
        endpoint = f'/v2/slots/{self.slot_id}/submissions/{self.id}'
        r = self.core.get_request(endpoint, params={'includeDelivery': True})
        r.raise_for_status()
        self.__definitionJSON = r.json()

    # The following @property decorated methods prevent the class from calling the api 
    # to get the submission JSON unless the call hasn't been made already.
    @property
    def type(self):
        self.__check_definition_exists()
        return self.__definitionJSON['slotSequence']['definition']['type']['slotSequenceTypeName']

    @property
    def expected_by(self):
        self.__check_definition_exists()
        return self.__definitionJSON['slot']['expectedBy']

    @property
    def name(self):
        self.__check_definition_exists()
        return _build_slot_sequence_name_dict(self.__definitionJSON['slotSequence']['definition']['name'])

    @property
    def status(self):
        self.__update_definition()
        return self.__definitionJSON['submission']['status']

    @property
    def start_time(self):
        self.__check_definition_exists()
        return self.__definitionJSON['submission']['startedOn']

    @property
    def end_time(self):
        self.__update_definition()
        return self.__definitionJSON['submission']['endedOn']

    @property
    def __param_groups(self):
        self.__check_definition_exists()
        return _build_param_dict(self.__definitionJSON['slotSequence']['parameters']['slotParameterGroups'])

    def params(self, group=None, key=None):
        """
        Search for slot parameters.

        Args:
        - group (str) : Parameter group to return
        - key (str) : Key within group to return the value of

        Returns:
        - result (dict or str)
        """
        if group:
            param_group = self.__param_groups[group]

            if key:
                return param_group[key]
            else:
                return param_group
        else:
            return self.__param_groups

    def get_delivery_schedule(self):
        """
        Return active delivery schedule. Works on assumption that there
        can only be one active schedule at a time.
        """
        self.__check_definition_exists()

        delivery_schedules = self.__definitionJSON['slotSequence']['delivery']

        for schedule in delivery_schedules:
            if schedule['isActive'] == True:
                return schedule

        # If there is no active schedule return None
        return None

    def get_metrics(self, stages=None, metrics=None, group_by_stage=False, include_duplicates=False):
        """
        Retrieve metrics from Submission.
        
        Filter by stage and metric by passing strings or lists of strings.
        Three different return formats:
            - list of dicts : Default behaviour. All metrics for filtered stages and metrics
            - dict : Metrics grouped by stage if kwarg group_by_stage=True
            - metric value : The value of the specified metric if stages and metrics are given as strings

        Args:
            stages (string or list of strings)
            metrics (string or list of strings)
            group_by_stage (bool) : Group metrics by stage. Skips metrics which do not have a stage.

        Returns:
            metrics (array, dict or metric value) : See docstring
        """
        endpoint = f'/slots/{self.slot_id}/submissions/{self.id}/metrics'

        # Define payload
        payload = {}
        payload['stages'] = [stages] if isinstance(stages, str) else stages
        payload['metrics'] = [metrics] if isinstance(metrics, str) else metrics
        payload['includeDuplicates'] = include_duplicates

        r = self.core.get_request(endpoint, params=payload)
        result = r.json()['slotSubmissionMetrics']

        if isinstance(stages, str) and isinstance(metrics, str):
            return result[0]['value']
        elif group_by_stage:
            return self.group_metrics_by_stage(result)
        else:
            return result

    def group_metrics_by_stage(self, metrics):

        stages = set()
        for metric in metrics:
            stage = metric['stage']
            if stage:
                stages.add(metric['stage'])

        # Group metrics into dict per stage
        new_result = {k: {} for k in stages}
        for metric in metrics:
            stage = metric['stage']
            kv_pair = {metric['metric']: metric['value']}
            new_result[stage].update(kv_pair)

        return new_result

    def get_quality(self):
        """
        Retrieve quality results
        
        Returns:
            quality (dict)
        """
        endpoint = f'/v2/slots/{self.slot_id}/submissions/{self.id}/quality'

        r = self.core.get_request(endpoint)
        collections = r.json()['collections']

        return collections

    def submit_run_environment(self, stage=None, run_environments=None):
        """
        Submit run environment details

        Args:
            stage (string) : Optional
            run_environments (dict or list of dicts) : Required

        Returns:
            response status (Bool) : Boolen success or failure       
        """
        endpoint = f'/slots/{self.slot_id}/submissions/{self.id}/runenvironment'

        if isinstance(run_environments, dict):
            run_environments = [run_environments]

        payload = {'stage': stage,
                   'runData': run_environments}

        header = {'content-type': 'application/json-patch+json'}
        r = self.core.post_request(endpoint, additionalHeaders=header, data=json.dumps(payload))
        r.raise_for_status()
        
        self.run_environments = run_environments

        return r.ok
    
    def submit_databricks_run_environment(self, spark, stage=None, raise_exception=False):

        try:
            from .environments import get_databricks_run_env
            run_env = get_databricks_run_env(spark)
            return self.submit_run_environment(stage=stage, run_environments=run_env)
        except Exception as e:
            logging.info(f'Failed to submit databricks run environment: {e}')
            if raise_exception:
                raise e
            return False

    def submit_metrics(self, stage=None, runId=None, metric=None, value=None, metrics=None):
        """
        Submit metrics

        metrics : takes a dictionary of Metric:Value pairs.

        If only submitting one metric, you can use metric='metric' and value='value'
        """
        endpoint = f'/v2/slots/{self.slot_id}/submissions/{self.id}/metrics'

        if metric !=None and value != None:
            metrics_list = [{"metric": metric,
                             "value": value}]
        elif metrics:
            metrics_list = []
            for k, v in metrics.items():
                metrics_list.append({"metric": k,
                                     "value": v})
        else:
            raise Exception('Metric:Value pairs not provided correctly')

        payload = {'stage': stage,
                   'metrics': metrics_list}

        header = {'content-type': 'application/json-patch+json'}
        r = self.core.post_request(endpoint, additionalHeaders=header, data=json.dumps(payload))

        r.raise_for_status()
        return r.ok

    def __submit_quality_v1(self, stage=None, runId=None, tool=None, results=None, dataset=None, action=None):
        """
        Submit quality
        
        Essential: stage, tool, results and action.
        
        Dataset is optional, runId is no longer stored.
        """
        for param in [tool, results, action]:
            if not param:
                raise Exception('Please provide: tool, results and action')

        if isinstance(results, dict):
            results = json.dumps(results)

        endpoint = f'/slots/{self.slot_id}/submissions/{self.id}/quality'

        payload = {'stage': stage,
                   'runId': '',
                   'tool': tool,
                   'results': results,
                   'dataSet': dataset,
                   'action': action}

        header = {'content-type': 'application/json-patch+json'}
        r = self.core.post_request(endpoint, additionalHeaders=header, data=json.dumps(payload))

        r.raise_for_status()
        return r.ok

    def __submit_quality_v2(self, results, stage=None, action=None, auto_determine_action=False, auto_raise_exception=False):
        """
        Submit quality results using the Luco DQ format.
        """

        endpoint = f'/v2/slots/{self.slot_id}/submissions/{self.id}/quality'

        if action == None and auto_determine_action:
            action = 'Cancelled' if results.is_exception_thrown() else 'Continued'

        params = {'stage': stage,
                  'action': action}

        header = {'content-type': 'application/json-patch+json'}

        r = self.core.post_request(endpoint, additionalHeaders=header, params=params, data=json.dumps(results.to_json_dict()))

        if action == 'Cancelled' and auto_raise_exception:
            # TODO: Should we do a status update here? Probably not to avoid doubling up on statuses
            raise DataQualityException('Data Quality validation failed. See Luco for results.')

        return r.ok

    def submit_quality(self, stage=None, runId=None, tool=None, results=None, dataset=None,
                       action=None, auto_determine_action=False, auto_raise_exception=False):
        """
        Submit Data Quality results

        If using great_expectations format: stage, tool, results and action are required. Dataset is optional.

        If using Luco DQ format: results is required, stage and action are optional

        runId is no longer used in either case.
        """

        if isinstance(results, str) or isinstance(results, dict):
            if 'validation_result' in results:
                # Check if great_expectaions format and point to v1 endpoint
                r = self.__submit_quality_v1(stage, runId, tool, results, dataset, action)
            else:
                # If Luco DQ format, use v2 endpoint
                results_obj = resolve_object_from_json_dict(results)
                r = self.__submit_quality_v2(results_obj, stage=stage, action=action, auto_determine_action=auto_determine_action, auto_raise_exception=auto_raise_exception)
        else:
            r = self.__submit_quality_v2(results, stage=stage, action=action, auto_determine_action=auto_determine_action, auto_raise_exception=auto_raise_exception)

        return r

    def submit_status(self, status, stage=None, runId=None, type=None, message=None, modified_by=None):
        """
        Submit the status of the Submission

        Args:
            runId       (str)
            status      (str)
            stage       (str)
            type        (str)
            message     (str)
            modified_by (str)

        Returns:
            response status (Bool) : Boolen success or failure
        """
        endpoint = f'/slots/{self.slot_id}/submissions/{self.id}/status'

        data = {'runId': '',
                'status': status,
                'stage' : stage,
                'type': type,
                'message': message,
                'modifiedBy': modified_by}

        header = {'content-type': 'application/json-patch+json'}
        r = self.core.post_request(endpoint, additionalHeaders=header, data=json.dumps(data))

        r.raise_for_status()
        return r.ok

    def submit_completed_status(self):
        """
        Submit a status for a completed submission.

        Equivalent to submit_status('Completed', 'Submission)
        """
        return self.submit_status('Completed', 'Submission')
