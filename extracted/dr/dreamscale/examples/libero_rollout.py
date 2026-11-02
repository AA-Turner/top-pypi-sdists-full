from __future__ import annotations

import math

import dreamscale
from dreamscale.policy import RunContext


def quat_to_axis_angle(quat_xyzw) -> list[float]:
    x, y, z, w = [float(value) for value in quat_xyzw]
    w = max(-1.0, min(1.0, w))
    den = math.sqrt(max(0.0, 1.0 - (w * w)))
    if den <= 1e-10:
        return [0.0, 0.0, 0.0]
    angle = 2.0 * math.acos(w)
    return [(x * angle) / den, (y * angle) / den, (z * angle) / den]


def build_libero_state(obs) -> list[float]:
    return [
        *[float(v) for v in obs["robot0_eef_pos"]],
        *quat_to_axis_angle(obs["robot0_eef_quat"]),
        *[float(v) for v in obs["robot0_gripper_qpos"]],
    ]


def run_libero_rollout(env, *, instruction: str, max_actions: int = 220):
    obs = env.reset()

    def observe(ctx: RunContext):
        return dreamscale.libero.observation(
            agent_frame=obs["agentview_image"],
            wrist_frame=obs["robot0_eye_in_hand_image"],
            state=build_libero_state(obs),
            actions_remaining=ctx.actions_remaining,
        )

    def act(action, ctx: RunContext):
        nonlocal obs
        _ = ctx
        obs, _reward, done, _info = env.step(list(action))
        return done

    with dreamscale.connect(model="molmoact2-libero") as policy:
        return policy.run(
            instruction=instruction,
            observe=observe,
            act=act,
            max_actions=max_actions,
            strategy=dreamscale.RunStrategy.libero_default(),
        )
