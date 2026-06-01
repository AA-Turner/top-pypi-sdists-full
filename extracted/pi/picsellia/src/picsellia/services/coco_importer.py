import logging
from pathlib import Path

from beartype import beartype
from picsellia_annotations.coco import Annotation as COCOAnnotation
from picsellia_annotations.coco import COCOFile, SegmentationRleIn
from picsellia_annotations.exceptions import FileError, ParsingError
from picsellia_annotations.utils import read_coco_file, read_video_coco_file
from picsellia_annotations.video_coco import (
    ExtendedImage,
    VideoAnnotation,
    VideoCOCOFile,
)

from picsellia.decorators import exception_handler
from picsellia.exceptions import (
    FileNotFoundException,
    UnparsableAnnotationFileException,
)
from picsellia.sdk.label import Label
from picsellia.types.enums import InferenceType

logger = logging.getLogger("picsellia")


@exception_handler
@beartype
def parse_coco_file(file_path: Path | str) -> COCOFile:
    try:
        return read_coco_file(file_path=file_path)
    except FileError:
        raise FileNotFoundException(f"{file_path} not found")
    except ParsingError as e:
        raise UnparsableAnnotationFileException(
            f"Could not parse COCO file {file_path} because : {e}"
        )


@exception_handler
@beartype
def parse_coco_video_file(file_path: Path | str) -> VideoCOCOFile:
    try:
        return read_video_coco_file(file_path=file_path)
    except FileError:
        raise FileNotFoundException(f"{file_path} not found")
    except ParsingError as e:
        raise UnparsableAnnotationFileException(
            f"Could not parse COCO VID file {file_path} because : {e}"
        )


@exception_handler
@beartype
def read_annotations(  # noqa: C901
    cocofile_type: InferenceType,
    coco_annotations: list[COCOAnnotation],
    labels: dict[int, Label],
    assets: dict[int, tuple[str, dict | None]],
) -> list[dict]:
    annotations: dict[str, dict] = {}
    for annotation in coco_annotations:
        try:
            label = labels[annotation.category_id]
        except KeyError:  # pragma: no cover
            logger.error(
                f"category_id {annotation.category_id} not found into retrieved labels"
            )
            continue

        try:
            asset_id = assets[annotation.image_id][0]
        except KeyError:
            logger.error(
                f"image_id {annotation.image_id} not found into retrieved assets"
            )
            continue

        if asset_id not in annotations:
            annotations[asset_id] = {
                "rectangles": [],
                "classifications": [],
                "polygons": [],
                "keypoints": [],
                "masks": [],
                "attributes": assets[annotation.image_id][1],
            }
        elif not annotations[asset_id]["attributes"]:
            annotations[asset_id]["attributes"] = assets[annotation.image_id][1]

        if cocofile_type == InferenceType.SEGMENTATION:
            if not annotation.is_rle():
                polygon_coords = annotation.polygon_to_list_coordinates()
            else:
                logger.error(
                    f"annotation_id {annotation.id} is a RLE which is only supported in MASK datasets yet"
                )
                continue

            for polygon_coord in polygon_coords:
                annotations[asset_id]["polygons"].append(
                    {
                        "polygon": polygon_coord,
                        "label_id": label.id,
                        "text": annotation.utf8_string,
                        "attributes": annotation.attributes,
                    }
                )
        elif cocofile_type == InferenceType.MASK:
            if not isinstance(annotation.segmentation, SegmentationRleIn):
                logger.error(
                    f"annotation_id {annotation.id} should be a RLE, the only supported type MASK datasets yet"
                )
                continue

            if not isinstance(annotation.segmentation.counts, str):
                logger.error(
                    f"annotation_id {annotation.id} must be a string representing counts"
                )
                continue

            annotations[asset_id]["masks"].append(
                {
                    "mask": annotation.segmentation.counts,
                    "label_id": label.id,
                    "text": annotation.utf8_string,
                    "attributes": annotation.attributes,
                }
            )
        elif cocofile_type == InferenceType.OBJECT_DETECTION:
            annotations[asset_id]["rectangles"].append(
                {
                    "x": int(annotation.bbox[0]),
                    "y": int(annotation.bbox[1]),
                    "w": int(annotation.bbox[2]),
                    "h": int(annotation.bbox[3]),
                    "label_id": label.id,
                    "text": annotation.utf8_string,
                    "attributes": annotation.attributes,
                }
            )
        elif cocofile_type == InferenceType.CLASSIFICATION:
            annotations[asset_id]["classifications"].append(
                {
                    "label_id": label.id,
                    "text": annotation.utf8_string,
                    "attributes": annotation.attributes,
                }
            )
        elif cocofile_type == InferenceType.KEYPOINT:
            if len(annotation.keypoints) % 3 != 0:
                logging.error(
                    f"Could not parse keypoints of annotation_id {annotation.id}, it must be a list like [x1, y1, v1, x2, y2, v2...]"
                )
                continue

            keypoints = []
            for i in range(0, len(annotation.keypoints), 3):
                batch = annotation.keypoints[i : i + 3]
                keypoints.append([batch[0], batch[1], int(batch[2])])
            annotations[asset_id]["keypoints"].append(
                {
                    "label_id": label.id,
                    "text": annotation.utf8_string,
                    "keypoints": keypoints,
                    "attributes": annotation.attributes,
                }
            )

    return [
        {"asset_id": asset_id, **annotation}
        for asset_id, annotation in annotations.items()
    ]


