from aiohttp import ClientSession, ClientResponseError
from poolsense.exceptions import PoolSenseError


class PoolSense:
    """Main Interface to the Poolsense Device"""

    def __init__(self, session: ClientSession, email, password, deviceId):
        self._version = "0.1.0"
        self._url_login = 'https://api.poolsense.net/api/v1/users/login'
        self._email = email
        self._password = password
        self._session = session
        self._deviceId = deviceId

    async def test_poolsense_credentials(self):
        """Function tests the credentials against the Poolsense Servers"""
        
        LOGIN_DATA = {
            "email": self._email,
            "password": self._password,
            "uuid": "26aab38027422a59",
            "registrationId": "c5tknccIS_I:APA91bF0LS4mAR2NETBJ9tNFYEbvUgileRovnuC1Y9-yTy2qDsW4_YHlDcapH7BnHWzxh74fPVJw0Y9KuM3sCVIWknSOlGu3WP0QNSFzfuhEwQ_yBujt9cSVak0eVUo_IfmFf6rtlng_"
        }

        # """Login to the system."""
        resp = await self._session.post(self._url_login, json=LOGIN_DATA)
        if resp.status == 200:
            data = await resp.json(content_type=None)
            if data["token"] is None:
                return False
            else:
                if len(data["devices"]) > 0:
                    return data["devices"][0]["serial"]
                return "DEMO"
        else:
            return False


    async def get_poolsense_data(self):
        """Function gets all the data for this user account from the Poolsense servers"""
        LOGIN_DATA = {
            "email": self._email,
            "password": self._password,
            "uuid": "26aab38027422a59",
            "registrationId": "c5tknccIS_I:APA91bF0LS4mAR2NETBJ9tNFYEbvUgileRovnuC1Y9-yTy2qDsW4_YHlDcapH7BnHWzxh74fPVJw0Y9KuM3sCVIWknSOlGu3WP0QNSFzfuhEwQ_yBujt9cSVak0eVUo_IfmFf6rtlng_"
        }

        results = {
            "Chlorine": 0,
            "pH": 0,
            "Water Temp": 0,
            "Chlorine Instant": 0,
            "pH Instant": 0,
            "Water Temp Instant": 0,
            "Battery": 0,
            "Last Seen": 0,
            "Chlorine High": 0,
            "Chlorine Low": 0,
            "pH High": 0,
            "pH Low": 0,
            "pH Status": 0,
            "Chlorine Status": 0
        }

        # """Login to the system."""
        resp = await self._session.post(self._url_login, json=LOGIN_DATA)
        if resp.status == 200:
            data = await resp.json(content_type=None)

            URL_DATA = 'https://api.poolsense.net/api/v1/sigfoxData/app/' + data['devices'][0]["serial"] + '/?tz=-120'
            if self._deviceId:
                URL_DATA = 'https://api.poolsense.net/api/v1/sigfoxData/app/' + self._deviceId + '/?tz=-120'
            head = {'Authorization': 'token {}'.format(data["token"])}

            #
            resp = await self._session.get(URL_DATA, headers=head)
            if resp.status == 200:
                data = await resp.json(content_type=None)
                
                results = {
                    "Chlorine": data["ORP"],
                    "pH": data["pH"],
                    "Water Temp": data["waterTemp"],
                    "Chlorine Instant": data["lastData"]["ORP"],
                    "pH Instant": data["lastData"]["pH"],
                    "Water Temp Instant": data["lastData"]["waterTemp"],
                    "Battery": data["vBat"],
                    "Last Seen": data["lastData"]["time"],
                    "Chlorine High": data["display"]["orpNotificationMax"],
                    "Chlorine Low": data["display"]["orpNotificationMin"],
                    "pH High": data["display"]["phNotificationMax"],
                    "pH Low": data["display"]["phNotificationMin"],
                    "pH Status": data["display"]["pHColor"],
                    "Chlorine Status": data["display"]["ORPColor"]
                }
            else:
                raise PoolSenseError(resp.status,"Server error.")
        else:
            raise PoolSenseError(resp.status,"Login failed.")

        return results
