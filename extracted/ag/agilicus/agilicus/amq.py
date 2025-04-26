from stomp import WSConnection
from stomp.listener import WaitingListener
from urllib.parse import urlparse

from .input_helpers import get_org_from_input_or_ctx
from .context import get_cacert, get_api, get_token, is_admin
from .context import get_user_id


class Dumper(WaitingListener):
    def __init__(self, receipt=None):
        WaitingListener.__init__(self, receipt)

    def on_message(self, frame):
        dest = ""
        if "destination" in frame.headers:
            dest = frame.headers.get("destination")
        print(f"{dest}: {frame.body}")


def subscribe(
    ctx, exchange, routing_key=None, org_id=None, queue_override=None, **kwargs
):
    cert = get_cacert(ctx)
    token = get_token(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id)

    url = urlparse(get_api(ctx))

    header = {}
    header = [f"Authorization: bearer {token}"]

    hosts = [(url.hostname, 443)]
    connection = WSConnection(
        hosts, heartbeats=(10000, 10000), ws_path="/mq", vhost="/", header=header
    )
    connection.set_ssl(for_hosts=hosts, ca_certs=cert)

    listener = Dumper()
    connection.set_listener("debugoutput", listener)
    user_id = get_user_id(ctx, user_token=token)
    connection.connect(user_id, token, wait=True)

    if routing_key is None:
        if is_admin(ctx):
            if org_id:
                routing_key = f"org.{org_id}.#"
            else:
                routing_key = "org.#"
        else:
            routing_key = f"org.{org_id}.#"

    if queue_override:
        subscription = f"/queue/{queue_override}"
    else:
        subscription = f"/exchange/{exchange}/{routing_key}"
    print(f"STOMP subscription: {subscription}")
    connection.subscribe(f"{subscription}", id="3")
    listener.wait_on_disconnected()
