import glob
import os
from tempfile import TemporaryDirectory

from transformers import (
    Trainer,
    TrainerCallback,
    TrainerControl,
    TrainerState,
    TrainingArguments,
)

from vessl.internal import api
from vessl.internal import hyperparameters as hp
from vessl.internal import log
from vessl.model import create_model, upload_model_volume_file
from vessl.util import logger

# keys which are in summary logs
SUMMARY_KEYS = {
    "train_runtime",
    "train_samples_per_second",
    "train_steps_per_second",
    "train_loss",
    "total_flos",
}


class VesslCallback(TrainerCallback):
    """
    A [`TrainerCallback`] that logs metrics, media, model checkpoints to [VESSL AI](https://vessl.ai/).

    Args:
        access_token(str): Access token to override. Defaults to
                `access_token` from `~/.vessl/config`.
        organization_name(str): Organization name to override. Defaults to
                `organization_name` from `~/.vessl/config`.
        project_name(str): Project name to override. Defaults to
            `project name` from `~/.vessl/config`.
        credentials_file(str): Defaults to None.
        force_update_access_token(bool): True if force update access token,
            False otherwise. Defaults to False.
        upload_model(bool): True if upload model after training finishes. Defaults to False.
        repository_name(str): Repository name to upload model. If it is None but upload_model is True,
            raise an exception. Defaults to None.
    """

    def __init__(
        self,
        access_token: str = None,
        organization_name: str = None,
        project_name: str = None,
        credentials_file: str = None,
        force_update_access_token: bool = False,
        upload_model: bool = False,
        repository_name: str = None,
    ) -> None:
        api.configure(
            access_token=access_token,
            organization_name=organization_name,
            project_name=project_name,
            credentials_file=credentials_file,
            force_update_access_token=force_update_access_token,
        )

        self.upload_model = upload_model
        self.repository_name = repository_name

        if self.upload_model and self.repository_name is None:
            raise ValueError("You must specify the repository name when you want to upload model")

    def on_log(
        self,
        args: "TrainingArguments",
        state: "TrainerState",
        control: "TrainerControl",
        logs: dict[str, float] = None,
        **kwargs,
    ) -> None:
        # log metrics in the main process only
        if state.is_world_process_zero:
            # if the current step is the max step, and the summary keys are subset of log keys, just skip logging.
            # It is summary log and it will be handled in on_train_end logs
            log_keys = set(logs.keys())
            if state.max_steps != state.global_step or not SUMMARY_KEYS.issubset(log_keys):
                log(payload=logs, step=state.global_step)

    def on_train_end(
        self, args: "TrainingArguments", state: "TrainerState", control: "TrainerControl", **kwargs
    ):
        """Clean up experiment and upload final model when training ends"""
        if state.is_world_process_zero:
            # get the last log and if it contains train stats such as train_runtime, train_steps_per_seconds, etc,
            # log to hyperparameter section
            summary_log = state.log_history[-1]
            if api.is_in_run_exec_context():
                for k in summary_log.keys():
                    print(f"{k}: {summary_log[k]}")
            else:
                hp.update(summary_log)

            if self.upload_model:
                with TemporaryDirectory() as temp_dir:
                    temp_trainer = Trainer(
                        args=args, model=kwargs.get("model"), tokenizer=kwargs.get("tokenizer")
                    )
                    temp_trainer.save_model(temp_dir)

                    response = create_model(self.repository_name)
                    if response is None:
                        # if model has not been created successfully, the function returns None
                        logger.exception("There was an error while creating model")
                    else:
                        model_number = response.number
                        for file_path in glob.glob(f"{temp_dir}/*"):
                            upload_model_volume_file(
                                self.repository_name,
                                model_number,
                                file_path,
                                os.path.basename(file_path),
                            )
