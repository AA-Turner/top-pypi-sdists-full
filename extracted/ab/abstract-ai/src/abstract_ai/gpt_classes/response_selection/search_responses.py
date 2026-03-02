import os
import re
from collections import defaultdict
from abstract_utilities import *
from abstract_solcatcher_database import get_timestamp_from_data

class PathManager:
    @staticmethod
    def get_abs_path():
        return os.path.abspath(__file__)

    @staticmethod
    def get_abs_dir():
        return os.path.dirname(PathManager.get_abs_path())

    @staticmethod
    def create_abs_path(relative_path):
        return os.path.join(PathManager.get_abs_dir(), relative_path)

    @staticmethod
    def search_for_file(filename, base_dirs):
        for base in base_dirs:
            for root, _, files in os.walk(base):
                if filename in files:
                    return os.path.join(root, filename)
        return None

    @staticmethod
    def get_conversation_path():
        filename = 'conversations.json'
        for location in [PathManager.get_abs_dir(), os.getcwd(), os.path.expanduser('~/Documents')]:
            candidate = os.path.join(location, filename)
            if os.path.isfile(candidate):
                return candidate
        # Recursive search
        found = PathManager.search_for_file(filename, [os.path.expanduser('~/Documents')])
        if found:
            return found
        raise FileNotFoundError(f"'{filename}' not found.")


def get_convo_path(file_path=None):
    return file_path or PathManager.get_conversation_path()


def get_conversation_data(file_path=None):
    return safe_read_from_json(get_convo_path(file_path))


class ConversationManager(metaclass=SingletonMeta):
    def __init__(self, file_path=None):
        self.original_file_path = file_path
        self.convo_path = get_convo_path(file_path)
        self.conversation_data = get_conversation_data(self.convo_path)


def get_conversation_manager(file_path=None):
    return ConversationManager(file_path=file_path)


def get_convo_data(file_path=None):
    return get_conversation_manager(file_path).conversation_data

def get_parts(data):
    parts = []
    for path in find_paths_to_key(json_data=data, key_to_find="message"):
        message_value = get_value_from_path(data, path)
        for sub_path in find_paths_to_key(message_value, 'parts'):
            parts_value = get_value_from_path(message_value, sub_path)
            parts.extend([p for p in parts_value if p])
    return parts

def split_language(text, **lang_flags):
    enabled_aliases = {
        'js': ['js', 'javascript'],
        'ts': ['ts', 'typescript'],
        'python': ['py', 'python'],
        'html': ['html'],
        'bash': ['bash', 'sh'],
        # Add more as needed
    }

    enabled = []
    for lang, active in lang_flags.items():
        if active and lang in enabled_aliases:
            enabled.extend(enabled_aliases[lang])

    if not enabled:
        return {}

    pattern = re.compile(rf'```(?:{"|".join(enabled)})\s*(.*?)```', re.DOTALL)
    results = defaultdict(list)

    for match in pattern.findall(text):
        for lang, aliases in enabled_aliases.items():
            if any(match.startswith(alias) for alias in aliases):
                results[lang].append(match.strip())
                break

    return dict(results)

def search_in_conversation(strings=None, *args, **kwargs):
    strings = make_list(strings or '')
    timestamp = get_timestamp_from_data(kwargs)
    before = kwargs.get('before', True)
    file_path = kwargs.get('file_path')

    convo_data = get_convo_data(file_path)
    raw_results = []

    for convo in convo_data:
        create_time = make_list(get_any_value(convo, 'create_time'))[0]
        if is_valid_time(create_time, timestamp, before):
            parts = get_parts(convo)
            matched = is_strings_in_string(strings, parts)
            if matched:
                raw_results.append(matched)

    # Language filtering
    requested_langs = [
        lang for lang in ['neither', 'uncertain', 'javascript','typescript', 'python', 'bash', 'html', 'php']
        if if_true_get_string(kwargs, lang)
    ]
    split_requested = kwargs.get('split_code', False)

    if requested_langs:
        filtered = search_code(requested_langs, raw_results)
        if split_requested:
            split_by_lang = defaultdict(list)
            for chunk in filtered:
                split_result = split_language(chunk, **{lang: True for lang in requested_langs})
                for lang, blocks in split_result.items():
                    split_by_lang[lang].extend(blocks)
            return dict(split_by_lang)
        return filtered

    return raw_results
