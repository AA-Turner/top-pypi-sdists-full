import os
import sys
#sys.path.insert(0, os.path.abspath('..')) 
sys.path.insert(0, os.path.abspath('../../'))
autodoc_mock_imports = ["dask", "distributed", "sqlite3"]

project = 'Pikobs'

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
project = 'Pikobs'
copyright = '2023, David Lobon'
author = 'David Lobon'
html_theme_options = {
    'collapse_navigation': False,  
    'sticky_navigation': True,    
    'navigation_depth': 4,     
    'includehidden': True,
    'titles_only': False
}
extensions = ['sphinx.ext.napoleon',
              'sphinx.ext.doctest', 
              'sphinx.ext.mathjax',
              "sphinx.ext.autodoc"]

napoleon_include_private_with_doc = False

# table cells wrap their text (see _static/custom.css)
html_css_files = list(globals().get('html_css_files', [])) + ['custom.css']

# configuration tables drawn from the wrappers (_ext/wrapper_settings.py)
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '_ext'))
extensions = list(globals().get('extensions', [])) + ['wrapper_settings']

# the flag bits and criteria, read from the code (_ext/flag_tables.py)
extensions = list(globals().get('extensions', [])) + ['flag_tables']

# pieces included by other pages (runtime.rst, the BUFR codes page),
# not pages of their own
exclude_patterns = ['runtime_*.rst', 'varno_search.rst']


# The BUFR code search: its two scripts are copied into the built site at
# the end of every build -- an incremental build of Sphinx does not always
# copy _static again -- and the page loads them with their date as a
# version (?v=...), so a browser fetches them again as soon as they change.
def _pikobs_search_files(app, exception):
    import os
    import re
    import shutil
    if exception or getattr(app.builder, "format", "") != "html":
        return
    src = os.path.join(app.srcdir, "_static")
    dst = os.path.join(app.outdir, "_static")
    names = ("varno_search.js", "varno_search_widget.js")
    os.makedirs(dst, exist_ok=True)
    stamp = {}
    for name in names:
        if os.path.isfile(os.path.join(src, name)):
            shutil.copy2(os.path.join(src, name), os.path.join(dst, name))
            stamp[name] = int(os.path.getmtime(os.path.join(src, name)))
    page = os.path.join(app.outdir, "varno.html")
    if stamp and os.path.isfile(page):
        html = open(page, encoding="utf-8").read()
        for name, v in stamp.items():
            html = re.sub(r'_static/' + re.escape(name) + r'(\?v=\d+)?"',
                          f'_static/{name}?v={v}"', html)
        open(page, "w", encoding="utf-8").write(html)


_pikobs_previous_setup = globals().get("setup")


def setup(app):
    result = _pikobs_previous_setup(app) if callable(_pikobs_previous_setup) else None
    app.connect("build-finished", _pikobs_search_files)
    return result


# The Pikobs Web version, read at each build from the same place the
# installer reads it (APP_VERSION in the launcher's config), so the pages
# always show the version that setup_pikobs.sh installs.
import pathlib as _pathlib
import re as _re
try:
    _cfg = (_pathlib.Path(__file__).resolve().parents[2]
            / "pikobs/web_launcher/app/config.py").read_text()
    PIKOBS_WEB_VERSION = _re.search(r"^APP_VERSION\s*=\s*['\"]([^'\"]+)", _cfg, _re.M).group(1)
except (OSError, AttributeError):
    PIKOBS_WEB_VERSION = "?"
rst_epilog = (globals().get("rst_epilog") or "") + \
    f"\n.. |pikobs_web_version| replace:: {PIKOBS_WEB_VERSION}\n"
