import fnmatch
import hashlib
import pathspec
import mimetypes
import os
import pathlib
import shutil
from base64 import b64decode
from os import path, walk
from pathlib import Path

import pkg_resources
import requests
from Crypto.Cipher import AES

DIGEST_SHA256 = "sha256"
DIGEST_SHA1 = "sha1"
DEFAULT_DIGEST = DIGEST_SHA1


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def path_is_wildcard(unix_path):
    """
    Returns whether the provided path is a unix path wildcard
    @param unix_path: [String] The path to check
    @return: [Boolean]
    """
    return any(wildcard in unix_path for wildcard in ["*", "?"])


def build_cnvrgignore_spec(root_path=None):
    """
    Return a gitignore pattern matcher
    @param root_path: Root path of the project/dataset
    @return: [PathSpec] a spec object used to match files
    """
    cnvrgignore_path = os.path.join(root_path, '.cnvrgignore')
    rules = ['.cnvrg/', '.tmp/']
    if os.path.exists(cnvrgignore_path):
        with open(cnvrgignore_path, 'r') as f:
            rules += f.readlines()

    spec = pathspec.PathSpec.from_lines('gitwildmatch', rules)
    return spec


def match_mimetypes(filters, path):
    """
    mimetypes for files will return in the following format: "TYPE/EXACT_TYPE", for ex. 'image/jpeg'
    This function will receive general types in the filters list (for ex. ['image']), and will only return
    True for files that match any of the filters
    @param filters: [List] Allowed file types.
    @param path: [String] File to test against filters
    @return: [Boolean] True if the path matches one of the filters, False otherwise
    """
    # This means we have no filters
    if not filters:
        return True

    # This means its a directory / file without extension
    if not mimetypes.guess_type(path)[0]:
        return False

    mime_type = mimetypes.guess_type(path)[0].split('/')[0]
    return mime_type in filters


def decrypt(key, iv, secret):
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, b64decode(iv.encode("utf8")))
    secret = b64decode(secret.encode("utf-8"))
    return unpad(cipher.decrypt(secret).decode('utf8'))


def download_file(file_url, file_path):
    """
    Download a file from the provided url and saves it to the requested path
    @param file_url: The URL from which the file will be downloaded
    @param file_path: The target path to which we want to save the file
    @return: None
    """
    sts_file = requests.get(file_url, verify=False)
    create_dir_if_not_exists(file_path)
    with open(file_path, 'wb') as f:
        f.write(sts_file.content)


def create_dir_if_not_exists(local_path):
    """
    Checks if the given file path directory exists and creates it if not.
    @param local_path: File path
    @return: None
    """
    dir_path = os.path.dirname(local_path)
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def get_relative_path(full_path):
    """
    Returns file relative path without '.' suffix
    @param full_path: Path string
    @return: String
    """
    if full_path.startswith("./"):
        full_path = full_path[2:]
    return full_path


def append_trailing_slash(path):
    """
    Appends trailing slash to path - used to differentiate files from directories
    @param path: String representing the directory path
    @return: String
    """
    return path if path.endswith("/") else "{}/".format(path)


def create_cnvrgignore(path):
    """
    Creates .cnvrgignore file in the root project/dataset
    @param path: Root path of the project/dataset
    @return: None
    """
    cnvrg_ignore = pkg_resources.resource_filename('cnvrgv2', 'utils/files/.cnvrgignore')
    shutil.copyfile(cnvrg_ignore, os.path.join(path, '.cnvrgignore'))


def get_cnvrgignore_rules(path):
    """
    Return list of rules after parsing the cnvrgignore file
    @param path: Root path of the project/dataset
    @return: [List] of rules
    """
    cnvrgignore_path = os.path.join(path, '.cnvrgignore')
    rules = ['.cnvrg/', '.tmp/']
    if not os.path.exists(cnvrgignore_path):
        return rules
    with open(cnvrgignore_path, 'r') as f:
        for line in f.readlines():
            if line.startswith("#") or line in ['\n', '\r\n']:
                continue
            rules.append(line.strip())
    return rules


def match_ignore(path, project_root):
    """
    Checks if path match any of the rules
    @param path: file path
    @param project_root: Root path of the project/dataset
    @return: [Bool] true if match rule , false if path didnt match any rules
    """
    rules = get_cnvrgignore_rules(project_root)
    for rule in rules:
        if rule.endswith("/"):
            if pathlib.PurePath(path).match(rule + '*'):
                return True
            elif path.startswith(rule):
                return True
        if pathlib.PurePath(path).match(rule):
            return True
    return False


def cnvrgignore_exists(path):
    """
    Check if .cnvrgignore file exists in project/dataset root path.
    @param path: Root path of the project/dataset
    @return: Bool
    """
    return os.path.exists(os.path.join(path, '.cnvrgignore'))


def get_files_and_dirs_recursive(
    root_dir=".",
    regex="*",
    project_root="",
    filters=None,
    force=False
):
    """
    Recursively traverse a given directory and get all of the relevant files and folders within
    @param root_dir: String representing the directory path
    @param regex: String representing the regex to filter out files/folders
    @param project_root: String representing the project root path
    @param force: Get all files and dirs regardless of .cnvrgignore rules. E.g, used to get .tmp folder
    @return: List
    """
    project_root = append_trailing_slash(project_root) if project_root else ''
    full_paths = []

    for root, dirs, files in walk(root_dir, topdown=False, followlinks=True):
        for name in files:
            file_path = get_relative_path(path.join(root, name)).replace(project_root, "")
            if not force and match_ignore(file_path, project_root):
                continue
            full_paths.append(file_path)
        for name in dirs:
            dir_path = append_trailing_slash(get_relative_path(path.join(root, name))
                                             .replace(project_root, ""))
            if not force and match_ignore(dir_path, project_root):
                continue
            full_paths.append(dir_path)

    # Add the folder itself, if it's an empty one
    if os.path.isdir(root_dir) and len(os.listdir(root_dir)) == 0:
        dir_path = append_trailing_slash(get_relative_path(root_dir).replace(project_root, ""))
        full_paths.append(dir_path)

    if regex:
        full_paths = fnmatch.filter(full_paths, regex)

    if filters:
        full_paths = [item for item in full_paths if match_mimetypes(filters, item)]

    return full_paths


def chunk_list(list, size):
    """
    Chunks a given list into equally sized chunks (except last chunk)
    @param list: List we want to chunk
    @param size: Integer representing the chunk size
    @return: List of lists
    """
    chunks = []
    for i in range(0, len(list), size):
        chunks.append(list[i:i + size])
    return chunks


def get_file_sha(full_path, digest):
    """
    Calculates the file SHA1 using its content
    @param full_path: String representing the file path
    @return: String
    """
    BUF_SIZE = 65536

    if digest not in [None, DIGEST_SHA256, DIGEST_SHA1]:
        raise ValueError(f"Unsupported digest algorithm. Use {DIGEST_SHA256}, {DIGEST_SHA1}, or None.")

    hash_func = hashlib.sha1() if digest in [None, DIGEST_SHA1] else hashlib.sha256()

    with open(full_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash_func.update(data)

    return hash_func.hexdigest()


def total_files_size(files):
    total = 0
    for full_path in files:
        if os.path.isfile(full_path):
            total += os.path.getsize(full_path)
    return total
