#!/usr/bin/env bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
set -euo pipefail

: "${SOURCE_ARCHIVE_URI:?}" "${RUN_PREFIX_URI:?}" "${CLI_ARGS_JSON:?}"
WORK=/var/tmp/connector-regression-eu
OUT="$WORK/out"
mkdir -p "$WORK" "$OUT"
cd "$WORK"

metadata_token() {
  curl -sf -H 'Metadata-Flavor: Google' \
    http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token |
    python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])'
}

split_gs_uri() {
  python3 -c 'import sys; print(sys.argv[1][5:].split("/",1)[0]); print(sys.argv[1][5:].split("/",1)[1])' "$1"
}

gcs_get() {
  local bucket object
  mapfile -t parsed < <(split_gs_uri "$1")
  bucket="${parsed[0]}"
  object="${parsed[1]}"
  curl -sf -H "Authorization: Bearer $(metadata_token)" -o "$2" \
    "https://storage.googleapis.com/storage/v1/b/${bucket}/o/$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$object")?alt=media"
}

gcs_put() {
  local bucket object
  mapfile -t parsed < <(split_gs_uri "$2")
  bucket="${parsed[0]}"
  object="${parsed[1]}"
  curl -sf -X POST -H "Authorization: Bearer $(metadata_token)" \
    --data-binary @"$1" -H 'Content-Type: application/octet-stream' \
    "https://storage.googleapis.com/upload/storage/v1/b/${bucket}/o?uploadType=media&name=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$object")" >/dev/null
}

pull_image() {
  if docker pull -q "mirror.gcr.io/$1"; then
    docker tag "mirror.gcr.io/$1" "$1"
  else
    docker pull -q "$1"
  fi
}

# The workflow built the PR's image in a job with no credentials and staged
# it. The archive is the PR's to write, so it must load that one image and
# nothing else: a second tag could stand in for the control image, which the
# CLI takes from the local store before pulling.
load_target_image() {
  local loaded
  gcs_get "$RUN_PREFIX_URI/target-image.tar" "$WORK/target-image.tar"
  loaded="$(docker load --input "$WORK/target-image.tar")"
  rm -f "$WORK/target-image.tar"
  if [[ "$loaded" != "Loaded image: $TARGET_IMAGE" ]]; then
    echo "The image archive did not load exactly $TARGET_IMAGE; stopping before any command runs." >&2
    exit 1
  fi
}

# The connector under test is the PR's code, and the metadata server hands any
# caller on this VM the job service account's token, which reads prod
# connection secrets. So containers, and the user mitmdump runs as, since a
# container's proxied requests leave the host as that user, are cut off from
# it. The harness, running as root, still uses it, and TCP 53 stays open:
# the metadata server is also the VM's DNS resolver.
MITMDUMP_USER=regression-proxy
SELF_TEST_IMAGE=library/busybox:1.36.1
METADATA_URL=http://169.254.169.254/computeMetadata/v1/

block_metadata_server() {
  command -v iptables >/dev/null || {
    apt-get update -qq
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq iptables
  }
  iptables -I DOCKER-USER -d 169.254.169.254 -p tcp ! --dport 53 -j REJECT
  id -u "$MITMDUMP_USER" >/dev/null 2>&1 ||
    useradd --system --create-home --home-dir "/var/lib/$MITMDUMP_USER" \
      --shell /usr/sbin/nologin "$MITMDUMP_USER"
  iptables -I OUTPUT -d 169.254.169.254 -p tcp ! --dport 53 \
    -m owner --uid-owner "$MITMDUMP_USER" -j REJECT
}

