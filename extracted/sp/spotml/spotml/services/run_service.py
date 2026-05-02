import logging
import os
from datetime import datetime

import boto3 as boto3
import requests as requests
from tabulate import tabulate
from dateutil import parser
from tzlocal import get_localzone

from spotml.config.config_utils import DEFAULT_CONFIG_FILENAME
from spotml.config.url import API_URL
from spotml.constants.constants import GENERIC_ERROR_MESSAGE


def get_local_time_from_string(utc_date_time_string):
    return parser.parse(utc_date_time_string).astimezone(get_localzone()).strftime('%b %d, %Y -%l:%M%p %Z')


def update_run_status(run_id, status):
    logging.info(f'Updating Run status to: {status}')
    r = requests.patch(f'{API_URL}/run/{run_id}',
                       data={'status': status, 'aws_batch_job_id': os.getenv('AWS_BATCH_JOB_ID')})
    if r.status_code != 201:
        print("Oops, looks like something went wrong in scheduling the run")
        print(GENERIC_ERROR_MESSAGE)
        raise Exception('Something went wrong updating Run Status', r)


def get_run(run_id):
    r = requests.get(f'{API_URL}/run/{run_id}')
    if r.status_code != 200:
        raise RuntimeError('Unable to get run metadata.')
    return r.json()


def print_run_status(should_print_logs: bool):
    session = boto3.session.Session()
    credentials = session.get_credentials()
    region = session.region_name
    access_key = credentials.access_key
    secret_key = credentials.secret_key

    with open(DEFAULT_CONFIG_FILENAME, 'r') as spotYml:
        files = {'spotml_config': spotYml}
        r = requests.get(f'{API_URL}/run/status', files=files,
                         data={'region': region, 'access_key': access_key,
                               'secret_key': secret_key})
        if r.status_code == 200:
            runs = r.json()['runs']
            multiple_job_logs = r.json()['logs']
            if len(runs) > 0:
                table = []
                for run in runs:
                    table.append(
                        [run['id'], run['script_name'], run['status'], get_local_time_from_string(run['created_date'])])
                print(tabulate(table, headers=['Run Id', 'Command', 'Status', 'Start Time'], tablefmt="psql"))
            else:
                print("No Active Runs")

            if should_print_logs:
                print_run_logs(multiple_job_logs)

        else:
            print("Sorry, Failed to get latest status runs.")
            print(GENERIC_ERROR_MESSAGE)


def print_run_logs(multiple_job_logs):
    print("\nLAST RUN LOGS: ")
    if len(multiple_job_logs) > 0:
        for job_log in multiple_job_logs:
            table = []
            for log in job_log:
                table.append(
                    [datetime.fromtimestamp(log['timestamp'] / 1000).strftime('%b %d, %Y -%l:%M%p %Z'),
                     log['message']])
            print(tabulate(table, headers=['Time', 'Log Text'], tablefmt="psql"))
    else:
        print("Nothing so far... \n")


def track_instance_start(ssh_key_path):
    session = boto3.session.Session()
    credentials = session.get_credentials()
    region = session.region_name
    access_key = credentials.access_key
    secret_key = credentials.secret_key

    with open(ssh_key_path, 'r') as sshKey:
        with open(DEFAULT_CONFIG_FILENAME, 'r') as spotYml:
            files = {'spotml_config': spotYml, 'ssh_key': sshKey}
            r = requests.post(f'{API_URL}/run/track-instance-start', files=files,
                              data={'region': region, 'access_key': access_key,
                                    'secret_key': secret_key})
            if r.status_code == 200:
                old_runs = r.json()['old_runs']
                print_old_runs(old_runs)
                print("\nTracking instance uptime now.\n")
            else:
                print("Failed to stop existing runs. Use \"spotml status%s\" command to check the status of runs.")
                print("\nOops, Unable to start track instance uptime.\n")
                print(GENERIC_ERROR_MESSAGE)


def track_instance_stop():
    session = boto3.session.Session()
    credentials = session.get_credentials()
    region = session.region_name
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    with open(DEFAULT_CONFIG_FILENAME, 'r') as spotYml:
        files = {'spotml_config': spotYml}
        r = requests.post(f'{API_URL}/run/track-instance-stop', files=files,
                          data={'region': region, 'access_key': access_key,
                                'secret_key': secret_key})

        if r.status_code == 200:
            old_runs = r.json()['old_runs']
            print_old_runs(old_runs)
            print("\nStopped tracking instance uptime.")
        else:
            print("\nOops, Unable to stop track instance uptime.")
            print(GENERIC_ERROR_MESSAGE)


def get_instance_tracking_status():
    session = boto3.session.Session()
    credentials = session.get_credentials()
    region = session.region_name
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    with open(DEFAULT_CONFIG_FILENAME, 'r') as spotYml:
        files = {'spotml_config': spotYml}
        r = requests.get(f'{API_URL}/instance/tracking-status', files=files,
                         data={'region': region, 'access_key': access_key,
                               'secret_key': secret_key})

        if r.status_code == 200:
            return r.json()['is_tracking_idle_time']
        else:
            return False


def print_old_runs(old_runs):
    if len(old_runs) > 0:
        print("\nStopped managing all active runs.")
        print("STOPPED RUNS")
        table = []
        for run in old_runs:
            table.append(
                [run['id'], run['script_name'], run['status'], get_local_time_from_string(run['created_date'])])
        print(tabulate(table, headers=['Run Id', 'Command', 'Status', 'Start Time'], tablefmt="psql"))
    else:
        print("\nNo active runs found.")
