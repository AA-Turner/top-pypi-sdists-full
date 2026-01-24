# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Valerio for Gecosistema S.r.l.
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
# Name:        gdal_wrappers.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     26/07/2017
# -------------------------------------------------------------------------------

from .gdal_utils import *


def gdalwarp(src_dataset, dst_dataset="", cutline="", of="GTiff", xres=-1, yres=-1, interpolation="bilinear", t_srs="",
             compress="", extraparams="", verbose=False):
    """
    gdalwarp -q -multi -cutline "{fileshp}" -crop_to_cutline -tr {pixelsize} {pixelsize} -of GTiff "{src_dataset}" "{dst_dataset}"
    """

    command = """gdalwarp -multi -overwrite -q -of {of} """
    command += """-dstnodata -9999 """
    command += """-co "BIGTIFF=YES" -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" """
    command += """--config GDAL_CACHEMAX 90% -wm 500 """
    command += """-cutline "{cutline}" -crop_to_cutline """ if cutline else ""
    command += """-tr {xres} -{yres} """ if xres > 0 and yres > 0 else ""
    command += """-r {interpolation} """
    command += """-t_srs {t_srs} """ if t_srs else ""
    command += """"{src_dataset}" "{dst_dataset}" """
    command += """{extraparams}"""

    translate_inplace = False
    if not dst_dataset or samepath(src_dataset, dst_dataset):
        translate_inplace = True
        dst_dataset = justpath(src_dataset) + "/" + tempname("tmp_")

    env = {
        "cutline": cutline,
        "src_dataset": src_dataset,
        "dst_dataset": dst_dataset,
        "of": of,
        "xres": xres,
        "yres": yres,
        "interpolation": interpolation,
        "t_srs": t_srs,
        "compress": compress,
        "extraparams": extraparams
    }

    dst_dataset = mpiexec(command, env, n=1, precond=[src_dataset], postcond=[dst_dataset], skipIfExists=True,
                          verbose=verbose)

    if translate_inplace:
        remove(src_dataset)
        rename(dst_dataset, src_dataset)
        dst_dataset = src_dataset

    if compress:
        gdal_translate(dst_dataset, dst_dataset, of, "Float32", xres, yres, compress=True, verbose=verbose)

    return dst_dataset

def gdal_grid(src_dataset, dst_dataset="", resample="nearest", verbose=False):
    """
    gdal_grid "{src_dataset}" "{dst_dataset}"
    """

    command = """gdal_grid -q -ot Float32 -of GTiff """
    command += """-co "BIGTIFF=YES" -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" -co "GDAL_NUM_THREADS=ALL_CPUS" """
    command += """-l {layername} -zfield VALUE """
    command += """-outsize {xsize} {ysize} """

    # Interpolation:
    resample = resample.upper()
    ##    if resample =="IDW":
    ##        command += """-a invdist:power=2.0:smoothing=1.0 """
    ##    else:
    ##        command += """-a nearest """
    command += """"{src_dataset}" "{dst_dataset}" """

    dst_dataset = dst_dataset if dst_dataset else forceext(src_dataset, "tif")

    env = {
        "layername": juststem(src_dataset),
        "src_dataset": src_dataset,
        "dst_dataset": dst_dataset,
        "xsize": 1000,
        "ysize": 1000

    }

    return Exec(command, env, precond=[src_dataset], postcond=[dst_dataset], skipIfExists=False, verbose=verbose)


def gdal_crop(src_dataset, cutline="", verbose=False):
    return gdalwarp(src_dataset, cutline=cutline, verbose=verbose)


def gdal_nodata(src_dataset, dst_dataset="", nodata=-9999, verbose=False):
    """
    gdalwarp -q -multi -of GTiff "{src_dataset}" "{dst_dataset}"
    """

    command = """gdalwarp -overwrite -q -of GTiff """
    command += """-dstnodata {nodata} """
    command += """-co "BIGTIFF=YES" -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" -co "NUM_THREADS=ALL_CPUS" """
    command += """--config GDAL_CACHEMAX 90% -wm 500 """
    command += """"{src_dataset}" "{dst_dataset}" """

    dst_dataset = forceext(src_dataset, "%d.tif" % (nodata)) if not dst_dataset else dst_dataset

    env = {
        "nodata": nodata,
        "src_dataset": src_dataset,
        "dst_dataset": dst_dataset
    }

    return mpiexec(command, env, n=1, precond=[src_dataset], postcond=[dst_dataset], skipIfExists=False,
                   verbose=verbose)


def gdal_mosaic(workdir, fileout, verbose=False):
    """
    gdal_mosaic
    """
    filenames = ls(workdir, ".*\.tif$", False)
    command = """gdalwarp -multi -overwrite -co "COMPRESS=LZW" -co "PREDICTOR=3" -of GTiff """
    counter = 0
    env = {"fileout": fileout}
    for filename in filenames:
        command += """"{filename%s}" """ % (counter)
        env["filename%s" % (counter)] = filename
        counter += 1
    command += """"{fileout}" """

    return Exec(command, env, precond=[], postcond=[fileout], skipIfExists=False, verbose=verbose)


