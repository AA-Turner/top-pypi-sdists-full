"""
nuScenes导出适配器
"""

import base64
from enum import Enum
from itertools import groupby
from pathlib import Path
import shutil
from typing import Callable, NamedTuple
import uuid
from fyuneru.geometry3d import (
    Box3D,
    Range3D,
    SElement,
    to_homogeneous_matrix,
    transform_pc,
)
from fyuneru.lib import mkdir
import numpy as np


class NuScenesIndex(Enum):
    """nuScenes索引文件"""

    ATTRIBUTE = "attribute.json"
    # 标定token + 传感器 token信息
    CALIBRATED_SENSOR = "calibrated_sensor.json"
    CATEGORY = "category.json"
    EGO_POSE = "ego_pose.json"
    INSTANCE = "instance.json"
    LIDARSEG = "lidarseg.json"
    LOG = "log.json"
    MAP = "map.json"
    SAMPLE_ANNOTATION = "sample_annotation.json"
    # 多个sample data token + calibration token
    SAMPLE_DATA = "sample_data.json"
    # 时间戳+sample data token
    SAMPLE_TIME = "sample_time.json"
    SAMPLE = "sample.json"
    SCENE = "scene.json"
    # 传感器的token和channel名称
    SENSOR = "sensor.json"
    VISIBILITY = "visibility.json"
    SAMPLES_SUB = "samples"
    SWEEPS_SUB = "sweeps"
    LIDARSEG_SUB = "lidarseg"


class Modality(Enum):
    """传感器类型"""

    CAMERA = "camera"
    LIDAR = "lidar"
    RADAR = "radar"


class Sensor(NamedTuple):
    """传感器 sensor.json 实体"""

    token: str | None
    channel: str
    modality: str


class EgoPose(NamedTuple):
    """ego_pose.json 实体"""

    token: str | None
    timestamp: int
    translation: list[float]
    rotation: list[float]


class Log(NamedTuple):
    """log.json 实体"""

    token: str | None
    logfile: str
    vehicle: str
    data_captured: str
    location: str
    map_token: str


class Map(NamedTuple):
    """map.json 实体"""

    category: str
    token: str | None
    filename: str
    log_tokens: list[str]


class Sample(NamedTuple):
    """sample.json 实体"""

    token: str | None
    timestamp: int
    prev: str
    next: str
    scene_token: str
    data: dict[str, str]
    anns: list[str]


class Scene(NamedTuple):
    """scene.json 实体"""

    token: str
    log_token: str
    nbr_samples: int
    first_sample_token: str
    last_sample_token: str
    name: str
    description: str


class CalibratedSensor(NamedTuple):
    """calibrated_sensor.json 实体"""

    token: str
    sensor_token: str
    translation: list
    rotation: list
    camera_intrinsic: list


class Visibility(NamedTuple):
    """visibility.json 实体"""

    description: str
    token: str
    level: str


class SampleData(NamedTuple):
    """sample_data.json 实体"""

    token: str
    sample_token: str
    ego_pose_token: str
    calibrated_sensor_token: str
    filename: str
    fileformat: str
    is_key_frame: bool
    height: int
    width: int
    timestamp: int
    prev: str
    next: str
    sensor_modality: str
    channel: str


class Category(NamedTuple):
    """category.json 实体"""

    token: str
    name: str
    description: str
    index: int


class Lidarseg(NamedTuple):
    """lidarseg.json 实体"""

    token: str
    sample_data_token: str
    filename: str


class GtsAnnotation(NamedTuple):
    """sample_annotation.json 实体"""

    token: str
    timestamp: int
    gt_path: str
    next: str
    prev: str


class Attribute(NamedTuple):
    """attribute.json 实体"""

    token: str
    name: str
    description: str


class SampleAnnotation(NamedTuple):
    """sample_annotation.json 实体"""

    token: str
    sample_token: str
    category_name: str
    instance_token: str
    visibility_token: str
    attribute_tokens: list[str]
    translation: list
    size: list
    rotation: list
    prev: str
    next: str
    num_lidar_pts: int
    num_radar_pts: int


class Instance(NamedTuple):
    """instance.json 实体"""

    token: str
    category_token: str
    nbr_annotations: int
    first_annotation_token: str
    last_annotation_token: str


def to_sample(sensor_name: str, sensor_files: list[Path], nuscenes_root: Path):
    """
    转化sample目录
    """
    sample_dir = nuscenes_root / NuScenesIndex.SAMPLES_SUB.value / sensor_name
    mkdir(sample_dir)
    for sensor_file in sensor_files:
        shutil.copy(sensor_file, sample_dir / sensor_file.name)


def cal_sample_path(sensor_name: str, sensor_file: Path) -> Path:
    """计算sample路径"""
    return NuScenesIndex.SAMPLES_SUB.value / sensor_name / sensor_file.name


