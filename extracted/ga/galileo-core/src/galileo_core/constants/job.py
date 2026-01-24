from enum import Enum, unique


@unique
class JobStatus(str, Enum):
    unstarted = "unstarted"  # When the job is created but not yet started.
    in_progress = "in_progress"  # When the job is running.
    processed = "processed"  # When the job is processed and results are in the object store.
    completed = "completed"  # When the job is finished successfully.
    error = "error"  # When the job fails because of a user error.
    failed = "failed"  # When the job fails because of a system error.

    @staticmethod
    def is_incomplete(status: "JobStatus") -> bool:
        return status in [JobStatus.unstarted, JobStatus.in_progress]

    @staticmethod
    def is_failed(status: "JobStatus") -> bool:
        return status in [JobStatus.failed, JobStatus.error]


@unique
class JobName(str, Enum):
    """
    Function name for runners entrypoint.

    For background jobs submitted to runners, the JobName dictate to the service runners which functions should be run.
    See 'BaseVaexService.run()' for more information.
    """

    default = "default"
    inference = "inference"
    lykos_migration = "lykos_migration"
    monitor_run = "monitor_run"
    monitor_scorer = "monitor_scorer"
    prompt_chain_run = "prompt_chain_run"
    prompt_optimization = "prompt_optimization"
    prompt_rater = "prompt_rater"
    prompt_run = "prompt_run"
    prompt_scorer = "prompt_scorer"
    protect_scorer = "protect_scorer"
    registered_scorer_validation = "registered_scorer_validation"
    metric_critique = "metric_critique"
    auto_gen = "auto_gen"
    generated_scorer_validation = "generated_scorer_validation"
    log_record_generated_scorer_validation = "log_record_generated_scorer_validation"
    log_record_registered_scorer_validation = "log_record_registered_scorer_validation"
    log_stream_run = "log_stream_run"
    playground_run = "playground_run"
    log_stream_scorer = "log_stream_scorer"
    synthetic_datagen = "synthetic_datagen"
    logstream_insights = "logstream_insights"
    auto_metric_suggestion = "auto_metric_suggestion"
