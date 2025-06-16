import os
import requests

class TeamworkManager:
    base = ''
    api_base = ''
    token = ''

    def __init__(self, config):
        self.base = f"https://{config.user}.teamwork.com/"
        self.token = config.token

    def get_issue_url(self, id):
        return f"{self.base}app/tasks/{id}"

    def get_tasklist(self, tasklist_id):
        url = f"{self.base}/projects/api/v3/tasklists/{tasklist_id}?include=projects&fields[projects]=name"
        response = requests.get(url, auth=(self.token, ''))
        response.raise_for_status()
        return response.json()

    def find_tasks_by_tags(self, tags):
        str_tags = ",".join(tags)
        url = self.base + f"projects/api/v3/tasks.json?tags={str_tags}&include= projects&fields[projects]=name&matchAllTags=true&fields[tags]=name&includeCompletedTasks=true"
        response = requests.get(url, auth=(self.token, ''))
        response.raise_for_status()
        return response.json()['tasks']

    def close_issue(self, task_id):
        url = self.base + f"/tasks/{task_id}.json"
        payload = {
            'todo-item': {
                'completed': True
            }
        }
        response = requests.put(url, auth=(self.token, ''), json=payload)

    def reassign(self, task_id, assign_to):
        url = self.base + f"projects/api/v3/tasks/{task_id}.json"
        payload = {
                "task": {
                    "assignees" :{
                    "userIds" : [assign_to]
                    }
                }
            }
        response = requests.patch(url, auth=(self.token, ''), json=payload)

    def add_comment(self, task_id, text):
        url = self.base + f"tasks/{task_id}/comments.json"
        payload = {
            "comment": {
                "body": text,
                "notify": True
            }
        }
        response = requests.post(url, auth=(self.token, ''), json=payload)

    def add_attachments_to_task(self, task_id, file_names):
        for file_path in file_names:
            # Get a presigned url
            file_name = os.path.basename(file_path)
            file_size = os.stat(file_path)
            url = self.base + f"/projects/api/v1/pendingfiles/presignedurl.json?fileName={file_name}&fileSize={file_size}"
            response = requests.get(url, auth=(self.token, ''))

            ref = response.json()['ref']
            upload_url = response.json()['url']

            # Upload a file to presigned url
            with open(file_path, 'rb') as file_handle:
                headers = {
                    "X-Amz-Acl": "public-read",
                    "Content-Type": "application/octet-stream"
                }
                response = requests.put(
                    upload_url,
                    headers = headers,
                    data = file_handle
                )
        
            # attach the uploaded file to the task
            url = self.base + f"/projects/api/v3/tasks/{task_id}.json"
            payload = {
                "attachments": 
                {
                    "pendingFiles": 
                        [{
                            "reference" :ref 
                        }]
                }
            }
            response = requests.patch(url, auth=(self.token, ''), json=payload)
