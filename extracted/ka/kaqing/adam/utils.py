from abc import ABC
from contextlib import redirect_stdout
import copy
import csv
from datetime import datetime
import importlib
import io
import os
from pathlib import Path
import random
import string
from typing import Generic, TypeVar
from dateutil import parser
import subprocess
import sys
import time
import yaml
from prompt_toolkit.completion import Completer

from adam.config_holder import ConfigHolder
from adam.directories import creating_dir
from adam.utils_log import log2

from . import __version__

T = TypeVar('T')

NO_SORT = 0
SORT = 1
REVERSE_SORT = -1

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def convert_seconds(total_seconds_float):
    total_seconds_int = int(total_seconds_float)  # Convert float to integer seconds

    hours = total_seconds_int // 3600
    remaining_seconds_after_hours = total_seconds_int % 3600

    minutes = remaining_seconds_after_hours // 60
    seconds = remaining_seconds_after_hours % 60

    return hours, minutes, seconds

def epoch(timestamp_string: str):
    return parser.parse(timestamp_string).timestamp()

def elapsed_time(start_time: float):
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"

def duration(start_time: float, end_time: float = None):
    if not end_time:
        end_time = time.time()
    d = convert_seconds(end_time - start_time)
    t = []
    if d:
        t.append(f'{d[0]}h')
    if t or d[1]:
        t.append(f'{d[1]}m')
    t.append(f'{d[2]}s')

    return ' '.join(t)

def strip(lines):
    return '\n'.join([line.strip(' ') for line in lines.split('\n')]).strip('\n')

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1.
    If a key exists in both dictionaries and its value is a dictionary,
    the function recursively merges those nested dictionaries.
    Otherwise, values from dict2 overwrite values in dict1.
    """
    merged_dict = dict1.copy()  # Create a copy to avoid modifying original dict1

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, recursively merge them
            merged_dict[key] = deep_merge_dicts(merged_dict[key], value)
        elif key not in merged_dict or value:
            # Otherwise, overwrite or add the value from dict2
            if key in merged_dict and isinstance(merged_dict[key], Completer):
                pass
            else:
                merged_dict[key] = value
    return merged_dict

def deep_sort_dict(d):
    """
    Recursively sorts a dictionary by its keys, and any nested lists by their elements.
    """
    if not isinstance(d, (dict, list)):
        return d

    if isinstance(d, dict):
        return {k: deep_sort_dict(d[k]) for k in sorted(d)}

    if isinstance(d, list):
        return sorted([deep_sort_dict(item) for item in d])

def get_deep_keys(d, current_path=""):
    """
    Recursively collects all combined keys (paths) from a deep dictionary.

    Args:
        d (dict): The dictionary to traverse.
        current_path (str): The current path of keys, used for recursion.

    Returns:
        list: A list of strings, where each string represents a combined key path
            (e.g., "key1.subkey1.nestedkey").
    """
    keys = []
    for k, v in d.items():
        new_path = f"{current_path}.{k}" if current_path else str(k)
        if isinstance(v, dict):
            keys.extend(get_deep_keys(v, new_path))
        else:
            keys.append(new_path)
    return keys

def display_help(replace_arg = False):
    if not ConfigHolder().is_display_help:
        return

    args = copy.copy(sys.argv)
    if replace_arg:
        args[len(args) - 1] = '--help'
    else:
        args.extend(['--help'])
    subprocess.run(args)

def random_alphanumeric(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string.lower()

def json_to_csv(json_data: list[dict[any, any]], delimiter: str = ','):
    def flatten_json(y):
        out = {}
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x
        flatten(y)
        return out

    if not isinstance(json_data, list):
        json_data = [json_data]

    flattened_data = [flatten_json(record) for record in json_data]
    if flattened_data:
        keys = flattened_data[0].keys()
        header = io.StringIO()
        with redirect_stdout(header) as f:
            dict_writer = csv.DictWriter(f, keys, delimiter=delimiter)
            dict_writer.writeheader()
        body = io.StringIO()
        with redirect_stdout(body) as f:
            dict_writer = csv.DictWriter(f, keys, delimiter=delimiter)
            dict_writer.writerows(flattened_data)

        return header.getvalue().strip('\r\n'), [l.strip('\r') for l in body.getvalue().split('\n')]
    else:
        return None

def copy_config_file(rel_path: str, module: str, suffix: str = '.yaml', show_out = True):
    dir = creating_dir(f'{Path.home()}/.kaqing')
    path = f'{dir}/{rel_path}'
    if not os.path.exists(path):
        module = importlib.import_module(module)
        with open(path, 'w') as f:
            yaml.dump(module.config(), f, default_flow_style=False)
        if show_out and not idp_token_from_env():
            log2(f'Default {os.path.basename(path).split(suffix)[0] + suffix} has been written to {path}.')

    return path

def idp_token_from_env():
    return os.getenv('IDP_TOKEN')

def in_docker() -> bool:
    if os.path.exists('/.dockerenv'):
        return True

    try:
        with open('/proc/1/cgroup', 'rt') as f:
            for line in f:
                if 'docker' in line or 'lxc' in line:
                    return True
    except FileNotFoundError:
        pass

    return False

def bytes_generator_from_file(file_path, chunk_size=4096):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

class GeneratorStream(io.RawIOBase):
    def __init__(self, generator):
        self._generator = generator
        self._buffer = b''  # Buffer to store leftover bytes from generator yields

    def readable(self):
        return True

    def _read_from_generator(self):
        try:
            chunk = next(self._generator)
            if isinstance(chunk, str):
                chunk = chunk.encode('utf-8')  # Encode if generator yields strings
            self._buffer += chunk
        except StopIteration:
            pass  # Generator exhausted

    def readinto(self, b):
        # Fill the buffer if necessary
        while len(self._buffer) < len(b):
            old_buffer_len = len(self._buffer)
            self._read_from_generator()
            if len(self._buffer) == old_buffer_len:  # Generator exhausted and buffer empty
                break

        bytes_to_read = min(len(b), len(self._buffer))
        b[:bytes_to_read] = self._buffer[:bytes_to_read]
        self._buffer = self._buffer[bytes_to_read:]
        return bytes_to_read

    def read(self, size=-1):
        if size == -1:  # Read all remaining data
            while True:
                old_buffer_len = len(self._buffer)
                self._read_from_generator()
                if len(self._buffer) == old_buffer_len:
                    break
            data = self._buffer
            self._buffer = b''
            return data
        else:
            # Ensure enough data in buffer
            while len(self._buffer) < size:
                old_buffer_len = len(self._buffer)
                self._read_from_generator()
                if len(self._buffer) == old_buffer_len:
                    break

            data = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return data

class ExecResult(ABC):
    def exit_code(self) -> int:
        pass

    def cat_log_file_cmd(self) -> str:
        pass

    def get_job_id(self) -> str:
        pass

    def header(self) -> str:
        pass

class Holder(Generic[T]):
    def __init__(self, obj: T = None):
        self.obj = obj

    def get(self) -> T:
        return self.obj

    def set(self, obj: T):
        self.obj = obj