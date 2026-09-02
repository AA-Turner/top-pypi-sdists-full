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
# Name:        gdal_shape.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     26/07/2017
# -------------------------------------------------------------------------------
"""apt-get -y install gdal-bin libgdal-dev python-gdal"""

from .gdal_utils import *


def GetFeatures(fileshp):
    """
    GetFeatures
    """
    res = []
    dataset = ogr.OpenShared(fileshp)
    if dataset:
        layer = dataset.GetLayer(0)
        for feature in layer:
            res.append(feature)
    dataset = None
    return res


def GetFeatureByFid(fileshp, layername=0, fid=0):
    """
    GetFeatureByFid
    """
    feature = None
    dataset = ogr.OpenShared(fileshp)
    if dataset:
        layer = dataset.GetLayer(layername)
        feature = layer.GetFeature(fid)
    dataset = None
    return feature


def GetFeatureBy(fileshp, layername=0, attrname="ogr_id", attrvalue=0):
    """
    GetFeatureByAttr - get the first feature with attrname=attrvalue
    """
    feature = None
    dataset = ogr.OpenShared(fileshp)
    if dataset:
        layer = dataset.GetLayer(layername)
        layerDefinition = layer.GetLayerDefn()
        fieldnames = [layerDefinition.GetFieldDefn(j).GetName().lower() for j in range(layerDefinition.GetFieldCount())]
        print(fieldnames)
        if attrname.lower() in fieldnames:
            for feature in layer:
                if feature.GetField(attrname) == attrvalue:
                    dataset = None
                    return feature

    dataset = None
    return None


def removeShape(filename):
    """
    removeShape
    """
    try:
        if file(filename):
            driver = ogr.GetDriverByName('ESRI Shapefile')
            driver.DeleteDataSource(filename)
    except Exception as ex:
        print(ex)
        return None


def SaveFeature(feature, fileshp=""):
    """
    SaveFeature
    """
    fileshp = fileshp if fileshp else "%d.shp" % (feature.GetField("OBJECTID"))
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(fileshp):
        driver.DeleteDataSource(fileshp)
    ds = driver.CreateDataSource(fileshp)
    geom = feature.GetGeometryRef()
    layer = ds.CreateLayer(fileshp, srs=geom.GetSpatialReference(), geom_type=geom.GetGeometryType())

    # create a field
    # idField = ogr.FieldDefn(fieldName, fieldType)
    # layer.CreateField(idField)

    # Create the feature and set values
    featureDefn = layer.GetLayerDefn()
    layer.CreateFeature(feature)
    feature = None
    ds = None
    return fileshp


def Bounds2shp(minx, miny, maxx, maxy, epsg=3857, fileout="extent.shp"):
    """
    Extent2shp
    """
    # (minx, miny, maxx, maxy) = extent
    minx, miny, maxx, maxy = val(minx), val(miny), val(maxx), val(maxy)
    minx, miny, maxx, maxy = min(minx, maxx), min(miny, maxy), max(minx, maxx), max(miny, maxy)

    rect = ogr.Geometry(ogr.wkbLinearRing)
    rect.AddPoint(minx, miny)
    rect.AddPoint(maxx, miny)
    rect.AddPoint(maxx, maxy)
    rect.AddPoint(minx, maxy)
    rect.AddPoint(minx, miny)

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(rect)

    # Save extent to a new Shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(fileout):
        driver.DeleteDataSource(fileout)

    # Create the output shapefile
    ds = driver.CreateDataSource(fileout)
    layername = juststem(fileout)
    srs = ogr.osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    strtofile(srs.ExportToWkt(), forceext(fileout, "prj"))

    layer = ds.CreateLayer(layername, geom_type=ogr.wkbPolygon)
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(poly)
    layer.CreateFeature(feature)
    feature, ds = None, None
    return fileout

