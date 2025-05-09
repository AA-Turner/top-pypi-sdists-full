from typing import List, Optional, Tuple

import mujoco
import numpy as np

from . import constants as consts
from .exceptions import InvalidKeyframe, InvalidMocapBody


def move_mocap_to_frame(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    mocap_name: str,
    frame_name: str,
    frame_type: str,
) -> None:
    """Initialize mocap body pose at a desired frame.

    Args:
        model: Mujoco model.
        data: Mujoco data.
        mocap_name: The name of the mocap body.
        frame_name: The desired frame name.
        frame_type: The desired frame type. Can be "body", "geom" or "site".
    """
    mocap_id = model.body(mocap_name).mocapid[0]
    if mocap_id == -1:
        raise InvalidMocapBody(mocap_name, model)

    obj_id = mujoco.mj_name2id(model, consts.FRAME_TO_ENUM[frame_type], frame_name)
    xpos = getattr(data, consts.FRAME_TO_POS_ATTR[frame_type])[obj_id]
    xmat = getattr(data, consts.FRAME_TO_XMAT_ATTR[frame_type])[obj_id]

    data.mocap_pos[mocap_id] = xpos.copy()
    mujoco.mju_mat2Quat(data.mocap_quat[mocap_id], xmat)


def get_freejoint_dims(model: mujoco.MjModel) -> Tuple[List[int], List[int]]:
    """Get all floating joint configuration and tangent indices.

    Args:
        model: Mujoco model.

    Returns:
        A (q_ids, v_ids) pair containing all floating joint indices in the
        configuration and tangent spaces respectively.
    """
    q_ids: List[int] = []
    v_ids: List[int] = []
    for j in range(model.njnt):
        if model.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE:
            qadr = model.jnt_qposadr[j]
            vadr = model.jnt_dofadr[j]
            q_ids.extend(range(qadr, qadr + 7))
            v_ids.extend(range(vadr, vadr + 6))
    return q_ids, v_ids


def custom_configuration_vector(
    model: mujoco.MjModel,
    key_name: Optional[str] = None,
    **kwargs,
) -> np.ndarray:
    """Generate a configuration vector where named joints have specific values.

    Args:
        model: Mujoco model.
        key_name: Optional keyframe name to initialize the configuration vector from.
            Otherwise, the default pose `qpos0` is used.
        kwargs: Custom values for joint coordinates.

    Returns:
        Configuration vector where named joints have the values specified in
            keyword arguments, and other joints have their neutral value or value
            defined in the keyframe if provided.
    """
    data = mujoco.MjData(model)
    if key_name is not None:
        key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, key_name)
        if key_id == -1:
            raise InvalidKeyframe(key_name, model)
        mujoco.mj_resetDataKeyframe(model, data, key_id)
    else:
        mujoco.mj_resetData(model, data)
    q = data.qpos.copy()
    for name, value in kwargs.items():
        jid = model.joint(name).id
        jnt_dim = consts.qpos_width(model.jnt_type[jid])
        qid = model.jnt_qposadr[jid]
        value = np.atleast_1d(value)
        if value.shape != (jnt_dim,):
            raise ValueError(
                f"Joint {name} should have a qpos value of {(jnt_dim,)} but "
                f"got {value.shape}"
            )
        q[qid : qid + jnt_dim] = value
    return q


def get_body_body_ids(model: mujoco.MjModel, body_id: int) -> List[int]:
    """Get immediate children bodies belonging to a given body.

    Args:
        model: Mujoco model.
        body_id: ID of body.

    Returns:
        A List containing all child body ids.
    """
    return [
        i
        for i in range(model.nbody)
        if model.body_parentid[i] == body_id
        and body_id != i  # Exclude the body itself.
    ]


def get_subtree_body_ids(model: mujoco.MjModel, body_id: int) -> List[int]:
    """Get all bodies belonging to subtree starting at a given body.

    Args:
        model: Mujoco model.
        body_id: ID of body where subtree starts.

    Returns:
        A List containing all subtree body ids.
    """
    body_ids: List[int] = []
    stack = [body_id]
    while stack:
        body_id = stack.pop()
        body_ids.append(body_id)
        stack += get_body_body_ids(model, body_id)
    return body_ids


def get_body_geom_ids(model: mujoco.MjModel, body_id: int) -> List[int]:
    """Get immediate geoms belonging to a given body.

    Here, immediate geoms are those directly attached to the body and not its
    descendants.

    Args:
        model: Mujoco model.
        body_id: ID of body.

    Returns:
        A list containing all body geom ids.
    """
    geom_start = model.body_geomadr[body_id]
    geom_end = geom_start + model.body_geomnum[body_id]
    return list(range(geom_start, geom_end))


def get_subtree_geom_ids(model: mujoco.MjModel, body_id: int) -> List[int]:
    """Get all geoms belonging to subtree starting at a given body.

    Here, a subtree is defined as the kinematic tree starting at the body and including
    all its descendants.

    Args:
        model: Mujoco model.
        body_id: ID of body where subtree starts.

    Returns:
        A list containing all subtree geom ids.
    """
    geom_ids: List[int] = []
    stack = [body_id]
    while stack:
        body_id = stack.pop()
        geom_ids.extend(get_body_geom_ids(model, body_id))
        stack += get_body_body_ids(model, body_id)
    return geom_ids
