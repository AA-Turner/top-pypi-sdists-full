from typing import Tuple

from qwak.inner.build_config.build_config_v1 import BuildConfigV1
from qwak.inner.build_logic.interface.build_phase import BuildPhase
from qwak.inner.build_logic.phases.phases_pipeline import PhasesPipeline
from qwak.inner.build_logic.trigger_build_context import TriggerBuildContext

from .client_logs.messages import SUCCESS_MSG_REMOTE_WITH_DEPLOY, SUCCESS_MSG_REMOTE
from .phase.a_fetch_model_code import get_fetch_model_code_steps
from .phase.b_remote_register_qwak_build import get_remote_register_qwak_build_steps
from .phase.c_deploy import get_deploy_steps


def remote_build_steps(config: BuildConfigV1) -> PhasesPipeline:
    steps_root = PhasesPipeline(config=config, context=TriggerBuildContext())
    steps_root.add_phase(
        steps=get_fetch_model_code_steps(),
        build_phase=BuildPhase(phase_id="FETCHING_MODEL_CODE"),
    )
    steps_root.add_phase(
        steps=get_remote_register_qwak_build_steps(),
        build_phase=BuildPhase(phase_id="REGISTERING_QWAK_BUILD"),
    )

    if config.deploy:
        steps_root.add_phase(
            steps=get_deploy_steps(),
            build_phase=BuildPhase(phase_id="DEPLOYING_PHASE", name="Deploying", description="Deploying"),
        )

    return steps_root


def create_pipeline(
    config: BuildConfigV1,
) -> Tuple[PhasesPipeline, str]:
    success_message = (
        SUCCESS_MSG_REMOTE_WITH_DEPLOY if config.deploy else SUCCESS_MSG_REMOTE
    )
    pipeline = remote_build_steps(config)

    return pipeline, success_message
