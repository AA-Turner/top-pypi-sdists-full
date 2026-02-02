import errno
import glob
import hashlib
import os
import re


def tail(f, lines=20):
    readlines = f.readlines()
    return "".join(readlines[-lines:])


def grep(f, patter):
    result = []
    for line in f:
        if re.search(patter, line):
            result.append(line)
    return result


def mkdir_p(filepath):
    try:
        os.makedirs(filepath)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(filepath):
            pass
        else:
            raise


class chdir(object):
    def __init__(self, directory):
        self.directory = directory
        self.current_dir = os.getcwd()

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.current_dir)


def parse_owner(owner):
    owner = owner or ""
    owner = owner.strip()

    user = None
    group = None

    splitted = owner.split(":", 2)
    if len(splitted) > 0:
        user = splitted[0].strip() or None
        if len(splitted) > 1:
            group = splitted[1].strip() or None

    return user, group


def parent_chain(filepath):
    filepath = os.path.abspath(filepath)
    while filepath != "/":
        filepath = os.path.dirname(filepath)
        yield filepath


def md5(file):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def yield_files(root: str, filter_list: tuple = tuple(), with_prefix: bool = True):
    for filename in glob.glob(root):
        base_filename = os.path.basename(filename)
        if base_filename in filter_list:
            continue
        if not with_prefix:
            yield base_filename
        else:
            yield filename