def Extent2shp(filename, fileout=""):
    """
    Extent2shp
    """
    fileout = fileout if fileout else forceext(filename, "ext.shp")
    layername, (minx, miny, maxx, maxy), proj4, geomtype, dontcare = GDAL_META(filename)
    rect = ogr.Geometry(ogr.wkbLinearRing)
    rect.AddPoint(minx, miny)
    rect.AddPoint(maxx, miny)
    rect.AddPoint(maxx, maxy)
    rect.AddPoint(minx, maxy)
    rect.AddPoint(minx, miny)
    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(rect)

    # Save extent to a new Shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # Remove output shapefile if it already exists
    if os.path.exists(fileout):
        driver.DeleteDataSource(fileout)

    # Create the output shapefile
    ds = driver.CreateDataSource(fileout)
    srs = ogr.osr.SpatialReference()
    srs.ImportFromProj4(proj4)
    strtofile(srs.ExportToWkt(), forceext(fileout, "prj"))

    layer = ds.CreateLayer(layername, geom_type=ogr.wkbPolygon)
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(poly)
    layer.CreateFeature(feature)
    feature, ds = None, None
    return fileout


def XYZ2Shp(filecsv, t_srs="EPSG:4326", fileout=None):
    """
    XYZ2Shp
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')
    fileout = forceext(filecsv, "shp") if not fileout else fileout
    remove(fileout)
    layername = juststem(fileout)
    # print(layername)
    dataset = driver.CreateDataSource(fileout)
    # important fix layername!!!!!
    layername = layername.encode('utf-8')
    # end fix
    layer = dataset.CreateLayer(layername, None, ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("VALUE", ogr.OFTReal))
    srs = None
    try:
        # Set the SpatialReference
        srs = ogr.osr.SpatialReference()
        epsg = val(t_srs.upper().replace("EPSG:", ""))
        srs.ImportFromEPSG(epsg)
        strtofile(srs.ExportToWkt(), forceext(fileout, "prj"))
    except Exception as ex:
        print(ex)

    with open(filecsv, 'rb') as stream:
        line = stream.readline()

        while line:
            arr = line.strip(" \r\n").split(",")
            arr = [item for item in arr if len(item) > 0]
            if len(arr) >= 3 and val(arr[0]) != None and val(arr[1]) != None and val(arr[2]) != None:
                X, Y, value = val(arr[0]), val(arr[1]), val(arr[2])
                feature = ogr.Feature(layer.GetLayerDefn())
                geom = ogr.CreateGeometryFromWkt("POINT (%s %s)" % (X, Y))
                if srs:
                    geom.AssignSpatialReference(srs)
                feature.SetGeometry(geom)
                feature.SetField2("VALUE", value)

                # Save the feature on the layer
                layer.CreateFeature(feature)
                feature.Destroy()
            line = stream.readline()
    return fileout


def XYZ2VRT(filename, t_srs="EPSG:4326", fileout=None):
    """
    XYZ2VRT
    """
    fileout = fileout if fileout else forceext(filename, "csv")
    filevrt = forceext(fileout, "vrt")
    ws = open(fileout, "wb")
    # ws.write("""X,Y,Z\n""")
    with open(filename, 'rb') as stream:
        line = stream.readline()
        while line:
            line = line.strip(" \r\n")
            line = re.sub(r'\s+', ',', line)
            if len(line.split(",")) == 5:
                arr = line.split(",")
                arr = val(arr)
                arr[0] *= 1000
                arr[1] *= 1000
                arr = ["%g" % item for item in arr[:3]]
                line = ",".join(arr)
                ws.write(line + "\n")
            line = stream.readline()
        ws.close()
    ##    srs = ogr.osr.SpatialReference()
    ##    epsg= val(t_srs.upper().replace("EPSG:",""))
    ##    srs.ImportFromEPSG(epsg)
    env = {"layername": juststem(fileout), "fileout": fileout, "t_srs": t_srs}
    text = """<OGRVRTDataSource>
    <OGRVRTLayer name="{layername}">
        <SrcDataSource>{fileout}</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <GeometryField encoding="PointFromColumns" x="field_1" y="field_2" z="field_3"/>
        <LayerSRS>{t_srs}</LayerSRS>
    </OGRVRTLayer>
</OGRVRTDataSource>"""
    text = sformat(text, env)
    strtofile(text, filevrt)


# -------------------------------------------------------------------------------
#   Main loop
# -------------------------------------------------------------------------------
if __name__ == '__main__':
    workdir = r"D:\Users\vlr20\Projects\BitBucket\OpenSITUA\projects\project88"

    chdir(workdir)
    pass
