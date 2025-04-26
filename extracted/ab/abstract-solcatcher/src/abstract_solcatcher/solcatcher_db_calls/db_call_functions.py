from abstract_solcatcher import get_pair,call_solcatcher_db,call_solcatcher_ts,delete_row
#..async_utils import call_solcatcher_db
def modular_fetch_any_combo(*args,**kwargs):
    fetch_any_combo_keys = """columnNames,tableName,searchColumn,searchValue,anyValue,zipit""".lower().split(',')
    fetch_any_combo_search_keys = """searchColumn,searchValue"""
    fetch_any_js = {}
    fetch_any_inputs = kwargs
    for key,value in fetch_any_inputs.items():
        if key.lower() in fetch_any_combo_keys:
            fetch_any_js[key] = value
            del kwargs[key]
    for key,value in kwargs.items():
        if key not in fetch_any_js:
            fetch_any_js["searchColumn"] = key
            fetch_any_js["searchValue"] = value
    return call_solcatcher_db('/api/fetch_any_combo',**fetch_any_js)
def get_args_kwargs_as_kwargs(keys, *args, **kwargs):
    new_kwargs = {}
    to_remove = []  # List of keys to remove after the loop

    for key, value in kwargs.items():
        if key in keys:
            new_kwargs[key] = value
            to_remove.append(key)  # Mark for removal
            keys.remove(key)

    # Remove keys after iteration
    for key in to_remove:
        del kwargs[key]

    # Handle positional arguments
    for arg in args:
        if keys:
            new_kwargs[keys.pop(0)] = arg
        else:
            break

    return new_kwargs

    
def call_metadata(*args,**kwargs):
    main_keys = ['mint','meta_id','pair_id']
    new_kwargs = get_args_kwargs_as_kwargs(main_keys,*args,**kwargs)
    if new_kwargs:
        return call_solcatcher_db('/api/get_meta_data',**new_kwargs)
    return modular_fetch_any_combo(*args,**kwargs)

def fix_meta_data(meta_id=None,mint=None):
    
    called_meta_data = call_metadata(meta_id = meta_id,mint=mint)
    called_meta_data_js = called_meta_data[0]
    called_meta_data_mint = called_meta_data_js.get('mint')
    if called_meta_data_js.get('meta_data') == {}:
        got_or_fetched_meta_data = call_solcatcher_ts('/get-or-fetch-metadata',mint=called_meta_data_mint)
open_metadata=[]
mint = 'FcWKJVmSAv8AKJuqscsizHWUfTQ2zEMLKaNseB3kpump'
for i in range(1,1000000):
    try:
        fix_meta_data(meta_id=i)
    except:
        open_metadata.append(i)
        print(i)
        get_pair(mint=mint)
