# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2013-2018 Luzzi Valerio
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated Execcumentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to Exec so, subject to the following
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
# Name:        ftp_utils.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     24/01/2018
# -------------------------------------------------------------------------------
import os, json
from .compression import *
from ftplib import *
import shutil


class FtpClient(FTP):
    def __init__(self, fileconf=None, verbose=False):
        """
        Constructor
        """
        fileconf = fileconf if fileconf else "ftp.conf"
        conf = {}
        if file(fileconf):
            text = filetostr(fileconf)
            conf = json.loads(text)
        host = conf["host"] if "host" in conf else "localhost"
        user = conf["user"] if "user" in conf else "anonymous"
        password = conf["password"] if "password" in conf else "anonymous"
        workdir = conf["workdir"] if "workdir" in conf else ""
        if verbose:
            print("Connect to %s" % (host))
        FTP.__init__(self, host)
        if verbose:
            print("login with %s" % (user))
        self.login(user, password)
        if verbose:
            print(self.getwelcome())
        if workdir:
            self.cwd(workdir)
        if verbose:
            print("We are in %s" % (self.pwd()))

    def ls(self, dirname="."):
        """
        ls
        :param dirname:
        :return:
        """
        res = []
        try:
            res = self.nlst(dirname)
        except Exception:
            pass
        return res

    def download(self, fileremote, filename=None, decompress=False, overwrite=True):
        """
        download
        """
        filename = filename if filename else justfname(fileremote)
        if directory(filename):
            filename = os.path.join(filename, justfname(fileremote))
        ext = justext(fileremote).lower()
        filetmp = tempdir() + "/" + tempname("ftp_", ext=ext)

        try:
            with open(filetmp, "wb") as f:
                self.retrbinary('RETR ' + fileremote, f.write)

            if decompress and ext in ("zip", "kmz", "rar",):
                dirname = justpath(filetmp) + "/" + tempname(ext + "_")
                mkdirs(dirname)
                filenames = unzip(filetmp, dirname)
                destdir = justpath(filename) if justpath(filename) else "."
                res = []
                for filename in filenames:
                    if overwrite and file(destdir + "/" + filename):
                        remove(destdir + "/" + filename)
                    shutil.move(dirname + "/" + filename, destdir)
                    res.append(destdir + "/" + filename)
                remove([dirname, filetmp])
                return res

            if overwrite and file(filename):
                remove(filename)
            shutil.move(filetmp, filename)
            return filename
        except Exception as ex:
            print(ex)
            return False

    def __del__(self):
        self.quit()


def main():
    pass

if __name__ == "__main__":
    main()
