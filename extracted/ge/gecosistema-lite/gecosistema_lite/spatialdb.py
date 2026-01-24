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
# Name:        spatialite.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     23/11/2017
# -------------------------------------------------------------------------------
from .sqlitedb import *
from .number import *
from .execution import Kriging
from osgeo import ogr, osr
import sqlite3


class SpatialDB(SqliteDB):

    def __init__(self, filename, modules=[]):
        """
        Constructor
        :param filename:
        """
        SqliteDB.__init__(self, filename, ["mod_spatialite"] + modules)
        self.CreateSpatialReferenceTable()
        self.CreateGeometryColumnTable()

    def CreateSpatialReferenceTable(self):
        sql = """
        CREATE TABLE [spatial_ref_sys] (
          [srid] INTEGER NOT NULL PRIMARY KEY, 
          [auth_name] TEXT NOT NULL, 
          [auth_srid] INTEGER NOT NULL, 
          [ref_sys_name] TEXT NOT NULL DEFAULT 'Unknown', 
          [proj4text] TEXT NOT NULL, 
          [srtext] TEXT NOT NULL DEFAULT 'Undefined');
        --INSERT OR REPLACE INTO [spatial_ref_sys](srid,auth_name,auth_srid,ref_sys_name,proj4text,srtext)
        --VALUES ({epsg},'epsg',{epsg},'epsg:'||{epsg},'{proj4text}','{srtext}');
        """
        self.execute(sql)

    def CreateGeometryColumnTable(self):
        sql = """
        CREATE TABLE IF NOT EXISTS [geometry_columns] (
          [f_table_name] VARCHAR, 
          [f_geometry_column] VARCHAR, 
          [geometry_type] INTEGER, 
          [coord_dimension] INTEGER, 
          [srid] INTEGER, 
          [geometry_format] VARCHAR, 
          PRIMARY KEY ([f_table_name]));
        """
        self.execute(sql)

    def CreateLayer(self, layername, epsg=3857, fieldnames="", fieldtypes="", geom_type=1, overwrite=True,
                    verbose=False):

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)

        fieldnames = ["geometry"] + listify(fieldnames)
        fieldnames = wrap(fieldnames, "[", "]")
        fieldtypes = ["BLOB"] + listify(fieldtypes)
        r = len(fieldnames) - len(fieldtypes)
        r = r if r >= 0 else 0
        fieldtypes = fieldtypes + ["TEXT"] * r
        fielddefs = [" ".join(item) for item in zip(fieldnames, fieldtypes)]
        fielddefs = ','.join(fielddefs)

        env = {
            "layername": layername,
            "epsg": epsg,
            "geom_type": geom_type,  # 1=Point,3=Polygons
            "proj4text": srs.ExportToProj4(),
            "srtext": srs.ExportToWkt(),
            "fielddefs": fielddefs,
            "if_overwrite": "" if overwrite else "--"
        }

        sql = """
        {if_overwrite}DROP TABLE IF EXISTS [{layername}];
        CREATE TABLE IF NOT EXISTS [{layername}](ogc_fid INTEGER PRIMARY KEY AUTOINCREMENT,{fielddefs});
        INSERT OR IGNORE INTO [geometry_columns]( f_table_name,f_geometry_column,geometry_type,coord_dimension,srid,geometry_format)
            VALUES('{layername}','geometry',{geom_type},2,{epsg},'WKB');
        INSERT OR IGNORE INTO [spatial_ref_sys](srid,auth_name,auth_srid,ref_sys_name,proj4text,srtext)
            VALUES ({epsg},'epsg',{epsg},'epsg:'||{epsg},'{proj4text}','{srtext}');
        """
        self.execute(sql, env, verbose=verbose)

    def CreateFeatureFromGeometry(self, layername, geom, verbose=False):
        """
        CreateFeatureFromGeometry
        """
        env = {"layername": layername}
        if isstring(geom):
            geom = ogr.CreateGeometryFromWkt(geom)
        values = [(sqlite3.Binary(geom.ExportToWkb()),)]
        # values = [(sqlite3.Binary(geom),)]
        self.execute("BEGIN;", commit=False)
        sql = """INSERT INTO [{layername}]([geometry]) VALUES(?);"""
        self.executemany(sql, env, values, commit=False, verbose=verbose)
        ogc_fid = self.executeScalar("SELECT MAX(ogc_fid) FROM [{layername}]", env, commit=False, verbose=verbose)
        self.execute("END;")
        return ogc_fid

    def UpdateFeature(self, layername, ogc_fid, fieldnames, values, verbose=False):
        """
        UpdateFeature
        """
        fnames, fvalues = [], []
        fieldnames, values = listify(fieldnames), listify(values)
        tablefields = lower(self.GetFieldNames(layername))
        for j in range(len(fieldnames)):
            fieldname = fieldnames[j].lower()
            if fieldname in tablefields:
                fnames.append(fieldname)
                if fieldname == "geometry":
                    values[j] = sqlite3.Binary(values[j].ExportToWkb())
                fvalues.append(values[j])

        updates = ",".join(["[%s]=?" % item for item in fnames])
        env = {"layername": layername, "fieldnames": ",".join(wrap(fnames, "[", "]")), "updates": updates,
               "ogc_fid": ogc_fid}
        sql = """
        UPDATE [{layername}] SET {updates} 
        WHERE ogc_fid = {ogc_fid};
        """
        self.executemany(sql, env, [fvalues], verbose=verbose)
        res = self.execute("SELECT {fieldnames} FROM [{layername}] WHERE ogc_fid={ogc_fid} LIMIT 1;", env,
                           keepdims=True, outputmode="object", verbose=verbose)
        return res[0] if len(res) > 0  else {}

    def DeleteFeature(self, layername, fid, verbose=False):
        """
        DeleteFeature
        """
        env = {
            "layername": layername,
            "fid": fid
        }
        sql = """DELETE FROM [{layername}] WHERE [ogc_fid]={fid};"""
        self.execute(sql, env, verbose=verbose)

    def GridFromExtent(self, layername, extent, dx=500.0, dy=None, verbose=False):
        """
        GridFromExtent -  Create a Receptor Grid
        """
        [minx, miny, maxx, maxy] = extent
        minx, miny, maxx, maxy = val(minx), val(miny), val(maxx), val(maxy)
        minx, miny, maxx, maxy = min(minx, maxx), min(miny, maxy), max(minx, maxx), max(miny, maxy)

        dx = float(dx)
        dy = float(dy) if dy else dx

        width = maxx - minx
        height = maxy - miny
        m, n = int(round(height / dy)), int(round(width / dx))

        rx = width - ((n - 1) * dx)
        ry = height - ((m - 1) * dy)

        values = []
        for i in range(m):
            for j in range(n):
                x = minx + (rx / 2.0) + (dx * j)
                y = miny + (ry / 2.0) + (dy * i)
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint_2D(x, y)
                blob = sqlite3.Binary(point.ExportToWkb())
                values.append((blob,))

        self.executemany("""INSERT OR REPLACE INTO [{layername}](geometry) VALUES(?);""", {"layername": layername},
                         values, verbose=verbose)

    def GridFromPoly(self, layername, geojson, dx=500.0, dy=None, verbose=False):
        """
        GridFromPoly
        """
        if isstring(geojson):
            geom = ogr.CreateGeometryFromJson(geojson)
        else:
            geom = geojson
        (minx, maxx, miny, maxy) = geom.GetEnvelope()

        minx, miny, maxx, maxy = val(minx), val(miny), val(maxx), val(maxy)
        minx, miny, maxx, maxy = min(minx, maxx), min(miny, maxy), max(minx, maxx), max(miny, maxy)

        dx = float(dx)
        dy = float(dy) if dy else dx

        width = maxx - minx
        height = maxy - miny
        m, n = int(round(height / dy)), int(round(width / dx))

        rx = width - ((n - 1) * dx)
        ry = height - ((m - 1) * dy)

        values = []
        for i in range(m):
            for j in range(n):
                x = minx + (rx / 2.0) + (dx * j)
                y = miny + (ry / 2.0) + (dy * i)
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint_2D(x, y)
                if point.Within(geom):
                    blob = sqlite3.Binary(point.ExportToWkb())
                    values.append((blob,))

        self.executemany("""INSERT OR REPLACE INTO [{layername}](geometry) VALUES(?);""", {"layername": layername},
                         values, verbose=verbose)

    def RectFromExtent(self, layername, extent, verbose=False):
        """
        RectFromExtent -  Create a Rectangle (LineString)  From extent
        """
        [minx, miny, maxx, maxy] = extent
        minx, miny, maxx, maxy = val(minx), val(miny), val(maxx), val(maxy)
        minx, miny, maxx, maxy = min(minx, maxx), min(miny, maxy), max(minx, maxx), max(miny, maxy)

        rect = ogr.Geometry(ogr.wkbLinearRing)
        rect.AddPoint_2D(minx, miny)
        rect.AddPoint_2D(maxx, miny)
        rect.AddPoint_2D(maxx, maxy)
        rect.AddPoint_2D(minx, maxy)
        rect.AddPoint_2D(minx, miny)
        # Create polygon
        geom_poly = ogr.Geometry(ogr.wkbPolygon)
        geom_poly.AddGeometry(rect)
        blob = sqlite3.Binary(geom_poly.ExportToWkb())
        values = [(blob,)]
        self.executemany("""INSERT OR REPLACE INTO [{layername}](geometry) VALUES(?);""", {"layername": layername},
                         values, verbose=verbose)

    def LineSegmentation(self, src_layer, dst_layer, step=50, overwrite=False):
        """
        LineSegmentation -  Transform a line in a collection of points
        """
        env = {"src_layer": src_layer, "dst_layer": dst_layer}
        self.CreateLayer(dst_layer, epsg=3857, fieldnames="p_ogc_fid", fieldtypes="INTEGER", geom_type=ogr.wkbPoint,
                         overwrite=overwrite)
        lines = self.execute("""SELECT ogc_fid,geometry,step FROM [{src_layer}] WHERE enabled;""", env,
                             outputmode="cursor")
        for (ogc_fid, buff, step) in lines:

            line = ogr.CreateGeometryFromWkb(buff) #str(buff)

            n = line.GetPointCount()
            points = []
            for j in range(1, n):
                c0 = line.GetPoint(j - 1)
                c2 = line.GetPoint(j)
                cosA = cosx(c0, c2)  # coseno in funzione della tangente
                sinA = sinx(c0, c2)
                l = 0.0
                d = dist(c0, c2)

                while l < d:
                    geom = ogr.Geometry(ogr.wkbPoint)
                    geom.AddPoint_2D(c0[0] + l * cosA, c0[1] + l * sinA)
                    points.append((ogc_fid, sqlite3.Binary(geom.ExportToWkb()),))
                    l += step

                #2021-02-10
                # aggiunta di un punto finale anche se la distanza <step
                if False and l>=d:
                    geom = ogr.Geometry(ogr.wkbPoint)
                    geom.AddPoint_2D( c2[0] , c2[1] )
                    points.append((ogc_fid, sqlite3.Binary(geom.ExportToWkb()),))

            self.executeMany("""INSERT OR REPLACE INTO [{dst_layer}](p_ogc_fid,geometry) VALUES(?,?);""", env, points)

    def CreateShape(self, layername, fileshp="", fieldnames=""):
        env = {"layername": layername}
        (f_geometry_column, geometry_type, srid,) = self.execute(
            "SELECT f_geometry_column,geometry_type,srid FROM [geometry_columns] WHERE f_table_name='{layername}';",
            env, outputmode="array", keepdims=False)
        env["f_geometry_column"] = f_geometry_column
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(srid)

        fileshp = fileshp if fileshp else forceext(juststem(layername), "shp")
        mkdirs(justpath(fileshp))
        driver = ogr.GetDriverByName("ESRI Shapefile")
        if file(fileshp):
            driver.DeleteDataSource(fileshp)
        ds = driver.CreateDataSource(fileshp)
        layer = ds.CreateLayer(str(layername), srs, geometry_type)

        if fieldnames == "*":
            items = self.GetFieldNames(layername, "INTEGER|FLOAT|TEXT", typeinfo=True)
            fieldnames = [fieldname for fieldname, _ in items]
            for fieldname, ftype in items:
                if ftype == "INTEGER":
                    ogrtype = ogr.OFTInteger
                elif ftype == "FLOAT":
                    ogrtype = ogr.OFTReal
                elif ftype == "TEXT":
                    ogrtype = ogr.OFTString
                else:
                    ogrtype = ogr.OFTReal
                layer.CreateField(ogr.FieldDefn(str(fieldname)[:10], ogrtype))
        else:
            fieldnames = listify(fieldnames)

            for fieldname in fieldnames:
                layer.CreateField(ogr.FieldDefn(str(fieldname)[:10], ogr.OFTReal))

        features = self.execute("SELECT * FROM [{layername}];", env, outputmode="object", verbose=False)
        for row in features:
            #geom = ogr.CreateGeometryFromWkb(str(row[f_geometry_column]))
            geom = ogr.CreateGeometryFromWkb(row[f_geometry_column])
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetFID(row["ogc_fid"])
            for fieldname in fieldnames:
                if fieldname in row:
                    feature.SetField(str(fieldname)[:10], row[fieldname])
            feature.SetGeometry(geom)
            layer.CreateFeature(feature)
            feature = None

        return fileshp


    def From(filename, sheetnames=None, nodata=["", "Na", "NaN", "-", "--", "---", "N/A"], guess_primary_key=True,
             verbose=False):
        """
        Initialize db from filename or sql
        """

        if isfiletype(filename, "db,sqlite"):
            return SpatialDB(filename)

        elif isfiletype(filename, "xls,xlsx,csv,txt,dat", check_if_exists=True):
            dsn = forceext(filename, "sqlite") if verbose else ":memory:"
            db = SpatialDB(dsn)
            db.importFrom(filename, sheetnames=sheetnames, Temp=False, nodata=nodata)
            return db

        elif isfile(forceext(filename, "sqlite")):
            db = SpatialDB(forceext(filename, "sqlite"))
            return db

        elif isquery(filename):
            # get from a simple sql string
            filexls, sheetname = SqliteDB.GetTablenameFromQuery(filename)
            filedb = forceext(filexls, "sqlite")
            if isfilexls(filexls, True):
                db = SpatialDB(filedb)
                db.importFrom(filexls, sheetnames=sheetname, Temp=False, nodata=nodata)
                return db
            elif isfile(filedb):
                db = SpatialDB(filedb)
                return db

        return None

    From = staticmethod(From)


def main():
    workdir = r'D:\Users\vlr20\Projects\BitBucket\OpenSITUA\projects\Valerio\Test00'
    chdir(workdir)
    pass




if __name__ == "__main__":
    main()