def gdal_translate(src_dataset, dst_dataset=None, of="GTiff", ot="Float32", xres=-1, yres=-1, compress=True,
                   verbose=False):
    """
    gdal_translate -q -of GTiff -ot Float32 -tr 25 25 "{src_dataset}" "{dst_dataset}"
    """
    translate_inplace = False
    command = """gdal_translate -q -of {of} -ot {ot} """
    command += """-tr {xres} {yres} """ if xres > 0 and yres > 0 else ""
    command += """--config GDAL_CACHEMAX 90% """
    command += """-co "BIGTIFF=YES" -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" -co "BIGTIFF=YES" """
    command += """-co "COMPRESS=LZW" -co "PREDICTOR={predictor}" """
    command += """"{src_dataset}" "{dst_dataset}" """

    if ot in ("Float32", "Float64", "CFloat32", "CFloat64"):
        predictor = 3
    elif ot in ("Int16", "UInt16", "Int32", "UInt32", "CInt16", "CInt32"):
        predictor = 2
    else:
        predictor = 1

    if not dst_dataset or samepath(src_dataset, dst_dataset):
        translate_inplace = True
        dst_dataset = justpath(src_dataset) + "/" + tempname("tmp_")

    env = {

        "src_dataset": src_dataset,
        "dst_dataset": dst_dataset,
        "ot": ot,
        "of": of,
        "xres": xres,
        "yres": yres,
        "predictor": predictor
    }

    if Exec(command, env, precond=[src_dataset], postcond=[dst_dataset], skipIfExists=False, verbose=verbose):

        if translate_inplace:
            remove(src_dataset)
            rename(dst_dataset, src_dataset)
            dst_dataset = src_dataset

        return dst_dataset
    return False

def gdal_rasterize(src_dataset, dst_dataset, attribute="field1", of="GTiff", ot="Float32", xres=25, yres=25, alignto="",
                   moreoptions="", verbose=False):
    """
    gdal_rasterize -q -of GTiff -ot Float32 -tr 25 25 "{src_dataset}" "{dst_dataset}"
    """
    command = """gdal_rasterize -q -of {of} -ot {ot} """
    command += """ -a "{attribute}" """
    command += """ -l "{layername}" """
    command += """ -tr {xres} {yres} """
    command += """{extent} """
    # command += """ --config GDAL_CACHEMAX 90% -wm 500 """
    command += """ -co "BIGTIFF=YES" -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256" -co "BIGTIFF=YES" -co "NUM_THREADS=ALL_CPUS" """
    command += """ -co "COMPRESS=LZW" -co "PREDICTOR=3" """
    command += """{moreoptions} """
    command += """"{src_dataset}" "{dst_dataset}" """

    if alignto:
        layername, extent, proj4, geomtype, (px, py, nodata, datatype) = GDAL_META(alignto)
        extent = " ".join(["%f" % item for item in extent])

    env = {

        "src_dataset": src_dataset,
        "dst_dataset": dst_dataset,
        "layername": juststem(src_dataset),
        "attribute": attribute,
        "extent": "-te " + extent if alignto else "",
        "ot": ot,  # if not alignto else datatype,
        "of": of,
        "xres": xres if not alignto else px,
        "yres": yres if not alignto else py,
        "moreoptions": moreoptions
    }

    return mpiexec(command, env, n=1, precond=[src_dataset], postcond=[dst_dataset], skipIfExists=False,
                   verbose=verbose)


def gdal_lzw(src_dataset, dst_dataset="", dtype="Float32", moreoptions="", verbose=False):
    """
    gdal_lzw
    """
    # -co "COMPRESS=LZW" -co "PREDICTOR=3" -co "GDAL_NUM_THREADS=ALL_CPUS"
    command = """gdal_translate -q  -of GTiff """
    command += """-co "BIGTIFF=YES" -co "TILED=YES" -co "BLOCKXSIZE=256" -co "BLOCKYSIZE=256"  """
    command += """-co "COMPRESS=LZW" -co "PREDICTOR={predictor}"  """
    command += """-ot {dtype} """
    command += " " + moreoptions + " "
    command += """"{src_dataset}" "{dst_dataset}" """

    if dtype in ("Float32", "Float64", "CFloat32", "CFloat64"):
        predictor = 3
    elif dtype in ("Int16", "UInt16", "Int32", "UInt32", "CInt16", "CInt32"):
        predictor = 2
    else:
        predictor = 1

    env = {
        "src_dataset": src_dataset,
        "dst_dataset": dst_dataset if dst_dataset else forceext(src_dataset, "lzw.tif"),
        "dtype": dtype,
        "predictor": predictor
    }
    return Exec(command, env, precond=[src_dataset], postcond=[dst_dataset], verbose=verbose)


# -------------------------------------------------------------------------------
#   Main loop
# -------------------------------------------------------------------------------
if __name__ == '__main__':
    workdir = r'c:\EUDEM_GECO\Basins\slpd100'
    chdir(workdir)

    filename = r"c:/EUDEM_GECO/Basins/slpd100/Angerman.slpd.100.tif"
    fileout = r"c:/EUDEM_GECO/Basins/slpd100/Angerman.slpd.3857.100.tif"

    print(gdalwarp(filename, fileout, interpolation="near", t_srs="epsg:3857", compress=True, verbose=False))
