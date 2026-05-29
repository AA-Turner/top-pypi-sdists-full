"""
Sassie.

Making operations over Sassie API.

"""

import copy
import re
import html
import urllib
from datetime import datetime, timezone
from ..exceptions import (
    ComponentError
)
import random
from .http import HTTPService, ua
from .cache import CacheSupport

_DYNAMIC_VALUE_RE = re.compile(r'^\{\{(\w+)\}\}$')


class SassieClient(CacheSupport, HTTPService):
    '''
        Manage Connection to Sassie
    '''
    def __init__(self, *args, **kwargs):
        self.token_type: str = "Bearer"
        self.auth_type: str = "apikey"
        self.domain: str = kwargs.pop('domain', None)
        self.domain = self.get_env_value(self.domain, self.domain)
        self.url_login: str = f'{self.domain}/token'
        super().__init__(*args, **kwargs)
        self.filters = kwargs.get('filter', [])

    def _build_filter_string(self, filters=None):
        """
        Build filter string for API URL
        Format: column,operator,value;column,operator,value
        """
        active_filters = filters if filters is not None else self.filters
        if not active_filters:
            return None

        filter_parts = []
        for filter_item in active_filters:
            column = filter_item.get('column')
            operator = filter_item.get('operator')
            value = filter_item.get('value')

            if not all([column, operator, value]):
                continue

            # Handle date values
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d+%H:%M:%S')
            # Handle string values with spaces
            elif isinstance(value, str):
                value = value.replace(' ', '+')

            filter_parts.append(f"{column},{operator},{value}")

        return ';'.join(filter_parts) if filter_parts else None

    def _resolve_filter_values(
        self,
        filters: list[dict],
        input_df,
    ) -> list[list[dict]]:
        """Expand dynamic filter values into a list of concrete filter sets.

        - ``{{column_name}}`` → unique non-null values from input_df column
        - ``[v1, v2, ...]``   → iterate over the list elements
        - scalar              → single-element list (no fan-out)

        Returns one filter set per iteration value.
        Raises ComponentError if a column reference is missing or if more than
        one filter has a multi-value (dynamic or list) expansion.
        """
        if not filters:
            return [[]]

        dynamic_indices: list[int] = []
        expansion_values: list[list] = []

        for i, f in enumerate(filters):
            value = f.get('value')
            match = _DYNAMIC_VALUE_RE.match(str(value)) if isinstance(value, str) else None

            if match:
                col = match.group(1)
                if input_df is None:
                    raise ComponentError(
                        f"{self.__class__.__name__}: filter references column "
                        f"'{col}' but no input DataFrame is available."
                    )
                if col not in input_df.columns:
                    raise ComponentError(
                        f"{self.__class__.__name__}: filter references column "
                        f"'{col}' which does not exist in the input DataFrame. "
                        f"Available columns: {list(input_df.columns)}"
                    )
                unique_vals = input_df[col].dropna().unique().tolist()
                dynamic_indices.append(i)
                expansion_values.append(unique_vals)

            elif isinstance(value, list):
                dynamic_indices.append(i)
                expansion_values.append(value)

        if len(dynamic_indices) > 1:
            raise ComponentError(
                f"{self.__class__.__name__}: only one filter may use a dynamic "
                f"({{{{column_name}}}}) or list value at a time; "
                f"found {len(dynamic_indices)} such filters."
            )

        if not dynamic_indices:
            return [copy.deepcopy(filters)]

        idx = dynamic_indices[0]
        result = []
        for val in expansion_values[0]:
            set_copy = copy.deepcopy(filters)
            set_copy[idx]['value'] = val
            result.append(set_copy)
        return result

    async def get_bearer_token(self):
        # Try to get API Key from REDIS
        with await self.open() as redis:
            api_key = redis.get('SASSIE_API_KEY')
            if api_key:
                self.auth['apikey'] = api_key
                self.headers["Authorization"] = f"Bearer {self.auth.get('apikey')}"
                return api_key
        # Get Bearer Token
        login_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        #print('>> Login Data:', login_data)
        try:
            response = await self.api_post(
                url=self.url_login,
                payload=login_data,
                use_proxy= False
            )
            access_token = response.get('access_token', '')
            self.headers["Authorization"] = f"Bearer {access_token}"
            self.setexp('SASSIE_API_KEY', access_token, '3600s')
        except Exception as err:
            raise ComponentError(
                f"Sassie: Error getting data from URL {err}"
            )

    async def request_iterate(self, url_base, args, item, subitem, filters_override=None):
        has_more_items = True
        resultset = []
        offset = 0
        limit = 500

        # Add filter to args if present
        filter_str = self._build_filter_string(filters=filters_override)
        if filter_str:
            args['filterby'] = filter_str

        while has_more_items == True:
            arguments = urllib.parse.urlencode({
                "limit": f"{offset},{limit}",
                **args
            })
            url = f'{url_base}?{arguments}'
            try:
                response = await self.api_get(
                    url=url,
                    headers=self.headers,
                    use_proxy= False
                )
            except Exception as err:
                break
            if not response[item]:
                break
            else:
                resultset = [*resultset, *response[item][subitem]]
                has_more_items = 'next' in response[item]
            offset += limit
        return resultset

    async def get_surveys(self, filters_override=None):
        result = await self.request_iterate(f'{self.domain}/surveys', {}, 'surveys', 'survey', filters_override=filters_override)
        return result

    async def get_questions(self, filters_override=None):
        result = []
        args = {
            'relatives': 'questions,questions.question_sections,questions.answer_options,survey_question_sets,questions.question_properties'
        }
        data = await self.request_iterate(f'{self.domain}/surveys', args, 'surveys', 'survey', filters_override=filters_override)
        for survey in data:
            survey_id = survey['survey_id']
            #survey_info = {k: v for k, v in survey.items() if k != "questions"}
            #print('>>> SURVEY', survey)
            questions = survey.get('questions', [])
            for question in questions:
                if "question_text" in question:
                    question_text = question["question_text"]
                    question_text = html.unescape(question_text)
                    question_text = re.sub(r'<.*?>', '', question_text)
                    question_text = re.sub(r'\s+', ' ', question_text).strip()
                    question["question_text"] = question_text
                merged = {'survey_id': survey_id, **question}
                result.append(merged)
        return result
    
    async def get_jobs(self, filters_override=None):
        result = []
        args = {
            'relatives': 'wave,responses,job_detail'
        }
        data = await self.request_iterate(f'{self.domain}/jobs', args, 'jobs', 'job', filters_override=filters_override)
        for job in data:
            job_detail = job.get('job_detail', [])
            wave = job.get('wave', [])
            job.update(job.pop("job_detail", {}))
            job.update(job.pop("wave", {}))
            result.append(job)
        return result

    async def get_responses(self, filters_override=None):
        result = []
        args = {
            'relatives': 'responses'
        }
        data = await self.request_iterate(f'{self.domain}/jobs', args, 'jobs', 'job', filters_override=filters_override)
        result = [response for job in data for response in job.get("responses", [])]
        return result

    async def get_waves(self, filters_override=None):
        result = await self.request_iterate(f'{self.domain}/waves', {}, 'waves', 'wave', filters_override=filters_override)
        return result

    async def get_locations(self, filters_override=None):
        result = await self.request_iterate(f'{self.domain}/locations', {}, 'locations', 'location', filters_override=filters_override)
        return result

    async def get_clients(self, filters_override=None):
        result = await self.request_iterate(f'{self.domain}/clients', {}, 'clients', 'client', filters_override=filters_override)
        return result

    async def get_question_sections(self, filters_override=None):
        result = []
        args = {
            'relatives': 'questions.question_sections'
        }
        data = await self.request_iterate(f'{self.domain}/surveys', args, 'surveys', 'survey', filters_override=filters_override)
        result = [
            section
            for survey in data
            for question in survey.get("questions", [])
            for section in question.get("question_sections", [])
        ]
        return result

    async def get_question_properties(self, filters_override=None):
        result = []
        args = {
            'relatives': 'questions.question_properties'
        }
        data = await self.request_iterate(f'{self.domain}/surveys', args, 'surveys', 'survey', filters_override=filters_override)
        result = [
            section
            for survey in data
            for question in survey.get("questions", [])
            for section in question.get("question_properties", [])
        ]
        return result

    async def get_custom(self, filters_override=None):
        result = []
        args = {}
        merged_columns = self.merged_columns if hasattr(self, 'merged_columns') else None
        subgroup = self.subgroup if hasattr(self, 'subgroup') else None
        endpoint = self.endpoint if hasattr(self, 'endpoint') else None
        if not endpoint:
            return []
        if hasattr(self, 'relatives'):
            args['relatives'] = self.relatives
        data = await self.request_iterate(f'{self.domain}/{endpoint}', args, endpoint, endpoint[:-1], filters_override=filters_override)
        if subgroup:
            result = [response for row in data for response in row.get(subgroup, [])]
        elif merged_columns:
            result = [row.update({k: v for merged in merged_columns for k, v in row.pop(merged, {}).items()}) or row for row in data]
        else:
            result = data
        return result