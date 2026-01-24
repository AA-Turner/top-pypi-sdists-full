# ------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012 -2017 Luzzi Valerio
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        http
# Purpose:
#
# Author:      Luzzi Valerio
# Created:     15/02/2013
# ----------------------------------------------------------------------------

import json
from cgi import FieldStorage
from .compression import *
from .stime import *
from .sqlitedb import SqliteDB
from .spatialdb import SpatialDB
from jinja2 import Environment, FileSystemLoader
import math, sys, os, re
from builtins import str as unicode

class Form:
    """
    Form
    """
    def __init__(self, environ):
        try:
            form = get_post_form(environ)
            self.form = {}
            for key in form:
                value = form.getvalue(key)
                self.form[key] = value
        except:
            _environ = {}
            for key in environ:
                value = environ[key]
                _environ[key] = value
            self.form = _environ

        if "encoded" in self.form and self.form["encoded"] == "true":
            for key in self.form:
                if key != "encoded":
                    try:
                        self.form[key] = base64.b64decode(self.form[key])
                    except:
                        pass
    def keys(self):
        """
        keys
        """
        return self.form

    def getvalue(self, key, default=None):
        """
        getvalue
        """
        if key in self.form:
            return self.form[key]
        else:
            return default

    def toObject(self):
        """
        toObject
        """
        return self.form


class InputProcessed(object):
    """
    InputProcessed
    """

    def read(self, *args):
        raise EOFError('The wsgi.input stream has already been consumed')

    readline = readlines = __iter__ = read


def get_post_form(environ):
    """
    get_post_form
    """
    input = environ['wsgi.input']
    post_form = environ.get('wsgi.post_form')
    if post_form is not None and post_form[0] is input:
        return post_form[2]
    # This must be done to avoid a bug in cgi.FieldStorage
    environ.setdefault('QUERY_STRING', '')
    form = FieldStorage(fp=input, environ=environ, keep_blank_values=1)
    new_input = InputProcessed()
    post_form = (new_input, input, form)
    environ['wsgi.post_form'] = post_form
    environ['wsgi.input'] = new_input
    return form


def doNotRespond(status, response_headers):
    """
    doNotRespond
    """
    pass


def httpResponse(text, status, start_response):
    """
    httpResponse
    """
    text = "%s" % str(text)
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(text)))]
    if start_response:
        start_response(status, response_headers)
    return [ text.encode('utf-8')]


def httpResponseOK(text, start_response):
    """
    httpResponseOK
    """
    return httpResponse(text, "200 OK", start_response)


def httpResponseNotFound(start_response):
    """
    httpResponseNotFound
    """
    return httpResponse("404 NOT FOUND", "404 NOT FOUND", start_response)


def httpDownload(files, removesrc, start_response):
    filename = "download-%s.zip" % (strftime("%Y-%m-%d %H.%M.%S"))

    if isstring(files):
        files = [files]

    if len(files) > 0:
        filename = juststem(files[0]) + ".zip"

    if (len(files) == 0):
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        return ['Not Found']

    if (len(files) == 1):
        if file(files[0]):
            filename = files[0]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            return ['Not Found']

    if len(files) > 1:
        # Zippo i files in un unico archivio
        if isinstance(files, (tuple, list)):
            compress(files, filename, removesrc )

    filesize = os.path.getsize(filename)

    status = "200 OK"
    with open(filename, "rb") as stream:
        headers = [('Content-Type', 'application/octet-stream'),
                   ('Content-Disposition', 'attachment; filename=%s' % justfname(filename)),
                   ('Content-Length', '%s' % filesize)]

        start_response(status, headers)
        return [stream.read()]

def JSONResponse(obj, start_response):
    """
    JSONResponse
    """
    if isstring(obj):
        res = obj
    elif isinstance(obj, (dict, list)):
        res = unicode(json.dumps(obj))
    else:
        res = obj
    return httpResponse(res, "200 OK", start_response)


def SQLResponse(db, sql, env={}, start_response=None, verbose=False):
    """
    SQLResponse
    """

    if not db:
        try:
            sql = filetostr(sql) if isfile(sql) else sql

            res = SqliteDB.Execute(sql, env, outputmode="response", verbose=verbose)
        except Exception as ex:
            res = {"status": "fail", "success": False, "exception": "%s" % ex, "sql": sql}
        return JSONResponse(res, start_response)
    else:
        # patcha le query - rimuovi [{dsn}].
        sql = re.sub(r"""\[\{dsn\}\]\.""", "", sql)
        sql = re.sub(r"""SELECT\s+'%s'\s*;""" % (juststem(db.dsn)), "", sql)


    # Standard query
    try:
        res = db.execute(sql, env, outputmode="response", keepdims=True, verbose=verbose)

    except Exception as ex:
        res = {"status": "fail", "success": False, "exception": "%s" % ex, "sql": sql}

    # anyway
    return JSONResponse(res, start_response)


def SQLScriptResponse(filename, env=None, start_response=None, verbose=False):
    """
    SQLScriptResponse
    """
    # Standard query
    if file(filename):
        res = SqliteDB.ExecuteScript(filename, env, outputmode="response", verbose=verbose)
    else:
        res = {"status": "fail", "success": False, "exception": "file %s does not exists!" % filename}
    return JSONResponse(res, start_response)


