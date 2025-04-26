from abstract_utilities import get_any_value
fetch_any_combo_keys = """columnNames,tableName,searchColumn,searchValue,anyValue,zipit""".lower().split(',')
fetch_any_combo_search_keys = """searchColumn,searchValue"""
fetch_any_js = {}
fetch_any_inputs = kwargs
for key,value in fetch_any_inputs:
    if key.lower() in fetch_any_combo_keys:
        fetch_any_js[key] = value
        del kwargs[key]
for key,value in kwargs.items():
    if key not in fetch_any_js:
        fetch_any_js["searchColumn"] = key
        fetch_any_js["searchValue"] = value
return 
