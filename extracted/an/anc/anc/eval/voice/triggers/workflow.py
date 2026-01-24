import os
import time

from ...utils import invoke_evaluation_service, collect_specific_repos
from ...utils import rank_zero_only

# TODO: implement this
class AncOmniCompassEvalTrigger():
    def __init__(self,
                 project,
                 seq_length,
                 save_path,
                 model_name,
                 tokenizer_path,
                 anc_omni_git_commit,
                 compass_git_commit,
                 eval_mode,
                 wandb_project,
                 wandb_api_key,
                 tp=1,
                 pp=1):
        self.project = project
        self.tp = tp
        self.pp = pp
        self.seq_length = seq_length
        self.save_path = save_path
        self.model_name = model_name
        self.tokenizer_path = tokenizer_path
        self.anc_omni_git_commit = anc_omni_git_commit
        self.compass_git_commit = compass_git_commit
        self.eval_mode = eval_mode
        self.wandb_project = wandb_project
        self.wandb_api_key = wandb_api_key
        self.project_name = os.path.basename(os.path.normpath(self.save_path))
        self.anc_omni_git_commit = anc_omni_git_commit
        self.compass_git_commit = compass_git_commit
        self.eval_mode = eval_mode
        self.wandb_project = wandb_project

    def trigger(self, model_path, steps):
        """
        Trigger an evaluation by sending a POST request to the model management server.

        Args:
            model_path (str, optional): Override the model path. If None, uses args.model_path or checkpoint path
        """
        pass
        

class AncOmniHarnessEvalTrigger():
    def __init__(self, 
                 tasks, 
                 batch_size,
                 save_path,
                 model_name,
                 tokenizer_path,
                 seq_length,
                 wandb_project,
                 wandb_api_key,
                 anc_omni_git_commit,
                 harness_git_commit,
                 tp=1,
                 pp=1):
        
        self.project = "voice"
        self.tp = tp
        self.pp = pp
        self.seq_length = seq_length
        self.save_path = save_path
        self.model_name = model_name
        self.batch_size = batch_size
        self.cluster = os.getenv("MLP_CLUSTER", "va")
        self.project = os.getenv("MLP_PROJECT", "voice")
        self.tasks = tasks
        self.start_time = time.time()
        self.wandb_project = wandb_project
        self.wandb_api_key = wandb_api_key
        self.tokenizer_path = tokenizer_path
        self.project_name = os.path.basename(os.path.normpath(self.save_path))
        self.anc_omni_git_commit = anc_omni_git_commit
        self.harness_git_commit = harness_git_commit


    def trigger(self, model_path, steps):
        """
        Trigger an evaluation by sending a POST request to the model management server.

        Args:
            model_path (str, optional): Override the model path. If None, uses args.model_path or checkpoint path
        """
        # Allow override of model_path and version_name
        assert model_path is not None, "model_path is required"

        # Prepare the payload
        payload = {
            "project": self.project,
            "project_name": self.project_name,
            "model_name": self.model_name,
            "cluster": self.cluster,
            "eval_tp": self.tp,
            "eval_pp": self.pp,
            "eval_seqlen": self.seq_length,
            "eval_batch_size": self.batch_size,
            "eval_ckpt_list": [model_path],
            "eval_tasks": self.tasks,
            "eval_tokenizer_path": self.tokenizer_path,
            "project": "voice",
            "train_steps": steps,
            "code_info": {
                "ANC_OMNI": {
                    "commit": self.anc_omni_git_commit
                },
                "LM_EVALUATION_HARNESS": {
                    "commit": self.harness_git_commit
                }
            },
            "eval_mode": "harness",
        }

        if os.getenv("WANDB_MODE") != "disabled":
            payload["wandb_project"] = self.wandb_project
            payload["wandb_api_key"] = self.wandb_api_key

        print(f"auto eval harness trigger payload: {payload}")

        return invoke_evaluation_service(payload, "evaluations")


class AncOmniEvalTrigger():
    def __init__(self, 
                 anc_omni_eval_config, save_path, model_name, seq_length):
        self.triggers = []
        if anc_omni_eval_config.harness.enable:
            harness_trigger = AncOmniHarnessEvalTrigger(
                tasks="|".join(anc_omni_eval_config.harness.tasks),
                batch_size=anc_omni_eval_config.batch_size,
                save_path=save_path,
                model_name=model_name,
                tokenizer_path=anc_omni_eval_config.tokenizer_path,
                seq_length=seq_length,
                wandb_project=anc_omni_eval_config.wandb_project,
                wandb_api_key=anc_omni_eval_config.wandb_api_key,
                tp=anc_omni_eval_config.tensor_parallel_size,
                anc_omni_git_commit=anc_omni_eval_config.anc_omni_git_commit,
                harness_git_commit=anc_omni_eval_config.harness_git_commit,
            )
            self.triggers.append(harness_trigger)
        if anc_omni_eval_config.opencompass.enable:
            pass


    @rank_zero_only
    def trigger(self, model_path, steps):
        """
        Trigger an evaluation one by one.

        Args:
            model_path (str, optional): Override the model path. If None, uses args.model_path or checkpoint path
        """
        # Allow override of model_path and version_name
        assert model_path is not None, "model_path is required"

        for trigger in self.triggers:
            trigger.trigger(model_path, steps)
