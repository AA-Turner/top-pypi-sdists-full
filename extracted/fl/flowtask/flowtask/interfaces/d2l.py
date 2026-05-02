"""
D2L.

Making operations over D2L.

"""
import re
from datetime import datetime, timezone
from ..exceptions import (
    ComponentError
)
import random
from .http import HTTPService, ua
from .cache import CacheSupport

class D2LClient(CacheSupport, HTTPService):
    '''
        Manage Connection to D2L
    '''
    def __init__(self, *args, **kwargs):
        self.token_type: str = "Bearer"
        self.auth_type: str = "apikey"
        self.domain: str = kwargs.pop('domain', None)
        self.domain = self.get_env_value(self.domain, self.domain)
        self.url_login: str = f'https://{self.domain}/d2l/lp/auth/login/login.d2l'
        self.url_token: str = f'https://{self.domain}/d2l/lp/auth/oauth2/token'
        self.file_format: str = 'application/zip'
        self.create_destination: bool = True  # by default
        self.dataset: str = kwargs.pop('dataset', None)
        self.plugin: str = kwargs.pop('plugin', None)
        self.d2l_session_val: str = None
        self.d2l_secure_session_val: str = None
        self.csrf_token: str = None
        self.auth: dict = {'apikey': None}
        super().__init__(*args, **kwargs)
        self.processing_credentials()
        self.username: str = self.credentials.get('username', None)
        self.password: str = self.credentials.get('password', None)
        self.headers = {
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua)
        }

    async def get_bearer_token(self):
        # Try to get API Key from REDIS
        with await self.open() as redis:
            api_key = redis.get('D2L_API_KEY')
            d2l_session_val = redis.get('D2L_SESSION_VAL')
            d2l_secure_session_val = redis.get('D2L_SECURE_SESSION_VAL')
            if api_key:
                self.auth['apikey'] = api_key
                self.cookies = {
                    "d2lSessionVal": d2l_session_val,
                    "d2lSecureSessionVal": d2l_secure_session_val
                }
                self.headers["Authorization"] = f"Bearer {self.auth.get('apikey')}"
                return api_key
        # Get cookies values
        login_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": f"https://{self.domain}",
            "Referer": f"https://{self.domain}/d2l/login",
            "User-Agent": random.choice(ua)
        }
        login_data = {
            "d2l_referrer": f"https://{self.domain}/d2l/login",
            "loginPath": "/d2l/login",
            "userName": self.username,
            "password": self.password,
        }
        try:
            response = await self._post(
                url=self.url_login,
                cookies=None,
                headers=login_headers,
                data=login_data,
                follow_redirects=False,
                raise_for_status=False,
                use_proxy= False
            )
            d2l_session_val = response.cookies.get("d2lSessionVal", "")
            d2l_secure_session_val = response.cookies.get("d2lSecureSessionVal", "")
            self.cookies = {
                "d2lSessionVal": d2l_session_val,
                "d2lSecureSessionVal": d2l_secure_session_val
            }
            response = await self._post(
                url=self.url_login,
                cookies=self.cookies,
                headers=login_headers,
                data=login_data,
                follow_redirects=True,
                raise_for_status=True,
                use_proxy= False
            )
            csrf_token_match = re.search(r"localStorage\.setItem\('XSRF\.Token','(.*?)'\)", response.text)
            csrf_token = csrf_token_match.group(1) if csrf_token_match else ""
        except Exception as err:
            raise ComponentError(
                f"D2L: Error getting data from URL {err}"
            )
        # Get Bearer Token
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": f"https://{self.domain}",
            "Referer": f"https://{self.domain}/d2l/home",
            "x-csrf-token": csrf_token,
            "User-Agent": random.choice(ua)
        }
        token_data = {"scope": "*:*:*"}
        try:
            response = await self._post(
                url=self.url_token,
                cookies=self.cookies,
                headers=token_headers,
                data=token_data,
                use_proxy= False
            )
            json = response.json()
            with await self.open() as redis:
                current_timestamp = int(datetime.now(timezone.utc).timestamp())
                expires_at = json.get('expires_at', (current_timestamp - 600))
                timeout = expires_at - current_timestamp
                self.setexp('D2L_API_KEY', json.get("access_token", None), f'{timeout}s')
                self.setexp('D2L_SESSION_VAL', d2l_session_val, f'{timeout}s')
                self.setexp('D2L_SECURE_SESSION_VAL', d2l_secure_session_val, f'{timeout}s')
            self.auth['apikey'] = json.get("access_token", None)
            self.headers["Authorization"] = f"Bearer {self.auth.get('apikey')}"
            return self.auth['apikey']
        except Exception as err:
            raise ComponentError(
                f"D2L: Error getting data from URL {err}"
            )

    async def download_file(self):
        # Get Download URL
        url = f'https://{self.domain}/d2l/api/lp/1.45/datasets/bds/{self.schema}/extracts'
        response = await self.api_get(
            url=url,
            headers=self.headers,
            use_proxy=False
        )
        download_link = ''
        if hasattr(self, "masks") and hasattr(self, 'date'):
            self.date = self.mask_replacement(self.date)
        for obj in response.get('Objects', []):
            if hasattr(self, "date") and self.date:
                target_date = datetime.strptime(self.date, "%Y-%m-%d").date()
                if obj.get("BdsType") == "Differential":
                    created_date = datetime.strptime(obj.get("CreatedDate", ""), "%Y-%m-%dT%H:%M:%S.%fZ").date()
                    if created_date == target_date:
                        download_link = obj.get("DownloadLink")
                        break
            else:
                if obj.get('BdsType', '') == 'Full':
                    download_link = obj.get('DownloadLink', '')
                    break
        # Download ZIP File
        self.download = True
        await self.async_request(
            url=download_link
        )
        return True

    async def request_iterate(self, endpoint, api=True, **kwargs):
        has_more_items = True
        resultset = []
        bookmark = 0
        if api == True:
            while has_more_items == True:
                url = f'https://{self.domain}/d2l/api{endpoint}/?bookmark={bookmark}'
                response = await self.api_get(
                    url=url,
                    headers=self.headers,
                    use_proxy= False
                )
                if not response['Items']:
                    break
                else:
                    bookmark = response['PagingInfo']['Bookmark']
                    has_more_items = response['PagingInfo']['HasMoreItems']
                    resultset = [*resultset, *response['Items']]
                #break
            return resultset
        else:
            item = kwargs.get('item', '')
            while has_more_items == True:
                url = f'https://{self.domain}/d2l{endpoint}/?limit=100&offset={bookmark}'
                try:
                    response = await self.api_get(
                        url=url,
                        headers=self.headers,
                        cookies=self.cookies,
                        use_proxy= False
                    )
                    if not response[item]:
                        break
                    else:
                        bookmark += 100
                        has_more_items = response['Metadata']['HasMore']
                        resultset = [*resultset, *response[item]]
                    #break
                except Exception:
                    break
            return resultset

    async def awards(self, org_units=None):
        result = []
        
        if org_units is None:
            org_units = await self.request_iterate('/lp/1.49/orgstructure', True)
            org_units = [item["Identifier"] for item in org_units["Items"]]
        
        for org_unit_id in org_units:
            users = await self.request_iterate(f'/awards/v1/{org_unit_id}/classlist', False, item='Users')
            for user in users:
                user_id = user['UserId']
                org_unit_id = user['OrgUnitId']
                
                if user['Paging'].get('HasMore', False) == True:
                    awards = await self.request_iterate(f'/awards/v1/{org_unit_id}/myAwards/{user_id}', False, item='Awards')
                else:
                    awards = user['Awards']
                
                for award in awards:
                    result.append({
                        'award_id': award['AwardId'],
                        'user_id': user_id,
                        'org_unit_id': org_unit_id,
                        'certificate_id': award['CertificateId'],
                        'achievement_id': award['AchievementId'],
                        'achievement': award['Achievement'].get('Title	', None),
                        'awarded_by': award['AwardedBy'],
                        'issue_date': award['IssueDate'][14:-1]
                    })
        return result