@exception_handler
@beartype
def read_video_annotations(  # noqa: C901
    cocofile_type: InferenceType,
    coco_annotations: list[VideoAnnotation],
    coco_frames: list[ExtendedImage],
    labels: dict[int, Label],
    assets: dict[int, tuple[str, dict | None]],
    only_key_frames: bool = True,
    use_image_id_as_frame_id: bool = False,
) -> list[dict]:
    frames: dict[int, ExtendedImage] = {
        coco_frame.id: coco_frame for coco_frame in coco_frames
    }

    tracks: dict[tuple[int, int], dict] = {}
    for annotation in coco_annotations:
        if annotation.attributes is None:
            logger.warning(
                f"annotation {annotation.id} does not have attributes with track_id information. We cannot parse it."
            )
            continue

        if only_key_frames and annotation.attributes.keyframe is False:
            # If you consider only key frames of COCO file, ignore others
            logger.debug(
                f"skipping annotation {annotation.id} because it is not a keyframe"
            )
            continue

        if annotation.attributes.track_id is None:
            logger.warning(
                f"annotation {annotation.id} has no 'attributes.track_id' set, we cannot infer track"
            )
            continue

        coco_track_id = annotation.attributes.track_id
        track_key = (annotation.video_id, coco_track_id)

        if annotation.attributes.frame_id is None:
            if annotation.image_id not in frames:
                logger.warning(
                    f"annotation {annotation.id} has no 'attributes.frame_id' and its image_id is unknown, we cannot infer frame index"
                )
                continue
            elif frames[annotation.image_id].frame_id is None:
                if use_image_id_as_frame_id:
                    frame_index = annotation.image_id
                else:
                    logger.warning(
                        f"annotation {annotation.id} is bound to image {annotation.image_id} which does not have frame_id, so we cannot infer frame index"
                    )
                    continue
            else:
                frame_index = frames[annotation.image_id].frame_id
        else:
            frame_index = annotation.attributes.frame_id

        try:
            label = labels[annotation.category_id]
        except KeyError:  # pragma: no cover
            logger.error(
                f"category_id {annotation.category_id} not found into retrieved labels"
            )
            continue

        if track_key not in tracks:
            tracks[track_key] = {
                "label_id": label.id,
                "start_frame_index": frame_index,
                # This field is not used by api
                "_last_frame_index": frame_index + 1,
                "polygon_keyframes": [],
                "rectangle_keyframes": [],
            }
        elif frame_index < tracks[track_key]["start_frame_index"]:
            # Case where current annotation is before current first keyframe of track
            # So we will store new start frame index
            # and we also need to reset already computed relative frame indexes
            offset = tracks[track_key]["start_frame_index"] - frame_index
            tracks[track_key]["start_frame_index"] = frame_index
            for keyframe_type in ["rectangle_keyframes", "polygon_keyframes"]:
                for keyframe in tracks[track_key][keyframe_type]:
                    keyframe["frame_index"] = keyframe["frame_index"] + offset

        # Only take first utf8_string key we find in annotations
        if "text" not in tracks[track_key] and annotation.utf8_string is not None:
            tracks[track_key]["text"] = annotation.utf8_string

        # Picsellia accepts relative frame index as frame_index of keyframes
        start_frame_index = tracks[track_key]["start_frame_index"]
        relative_frame_index = frame_index - start_frame_index

        if cocofile_type == InferenceType.SEGMENTATION:
            if not annotation.is_rle():
                polygon_coords = annotation.polygon_to_list_coordinates()
            else:
                logger.error(
                    f"annotation_id {annotation.id} is a RLE which is not supported yet"
                )
                continue

            for polygon_coord in polygon_coords:
                tracks[track_key]["polygon_keyframes"].append(
                    {"polygon": polygon_coord, "frame_index": relative_frame_index}
                )
        elif cocofile_type == InferenceType.OBJECT_DETECTION:
            tracks[track_key]["rectangle_keyframes"].append(
                {
                    "x": int(annotation.bbox[0]),
                    "y": int(annotation.bbox[1]),
                    "w": int(annotation.bbox[2]),
                    "h": int(annotation.bbox[3]),
                    "frame_index": relative_frame_index,
                }
            )
        elif cocofile_type == InferenceType.CLASSIFICATION:
            raise NotImplementedError()

        tracks[track_key]["_last_frame_index"] = max(
            tracks[track_key]["_last_frame_index"], frame_index + 1
        )

    annotations_asset_map: dict[str, dict] = {}
    for track_key, track in tracks.items():
        video_id, _ = track_key
        try:
            asset_id = assets[video_id][0]
        except KeyError:
            logger.error(f"image_id {video_id} not found into retrieved assets")
            continue

        if asset_id not in annotations_asset_map:
            annotations_asset_map[asset_id] = {"tracks": []}

        # End key frames are relative
        relative_frame_index = track["_last_frame_index"] - track["start_frame_index"]
        track["end_keyframes"] = [{"frame_index": relative_frame_index}]

        annotations_asset_map[asset_id]["tracks"].append(track)

    return [
        {"asset_id": asset_id, **annotation}
        for asset_id, annotation in annotations_asset_map.items()
    ]
