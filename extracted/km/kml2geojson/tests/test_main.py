import xml.dom.minidom as md
import io
import pytest

from .context import DATA_DIR
import kml2geojson.main as m


def _parse(xml: str):
    return md.parseString(xml)


def _read_kml(path):
    with open(path, encoding="utf-8", errors="ignore") as src:
        return md.parseString(src.read())


def test_get():
    # section: returns all matching nodes
    root = _parse(
        """
        <Document>
          <Placemark id="a" />
          <Placemark id="b" />
          <Folder />
        </Document>
        """
    )
    placemarks = m.get(root, "Placemark")
    assert len(placemarks) == 2
    assert placemarks[0].getAttribute("id") == "a"
    assert placemarks[1].getAttribute("id") == "b"

    # section: returns empty list when tag is missing
    assert list(m.get(root, "Missing")) == []


def test_get1():
    # section: returns first matching node
    root = _parse(
        """
        <Document>
          <Placemark id="a" />
          <Placemark id="b" />
        </Document>
        """
    )
    first = m.get1(root, "Placemark")
    assert first is not None
    assert first.getAttribute("id") == "a"

    # section: returns None when tag is missing
    assert m.get1(root, "Missing") is None


def test_attr():
    # section: returns attribute value
    root = _parse('<Placemark id="abc" />')
    node = m.get1(root, "Placemark")
    assert node is not None
    assert m.attr(node, "id") == "abc"

    # section: returns empty string when attribute is missing
    assert m.attr(node, "name") == ""


def test_val():
    # section: strips surrounding whitespace
    root = _parse("<name>  Hello world  </name>")
    assert m.val(root.documentElement) == "Hello world"

    # section: handles cdata content
    root = _parse("<description><![CDATA[ hello ]]></description>")
    assert m.val(root.documentElement) == "hello"

    # section: returns empty string when no text content exists
    root = _parse("<name></name>")
    assert m.val(root.documentElement) == ""


def test_valf():
    # section: parses float text
    root = _parse("<width>2.5</width>")
    assert m.valf(root.documentElement) == 2.5

    # section: returns None for non-float text
    root = _parse("<width>abc</width>")
    assert m.valf(root.documentElement) is None


def test_numarray():
    # section: converts numeric strings to floats
    assert m.numarray(["1", "2.5", "-3"]) == [1.0, 2.5, -3.0]


def test_coords1():
    # section: parses one kml coordinate tuple
    assert m.coords1(" -112.2,36.0,2357 ") == [-112.2, 36.0, 2357.0]


def test_coords():
    # section: parses multiple kml coordinate tuples
    actual = m.coords(
        """
        -112.0,36.1,0
        -113.0,36.0,0
        """
    )
    assert actual == [[-112.0, 36.1, 0.0], [-113.0, 36.0, 0.0]]


def test_fix_ring():
    # section: closes an unclosed ring
    assert m.fix_ring([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]]) == [
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 0.0],
    ]

    # section: leaves a closed ring unchanged
    ring = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]]
    assert m.fix_ring(ring) == ring

    # section: leaves an empty ring unchanged
    assert m.fix_ring([]) == []


def test_gx_coords1():
    # section: parses one gx coordinate tuple
    assert m.gx_coords1("-113.0 36.0 0") == [-113.0, 36.0, 0.0]


def test_gx_coords():
    # section: extracts gx track coordinates and timestamps
    root = _parse(
        """
        <gx:Track xmlns:gx="http://www.google.com/kml/ext/2.2">
          <when>2020-01-01T00:00:00Z</when>
          <when>2020-01-01T00:01:00Z</when>
          <gx:coord>-113.0 36.0 0</gx:coord>
          <gx:coord>-113.1 36.1 1</gx:coord>
        </gx:Track>
        """
    )
    actual = m.gx_coords(root.documentElement)
    assert actual == {
        "coordinates": [[-113.0, 36.0, 0.0], [-113.1, 36.1, 1.0]],
        "times": ["2020-01-01T00:00:00Z", "2020-01-01T00:01:00Z"],
    }

    # section: falls back to unprefixed coord elements
    root = _parse(
        """
        <Track>
          <when>2020-01-01T00:00:00Z</when>
          <coord>-113.0 36.0 0</coord>
        </Track>
        """
    )
    actual = m.gx_coords(root.documentElement)
    assert actual == {
        "coordinates": [[-113.0, 36.0, 0.0]],
        "times": ["2020-01-01T00:00:00Z"],
    }


