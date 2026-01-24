from ...imports import os
from dotenv import load_dotenv
from ...ssh_utils import is_file
from ...string_utils import eatAll,eatInner,eatOuter
from ...safe_utils import safe_split
from ...compare_utils import line_contains
from ...type_utils import is_list,is_bool
from ...directory_utils import get_slash,path_join,if_not_last_child_join,get_home_folder,simple_path_join
DEFAULT_FILE_NAME = '.env'
DEFAULT_KEY = 'MY_PASSWORD'
