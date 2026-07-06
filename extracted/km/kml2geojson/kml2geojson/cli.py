import json
import pathlib as pl

import click

import kml2geojson.main as m


@click.command(short_help="Convert KML to GeoJSON")
@click.argument("kml_path_or_buffer", type=click.Path(exists=True))
@click.argument("output_dir")
@click.option("-fcn", "--feature-collection-name", default="main")
@click.option("-st", "--style-type", type=click.Choice(m.STYLE_TYPES), default=None)
@click.option("-sf", "--style-filename", default="style.json")
@click.option("-smk", "--style-map-key", default="normal")
@click.option("-f", "--separate-folders", is_flag=True, default=False)
@click.option("-sn", "--skip-null-geometry", is_flag=True, default=False)
def k2g(
    kml_path_or_buffer,
    output_dir,
    feature_collection_name,
    style_type,
    style_filename,
    style_map_key,
    separate_folders,
    skip_null_geometry,
):
    """
    Given a path to a KML file, convert it to a GeoJSON FeatureCollection
    with name = ``--feature_collection_name`` (which defaults to 'main') and
    save the GeoJSON to a '.geojson' file in the given output directory.

    If ``--separate_folders``, then create several GeoJSON files, one for each
    folder in the KML file that contains geodata or that has a descendant node
    that contains geodata. Warning: this can produce GeoJSON files with the
    same geodata in case the KML file has nested folders with geodata.

    If ``--style_type`` is specified, then also build a JSON style file of the
    given style type and save it to the output directory under the file name
    given by ``--style_filename`` which defaults to "style.json".
    KML StyleMaps are resolved to the style referenced by their pair with key
    ``--style_map_key``, which defaults to "normal".

    If ``--skip_null_geometry``, then omit GeoJSON Features without geometry.
    """
    result = m.convert(
        kml_path_or_buffer,
        style_type=style_type,
        separate_folders=separate_folders,
        feature_collection_name=feature_collection_name,
        skip_null_geometry=skip_null_geometry,
        style_map_key=style_map_key,
    )

    output_dir = pl.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir = output_dir.resolve()

    if "style" in result:
        with (output_dir / style_filename).open("w") as tgt:
            json.dump(result["style"], tgt)

    layers = result["feature_collections"]

    stems = m.disambiguate(m.to_filename(layer["name"]) for layer in layers)
    filenames = [f"{stem}.geojson" for stem in stems]

    for layer, filename in zip(layers, filenames):
        with (output_dir / filename).open("w") as tgt:
            json.dump(layer, tgt)
