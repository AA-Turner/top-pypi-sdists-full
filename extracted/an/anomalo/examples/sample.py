import time

import anomalo


# Expects ANOMALO_INSTANCE_HOST and ANOMALO_API_SECRET_TOKEN to hold the auth and connection info

# Start API client
api_client = anomalo.Client()

# Retrieve table information based on a fully qualified name
table = api_client.get_table_information(table_name="pg-local.public.main_dguser")

# Get ID for table and run it's checks/validations

table_id = table["id"]
run = api_client.run_checks(table_id=table_id)

# Get the results of the run -- waiting until all checks are completed (i.e. no logner pending)

run_checks_job_id = run["run_checks_job_id"]

while True:
    run_result = api_client.get_run_result(job_id=run_checks_job_id)

    num_pending_checks = sum(
        1 for c in run_result["check_runs"] if c["results_pending"]
    )

    if num_pending_checks == 0:
        break
    else:
        time.sleep(5)

# Collect checks that have passed and those that failed

passed_checks = [c for c in run_result["check_runs"] if c["results"]["success"]]
failed_checks = [c for c in run_result["check_runs"] if not c["results"]["success"]]

# Make some decision here or return some value based on the results. We just print status.

print(f"Number of Passed Checks: {len(passed_checks)}")
print(f"Numner of Failed Checks: {len(failed_checks)}")
