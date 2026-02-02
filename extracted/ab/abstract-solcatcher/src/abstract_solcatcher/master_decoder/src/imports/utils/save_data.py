from .imports import *
def get_data_dir():
    abs_dir = get_initial_caller_dir()
    imports_dir = os.path.dirname(abs_dir)
    src_dir = os.path.dirname(imports_dir)
    return os.path.join(src_dir,'data')
def get_none_payloads_path():
    return os.path.join(get_data_dir(),'sample_payloads.json')
def get_sample_payloads_path():
    return os.path.join(get_data_dir(),'sample_payloads.json')
def get_json_data(path):
    if not os.path.isfile(path):
        safe_dump_to_json(data={},file_path=path)
    return safe_read_from_json(file_path=path)
def safe_json_save_data(data,file_path):
    i=0
    while True:
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        filepath,ext = os.path.splitext(file_path)
        temp_path = os.path.join(dirname,f"{filename}.tmp")
        safe_dump_to_json(data=data,file_path=file_path)
        try:
            json.loads(file_path)
            shutil.move(temp_path,file_path)
            return True
        except:
            i+=1
            if i ==3:
                break
    return False

def update_json_data(path,discriminator,event,**kwargs):
    data = get_json_data(path)
    if discriminator not in data:
        data[discriminator] = []
    if event not in data[discriminator]:
        data[discriminator][event] =  kwargs
        safe_json_save_data(data,path)
        
def get_sample_payloads():
    sample_payloads_path = get_sample_payloads_path()
    return get_json_data(sample_payloads_path)
def save_sample_payloads_data(data):
    sample_payloads_path = get_sample_payloads_path()
    return safe_json_save_data(data,sample_payloads_path)
def update_sample_payloads(discriminator,event,**kwargs):
    sample_payloads_path = get_sample_payloads_path()
    update_json_data(sample_payloads_path,discriminator,event,**kwargs)
def get_none_payloads_data():
    none_payloads_path = get_none_payloads_path()
    return get_json_data(sample_payloads_path)
def save_none_payloads(data):
    none_payloads_path = get_none_payloads_path()
    return safe_json_save_data(data,none_payloads_path)
def update_none_payloads(discriminator,event,**kwargs):
    none_payloads_path = get_none_payloads_path()
    update_json_data(none_payloads_path,discriminator,event,**kwargs)
