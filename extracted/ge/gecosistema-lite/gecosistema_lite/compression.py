# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio 
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
# Name:        compression.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     11/08/2017
# -------------------------------------------------------------------------------
import zipfile
import bz2
import tarfile
import rarfile
import os
from .filesystem import *

rarfile.PATH_SEP = '/'
rarfile.UNRAR_TOOL = "c:/Program Files/winrar/unrar.exe"


def namelist(filezip):
    """
    namelist
    """
    if filezip and file(filezip):
        ext = justext(filezip).lower()
        res = []
        if ext in ("zip", "kmz",):
            sourceZip = zipfile.ZipFile(filezip, 'r')
            res = sourceZip.namelist()
        elif ext in ("rar",):
            sourceZip = rarfile.RarFile(filezip)
            res = sourceZip.namelist()
        elif ext in ("bz2",):
            res = [justpath(filezip) + "/" + juststem(filezip)]
        elif ext in ("tgz",):
            sourceZip = tarfile.open(filezip, 'r:*')
            res = sourceZip.getmembers()

        return res

    return None


def compress(filenames, filezip="", removesrc=False):
    """
    compress
    """

    if isstring(filenames) and directory(filenames):
        #filenames = ls(filenames)
        root = "%s"%filenames
        filenames = []
        for path, _, files in os.walk(root):
            for filename in files:
                relpath = os.path.relpath(path, root)
                filenames.append(os.path.join(relpath, filename))
    else:
        filenames = listify(filenames, sep=",")

    if not filezip:
        if len(filenames) == 1:
            filezip = forceext(filenames[0], "zip")
        elif len(filenames) > 1:
            filezip = forceext(justpath(filenames[0]), "zip")
        else:
            return None

    mkdirs(justpath(filezip))

    if (justext(filezip) == "zip"):
        with zipfile.ZipFile(filezip, 'w', zipfile.ZIP_DEFLATED) as archive:
            for filename in filenames:
                if file(filename):
                    archive.write(filename, filename)

    if (justext(filezip) == "tgz"):
        with tarfile.open(filezip, "w") as archive:
            for filename in filenames:
                if file(filename):
                    archive.add(filename)

    if file(filezip):
        if removesrc:
            remove(filenames)
        return filezip
    return False


def unzip(filename, directory="", removeSrc=False):
    """
    unzip
    """
    directory = justpath(filename) if len(directory) == 0 else directory
    res = []
    if os.path.isfile(filename):
        sourceZip = None
        mkdirs(directory)
        ext = justext(filename).lower()

        if ext in ("zip", "kmz",):
            try:
                sourceZip = zipfile.ZipFile(filename, 'r')
                for name in sourceZip.namelist():
                    sourceZip.extract(name, directory)
                res = sourceZip.namelist()
            except:
                pass

        elif ext == "rar":

            try:
                # rarfile.PATH_SEP = '/'
                # rarfile.UNRAR_TOOL = "c:/Program Files/winrar/unrar.exe"
                sourceZip = rarfile.RarFile(filename)
                sourceZip.extractall(path=directory)
                res = sourceZip.namelist()
            except Exception as e:
                print(e)

        elif ext == "bz2":

            try:
                BUFFERSIZE = 1024 * 1024
                fileout = forceext(filename, "")
                with open(fileout, 'wb') as new_file, bz2.BZ2File(filename, 'rb') as file:
                    for data in iter(lambda: file.read(BUFFERSIZE), b''):
                        new_file.write(data)
                res = [fileout]
            except Exception as e:
                print(e)

        elif ext == "tgz":
            try:
                sourceZip = tarfile.open(filename, 'r:*')
                sourceZip.extractall(path=directory)
                res = sourceZip.getmembers()
            except Exception as e:
                print(e)



        if removeSrc:
            remove(filename)
        return res

if __name__ == "__main__":
    pass
