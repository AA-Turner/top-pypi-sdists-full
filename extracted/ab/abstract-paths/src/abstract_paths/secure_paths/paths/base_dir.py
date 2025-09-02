import os
WWW_DIR="/var/www/"
MEDIA_DIR = f"{WWW_DIR}media"
BASE_DIR = os.path.join(MEDIA_DIR, "users")
API_URL_PREFIX = "/api/"
ABS_URL_PREFIX = "/api/secure-files/"
ABS_BASE_DIR = os.path.join(BASE_DIR, "secure-files")
def get_base_path(path):
    base_dir = os.path.join(ABS_BASE_DIR, path)
    return base_dir
