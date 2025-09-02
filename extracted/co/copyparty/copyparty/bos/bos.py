# coding: utf-8
from __future__ import print_function, unicode_literals

import os

from ..util import SYMTIME, fsdec, fsenc
from . import path as path

MKD_755 = {"chmod_d": 0o755}
MKD_700 = {"chmod_d": 0o700}

_ = (path, MKD_755, MKD_700)
__all__ = ["path", "MKD_755", "MKD_700"]

# grep -hRiE '(^|[^a-zA-Z_\.-])os\.' . | gsed -r 's/ /\n/g;s/\(/(\n/g' | grep -hRiE '(^|[^a-zA-Z_\.-])os\.' | sort | uniq -c
# printf 'os\.(%s)' "$(grep ^def bos/__init__.py | gsed -r 's/^def //;s/\(.*//' | tr '\n' '|' | gsed -r 's/.$//')"


def chmod(p , mode )  :
    return os.chmod(fsenc(p), mode)


def chown(p , uid , gid )  :
    return os.chown(fsenc(p), uid, gid)


def listdir(p  = ".")  :
    return [fsdec(x) for x in os.listdir(fsenc(p))]


def makedirs(name , vf   = MKD_755, exist_ok  = True)  :
    # os.makedirs does 777 for all but leaf; this does mode on all
    todo = []
    bname = fsenc(name)
    while bname:
        if os.path.isdir(bname):
            break
        todo.append(bname)
        bname = os.path.dirname(bname)
    if not todo:
        if not exist_ok:
            os.mkdir(bname)  # to throw
        return False
    mode = vf["chmod_d"]
    chown = "chown" in vf
    for zb in todo[::-1]:
        try:
            os.mkdir(zb, mode)
            if chown:
                os.chown(zb, vf["uid"], vf["gid"])
        except:
            if os.path.isdir(zb):
                continue
            raise
    return True


def mkdir(p , mode  = 0o755)  :
    return os.mkdir(fsenc(p), mode)


def open(p , *a, **ka)  :
    return os.open(fsenc(p), *a, **ka)


def readlink(p )  :
    return fsdec(os.readlink(fsenc(p)))


def rename(src , dst )  :
    return os.rename(fsenc(src), fsenc(dst))


def replace(src , dst )  :
    return os.replace(fsenc(src), fsenc(dst))


def rmdir(p )  :
    return os.rmdir(fsenc(p))


def stat(p )  :
    return os.stat(fsenc(p))


def unlink(p )  :
    return os.unlink(fsenc(p))


def utime(
    p , times   = None, follow_symlinks  = True
)  :
    if SYMTIME:
        return os.utime(fsenc(p), times, follow_symlinks=follow_symlinks)
    else:
        return os.utime(fsenc(p), times)


if hasattr(os, "lstat"):

    def lstat(p )  :
        return os.lstat(fsenc(p))

else:
    lstat = stat
