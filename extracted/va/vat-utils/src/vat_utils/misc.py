import os
import random
import string

def get_file_dir_path(file_path):
    return os.path.dirname(os.path.abspath(file_path))

def make_random_string(length=8):
   return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(length))

def merge_dicts(d1, d2):
   d = {}
   d.update(d1)
   d.update(d2)
   return d
