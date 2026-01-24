from ..util import is_valid_source_path, get_file_or_folder_name, convert_to_absolute_path
from anc.conf.remote import remote_server, remote_storage_prefix, repo_url
from anc.api.connection import Connection
import subprocess
import os
import sys
import json
from requests.exceptions import RequestException
from tabulate import tabulate

from ..util import ConfigManager


class DatasetOperator:
    def __init__(self):
        self.conn = Connection(url=remote_server)
        self.config_manager = ConfigManager()

    def download_dataset(self, name, version, dest, cache_policy):
        git_commit_id = self.get_commit_id(name, version)
        if git_commit_id is None:
            print("Not found a git commit id for the dataset, can't do download.")
            return
        dest = os.path.abspath(dest)
        if remote_storage_prefix in dest:
            return self.remote_download(name, version, dest, cache_policy)
        self.local_download(git_commit_id, name, dest)

    # for training job use.
    def add_dataset(self, dataset_name, version, source_path, message):
        if remote_storage_prefix in source_path:
            return self.remote_add(dataset_name, version, source_path, message)
        self.local_add(dataset_name, version, source_path, message)

    def remote_add(self, version, source_path, message):
        project, cluster, peronsal = self.config_manager.get_environment()
        if not project or not cluster:
            print("Failed to add dataset, because in current enviroment cli can't identify your project or cluster, plz reach out infra team to setup")
            sys.exit(1)
        source_path = os.path.abspath(source_path)
        if not is_valid_source_path(source_path, peronsal):
            sys.exit(1)
        abs_path = convert_to_absolute_path(source_path)
        dataset_name = get_file_or_folder_name(abs_path)
        conn = Connection(url=remote_server)
        data = {
            "dataset_name": dataset_name,
            "version": version,
            "source_path": abs_path,
            "dest_path": "local",
            "project": project,
            'cluster': cluster,
            'personal': peronsal,
            "message": message
        }
        try:
            response = conn.post("/add", json=data)

            # Check if the status code is in the 2xx range
            if 200 <= response.status_code < 300:
                response_data = response.json()
                task_id = response_data.get('task_id')
                if task_id:
                    print(f"Task added successfully. Your task ID is: \033[92m{task_id}\033[0m")
                    print(f"You can check the status later by running:  \033[92manc ds list -n {dataset_name}\033[0m")
                    print(f"You can check the task status:  \033[92manc ds task status {task_id}\033[0m")
                    print(f"If your task has been pending a long time, please check the queue with: anc ds queue status")
                else:
                    print("Task added successfully, but no task ID was returned.")
            else:
                #print(f"Error: Server responded with status code {response.status_code}")
                print(f"{response.text}")
  
        except RequestException as e:
            print(f"Sorry, you can't add dataset out of clusters, please use it in a notebook")
        except json.JSONDecodeError:
            print("Sorry: received invalid JSON response from server")
        except KeyboardInterrupt:
            print(f"Operation interrupted.")
            sys.exit(0)
        except Exception as e:
            print(f"Sorry, your command run failed, you can try again or reach out infra team")

    # TODO
    def local_add(self, dataset_name, version, source_path, message):
        if os.getenv("AWS_ACCESS_KEY_ID", None) is None or os.getenv("AWS_SECRET_ACCESS_KEY", None) is None or os.getenv("GIT_TOKEN", None) is None:
            print("!!!! Hey, are you sure you want to upload it to remote? if yes, please set environment for <AWS_ACCESS_KEY_ID> and <AWS_SECRET_ACCESS_KEY> and <GIT_TOKEN>, so we can continue !!!!")
            sys.exit(1)


    def remote_download(self, name, version, dest, cache_policy):
        abs_path = convert_to_absolute_path(dest)
        project, cluster, personal = self.config_manager.get_environment()
        if not project or not cluster:
            print("Failed to download dataset, because in current enviroment cli can't identify your project or cluster, plz reach out infra team to setup")
            sys.exit(1)

        if abs_path.startswith("/mnt/personal") and not personal:
            print(f"We can't get your personal information as you want to use {abs_path}, so please reach out infra team to setup.")
            return False
        data = {
            "dataset_name": name,
            "version": version,
            "dest_path": abs_path,
            "cache_policy": cache_policy,
            "project": project,
            "cluster": cluster,
            "personal": personal,
        }
        try:
            response = self.conn.post("/get", json=data)

            # Check if the status code is in the 2xx range
            if 200 <= response.status_code < 300:
                response_data = response.json()
                task_id = response_data.get('task_id')
                if task_id:
                    print(f"Dataset get operation initiated. Your task ID is: \033[92m{task_id}\033[0m")
                    print(f"You can check the status later by running: \033[92manc ds task status {task_id}\033[0m")
                    print(f"If your task has been pending a long time, please check the queue with: \033[92manc ds queue status\033[0m")
                    print(f"please don't do any directory change along with {abs_path}")
                else:
                    print("Dataset get operation initiated, but no task ID was returned.")
            else:
                print(f"Error: Server responded with status code {response.status_code}")
                print(f"{response.text}")

        except RequestException as e:
            print(f"Sorry, you can't add dataset out of clusters, please use it in a notebook")
        except json.JSONDecodeError:
            print("Error: Received invalid JSON response from server")
        except KeyboardInterrupt:
            print(f"Operation interrupted.")
            sys.exit(0)
        except Exception as e:
            print(f"Sorry, your command run failed, you can try again or reach out infra team")

    def list_dataset(self, dataset_name, verbose):
        response = self.conn.get("/query_datasets", params={"dataset_name": dataset_name})
        if response.status_code == 200:
            data = response.json()

            if not verbose:
                data = data[-10:]

            headers = [
                "Created At", "Dataset Name", 
                "Dataset Version", "Source Path"
            ]
            if verbose:
                headers.append("Message")
            
            table = [
                [
                    item["created_at"], item["dataset_name"],
                    item["dataset_version"], item["source_path"]
                ] + ([item["message"]] if verbose else [])
                for item in data
            ]
            print(tabulate(table, headers=headers, tablefmt="grid", disable_numparse=True))
        else:
            print("Failed to retrieve datasets. Status code:", response.status_code)

    def get_commit_id(self, dataset_name, dataset_version):
        data = {
            "dataset_name": dataset_name,
            "version": dataset_version,
        }
        try:
            response = self.conn.get("/query_datasets", params={"dataset_name": dataset_name, "dataset_version": dataset_version})
            data = response.json()
            return data[0]["git_commit_id"] if len(data) > 0 and "git_commit_id" in data[0] else None
        except Exception as e:
            print(f"Error occurred: {e}")


    def local_download(self, git_commit_id, dataset_name, dest_path):
        print("<<This is a local download operation>>")
        if os.getenv("AWS_ACCESS_KEY_ID", None) is None or os.getenv("AWS_SECRET_ACCESS_KEY", None) is None or os.getenv("GIT_TOKEN", None) is None:
            print("!!!! Hey, are you sure you want to download it to your local? if yes, please set environment for <AWS_ACCESS_KEY_ID> and <AWS_SECRET_ACCESS_KEY> and <GIT_TOKEN>, so we can continue !!!!")
            sys.exit(1)
        url = repo_url
        git_token = os.environ["GIT_TOKEN"]
        repo_url_with_token = url.replace("https://", f"https://{git_token}@")
        source_path = 'local/' +  dataset_name
        command = ["dvc", "get", repo_url_with_token, source_path, "--rev", git_commit_id, "-o", dest_path]

        try:
            subprocess.run(command, check=True)
            print(f"Successfully downloaded {source_path} from {repo_url} to {dest_path}.")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to download {source_path}: {e}")
