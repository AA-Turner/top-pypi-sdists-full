# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2013-2017 Luzzi Valerio
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
# Name:        taudem.py
# Purpose:     taudem wrappers
#
# Author:      Luzzi Valerio
#
# Created:     22/02/2017
# -------------------------------------------------------------------------------
from .gdal_utils import *
from .gdal_numpy import *

def PitRemove(demfile, felfile="", n=-1, skipIfExists=False, verbose=False):
    """
    PitRemove
    """
    command = """{exe} -z "{demfile}" -fel "{felfile}" """

    felfile = name_without_ext(demfile) + "fel.tif" if not felfile else felfile
    mkdirs(justpath(felfile))
    env = {"exe": "pitremove", "demfile": demfile, "felfile": felfile, "n": n}

    felfile = mpiexec(command, env, n, precond=[demfile], postcond=[felfile], skipIfExists=skipIfExists,
                      verbose=verbose)

    # Fix nodata if needed
    if felfile and GetNoData(felfile) != GetNoData(demfile):
        nodata = GetNoData(demfile)
        if verbose:
            print("fixing nodata with %s" % nodata)
        gdal_numpy("f=np.where(abs(f)>1e+38,{nodata},f)", {"f": felfile, "nodata": nodata})
        SetNoData(felfile, nodata)

    return felfile


def D8FlowDir(felfile, pfile="", sd8file="", n=-1, skipIfExists=False, verbose=False):
    """
    D8FlowDir
    """
    command = """{exe} -fel "{felfile}" -p "{pfile}" -sd8 "{sd8file}" """

    pfile = remove_suffix(felfile, "fel") + "p.tif" if not pfile   else pfile
    sd8file = remove_suffix(felfile, "fel") + "sd8.tif" if not sd8file else sd8file
    mkdirs(justpath(pfile))
    mkdirs(justpath(sd8file))

    env = {"exe": "d8flowdir", "felfile": felfile, "pfile": pfile, "sd8file": sd8file, "n": n}
    return mpiexec(command, env, n, precond=[felfile], postcond=[pfile, sd8file], skipIfExists=skipIfExists,
                   verbose=verbose)


def AreaD8(pfile, ad8file="", nc=True, n=-1, skipIfExists=False, verbose=False):
    """
    AreaD8
    """
    command = """{exe} -p "{pfile}" -ad8 "{ad8file}" {nc} """

    ad8file = remove_suffix(pfile, "p") + "ad8.tif" if not ad8file else ad8file
    mkdirs(justpath(ad8file))

    env = {"exe": "aread8", "pfile": pfile, "ad8file": ad8file, "nc": "-nc" if nc else "", "n": n}
    return mpiexec(command, env, n, precond=[pfile], postcond=[ad8file], skipIfExists=skipIfExists, verbose=verbose)


def Threshold(ssafile, srcfile="", thresh=100, maskfile="", n=-1, skipIfExists=False, verbose=False):
    """
    Threshold
    """
    command = """{exe} -ssa "{ssafile}" -src "{srcfile}" -thresh {thresh} """
    command += """ -mask "{maskfile}" """ if maskfile else ""

    srcfile = remove_suffix(ssafile, "ssa") + "src.tif" if not srcfile else srcfile
    env = {"exe": "threshold", "ssafile": ssafile, "srcfile": srcfile, "thresh": thresh, "maskfile": maskfile, "n": n}

    return mpiexec(command, env, n, precond=[ssafile], postcond=[srcfile], skipIfExists=skipIfExists, verbose=verbose)


def StreamNet(felfile, pfile, ad8file, srcfile, ordfile="", treefile="", coordfile="",
              netfile="", netlayername="", outletfile="",
              layername="", layernumber=0, wfile="", n=-1, skipIfExists=False, verbose=False):
    """
    StreamNet
    """
    command = """{exe} -fel "{felfile}" -p "{pfile}" -ad8 "{ad8file}" -src "{srcfile}" -ord "{ordfile}" -tree "{treefile}" -coord "{coordfile}" -net "{netfile}" -w "{wfile}" """
    command += """ -netlyr "{netlayername}" """ if netlayername else ""
    command += """ -o "{outletfile}" """ if outletfile   else ""
    command += """ -lyrname "{layername}" """ if layername    else ""
    command += """ -lyrno   "{layernumber}" """ if layernumber  else ""

    ordfile = remove_suffix(felfile, "fel") + "ord.tif" if not ordfile else ordfile
    treefile = remove_suffix(felfile, "fel") + "tree.txt" if not treefile else treefile
    coordfile = remove_suffix(felfile, "fel") + "coord.txt" if not coordfile else coordfile
    netfile = remove_suffix(felfile, "fel") + "net.shp" if not netfile else netfile
    wfile = remove_suffix(felfile, "fel") + "w.tif" if not wfile else wfile

    env = {
        "exe": "streamnet",
        "felfile": felfile,
        "pfile": pfile,
        "ad8file": ad8file,
        "srcfile": srcfile,
        "ordfile": ordfile,
        "treefile": treefile,
        "coordfile": coordfile,
        "netfile": netfile,
        "netlayername": netlayername,
        "outletfile": outletfile,
        "layername": layername,
        "layernumber": layernumber,
        "wfile": wfile,
        "n": n
    }

    return mpiexec(command, env, n, precond=[felfile, pfile, ad8file, srcfile],
                   postcond=[ordfile, treefile, coordfile, netfile, wfile], skipIfExists=skipIfExists, verbose=verbose)


def SlopeAveDown(felfile, pfile, slpdfile="", dn=100, n=-1, skipIfExists=False, verbose=False):
    """
    SlopeAveDown -fel <felfile> -p <pfile> -slpd <slpdfile> [-dn]
    """
    command = """{exe} -fel "{felfile}" -p "{pfile}" -slpd "{slpdfile}" -dn {dn} """

    slpdfile = remove_suffix(felfile, "fel") + "slpd.tif" if not slpdfile else slpdfile
    env = {"exe": "slopeavedown", "felfile": felfile, "pfile": pfile, "slpdfile": slpdfile, "dn": dn, "n": n}
    slpdfile = mpiexec(command, env, n, precond=[felfile, pfile], postcond=[slpdfile], skipIfExists=skipIfExists,
                       verbose=verbose)

    # Fix nodata if needed
    if felfile and GetNoData(slpdfile) != GetNoData(felfile):
        nodata = GetNoData(felfile)
        if verbose:
            print("fixing nodata with %s" % nodata)
        gdal_numpy("f=np.where(abs(f)>1e+38,{nodata},f)", {"f": slpdfile, "nodata": nodata})
        SetNoData(slpdfile, nodata)

    return slpdfile


def StreamBurning(filedem, fileriver, fileburn="", value=20, verbose=False):
    """
    StreamBurning
    """
    fileburn = fileburn if fileburn else forceext(filedem, "brn.tif")
    env = {
        "burn": fileburn,
        "river": fileriver,
        "dem": filedem,
        "value": value
    }
    return gdal_numpy("""burn=np.where(river>0,dem-value,0)""", env, verbose=verbose)


if __name__ == "__main__":
    print(os.getcwd())
    filedem = r"d:\EUDEM_GECO\Basins\DTM\Ebro.tif"
    fileburn = r"d:\EUDEM_GECO\Basins\DTM\Ebro.burn.tif"
    filelzw = r"d:\EUDEM_GECO\Basins\DTM\Ebro.burn.lzw.tif"
    fileriver = r"d:\EUDEM_GECO\Basins\rivers\Raster\Ebro_river.tif"

    PitRemove(fileburn, verbose=True)
