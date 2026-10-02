from probe.cli.import_job_messages import enqueue_report


def test_running_job_is_reported_as_already_running():
    lines = enqueue_report({"id": "job", "state": "running"}, "Session import")
    assert lines[0] == "Session import already running: job"
    assert "Existing imports" in lines[1]


def test_interrupted_job_prompts_resume_in_existing_imports():
    lines = enqueue_report({"id": "job", "state": "interrupted"}, "Folder import")
    assert lines[0] == "Folder import interrupted: job"
    assert "Existing imports" in lines[-1] and "resume" in lines[-1]
