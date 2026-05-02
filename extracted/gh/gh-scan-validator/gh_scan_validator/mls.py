"""MLS scan checker and density grid estimator
The density grid cell means the minimum X and Y coordinates of a point
For example considering 1m grid cell (1.2, 2.9) would be in cell (1,2)
"""
import argparse
import csv
import json
import logging
import shutil
import traceback
from configparser import ConfigParser
from multiprocessing import Pool
from os import cpu_count
from pathlib import Path
from typing import Dict, List, Tuple, Union

import coloredlogs
import geopandas as gpd
import laspy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numba import jit, prange
from scipy import sparse
from tse_location.las_reader import download_blob, get_container_client

# density grid cell size in meters
GRID_CELL_SIZE_M = 1


def error(msg: str):
    logging.error(msg)
    raise RuntimeError(msg)


@jit(nopython=True, fastmath=True, parallel=False, cache=True)
def fill_grid(grid, points, x_min, y_min):
    grid_div_const = 1 / GRID_CELL_SIZE_M
    for i in prange(len(points)):
        p = points[i]
        grid[int((p[0] - x_min) * grid_div_const), int((p[1] - y_min) * grid_div_const)] += 1


def get_header(csv_path: Path) -> Tuple[List[str], List[str]]:
    with open(csv_path) as in_fp:
        reader = csv.reader(in_fp)
        column_count = len(next(reader))

    header = [
        "timestamp",
        "filename",
        "origin_x",
        "origin_y",
        "origin_z",
        "direction_x",
        "direction_y",
        "direction_z",
        "up_x",
        "up_y",
        "up_z",
        "roll",
        "pitch",
        "yaw",
    ]
    float_fields = [
        "origin_x",
        "origin_y",
        "origin_z",
        "direction_x",
        "direction_y",
        "direction_z",
        "up_x",
        "up_y",
        "up_z",
        "roll",
        "pitch",
        "yaw",
    ]

    if column_count == len(header) + 3:
        header = header + ["omega", "phi", "kappa"]
        float_fields = float_fields + ["omega", "phi", "kappa"]
    elif column_count != len(header):
        error(f"Unknown CSV header format! Expected order: {header}")

    return header, float_fields


def load_camera_orbit_csv(csv_path: Path) -> pd.DataFrame:
    if csv_path.is_file():
        header, float_fields = get_header(csv_path)
        df = pd.read_csv(
            csv_path,
            header=0,
            names=header,
        )

        # convert to float:
        df[float_fields] = df[float_fields].apply(pd.to_numeric)

        return df
    else:
        scan_root = csv_path.parent.parent.parent
        camera_name = csv_path.parent.name
        common_camera_csv_path = scan_root / f"{camera_name}.csv"
        if not common_camera_csv_path.is_file():
            error(
                f"Cannot find orbit CSV for camera: {csv_path} and cannot locate common CSV either: {common_camera_csv_path}"
            )

        header, float_fields = get_header(csv_path)
        df = pd.read_csv(
            common_camera_csv_path,
            header=0,
            names=header,
        )

        images_in_path = [i.name for i in csv_path.parent.glob("*.jpg")]
        df = df[df["filename"].isin(images_in_path)]

        # convert to float:
        df[float_fields] = df[float_fields].apply(pd.to_numeric)

        return df


def load_scan_grid_and_meta(scan_path: Path) -> Tuple[sparse.csr_matrix, Dict]:
    density_path = scan_path / "05_DENSITY"
    npz = density_path / "density_grid.npz"
    meta_path = density_path / "density_grid.json"

    return sparse.load_npz(npz), json.loads(meta_path.read_text())


