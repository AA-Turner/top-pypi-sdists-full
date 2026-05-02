import base64
import gzip
from io import BytesIO
import json
from pathlib import Path
from typing import NamedTuple
from urllib.parse import unquote, urlparse

import numpy as np
from fyuneru.geometry3d import SElement
from returns.maybe import Maybe
from funcy import first


class TaskConfig(NamedTuple):
    uid: str
    domain_id: str
    name: str
    setting: dict


class Label(NamedTuple):
    uid: str
    id: Maybe[int]
    draw_type: str
    hash: str
    label: Maybe[str]
    frame_index: int
    lens_index: Maybe[int]
    points: Maybe[list]
    attributes: Maybe[dict]
    label_id_map: Maybe[str]
    points_in_box: Maybe[int]
    group: int | None


class Frame(NamedTuple):
    idx: int
    url: str
    imgUrls: Maybe[list[str]]
    location: Maybe[SElement]
    size: Maybe[dict]


class Item(NamedTuple):
    uid: str
    batch_uid: str
    labels: list[Label]
    frames: list[Frame]


def is_merge(urls: list[str]) -> bool:
    """
    urls 是否是合并任务
    """
    return len(urls) == 1


def extract_frames(item: dict) -> list[Frame]:
    info = item["info"]["info"]
    locations = info.get("locations", [])
    image_urls = (
        info.get("url")
        or info.get("imgUrls")
        or [location["imgUrls"] for location in locations]
    )
    urls = info.get("pcdUrls") or info.get("urls", None)
    # locations 出现可能是叠帧、重建
    if locations:
        if is_merge(urls):
            return [
                Frame(idx=idx, url=url, imgUrls=imgUrls, location=location, size=None)
                for idx, (url, imgUrls, location) in enumerate(
                    zip(urls * len(locations), image_urls, locations)
                )
            ]
        return [
            Frame(idx=idx, url=url, imgUrls=imgUrls, location=location, size=None)
            for idx, (url, imgUrls, location) in enumerate(
                zip(urls, image_urls, locations)
            )
        ]
    # 没有 locations 但是有 urls 单帧点云
    elif urls:
        return [
            Frame(idx=idx, url=url, imgUrls=imgUrls, location=None, size=None)
            for idx, (url, imgUrls) in enumerate(zip(urls, image_urls))
        ]
    # 没有 pcd 就是 2D 任务
    elif image_urls:
        size = info.get("size", None)
        return [
            Frame(idx=idx, url=url, imgUrls=None, location=None, size=size[idx])
            for idx, url in enumerate(image_urls)
        ]
    else:
        raise ValueError("Unknown task")


def extract_label(label: dict) -> Label:
    label_data = label["data"]
    uid = label["_id"]
    id = label_data.get("id", None)
    draw_type = label_data["drawType"]
    hash = label_data["hash"]
    label = label_data.get("label", None)
    frame_index = label_data["frameIndex"]
    lens_index = label_data.get("lensIndex", None)
    points = label_data.get("points", None)
    attributes = label_data.get("attributes", None)
    label_id_map = label_data.get("labelIdMap", None)
    points_in_box = label_data.get("pointsInBox", None)
    group = label_data.get("group", None)
    return Label(
        uid=uid,
        id=id,
        draw_type=draw_type,
        hash=hash,
        label=label,
        frame_index=frame_index,
        lens_index=lens_index,
        points=points,
        attributes=attributes,
        label_id_map=label_id_map,
        points_in_box=points_in_box,
        group=group,
    )


def extract_labels(item: dict) -> list[Label]:
    return [extract_label(label=label) for label in item["labels"]]


def parse_task_config(task: dict) -> TaskConfig:
    uid = task["_id"]
    domain_id = task["domainId"]
    name = task["name"]
    setting = task["setting"]
    return TaskConfig(uid=uid, domain_id=domain_id, name=name, setting=setting)


def parse_export_config(config: dict) -> dict:
    return config


def parse_item(item: dict) -> Item:
    uid = item["_id"]
    batch_uid = item["item"]["batchId"]
    labels = extract_labels(item)
    frames = extract_frames(item)

    return Item(uid=uid, batch_uid=batch_uid, labels=labels, frames=frames)


def parse_items(items: list[dict]) -> list[Item]:
    return [parse_item(item) for item in items]


class ExportTask(NamedTuple):
    task_config: TaskConfig
    export_config: dict
    items: list[Item]


def parse_origin(origin: dict) -> ExportTask:
    task = origin.get("task")
    config = origin.get("config")
    data = origin.get("data")

    export_config = parse_export_config(config)
    task_config: TaskConfig = parse_task_config(task)
    items: list[Item] = parse_items(data)

    return ExportTask(task_config=task_config, export_config=export_config, items=items)


def url_to_path(url: str) -> Path:
    parsed_url_path = urlparse(url).path
    unquote_path = unquote(parsed_url_path)
    return Path(unquote_path)


def calculate_resource_dst(sub_path: Path, dst_root: Path, level: int) -> Path:
    return dst_root / Path(*sub_path.parts[level:])


def build_frame_resource(frame: Frame, dst_root: Path, level: int) -> dict[Path, str]:
    path_url_dict = dict()
    main_resource_path = url_to_path(frame.url)
    path_url_dict[calculate_resource_dst(main_resource_path, dst_root, level)] = (
        frame.url
    )
    if frame.imgUrls:
        path_url_dict.update(
            {
                calculate_resource_dst(url_to_path(img_url), dst_root, level): img_url
                for img_url in frame.imgUrls
            }
        )
    return path_url_dict


def extract_xyz(label: Label) -> np.ndarray:
    """提取xyz"""
    points = label.points
    translation = slice(0, 3)
    return np.array(points[translation])


def extract_rpy(label: Label) -> np.ndarray:
    """提取rpy"""
    points = label.points
    rpy = slice(3, 6)
    return np.array(points[rpy])


def extract_size(label: Label) -> np.ndarray:
    """提取size"""
    points = label.points
    size = slice(6, 9)
    return np.array(points[size])


def extract_half_size(label: Label) -> np.ndarray:
    """提取half_size"""
    points = label.points
    # 兼容预设矩形
    if len(points) != 9:
        points = points.tolist() + [0] * (9 - len(points))
    box_lwh = extract_size(label)
    box_size = box_lwh / 2
    box_size = np.array(
        [
            -box_size[0],
            box_size[0],
            -box_size[1],
            box_size[1],
            -box_size[2],
            box_size[2],
        ]
    )
    return box_size


def decompress_and_decode(encoded_str):
    """解析labelIdMap"""

    # 1. Base64 解码
    compressed_data = base64.b64decode(encoded_str)

    # 2. Gzip 解压
    with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode="rb") as f:
        decompressed_data = f.read().decode("utf-8")  # 解压后的字节流转为字符串

    # 3. JSON 解析
    scalar_ins_list = json.loads(decompressed_data)
    return scalar_ins_list


def get_id_semantic_map(
    frame_seg_labels: list[Label], alias_mean_map: dict[str, int]
) -> dict[int, int]:
    """获取id到semantic的映射"""
    id_semantic_map = {}
    for seg_label in frame_seg_labels:
        if seg_label.draw_type != "SEMANTIC_POINT":
            continue
        id_semantic_map[seg_label.id] = alias_mean_map[seg_label.label]
    return id_semantic_map


def extract_semantic_base(seg_labels: list[Label]) -> Label:
    """提取semantic_base"""
    return first(
        seg_label for seg_label in seg_labels if seg_label.draw_type == "SEMANTIC_BASE"
    )
