import tempfile
import time
from pathlib import Path
from uuid import UUID

import pytest

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import JobNames, RuntimeConfig, TaskRequest
from edison_client.models.data_storage_methods import RawFetchResponse

pytestmark = [pytest.mark.live, pytest.mark.live_agent]


@pytest.mark.timeout(420)
def test_upload_and_run_analysis_task(admin_client: RestClient):
    """Test uploading a file with prompt, running analysis task, and downloading outputs."""
    prompt_content = "draw a blue square"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", encoding="utf-8"
    ) as temp_file:
        temp_file.write(prompt_content)
        temp_file.flush()
        temp_file_path = Path(temp_file.name)

        data_entry_uri = admin_client.upload_file(
            file_path=temp_file_path,
            name="blue_square_prompt",
            description="A prompt to draw a blue square",
        )

        # Verify the upload by extracting the ID and fetching
        data_storage_id = data_entry_uri.split(":", 1)[1]
        fetch_response = admin_client.fetch_data_from_storage(UUID(data_storage_id))
        assert isinstance(fetch_response, RawFetchResponse)
        assert fetch_response.content == prompt_content

        task_request = TaskRequest(
            name=JobNames.ANALYSIS,  # Use the data analysis crow
            query="Open the attached file and follow the instructions in it. Create an image as specified.",
            runtime_config=RuntimeConfig(
                timeout=180,
            ),
        )

        results = admin_client.run_tasks_until_done(
            task_data=task_request,
            files=[data_entry_uri],  # Simple file attachment!
            verbose=True,
            progress_bar=True,
            timeout=300,
        )

        assert len(results) == 1
        task_result = results[0]
        print(f"\nTrajectory ID: {task_result.task_id}, status: {task_result.status}")

        # Verify task completed successfully before checking for files
        assert task_result.status == "success", (
            f"Task did not complete successfully. Status: {task_result.status}. "
            f"Task ID: {task_result.task_id}"
        )

        # Add retry logic for listing files to handle eventual consistency
        # in the provenance system
        max_retries = 5
        retry_delay = 2  # seconds
        output_files = None

        for attempt in range(max_retries):
            output_files = admin_client.list_files(str(task_result.task_id))
            if len(output_files.get("data", [])) > 0:
                break
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        assert output_files is not None, "Failed to retrieve output files"
        assert len(output_files.get("data", [])) > 0, (
            f"Task completed successfully but created no output files. "
            f"Task ID: {task_result.task_id}, Status: {task_result.status}"
        )

        with tempfile.TemporaryDirectory() as output_dir:
            for file_entry in output_files["data"]:
                data_storage = file_entry["data_storage"]
                file_id = data_storage["id"]

                result = admin_client.fetch_data_from_storage(UUID(file_id))

                # Save the file content
                if isinstance(result, RawFetchResponse):
                    downloaded_path = Path(output_dir) / (
                        result.filename.name if result.filename else result.entry_name
                    )
                    downloaded_path.write_text(result.content)
                elif isinstance(result, Path):
                    downloaded_path = result
                else:
                    raise TypeError(f"Unexpected result type: {type(result)}")

                assert downloaded_path.exists()
                assert downloaded_path.stat().st_size > 0

        # Clean up the uploaded input file
        admin_client.delete_data_storage_entry(UUID(data_storage_id))
