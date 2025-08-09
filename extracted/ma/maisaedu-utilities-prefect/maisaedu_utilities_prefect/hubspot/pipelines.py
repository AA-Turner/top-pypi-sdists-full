import requests
import json
import urllib
from retry import retry

@retry(tries=5, delay=1, jitter=1)
def get_all_pipelines(hapikey, app_private_token, types = ['tickets', 'deals']):
    final_result = list()
    for type in types:
        if type in ['tickets', 'deals']:
            url = "https://api.hubapi.com/crm-pipelines/v1/pipelines"
        if type == 'p5643730_ids_de_inadimpl_ncia':
            url = "https://api.hubapi.com/crm/v3/pipelines"

        if hapikey is not None:
            parameter_dict = {"hapikey": hapikey, "archived": False}
            headers = {}
        else:
            parameter_dict = {"archived": False}
        headers = {"content-type": "application/json", "cache-control": "no-cache", 'Authorization': f"Bearer {app_private_token}"}

        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = "%s/%s?" % (url, type) + parameters
        r = requests.get(url=get_url, headers=headers)
        data = list()
        res = json.loads(r.text)

        for item in res["results"]:
            if "objectType" not in item:
                item["objectType"] = type
            if "pipelineId" not in item:
                item["pipelineId"] = item.get("id", None)
                for stage in item.get("stages", []):
                    if "stageId" not in stage:
                        stage["stageId"] = stage.get("id", None)
            data.append(item)

    final_result.extend(data)

    return final_result
