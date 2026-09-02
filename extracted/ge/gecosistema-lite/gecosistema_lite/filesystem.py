"""
# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio for Gecosistema S.r.l.
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
# Name:        filesystem
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     27/12/2012
# -------------------------------------------------------------------------------
"""
import os
import shutil
import sys
import tempfile
import base64
import mimetypes
import uuid
import csv
import datetime
import hashlib
from .strings import *
from .stime import *

def isWindows():
    """
    isWindows
    """
    return os.name == "nt" or sys.platform.startswith("win")


def isLinux():
    """
    isLinux
    """
    return sys.platform.startswith("linux")


def isMac():
    """
    isMac
    """
    return sys.platform.startswith("darwin")


def file(pathname):
    """
    file - True se pathname e' un file
    """
    return os.path.isfile(pathname) if pathname else False


def isfile(pathname):
    """
    isfile -  alias for file
    """
    return file(pathname)


def directory(pathname):
    """
    directory - True se pathname e'  una cartella
    """
    return os.path.isdir(pathname) if pathname else False


def normpath(pathname):
    """
    normpath
    """
    if not pathname:
        return ""
    return os.path.normpath(pathname.replace("\\", "/")).replace("\\", "/")


def justdrive(pathname):
    """
    justdrive - ritorna il drive o ptotocollo http: ftp: ... del url
    """
    arr = normpath(pathname).split("/", 2)
    return arr[0] if len(arr) > 1 else ""


def justpath(pathname, n=1):
    """
    justpath
    """
    for j in range(n):
        (pathname, tail) = os.path.split(normpath(pathname))
    return normpath(pathname)


def justfname(pathname):
    """
    justfname - returns the basename
    """
    return normpath(os.path.basename(normpath(pathname)))


def juststem(pathname):
    """
    juststem
    """
    pathname = os.path.basename(normpath(pathname))
    (root, _) = os.path.splitext(pathname)
    return root


def justext(pathname):
    """
    justext
    """
    pathname = os.path.basename(normpath(pathname))
    (_, ext) = os.path.splitext(pathname)
    return ext.lstrip(".")


def forceext(pathname, newext):
    """
    forceext
    """
    (root, _) = os.path.splitext(normpath(pathname))
    pathname = root + ("." + newext if len(newext.strip()) > 0 else "")
    return normpath(pathname)


def abspath(pathname):
    """
    abspath
    """
    return normpath(os.path.abspath(pathname))


def samepath(pathname1, pathname2):
    """
    samepath
    """
    if isWindows():
        pathname1 = abspath(pathname1).lower()
        pathname2 = abspath(pathname2).lower()
        return pathname1 == pathname2
    return abspath(pathname1) == abspath(pathname2)


def isfiletype(filename, ext="db,sqlite", check_if_exists=False):
    """
    isfiletype
    """
    if check_if_exists and not file(filename):
        return False
    return justext(filename).lower() in listify(ext)


def isfilexls(filename, check_if_exists=False):
    """
    isfilexls
    :param filename:
    :param check_if_exists:
    :return:
    """
    return isfiletype(filename, "xls,xlsx", check_if_exists)


def name_without_ext(filename):
    """
    name_without_ext
    """
    return re.sub(r'\.(\w)+$', '', filename, 1, re.I)


def remove_suffix(filename, suffix=""):
    """
    remove_suffix
    """
    return re.sub(suffix + "$", "", name_without_ext(filename), 1, re.I)


def strtofile(text, filename, append=False):
    """
    strtofile
    """
    try:
        flag = "ab" if append else "wb"
        mkdirs(justpath(filename))
        with open(filename, flag) as stream:
            if text:
                if isinstance(text,str):
                    text = text.encode('utf-8')
                stream.write(text)
    except Exception as ex:
        print(ex)
        return ""
    return filename


def filetostr(filename):
    """
    filetostr
    """
    try:
        with open(filename, "r") as stream:
            return stream.read()
    except:
        return None

