from .main_dir import *
WWW_DIR = '/var/www'
MEDIA_DIR = f"{WWW_DIR}/media"
ABS_UPLOAD_DIR = f"{MEDIA_DIR}/users"
ABS_FUNCTIONS_DIR= get_src_path("functions")
ABS_COMPONENTS_DIR= get_src_path("components")
ABS_ASSETS_DIR= get_src_path("assets")
ABS_STATIC_DIR= get_src_path("static")
def get_functions_path(path):
    functions_dir = os.path.join(ABS_FUNCTIONS_DIR, path)
    return functions_dir
def get_components_path(path):
    components_dir = os.path.join(ABS_COMPONENTS_DIR, path)
    return components_dir
def get_assets_path(path):
    assets_dir = os.path.join(ABS_ASSETS_DIR, path)
    return assets_dir
def get_static_path(path):
    static_dir = os.path.join(ABS_STATIC_DIR, path)
    return static_dir
