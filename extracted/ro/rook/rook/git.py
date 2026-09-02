import os
import re

GIT_FOLDER = '.git'
GIT_HEAD = 'HEAD'
GIT_CONFIG = 'config'


def is_git(path):
    return os.path.isdir(os.path.join(path, GIT_FOLDER))


def find_root(path):
    if is_git(path):
        return path
    else:
        next_path = os.path.dirname(path)
        if next_path != path:
            return find_root(next_path)
        else:
            return None


def get_revision(path):
    return follow_sym_links(os.path.join(path, GIT_FOLDER), GIT_HEAD)


def get_remote_url(path):
    with open(os.path.join(path, GIT_FOLDER, GIT_CONFIG)) as config_file:
        config = config_file.read()

    remote_name = get_remote_name(path, config)
    match = re.search(r'\[remote "' + remote_name + '"\]\s*url\s*=\s(?P<url>\S*)', config)
    if match and len(match.groups()) == 1:
        return match.group(1)
    else:
        return ''


def get_remote_name(path, config):
    with open(os.path.join(path, GIT_FOLDER, GIT_HEAD)) as head:
        head_content = head.read()
    if not head_content.startswith("ref:"):
        return 'origin'
    branch = head_content.split('ref: refs/heads/')[1].strip()

    match = re.search(r'\[branch "' + branch + '"\]\s*remote\s*=\s(?P<remote>\S*)', config)
    if match and len(match.groups()) == 1:
        return match.group(1)
    else:
        return 'origin'


def follow_sym_links(root, link):
    with open(os.path.join(root, link), 'r') as f:
        content = f.read()

    if content.startswith("ref:"):
        next_link = content.split(' ')[1].strip()
        return follow_sym_links(root, next_link)
    else:
        return content.strip()