def create_density_grid_for_laz(laz_path: Path, density_path: Path) -> None:
    logging.info(f"running density grid on {laz_path}")

    inFile = laspy.file.File(str(laz_path), mode="r")

    coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

    # add density grid logic here
    meta = {
        "laz_name": laz_path.name,
        "cell_size": GRID_CELL_SIZE_M,
        "x_min": int(np.min(coords[:, 0])),
        "x_max": int(np.max(coords[:, 0])) + 1,
        "y_min": int(np.min(coords[:, 1])),
        "y_max": int(np.max(coords[:, 1])) + 1,
    }
    x_range = meta["x_max"] - meta["x_min"]
    y_range = meta["y_max"] - meta["y_min"]

    grid = np.zeros((int(x_range / GRID_CELL_SIZE_M), int(y_range / GRID_CELL_SIZE_M)), dtype=np.int32)
    fill_grid(grid, coords, meta["x_min"], meta["y_min"])

    # save density grid as pkl and add metadata
    np.save(density_path, grid)
    meta_file = density_path.parent / density_path.name.replace(".npy", ".json")
    meta_file.write_text(json.dumps(meta, indent=4))

    logging.info(f"Loaded {laz_path} - {len(coords)} points")


def density_grid(paths: List[Path], density_path: Path) -> None:
    cpus = cpu_count() - 1
    if cpus == 0:
        cpus = 1
    logging.info(f"Loading {len(paths)} las files with {cpus} cpu cores.")
    with Pool(cpus) as p:
        p.starmap(create_density_grid_for_laz, [(p, density_path / p.name.replace(".laz", ".npy")) for p in paths])


def merge_tile_densities(density_path: Path, tile_densities: Path) -> Tuple[np.array, Dict]:
    grids = {}
    metas = {}
    for d in tile_densities.glob("*.npy"):
        laz_name = d.name.replace(".npy", "")
        grids[laz_name] = np.load(d)
        metas[laz_name] = json.loads((d.parent / f"{laz_name}.json").read_text())

    scan_grid_meta = {
        "cell_size": GRID_CELL_SIZE_M,
        "x_min": int(min([v["x_min"] for v in metas.values()])),
        "x_max": int(max([v["x_max"] for v in metas.values()])),
        "y_min": int(min([v["y_min"] for v in metas.values()])),
        "y_max": int(max([v["y_max"] for v in metas.values()])),
    }
    scan_grid = np.zeros(
        (
            int((scan_grid_meta["x_max"] - scan_grid_meta["x_min"]) / GRID_CELL_SIZE_M),
            int((scan_grid_meta["y_max"] - scan_grid_meta["y_min"]) / GRID_CELL_SIZE_M),
        ),
        dtype=np.int32,
    )
    for i, grid in grids.items():
        meta = metas[i]
        x_size, y_size = grid.shape
        x_offset = int((meta["x_min"] - scan_grid_meta["x_min"]) / GRID_CELL_SIZE_M)
        y_offset = int((meta["y_min"] - scan_grid_meta["y_min"]) / GRID_CELL_SIZE_M)
        scan_grid[x_offset : x_offset + x_size, y_offset : y_offset + y_size] = grid

    # save grid
    npz = density_path / "density_grid.npz"
    sparse.save_npz(npz, sparse.csr_matrix(scan_grid))
    (density_path / "density_grid.json").write_text(json.dumps(scan_grid_meta, indent=4))

    return scan_grid, scan_grid_meta


def get_tile_field(laz_gdf):
    tile_field = None
    if "tilename" in laz_gdf:
        tile_field = "tilename"
    elif "layer" in laz_gdf:
        tile_field = "layer"
    else:
        error("Unkown shapefile column, it needs to be either 'tilename' or 'layer'")
    return tile_field


