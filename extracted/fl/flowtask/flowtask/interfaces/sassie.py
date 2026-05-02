"""
Sassie.

Making operations over Sassie API.

"""

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

    def _build_filter_string(self):
        """
        Build filter string for API URL
        Format: column,operator,value;column,operator,value
        """
        if not self.filters:
            return None

        filter_parts = []
        for filter_item in self.filters:
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

    async def request_iterate(self, url_base, args, item, subitem):
        has_more_items = True
        resultset = []
        offset = 0
        limit = 500

        # Add filter to args if present
        filter_str = self._build_filter_string()
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

    async def get_surveys(self):
        result = await self.request_iterate(f'{self.domain}/surveys', {}, 'surveys', 'survey')
        return result

    async def get_questions(self):
        result = []
        args = {
            'relatives': 'questions,questions.question_sections,questions.answer_options,survey_question_sets,questions.question_properties'
        }
        data = await self.request_iterate(f'{self.domain}/surveys', args, 'surveys', 'survey')
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
    
    async def get_jobs(self):
        result = []
        args = {
            'relatives': 'wave,responses,job_detail'
        }
        data = await self.request_iterate(f'{self.domain}/jobs', args, 'jobs', 'job')
        for job in data:
            job_detail = job.get('job_detail', [])
            wave = job.get('wave', [])
            job.update(job.pop("job_detail", {}))
            job.update(job.pop("wave", {}))
            result.append(job)
        return result

    async def get_responses(self):
        result = []
        args = {
            'relatives': 'responses'
        }
        data = await self.request_iterate(f'{self.domain}/jobs', args, 'jobs', 'job')
        result = [response for job in data for response in job.get("responses", [])]
        return result

    async def get_waves(self):
        result = await self.request_iterate(f'{self.domain}/waves', {}, 'waves', 'wave')
        return result

    async def get_locations(self):
        result = await self.request_iterate(f'{self.domain}/locations', {}, 'locations', 'location')
        return result

    async def get_clients(self):
        result = await self.request_iterate(f'{self.domain}/clients', {}, 'clients', 'client')
        return result

    async def get_question_sections(self):
        result = []
        args = {
            'relatives': 'questions.question_sections'
        }
        data = await self.request_iterate(f'{self.domain}/surveys', args, 'surveys', 'survey')
        result = [
            section
            for survey in data
            for question in survey.get("questions", [])
            for section in question.get("question_sections", [])
        ]
        return result

    async def get_question_properties(self):
        result = []
        args = {
            'relatives': 'questions.question_properties'
        }
        data = await self.request_iterate(f'{self.domain}/surveys', args, 'surveys', 'survey')
        result = [
            section
            for survey in data
            for question in survey.get("questions", [])
            for section in question.get("question_properties", [])
        ]
        return result

    async def get_custom(self):
        result = []
        args = {}
        merged_columns = self.merged_columns if hasattr(self, 'merged_columns') else None
        subgroup = self.subgroup if hasattr(self, 'subgroup') else None
        endpoint = self.endpoint if hasattr(self, 'endpoint') else None
        if not endpoint:
            return []
        if hasattr(self, 'relatives'):
            args['relatives'] = self.relatives
        data = await self.request_iterate(f'{self.domain}/{endpoint}', args, endpoint, endpoint[:-1])
        if subgroup:
            result = [response for row in data for response in row.get(subgroup, [])]
        elif merged_columns:
            result = [row.update({k: v for merged in merged_columns for k, v in row.pop(merged, {}).items()}) or row for row in data]
        else:
            result = data
        return result