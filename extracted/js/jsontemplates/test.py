import os
import sys
import unittest 
from json_templates import *

GOOD_JSON = """{
   "key":"hard coded value",
   "key2":1,
   "key3":"{{ variable }}",
   "key4":"{% array %}"
}
"""

BAD_JSON = """{
   "key":"hard coded value",
   "key2":1,
   "key3":"{{ variable }}"
   "key4":"{% array %}"
}
"""

REPLACE_TEMPLATE = """{
 "key":"{{ key }}"
}"""

REPLACE_RESULT = "hello world"
REPLACE_KEY    = "key"

REPLACE_ARR_TEMPLATE = """{
 "array":"{% array %}"
}"""

REPLACE_ARR_RESULT = ["hello","world"]
REPLACE_ARR_KEY    = "array"

NESTING_JSON = """{
 "key":{
  "innerkey":{
   "inner2key":{
    "inner3key1":"a value",
    "inner3key2":4,
    "inner3key3":"{{ innertest }}"
   }
  }
 }
}"""

NESTING_KEY = "innertest"
NESTING_VALUE = "success"

class basic_tests(unittest.TestCase):
 
#-----------------------------------------------------------------------
 def test_object(self):
  json_tmp = JsonTemplates()
  self.assertIsInstance(json_tmp,JsonTemplates)

 
#-----------------------------------------------------------------------
 def test_json_string(self):
  json_tmp = JsonTemplates()
  self.assertTrue(json_tmp.loads(GOOD_JSON)[0])
  
#-----------------------------------------------------------------------
 def test_json_file(self):
  json_tmp = JsonTemplates()
  result = json_tmp.load(os.path.join(os.getcwd(),"examples/example1.json"))
  self.assertTrue(result[0],msg="Failed to load json file. Error: {}".format(result[1]))
  
#-----------------------------------------------------------------------
 def test_bad_json_string(self):
  json_tmp = JsonTemplates()
  self.assertFalse(json_tmp.loads(BAD_JSON)[0])

#-----------------------------------------------------------------------
 def test_compare_variable_replacement(self):
  json_tmp = JsonTemplates()
  self.assertTrue(json_tmp.loads(REPLACE_TEMPLATE)[0])
  
  result = json_tmp.generate({REPLACE_KEY:REPLACE_RESULT})
  
  self.assertTrue(result[0],msg="Generate failed with this message. {}".format(result[1]))

  self.assertEqual(result[1][REPLACE_KEY],REPLACE_RESULT)
  
#-----------------------------------------------------------------------
 def test_compare_array_replacement(self):
  json_tmp = JsonTemplates()
  self.assertTrue(json_tmp.loads(REPLACE_ARR_TEMPLATE)[0])
  
  result = json_tmp.generate({REPLACE_ARR_KEY:REPLACE_ARR_RESULT})
  
  self.assertTrue(result[0],msg="Generate failed with this message. {}".format(result[1]))
  
  for x in range(0,len(REPLACE_ARR_RESULT)):
   self.assertEqual(result[1][REPLACE_ARR_KEY][x],REPLACE_ARR_RESULT[x])
   
#-----------------------------------------------------------------------
 def test_compare_nesting_replacement(self):
  json_tmp = JsonTemplates()
  self.assertTrue(json_tmp.loads(NESTING_JSON)[0])
  
  result = json_tmp.generate({NESTING_KEY:NESTING_VALUE})
  
  self.assertTrue(result[0],msg="Generate failed with this message. {}".format(result[1]))
  
  self.assertEqual(result[1]["key"]["innerkey"]["inner2key"]["inner3key3"],NESTING_VALUE)
 
#-----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
