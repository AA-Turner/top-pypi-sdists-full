"""
3D 几何工具
"""

from typing import Iterable, NamedTuple
import numpy as np
from scipy.spatial.transform import Rotation as R


class SElement(NamedTuple):
    """3D元素
    平移和旋转

    Args:
        translation: 平移向量
        rotation: 旋转四元数
    """

    translation: np.ndarray
    rotation: np.ndarray


def default_element() -> SElement:
    """初始化默认3D元素"""
    return SElement(
        translation=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0, 1.0])
    )


def homogeneous_to_element(homogeneous: np.ndarray) -> SElement:
    """将齐次矩阵转换为3D元素"""
    translation = homogeneous[:3, 3]
    rotation = R.from_matrix(homogeneous[:3, :3]).as_quat()
    return SElement(translation=translation, rotation=rotation)


def to_rotation_matrix(element: SElement) -> np.ndarray:
    """提取旋转矩阵"""
    return R.from_quat(element.rotation).as_matrix()


def to_homogeneous_matrix(element: SElement) -> np.ndarray:
    """将3D元素转换为齐次矩阵"""
    matrix = np.eye(4)
    matrix[:3, :3] = R.from_quat(element.rotation).as_matrix()
    matrix[:3, 3] = element.translation
    return matrix


class Range3D(NamedTuple):
    """3D范围"""

    x_min: float
    y_min: float
    z_min: float
    x_max: float
    y_max: float
    z_max: float


class Box3D(NamedTuple):
    element: SElement
    size: Range3D


def transform_pc(xyz: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """
    三维点 转换到box坐标系
    """
    xyz_homo = np.hstack([xyz, np.ones((xyz.shape[0], 1))])
    return (matrix @ xyz_homo.T).T[:, :3]


def in_box_mask(xyz: np.ndarray, box: Box3D) -> np.ndarray:
    """
    返回布尔掩码, 表点在box内。
    pc: (N, 3) ndarray
    box: Box3D
    """
    # 世界坐标系 -> box局部坐标系
    t_glo_box = to_homogeneous_matrix(box.element)
    t_box_glo = np.linalg.inv(t_glo_box)
    xyz_in_box_element = transform_pc(xyz=xyz, matrix=t_box_glo)

    x_idx = 0
    y_idx = 1
    z_idx = 2
    mask = np.ones((xyz_in_box_element.shape[0],), dtype=np.bool_)
    mask &= xyz_in_box_element[:, x_idx] >= box.size.x_min
    mask &= xyz_in_box_element[:, x_idx] < box.size.x_max
    mask &= xyz_in_box_element[:, y_idx] >= box.size.y_min
    mask &= xyz_in_box_element[:, y_idx] < box.size.y_max
    mask &= xyz_in_box_element[:, z_idx] >= box.size.z_min
    mask &= xyz_in_box_element[:, z_idx] < box.size.z_max
    return mask


def in_boxes_mask(xyz: np.ndarray, boxes: Iterable[Box3D]) -> np.ndarray:
    """
    返回布尔掩码，表示点是否落在任意一个 box 内。
    - 在任意 box 内 → True
    - 在所有 box 外 → False
    """

    mask = np.zeros((xyz.shape[0],), dtype=np.bool_)
    for box in boxes:
        mask |= in_box_mask(xyz=xyz, box=box)
    return mask