def test_disambiguate():
    # section: leaves unique names unchanged
    assert m.disambiguate(["a", "b"]) == ["a", "b"]

    # section: appends mark repeatedly to duplicates
    assert m.disambiguate(["sing", "song", "sing", "sing"]) == [
        "sing",
        "song",
        "sing1",
        "sing11",
    ]

    # section: supports custom mark
    assert m.disambiguate(["x", "x"], mark="_") == ["x", "x_"]


def test_to_filename():
    # section: strips unsafe characters and normalizes spaces
    assert m.to_filename("% A dbla'{-+)(ç? ") == "A_dbla-ç"

    # section: keeps dots dashes and underscores
    assert m.to_filename("a b-c_d.txt") == "a_b-c_d.txt"


def test_build_rgb_and_opacity():
    # section: parses 8-char kml color
    assert m.build_rgb_and_opacity("ee001122") == ("#221100", 0.93)

    # section: full alpha yields opacity one
    assert m.build_rgb_and_opacity("ff334455") == ("#554433", 1.0)

    # section: parses 6-char color
    assert m.build_rgb_and_opacity("001122") == ("#221100", 1)

    # section: parses 3-char color
    assert m.build_rgb_and_opacity("abc") == ("#cba", 1)

    # section: ignores leading hash
    assert m.build_rgb_and_opacity("#ee001122") == ("#221100", 0.93)


def test_build_schema():
    # section: maps simple field types to converters
    root = _parse(
        """
        <Document>
          <Schema>
            <SimpleField name="n" type="int" />
            <SimpleField name="x" type="float" />
            <SimpleField name="b" type="bool" />
            <SimpleField name="s" type="string" />
            <SimpleField name="u" type="wibble" />
          </Schema>
        </Document>
        """
    )
    schema = m.build_schema(root)
    assert schema["n"]("4") == 4
    assert schema["x"]("4.5") == 4.5
    assert schema["b"]("true") is True
    assert schema["b"]("0") is False
    assert schema["s"]("hi") == "hi"

    # section: unknown types fall back to identity
    assert schema["u"]("7") == "7"

    # section: returns empty dict when no simple fields exist
    root = _parse("<Document />")
    assert m.build_schema(root) == {}


def test_build_style():
    # section: extracts poly line label and icon styles
    root = _parse(
        """
        <Style id="s">
          <PolyStyle>
            <color>ee001122</color>
            <fill>1</fill>
            <outline>0</outline>
          </PolyStyle>
          <LineStyle>
            <color>ff334455</color>
            <width>2</width>
          </LineStyle>
          <LabelStyle>
            <color>7f334455</color>
            <scale>2</scale>
          </LabelStyle>
          <IconStyle>
            <color>a1ff00ff</color>
            <scale>1.5</scale>
            <heading>90</heading>
            <hotSpot x="0.5" y="0.5" xunits="fraction" yunits="fraction" />
            <Icon><href>https://example.com/pin.png</href></Icon>
          </IconStyle>
        </Style>
        """
    )
    actual = m.build_style(root)
    assert actual["fill"] == "#221100"
    assert actual["fill-opacity"] == 0.93
    assert actual["stroke"] == "#554433"
    assert actual["stroke-opacity"] == 1.0
    assert actual["stroke-width"] == 2.0
    assert actual["label-color"] == "#554433"
    assert actual["label-opacity"] == 0.5
    assert actual["label-scale"] == 2.0
    assert actual["icon-color"] == "#ff00ff"
    assert actual["icon-opacity"] == 0.63
    assert actual["icon-scale"] == 1.5
    assert actual["icon-heading"] == 90.0
    assert actual["icon-offset"] == [0.5, 0.5]
    assert actual["icon-offset-units"] == ["fraction", "fraction"]
    assert actual["iconUrl"] == "https://example.com/pin.png"

    # section: icon style does not wipe other styles
    root = _parse(
        """
        <Style id="s">
          <LineStyle>
            <color>ff334455</color>
          </LineStyle>
          <IconStyle>
            <Icon><href>https://example.com/pin.png</href></Icon>
          </IconStyle>
        </Style>
        """
    )
    actual = m.build_style(root)
    assert actual["stroke"] == "#554433"
    assert actual["iconUrl"] == "https://example.com/pin.png"