class Validator(object):
    def __init__(self, scan_path: Path, scan_name: str = None) -> None:
        if scan_name is None:
            scan_name = scan_path.name
        self.scan_name = scan_name
        self.scan_path = scan_path

    def validate_folder_structure(self):
        if not self.directory_exists(self.scan_path):
            error(f"Scan path {self.scan_path} does not exist")

        folders = ["02_CAMERA", "02_CAMERA/Images", "03_LAZ"]

        for folder in folders:
            folder = self.scan_path / folder
            if not self.directory_exists(folder):
                error(f"Folder does not exist: {folder}")
        logging.info("Root folder structure ok")

    def validate_geodata(self):
        # load shapefile to geodataframe
        laz_path = self.scan_path / "03_LAZ"

        shape_folders = self.get_shape_folders(laz_path)

        if not len(shape_folders) == 1:
            error(f"Could not locate shapefile folder in 03_LAZ path: {laz_path}")

        shape = shape_folders[0]

        shape_folder_base_name, recording_date = shape.name.rsplit("_", 1)

        if self.scan_name not in shape.name or self.scan_name != shape_folder_base_name or len(recording_date) != 8:
            error(
                f"Invalid shapefile folder name: {shape.name} shapefile folder should be named: {self.scan_name}_YYYYMMDD where YYYYMMDD is the recording date"
            )

        logging.info(f"ESRI shapefile folder found: {shape}")

        try:
            laz_gdf = self.load_shape_file(shape)
            logging.info("Read shapefile successful")
        except:
            error("Could not read shapefile")

        self.check_tiles(laz_path, laz_gdf)
        logging.info("Found all laz files from shapefile")

    def validate_image_folder(self):
        # check checksum if present
        logging.warning("Checksum is not yet validated")

        images_path = self.scan_path / "02_CAMERA" / "Images"

        cameras = []
        topodot_cal_files = self.get_topodot_files(images_path)
        for topo_cal_file in topodot_cal_files:
            calib_name = topo_cal_file.name.replace(".TopoDOT.cal", "")
            cameras.append(calib_name.split("-")[-1])
            logging.info(f"Found camera with name: {cameras[-1]}")

        logging.info("Validating calibration files")
        for topo_cal_file in topodot_cal_files:
            config = ConfigParser()
            config.optionxform = str
            config.read(topo_cal_file)
            calibration = dict(config["Calibration"])
            for field in ["k1", "k2", "k3", "k4", "P1", "P2"]:
                if float(calibration[field]) != 0.0:
                    error(
                        f"Invalid calibration file field: {field}, should be 0 instead of {calibration[field]} in {topo_cal_file}, image re-export is needed"
                    )
        logging.info("Validated calibration files")

        self.validate_images(images_path, cameras)
        logging.info("Images validated")

    def validate_images(self, images_path: Union[str, Path], cameras: List):
        raise NotImplementedError("This is an abstract class, please not use directly")

    def get_topodot_files(self, images_path: Union[str, Path], download: bool = False):
        raise NotImplementedError("This is an abstract class, please not use directly")

    def validate(self):
        if not shutil.which("laszip"):
            logging.warning("laszip executable does not exist, processing might run into issues")

        self.validate_folder_structure()
        self.validate_geodata()
        self.validate_image_folder()
        logging.info("Check completed, all checks passed")

    def directory_exists(self, path: Union[Path, str]):
        raise NotImplementedError("This is an abstract class, please not use directly")

    def get_shape_folders(self, laz_path: Union[Path, str]):
        raise NotImplementedError("This is an abstract class, please not use directly")

    def load_shape_file(self, shape_folder: Union[str, Path]):
        shp = [p for p in shape_folder.glob("*.shp") if p.name[0] != "."][0]
        laz_gdf = gpd.read_file(shp)
        return laz_gdf

    def check_tiles(self, laz_path: Union[str, Path], laz_gdf: gpd.GeoDataFrame):
        raise NotImplementedError("This is an abstract class, please not use directly")


