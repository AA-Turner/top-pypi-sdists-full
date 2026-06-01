import logging
import os
from pathlib import Path
from uuid import UUID

import yaml

from picsellia.exceptions import (
    FileNotFoundException,
    ResourceConflictError,
    ResourceNotFoundError,
    UnparsableAnnotationFileException,
)
from picsellia.sdk.asset import Asset, MultiAsset
from picsellia.sdk.label import Label
from picsellia.types.enums import InferenceType

logger = logging.getLogger("picsellia")


def read_filenames_from_file_paths(
    file_paths: list[str | Path],
) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for file_path in file_paths:
        if isinstance(file_path, str):
            file_path = Path(file_path)

        if not os.path.isfile(file_path) and file_path.suffix != "txt":
            raise UnparsableAnnotationFileException(
                f"{file_path} is not a yolo annotation file."
            )

        filename = Path(file_path).name[:-4]  # remove extension
        files[filename] = file_path

    return files


def parse_configuration_file(configuration_yaml_path: str | Path) -> list[str]:
    try:
        with open(configuration_yaml_path) as yaml_file:
            configuration_yolo = yaml.safe_load(yaml_file)

        nc = configuration_yolo["nc"]
        names = configuration_yolo["names"]

        if not isinstance(nc, int) or not isinstance(names, list):
            raise TypeError(
                "Parameters 'nc' should be an integer and 'names' a list of string"
            )

        if nc != len(names):
            raise ValueError(
                f"Parameter 'nc' is {nc} but there are {len(names)} classes in 'names'"
            )
    except FileNotFoundError:
        raise FileNotFoundException(f"{configuration_yaml_path} not found")
    except KeyError as e:
        raise UnparsableAnnotationFileException(
            f"Could not find key `{e}` inside yolo configuration file {configuration_yaml_path}"
        )

    return names


def match_assets_with_filenames(files: dict[str, Path], multi_assets: MultiAsset):
    assets: dict[str, Asset] = {}
    for asset in multi_assets:
        filename = asset.filename[:-4]
        if filename not in files:
            # Retrieved an asset that we were not looking for
            continue

        if filename in assets:  # pragma: no cover
            raise ResourceConflictError(
                f"A filename was retrieved twice in your dataset. Please remove one of it. Prefix of filename is {filename}"
            )

        assets[filename] = asset

    return assets


def assert_coherence_files_assets(
    files: dict[str, Path], assets: dict[str, Asset], fail_on_asset_not_found: bool
):
    if fail_on_asset_not_found and len(assets) != len(files):
        assets_not_found = set(files.keys()).difference(set(assets.keys()))
        raise ResourceNotFoundError(
            f"Filenames {assets_not_found} were not found in your dataset"
        )


def parse_files_to_annotations(
    inference_type: InferenceType,
    files: dict[str, Path],
    assets: dict[str, Asset],
    labels: list[Label],
) -> list[dict]:
    annotations: list[dict] = []
    for filename, asset in assets.items():
        raw_annotations: list[list[str]] = _open_yolo_file(files[filename])
        if len(raw_annotations) == 0:
            logger.info(f"No annotation found in file {filename}")
            continue

        if len(raw_annotations) > 1 and inference_type == InferenceType.CLASSIFICATION:
            raise UnparsableAnnotationFileException(
                f"Could not parse yolo file {filename} : only one classification can be given by file"
            )

        try:
            annotations.append(
                _parse_file_to_annotation(
                    asset, raw_annotations, inference_type, labels
                )
            )
        except Exception as e:
            raise UnparsableAnnotationFileException(
                f"Could not parse yolo annotation file {filename}"
            ) from e

    return annotations


def _open_yolo_file(file_path: Path) -> list[list[str]]:
    raw_annotations = []
    with open(file_path) as txt_file:
        for content in txt_file.readlines():
            if content:
                raw_annotations.append(content.strip().split(" "))

    return raw_annotations


def _parse_file_to_annotation(
    asset: Asset,
    raw_annotations: list,
    inference_type: InferenceType,
    labels: list[Label],
) -> dict:
    rectangles = []
    polygons = []
    classifications = []
    for raw_shape in raw_annotations:
        if len(raw_shape) < 1:  # pragma: no cover
            continue

        label_id = _parse_raw_yolo_annotation_label(raw_shape, labels)

        if inference_type == InferenceType.OBJECT_DETECTION:
            rectangles.append(
                _convert_raw_yolo_annotation_to_rectangle(
                    raw_shape, label_id, asset.width, asset.height
                )
            )
        elif inference_type == InferenceType.SEGMENTATION:
            polygons.append(
                _convert_raw_yolo_annotation_to_polygon(
                    raw_shape, label_id, asset.width, asset.height
                )
            )
        elif inference_type == InferenceType.CLASSIFICATION:
            classifications.append(
                _convert_raw_yolo_annotation_to_classification(label_id)
            )
        else:  # pragma: no cover
            raise TypeError(f"{inference_type} is not supported yet")

    return {
        "asset_id": asset.id,
        "rectangles": rectangles,
        "polygons": polygons,
        "classifications": classifications,
    }


def _parse_raw_yolo_annotation_label(
    raw_shape: list[str],
    labels: list[Label],
):
    label_offset = int(raw_shape[0])
    if label_offset > len(labels):
        raise UnparsableAnnotationFileException(
            f"This annotation has label {label_offset} but it is not defined. "
            f"Check your yolo configuration file"
        )
    return labels[label_offset].id


def _convert_raw_yolo_annotation_to_polygon(
    raw_shape: list[str],
    label_id: UUID,
    asset_width: int,
    asset_height: int,
) -> dict:
    shape_values = _convert_raw_shape_to_shape_values(raw_shape[1:])
    if len(shape_values) % 2 != 0 or len(shape_values) < 6:
        raise UnparsableAnnotationFileException(
            f"This polygon cannot be parsed: {shape_values}. It needs at least 3 points to create a polygon."
        )
    coords = [
        [
            int(shape_values[k] * asset_width),
            int(shape_values[k + 1] * asset_height),
        ]
        for k in range(0, len(shape_values), 2)
    ]
    return {"polygon": coords, "label_id": label_id}


def _convert_raw_yolo_annotation_to_rectangle(
    raw_shape: list[str],
    label_id: UUID,
    asset_width: int,
    asset_height: int,
) -> dict:
    shape_values = _convert_raw_shape_to_shape_values(raw_shape[1:])
    if len(shape_values) != 4:
        raise UnparsableAnnotationFileException(
            f"This rectangle cannot be parsed: {raw_shape}. It needs to be formatted as label_id, x, y, w, h"
        )
    # Yolo format give the shape at its center
    # Also, precision can lead to a negative number, which backend won't allow
    w = shape_values[2] * asset_width
    h = shape_values[3] * asset_height
    x = max(0.0, shape_values[0] * asset_width - w / 2)
    y = max(0.0, shape_values[1] * asset_height - h / 2)

    return {
        "x": int(x),
        "y": int(y),
        "w": int(w),
        "h": int(h),
        "label_id": label_id,
    }


def _convert_raw_yolo_annotation_to_classification(label_id: UUID) -> dict:
    return {"label_id": label_id}


def _convert_raw_shape_to_shape_values(raw_shape: list[str]):
    shape_values = []
    for value in raw_shape:
        if value == "":
            continue

        value = float(value)

        if 0 > value or value > 1:
            raise ValueError(f"A value of {raw_shape} is not in [0, 1]")

        shape_values.append(value)

    return shape_values
