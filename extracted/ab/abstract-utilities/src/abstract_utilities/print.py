from abstract_utilities import *
from abstract_utilities.json_utils import get_any_value
json_list = """C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Example Review.py_0.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Strategies in PromptBuilder.py.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Strategies in PromptBuilder.py_0.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Strategies in PromptBuilder.py_1.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Strategies in PromptBuilder.py_2.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Strategies in PromptBuilder.py_3.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Strategies in PromptBuilder.py_4.json
C:/Users/jrput/Documents/python projects/Modules/test_modules/new_ai_test/response_data/2023-11-03/gpt-4-0613/Chunking Example Review.py.json""".split('\n')
for path in json_list:
   json = get_any_value(safe_read_from_json(path),'content')
   if json:
       json=safe_json_loads(json)
       if isinstance(json,list):
           for value in json:
               value=safe_json_loads(value)
               if isinstance(value,dict):
                   for key,value2 in value.items():
                       print(key)
                       input(value2)
       if isinstance(json,dict):
           for key,value in json.items():
               print(key)
               input(value)
     
   if isinstance(json,dict):
       for key,value in json.items():
           print(key)
           input(value)