class LocalValidator(Validator):
    def directory_exists(self, path: Union[str, Path]):
        return path.is_dir()

    def get_shape_folders(self, laz_path: Union[str, Path]):
        return [
            i
            for i in laz_path.glob("*")
            if i.is_dir() and self.scan_name in i.name and len(list(i.glob("*.shp"))) >= 1 and i.name[0] != "."
        ]

    def check_tiles(self, laz_path: Union[str, Path], laz_gdf: gpd.GeoDataFrame):
        for tile in laz_gdf[get_tile_field(laz_gdf)]:
            laz = laz_path / f"{tile}.laz"
            if not laz.is_file():
                error(f"laz file cannot be found: {laz}")

    def get_topodot_files(self, images_path: List, download: bool = False):
        assert not download, "Download keyword is not supported in the Local Validator"
        topodot_cal_files = [c for c in images_path.glob("*.TopoDOT.cal") if c.name[0] != "."]
        if len(topodot_cal_files) == 0:
            error(f"The camera calibration topodot files are not present in: {images_path}")
        return topodot_cal_files

    def validate_images(self, images_path: Union[str, Path], cameras: List):
        recordings = [c for c in images_path.glob("Record*") if c.name[0] != "." and c.is_dir()]
        if len(recordings) == 0:
            error(f"The camera Record** folders are not present in: {images_path}")
        csvs = []
        for rec in recordings:
            for camera in cameras:
                camdir = rec / camera
                if not camdir.is_dir():
                    error(f"Cannot find camera directory: {camdir}")

                orbit_paths = [i for i in list(camdir.glob("*.orbit.csv")) if i.name[0] != "."]
                if len(orbit_paths) != 1:
                    logging.warning(f"Found {len(orbit_paths)} orbit CSV files, we need exactly one")

                csv_path = orbit_paths[0]

                if not csv_path.is_file():
                    logging.info(f"Cannot find orbit CSV for camera: {csv_path}, trying with shared CSV")

                df = load_camera_orbit_csv(csv_path)
                count = 0
                for img in df.itertuples(index=False, name="Image"):
                    count += 1
                    if not (camdir / str(img.filename)).is_file():
                        error(f"Could not find image: {camdir / str(img.filename)}")

                csvs.append((rec.name, camera, csv_path))
                logging.info(f"Validated {count} images in {camdir}")
        return csvs


class BlobValidator(Validator):
    def __init__(self, scan_path: Path, scan_name: str = None, cache_folder=Path("/cache/scan_input_validator")):
        super(BlobValidator, self).__init__(scan_path, scan_name=scan_name)
        self.container_client = get_container_client()
        self.cache_folder = cache_folder
        self.cache_folder.mkdir(parents=True)
        self.shape_folder_cached = False
        self.topodot_files_cached = False
        self.orbit_csv_cached = False

    def directory_exists(self, path: Union[Path, str]):
        return len(list(self.container_client.list_blobs(name_starts_with=path))) > 0

    def get_shape_folders(self, laz_path: Union[Path, str]):
        files = self.container_client.list_blobs(name_starts_with=laz_path)

        return [
            Path(i["name"]).parent
            for i in files
            if Path(i["name"]).name.startswith(self.scan_name) and i["name"].endswith(".shp")
        ]

    def load_shape_file(self, shape_folder: Union[Path, str]):
        files = self.container_client.list_blobs(name_starts_with=shape_folder)
        if not self.shape_folder_cached:
            for f in files:
                download_blob(f["name"], self.cache_folder / Path(f["name"]).name)

            self.shape_folder_cached = True

        return Validator.load_shape_file(self, self.cache_folder)

    def check_tiles(self, laz_path: Union[str, Path], laz_gdf: gpd.GeoDataFrame):
        files = self.container_client.list_blobs(name_starts_with=laz_path)
        lazes = [f["name"] for f in files if f["name"].endswith(".laz")]
        for tile in laz_gdf[get_tile_field(laz_gdf)]:
            laz = laz_path / f"{tile}.laz"
            if str(laz) not in lazes:
                error(f"laz file cannot be found: {laz}")

    def validate_images(self, images_path: Union[Path, str], cameras: List):
        files = self.container_client.walk_blobs(f"{images_path}/")
        recordings = [f["name"] for f in files if "blob_type" not in f.keys() and "Record" in f["name"]]
        if len(recordings) == 0:
            error(f"The camera Record** folders are not present in: {images_path}")

        csvs = []

        for recording in recordings:
            files = list(self.container_client.list_blobs(name_starts_with=recording))
            blob_csvs = [f["name"] for f in files if f["name"].endswith(".orbit.csv")]
            blob_images = [f["name"] for f in files if f["name"].endswith(".jpg")]
            for blob_csv in blob_csvs:
                camera_name = Path(blob_csv).parent.name

                if camera_name not in cameras:
                    error(f"Cannot find {camera_name} from topodot files")

                local_folder = self.cache_folder / recording / camera_name
                local_folder.mkdir(exist_ok=True, parents=True)
                if not self.orbit_csv_cached:
                    download_blob(blob_csv, local_folder / Path(blob_csv).name)
                df = load_camera_orbit_csv(local_folder / Path(blob_csv).name)
                count = 0
                for img in df.itertuples(index=False, name="Image"):
                    count += 1
                    if not str(Path(recording) / camera_name / str(img.filename)) in blob_images:
                        error(f"Could not find image: {Path(recording) /camera_name / str(img.filename)}")
                logging.info(f"Validated {count} images in {camera_name}")
                csvs.append((recording, camera_name, local_folder / Path(blob_csv).name))
        self.orbit_csv_cached = True
        return csvs

    def get_topodot_files(self, images_path: Union[str, Path], download=False):
        cal_files = self.container_client.list_blobs(name_starts_with=images_path)

        topodot_cal_files = []
        for cal_file in cal_files:
            if not cal_file["name"].endswith(".TopoDOT.cal"):
                continue
            topodot_cal_files.append(self.cache_folder / Path(cal_file["name"]).name)
            if download and not self.topodot_files_cached:
                download_blob(cal_file["name"], self.cache_folder / Path(cal_file["name"]).name)
        if download:
            self.topodot_files_cached = True

        if len(topodot_cal_files) == 0:
            error(f"The camera calibration topodot files are not present in: {images_path}")

        return topodot_cal_files

    def __del__(self):
        shutil.rmtree(self.cache_folder)


