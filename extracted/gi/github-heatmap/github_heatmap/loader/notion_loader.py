import argparse
import json
import time
import warnings
from collections import defaultdict
from datetime import datetime, timedelta

import pendulum
import requests

from github_heatmap.loader.base_loader import BaseLoader
from github_heatmap.loader.config import NOTION_API_URL, NOTION_API_VERSION


class NotionLoader(BaseLoader):
    track_color = "#40C463"
    unit = "times"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = self.generate_date_dict(from_year, to_year)
        self.notion_token = (kwargs.get("notion_token") or "").strip()
        self.data_source_id = (kwargs.get("data_source_id") or "").strip()
        deprecated_database_id = (kwargs.get("database_id") or "").strip()
        if deprecated_database_id and not self.data_source_id:
            warnings.warn(
                "--database_id is deprecated; use --data_source_id instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            self.data_source_id = deprecated_database_id
        self.date_prop_name = kwargs.get("date_prop_name") or ""
        self.value_prop_name = kwargs.get("value_prop_name") or ""
        self.data_source_filter = kwargs.get("data_source_filter") or ""
        deprecated_database_filter = kwargs.get("database_filter") or ""
        if deprecated_database_filter and not self.data_source_filter:
            warnings.warn(
                "--database_filter is deprecated; use --data_source_filter instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            self.data_source_filter = deprecated_database_filter
        self.tooltip_prop_name = (kwargs.get("tooltip_prop_name") or "").strip()
        self.tooltip_by_date_dict = defaultdict(list)

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--notion_token",
            dest="notion_token",
            type=str,
            help="The Notion internal integration token.",
        )
        parser.add_argument(
            "--data_source_id",
            dest="data_source_id",
            type=str,
            help="The Notion data source id.",
        )
        parser.add_argument(
            "--database_id",
            dest="database_id",
            type=str,
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "--date_prop_name",
            dest="date_prop_name",
            type=str,
            default="Datetime",
            required=optional,
            help="The Notion data source property name that stores the date.",
        )
        parser.add_argument(
            "--value_prop_name",
            dest="value_prop_name",
            type=str,
            default="Datetime",
            required=optional,
            help="The Notion data source property name used as the heatmap value.",
        )
        parser.add_argument(
            "--data_source_filter",
            dest="data_source_filter",
            type=str,
            default="",
            required=False,
            help="Optional Notion data source query filter in JSON format.",
        )
        parser.add_argument(
            "--database_filter",
            dest="database_filter",
            type=str,
            default="",
            required=False,
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "--tooltip_prop_name",
            dest="tooltip_prop_name",
            type=str,
            default="",
            required=False,
            help="The Notion property name used for tooltip text.",
        )

    def get_api_data(self, start_cursor="", page_size=100, data_list=None):
        if data_list is None:
            data_list = []
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
        if self.data_source_filter:
            payload["filter"]["and"].append(json.loads(self.data_source_filter))
        if start_cursor:
            payload.update({"start_cursor": start_cursor})
        headers = {
            "Accept": "application/json",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.notion_token,
        }
        try:
            resp = requests.post(
                NOTION_API_URL.format(data_source_id=self.data_source_id),
                json=payload,
                headers=headers,
            )
        except requests.RequestException:
            print("Failed to connect to Notion API.")
            return data_list
        if not resp.ok:
            # Treat non-OK responses as an empty result set so we can still draw
            # a heatmap even when the Notion API yields no rows for the period.
            return data_list
        try:
            data = resp.json()
        except ValueError:
            return data_list
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
            tooltip_text = ""
            if self.tooltip_prop_name:
                tooltip_prop = result["properties"].get(self.tooltip_prop_name)
                tooltip_text = self._extract_property_text(tooltip_prop)
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
                if tooltip_text:
                    self.tooltip_by_date_dict[date_str].append(tooltip_text.strip())
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)
        for key, texts in list(self.tooltip_by_date_dict.items()):
            joined = "\n".join(filter(None, [t.strip() for t in texts if t]))
            if joined:
                self.tooltip_by_date_dict[key] = joined
            else:
                self.tooltip_by_date_dict.pop(key, None)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list

    @staticmethod
    def _format_date(date_dict):
        if not date_dict:
            return ""
        start = date_dict.get("start")
        end = date_dict.get("end")
        if start and end and start != end:
            return f"{start} - {end}"
        return start or end or ""

    @staticmethod
    def _join_plain_text(items):
        if not items:
            return ""
        return "".join([item.get("plain_text", "") for item in items]).strip()

    @classmethod
    def _extract_rollup_item(cls, item):
        if not item:
            return ""
        item_type = item.get("type")
        if item_type in ("title", "rich_text"):
            return cls._join_plain_text(item.get(item_type))
        if item_type == "people":
            return ", ".join(
                [p.get("name") or p.get("id", "") for p in item.get("people", [])]
            ).strip()
        if item_type == "relation":
            return ", ".join(
                [r.get("id", "") for r in item.get("relation", [])]
            ).strip()
        if item_type == "date":
            return cls._format_date(item.get("date", {}))
        if item_type in ("url", "email", "phone_number"):
            return item.get(item_type) or ""
        if item_type == "number":
            number_value = item.get("number")
            return "" if number_value is None else str(number_value)
        if item_type == "checkbox":
            value = item.get("checkbox")
            if value is None:
                return ""
            return "Yes" if value else "No"
        if item_type == "formula":
            return cls._extract_property_text(
                {"type": "formula", "formula": item.get("formula", {})}
            )
        if item_type == "rollup":
            return cls._extract_property_text(
                {"type": "rollup", "rollup": item.get("rollup", {})}
            )
        return ""

    @classmethod
    def _extract_property_text(cls, prop):
        if not prop:
            return ""
        prop_type = prop.get("type")
        if not prop_type:
            return ""
        if prop_type in ("title", "rich_text"):
            return cls._join_plain_text(prop.get(prop_type))
        if prop_type == "multi_select":
            return ", ".join(
                [item.get("name", "") for item in prop.get("multi_select", []) if item]
            ).strip()
        if prop_type in ("select", "status"):
            option = prop.get(prop_type) or {}
            return option.get("name", "") if option else ""
        if prop_type in ("url", "email", "phone_number"):
            return prop.get(prop_type) or ""
        if prop_type == "checkbox":
            value = prop.get("checkbox")
            if value is None:
                return ""
            return "Yes" if value else "No"
        if prop_type == "number":
            number_value = prop.get("number")
            return "" if number_value is None else str(number_value)
        if prop_type == "people":
            return ", ".join(
                [p.get("name") or p.get("id", "") for p in prop.get("people", [])]
            ).strip()
        if prop_type in ("created_time", "last_edited_time"):
            return prop.get(prop_type) or ""
        if prop_type in ("created_by", "last_edited_by"):
            person = prop.get(prop_type)
            if isinstance(person, dict):
                return person.get("name") or person.get("id", "") or ""
            return ""
        if prop_type == "date":
            return cls._format_date(prop.get("date", {}))
        if prop_type == "relation":
            return ", ".join(
                [r.get("id", "") for r in prop.get("relation", [])]
            ).strip()
        if prop_type == "files":
            texts = []
            for file_obj in prop.get("files", []):
                name = file_obj.get("name")
                if name:
                    texts.append(name)
                    continue
                file_url = file_obj.get("file", {}).get("url")
                external_url = file_obj.get("external", {}).get("url")
                texts.append(file_url or external_url or "")
            return ", ".join([t for t in texts if t]).strip()
        if prop_type == "formula":
            formula = prop.get("formula", {})
            formula_type = formula.get("type")
            if formula_type in ("string", "url", "email", "phone_number"):
                return formula.get(formula_type) or ""
            if formula_type == "boolean":
                value = formula.get("boolean")
                if value is None:
                    return ""
                return "Yes" if value else "No"
            if formula_type == "number":
                number_value = formula.get("number")
                return "" if number_value is None else str(number_value)
            if formula_type == "date":
                return cls._format_date(formula.get("date", {}))
        if prop_type == "rollup":
            rollup = prop.get("rollup", {})
            rollup_type = rollup.get("type")
            if rollup_type == "number":
                number_value = rollup.get("number")
                return "" if number_value is None else str(number_value)
            if rollup_type == "date":
                return cls._format_date(rollup.get("date", {}))
            if rollup_type == "array":
                texts = [
                    cls._extract_rollup_item(item) for item in rollup.get("array", [])
                ]
                texts = [text for text in texts if text]
                return ", ".join(texts)
        return ""