# A container or user that fails to run also fails to reach the server, so the
# name lookup, from the same image, shows the containers did run.
metadata_block_holds() {
  if docker run --rm "$SELF_TEST_IMAGE" wget -q -T 5 -O /dev/null \
    --header 'Metadata-Flavor: Google' "$METADATA_URL"; then
    echo "A container reached the metadata server." >&2
    return 1
  fi
  if runuser -u "$MITMDUMP_USER" -- curl -sf -m 5 -o /dev/null \
    -H 'Metadata-Flavor: Google' "$METADATA_URL"; then
    echo "The proxy's user reached the metadata server." >&2
    return 1
  fi
  if ! docker run --rm "$SELF_TEST_IMAGE" nslookup storage.googleapis.com >/dev/null; then
    echo "A container could not resolve a name." >&2
    return 1
  fi
}

echo "== Docker"
command -v docker >/dev/null || {
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker.io
}
systemctl start docker || true
block_metadata_server
pull_image "$SELF_TEST_IMAGE"
if ! metadata_block_holds; then
  echo "The metadata server block does not hold; stopping before any command runs." >&2
  exit 1
fi
export REGRESSION_MITMDUMP_USER="$MITMDUMP_USER"

curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
# mitmdump runs from this tree's virtualenv as $MITMDUMP_USER, who cannot
# enter root's home, where uv keeps its Pythons by default.
export UV_PYTHON_INSTALL_DIR="$WORK/python"
uv python install 3.12
gcs_get "$SOURCE_ARCHIVE_URI" "$WORK/source.tar.gz"
mkdir "$WORK/ops-mcp"
tar -xzf "$WORK/source.tar.gz" -C "$WORK/ops-mcp"
cd "$WORK/ops-mcp"
uv sync --python 3.12 --group dev --group live-tests --all-packages

if [[ -n "${TARGET_IMAGE:-}" ]]; then
  load_target_image
fi

mapfile -t CLI_ARGS < <(
  python3 -c 'import json,sys; [print(arg) for arg in json.load(sys.stdin)]' <<<"$CLI_ARGS_JSON"
)
SKIP_READ=false
FILTERED_ARGS=()
HAS_CONNECTION_ID=false
HAS_CATALOG_PATH=false
for arg in "${CLI_ARGS[@]}"; do
  if [[ "$arg" == "--eu-skip-read-action" ]]; then
    SKIP_READ=true
  else
    FILTERED_ARGS+=("$arg")
  fi
  if [[ "$arg" == "--connection-id" ]]; then
    HAS_CONNECTION_ID=true
  elif [[ "$arg" == "--catalog-path" ]]; then
    HAS_CATALOG_PATH=true
  fi
done
CLI_ARGS=("${FILTERED_ARGS[@]}")
# The CLI builds the connector from source when it has no `--test-image`, and
# nothing on this VM builds.
if [[ " ${CLI_ARGS[*]} " != *" --test-image "* ]]; then
  echo "No --test-image: the VM does not build the connector; stopping before any command runs." >&2
  exit 1