def validate_scan(scan_path: Path, scan_name: str = None, use_blob=False) -> None:
    validator = (
        BlobValidator(scan_path, scan_name=scan_name) if use_blob else LocalValidator(scan_path, scan_name=scan_name)
    )
    validator.validate()
    # del validator  # for calling destructor. WTF Python?
    return validator


def generate_scan_density(scan_path: Path, scan_name: str = None) -> None:
    if not scan_name:
        scan_name = scan_path.name

    laz_path = scan_path / "03_LAZ"
    laz_files = list(laz_path.glob("*.laz"))

    # generate density grid for all tiles
    logging.info("Generating density grid")
    density_path = scan_path / "05_DENSITY"
    density_path.mkdir(exist_ok=True)
    tile_densities = density_path / "tiles"
    tile_densities.mkdir(exist_ok=True)

    density_grid(laz_files, tile_densities)
    logging.info("Density grid created")

    # merge all grids to a big one
    logging.info("Creating merged density grid")
    scan_grid, scan_grid_meta = merge_tile_densities(density_path, tile_densities)
    logging.info(f"Merged grid created and saved: {load_scan_grid_and_meta(scan_path)}")

    # plot density grid
    logging.info("Rendering map plot")
    plt.rcParams["figure.dpi"] = 800
    plt.rcParams["figure.figsize"] = (15, 15)

    plt.imshow(
        scan_grid,
        cmap="jet",
        origin="lower",
        extent=[scan_grid_meta["y_min"], scan_grid_meta["y_max"], scan_grid_meta["x_min"], scan_grid_meta["x_max"]],
    )
    plt.savefig(density_path / "density.png")

    logging.info("Density created")


if __name__ == "__main__":
    coloredlogs.install(level="info")
    logging.getLogger("numba").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser(description="greeHill MLS scan structure validator")
    parser.add_argument("scan_path", help="Path to the scan which has 03_LAZ, 02_CAMERA folders")
    parser.add_argument(
        "--use_blob", action="store_true", help="Switch for using scan validor on a local path or a blob path"
    )

    args = parser.parse_args()

    indata = Path(args.scan_path)

    try:
        validate_scan(indata, use_blob=args.use_blob)
        # generate_scan_density(indata)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(e)
        exit(1)