def test_build_svg_style():
    # section: maps polygon and line style fields
    root = _parse(
        """
        <Document>
          <Style id="poly">
            <PolyStyle>
              <color>ee001122</color>
              <fill>1</fill>
              <outline>0</outline>
            </PolyStyle>
            <LineStyle>
              <color>ff334455</color>
              <width>2</width>
            </LineStyle>
          </Style>
          <Style id="icon">
            <IconStyle>
              <Icon><href>https://example.com/pin.png</href></Icon>
            </IconStyle>
          </Style>
          <StyleMap id="map">
            <Pair>
              <key>normal</key>
              <styleUrl>#poly</styleUrl>
            </Pair>
            <Pair>
              <key>highlight</key>
              <styleUrl>#icon</styleUrl>
            </Pair>
          </StyleMap>
        </Document>
        """
    )
    actual = m.build_svg_style(root)
    assert actual["#poly"]["fill"] == "#221100"
    assert actual["#poly"]["fill-opacity"] == 0.93
    assert actual["#poly"]["stroke"] == "#554433"
    assert actual["#poly"]["stroke-opacity"] == 1.0
    assert actual["#poly"]["stroke-width"] == 2.0
    assert actual["#icon"] == {"iconUrl": "https://example.com/pin.png"}

    # section: resolves style maps to their normal pair
    assert actual["#map"] == actual["#poly"]

    # section: resolves style maps to their highlight pair when requested
    actual = m.build_svg_style(root, style_map_key="highlight")
    assert actual["#map"] == actual["#icon"]


def test_build_leaflet_style():
    # section: maps polygon line label and icon style fields
    root = _parse(
        """
        <Document>
          <Style id="poly">
            <PolyStyle>
              <color>ee001122</color>
              <fill>1</fill>
              <outline>0</outline>
            </PolyStyle>
            <LineStyle>
              <color>ff334455</color>
              <width>2</width>
            </LineStyle>
            <LabelStyle>
              <color>7f334455</color>
            </LabelStyle>
          </Style>
          <Style id="icon">
            <IconStyle>
              <scale>1.5</scale>
              <Icon><href>https://example.com/pin.png</href></Icon>
            </IconStyle>
          </Style>
          <StyleMap id="map">
            <Pair>
              <key>normal</key>
              <styleUrl>#poly</styleUrl>
            </Pair>
          </StyleMap>
        </Document>
        """
    )
    actual = m.build_leaflet_style(root)
    assert actual["#poly"]["fillColor"] == "#221100"
    assert actual["#poly"]["fillOpacity"] == 0.93
    assert actual["#poly"]["color"] == "#554433"
    assert actual["#poly"]["opacity"] == 1.0
    assert actual["#poly"]["weight"] == 2.0
    assert actual["#poly"]["labelColor"] == "#554433"
    assert actual["#icon"] == {
        "iconScale": 1.5,
        "iconUrl": "https://example.com/pin.png",
    }

    # section: resolves style maps to their normal pair
    assert actual["#map"] == actual["#poly"]