fi
# A registry image pulled under the loaded tag would replace the PR's build.
for option in --control-image --test-image; do
  for ((i = 0; i < ${#CLI_ARGS[@]}; i++)); do
    if [[ "${CLI_ARGS[i]}" == "$option" && $((i + 1)) -lt ${#CLI_ARGS[@]} ]]; then
      image="${CLI_ARGS[i + 1]}"
      if [[ "$image" != "${TARGET_IMAGE:-}" ]]; then
        pull_image "$image"
      fi
    fi
  done
done

unset GCP_PROD_DB_ACCESS_CREDENTIALS GCP_GSM_CREDENTIALS
export DO_NOT_TRACK=1 USE_CONNECTION_SECRET_RETRIEVER=true
if [[ " ${CLI_ARGS[*]} " == *" --connection-id "* ]]; then
  set +x
  token="$(metadata_token)"
  secret_json="$(
    curl -sf -H "Authorization: Bearer $token" \
      "https://secretmanager.googleapis.com/v1/projects/internal-airbyte-ai-infra/secrets/connector-regression-eu-cloud-api/versions/latest:access" |
      python3 -c 'import base64,json,sys; print(base64.b64decode(json.load(sys.stdin)["payload"]["data"]).decode())'
  )"
  export AIRBYTE_CLOUD_CLIENT_ID
  export AIRBYTE_CLOUD_CLIENT_SECRET
  AIRBYTE_CLOUD_CLIENT_ID="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["client_id"])' <<<"$secret_json")"
  AIRBYTE_CLOUD_CLIENT_SECRET="$(python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["client_secret"])' <<<"$secret_json")"
  unset secret_json token
fi

# The workflow stages state.json only for a requested seed and says so here.
# A read without it would start from another state and could still pass, so a
# seed that does not download stops the run before any command, and the job's
# failure is the run's internal failure.
STATE_ARGS=()
if [[ "${SEED_STATE_STAGED:-false}" == "true" ]]; then
  for attempt in 1 2 3; do
    if gcs_get "$RUN_PREFIX_URI/state.json" "$WORK/state.json"; then
      STATE_ARGS+=(--state-path "$WORK/state.json")
      break
    fi
    [[ $attempt -eq 3 ]] || sleep $((attempt * 10))
  done
  if [[ ${#STATE_ARGS[@]} -eq 0 ]]; then
    echo "The requested seed state could not be downloaded; stopping before any command runs." >&2
    exit 1
  fi
fi

select_commands() {
  local has_connection_id="$1"
  local skip_read="$2"

  COMMANDS=(spec)
  if [[ "$has_connection_id" != true ]]; then
    return
  fi

  COMMANDS+=(check discover)
  if [[ "$skip_read" != true ]]; then
    COMMANDS+=(read)
  fi
}
# Connectionless forced runs only have a connector spec to exercise.
select_commands "$HAS_CONNECTION_ID" "$SKIP_READ"
# One masking key for the run, so every command's tokens pair, as on the US
# runner. It stays under $WORK, outside $OUT and so outside every upload, is
# never printed, and goes when the script exits, keeping its exit code.
MASK_KEY_PATH="$WORK/mask_key"
trap 'rm -f "$MASK_KEY_PATH" || true' EXIT
python3 -c 'import secrets; print(secrets.token_hex(32))' > "$MASK_KEY_PATH"
chmod 600 "$MASK_KEY_PATH"
rc=0
last_command=""
for command in "${COMMANDS[@]}"; do
  command_output="$WORK/$command.github-output"
  command_args=("${CLI_ARGS[@]}" --command "$command" --output-mode masked \
    --mask-key-path "$MASK_KEY_PATH" --output-dir "$OUT/$command")
  if [[ "$command" == "read" ]]; then
    command_args+=("${STATE_ARGS[@]}")
    if [[ "$HAS_CONNECTION_ID" != true && "$HAS_CATALOG_PATH" != true ]]; then
      mkdir -p "$OUT/$command"
      catalog="$OUT/discover/target/airbyte_messages/catalog.jsonl"
      if [[ ! -f "$catalog" ]]; then
        catalog="$OUT/discover/airbyte_messages/catalog.jsonl"
      fi
      if [[ ! -f "$catalog" ]]; then
        echo "No catalog file found for READ." >&2
        rc=1
        break
      fi
      python3 - "$catalog" "$WORK/configured-catalog.json" <<'PY'
import json
import sys

catalog_path, output_path = sys.argv[1:]
catalog = None
with open(catalog_path) as catalog_file:
    for line in catalog_file:
        message = json.loads(line.strip()) if line.strip() else {}
        if message.get("type") == "CATALOG":
            catalog = message["catalog"]
            break
if catalog is None:
    raise SystemExit("No CATALOG message found")
streams = [
    {
        "stream": stream,
        "sync_mode": (
            "full_refresh"
            if not stream.get("supported_sync_modes")
            or "full_refresh" in stream.get("supported_sync_modes", [])
            else stream["supported_sync_modes"][0]
        ),
        "destination_sync_mode": "overwrite",
    }
    for stream in catalog.get("streams", [])
]
with open(output_path, "w") as output_file:
    json.dump({"streams": streams}, output_file, indent=2)
PY
      command_args+=(--catalog-path "$WORK/configured-catalog.json")
    fi
  fi
  set +e
  GITHUB_OUTPUT="$command_output" uv run airbyte-ops cloud connector regression-test \
    "${command_args[@]}"
  command_rc=$?
  set -e
  printf '%s\n' "$command_rc" > "$WORK/$command.exit-code"
  last_command="$command"
  python3 - "$command_output" "$OUT/$command/regression_report.json" <<'PY'
import json
import sys

source_path, destination_path = sys.argv[1:]
try:
    with open(source_path) as source:
        lines = source.readlines()
except FileNotFoundError:
    raise SystemExit(0)
for index, line in enumerate(lines):
    if line.startswith("regression_report<<"):
        delimiter = line.rstrip("\n").split("<<", 1)[1]
        value = []
        for item in lines[index + 1 :]:
            if item.rstrip("\n") == delimiter:
                with open(destination_path, "w") as destination:
                    destination.write("".join(value))
                break
            value.append(item)
        break
PY
  if [[ $command_rc -ne 0 ]]; then
    rc=$command_rc
    break
  fi
done

if [[ -n "$last_command" && -f "$OUT/$last_command/report.html" ]]; then
  cp "$OUT/$last_command/report.html" "$OUT/report.html"
fi
python3 - "$OUT" "$rc" "$WORK" <<'PY'
import json
import pathlib
import sys

output_dir, exit_code, work_dir = pathlib.Path(sys.argv[1]), int(sys.argv[2]), pathlib.Path(sys.argv[3])
commands = []
both_failed = False
incomplete = False
not_exercised = False
for exit_path in sorted(work_dir.glob("*.exit-code")):
    command = exit_path.stem.removesuffix(".exit-code")
    command_exit = int(exit_path.read_text())
    # The CLI exits 0 on a failed verdict, so the remaining commands still
    # run; its success output, not the exit code, says the command failed.
    verdict_failed = False
    output_path = work_dir / f"{command}.github-output"
    if output_path.exists():
        for line in output_path.read_text().splitlines():
            key, separator, value = line.partition("=")
            if separator and key == "success":
                verdict_failed = verdict_failed or value.lower() == "false"
            if separator and key == "both_failed":
                both_failed = both_failed or value.lower() == "true"
            if separator and key == "incomplete":
                incomplete = incomplete or value.lower() == "true"
            if separator and key == "not_exercised":
                not_exercised = not_exercised or value.lower() == "true"
    commands.append(
        {
            "command": command,
            "exit_code": command_exit,
            "passed": command_exit == 0 and not verdict_failed,
        }
    )
summary = {
    "exit_code": exit_code,
    "success": exit_code == 0 and all(item["passed"] for item in commands),
    "both_failed": both_failed,
    "incomplete": incomplete,
    "not_exercised": not_exercised,
    "commands": commands,
}
(output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
PY
uv run airbyte-ops cloud connector eu-runner write-verdict \
  --output-dir "$OUT" --out "$WORK/verdict.json"
gcs_put "$OUT/summary.json" "$RUN_PREFIX_URI/summary.json"
gcs_put "$WORK/verdict.json" "$RUN_PREFIX_URI/verdict.json"
# The CLI leaves the HTTP captures in $OUT for the upload to filter, as the US
# job's upload steps do. They hold the connector's request headers, credentials
# included, and its response bodies.
tar --exclude='*.mitm' --exclude='*.har' -czf "$WORK/out.tar.gz" -C "$WORK" out
gcs_put "$WORK/out.tar.gz" "$RUN_PREFIX_URI/out.tar.gz"
if [[ -f "$OUT/report.html" ]]; then
  gcs_put "$OUT/report.html" "$RUN_PREFIX_URI/report.html"
fi
exit "$rc"
