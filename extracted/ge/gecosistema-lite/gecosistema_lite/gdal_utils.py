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
# Name:        gdal_utils.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     16/05/2013
# -------------------------------------------------------------------------------
"""apt-get -y install gdal-bin libgdal-dev python-gdal"""

import struct
from osgeo import gdal,gdalconst
from osgeo import ogr, osr
import numpy as np
from pyproj import *
from .execution import *

# TYPE [chart|circle|line|point|polygon|raster|query]
GEOMETRY_TYPE = {
    ogr.wkb25DBit: "wkb25DBit",
    ogr.wkb25Bit: "wkb25Bit",
    ogr.wkbUnknown: "LINE",  # unknown
    ogr.wkbPoint: "POINT",
    ogr.wkbLineString: "LINE",
    ogr.wkbPolygon: "POLYGON",
    ogr.wkbMultiPoint: "POINT",
    ogr.wkbMultiLineString: "LINE",
    ogr.wkbMultiPolygon: "POLYGON",
    ogr.wkbGeometryCollection: "POLYGON",
    ogr.wkbNone: "NONE",
    ogr.wkbLinearRing: "POLYGON",
    ogr.wkbPoint25D: "POINT",
    ogr.wkbLineString25D: "LINE",
    ogr.wkbPolygon25D: "POLYGON",
    ogr.wkbMultiPoint25D: "POINT",
    ogr.wkbMultiLineString25D: "LINE",
    ogr.wkbMultiPolygon25D: "POLYGON",
    ogr.wkbGeometryCollection25D: "POLYGON"
}


def ProjFrom(text):
    if val(text):
        return "+init=epsg:%s" % (text)
    if isstring(text) and text.lower().startswith("epsg:"):
        return "+init=%s" % (text)
    if isstring(text) and text.lower().startswith("init="):
        return "+%s" % (text)
    if isstring(text) and text.lower().startswith("+proj"):
        return text
    return ""


# -------------------------------------------------------------------------------
#   Reproj
# -------------------------------------------------------------------------------
def Reproj(lon, lat, epsgfrom="epsg:4326", epsgto="epsg:32632"):
    try:
        epsgfrom = ProjFrom(epsgfrom)
        epsgto = ProjFrom(epsgto)
        p1 = Proj(epsgfrom)
        p2 = Proj(epsgto)
        if (p1 != p2):
            x, y = transform(p1, p2, lon, lat)
            return (x, y)
        return lon, lat
    except Exception as ex:
        print(ex)
        print("Proj Error", "Proj Error")
    return 0, 0


def ReProject(blon, blat, elon, elat, epsgfrom="epsg:4326", epsgto="epsg:32632"):
    blon, blat, elon, elat = float(blon), float(blat), float(elon), float(elat)
    blon, blat = Reproj(blon, blat, epsgfrom, epsgto)
    elon, elat = Reproj(elon, elat, epsgfrom, epsgto)
    return blon, blat, elon, elat


def MapToPixel(mx, my, gt):
    """
    MapToPixel
    """
    ''' Convert map to pixel coordinates
        @param  mx:    Input map x coordinate (double)
        @param  my:    Input map y coordinate (double)
        @param  gt:    Input geotransform (six doubles)
        @return: px,py Output coordinates (two ints)
    '''
    if gt[2] + gt[4] == 0:  # Simple calc, no inversion required
        px = (mx - gt[0]) / gt[1]
        py = (my - gt[3]) / gt[5]

        return int(px), int(py)

    raise Exception("I need to Invert geotransform!")


def GetValueAt(X, Y, filename, band=1):
    """
    GetValueAt
    """
    # Converto in epsg 3857
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(band)
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        gt = dataset.GetGeoTransform()
        # Convert from map to pixel coordinates.
        # Only works for geotransforms with no rotation.
        # If raster is rotated, see http://code.google.com/p/metageta/source/browse/trunk/metageta/geometry.py#493
        # print  gt
        j, i = MapToPixel(float(X), float(Y), gt)

        if i in range(0, band.YSize) and j in range(0, band.XSize):
            scanline = band.ReadRaster(j, i, 1, 1, buf_type=gdalconst.GDT_Float32)  # Assumes 16 bit int aka 'short'
            (value,) = struct.unpack('f', scanline)
            return value

    # raise ValueError("Unexpected (Lon,Lat) values.")
    return None


def readmssqlstring(text):
    """
    readmssqlstring
    """
    #   "dbname='Catasto' host=.\SQLEXPRESS user='sa' password='12345' srid=4326 type=MultiPolygon table="dbo"."SearchComboBox" (Geometry) sql="  from .qgs file
    #   "MSSQL:server=.\SQLEXPRESS;trusted_connection=no;uid=sa;pwd=12345;database=Catasto;"   MSSQLSpatial dns
    #   "DRIVER={SQL Server};SERVER=.\SQLEXPRESS;PORT=1433;DATABASE=Catasto;uid=sa;pwd=12345"  ODBC
    #
    env = {}
    DICTIONARY = {"host": "server", "user": "uid", "password": "pwd", "dbname": "database", "table": "tablename",
                  "type": "geometry_type"}
    text = text.replace("MSSQL:", "")

    for item in listify(text, " ;"):
        item = item.split("=", 1)
        if len(item) > 1:
            key = DICTIONARY[item[0]] if item[0] in DICTIONARY else item[0]
            env[key] = ("%s" % item[1]).strip("'")
    # some correction
    if "tablename" in env and "." in env["tablename"]:
        text = chrtran(env["tablename"], '"', '')
        env["catalog"], env["tablename"] = text.split(".", 1)
    return env


