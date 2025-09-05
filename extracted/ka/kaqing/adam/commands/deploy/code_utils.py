import os
from pathlib import Path
import socket
import subprocess

from adam.apps import Apps
from adam.config import Config
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.services import Services
from adam.utils import log2, random_alphanumeric

def start_user_code(namespace: str):
    try:
        id = random_alphanumeric(8)
        port = get_available_port()
        name = f'ops-{port}-{id}'
        user = os.getenv('USER')
        base_path = f'/c3/c3/ops/code/{user}/{port}/{id}'
        host = Apps.app_host('c3', 'c3', namespace)
        Services.create_service(name, namespace, port, {"run": "ops"}, labels={
            'user': user
        })
        Ingresses.create_ingress(name, namespace, host, f'{base_path}/(.*)', port, annotations={
            'kubernetes.io/ingress.class': 'nginx',
            'nginx.ingress.kubernetes.io/use-regex': 'true',
            'nginx.ingress.kubernetes.io/rewrite-target': '/$1'
        }, labels={
            'user': user
        }, path_type='Prefix')
        # code-server --auth none --abs-proxy-base-path base_path $HOME
        code_cmd = f'code-server --auth none --bind-addr 0.0.0.0:{port} --abs-proxy-base-path {base_path} {Path.home()}'
        log2(code_cmd)
        log2(f'* vscode is available at https://{host}{base_path}/ *')
        os.system(code_cmd)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        if e.status == 409:
            log2(f"Error: '{name}' already exists in namespace '{namespace}'.")
        else:
            log2(f"Error creating ingress or service: {e}")

def stop_user_codes(namespace: str, dry=False):
    user = os.getenv("USER")
    label_selector=f'user={user}'
    Ingresses.delete_ingresses(namespace, label_selector=label_selector, dry=dry)
    Services.delete_services(namespace, label_selector=label_selector, dry=dry)

    pattern = f'/c3/c3/ops/code/{user}/'
    kill_process_by_pattern(pattern, dry=dry)

def kill_process_by_pattern(pattern, dry=False):
    try:
        # Find PIDs of processes matching the pattern, excluding the grep process itself
        command = f"ps aux | grep '{pattern}' | grep -v 'grep' | awk '{{print $2}}'"
        process = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        pids = process.stdout.strip().split('\n')

        if not pids or pids == ['']:
            Config().debug(f"No processes found matching pattern: '{pattern}'")
            return

        for pid in pids:
            if pid:
                try:
                    if not dry:
                        subprocess.run(f"kill -9 {pid}", shell=True, check=True)

                    Config().debug(f"Killed process with PID: {pid} (matching pattern: '{pattern}')")
                except subprocess.CalledProcessError as e:
                    log2(f"Error killing process {pid}: {e}")

    except subprocess.CalledProcessError as e:
        log2(f"Error finding processes: {e}")
    except Exception as e:
        log2(f"An unexpected error occurred: {e}")

def get_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))  # Bind to localhost and let OS assign a free port
        return s.getsockname()[1]  # Return the assigned port number