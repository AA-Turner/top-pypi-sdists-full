from abstract_utilities.dynimport import *
import_modules = [
   
    {"module":'abstract_react.react_analyzer',"symbols":[
        "ImportGraphWorker",
        "build_graph_reachable",
        "build_graph_all",
        "invert_to_symbol_map",
        "invert_to_function_map",
        "invert_to_variable_map"
        ]},
    {"module":'abstract_paths.content_utils.file_utils',"symbols":[
        'get_directory_map',
        'findGlobFiles'
        ]},
    {"module":'abstract_paths.file_filtering.file_filters',"symbols":[
        'collect_filepaths'
        ]},
    {"module":'abstract_paths.python_utils.utils.utils',"symbols":[
        'get_py_script_paths'
        ]},
    {"module":'abstract_paths.content_utils.diff_engine',"symbols":[
        'plan_previews',
        'apply_diff_text',
        'ApplyReport',
        'write_text_atomic'
        ]},
    {"module":'abstract_paths.content_utils.find_content',"symbols":[
        'findContent',
        'getLineNums',
        'findContentAndEdit',
        'findContent',
        'get_line_content'
        ]},
    {"module":'abstract_paths.content_utils.find_content',"symbols":[
        'getLineNums',
        'findContentAndEdit',
        'findContent',
        'get_line_content'
        ]}
     ]

import_symbols_to_parent(import_modules, update_all=True)
