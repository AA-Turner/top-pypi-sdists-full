#!/usr/bin/env python3
import json
import subprocess

from datetime import datetime, timedelta
from dateutil.tz import tzutc
from dateutil.parser import parse as date_parser

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

data = {}


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def get_docker_container_ids():
    container_ids = []
    process = subprocess.Popen(["docker", "ps", "--format='{{json .}}'"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    line_items = process.stdout.read().strip().split(b"\n")
    for element in line_items:
        element = element.decode().strip()[1:-1]
        if not element:
            continue
        metadata = json.loads(element)
        container_ids.append(metadata['ID'])
    return container_ids


def get_a_running_command(container_id: str):
    process = subprocess.Popen(["docker", "top", container_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line_items = process.stdout.read().strip().split(b"\n")
    data["all_commands"] = []
    for element in line_items[1:]:
        command = element.split()[7:]
        command = b" ".join(command)
        command = command.decode()
        data["all_commands"].append(command)
        executable_command = command.split()[0].lower().split('/')[-1]
        bash_like_commands = ["command", "ps", "bash", "fish", "sh", "tsh", "tini", "zsh"]
        if executable_command not in bash_like_commands and 'jupyter-lab' not in command and 'ipykernel_launcher' not in command and "<defunct>" not in command:
            data['running_command'] = command
            return command
    return None


def get_least_idle_tty_time():
    current_time = datetime.now(tzutc())
    process = subprocess.Popen(["docker", "exec", container_id, "ls", "/dev/pts"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    pseudo_terminals = process.stdout.read().decode('utf8').strip().split()
    data['pts_all'] = pseudo_terminals
    pseudo_terminals = [x for x in pseudo_terminals if x[0].isdigit()]
    least_idle_time_seconds = 60 * 60 * 24 * 365  # 1 year
    data['pts_timestamp_messages'] = []
    data['pts_last_seen_messages'] = []
    for pseudo_terminal in pseudo_terminals:
        process = subprocess.Popen(["docker", "exec", container_id, "stat", "/dev/pts/" + str(pseudo_terminal)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        line_items = process.stdout.read().strip().split(b"\n")

        for element in line_items:
            element = element.decode()
            accessors = element.split()
            if accessors[0] in ["Access:", "Modify:", "Change:"] and len(accessors) == 4:
                pts_timestamp_msg = "PTS %s was last %s at %s %s %s" % (
                    pseudo_terminal, accessors[0], accessors[1], accessors[2], accessors[3])
                data['pts_timestamp_messages'].append(pts_timestamp_msg)
                last_accessed_time = date_parser(accessors[1] + " " + accessors[2] + " " + accessors[3])
                idle_time_seconds = (current_time - last_accessed_time).total_seconds()
                data['pts_last_seen_messages'].append("TTY activity last seen %s ago" % display_time(idle_time_seconds))
                if idle_time_seconds < least_idle_time_seconds:
                    least_idle_time_seconds = idle_time_seconds
    return least_idle_time_seconds


docker_container_ids = get_docker_container_ids()
data["container_ids"] = docker_container_ids

running_command = False
for container_id in docker_container_ids:
    running_command = get_a_running_command(container_id)
    has_running_command = True if running_command else False
    idle_time_seconds = get_least_idle_tty_time()

data["running_command"] = running_command
data["idle_time_seconds"] = idle_time_seconds
data["idle_time"] = display_time(idle_time_seconds)

print(json.dumps(data))
