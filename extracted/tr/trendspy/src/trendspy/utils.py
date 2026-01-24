from collections import OrderedDict
from typing import Any
import re
import json
from enum import Enum
from datetime import datetime, timedelta, timezone
import time

_HEX_TO_CHAR_DICT = {
	r'\x7b':'{',
	r'\x7d':'}',
	r'\x22':'"',
	r'\x5d':']',
	r'\x5b':'[',
		'\\\\':'\\'
}
_tag_pattern = re.compile(r'<([\w:]+)>(.*?)</\1>', re.DOTALL)

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

class LRUCache(OrderedDict):
    def __init__(self, maxsize=128):
        super().__init__()
        self.maxsize = maxsize

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]

def ensure_list(item):
	return list(item) if hasattr(item, '__iter__') and not isinstance(item, str) and not isinstance(item, dict) else [item]

def extract_column(data, column, default: Any = None, f=None):
	if f is None:
		return [item.get(column, default) for item in data]
	return [f(item.get(column, default)) for item in data]

def flatten_data(data, columns):
    return [{**{kk: vv for k in columns if k in d for kk, vv in d[k].items()},
             **{k: v for k, v in d.items() if k not in columns}} 
            for d in data]

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def filter_data(data, desired_columns):
	desired_columns = set(desired_columns)
	return [{k: v for k, v in item.items() if k in desired_columns} for item in data]

def decode_escape_text(text):
	for k,v in _HEX_TO_CHAR_DICT.items():
		text = text.replace(k, v)
		
	if r'\x' in text:
		text = re.sub(r'\\x[0-9a-fA-F]{2}', lambda match:chr(int(match.group(0)[2:], 16)), text)
	return text

def parse_xml_to_dict(text, prefix=''):
	item_dict = {}
	for tag, content in _tag_pattern.findall(text):
		content = parse_xml_to_dict(content.strip(), tag+'_')
		tag = tag.replace(prefix, '')
		if tag in item_dict:
			if not isinstance(item_dict[tag], list):
				item_dict[tag] = [item_dict[tag]]
			item_dict[tag].append(content)
			continue
		item_dict[tag] = content
	if not item_dict:
		return text
	return item_dict

def get_utc_offset_minutes():
    """
    Returns the local time offset from UTC in minutes.
    Positive values for time zones ahead of UTC (eastward),
    negative values for time zones behind UTC (westward).
    """
    # Get current local time
    now = datetime.now()
    
    # Get offset in seconds
    utc_offset = -time.timezone
    
    # Account for daylight saving time if active
    if time.localtime().tm_isdst:
        utc_offset += 3600  # Add one hour in seconds
    
    # Convert seconds to minutes
    return utc_offset // 60

def parse_time_ago(time_ago):
	if not time_ago:
		return None
	
	match = re.match(r'(\d+)\s*(\w+)', time_ago)
	if not match:
		return None
	
	value, unit = match.groups()
	value = int(value)

	if 'h' in unit:
		delta = timedelta(hours=value)
	elif 'd' in unit:
		delta = timedelta(days=value)
	elif 'm' in unit:
		delta = timedelta(minutes=value)
	else:
		delta = timedelta(0)

	now = datetime.now(timezone.utc)
	timestamp = int((now - delta).replace(microsecond=0).timestamp())
	return timestamp

def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length - 3] + '...'
    return s