def GDAL_SIZE(filename):
    """
    GDAL_SIZE
    """
    data = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if data:
        band = data.GetRasterBand(1)
        m = data.RasterYSize
        n = data.RasterXSize
        data, band = None, None
        return (m, n)
    return (0, 0)


def GDAL_DATASOURCE(datasource):
    """
    GDAL_DATASOURCE - get filename,layerid from datasource
    """
    if "|" in datasource:
        arr = listify(datasource, "|")
        if len(arr) == 2:
            filename, layerid = arr
            _, layerid = layerid.split("=", 1)
            layerid = val(layerid)
            return filename, layerid, None
        elif len(arr) == 3:
            filename, layerid, geom_type = arr
            _, layerid = layerid.split("=", 1)
            _, geom_type = geom_type.split("=", 1)
            layerid = val(layerid)
            return filename, layerid, geom_type

    if justext(datasource).lower() in ("shp", "dbf", "sqlite"):
        return datasource, 0, None

    return datasource, 0, None

def GDAL_META(filename):
    """
    GDAL_META
    """
    layername, layerid, extent, proj4, geomtype, other = "", 0, (0, 0, 0, 0), "", "", None
    filename, layerid, geomtype = GDAL_DATASOURCE(filename)
    ext = justext(filename).lower()

    # Shape
    if ext in ("shp", "dbf", "sqlite", "dxf"):
        data = ogr.OpenShared(filename)
        if data and data.GetLayer(layerid):
            layer = data.GetLayer(layerid)
            layername = layer.GetName()
            minx, maxx, miny, maxy = layer.GetExtent()
            geomtype = GEOMETRY_TYPE[layer.GetGeomType()]
            n = layer.GetFeatureCount(True)
            srs = layer.GetSpatialRef()
            epsg = srs.ExportToProj4() if srs else "epsg:4326"
            proj4 = epsg if epsg.startswith("+proj") else "init=%s" % epsg
            extent = (minx, miny, maxx, maxy)
            ##extent = ReProject(minx,miny,maxx,maxy,epsg,epsgto="epsg:3857")
            other = (n)

    # Raster
    if ext in ("tif", "tiff"):
        data = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if data:
            band = data.GetRasterBand(1)
            n = data.RasterXSize
            m = data.RasterYSize
            gt = data.GetGeoTransform()
            prj = data.GetProjection()
            srs = osr.SpatialReference(prj)
            epsg = srs.ExportToProj4() if srs else "AUTO"
            proj4 = epsg if epsg.startswith("+proj") else "init=%s" % epsg

            geomtype = "raster"
            nodata = band.GetNoDataValue()
            rdata = band.ReadAsArray(0, 0, 1, 1)
            datatype = str(rdata.dtype)
            del data
            (x0, px, rot, y0, rot, py) = gt
            minx = min(x0, x0 + n * px)
            miny = min(y0, y0 + m * py)
            maxx = max(x0, x0 + n * px)
            maxy = max(y0, y0 + m * py)
            extent = (minx, miny, maxx, maxy)
            ##extent = ReProject(minx,miny,maxx,maxy,epsg,epsgto="epsg:3857")
            other = (px, py, nodata, datatype)
            layername = juststem(filename)

    if ext in ("mssql") or filename.lower().startswith("mssql") or "dbname" in filename.lower():
        # layername = juststem(filename)
        if "dbname" in filename.lower():
            dsn = sformat(
                """MSSQL:server={server};trusted_connection=no;uid={uid};pwd={pwd};database={database};tablename={tablename};""",
                readmssqlstring(filename))
        else:
            dsn = filename

        layername = textin(dsn.lower(), "tablename=", ";")
        data = ogr.OpenShared(dsn)
        if data:
            layer = data.GetLayer(str(layername)) if layername else data.GetLayer()
            if layer:
                minx, maxx, miny, maxy = layer.GetExtent()
                geomtype = GEOMETRY_TYPE[layer.GetGeomType()]
                n = layer.GetFeatureCount(True)
                srs = layer.GetSpatialRef()
                epsg = srs.ExportToProj4() if srs else "epsg:3857"
                proj4 = epsg if epsg.startswith("+proj") else "init=%s" % epsg
                extent = (minx, miny, maxx, maxy)
                ##extent = ReProject(minx,miny,maxx,maxy,epsg,epsgto="epsg:3857")
                other = (n)

    return layername, extent, proj4, geomtype, other


