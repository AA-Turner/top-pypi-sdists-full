from .base_dir import *
UPLOAD_DIR = get_base_path("uploads")
ABS_SRC_DIR = get_base_path("src")
ABS_PUBLIC_DIR = get_base_path("public")
def get_upload_path(path):
    upload_dir = os.path.join(ABS_UPLOAD_DIR, path)
    return upload_dir
def get_src_path(path):
    src_dir = os.path.join(ABS_SRC_DIR, path)
    return src_dir
def get_public_path(path):
    public_dir = os.path.join(ABS_PUBLIC_DIR, path)
    return public_dir
