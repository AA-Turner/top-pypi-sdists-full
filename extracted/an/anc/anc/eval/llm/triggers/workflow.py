import os
import time

import torch.distributed as dist

from ...utils import get_eval_ckpt_list, invoke_evaluation_service


class AutoEvaluationWorkflowTrigger():
    def __init__(self, 
                 args, 
                 code_info=None):
        self.project = args.eval_project
        self.project_name = args.project_name
        self.modality = args.eval_modality
        self.model_name = args.model_name
        self.cluster = os.getenv("MLP_CLUSTER", "va")
        self.project = os.getenv("MLP_PROJECT", "llm")
        self.train_data_type = args.data_type
        self.train_dataset_name = args.data_type
        self.train_tp = args.tp
        self.train_pp = args.pp
        self.train_cp = args.context_p
        self.train_ep = args.ep
        self.train_sp = args.enable_sp
        self.train_seqlen = args.seq_length
        self.train_batch_size = args.global_batch_size
        self.train_learning_rate = args.lr
        self.train_batch_size = args.global_batch_size
        self.train_tokenizer_path = args.tokenizer_path
        self.eval_tp = args.eval_tp
        self.eval_pp = args.eval_pp
        self.eval_cp = args.eval_cp
        self.eval_ep = args.eval_ep
        self.eval_sp = args.eval_sp
        self.eval_seqlen = args.seq_length  # keep the same as train_seqlen
        self.eval_batch_size = args.eval_batch_size
        self.eval_tokenizer_path = args.tokenizer_path
        # change to eval_dataset_list
        self.eval_dataset_list = get_eval_ckpt_list(
            args.eval_dataset_path, args.eval_dataset_list)
        self.eval_validation_batch_size = args.eval_validation_batch_size
        self.eval_tasks = args.eval_tasks
        self.start_time = time.time()
        self.wandb_project = args.wandb_project
        self.wandb_api_key = os.getenv("WANDB_API_KEY")
        self.inference_max_seq_length = args.inference_max_seq_length
        self.code_info = code_info
        print(f"code_info: {self.code_info}")
        self.train_dataset_name_str = args.dataset_name
        self.train_dataset_ratios_str = args.ds_ratios

    def get_job_url(self):
        # Split by "-master-" and take the first part
        master_addr = os.getenv("MASTER_ADDR", None)
        cluster = os.getenv("MLP_CLUSTER", None)

        def get_job_id(master_addr):
            if not master_addr:
                return None

            # Extract everything before the last "-master-" substring
            if "-master-" in master_addr:
                job_id = master_addr.split("-master-")[0]
                return job_id
            return master_addr
        if master_addr and cluster:
            job_id = get_job_id(master_addr)
            # https://va-mlp.anuttacon.com/console/dlc_job/job-yz8korktg6
            return f"https://{cluster}-mlp.anuttacon.com/console/dlc_job/{job_id}"
        return ""

    def trigger(self, model_path,  tflops, mfu, steps):
        """
        Trigger an evaluation by sending a POST request to the model management server.

        Args:
            model_path (str, optional): Override the model path. If None, uses args.model_path or checkpoint path
        """
        # Allow override of model_path and version_name
        assert model_path is not None, "model_path is required"
        world_size = dist.get_world_size()
        self.train_dp = world_size // (self.train_tp * self.train_pp)
        # Prepare the payload
        payload = {
            "project": self.project,
            "project_name": self.project_name,
            "modality": self.modality,
            "model_name": self.model_name,
            "cluster": self.cluster,
            "train_tp": self.train_tp,
            "train_pp": self.train_pp,
            "train_cp": self.train_cp,
            "train_dp": self.train_dp,
            "train_ep": self.train_ep,
            "train_sp": self.train_sp,
            "train_seqlen": self.train_seqlen,
            "train_batch_size": self.train_batch_size,
            "train_dataset_type": self.train_data_type,
            "train_dataset_name": self.train_dataset_name,
            "train_learning_rate": self.train_learning_rate,
            "train_tflops": tflops,
            "train_mfu": mfu,
            "train_tokenizer_path": self.train_tokenizer_path,
            "eval_tp": self.eval_tp,
            "eval_pp": self.eval_pp,
            "eval_cp": self.eval_cp,
            "eval_ep": self.eval_ep,
            "eval_sp": self.eval_sp, 
            "eval_seqlen": self.eval_seqlen,
            "eval_batch_size": self.eval_batch_size,
            "eval_ckpt_list": [model_path],
            "eval_dataset_list": self.eval_dataset_list,
            "eval_tasks": self.eval_tasks,
            "eval_tokenizer_path": self.eval_tokenizer_path if self.eval_tokenizer_path else self.train_tokenizer_path,
            "project": self.project,
            "train_steps": steps,
            "validation_batch_size": self.eval_validation_batch_size,
            "inference_max_seq_length": self.inference_max_seq_length,
            "code_info": self.code_info,
            "train_dataset_name_str": self.train_dataset_name_str,
            "train_dataset_ratios_str": self.train_dataset_ratios_str,
        }

        if os.getenv("WANDB_MODE") != "disabled":
            payload["wandb_project"] = self.wandb_project
            payload["wandb_api_key"] = self.wandb_api_key

        end_time = time.time()
        payload["train_job_url"] = self.get_job_url()
        payload["train_cost_time"] = round(
            (end_time - self.start_time) / 3600, 2)
        payload["finished_at"] = end_time

        return invoke_evaluation_service(payload, "evaluations")