def test_build_geometry():
    # section: builds point geometry
    root = _parse(
        """
        <Placemark>
          <Point><coordinates>-113.0,36.0,0</coordinates></Point>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert actual["geoms"] == [{"type": "Point", "coordinates": [-113.0, 36.0, 0.0]}]
    assert actual["times"] == []

    # section: builds polygon geometry
    root = _parse(
        """
        <Placemark>
          <Polygon>
            <outerBoundaryIs>
              <LinearRing>
                <coordinates>
                  -1,1,0 -2,2,0 -3,3,0 -1,1,0
                </coordinates>
              </LinearRing>
            </outerBoundaryIs>
          </Polygon>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert actual["geoms"][0]["type"] == "Polygon"
    assert actual["geoms"][0]["coordinates"] == [
        [[-1.0, 1.0, 0.0], [-2.0, 2.0, 0.0], [-3.0, 3.0, 0.0], [-1.0, 1.0, 0.0]]
    ]

    # section: closes unclosed polygon rings
    root = _parse(
        """
        <Placemark>
          <Polygon>
            <outerBoundaryIs>
              <LinearRing>
                <coordinates>
                  -1,1,0 -2,2,0 -3,3,0
                </coordinates>
              </LinearRing>
            </outerBoundaryIs>
          </Polygon>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert actual["geoms"][0]["coordinates"][0][-1] == [-1.0, 1.0, 0.0]
    assert len(actual["geoms"][0]["coordinates"][0]) == 4

    # section: converts a bare linear ring to a linestring
    root = _parse(
        """
        <Placemark>
          <LinearRing>
            <coordinates>-1,1,0 -2,2,0 -3,3,0 -1,1,0</coordinates>
          </LinearRing>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert actual["geoms"][0]["type"] == "LineString"

    # section: gx track becomes linestring and captures times
    root = _parse(
        """
        <Placemark xmlns:gx="http://www.google.com/kml/ext/2.2">
          <gx:Track>
            <when>2020-01-01T00:00:00Z</when>
            <when>2020-01-01T00:01:00Z</when>
            <gx:coord>-113.0 36.0 0</gx:coord>
            <gx:coord>-113.1 36.1 1</gx:coord>
          </gx:Track>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert actual["geoms"][0]["type"] == "LineString"
    assert actual["geoms"][0]["coordinates"] == [
        [-113.0, 36.0, 0.0],
        [-113.1, 36.1, 1.0],
    ]
    assert actual["times"] == [["2020-01-01T00:00:00Z", "2020-01-01T00:01:00Z"]]

    # section: single-coordinate gx track becomes a point
    root = _parse(
        """
        <Placemark xmlns:gx="http://www.google.com/kml/ext/2.2">
          <gx:Track>
            <gx:coord>-113.0 36.0 0</gx:coord>
          </gx:Track>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert actual["geoms"][0] == {"type": "Point", "coordinates": [-113.0, 36.0, 0.0]}

    # section: multigeometry recurses to child container
    root = _parse(
        """
        <Placemark>
          <MultiGeometry>
            <Point><coordinates>-113.0,36.0,0</coordinates></Point>
            <LineString><coordinates>-113.0,36.0,0 -114.0,37.0,0</coordinates></LineString>
          </MultiGeometry>
        </Placemark>
        """
    )
    actual = m.build_geometry(root.documentElement)
    assert sorted(geom["type"] for geom in actual["geoms"]) == ["LineString", "Point"]


def test_build_feature():
    # section: keeps null geometry by default and skips it on request
    root = _parse("<Placemark><name>Empty</name></Placemark>")
    actual = m.build_feature(root.documentElement)
    assert actual is not None
    assert actual["geometry"] is None
    assert actual["properties"]["name"] == "Empty"
    assert m.build_feature(root.documentElement, skip_null_geometry=True) is None

    # section: builds feature with properties styles extended data timespan and id
    root = _parse(
        """
        <Placemark id="pm1">
          <name>Example</name>
          <address>1 Example St</address>
          <phoneNumber>555-1234</phoneNumber>
          <visibility>0</visibility>
          <description>Desc</description>
          <styleUrl>style-1</styleUrl>
          <ExtendedData>
            <Data name="foo"><value>bar</value></Data>
            <SimpleData name="baz">qux</SimpleData>
          </ExtendedData>
          <TimeSpan>
            <begin>2020-01-01</begin>
            <end>2020-01-02</end>
          </TimeSpan>
          <LineStyle>
            <color>ff334455</color>
            <width>2</width>
          </LineStyle>
          <PolyStyle>
            <color>ee001122</color>
            <fill>1</fill>
            <outline>0</outline>
          </PolyStyle>
          <Point><coordinates>-113.0,36.0,0</coordinates></Point>
        </Placemark>
        """
    )
    actual = m.build_feature(root.documentElement)
    assert actual is not None
    assert actual["id"] == "pm1"
    assert actual["geometry"]["type"] == "Point"
    assert actual["properties"]["name"] == "Example"
    assert actual["properties"]["address"] == "1 Example St"
    assert actual["properties"]["phoneNumber"] == "555-1234"
    assert actual["properties"]["visibility"] is False
    assert actual["properties"]["description"] == "Desc"
    assert actual["properties"]["styleUrl"] == "#style-1"
    assert actual["properties"]["foo"] == "bar"
    assert actual["properties"]["baz"] == "qux"
    assert actual["properties"]["timeSpan"] == {
        "begin": "2020-01-01",
        "end": "2020-01-02",
    }
    assert actual["properties"]["fill"] == "#221100"
    assert actual["properties"]["fill-opacity"] == 0.93
    assert actual["properties"]["stroke"] == "#554433"
    assert actual["properties"]["stroke-opacity"] == 1.0
    assert actual["properties"]["stroke-width"] == 2.0

    # section: marks cdata descriptions as html
    root = _parse(
        """
        <Placemark>
          <description><![CDATA[<b>Bold</b>]]></description>
          <Point><coordinates>-113.0,36.0,0</coordinates></Point>
        </Placemark>
        """
    )
    actual = m.build_feature(root.documentElement)
    assert actual["properties"]["description"] == {
        "@type": "html",
        "value": "<b>Bold</b>",
    }

    # section: extracts timestamps
    root = _parse(
        """
        <Placemark>
          <TimeStamp><when>2020-01-01T00:00:00Z</when></TimeStamp>
          <Point><coordinates>-113.0,36.0,0</coordinates></Point>
        </Placemark>
        """
    )
    actual = m.build_feature(root.documentElement)
    assert actual["properties"]["timeStamp"] == "2020-01-01T00:00:00Z"

    # section: types simple data via document schema
    root = _parse(
        """
        <kml>
          <Document>
            <Schema>
              <SimpleField name="n" type="int" />
            </Schema>
            <Placemark>
              <ExtendedData>
                <SchemaData>
                  <SimpleData name="n">4</SimpleData>
                </SchemaData>
              </ExtendedData>
              <Point><coordinates>-113.0,36.0,0</coordinates></Point>
            </Placemark>
          </Document>
        </kml>
        """
    )
    placemark = m.get1(root, "Placemark")
    actual = m.build_feature(placemark)
    assert actual["properties"]["n"] == 4

    # section: builds geometrycollection for multiple geometries
    root = _parse(
        """
        <Placemark>
          <Point><coordinates>-113.0,36.0,0</coordinates></Point>
          <LineString><coordinates>-113.0,36.0,0 -114.0,37.0,0</coordinates></LineString>
        </Placemark>
        """
    )
    actual = m.build_feature(root.documentElement)
    assert actual is not None
    assert actual["geometry"]["type"] == "GeometryCollection"
    assert len(actual["geometry"]["geometries"]) == 2

    # section: flattens one track time list into coordinate properties
    root = _parse(
        """
        <Placemark xmlns:gx="http://www.google.com/kml/ext/2.2">
          <gx:Track>
            <when>2020-01-01T00:00:00Z</when>
            <when>2020-01-01T00:01:00Z</when>
            <gx:coord>-113.0 36.0 0</gx:coord>
            <gx:coord>-113.1 36.1 1</gx:coord>
          </gx:Track>
        </Placemark>
        """
    )
    actual = m.build_feature(root.documentElement)
    assert actual is not None
    assert actual["properties"]["coordinateProperties"] == {
        "times": ["2020-01-01T00:00:00Z", "2020-01-01T00:01:00Z"]
    }

    # section: preserves one times list per track when multiple tracks are present
    root = _parse(
        """
        <Placemark xmlns:gx="http://www.google.com/kml/ext/2.2">
          <gx:MultiTrack>
            <gx:Track>
              <when>2020-01-01T00:00:00Z</when>
              <when>2020-01-01T00:01:00Z</when>
              <gx:coord>-113.0 36.0 0</gx:coord>
              <gx:coord>-113.1 36.1 1</gx:coord>
            </gx:Track>
            <gx:Track>
              <when>2020-01-02T00:00:00Z</when>
              <when>2020-01-02T00:01:00Z</when>
              <gx:coord>-114.0 37.0 0</gx:coord>
              <gx:coord>-114.1 37.1 1</gx:coord>
            </gx:Track>
          </gx:MultiTrack>
        </Placemark>
        """
    )
    actual = m.build_feature(root.documentElement)
    assert actual is not None
    assert actual["geometry"]["type"] == "GeometryCollection"
    assert [g["type"] for g in actual["geometry"]["geometries"]] == [
        "LineString",
        "LineString",
    ]
    assert actual["properties"]["coordinateProperties"] == {
        "times": [
            ["2020-01-01T00:00:00Z", "2020-01-01T00:01:00Z"],
            ["2020-01-02T00:00:00Z", "2020-01-02T00:01:00Z"],
        ]
    }


def test_build_ground_overlay():
    # section: builds polygon from latlonbox with bbox
    root = _parse(
        """
        <GroundOverlay id="go1">
          <name>Overlay</name>
          <Icon><href>https://example.com/overlay.png</href></Icon>
          <LatLonBox>
            <north>1</north>
            <south>-1</south>
            <east>1</east>
            <west>-1</west>
          </LatLonBox>
        </GroundOverlay>
        """
    )
    actual = m.build_ground_overlay(root.documentElement)
    assert actual is not None
    assert actual["id"] == "go1"
    assert actual["bbox"] == [-1.0, -1.0, 1.0, 1.0]
    assert actual["properties"]["@geometry-type"] == "groundoverlay"
    assert actual["properties"]["name"] == "Overlay"
    assert actual["properties"]["iconUrl"] == "https://example.com/overlay.png"
    assert actual["geometry"] == {
        "type": "Polygon",
        "coordinates": [
            [
                [-1.0, 1.0],
                [1.0, 1.0],
                [1.0, -1.0],
                [-1.0, -1.0],
                [-1.0, 1.0],
            ]
        ],
    }

    # section: rotates latlonbox coordinates
    root = _parse(
        """
        <GroundOverlay>
          <LatLonBox>
            <north>1</north>
            <south>-1</south>
            <east>1</east>
            <west>-1</west>
            <rotation>90</rotation>
          </LatLonBox>
        </GroundOverlay>
        """
    )
    actual = m.build_ground_overlay(root.documentElement)
    expect = [
        [-1.0, -1.0],
        [-1.0, 1.0],
        [1.0, 1.0],
        [1.0, -1.0],
        [-1.0, -1.0],
    ]
    for position, expect_position in zip(actual["geometry"]["coordinates"][0], expect):
        assert position == pytest.approx(expect_position)

    # section: builds polygon from gx latlonquad
    root = _parse(
        """
        <GroundOverlay xmlns:gx="http://www.google.com/kml/ext/2.2">
          <gx:LatLonQuad>
            <coordinates>0,0 1,0 1,1 0,1</coordinates>
          </gx:LatLonQuad>
        </GroundOverlay>
        """
    )
    actual = m.build_ground_overlay(root.documentElement)
    assert actual["geometry"] == {
        "type": "Polygon",
        "coordinates": [
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [1.0, 1.0],
                [0.0, 1.0],
                [0.0, 0.0],
            ]
        ],
    }

    # section: keeps null geometry by default and skips it on request
    root = _parse("<GroundOverlay><name>Boxless</name></GroundOverlay>")
    actual = m.build_ground_overlay(root.documentElement)
    assert actual is not None
    assert actual["geometry"] is None
    assert m.build_ground_overlay(root.documentElement, skip_null_geometry=True) is None


def test_build_network_link():
    # section: builds feature with link fields region box and lod
    root = _parse(
        """
        <NetworkLink id="nl1">
          <name>Remote</name>
          <refreshVisibility>0</refreshVisibility>
          <flyToView>1</flyToView>
          <Link>
            <href>https://example.com/remote.kml</href>
            <refreshMode>onInterval</refreshMode>
            <refreshInterval>30</refreshInterval>
          </Link>
          <Region>
            <LatLonAltBox>
              <north>2</north>
              <south>0</south>
              <east>2</east>
              <west>0</west>
            </LatLonAltBox>
            <Lod>
              <minLodPixels>128</minLodPixels>
            </Lod>
          </Region>
        </NetworkLink>
        """
    )
    actual = m.build_network_link(root.documentElement)
    assert actual is not None
    assert actual["id"] == "nl1"
    assert actual["bbox"] == [0.0, 0.0, 2.0, 2.0]
    assert actual["properties"]["@geometry-type"] == "networklink"
    assert actual["properties"]["name"] == "Remote"
    assert actual["properties"]["refreshVisibility"] == "0"
    assert actual["properties"]["flyToView"] == "1"
    assert actual["properties"]["href"] == "https://example.com/remote.kml"
    assert actual["properties"]["refreshMode"] == "onInterval"
    assert actual["properties"]["refreshInterval"] == "30"
    assert actual["properties"]["lod"] == [128.0, -1, None, None]
    assert actual["geometry"]["type"] == "Polygon"

    # section: keeps null geometry by default and skips it on request
    root = _parse(
        """
        <NetworkLink>
          <Link><href>https://example.com/remote.kml</href></Link>
        </NetworkLink>
        """
    )
    actual = m.build_network_link(root.documentElement)
    assert actual is not None
    assert actual["geometry"] is None
    assert actual["properties"]["href"] == "https://example.com/remote.kml"
    assert m.build_network_link(root.documentElement, skip_null_geometry=True) is None


def test_build_feature_collection():
    # section: includes placemarks ground overlays and network links
    root = _parse(
        """
        <Folder>
          <Placemark>
            <name>Point A</name>
            <Point><coordinates>-113.0,36.0,0</coordinates></Point>
          </Placemark>
          <GroundOverlay>
            <LatLonBox>
              <north>1</north><south>-1</south><east>1</east><west>-1</west>
            </LatLonBox>
          </GroundOverlay>
          <NetworkLink>
            <Link><href>https://example.com/remote.kml</href></Link>
          </NetworkLink>
        </Folder>
        """
    )
    actual = m.build_feature_collection(root.documentElement, name="layer-a")
    assert actual["type"] == "FeatureCollection"
    assert actual["name"] == "layer-a"
    assert len(actual["features"]) == 3

    # section: keeps placemarks without geometry by default
    root = _parse(
        """
        <Folder>
          <Placemark><name>Empty</name></Placemark>
          <Placemark>
            <name>Point A</name>
            <Point><coordinates>-113.0,36.0,0</coordinates></Point>
          </Placemark>
        </Folder>
        """
    )
    actual = m.build_feature_collection(root.documentElement)
    assert len(actual["features"]) == 2
    assert actual["features"][0]["geometry"] is None

    # section: skips null geometry features when requested
    actual = m.build_feature_collection(root.documentElement, skip_null_geometry=True)
    assert len(actual["features"]) == 1
    assert actual["features"][0]["properties"]["name"] == "Point A"


def test_build_feature_tree():
    # section: preserves nested folder structure with metadata
    root = _parse(
        """
        <kml>
          <Document>
            <Folder>
              <name>Outer</name>
              <description>Outer folder</description>
              <Placemark>
                <name>P1</name>
                <Point><coordinates>-113.0,36.0,0</coordinates></Point>
              </Placemark>
              <Folder>
                <name>Inner</name>
                <Placemark>
                  <name>P2</name>
                  <Point><coordinates>-114.0,37.0,0</coordinates></Point>
                </Placemark>
              </Folder>
            </Folder>
            <Placemark>
              <name>P0</name>
              <Point><coordinates>-115.0,38.0,0</coordinates></Point>
            </Placemark>
          </Document>
        </kml>
        """
    )
    actual = m.build_feature_tree(root)
    assert actual["type"] == "root"
    assert len(actual["children"]) == 2

    outer, p0 = actual["children"]
    assert outer["type"] == "folder"
    assert outer["meta"] == {"name": "Outer", "description": "Outer folder"}
    assert p0["type"] == "Feature"
    assert p0["properties"]["name"] == "P0"

    p1, inner = outer["children"]
    assert p1["properties"]["name"] == "P1"
    assert inner["type"] == "folder"
    assert inner["meta"] == {"name": "Inner"}
    assert inner["children"][0]["properties"]["name"] == "P2"

    # section: skips null geometry features when requested
    root = _parse(
        """
        <kml>
          <Document>
            <Folder>
              <name>Outer</name>
              <Placemark><name>Empty</name></Placemark>
            </Folder>
          </Document>
        </kml>
        """
    )
    actual = m.build_feature_tree(root, skip_null_geometry=True)
    assert actual["children"][0]["children"] == []


def test_build_layers():
    # section: builds one layer per folder with geodata
    root = _read_kml(DATA_DIR / "two_layers" / "two_layers.kml")
    actual = m.build_layers(root)
    assert [layer["name"] for layer in actual] == ["%Bingo", "#Bingo"]

    # section: raw layer names can be sanitized and disambiguated for filenames
    stems = m.disambiguate(m.to_filename(layer["name"]) for layer in actual)
    assert stems == ["Bingo", "Bingo1"]

    # section: falls back to root when no folders exist
    root = _parse(
        """
        <kml>
          <Document>
            <name>root-layer</name>
            <Placemark>
              <Point><coordinates>-113.0,36.0,0</coordinates></Point>
            </Placemark>
          </Document>
        </kml>
        """
    )
    actual = m.build_layers(root)
    assert len(actual) == 1
    assert actual[0]["name"] == "root-layer"

    # section: can skip disambiguation
    root = _parse(
        """
        <Document>
          <Folder>
            <name>A</name>
            <Placemark><Point><coordinates>-1,1,0</coordinates></Point></Placemark>
          </Folder>
          <Folder>
            <name>A</name>
            <Placemark><Point><coordinates>-2,2,0</coordinates></Point></Placemark>
          </Folder>
        </Document>
        """
    )
    actual = m.build_layers(root, disambiguate_names=False)
    assert [layer["name"] for layer in actual] == ["A", "A"]


def test_convert():
    kml_path = DATA_DIR / "two_layers" / "two_layers.kml"

    # section: converts from path into one named feature collection
    actual = m.convert(kml_path, feature_collection_name="main")
    assert "style" not in actual
    layers = actual["feature_collections"]
    assert len(layers) == 1
    assert layers[0]["type"] == "FeatureCollection"
    assert layers[0]["name"] == "main"

    # section: returns separate folder layers with raw folder names
    actual = m.convert(kml_path, separate_folders=True)
    layers = actual["feature_collections"]
    assert [layer["name"] for layer in layers] == ["%Bingo", "#Bingo"]

    # section: raw layer names can later be sanitized and disambiguated for filenames
    stems = m.disambiguate(m.to_filename(layer["name"]) for layer in layers)
    assert stems == ["Bingo", "Bingo1"]

    # section: includes svg style dict when requested
    actual = m.convert(kml_path, style_type="svg", separate_folders=True)
    assert isinstance(actual["style"], dict)
    layers = actual["feature_collections"]
    assert [layer["name"] for layer in layers] == ["%Bingo", "#Bingo"]

    # section: includes leaflet style dict when requested
    actual = m.convert(kml_path, style_type="leaflet")
    assert isinstance(actual["style"], dict)
    assert len(actual["feature_collections"]) == 1

    # section: accepts text and binary file-like buffers
    with open(kml_path, encoding="utf-8", errors="ignore") as src:
        text_buffer = io.StringIO(src.read())

    actual = m.convert(text_buffer, feature_collection_name="main")
    layers = actual["feature_collections"]
    assert len(layers) == 1
    assert layers[0]["type"] == "FeatureCollection"
    assert layers[0]["name"] == "main"

    with open(kml_path, "rb") as src:
        binary_buffer = io.BytesIO(src.read())

    actual = m.convert(binary_buffer, separate_folders=True)
    layers = actual["feature_collections"]
    assert [layer["name"] for layer in layers] == ["%Bingo", "#Bingo"]

    # section: can skip features without geometry
    kml_str = """
        <kml>
          <Document>
            <Placemark><name>Empty</name></Placemark>
            <Placemark>
              <name>Point A</name>
              <Point><coordinates>-113.0,36.0,0</coordinates></Point>
            </Placemark>
          </Document>
        </kml>
        """
    actual = m.convert(io.StringIO(kml_str))
    assert len(actual["feature_collections"][0]["features"]) == 2

    actual = m.convert(io.StringIO(kml_str), skip_null_geometry=True)
    assert len(actual["feature_collections"][0]["features"]) == 1

    # section: rejects unsupported style type
    with pytest.raises(ValueError, match="style type must be one of"):
        m.convert(kml_path, style_type="not-a-style")
