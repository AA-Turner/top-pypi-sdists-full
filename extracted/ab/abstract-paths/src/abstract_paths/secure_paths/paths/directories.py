from .static_dir import *

ABS_HTML_AUTHS_FOLDER = get_html_path('auths')
ABS_HTML_CHANGE_PASSWORD_DIR = get_html_path('changepassword')
ABS_HTML_LOGIN_DIR = get_html_path('login')
ABS_HTML_INDEX_DIR = get_html_path('index')
URL_PREFIX = f"/secure-files/"
STATIC_FOLDER = ABS_STATIC_DIR
UPLOAD_FOLDER = ABS_UPLOAD_DIR
TEMPLATES_FOLDER = '/var/www/api/abstract_logins/app/src/templates'
ABS_PUBLIC_FOLDER = ABS_PUBLIC_DIR
ABS_UPLOAD_ROOT = ABS_UPLOAD_DIR
def get_rel_path(path,rel_path):
    rel_path = os.path.relpath(path, rel_path)
    return rel_path
def get_rel_uploads_path(path):
    rel_path = get_rel_path(path, ABS_UPLOAD_ROOT)
    return rel_path

ABS_REMOVED_DIR = get_rel_uploads_path('removed')
