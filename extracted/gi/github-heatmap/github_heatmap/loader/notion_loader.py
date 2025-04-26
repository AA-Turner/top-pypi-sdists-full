from datetime import datetime, timedelta
import time
from collections import defaultdict

import pendulum
import requests
import json

from github_heatmap.loader.base_loader import BaseLoader, LoadError
from github_heatmap.loader.config import NOTION_API_URL, NOTION_API_VERSION


class NotionLoader(BaseLoader):
    track_color = "#40C463"
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = self.generate_date_dict(from_year, to_year)
        self.notion_token = kwargs.get("notion_token", "").strip()
        self.database_id = kwargs.get("database_id", "").strip()
        self.date_prop_name = kwargs.get("date_prop_name", "")
        self.value_prop_name = kwargs.get("value_prop_name", "")
        self.database_filter = kwargs.get("database_filter", "")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--notion_token",
            dest="notion_token",
            type=str,
            help="The Notion internal integration token.",
        )
        parser.add_argument(
            "--database_id",
            dest="database_id",
            type=str,
            help="The Notion database id.",
        )
        parser.add_argument(
            "--date_prop_name",
            dest="date_prop_name",
            type=str,
            default="Datetime",
            required=optional,
            help="The database property name which stored the datetime.",
        )
        parser.add_argument(
            "--value_prop_name",
            dest="value_prop_name",
            type=str,
            default="Datetime",
            required=optional,
            help="The database property name which stored the datetime.",
        )        
        parser.add_argument(
            "--database_filter",
            dest="database_filter",
            type=str,
            default="",
            required=False,
            help="The database property name which stored the datetime.",
        )

    def get_api_data(self, start_cursor="", page_size=100, data_list=[]):
        payload = {
            "page_size": page_size,
            "filter": {
                "and": [
                    {
                        "property": self.date_prop_name,
                        "date": {"on_or_after": f"{self.from_year}-01-01"},
                    },
                    {
                        "property": self.date_prop_name,
                        "date": {"on_or_before": f"{self.to_year}-12-31"},
                    },
                ]
            },
        }
        if self.database_filter:
            payload["filter"]["and"].append(json.loads(self.database_filter))
        if start_cursor:
            payload.update({"start_cursor": start_cursor})

        headers = {
            "Accept": "application/json",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.notion_token,
        }

        resp = requests.post(
            NOTION_API_URL.format(database_id=self.database_id),
            json=payload,
            headers=headers,
        )
        if not resp.ok:
            raise LoadError("Can not get Notion data, please check your config")
        data = resp.json()
        results = data["results"]
        next_cursor = data["next_cursor"]
        data_list.extend(results)
        if not data["has_more"]:
            return data_list
        # Avoid request limits
        # The rate limit for incoming requests is an average
        # of 3 requests per second.
        # See https://developers.notion.com/reference/request-limits
        time.sleep(0.3)
        return self.get_api_data(
            start_cursor=next_cursor, page_size=page_size, data_list=data_list
        )

    def generate_date_dict(self, start_year, end_year):
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        # 使用字典推导式生成日期字典
        return {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): 0
            for i in range((end_date - start_date).days + 1)
        }

    def make_track_dict(self):
        data_list = self.get_api_data()
        for result in data_list:
            date = result["properties"][self.date_prop_name]["date"]
            value = result["properties"][self.value_prop_name]
            if date and value:
                dt = date.get("start")
                type = value.get("type")
                if type == "formula" and value.get(type).get("type") == "number":
                    value = float(value.get(type).get("number"))
                elif type == "rollup" and value.get(type).get("type") == "number":
                    value = float(value.get(type).get("number"))
                else:
                    value = value.get(type)
                date_str = pendulum.parse(dt).to_date_string()
                self.number_by_date_dict[date_str] = (
                    self.number_by_date_dict.get(date_str, 0) + value
                )
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