def filetoarray(filename):
    """
    filetoarray
    """
    try:
        with open(filename, "rb") as stream:
            return stream.readlines()
    except:
        return []


def filesize(filename):
    """
    filesize
    """
    if file(filename):
        return os.path.getsize(filename)
    else:
        return -1


def filectime(filename):
    """
    filectime - get the creation date
    """
    if file(filename) or directory(filename):
        unixtimestamp = os.path.getctime(filename)
        return strftime("%Y-%m-%d %H:%M:%S", datetime.datetime.fromtimestamp(unixtimestamp))
    else:
        return None

def rename(filesrc, filedest, overwrite=True):
    """
    rename
    """
    try:
        if file(filedest) and overwrite:
            remove(filedest)
        mkdirs(justpath(filedest))
        os.rename(filesrc, filedest)
        return True
    except Exception as ex:
        print(ex)
    return False


def remove(files):
    """
    remove
    """
    for item in listify(files):
        try:
            if os.path.isfile(item):
                os.remove(item)
            if os.path.isdir(item):
                shutil.rmtree(item)
        except Exception as ex:
            print(ex)
            pass


def mkdirs(pathname):
    """
    mkdirs - create a folder
    """
    try:
        if file(pathname):
            pathname = justpath(pathname)
        os.makedirs(pathname)
    except:
        pass
    return directory(pathname)


def chdir(pathname):
    """
    chdir - change directory
    """
    pathname = justpath(pathname) if os.path.isfile(pathname) else pathname
    if os.path.isdir(pathname):
        os.chdir(pathname)
        return True
    return False


def cwd():
    """
    pwd - get current working directory
    """
    return os.getcwd()


def ls(dirname=".", filter=r'.*', recursive=True, exclude=""):
    """
    ls - list all files in dirname
    """
    res = []
    dirname = normpath(dirname)
    if os.path.isdir(dirname):
        try:
            # Some dir could not be accessible
            filenames = os.listdir(dirname)
            filenames.sort()
        except:
            filenames = []

        for filename in filenames:
            filename = dirname + "/" + filename
            if os.path.isfile(filename) and re.match(filter, filename, re.IGNORECASE):

                if (not exclude) or (exclude and not (exclude.lower() in filename.lower())):
                    text = "%s" % (filename)
                    res += [text]

            if os.path.isdir(filename) and recursive:
                res += ls(filename, filter, True, exclude)

    return res


def listdir(dirname=".", filter=r'.*', recursive=True, sortby="name"):
    """
    listdir - list all directoriesin dirname
    """
    res = []
    dirname = normpath(dirname)
    if os.path.isdir(dirname):
        try:
            # Some dir could not be accessible
            items = os.listdir(dirname)
            if sortby == "name":
                items.sort()
            elif sortby == "ctime":
                items = [{"name": item, "ctime": filectime(dirname+"/"+item)} for item in items]
                items.sort(key=lambda k: k["ctime"])
                items = [item["name"] for item in items]
        except:
            items = []
        for item in items:
            item = dirname + "/" + item
            if os.path.isdir(item) and re.match(filter, item, re.IGNORECASE):
                res += ["%s" % (item)]
                if recursive:
                    res += listdir(item, filter=filter, recursive=True, sortby=sortby)
    return res


def findpath(searchdir=".", filter=r".*", maxdepth=-1, firstonly=False):
    """
    findpath
    """
    res = []

    # Limit depth search
    if maxdepth == 0:
        return res

    try:
        items = os.listdir(searchdir)
        for item in items:
            pathname = os.path.join(searchdir, item)
            if os.path.isdir(pathname):
                if re.match(filter, item, re.IGNORECASE):
                    if firstonly:
                        return [pathname]
                    res.append(pathname)
        # Recursion
        for item in items:
            pathname = os.path.join(searchdir, item)
            if os.path.isdir(pathname):
                results = findpath(pathname, filter, maxdepth - 1, firstonly)
                if len(results) and firstonly:
                    return results[0]
                res += results
    except Exception:
        # print ex
        pass
    return res

