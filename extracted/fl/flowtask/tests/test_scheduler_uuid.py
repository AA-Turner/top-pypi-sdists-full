import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from flowtask.scheduler.functions import TaskScheduler

@pytest.fixture
def mock_worker():
    worker = MagicMock()
    # Mock the QClient or queue interface
    worker.queue = AsyncMock(return_value={"message": "ok"})
    worker.publish = AsyncMock(return_value={"message": "ok"})
    worker.run = AsyncMock(return_value={"message": "ok"})
    return worker

@pytest.fixture
def scheduler(mock_worker):
    return TaskScheduler(
        program="test_program",
        task="test_task",
        job_id="test_job_001",
        priority="low",
        worker=mock_worker,
    )

class TestTaskSchedulerUUID:
    def test_consecutive_calls_produce_unique_ids(self, scheduler):
        """Each _create_wrapper() call must generate a distinct UUID."""
        # Create 10 wrappers consecutively
        wrappers = [scheduler._create_wrapper() for _ in range(10)]
        ids = {w.id for w in wrappers}
        # If all 10 are unique, the set length will be 10
        assert len(ids) == 10, "Wrapper IDs must be unique across creations"

    def test_wrapper_recreated_per_call(self, scheduler):
        """Each _create_wrapper() returns a NEW TaskWrapper instance."""
        w1 = scheduler._create_wrapper()
        w2 = scheduler._create_wrapper()
        assert w1 is not w2, "TaskWrapper must be a new instance"
        assert w1.id != w2.id, "TaskWrapper IDs must differ"

    @patch("flowtask.scheduler.functions.TaskScheduler.save_task_id", new_callable=AsyncMock)
    def test_scheduler_dispatch_unique_ids(self, mock_save, scheduler):
        """Simulates multiple scheduler triggers and verifies unique IDs in dispatch."""
        collected_ids = []

        # We patch the internal _schedule_task method to capture the wrapper it receives
        async def capture_schedule(wrapper, worker):
            collected_ids.append(wrapper.id)
            return {"message": "ok"}
        
        # Override the bound method for this instance
        scheduler._schedule_task = capture_schedule

        # Trigger the scheduler 5 times as APScheduler would
        for _ in range(5):
            scheduler()

        assert len(set(collected_ids)) == 5, "Every dispatch must use a unique wrapper ID"
