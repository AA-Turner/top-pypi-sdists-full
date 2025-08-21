import json
import os
import urllib.request

prefix = ""
mount_prefix = None
# Override prefix if it's set in the http config
if (http := os.environ.get("LANGGRAPH_HTTP")) and (
    mount_prefix := json.loads(http).get("mount_prefix")
):
    prefix = mount_prefix
# Override that
if os.environ.get("MOUNT_PREFIX"):
    prefix = os.environ["MOUNT_PREFIX"]

with urllib.request.urlopen(
    f"http://localhost:{os.environ['PORT']}{prefix}/ok"
) as response:
    assert response.status == 200