def get_default_category_index_map() -> dict[str, int]:
    """nuscenes官方label:id语义"""
    return {
        "noise": 0,
        "animal": 1,
        "human.pedestrian.adult": 2,
        "human.pedestrian.child": 3,
        "human.pedestrian.construction_worker": 4,
        "human.pedestrian.personal_mobility": 5,
        "human.pedestrian.police_officer": 6,
        "human.pedestrian.stroller": 7,
        "human.pedestrian.wheelchair": 8,
        "movable_object.barrier": 9,
        "movable_object.debris": 10,
        "movable_object.pushable_pullable": 11,
        "movable_object.trafficcone": 12,
        "static_object.bicycle_rack": 13,
        "vehicle.bicycle": 14,
        "vehicle.bus.bendy": 15,
        "vehicle.bus.rigid": 16,
        "vehicle.car": 17,
        "vehicle.construction": 18,
        "vehicle.emergency.ambulance": 19,
        "vehicle.emergency.police": 20,
        "vehicle.motorcycle": 21,
        "vehicle.trailer": 22,
        "vehicle.truck": 23,
        "flat.driveable_surface": 24,
        "flat.other": 25,
        "flat.sidewalk": 26,
        "flat.terrain": 27,
        "static.manmade": 28,
        "static.other": 29,
        "static.vegetation": 30,
        "vehicle.ego": 31,
    }


def get_default_category_s() -> list[Category]:
    """获取默认category列表"""
    default_category_index_map = get_default_category_index_map()
    return [
        Category(
            token=gen_token(seed=name),
            name=name,
            description="",
            index=index,
        )
        for name, index in default_category_index_map.items()
    ]


def gen_token(seed: str | None = None) -> str:
    """生成token"""
    if not seed:
        return uuid.uuid4().hex
    data = seed.encode("utf-8")
    return base64.b64encode(data).decode("utf-8")


class MolarIndex(NamedTuple):
    """molar索引"""

    task: str
    item: str
    sample: str
    channel: str
    label: str


def hash_molar_index(molar_index: MolarIndex) -> str:
    """hash平台索引"""
    task = molar_index.task
    item = molar_index.item
    sample = molar_index.sample if molar_index.sample else ""
    channel = molar_index.channel if molar_index.channel else ""
    label = molar_index.label if molar_index.label else ""
    return f"{task}_{item}_{sample}_{channel}_{label}"


def unhash_molar_index(molar_hash: str) -> MolarIndex:
    """unhash平台索引"""
    task, item, sample, channel, label = molar_hash.split("_")
    return MolarIndex(task=task, item=item, sample=sample, channel=channel, label=label)


def xyz_wxyz_to_homogeneous_matrix(xyz: np.ndarray, wxyz: np.ndarray) -> np.ndarray:
    """wxyz转homogeneous_matrix"""
    element = SElement(translation=xyz, rotation=wxyz2xyzw(wxyz))
    return to_homogeneous_matrix(element)


def point_cloud_sensor_to_ego(
    point_cloud_in_sensor: np.ndarray,
    calibrated_sensor: CalibratedSensor,
) -> np.ndarray:
    """点云传感器坐标系到ego坐标系"""
    t_ego_sensor = xyz_wxyz_to_homogeneous_matrix(
        xyz=calibrated_sensor.translation, wxyz=calibrated_sensor.rotation
    )
    xyz_in_sensor = point_cloud_in_sensor[:, :3]
    xyz_in_ego = transform_pc(xyz=xyz_in_sensor, matrix=t_ego_sensor)
    point_cloud_in_ego = np.hstack([xyz_in_ego, point_cloud_in_sensor[:, 3:]])
    return point_cloud_in_ego


def load_ego_point_cloud(
    sample_data: SampleData,
    calibrated_sensor: CalibratedSensor,
    nusc_root: Path,
    point_cloud_loader: Callable[[Path], np.ndarray],
) -> np.ndarray:
    """加载ego坐标系点云"""
    bin_file = nusc_root / sample_data.filename
    load_point_cloud = point_cloud_loader
    point_cloud_in_sensor = load_point_cloud(bin_file)
    point_cloud_in_ego = point_cloud_sensor_to_ego(
        point_cloud_in_sensor, calibrated_sensor
    )
    return point_cloud_in_ego


def xyzw2wxyz(quat_xyzw: np.ndarray) -> np.ndarray:
    """wxyz转xyzw"""
    return np.roll(quat_xyzw, 1)


def wxyz2xyzw(quat_wxyz: np.ndarray) -> np.ndarray:
    """xyzw转wxyz"""
    return np.roll(quat_wxyz, -1)


