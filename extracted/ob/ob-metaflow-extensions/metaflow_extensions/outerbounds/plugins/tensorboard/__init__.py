import functools
from metaflow.decorators import StepDecorator


class TensorboardDecorator(StepDecorator):
    name = "tensorboard"
    defaults = {}

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        @functools.wraps(step_func)
        def tb_wrapper():
            import sys, os
            from metaflow import metaflow_config, current

            try:
                from torch.utils.tensorboard import SummaryWriter
            except:
                print(
                    "[@tensorboard] Torch and tensorboard not found - logging disabled!",
                    file=sys.stderr,
                )
                step_func()
            else:
                tb_root = os.path.join(metaflow_config.DATATOOLS_S3ROOT, "tb")
                pathspec = current.pathspec
                try:
                    log_dir = os.path.join(tb_root, current.project_flow_name, pathspec)
                except:
                    log_dir = os.path.join(tb_root, pathspec)
                comps = log_dir[len(tb_root) + 1 :].split("/")
                run_level = "/".join(comps[:-2])
                flow_level = "/".join(comps[:-3])

                print("[@tensorboard] -- INSPECTING RESULTS")
                print(
                    "[@tensorboard] -- Execute one of these commands on your workstation:"
                )
                print(f"[@tensorboard] Compare tasks of this run: obtb {run_level}")
                print(f"[@tensorboard] Compare across runs: obtb {flow_level}")
                writer = SummaryWriter(log_dir=log_dir)
                setattr(flow, "obtb", writer)
                try:
                    step_func()
                finally:
                    writer.flush()
                    delattr(flow, "obtb")

        return tb_wrapper