def tempdir():
    """
    tempdir - retunrs the name of temporary folder
    """
    return tempfile.gettempdir()


def tempname(prefix="", postfix="", ext=""):
    """
    tempname -returns a temporary name
    """
    uid = str(uuid.uuid4()).replace("-", "").upper()
    return forceext(prefix + uid[:8] + postfix, ext)


def safename(filename, additional_chars=r''):
    """
    safename - give a safe name for the filesystem
    """
    if isWindows():
        notallowed = r'~"#%&*:<>?{|}'
    elif isLinux():
        notallowed = r''
    elif isMac():
        notallowed = r':'

    chars = notallowed + additional_chars
    return chrtran(filename, chars, '_' * len(chars))

def cat(filenames, fileout):
    """
    cat - catenate all files
    """
    for filename in filenames:
        if os.path.isfile(filename):
            text = filetostr(filename)
            strtofile(text, fileout, True)

    return fileout

def Desktop():
    """
    Desktop path
    """
    return os.path.expanduser('~') + "/Desktop"


def Home():
    """
    Home directory
    """
    return os.path.expanduser('~')


def md5sum(filename):
    """
    md5sum - returns themd5 of the file
    """
    if file(filename):
        f = open(filename, mode='rb')
        d = hashlib.md5()
        while True:
            buf = f.read(4096)
            if not buf:
                break
            d.update(buf)
        f.close()
        return d.hexdigest()
    else:
        return ""


def filehaschanged(filename, filemd5="", updatemd5=False):
    """
    filehaschanged - It needs an .md5 file to check
    """
    filemd5 = filemd5 if filemd5 else forceext(filename, "md5")
    oldmd5 = filetostr(filemd5)
    if oldmd5:
        newmd5 = md5sum(filename)
        if oldmd5.upper() == newmd5.upper():
            return False
    # If specified update the .md5 file
    if updatemd5:
        strtofile(md5sum(filename), filemd5)
    return True


def from_template(filetpl, fileout=None, env=None):
    """
    from_template
    """
    text = filetostr(filetpl)
    text = sformat(text, env)
    fileout = fileout if fileout else forceext(filetpl, "out")
    strtofile(text, fileout)
    return fileout


def create_template(filetpl, fileout=None, env=None):
    """
    create_template
    """
    return from_template(filetpl, fileout, env)


def b64(filename):
    """
    b64
    """
    if file(filename):
        with open(filename, 'rb') as stream:
            data = stream.read()
    else:
        data = b''
    return base64.standard_b64encode(data).decode('utf-8')


def b64image(filename):
    """
    b64image
    """
    mimetype, _encoding = mimetypes.guess_type(filename)
    return sformat("data:{mimetype};base64,{data}", {"mimetype": mimetype, "data": b64(filename)})


def detectSeparator(filecsv, sep=';\t,|', buffsize=128):
    """
    detectSeparator in csv files
    """
    res = ","
    sniffer = csv.Sniffer()
    with open(filecsv, 'r') as f:
        dialect = sniffer.sniff(f.read(buffsize), delimiters=sep)
        f.seek(0)
        res = dialect.delimiter
    return res


def detectDecimal(filecsv, sep):
    """
    detectDecimal in csv files
    """
    res = "."
    if sep == ",":
        return "."
    with open(filecsv, 'r') as f:
        line = f.readline()
        while line:
            arr = line.split(sep)
            if len(arr) > 0:
                if "," in arr[0] and isnumeric(arr[0].replace(",", ".")):
                    res = ","
                    break
                elif "." in arr[0] and isnumeric(arr[0]):
                    res = "."
                    break
            line = f.readline()
    return res

if __name__ == '__main__':
    workdir = r"D:\Users\vlr20\Projects\BitBucket\OpenSITUA\apps\common\lib\js\corex"
    chdir(workdir)
    filename = "hello.txt"
    print(safename(filename))