def template(filetpl, env, fileout=None):
    """
    template -  generate text from jinja2 template file
    """
    workdir = justpath(filetpl)
    workdir = workdir if workdir else "."
    environ = Environment(loader=FileSystemLoader(workdir))
    t = environ.get_template(justfname(filetpl))
    text = t.render(env).encode("utf-8")
    if fileout:
        strtofile(text, fileout)
    return text

def DocumentRoot(environ=None):
    """
    DocumentRoot
    """
    return environ["DOCUMENT_ROOT"] if environ and "DOCUMENT_ROOT" in environ else leftpart(normpath(__file__), "/apps/")

def httpPage(environ, start_response=None, checkuser=False):
    """
    httpPage -
    """
    import gecosistema_lite as gs

    url = environ["url"] if "url" in environ else re.sub(r'\\', '/', environ["SCRIPT_FILENAME"])
    url = forceext(url, "html")
    # root   = environ["ROOTDIR"] if "ROOTDIR" in environ else ""
    DOCUMENT_ROOT = environ["DOCUMENT_ROOT"] if "DOCUMENT_ROOT" in environ else ""
    HTTP_COOKIE = environ["HTTP_COOKIE"] if "HTTP_COOKIE" in environ else ""

    if checkuser and not check_user_permissions(environ):
        environ["url"] = "back.html"
        return httpPage(environ, start_response)

    if "__file__" in environ:
        chdir(justpath(environ["__file__"]))

    if not file(url):
        return httpResponseNotFound(start_response)

    workdir = justpath(url)
    index_html = justfname(url)

    jss = (DOCUMENT_ROOT + "/apps/common/lib/js",
           justpath(url),)

    csss = (DOCUMENT_ROOT + "/apps/common/lib/css",
            DOCUMENT_ROOT + "/apps/common/lib/js",
            DOCUMENT_ROOT + "/apps/common/lib/images",
            justpath(url),)

    env = Environment(loader=FileSystemLoader(workdir))
    t = env.get_template(index_html)
    variables = {
        "loadjs": loadjs(jss),
        "loadcss": loadcss(csss),
        "APPNAME": juststem(workdir),
        "splashscreen": loadsplash(justpath(url) + "/splashscreen.png"),
        "os": os,
        "math": math,
        "gecosistema_lite": gs,
        "environ": environ
    }
    html = t.render(variables) #.encode("utf-8", "replace")
    return httpResponseOK(html, start_response)


def check_user_permissions(environ):
    """
    check_user_permissions
    """
    DOCUMENT_ROOT = environ["DOCUMENT_ROOT"] if "DOCUMENT_ROOT" in environ else leftpart(normpath(__file__), "/apps/")
    filedb = DOCUMENT_ROOT + "/projects/htaccess.sqlite"
    HTTP_COOKIE = environ["HTTP_COOKIE"] if "HTTP_COOKIE" in environ else ""

    if file(filedb):
        HTTP_COOKIE = mapify(HTTP_COOKIE, ";")
        db = SqliteDB(filedb, modules=["math.so"])
        user_enabled = db.execute("""
            SELECT COUNT(*) FROM [users] WHERE '{__token__}' LIKE md5([token]||strftime('%Y-%m-%d','now'));
            """, HTTP_COOKIE, outputmode="scalar", verbose=False)
        db.close()
        return user_enabled

    return False


def webpath(filename, pivot):
    """
    webpath -  pivot = "/apps/"
    """
    return "/" + rightpart(normpath(filename), pivot)


def loadcss(dirnames):
    """
    loadcss
    """
    text = ""
    dirnames = listify(dirnames, sep=",")
    for dirname in dirnames:
        for filename in ls(dirname, r'.*\.css$'):
            filename = webpath(filename, "/apps/")
            if filename != '/':
                text += sformat("<link href='{filename}' rel='stylesheet' type='text/css'/>\n", {"filename": filename});
    return text


def loadjs(dirnames):
    """
    loadjs
    """
    text = ""
    dirnames = listify(dirnames, sep=",")

    for dirname in dirnames:
        filenames = ls(dirname, r'.*\.js$', recursive=True)
        for filename in filenames:
            filename = webpath(filename, "/apps/")
            if filename != '/':
                text += sformat("<script type='text/javascript' src='{filename}'></script>\n", {"filename": filename});

    return text


def loadsplash(filename):
    # filename = filename if file(filename) else leftpart(filename,"/WebGIS/") + "/WebGIS/apps/common/template/splashscreen.png",
    text = """
<div id="splashscreen" style="
	background-image:url({data});
	background-repeat:no-repeat;
	background-color:white; 
	box-shadow: 10px 10px 5px #888888;
	position:absolute;
	z-index:100000;
	border:1px solid black;
	top: 50%;
	left: 50%;
	margin-top:  -101px;
	margin-left: -300px;
	width:  600px;
	height: 200px;">
</div>
"""
    return sformat(text, {"data": b64image(filename)})


if __name__ == '__main__':
    pass
