"""Eight independent raw-camera LIBERO clients against an already-ready deployment.

Install the existing LIBERO simulator/assets first. This example creates no cloud
resources and changes no warm floor. It is a smoke, not a 4 Hz load/quality study.
"""

import argparse
import concurrent.futures
import json
import multiprocessing
import os
import time
from uuid import uuid4

import httpx

from dreamscale.errors import DreamscaleError
from dreamscale.inference import InferenceClient, action_request


def _api_key() -> str | None:
    # DROPBEAR_API_KEY is the pre-rename name.
    return os.environ.get("DREAMSCALE_API_KEY") or os.environ.get("DROPBEAR_API_KEY")


def run_robot(slot, deployment, calls, start_sequence):
    from dreamscale.sim.runtime import LiberoSimEnv, create_task_handle

    handle = create_task_handle(
        task_suite_name="libero_spatial",
        task_id=slot,
        seed=197 + slot,
        env_resolution=360,
        assets_path=None,
    )
    env = LiberoSimEnv(handle)
    episode_id, completed, done = uuid4().hex, 0, False
    requests, simulator_steps = [], 0
    try:
        obs = env.reset()
        with InferenceClient(
            api_key=_api_key(), api_base=deployment["api_base"]
        ) as client:
            client.connect()  # Discover direct ingress; retain the stable URL for results.
            for index in range(calls):
                raw = {
                    **obs,
                    "agentview_image": env.agent_frame(obs),
                    "robot0_eye_in_hand_image": env.wrist_frame(obs),
                }
                request = action_request(
                    deployment_id=deployment["id"],
                    robot_slot=slot,
                    sequence=start_sequence + index,
                    request_id=uuid4(),
                    episode_id=episode_id,
                    noise_seed=197 + slot * calls + index,
                    instruction=env.task_description,
                    observation=raw,
                )
                # Recover the original identity; never repeat the inference POST.
                try:
                    result = client.predict(request)
                except httpx.TransportError:
                    result = {"status": "pending"}
                except DreamscaleError as exc:
                    if exc.info.code not in (
                        "request_not_admitted",
                        "expired",
                        "preprocessing_failed",
                        "inference_unavailable",
                    ):
                        raise
                    result = {"status": "pending"}
                if result.get("status") == "pending":
                    result = client.resolve_request(
                        **{
                            k: request[k]
                            for k in (
                                "deployment_id",
                                "robot_slot",
                                "request_id",
                                "sequence",
                                "episode_id",
                            )
                        }
                    )
                until = time.monotonic() + 5
                while result.get("status") == "pending" and time.monotonic() < until:
                    time.sleep(1)
                    result = client.get_result(
                        deployment_id=deployment["id"],
                        robot_slot=slot,
                        request_id=request["request_id"],
                        sequence=request["sequence"],
                    )
                if result.get("status") == "pending":
                    raise RuntimeError(
                        f"robot {slot} remains fenced; resolve request {request['request_id']}"
                    )
                if result.get("status") == "failed":
                    raise RuntimeError(
                        f"robot {slot} request did not execute: {result['error']['code']}"
                    )
                if (result["sequence"], result["episode_id"]) != (
                    request["sequence"],
                    request["episode_id"],
                ):
                    raise ValueError("recovered result belongs to a different sequence/episode")
                completed += 1
                requests.append(
                    {"request_id": request["request_id"], "sequence": request["sequence"]}
                )
                for action in result["actions"]:
                    obs, done = env.step(action)
                    simulator_steps += 1
                    if done:
                        break
                if done:
                    break
        return {
            "robot_slot": slot,
            "task_suite": "libero_spatial",
            "task_id": slot,
            "seed": 197 + slot,
            "episode_id": episode_id,
            "completed_requests": completed,
            "requests": requests,
            "simulator_steps": simulator_steps,
            "task_done": done,
        }
    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-api", help="Override the saved Dreamscale control-plane origin")
    parser.add_argument("--deployment-id", required=True)
    parser.add_argument("--calls-per-robot", type=int, choices=range(1, 21), default=1)
    parser.add_argument("--start-sequence", type=int, required=True)
    parser.add_argument("--execute-approved", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.start_sequence <= 2**63 - 21:
        parser.error("start sequence must leave room for all requests")
    if not args.execute_approved:
        parser.error("requires an already funded allocation and --execute-approved")
    with InferenceClient(
        api_key=_api_key(), api_base=args.control_api
    ) as cp:
        deployment = cp.deployment(args.deployment_id)
    if deployment["status"] != "ready" or deployment["ready_robots"] < 8:
        parser.error("wait for eight qualified ready slots before running the example")
    # Separate simulator processes avoid sharing an OpenGL/MuJoCo context.
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=8, mp_context=multiprocessing.get_context("spawn")
    ) as pool:
        futures = [
            pool.submit(run_robot, slot, deployment, args.calls_per_robot, args.start_sequence)
            for slot in range(8)
        ]
        print(json.dumps([future.result() for future in futures]))


if __name__ == "__main__":
    main()