def GDAL_QUERY(filename, sql, data=None):
    """
    GDAL_QUERY
    """
    res = []
    data = data if data else {}
    sql = sformat(sql, data)
    ds = ogr.OpenShared(filename)
    if ds:
        try:
            layer = ds.ExecuteSQL(sql)
            definition = layer.GetLayerDefn()
            n = definition.GetFieldCount()
            for feature in layer:
                row = {}
                for i in range(n):
                    fieldname = definition.GetFieldDefn(i).GetName()
                    row[fieldname] = feature.GetField(fieldname)
                res += [row]
        except Exception as ex:
            print("GDAL_QUERY Exception:", ex)
    return res


def GDAL2Numpy(pathname, band=1):
    """
    GDAL2Numpy
    """
    dataset = gdal.Open(pathname, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(band)
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()
        nodata = band.GetNoDataValue()
        bandtype = gdal.GetDataTypeName(band.DataType)
        wdata = band.ReadAsArray(0, 0, cols, rows)
        # translate nodata as Nan
        if not wdata is None:
            if bandtype in ('Float32', 'Float64', 'CFloat32', 'CFloat64'):
                if not nodata is None and abs(nodata) > 3.4e38:
                    wdata[abs(wdata) > 3.4e38] = np.nan
                elif not nodata is None:
                    wdata[wdata == nodata] = np.nan
            elif bandtype in ('Byte', 'Int16', 'Int32', 'UInt16', 'UInt32', 'CInt16', 'CInt32'):
                wdata = wdata.astype("Float32", copy=False)
                wdata[wdata == nodata] = np.nan
        band = None
        dataset = None
        return (wdata, geotransform, projection)
    print("file %s not exists!" % (pathname))
    return (None, None, None)


def Numpy2GTiff(arr, geotransform, projection, filename, nodata=-9999):
    """
    Numpy2GTiff
    """
    if isinstance(arr, np.ndarray):
        rows, cols = arr.shape
        if rows > 0 and cols > 0:
            dtype = str(arr.dtype)
            if dtype in ["uint8"]:
                fmt = gdal.GDT_Byte
            elif dtype in ["uint16"]:
                fmt = gdal.GDT_UInt16
            elif dtype in ["uint32"]:
                fmt = gdal.GDT_UInt32
            elif dtype in ["float32"]:
                fmt = gdal.GDT_Float32
            elif dtype in ["float64"]:
                fmt = gdal.GDT_Float64
            else:
                fmt = gdal.GDT_Float64

            driver = gdal.GetDriverByName("GTiff")
            dataset = driver.Create(filename, cols, rows, 1, fmt)
            if (geotransform != None):
                dataset.SetGeoTransform(geotransform)
            if (projection != None):
                dataset.SetProjection(projection)
            dataset.GetRasterBand(1).SetNoDataValue(nodata)
            dataset.GetRasterBand(1).WriteArray(arr)
            # ?dataset.GetRasterBand(1).ComputeStatistics(0)
            dataset = None
            return filename
    return None


def Numpy2AAIGrid(data, geotransform, filename, nodata=-9999):
    """
    Numpy2AAIGrid
    """
    (x0, pixelXSize, rot, y0, rot, pixelYSize) = geotransform
    (rows, cols) = data.shape
    stream = open(filename, "wb")
    stream.write("ncols         %d\r\n" % (cols))
    stream.write("nrows         %d\r\n" % (rows))
    stream.write("xllcorner     %d\r\n" % (x0))
    stream.write("yllcorner     %d\r\n" % (y0 + pixelYSize * rows))
    stream.write("cellsize      %d\r\n" % (pixelXSize))
    stream.write("NODATA_value  %d\r\n" % (nodata))
    template = ("%.7g " * cols) + "\r\n"
    for row in data:
        line = template % tuple(row.tolist())
        stream.write(line)
    stream.close()
    return filename

def Numpy2Gdal(data, geotransform, projection, filename, nodata=-9999):
    """
    Numpy2Gdal
    """
    ext = os.path.splitext(filename)[1][1:].strip().lower()
    mkdirs(justpath(filename))
    if ext == "tif" or ext == "tiff":
        return Numpy2GTiff(data, geotransform, projection, filename, nodata)
    elif ext == "asc":
        return Numpy2AAIGrid(data, geotransform, filename, nodata)
    else:
        return ""


def GetNoData(filename):
    """
    GetNoData
    """
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        data, band, dataset = None, None, None
        return nodata
    return None


def SetNoData(filename, nodata=9999):
    """
    SetNoData
    """
    dataset = gdal.Open(filename, gdalconst.GA_Update)
    if dataset:
        band = dataset.GetRasterBand(1)
        nodata = band.SetNoDataValue(nodata)
        data, band, dataset = None, None, None
    return None



# -------------------------------------------------------------------------------
#   Main loop
# -------------------------------------------------------------------------------
if __name__ == '__main__':
    filename = r"C:/Users/vlr20/Desktop/PD_E_2D_TORRENTE.dxf|layerid=0|geometrytype=LineString"
    print(GDAL_META(filename))
