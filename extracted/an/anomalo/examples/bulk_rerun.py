# Example usage: $ python www/api_client/bulk_rerun.py --table "public.fact_listing" --warehouse_id 129 --start "2021-06-01" --end "2021-06-03" --days_of_month_to_skip [1,2,3]
# --start / --end are [inclusive, exclusive)
# --end, --days_of_month_to_skip are optional

import datetime
import time

import dateutil.parser
import fire
import tqdm

import anomalo


ML_CHECKS = {
    "MLTime": -100,
    "MLNull": -101,
}
ANALYZE_CHECKS = {"ANALYZE_SAMPLE": -103}

DEFAULT_DAYS_OF_MONTH_TO_SKIP = [1, 7, 14, 21, 28, 29, 30, 31]

api_client = anomalo.Client()


# Run checks against table for all completed intervals from "start" to "end" (defaults to now)
def _run_checks_sync(table_id, interval_id=None, check_ids=None):
    run_resp = api_client.run_checks(
        table_id, interval_id=interval_id, check_ids=check_ids
    )
    job_id = run_resp["run_checks_job_id"]

    results_resp = None
    all_finished = False
    while not all_finished:
        results_resp = api_client.get_run_result(job_id)
        all_finished = all(not r["results_pending"] for r in results_resp["check_runs"])
        if not all_finished:
            time.sleep(15)
    return results_resp


def _rerun_checks(
    warehouse_id,
    table_name,
    start,
    end=None,
    days_of_month_to_skip=DEFAULT_DAYS_OF_MONTH_TO_SKIP,
):
    if not end:
        end = datetime.datetime.now().strftime("%Y-%m-%d")  # noqa: DTZ005 (call-datetime-now-without-tzinfo)
    info = api_client.get_table_information(
        warehouse_id=warehouse_id, table_name=table_name
    )
    table_id = info["id"]

    # Get intervals by date
    interval_data = api_client.get_check_intervals(
        table_id=table_id, start=start, end=end
    )
    for interval_dict in interval_data:
        interval_dict["start"] = dateutil.parser.parse(
            interval_dict["time_period_start"]
        )
        interval_dict["end"] = dateutil.parser.parse(interval_dict["time_period_end"])

    interval_data.sort(key=lambda i: i["start"])

    for interval_dict in tqdm.tqdm(interval_data):
        interval_start = interval_dict["start"]
        start_str = interval_start.strftime("%Y-%m-%d")

        if interval_start.day in days_of_month_to_skip:
            print(f"Skipping checks for {table_name} on {start_str}")
            continue

        # Run checks
        print(f"Running checks for {table_name} on {start_str}")
        interval_id = interval_dict["interval_id"]
        results_resp = _run_checks_sync(
            table_id, interval_id=interval_id, check_ids=list(ML_CHECKS.values())
        )
        errored_runs = [
            r for r in results_resp["check_runs"] if r.get("results", {}).get("errored")
        ]
        if len(errored_runs) > 0:
            for run in errored_runs:
                print("Encountered error:")
                print(run["results"]["exception_traceback"])
                print("Check details:")
                print(run)
            raise RuntimeError(
                f"Halting due to error; Resolve the error and re-run starting at {start_str}"
            )
        print(f"Checks finished for {table_name} on {start_str}")

    # Run analyze check for the final date
    last_interval = interval_data[-1]
    _run_checks_sync(
        table_id,
        interval_id=last_interval["interval_id"],
        check_ids=list(ANALYZE_CHECKS.values()),
    )


def run_backfill(
    table=None,
    warehouse_id=None,
    start=None,
    end=None,
    days_of_month_to_skip=DEFAULT_DAYS_OF_MONTH_TO_SKIP,
):
    _rerun_checks(
        warehouse_id,
        table,
        start,
        end=end,
        days_of_month_to_skip=days_of_month_to_skip,
    )


fire.Fire(run_backfill)