def xyz_wxyz_to_element(xyz: np.ndarray, wxyz: np.ndarray) -> SElement:
    """xyzw转element"""
    xyzw = wxyz2xyzw(wxyz)
    return SElement(translation=xyz, rotation=xyzw)


def point_cloud_to_ego_coord(
    point_cloud: np.ndarray, calibrated_sensor: CalibratedSensor
) -> np.ndarray:
    """定云传感器坐标转化自车系坐标"""
    xyz_in_sensor_coord = point_cloud[:, :3]
    t_ego_sensor = to_homogeneous_matrix(
        xyz_wxyz_to_element(
            xyz=calibrated_sensor.translation, wxyz=calibrated_sensor.rotation
        )
    )
    xyz_in_ego_sensor_coord = transform_pc(xyz=xyz_in_sensor_coord, matrix=t_ego_sensor)
    return np.hstack([xyz_in_ego_sensor_coord, point_cloud[:, 3:]])


def init_func_sample_data_point_cloud_loader(
    nusc_root: Path, point_cloud_loader: Callable[[Path], np.ndarray]
) -> Callable[[SampleData], np.ndarray]:
    """初始化sample_data点云加载器"""
    load_point_cloud = point_cloud_loader

    def sample_data_point_cloud_loader(sample_data: SampleData) -> np.ndarray:
        pc_file = nusc_root / sample_data.filename
        return load_point_cloud(pc_file)

    return sample_data_point_cloud_loader


def init_func_ego_point_cloud_loader(
    calibrated_sensor_s: list[CalibratedSensor],
    sample_data_point_cloud_loader: Callable[[SampleData], np.ndarray],
) -> Callable[[SampleData], np.ndarray]:
    """初始化ego点云加载器"""
    token_indexed_calibrated_sensor = {
        calibrated_sensor.token: calibrated_sensor
        for calibrated_sensor in calibrated_sensor_s
    }
    load_sample_data_point_cloud = sample_data_point_cloud_loader

    def ego_point_cloud_loader(sample_data: SampleData) -> np.ndarray:
        point_cloud_in_sensor = load_sample_data_point_cloud(sample_data)
        calibrated_sensor = token_indexed_calibrated_sensor[
            sample_data.calibrated_sensor_token
        ]
        point_cloud_in_ego = point_cloud_sensor_to_ego(
            point_cloud_in_sensor, calibrated_sensor
        )
        return point_cloud_in_ego

    return ego_point_cloud_loader


def init_func_instance_id_generator(
    log_instance_s: list[Instance],
) -> Callable[[Instance], int]:
    """初始化实例id生成器
    Args:
        log_instance_s: log单位内的instance
    Returns:
        instance_id_generator: 实例id生成器
    """
    instance_id_map = {
        instance.token: idx for idx, instance in enumerate(log_instance_s, 1)
    }

    def instance_id_generator(instance_token: str) -> int:
        return instance_id_map[instance_token]

    return instance_id_generator


def init_func_global_point_cloud_loader(
    ego_pose_s: list[EgoPose],
    ego_point_cloud_loader: Callable[[SampleData], np.ndarray],
) -> Callable[[SampleData], np.ndarray]:
    """初始化全局点云加载器"""
    token_indexed_ego_pose = {ego_pose.token: ego_pose for ego_pose in ego_pose_s}

    def global_point_cloud_loader(sample_data: SampleData) -> np.ndarray:
        point_cloud_in_ego = ego_point_cloud_loader(sample_data)
        ego_pose_token = sample_data.ego_pose_token
        ego_pose = token_indexed_ego_pose[ego_pose_token]
        t_map_ego = to_homogeneous_matrix(
            xyz_wxyz_to_element(xyz=ego_pose.translation, wxyz=ego_pose.rotation)
        )
        xyz_in_ego = point_cloud_in_ego[:, :3]
        xyz_in_map = transform_pc(xyz=xyz_in_ego, matrix=t_map_ego)
        point_cloud_in_map = np.hstack([xyz_in_map, point_cloud_in_ego[:, 3:]])
        return point_cloud_in_map

    return global_point_cloud_loader


def init_func_log_scene_getter(scene_s: list[Scene]) -> Callable[[str], list[Scene]]:
    """初始化log单位内的scene获取"""
    log_token_scene_grouper = groupby(iterable=scene_s, key=lambda x: x.log_token)
    log_token_scene_s_map = {
        log_token: list(values) for log_token, values in log_token_scene_grouper
    }

    def log_scene_getter(log_token: str) -> list[Scene]:
        return log_token_scene_s_map[log_token]

    return log_scene_getter


