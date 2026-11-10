"""Miles' RL samples in Probe's sample store (front door; DESIGN.md): the rollout hooks, the train-rank
wraps and this process's producer handle."""

from probe.integrations.miles.samples.events import EventRecorder, install_event_recorder
from probe.integrations.miles.samples.producers import PROCESS, ROLLOUT, get_trainer_name
from probe.integrations.miles.samples.samples import (
    add_hook_arguments,
    log_dropped_samples,
    log_eval_samples,
    log_samples,
    make_log_samples,
)
from probe.integrations.miles.samples.trainer import TRAINER, find_new_checkpoint, record_checkpoint
from probe.integrations.miles.samples.wraps import install_worker_wraps

__all__ = [
    "PROCESS",
    "ROLLOUT",
    "TRAINER",
    "EventRecorder",
    "add_hook_arguments",
    "find_new_checkpoint",
    "get_trainer_name",
    "install_event_recorder",
    "install_worker_wraps",
    "log_dropped_samples",
    "log_eval_samples",
    "log_samples",
    "make_log_samples",
    "record_checkpoint",
]
