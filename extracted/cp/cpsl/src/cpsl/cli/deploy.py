import time

import click
import grpc

from .. import terminal
from ..channel import pass_service_client, ServiceClient
from ..typestubs import generate_type_stubs
from ..utils import (
    resolve_entry_point,
    collect_source_archive,
    build_image_spec,
    build_channel_specs,
    build_filesystem_mount_specs,
    build_integration_specs,
    build_schedule_specs,
    normalize_image,
)

DEPLOY_TIMEOUT = 240.0
BUILD_LOG_PREFIX = "Image build: "


def _handle_status(spinner, status: str, build_logs_seen: bool) -> bool:
    if status.startswith(BUILD_LOG_PREFIX):
        if not build_logs_seen:
            terminal.header("Build logs")
            build_logs_seen = True
        terminal.detail(f"  │ {status[len(BUILD_LOG_PREFIX):]}", dim=True)
        spinner.update("Building image...")
        return build_logs_seen

    spinner.update(status)
    return build_logs_seen


@click.command("deploy")
@click.argument("entry_point")
@pass_service_client
def deploy(client: ServiceClient, entry_point: str):
    """Deploy an app.

    ENTRY_POINT is <file.py>:<Name>, e.g. app.py:OutreachAgent or app.py:app
    """
    config = resolve_entry_point(entry_point)

    image = normalize_image(config["image"])
    channels = config.get("channels", [])
    secrets = config.get("secrets", [])
    keep_warm = config.get("keep_warm_seconds", 0)
    filesystems = config.get("filesystems", {})
    integrations = config.get("integrations", [])
    schedules = config.get("schedules", [])
    cpu = config.get("cpu", 0.25)
    memory = config.get("memory", 512)
    gpu = config.get("gpu")

    pages = config.get("pages", [])
    data_sources = config.get("data_sources", [])

    generate_type_stubs(pages)

    terminal.header("Deploying", f"[bold]{config['app_name']}[/bold]")
    entry_label = config['class_name'] or config['app_name']
    terminal.detail(f"  entry:    {config['module']}:{entry_label}")
    pricing = config.get("pricing_type", "one_time")
    price_display = f"${config['price'] / 100:.2f}" if config['price'] >= 100 else f"{config['price']}¢"
    terminal.detail(f"  price:    {price_display}/{pricing.replace('_', ' ')}")
    terminal.detail(f"  channels: {len(channels)}")

    if pages:
        terminal.detail(f"  pages:    {', '.join(p['name'] for p in pages)}")
    if data_sources:
        terminal.detail(f"  data:     {', '.join(data_sources)}")
    if secrets:
        terminal.detail(f"  secrets:  {', '.join(secrets)}")

    if keep_warm > 0:
        terminal.detail(f"  keep_warm: {keep_warm}s")

    if filesystems:
        for mount, fs in filesystems.items():
            details = []
            if fs.get("sources"):
                details.append(f"{len(fs['sources'])} source view(s)")
            if fs.get("tools"):
                details.append(f"{len(fs['tools'])} tool(s)")
            suffix = f" ({', '.join(details)})" if details else ""
            terminal.detail(f"  fs:       {mount} -> {fs.get('name', '')}{suffix}")

    compute = f"{cpu} vCPU / {memory} MiB"
    if gpu:
        compute += f" / {gpu} GPU"
    terminal.detail(f"  compute:  {compute}")

    if image.get("python_packages"):
        terminal.detail(f"  pip:      {', '.join(image['python_packages'])}")
    if image.get("apt_packages"):
        terminal.detail(f"  apt:      {', '.join(image['apt_packages'])}")

    terminal.header("Syncing files")
    archive = collect_source_archive()

    terminal.header("Pushing")

    from ..clients.capsule import DeployRequest, DeployResponse

    req = DeployRequest(
        app_name=config["app_name"],
        image=build_image_spec(image, cpu=cpu, memory=memory, gpu=gpu),
        channels=build_channel_specs(channels),
        entry_point=f"{config['module']}:{config['class_name'] or entry_point.rsplit(':', 1)[1]}",
        price_in_cents=config["price"],
        source_archive=archive,
        keep_warm_seconds=keep_warm,
        secrets=secrets,
        filesystems=build_filesystem_mount_specs(filesystems),
        integrations=build_integration_specs(integrations),
        schedules=build_schedule_specs(schedules),
        pricing_type=config.get("pricing_type", "one_time"),  # wire value: "one_time" | "monthly"
    )

    with terminal.progress("Provisioning machine...") as spinner:
        t0 = time.monotonic()
        build_logs_seen = False
        deploy_call = client.channel.unary_stream(
            "/capsule.CapsuleService/Deploy",
            DeployRequest.SerializeToString,
            DeployResponse.FromString,
        )
        res = None
        try:
            for msg in deploy_call(req, timeout=DEPLOY_TIMEOUT):
                if msg.ok or msg.err_msg:
                    res = msg
                    break
                if msg.status:
                    build_logs_seen = _handle_status(spinner, msg.status, build_logs_seen)
        except grpc.RpcError as err:
            if err.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                terminal.error(
                    "Timed out waiting for Deploy. "
                    "If you're using local dev, restart `make start`."
                )
                raise SystemExit(1)
            raise

        if res is None:
            terminal.error("Deploy stream ended without a result.")
            raise SystemExit(1)

        elapsed = time.monotonic() - t0

    if not res.ok:
        terminal.error(f"Deploy failed: {res.err_msg}")

    terminal.success(f"Validated in {elapsed:.1f}s")
    terminal.header(f"Deployed {config['app_name']} v{res.version}")
    terminal.url(res.url or f"https://{res.hostname}.capsule.new")
