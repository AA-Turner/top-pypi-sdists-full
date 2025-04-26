from json import loads as json_loads

import click
from rich import print

import coiled

from .utils import CONTEXT_SETTINGS


@click.command(
    context_settings=CONTEXT_SETTINGS,
    help="CLI to hit endpoints using Coiled account authentication (mostly for internal use)",
)
@click.argument("url")
@click.option("-X", "--request", default="GET")
@click.option("-d", "--data", multiple=True)
@click.option("--json", is_flag=True, default=False)
@click.option("--json-output", is_flag=True, default=False, help="Set to pretty print JSON responses")
def curl(url: str, request, data, json, json_output):
    all_data = "&".join(data) if data else None
    with coiled.Cloud() as cloud:
        if not url.startswith("http"):
            url = f"{cloud.server}{url}"
        response = sync_request(cloud, url, method=request, data=all_data, json=json, json_output=json_output)

    print(response)


def sync_request(cloud, url, method, data, json: bool = False, json_output: bool = False):
    kwargs = {"method": method, "url": url}

    if json:
        kwargs["json"] = json_loads(data) if isinstance(data, str) else data
    else:
        kwargs["data"] = data
    response = cloud._sync(cloud._do_request, **kwargs)
    if response.status >= 400:
        print(f"{url} returned {response.status}")

    async def get_result(r):
        return await (r.json() if json_output else r.text())

    return cloud._sync(
        get_result,
        response,
    )
