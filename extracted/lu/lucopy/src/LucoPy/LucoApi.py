import urllib
import logging
import json
import os
import re

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)

from .ApiCore import ApiCore
from .Submissions import Submission
from .exceptions import ApiException
from .api_helpers import (
    _build_slot_sequence_name_dict,
    _build_slot_sequence_name_array,
    _build_param_dict)

class LucoApi:
    """
    This class acts as the user gateway to the API.
    Authentication is handled behind the scenes by the ApiCore class so that 
    access tokens can be shared by multiple API calls.
    """
    def __init__(self, base_url=None, tenant_id=None, client_id=None, client_secret=None, 
                 resource_id=None, identity=None, timeout=20, log=False):

        config = {
            'base_url': base_url,
            'tenant_id': tenant_id,
            'client_id': client_id,
            'client_secret': client_secret,
            'resource_id': resource_id
        }

        for k, v in config.items():
            if not v:
                # Fill in None's with env where possible
                config[k] = os.environ.get(f'LUCO_{k.upper()}')

        if config['base_url']:
            if not re.search('^https.+', config['base_url']):
                raise ApiException(f'API base URL must use https: {base_url}')
        else:
            raise ApiException(f'Luco URL not defined: {config["base_url"]}')
            
        self.core = ApiCore(config, timeout, identity)

        if log:
            file_handler = logging.FileHandler('log.txt', mode='w')
            formatter = logging.Formatter('%(name)s : %(levelname)s : %(message)s')
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)
        else:
            logging.getLogger().addHandler(logging.NullHandler())

    def find_slotId(self, date, slotSequence):
        """
        Deprecated: Please use find_slot_id()
        """
        return self.find_slot_id(date, slotSequence)

    def find_slot_id(self, tag=None, slot_sequence=None):
        """
        Find slot id from a tag/date and slot sequence definition.

        Args:
            tag (str) : Date (YYYY-MM-DD) for scheduled deliveries or Unique tag for unscheduled deliveries
            slot_sequence (dict or list of k:v pairs (dicts)) : list slot sequence definitions in form {'key': 'value'}.
                Order matters - this determines parameter position.

        Returns:
            slot_id (int)
        """

        endpoint = f'/slots/search/'

        definitions = _build_slot_sequence_name_array(slot_sequence)
                
        payload = urllib.parse.urlencode({'Tag': tag,
                                          'SlotSequenceDefinition': definitions}, doseq=True)

        r = self.core.get_request(endpoint, params=payload, allow_status=[404])
        
        if r.status_code == 404:
            slot_id = self.__create_unscheduled_slot(tag, definitions)
        else:
            r.raise_for_status()
            slot_id = r.json()['slotId']

        return slot_id

    def __create_unscheduled_slot(self, tag, slot_sequence):
        """
        If find_slot_id receives a 404 error code, this means a slot with the requested tag does
        not exist. In this case we use the POST /slots/ endpoint to create a new slot on the 
        slot sequence with the requested tag. 

        The slot id of the newly created slot is passed back to the user.
        """
        endpoint = '/slots/'

        payload = {'tag': str(tag),
                   'slotSequenceDefinition': slot_sequence}

        header = {'content-type': 'application/json-patch+json'}
        r = self.core.post_request(endpoint, additionalHeaders=header, data=json.dumps(payload))

        r.raise_for_status()

        return r.json()['slotId']

    def get_submission(self, slot_id, submission_id):
        """
        Returns a submission object representing an existing submission.
        
        Args:
            slot_id (int)
            submission_id (int)

        Returns:
            submission (Submission)
        """
        return Submission(slot_id, submission_id, self.core)

    def create_submission(self, slot_id, stage=None, run_environments=None):
        """
        Create a submission against a slot and return a Submission object representing it.
        
        Args:
            slot_id (int)
            stage (string) : None
            run_environment (dict or list of dicts) : None
        Returns:
            submission (Submission)
        """
        # Create new submission
        endpoint = f'/slots/{slot_id}/submissions'
        r = self.core.post_request(endpoint)
        r.raise_for_status()

        submission_id = r.json()['slotSubmissionId']

        # Get Submission object of newly created submission
        new_submission = self.get_submission(slot_id, submission_id)
        
        if stage and run_environments:
            new_submission.submit_run_environment(stage, run_environments)

        return new_submission

    def find_submission_in_slot_sequence(self, slot_id, submission_id, OnlyCompletedSubmissions=False, TimeDifference=None, FindClosest='historic'):
        """
        Returns a Slot and Submission ID and whether it is an exact match 
        based on the search criteria, and what the relative difference is 
        in terms of time and number of slots.

        endpoint: GET /slots/{slotId}/submissions/{submissionId}/search

        Args:
            slot_id (int)
            submission_id (int)
            OnlyCompletedSubmissions (bool)
            TimeDifference (str) : d:HH:MM:SS
            FindClosest (str) : historic, future, either or exact
            
        Returns:
            Response JSON (dict)
        """
        endpoint = f'/slots/{slot_id}/submissions/{submission_id}/search'

        payload = {'OnlyCompletedSubmissions': OnlyCompletedSubmissions,
                   'FindClosest': FindClosest}

        if TimeDifference:
            payload['TimeDifference'] = TimeDifference

        r = self.core.get_request(endpoint, params=payload)
        r.raise_for_status()

        return r.json()

    def find_submissions_by_slot_sequence(self, slotSequence, onlyLatestSlot=True, onlyDeliveredSlots=True, onlyCompletedSubmissions=True,
                                  onlyLatestSubmission=True, expectedAfterUtc=None, expectedBeforeUtc=None):
        """
        Returns submissions and their slots for a slot sequence

        endpoint: GET /slotsequences/submissions

        Args:
            slotSequence (list of k:v pairs (dicts))
            onlyLatestSlot (bool)
            onlyDeliveredSlots (bool)
            onlyCompletedSubmissions (bool)
            onlyLatestSubmission (bool)
            expectedAfterUtc (str) : YYYY-MM-DD or YYYY-MM-DDThh:mm:ss
            expectedBeforeUtc (str) : YYYY-MM-DD or YYYY-MM-DDThh:mm:ss
        """
        endpoint = f'/slotsequences/submissions'

        definitions = _build_slot_sequence_name_array(slotSequence)
        
        payload_dict = {'SlotSequenceDefinition': definitions,
                        'OnlyLatestSlot': onlyLatestSlot,
                        'OnlyDeliveredSlots': onlyDeliveredSlots,
                        'OnlyCompletedSubmissions': onlyCompletedSubmissions,
                        'OnlyLatestSubmission': onlyLatestSubmission}

        if expectedAfterUtc:
            payload_dict['ExpectedAfterUtc'] = expectedAfterUtc
        if expectedBeforeUtc:
            payload_dict['ExpectedBeforeUtc'] = expectedBeforeUtc

        payload = urllib.parse.urlencode(payload_dict, doseq=True)

        r = self.core.get_request(endpoint, params=payload)
        r.raise_for_status()

        return r.json()

    def find_latest_submission_by_slot_sequence(self, slotSequence, expectedAfterUtc=None, expectedBeforeUtc=None):
        """
        Accessory method to LucoApi.find_submissions_by_slot_sequence(). Returns the slot id and submission id of 
        the most recently completed submission on the slot sequence.

        Equivalent to: 
        
        find_submissions_by_slot_sequence(slotSequence, expectedAfterUtc=expectedAfterUtc, expectedBeforeUtc=expectedBeforeUtc)

        Where the response JSON is interpreted to only return the slot id and submission id.
        """
        r = self.find_submissions_by_slot_sequence(slotSequence, 
                expectedAfterUtc=expectedAfterUtc, expectedBeforeUtc=expectedBeforeUtc)

        slot_id = r['slots'][0]['slotId']
        submission_id = r['slots'][0]['submissions'][0]['slotSubmissionId']

        return slot_id, submission_id

    def submit_slot_sequences(self, slot_sequences, allow_overwrites=False, allow_archiving=False, ignore_delivery_config=False):
        """
        Submit slot sequence definitions to create a new slot sequence or update an existing slot sequence
        """

        # ensure slot_sequences is a list
        slot_sequences = [slot_sequences] if isinstance(slot_sequences, dict) else slot_sequences

        endpoint = f'/v2/slotsequences/import'

        payload = {
            'allowOverwrites': allow_overwrites,
            'allowArchiving': allow_archiving,
            'ignoreDeliveryConfig': ignore_delivery_config,
            'slotSequences': slot_sequences
        }

        header = {'content-type': 'application/json-patch+json'}
        r = self.core.post_request(endpoint, additionalHeaders=header, json=payload)

        response = r.json()
        
        counts = {'created': response['createdCount'],
                  'exists': response['existsCount'],
                  'notProcessed': response['notProcessedCount'],
                  'updated': response['updatedCount'],
                  'notUpdated': response['notUpdatedCount'],
                  'archived': response['archivedCount']}

        imports = response['slotSequenceImports']

        for ss_import in imports:
            ss_import['slotSequenceDefinition'] = _build_slot_sequence_name_dict(ss_import['slotSequenceDefinition'])

        results = {}
        results['counts'] = counts
        results['imports'] = imports

        return results

    def __get_slot_sequence_id(self, name, is_active=True):
        """
        Get slot sequence id from slot sequence name

        Args:
            name (dict)
        Returns:
            id (int)
        """

        endpoint = f'/slotsequences/search/'

        slot_sequence_definition = _build_slot_sequence_name_array(name)
                
        payload = urllib.parse.urlencode({'isActive': is_active,
                                          'SlotSequenceDefinition': slot_sequence_definition}, doseq=True)

        r = self.core.get_request(endpoint, params=payload)
        sequence_id = r.json()['slotSequenceId']

        if sequence_id:
            return int(sequence_id)
        else:
            raise Exception(f'Could not identify Id for Slot Sequence: {name}')

    def export_slot_sequences(self, ids=None, names=None, active=True):
        """
        Export slot sequences

        Args:
            ids (str/int or list) : slot sequence ids to export
            Or, names (dict or list) : slot sequence names to export
        Returns:
            slotSequences (JSON)
        """
        if names:
            names = [names] if not isinstance(names, list) else names
            ids = [self.__get_slot_sequence_id(name, active) for name in names]
        
        endpoint = '/v2/slotsequences/export'

        params = {'slotSequenceId': ids}
        r = self.core.get_request(endpoint, params=params)

        return r.json()

    def slot_sequences_overview(self,
            count=None,
            pagination_size=500,
            is_active=True, 
            type=None,
            cadence=None,
            overdue_count_start=None,
            overdue_count_end=None,
            failed_count_start=None,
            failed_count_end=None,
            slot_sequence_name_values=None,
            slot_sequence_name_values_filter_operator=None,
            last_delivery_slot_start=None,
            last_delivery_slot_end=None,
            upcoming_slot_start=None,
            upcoming_slot_end=None,
            sort_by=None,
            sort_dir=None
        ):
        """
        Slot sequences overview.

        Args:
            count (int) : Number of slot sequences to return
            pagination_size (int) : Default=500
            is_active (bool) : Default=True
            type (string or list)
            cadence (string or list)
            overdue_count_start (int)
            overdue_count_end (int)
            failed_count_start (int)
            failed_count_end (int)
            slot_sequence_name_values (list of strings)
            slot_sequence_name_values_filter_operator ('and', 'or')
            last_delivery_slot_start (string)
            last_delivery_slot_end (string)
            upcoming_slot_start (string)
            upcoming_slot_end (string)
            sort_by (string)
            sort_dir (string)
            
        Returns:
            slot_sequences (dict) : array of slot sequences and total count
        """
        
        endpoint = '/v2/slotsequences/overview'

        params = {'isActive': is_active, 'type': type, 'cadence': cadence, 'overdueCountStart': overdue_count_start,
                  'overdueCountEnd':overdue_count_end, 'failedCountStart': failed_count_start, 'failedCountStart': failed_count_end,
                  'slotSequenceDefinitionValues': slot_sequence_name_values, 'slotSequenceDefinitionValuesFilterOperator': slot_sequence_name_values_filter_operator,
                  'lastDeliverySlotStart': last_delivery_slot_start, 'lastDeliverySlotEnd': last_delivery_slot_end,
                  'upcomingSlotStart': upcoming_slot_start, 'upcomingSlotEnd': upcoming_slot_end, 'sortBy': sort_by, 'sortDir': sort_dir,
                  'pageNumber': 1, 'pageSize': 1}
        
        # Make inital request for one slot sequence to get the total count
        r = self.core.get_request(endpoint, params=params)
        total = r.json()['totalCount']
        count = total if not count else count
        
        quotient, remainder = divmod(count, pagination_size)

        if quotient == 0:
            params['pageSize'] = remainder
        else:
            params['pageSize'] = pagination_size

        slot_sequences = []
        for i in range(quotient + 1):
            params['pageNumber'] = i + 1

            r = self.core.get_request(endpoint, params=params)

            if i == quotient:
                slot_sequences.extend(r.json()['slotSequences'][:remainder])
                test1 = r.json()['slotSequences'][:remainder]
                import json
                with open('data.json', 'w') as f:
                    json.dump(test1, f)
                print(test1)
            else:
                 slot_sequences.extend(r.json()['slotSequences'])

        for i, slot_sequence in enumerate(slot_sequences):
            name = slot_sequence['name']
            slot_sequences[i]['name'] = _build_slot_sequence_name_dict(name)

        return {'slotSequences': slot_sequences, 'totalCount': total}
    
    def slots_overview(self,
            count=None,
            pagination_size=1000,
            slot_id=None, 
            slot_sequence_id=None,
            type=None,
            cadence=None,
            slot_status=None,
            slot_sequence_name_values=None,
            slot_sequence_name_values_filter_operator=None,
            expected_by_start=None,
            expected_by_end=None,
            updated_on_start=None,
            updated_on_end=None,
            created_on_start=None,
            created_on_end=None,
            last_submission_status=None,
            sort_by=None,
            sort_dir=None,
            min_submissions=None,
            max_submissions=None            
        ):
        """
        Slots overview. 

        Args:
            count (int) : Number of slots to return
            pagination_size (int) : Default=1000
            slot_id (int or list)
            slot_sequence_id (int)
            type (string or list)
            cadence (string or list)
            slot_status (string or list)
            slot_sequence_name_values (string or list)
            slot_sequence_name_values_filter_operator ('and', 'or')
            expected_by_start (string)
            expected_by_end (string)
            updated_on_start (string)
            updated_on_end (string)
            created_on_start (string)
            created_on_end (string)
            last_submission_status (string or list)
            sort_by (string)
            sort_dir (string)
            min_submissions (int)
            max_submissions (int)

        Returns:
            slots (dict) : array of slots and total count
        """
        
        endpoint = '/v2/slots/overview'

        params = {'slotId': slot_id, 'slotSequenceId': slot_sequence_id, 'type': type, 'cadence': cadence, 'slotStatus': slot_status,
                  'slotSequenceDefinitionValues': slot_sequence_name_values, 'slotSequenceDefinitionValuesFilterOperator': slot_sequence_name_values_filter_operator,
                  'expectedByStart': expected_by_start, 'expectedByEnd': expected_by_end, 'updatedOnStart': updated_on_start, 'updatedOnEnd': updated_on_end,
                  'createdOnStart': created_on_start, 'createdOnEnd': created_on_end, 'lastSubmissionStatus': last_submission_status, 'sortBy': sort_by, 
                  'sortDir': sort_dir, 'minSubmissions': min_submissions, 'maxSubmissions': max_submissions, 'pageNumber': 1, 'pageSize': 1}

        r = self.core.get_request(endpoint, params=params)
        test = r.json()
        total = r.json()['totalCount']
        count = total if not count else count
        
        quotient, remainder = divmod(count, pagination_size)

        if quotient == 0:
            params['pageSize'] = remainder
        else:
            params['pageSize'] = pagination_size

        slots = []
        for i in range(quotient + 1):
            params['pageNumber'] = i + 1

            r = self.core.get_request(endpoint, params=params)

            if i == quotient:
                test1 = r.json()['slots'][:remainder]
                import json
                with open('data.json', 'w') as f:
                    json.dump(test1, f)
                print(test1)
                slots.extend(r.json()['slots'][:remainder])
            else:
                slots.extend(r.json()['slots'])

        for i, slot in enumerate(slots):
            name = slot['name']
            slots[i]['name'] = _build_slot_sequence_name_dict(name)

        return {'slots': slots, 'totalCount': total}
    
    def slot_sequence_parameters(self, slot_sequence_name, group=None, key=None):

        slot_sequence_id = self.__get_slot_sequence_id(slot_sequence_name)

        endpoint = f'/v2/slotsequences/{slot_sequence_id}'

        r = self.core.get_request(endpoint)

        params = _build_param_dict(r.json()['parameters']['slotParameterGroups'])

        if group:
            param_group = params[group]

            if key:
                return param_group[key]
            else:
                return param_group
        else:
            return params
