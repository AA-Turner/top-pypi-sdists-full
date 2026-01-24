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
# Name:        xml_utils.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     13/08/2017
# -------------------------------------------------------------------------------
from .filesystem import *
import json
from xmljson import yahoo as bf
from xml.etree.ElementTree import fromstring

# -------------------------------------------------------------------------------
#   parsexml
# -------------------------------------------------------------------------------
def parsexml(filename, patching=True):
    """
    parsexml
    """
    if isinstance(filename, (dict)):
        return filename
    elif isstring(filename) and filename.startswith("<"):
        text = filename
    elif file(filename):
        text = filetostr(filename)
    else:
        return ""
    # patch  remove text that could create problems in javascript parsing
    if patching:
        text2remove = textin(text, "![CDATA[", "]]", False)
        text = text.replace(text2remove, "")

        # text = text.replace("&lt;","<")
    # end patch
    data = bf.data(fromstring(text))
    return data


def qml2json(filename):
    """
    qml2json
    """
    data = parsexml(filename, True)
    text = json.dumps(data)
    return text


def readMSSQL(filename):
    """
    readMSSQL
    """
    env = {}
    xml = parsexml(filename)
    if xml:
        conn = xml["qgsMssqlConnections"]["mssql"]
        env["server"] = conn["host"]
        env["uid"] = conn["username"]
        env["pwd"] = conn["password"]
        env["database"] = conn["database"]
        env["catalog"] = "dbo"
        env["tablename"] = conn["name"]
    return env


def readmssqlstring(text):
    #   "dbname='Catasto' host=.\SQLEXPRESS user='sa' password='12345' srid=4326 type=MultiPolygon table="dbo"."SearchComboBox" (Geometry) sql="  from .qgs file
    #   "MSSQL:server=.\SQLEXPRESS;trusted_connection=no;uid=sa;pwd=12345;database=Catasto;"   MSSQLSpatial dns
    #   "DRIVER={SQL Server};SERVER=.\SQLEXPRESS;PORT=1433;DATABASE=Catasto;uid=sa;pwd=12345"  ODBC
    #
    env = {}
    DICTIONARY = {"host": "server", "user": "uid", "password": "pwd", "dbname": "database", "table": "tablename",
                  "type": "geometry_type"}
    text = text.replace("MSSQL:", "")

    arr = listify(text, " ;")
    for item in arr:
        item = item.split("=", 1)
        if len(item) > 1:
            key = DICTIONARY[item[0]] if item[0] in DICTIONARY else item[0]
            env[key] = ("%s" % item[1]).strip("'")
    # some correction
    if "tablename" in env and "." in env["tablename"]:
        text = chrtran(env["tablename"], '"', '')
        env["catalog"], env["tablename"] = text.split(".", 1)
    return env


def readwmsstring(text):
    env = {}
    text = re.sub(r' ', '&', text)
    arr = listify(text, "&")
    for item in arr:
        item = item.split("=", 1)
        if len(item) > 1:
            key = item[0]
            env[key] = ("%s" % item[1]).strip("'")

    return env


def createMSSQLconn(text, filename):
    if file(filename):
        return filename
    env = readmssqlstring(text)
    text = """<!DOCTYPE connections>
<qgsMssqlConnections version="1.0">
    <mssql port="" saveUsername="true" password="{pwd}" savePassword="true" sslmode="1" service="" username="{uid}" host="{server}" database="{database}" name="{tablename}" estimatedMetadata="true"/>
</qgsMssqlConnections>
"""
    text = sformat(text, env)
    strtofile(text, filename)
    return filename


def parseqgsextent(filename):
    layers = []
    data = parsexml(filename)
    qgis = data["qgis"]
    extent = qgis["mapcanvas"]["extent"]
    extent["rotation"] = qgis["mapcanvas"]["rotation"]
    return extent


def parseqgslayers(filename):
    layers = []
    data = parsexml(filename)
    qgis = data["qgis"]
    layer_tree_group = qgis["layer-tree-group"]
    projectlayers = qgis["projectlayers"]

    if "maplayer" not in projectlayers:
        return []

    MAPLAYERS = {}
    maplayers = listify(projectlayers["maplayer"])
    for maplayer in maplayers:
        MAPLAYERS[maplayer["id"]] = maplayer

    LAYERS = []
    layer_tree_layers = parseqgstree(layer_tree_group)
    for layer_tree_layer in layer_tree_layers:

        maplayer = MAPLAYERS[layer_tree_layer["id"]]

        # path for overwrite legend if qml exists
        if "datasource" in maplayer:
            fileqml = forceext(maplayer["datasource"], "qml")
            fileqml = fileqml if os.path.isabs(fileqml) else justpath(filename) + "/" + fileqml
            if file(fileqml):
                qml = parsexml(fileqml)
                maplayer["pipe"] = qml["qgis"]["pipe"]
        # end patch

        maplayer["layer_tree_group"] = layer_tree_layer["layer-tree-group"]
        maplayer["expanded"] = layer_tree_layer["expanded"]
        maplayer["checked"] = layer_tree_layer["checked"]
        LAYERS += [maplayer]

    return LAYERS


def parseqgstree(layer_tree_group, group_name=""):
    layers = []
    group_name += "/" + layer_tree_group["name"] if layer_tree_group["name"] else ""
    for item in layer_tree_group:
        if item == "layer-tree-layer":
            lyrs = listify(layer_tree_group["layer-tree-layer"])
            for lyr in lyrs:
                lyr["layer-tree-group"] = group_name
            layers += lyrs
        elif item == "layer-tree-group":
            lyrs = listify(layer_tree_group["layer-tree-group"])
            for lyr in lyrs:
                layers += parseqgstree(lyr, group_name)

    return layers


def qmlfromqgs(fileqgs, layername):
    text = filetostr(fileqgs)
    maplayer = textbetween(text, "<maplayer", "</maplayer>", False)
    while "<maplayer" in text:
        subtext = textbetween(text, "<maplayer", "</maplayer>", False)
        xml = parsexml(subtext)
        layerid = xml["maplayer"]["id"]
        if layerid.lower().startswith(layername.lower()):
            # qmltext = subtext.replace("<maplayer","<qgis").replace("</maplayer>","</qgis>")
            qmltext = subtext
            return qml2json(qmltext)
        # ---> go next maplayer
        text = text.replace(subtext, "")


if __name__ == '__main__':
    workdir = r"D:\Program Files (x86)\GecoGIS\projects\example"
    chdir(workdir)
    print(parsexml("gfi_po3857.qml"))
