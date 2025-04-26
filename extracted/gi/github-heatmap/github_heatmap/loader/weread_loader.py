import pendulum
import requests
import os

from github_heatmap.loader.base_loader import BaseLoader
from github_heatmap.loader.config import WEREAD_BASE_URL, WEREAD_HISTORY_URL


class WereadLoader(BaseLoader):
    track_color = "#2EA8F7"
    unit = "mins"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.weread_cookie = kwargs.get("weread_cookie", "")
        if not self.weread_cookie:
            self.weread_cookie = self.get_cookie()
        self.session = requests.Session()
        self._make_years_list()

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--weread_cookie",
            dest="weread_cookie",
            type=str,
            required=False,
            help="",
        )

    def get_cookie(self):
        url = os.getenv("CC_URL")
        if not url:
            url = "https://cookiecloud.malinkang.com/"
        id = os.getenv("CC_ID")
        password = os.getenv("CC_PASSWORD")
        cookie = os.getenv("WEREAD_COOKIE")
        if url and id and password:
            cookie = self.try_get_cloud_cookie(url, id, password)
        if not cookie or not cookie.strip():
            raise Exception("没有找到cookie，请按照文档填写cookie")
        return cookie
    
    def try_get_cloud_cookie(self,url, id, password):
        if url.endswith("/"):
            url = url[:-1]
        req_url = f"{url}/get/{id}"
        data = {"password": password}
        result = None
        response = requests.post(req_url, data=data)
        if response.status_code == 200:
            data = response.json()
            cookie_data = data.get("cookie_data")
            if cookie_data and "weread.qq.com" in cookie_data:
                cookies = cookie_data["weread.qq.com"]
                cookie_str = "; ".join(
                    [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
                )
                result = cookie_str
        return result
    
    def get_api_data(self):
        self.session.get(WEREAD_BASE_URL)
        r = self.session.get(WEREAD_HISTORY_URL)
        if not r.ok:
            print(r.text)
            # need to refresh cookie
            if r.json()["errcode"] == -2012:
                raise Exception("Cookie过期了请重新设置cookie")
            else:
                raise Exception("Can not get weread history data")
        return r.json()

    def make_track_dict(self):
        api_data = self.get_api_data()
        if("readTimes" in api_data):
            readTimes = dict(sorted(api_data["readTimes"].items(), reverse=True))
            for k, v in readTimes.items():
                k = pendulum.from_timestamp(int(k), tz=self.time_zone)
                self.number_by_date_dict[k.to_date_string()] = round(v / 60.0, 2)
            for _, v in self.number_by_date_dict.items():
                self.number_list.append(v)

    def get_all_track_data(self):
        self.session.cookies = self.parse_cookie_string(self.weread_cookie)
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
