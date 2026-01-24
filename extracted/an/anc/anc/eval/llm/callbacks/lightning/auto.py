from pathlib import PosixPath

# external imports, we don't want to import them when anc cli is installed
try:
    from lightning.pytorch.callbacks import Callback
    from lightning.pytorch.callbacks import ModelCheckpoint
    from lightning.fabric.utilities.rank_zero import rank_zero_only
    
    #from nemo.scripts.a7n.a7n_monitors import DirectTFLOPSMonitor
except:
    pass

from ....utils import rank0_print
from ...triggers.workflow import AutoEvaluationWorkflowTrigger


class AutoEvaluationCallback(Callback):
    """
    Callback for triggering evaluation pipeline at specified training step intervals.

    This callback tracks training progress and triggers evaluation pipeline
    every stride_steps_eval steps. When the interval is reached, it evaluates
    the current checkpoint.

    Args:
        args: Arguments object containing stride_steps_eval and other configuration

    Example usage:
        # If stride_steps_eval = 100
        # Training steps: 50, 100, 150, 200, 250, 300...
        # 
        # Evaluation will be triggered:
        # - At step 100 -> evaluate current checkpoint
        # - At step 200 -> evaluate current checkpoint  
        # - At step 300 -> evaluate current checkpoint
        # 
        # This provides regular evaluation intervals based on training progress.

    Configuration:
        args.stride_steps_eval (int): Interval for step-based evaluation
            - If None or 0: Only evaluate at training end
            - If > 0: Evaluate every N steps (using the current checkpoint)
    """

    def __init__(self, args, target_callback_type, code_info=None):
        super().__init__()
        self.workflow_trigger = AutoEvaluationWorkflowTrigger(args, code_info=code_info)
        self.stride_steps_eval = getattr(args, 'stride_steps_eval', None)
        self.checkpoint_list = []
        self.checkpoint_count = 0
        self.evaluated_checkpoints = set()
        self.target_callback_type = target_callback_type

        rank0_print(
            f"AutoEvaluationCallback initialized with stride_steps_eval={self.stride_steps_eval}")
        if self.stride_steps_eval and self.stride_steps_eval > 0:
            rank0_print(
                f"Will evaluate every {self.stride_steps_eval} steps using the current checkpoint")
            rank0_print(
                f"Evaluation trigger: when global steps % {self.stride_steps_eval} == 0")
            rank0_print(f"Final checkpoint will always be evaluated regardless of stride")
        else:
            rank0_print("Evaluation will only be triggered at training end")

    @rank_zero_only
    def on_save_checkpoint(self, trainer, pl_module, checkpoint):
        if self.stride_steps_eval is None or self.stride_steps_eval == 0:
            return

        checkpoint_cb = next(
            (cb for cb in trainer.callbacks if isinstance(cb, ModelCheckpoint)),
            None
        )

        if checkpoint_cb is None:
            rank0_print("Warning: No ModelCheckpoint callback found.")
            return

        best_k_models = trainer.checkpoint_callback.best_k_models
        last_model_path = checkpoint_cb.last_model_path
        expected_ckpt_step_keyword = '_' + 'step=' + \
            str(trainer.global_step-1) + '_'  # e.g. _step=800_
        # For resume case, if save last == 'link', here last_model_path is not the latest checkpoint.
        # We need to find the latest checkpoint from best_k_models.
        if isinstance(last_model_path, PosixPath):
            last_model_path = str(last_model_path)
        if expected_ckpt_step_keyword not in last_model_path:
            for path in best_k_models.keys():
                if expected_ckpt_step_keyword in path:
                    rank0_print(
                        f"find the latest checkpoint from best_k_models: {path}")
                    last_model_path = path
                    break

        if last_model_path:
            if last_model_path.endswith(".ckpt"):
                last_model_path = last_model_path.replace(".ckpt", "")

            clean_ckpt_path = last_model_path
            if last_model_path.endswith('-last'):
                clean_ckpt_path = last_model_path[:-5]

            if clean_ckpt_path in self.checkpoint_list:
                rank0_print(
                    f"Checkpoint already processed, skipping: {clean_ckpt_path}")
                return

            self.checkpoint_list.append(clean_ckpt_path)
            self.checkpoint_count += 1
            if trainer.global_step % self.stride_steps_eval == 0:
                target_ckpt = clean_ckpt_path
                rank0_print(
                    f"Scheduling evaluation for current checkpoint (#{self.checkpoint_count}): {target_ckpt}")
                self.evaluated_checkpoints.add(clean_ckpt_path)
                self._schedule_evaluation_when_checkpoint_exists(
                    trainer, target_ckpt)
        else:
            rank0_print(
                f"Warning: No checkpoint found for step {trainer.global_step}")

    def _schedule_evaluation_when_checkpoint_exists(self, trainer, checkpoint_path):
        import threading
        import time
        import os

        def check_and_evaluate():
            max_wait_time = 600
            check_interval = 5
            waited_time = 0

            rank0_print(
                f"Background thread: Waiting for checkpoint to exist: {checkpoint_path}")

            while waited_time < max_wait_time:
                try:
                    checkpoint_exists = False

                    if os.path.isdir(checkpoint_path):
                        checkpoint_exists = True

                    if checkpoint_exists:
                        rank0_print(
                            f"Background thread: Checkpoint verified, triggering evaluation: {checkpoint_path}")
                        self._trigger_evaluation(trainer, checkpoint_path)
                        return
                    else:
                        rank0_print(
                            f"Background thread: Checked: {checkpoint_path}, {checkpoint_path}.ckpt, directory {checkpoint_path}")

                except Exception as e:
                    rank0_print(f"Background thread: Error checking checkpoint: {e}")

                time.sleep(check_interval)
                waited_time += check_interval

            rank0_print(
                f"Eval warning: timeout waiting for checkpoint, attempting evaluation anyway: {checkpoint_path}")
            self._trigger_evaluation(trainer, checkpoint_path)

        check_thread = threading.Thread(target=check_and_evaluate, daemon=True)
        check_thread.start()
        rank0_print(
            f"Started background thread to monitor checkpoint: {checkpoint_path}")

    def _trigger_evaluation(self, trainer, checkpoint_path):
        try:
            tflops_monitor = next(
                (cb for cb in trainer.callbacks if isinstance(
                    cb, self.target_callback_type)),  
                None
            )

            metrics = {"avg_tflops": 0.0, "avg_mfu": 0.0, "steps": 0}
            if tflops_monitor:
                metrics = tflops_monitor.get_performance_metrics()
                rank0_print(f"Performance metrics for checkpoint {checkpoint_path}: "
                      f"Avg TFLOPS={metrics['avg_tflops']:.2f}, "
                      f"Avg MFU={metrics['avg_mfu']:.4f}, "
                      f"Steps={metrics['steps']}")

            response = self.workflow_trigger.trigger(
                checkpoint_path,
                metrics.get('avg_tflops', 0.0),
                metrics.get('avg_mfu', 0.0),
                metrics.get('steps', 0)
            )
            rank0_print(
                f"Evaluation triggered successfully for {checkpoint_path}. Response: {response}")

        except Exception as e:
            rank0_print(f"Failed to trigger evaluation for {checkpoint_path}: {e}")

    @rank_zero_only
    def on_train_end(self, trainer, pl_module):
        """Get the final checkpoint path at the end of training"""
        # Find ModelCheckpoint callback
        checkpoint_cb = next(
            (cb for cb in trainer.callbacks if isinstance(cb, ModelCheckpoint)),
            None
        )
        rank0_print(f"checkpoint_cb: {checkpoint_cb}")
        if checkpoint_cb is None:
            rank0_print(
                "Warning: No ModelCheckpoint callback found. Cannot retrieve checkpoint.")
            return

        last_ckpt = checkpoint_cb.last_model_path

        if not last_ckpt:
            rank0_print("Warning: last_model_path is empty. No checkpoint was saved.")
            return

        if isinstance(last_ckpt, PosixPath):
            last_ckpt = str(last_ckpt)

        if last_ckpt.endswith(".ckpt"):
            last_ckpt = last_ckpt.replace(".ckpt", "")

        if last_ckpt.endswith('-last'):
            last_ckpt = last_ckpt[:-5]  # remove -last suffix
            rank0_print(f"Removed -last suffix from final checkpoint path")

        rank0_print(f"Final checkpoint path: {last_ckpt}")

        tflops_monitor = next(
            (cb for cb in trainer.callbacks if isinstance(cb, self.target_callback_type)),
            None
        )
        metrics = None

        if tflops_monitor:
            metrics = tflops_monitor.get_performance_metrics()
            avg_tflops = metrics['avg_tflops']
            avg_mfu = metrics['avg_mfu']
            steps = metrics['steps']
            rank0_print(
                f"Performance metrics: Avg TFLOPS={avg_tflops:.2f}, Avg MFU={avg_mfu:.4f}, Steps={steps}")

        if last_ckpt not in self.evaluated_checkpoints:
            rank0_print(
                f"Final checkpoint has not been evaluated yet, scheduling evaluation: {last_ckpt}")
            self.evaluated_checkpoints.add(last_ckpt)
            self._schedule_evaluation_when_checkpoint_exists(
                trainer, last_ckpt)
        else:
            rank0_print(
                f"Final checkpoint has already been scheduled for evaluation, skipping: {last_ckpt}")

    def get_final_checkpoint(self, trainer):
        """Utility method to get final checkpoint path anytime"""
        for callback in trainer.callbacks:
            if 'ModelCheckpoint' in callback.__class__.__name__:
                return {
                    "best_checkpoint": callback.best_model_path,
                    "last_checkpoint": callback.last_model_path,
                    "checkpoint_dir": callback.dirpath
                }
        return None

    def get_checkpoint_list(self):
        return self.checkpoint_list.copy()

    def get_checkpoint_count(self):
        return self.checkpoint_count
