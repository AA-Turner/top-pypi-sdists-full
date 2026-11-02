from agentic_devtools.adapters.pull_request_threads import PullRequestThread


def test_thread_stores_normalized_fields() -> None:
    thread = PullRequestThread("1", "active", "file.py", 4, ())
    assert thread.file == "file.py"
