import re,threading,os,shutil,requests,asyncio,time,subprocess,json,glob,sys,logging
from datetime import timedelta
from datetime import datetime
from typing import *
from .hash_utils import *
from .json_utils import (unified_json_loader,
                         find_keys,
                         get_key_values_from_path,
                         get_value_from_path,
                         find_paths_to_key,
                         create_and_read_json,
                         unified_json_loader,
                         all_try,
                         try_json_loads,
                         get_error_msg,
                         get_any_key,
                         get_any_value,
                         json_key_or_default,
                         format_json_key_values,
                         get_all_keys,
                         update_dict_value,
                         get_all_key_values,
                         get_json_data,
                         safe_json_dumps,
                         safe_json_loads,
                         read_from_json,
                         safe_load_from_json,
                         safe_load_from_file,
                         safe_json_reads,
                         safe_read_from_json,
                         safe_dump_to_file,
                         safe_dump_to_json,
                         safe_write_to_json,
                         safe_write_to_file,
                         safe_save_updated_json_data,
                         get_result_from_data,
                         flatten_json
                         )
from .read_write_utils import (read_from_file,
                               write_to_file)
from .path_utils import (get_file_create_time,
                         get_files,
                         get_folders,
                         path_join,
                         mkdirs,
                         split_text,
                         get_all_item_paths,
                         get_directory_items,
                         get_files,
                         get_folders,
                         break_down_find_existing,
                         get_directory_items,
                         get_directory_files,
                         get_all_item_paths,
                         get_all_file_paths,
                         get_directory,
                         create_directory,
                         initialize_file,
                         join_path,
                         is_last_itter,
                         path_join,
                         is_file,
                         is_dir,
                         is_path,
                         get_all_directories,
                         get_all_files,
                         get_all_items,
                         collate_text_docs,
                         get_dirlist,
                         get_content,
                         is_directory_in_paths,
                         make_dirs,
                         remove_directory,
                         remove_path,
                         get_file_parts
                         )
from .list_utils import (get_highest_value_obj,
                         make_list,
                         safe_list_return,
                         get_actual_number,
                         compare_lists,
                         get_symetric_difference,
                         list_set,
                         make_list_it)
from .time_utils import (get_time_stamp,
                         get_sleep,
                         sleep_count_down,
                         get_date,
                         get_current_time_with_delta,
                         format_timestamp,
                         timestamp_to_milliseconds,
                         parse_timestamp,
                         get_time_now_iso,
                         is_valid_time)
from .string_clean import (eatInner,
                           eatAll,
                           eatOuter,
                           url_join,
                           capitalize
                           )
from .type_utils import (make_bool,
                         T_or_F_obj_eq,
                         is_number,
                         makeInt,
                         str_lower,
                         confirm_type,
                         get_all_file_types,
                         is_media_type,
                         get_bool_response,
                         get_mime_type,
                         get_media_exts,
                         if_true_get_string,
                         find_for_string,
                         is_strings_in_string,
                         get_alphabet_str,
                         get_alphabet_upper_str,
                         get_alphabet_comp_str,
                         get_numbers,
                         get_numbers_comp,
                         is_any_instance,
                         break_string
                         )
get_media_types = get_all_types = get_all_file_types
from .math_utils import (convert_to_percentage,
                         exponential,
                         get_percentage,
                         add_it,
                         divide_it,
                         exp_it,
                         return_0)
from .compare_utils import (create_new_name,
                            get_last_comp_list,
                            get_closest_match_from_list)
from .thread_utils import ThreadManager
from .history_utils import HistoryManager
from .abstract_classes import *
from .parse_utils import (num_tokens_from_string,
                          chunk_source_code,
                          chunk_any_to_tokens,
                          detect_language_from_text,
                          chunk_by_language_context,
                          search_code)

from .log_utils import get_caller_info,get_logFile,print_or_log,get_json_call_response,initialize_call_log
from .error_utils import try_func
from .class_utils import alias,get_class_inputs
from .robust_reader import *


