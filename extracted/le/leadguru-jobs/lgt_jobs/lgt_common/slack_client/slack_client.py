import asyncio
import mimetypes
from datetime import datetime
import aiohttp
import requests
import json
import io
from urllib import parse
from requests import Response
from websockets.client import WebSocketClientProtocol

from lgt_jobs.lgt_common.slack_client.methods import SlackMethods


class SlackClient:
    base_url = 'https://slack.com/api/'
    token: str
    cookies: dict
    socket: WebSocketClientProtocol
    headers: dict

    def __init__(self, token: str, cookies):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}
        if isinstance(cookies, list):
            self.cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        else:
            self.cookies = cookies

    def get_presence(self, user_id: str) -> Response:
        url = f'{self.base_url}{SlackMethods.users_get_presence}'
        return requests.get(url=url, headers=self.headers, cookies=self.cookies, params={'user': user_id})

    def join_channels(self, channels):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = asyncio.gather(*[self.join_channel_async(channel) for channel in channels])
        results = loop.run_until_complete(tasks)
        loop.close()
        return results

    def leave_channels(self, channels):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = asyncio.gather(*[self.leave_channel_async(channel) for channel in channels])
        results = loop.run_until_complete(tasks)
        loop.close()
        return results

    async def join_channel_async(self, channel):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}{SlackMethods.conversations_join}?{self.__channel_payload(channel)}'
            async with session.post(url=url, cookies=self.cookies) as response:
                return await response.json()

    async def leave_channel_async(self, channel):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}{SlackMethods.conversations_leave}?{self.__channel_payload(channel)}'
            async with session.post(url=url, cookies=self.cookies) as response:
                return await response.json()

    def users_list(self, cursor=None, limit: int = 1000):
        url = f'{self.base_url}{SlackMethods.users_list}'
        payload = {}
        if cursor:
            payload['cursor'] = cursor

        if limit:
            payload['limit'] = limit

        return requests.get(url=url, cookies=self.cookies, headers=self.headers, params=payload).json()

    def upload_file(self, file, file_name):
        payload = {"filename": file_name, "length": len(file)}
        url_response = requests.post(f"{self.base_url}{SlackMethods.get_upload_url}", data=payload, headers=self.headers, cookies=self.cookies).json()

        upload_url = url_response["upload_url"]
        content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        requests.post(upload_url, files={"file": (file_name, file, content_type)}, cookies=self.cookies)

        payload = {
            "token": self.token,
            "files": json.dumps([{"id": url_response["file"], "title": file_name}]),
        }
        requests.post(f"{self.base_url}{SlackMethods.complete_upload}", data=payload, cookies=self.cookies).json()

        return url_response['file']

    def download_file(self, file_url) -> Response:
        return requests.get(file_url, headers=self.headers, cookies=self.cookies)

    def delete_file(self, file_id: str):
        payload = {"file": file_id}
        return requests.post(f"{self.base_url}{SlackMethods.delete_file}", data=payload,
                             headers=self.headers, cookies=self.cookies).json()

    def share_files(self, files_ids: list, channel: str, text: str = None) -> dict:
        payload = {
            "files": ','.join(files_ids),
            "channel": channel,
        }
        if text:
            payload["blocks"] = json.dumps([{"type": "rich_text", "elements": [
                {"type": "rich_text_section", "elements": [{"type": "text", "text": text}]}]}])

        return requests.post(f"{self.base_url}{SlackMethods.share_files}", data=payload,
                             headers=self.headers, cookies=self.cookies).json()

    def get_file_info(self, file_id: str):
        return requests.get(url=f"{self.base_url}{SlackMethods.files_info}",
                            cookies=self.cookies, headers=self.headers, params={'file': file_id}).json()

    def get_profile(self, user_id: str = None):
        url = f'{self.base_url}{SlackMethods.profile_get}'
        payload = {}
        if user_id:
            payload['user'] = user_id
        return requests.post(url=url, cookies=self.cookies, headers=self.headers, json=payload).json()

    def get_team_profile(self):
        url = f'{self.base_url}{SlackMethods.team_profile_get}'
        return requests.post(url=url, cookies=self.cookies, headers=self.headers).json()

    def get_team_info(self):
        url = f'{self.base_url}{SlackMethods.team_info}'
        return requests.get(url=url, cookies=self.cookies, headers=self.headers).json()

    def update_profile(self, profile):
        url = f'{self.base_url}{SlackMethods.profile_set}'
        return requests.post(url=url, headers=self.headers, cookies=self.cookies, json={'profile': profile}).json()

    def update_section(self, user_id: str, section_id: str, element_id: str, text: str):
        url = f'{self.base_url}{SlackMethods.set_sections}'
        payload = {
            'token': self.token,
            'user': user_id,
            'section': section_id,
            'elements': json.dumps([{"element_id": element_id, "text": {"text": text}}]),
        }
        return requests.post(url=url, headers=self.headers, cookies=self.cookies, data=payload).json()

    def update_profile_photo(self, photo_url):
        url = f'{self.base_url}{SlackMethods.profile_set_photo}'
        with requests.get(photo_url) as img_resp:
            if img_resp.status_code != 200:
                raise Exception(f"Invalid url: {photo_url}")
            image = io.BytesIO(img_resp.content)

            files = {"image": image}
            headers = {"Authorization": f"Bearer {self.token}"}

            return requests.post(url=url, files=files, headers=headers, cookies=self.cookies).json()

    def get_conversations_list(self):
        payload = {'types': ','.join(["public_channel", "private_channel"])}
        base_url = f'{self.base_url}{SlackMethods.conversations_list}?limit=1000'
        page = requests.post(url=base_url, cookies=self.cookies, data=payload, headers=self.headers).json()
        result = page.copy()
        if page["ok"]:
            while page.get("response_metadata", {}).get("next_cursor"):
                url = base_url + f'&cursor={page.get("response_metadata", {}).get("next_cursor")}'
                page = requests.post(url=url, cookies=self.cookies, data=payload, headers=self.headers).json()
                if page['ok']:
                    result['channels'].extend(page['channels'])
            result["channels"] = [ch for ch in result["channels"]
                                  if ch.get('is_channel')
                                  and not ch.get('is_archived')
                                  and not ch.get('is_frozen')]

        return result

    def get_im_list(self):
        url = f'{self.base_url}{SlackMethods.conversations_list}?{self.__conversation_list_payload(["im"])}'
        return requests.get(url=url, cookies=self.cookies).json()

    def im_open(self, user: str):
        url = f'{self.base_url}{SlackMethods.conversations_open}?{self.__im_open_payload(user)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def delete_message(self, channel: str, id: str):
        url = f'{self.base_url}{SlackMethods.chat_delete}?{self.__delete_message_payload(channel, id)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def conversations_info(self, channel: str):
        url = f'{self.base_url}{SlackMethods.conversations_info}?{self.__conversation_info_payload(channel)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def update_message(self, channel: str, id: str, text: str, file_ids: str):
        url = f'{self.base_url}{SlackMethods.chat_update}?{self.__update_message_payload(channel, id, text, file_ids)}'
        return requests.post(url=url, cookies=self.cookies).json()

    def conversations_history(self, channel: str, id: str = None, date_from: datetime = None, date_to: datetime = None):
        payload = self.__conversation_history_payload(channel, id, date_from, date_to)
        base_url = f'{self.base_url}{SlackMethods.conversations_history}'
        page = requests.post(url=base_url, cookies=self.cookies, headers=self.headers, data=payload).json()

        result = page.copy()
        if page["ok"]:
            while page.get("response_metadata", {}).get("next_cursor"):
                url = base_url + f'?cursor={page.get("response_metadata", {}).get("next_cursor")}'
                page = requests.post(url=url, cookies=self.cookies, data=payload, headers=self.headers).json()
                if page['ok']:
                    result['messages'].extend(page['messages'])
        return result

    def conversations_replies(self, channel: str, id: str):
        url = f'{self.base_url}{SlackMethods.conversations_replies}?{self.__ts_payload(channel, id)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def post_message(self, channel: str, text: str, thread_ts: str = None):
        import uuid
        payload = {
            'channel': channel,
            'text': text,
            'client_msg_id': str(uuid.uuid4()),
            'thread_ts': thread_ts
        }
        url = f'{self.base_url}{SlackMethods.chat_post_message}'
        return requests.post(url=url, cookies=self.cookies, headers=self.headers, data=payload).json()

    def user_info(self, user: str):
        url = f'{self.base_url}{SlackMethods.users_info}?{self.__user_info_payload(user)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def get_reactions(self, channel: str, id: str):
        url = f'{self.base_url}{SlackMethods.reactions_get}?{self.__get_reactions_payload(channel, id)}'
        return requests.get(url=url, cookies=self.cookies).json()

    def check_email(self, email: str, user_agent: str) -> bool:
        payload = {'email': email}
        headers = {'User-Agent': user_agent}
        response = requests.post(f"{self.base_url}{SlackMethods.check_email}", data=payload, headers=headers)
        return response.json()['ok'] if response.status_code == 200 else False

    def confirm_email(self, email: str, user_agent: str, locale: str = 'en-US') -> bool:
        payload = {'email': email, 'locale': locale}
        headers = {'User-Agent': user_agent}
        response = requests.post(f"{self.base_url}{SlackMethods.confirm_email}", data=payload, headers=headers)
        result = response.json()['ok'] if response.status_code == 200 else False
        return result

    def confirm_code(self, email: str, code: str, user_agent: str) -> requests.Response:
        payload = {'email': email, 'code': code}
        headers = {'User-Agent': user_agent}
        return requests.post(f"{self.base_url}{SlackMethods.confirm_code}", data=payload, headers=headers)

    def find_workspaces(self, user_agent: str) -> requests.Response:
        headers = {'User-Agent': user_agent}
        response = requests.post(f"{self.base_url}{SlackMethods.find_workspaces}",
                                 cookies=self.cookies, headers=headers)
        return response

    def create_shared_invite(self):
        expiration = '36000'
        max_signups = '100'
        payload = {
            'expiration': expiration,
            'max_signups': max_signups
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{SlackMethods.create_shared_invite}", headers=headers,
                                 cookies=self.cookies, data=payload)
        return response

    def send_slack_invite_to_workspace(self, email):
        payload = {"invites": [{'email': email, "type": "regular", "mode": "manual"}]}
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{SlackMethods.send_invite_by_email}", headers=headers,
                                 cookies=self.cookies, json=payload)
        if not response.json()['ok']:
            payload = {"requests": payload["invites"]}
            response = requests.post(f"{self.base_url}{SlackMethods.alternative_invite_by_email}", headers=headers,
                                     cookies=self.cookies, json=payload)
        return response

    def test_auth(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.post(f"{self.base_url}{SlackMethods.auth_test}", headers=headers, cookies=self.cookies)

    def __user_info_payload(self, user):
        payload = {
            'token': self.token,
            'user': user
        }
        return parse.urlencode(payload)

    def __update_message_payload(self, channel, id, text, file_ids):
        payload = {
            'parse': 'none',
            'token': self.token,
            'channel': channel,
            'ts': id,
            'text': text,
            'file_ids': file_ids
        }
        return parse.urlencode(payload)

    def __conversation_info_payload(self, channel):
        payload = {
            'token': self.token,
            'channel': channel,
            'include_num_members': "true"
        }
        return parse.urlencode(payload)

    def __delete_message_payload(self, channel, id):
        payload = {
            'token': self.token,
            'channel': channel,
            'ts': id
        }
        return parse.urlencode(payload)

    def __conversation_list_payload(self, types: list):
        payload = {
            'token': self.token,
            'types': ','.join(types)
        }
        return parse.urlencode(payload)

    def __im_open_payload(self, user: str):
        payload = {
            'token': self.token,
            'users': user,
            'types': 'im'
        }
        return parse.urlencode(payload)

    def __channel_payload(self, channel, id=None):
        payload = {
            'token': self.token,
            'channel': channel
        }

        if id:
            payload["ts"] = id
            payload["limit"] = 1
            payload["inclusive"] = True

        return payload

    def __conversation_history_payload(self, channel, id=None, date_from: datetime=None, date_to: datetime=None):
        payload = {
            'token': self.token,
            'channel': channel
        }

        if id:
            payload["ts"] = id
            payload["limit"] = 1
            payload["inclusive"] = True

        if date_from:
            payload["oldest"] = date_from.timestamp()
        if date_to:
            payload["latest"] = date_to.timestamp()

        return payload

    def __ts_payload(self, channel: str, id: str):
        payload = {
            'token': self.token,
            'channel': channel,
            'ts': id
        }
        return parse.urlencode(payload)

    def __get_reactions_payload(self, channel, id):
        payload = {
            'token': self.token,
            'full': True,
            'channel': channel,
            'timestamp': id
        }
        return parse.urlencode(payload)
