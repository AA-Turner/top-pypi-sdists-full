from ..imports import start_analyzer,pydot,os,safe_read_from_json,make_dirs
BASE_DIRECTORY = '/var/www/html/clownworld/bolshevid'
DATA_DIR = make_dirs(BASE_DIRECTORY,"data")
IMPORT_MAP_DIR = make_dirs(DATA_DIR,"import_tools")

def get_dot_path():
    return os.path.join(IMPORT_MAP_DIR,'graph.dot')
def get_import_graph_path():
    return os.path.join(IMPORT_MAP_DIR,'import-graph.json')
def read_from_dot_file(path = None):
    path = get_dot_path()
    graphs, = pydot.graph_from_dot_file(path)
    return graphs
def get_dot_data():
    dot_path = get_dot_path()
    ensure_import_creation(dot_path)
    return read_from_dot_file()
def get_import_graph_data():
    graph_path = get_import_graph_path()
    ensure_import_creation(graph_path)
    return safe_read_from_json(graph_path)
def ensure_import_creation(path):
    if not os.path.isfile(path):
        create_import_maps()
def create_import_maps():
    root = BASE_DIRECTORY
    directory = os.getcwd()
    entries = 'index,main'
    out = get_import_graph_path()
    dot = get_dot_path()
    start_analyzer(root=root,entries=entries,out=out,dot=dot)
