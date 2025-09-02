from .src_dir import *
ABS_HTML_DIR= get_static_path("html")
ABS_JS_DIR= get_static_path("js")
ABS_CSS_DIR= get_static_path("css")
ABS_TS_DIR= get_static_path("ts")
ABS_PY_DIR= get_static_path("py")
def get_html_path(path):
    html_path = os.path.join(ABS_HTML_DIR,path)
    return html_path
def get_js_path(path):
    js_path = os.path.join(ABS_JS_DIR,path)
    return js_path
def get_css_path(path):
    css_path = os.path.join(ABS_CSS_DIR,path)
    return html_path
def get_ts_path(path):
    ts_path = os.path.join(ABS_TS_DIR,path)
    return ts_path
def get_py_path(path):
    py_path = os.path.join(ABS_PY_DIR,path)
    return py_path