def init_func_scene_sample_getter(
    sample_s: list[Sample],
) -> Callable[[str], list[Sample]]:
    """初始化scene单位内的sample获取"""
    scene_sample_groupper = groupby(
        iterable=sample_s, key=lambda sample: sample.scene_token
    )
    scene_sample_s_map = {
        scene_token: list[Sample](values)
        for scene_token, values in scene_sample_groupper
    }

    def scene_sample_getter(scene_token: str) -> list[Sample]:
        return scene_sample_s_map[scene_token]

    return scene_sample_getter


def init_func_sample_data_getter(
    sample_data_s: list[SampleData],
) -> Callable[[str], SampleData]:
    """初始化sample_data获取"""
    sample_data_groupper = groupby(iterable=sample_data_s, key=lambda x: x.sample_token)
    sample_data_s_map = {
        sample_token: list[SampleData](values)
        for sample_token, values in sample_data_groupper
    }

    def sample_data_getter(sample_token: str) -> SampleData:
        return sample_data_s_map[sample_token]

    return sample_data_getter


def init_func_sample_annotation_getter(
    sample_annotation_s: list[SampleAnnotation],
) -> Callable[[str], list[SampleAnnotation]]:
    """初始化sample_annotation获取"""
    sample_annotation_groupper = groupby(
        iterable=sample_annotation_s, key=lambda x: x.sample_token
    )
    sample_annotation_s_map = {
        sample_token: list[SampleAnnotation](values)
        for sample_token, values in sample_annotation_groupper
    }

    def sample_annotation_getter(sample_token: str) -> list[SampleAnnotation]:
        return sample_annotation_s_map[sample_token]

    return sample_annotation_getter


class InstanceMask(NamedTuple):
    """实例掩码"""

    sample_data_token: str
    instance_index_token_map: dict[int, str]
    instance_mask: np.ndarray


def nusc_to_plat_size(nusc_size: np.ndarray) -> np.ndarray:
    """nuscenes w l h->plat l w h"""
    width_idx = 0
    length_idx = 1
    height_idx = 2
    return np.array(
        [nusc_size[length_idx], nusc_size[width_idx], nusc_size[height_idx]]
    )


def size_to_range(size: np.ndarray) -> Range3D:
    """size转range"""
    x_idx = 0
    y_idx = 1
    z_idx = 2
    x_min = -size[x_idx] / 2
    x_max = size[x_idx] / 2
    y_min = -size[y_idx] / 2
    y_max = size[y_idx] / 2
    z_min = -size[z_idx] / 2
    z_max = size[z_idx] / 2
    return Range3D(
        x_min=x_min, y_min=y_min, z_min=z_min, x_max=x_max, y_max=y_max, z_max=z_max
    )


def annotation_to_box(annotation: SampleAnnotation) -> Box3D:
    """nusc标签转 box3d"""
    xyz = annotation.translation
    wxyz = annotation.rotation
    element = xyz_wxyz_to_element(xyz, wxyz)
    wlh = annotation.size
    lwh = nusc_to_plat_size(wlh)
    range3d = size_to_range(lwh)
    return Box3D(element=element, size=range3d)


def init_func_no_target_point_loader(
    global_point_cloud_loader: Callable[[SampleData], np.ndarray],
    sample_data_instance_mask_getter: Callable[[str], InstanceMask],
) -> Callable[[SampleData], np.ndarray]:
    """初始化无目标点云加载器"""

    def no_target_point_loader(sample_data: SampleData) -> np.ndarray:
        global_point_cloud = global_point_cloud_loader(sample_data)
        instance_mask = sample_data_instance_mask_getter(sample_data.token)
        return global_point_cloud[~instance_mask.instance_mask]

    return no_target_point_loader


def init_func_lidarseg_getter(
    lidarseg_s: list[Lidarseg],
) -> Callable[[str], Lidarseg]:
    """初始化lidarseg获取"""
    lidarseg_groupper = groupby(iterable=lidarseg_s, key=lambda x: x.sample_data_token)
    lidarseg_s_map = {
        sample_data_token: list[Lidarseg](values)
        for sample_data_token, values in lidarseg_groupper
    }

    def lidarseg_getter(sample_data_token: str) -> Lidarseg:
        return lidarseg_s_map[sample_data_token]

    return lidarseg_getter


def init_func_lidarseg_bin_loader(
    segmentation_dtype: np.dtype,
    nusc_root: Path,
    nuscenes_version: str,
) -> Callable[[Lidarseg], np.ndarray]:
    """初始化lidarseg二进制加载器"""

    def lidarseg_bin_loader(lidarseg: Lidarseg) -> np.ndarray:
        lidarseg_file = (
            nusc_root
            / NuScenesIndex.LIDARSEG_SUB.value
            / nuscenes_version
            / lidarseg.filename
        )
        return np.fromfile(lidarseg_file, dtype=segmentation_dtype)

    return lidarseg_bin_loader
