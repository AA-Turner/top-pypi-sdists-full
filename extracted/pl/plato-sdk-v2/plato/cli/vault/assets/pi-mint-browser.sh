#!/usr/bin/env bash
# pi-mint-browser: one Chromium for one `plato vault ... --browser pi` command, on pi5-2.
# Install (no sudo): install -m 700 pi-mint-browser.sh ~/.local/bin/pi-mint-browser
# The vault command runs this over ssh (pi_browser.py PiLauncher). Each mode prints ONE line:
#   @@PIMINT {json}
# The modes, exit codes and files are in docs/exploration/vault-app.md ("The launcher").
#
# Every mode but --status holds one lock ($DATA_DIR/launcher.lock, outside the run
# directory that --start and --stop remove): two commands that started at the same time
# each started a Chromium on one profile, and the stop then left one of them running.
#
# One saved login per vault account (L, the slug `<login_key>.<account>`). Every save of a
# run goes to the tar of the run's own L: a shared tar let a 2FA setup run as another account.
#
# Warning: CDP gives full control of this browser and its cookies to every process
# of this user. The port binds 127.0.0.1 only, and Chromium runs only while a
# command runs.

set -u
umask 077

ROOT=/dev/shm/pi-mint
PROFILE="$ROOT/profile"
CACHE="$ROOT/cache"
PIDFILE="$ROOT/chromium.pid"
TOKENFILE="$ROOT/token"
HANDOFF="$ROOT/handoff"
COOKIES_SHA="$ROOT/cookies.sha256"
LOGINFILE="$ROOT/login"  # the run's account slug (empty: the run saves no login)
DATA_DIR="$HOME/.local/share/pi-mint"
LOGIN_DIR="$DATA_DIR/logins"
LOCKFILE="$DATA_DIR/launcher.lock"
LOCK_WAIT_S=60  # under the 90 s that the vault command waits for one launcher call
LOGIN_MAX=120
CDP_PORT=9222
CDP_WAIT_S=30
STOP_WAIT_S=10
CHROMIUM="${PI_MINT_CHROMIUM:-chromium}"

reply() { printf '@@PIMINT %s\n' "$1"; }
fail() {  # fail <exit code> <short error>
  reply "{\"error\":\"$2\"}"
  exit "$1"
}
run_token() { cat "$TOKENFILE" 2>/dev/null; }
busy() {  # busy <short error>: exit 3, with the token of the run that holds the browser
  # The token is a run name, not a secret: the person who must stop that run by hand
  # needs it, because a stop with no token is refused.
  local held
  held=$(run_token)
  if [ -n "$held" ]; then
    reply "{\"error\":\"$1\",\"token\":\"$held\"}"
  else
    reply "{\"error\":\"$1\"}"
  fi
  exit 3
}

# One launcher call at a time. fd 9 stays open for the whole call; flock(1) frees it
# when this shell exits. Chromium must not inherit fd 9 (its launch closes it).
take_lock() {
  if ! { mkdir -p "$DATA_DIR" && chmod 700 "$DATA_DIR"; }; then fail 5 "cannot make $DATA_DIR"; fi
  exec 9>>"$LOCKFILE" || fail 5 "cannot open $LOCKFILE"
  flock -w "$LOCK_WAIT_S" 9 || busy "another launcher call holds $LOCKFILE"
}

# Something listens on the CDP port. Before a launch no Chromium of ours runs, so a
# listener is a Chromium that this launcher lost (or another program): a new Chromium
# could not bind, and the CDP wait then took the other one for the new run.
port_in_use() { (exec 3<>"/dev/tcp/127.0.0.1/$CDP_PORT") 2>/dev/null; }

# The pid of the running pi-mint Chromium, or nothing. A pid counts only when its
# command line holds our profile path (a reused pid is not ours).
running_pid() {
  [ -f "$PIDFILE" ] || return 0
  local pid
  pid=$(cat "$PIDFILE" 2>/dev/null)
  case "$pid" in '' | *[!0-9]*) return 0 ;; esac
  if kill -0 "$pid" 2>/dev/null && pid_cmdline "$pid" | grep -q -- "--user-data-dir=$PROFILE"; then
    printf '%s' "$pid"
  fi
}

pid_cmdline() {  # /proc on the Pi; ps where there is no /proc (the unit tests on a Mac)
  if [ -r "/proc/$1/cmdline" ]; then
    tr '\0' ' ' <"/proc/$1/cmdline" 2>/dev/null
  else
    ps -ww -o command= -p "$1" 2>/dev/null
  fi
}

cookies_sha() {
  cat "$PROFILE/Default/Cookies" "$PROFILE/Default/Network/Cookies" 2>/dev/null | sha256sum | cut -d' ' -f1
}

run_login() { cat "$LOGINFILE" 2>/dev/null; }

login_tar() { printf '%s/%s.tar.zst' "$LOGIN_DIR" "$1"; }

# The run's slug as JSON: "canva.jim" or null. The slug holds no character that JSON escapes.
login_json() {
  local slug
  slug=$(run_login)
  if [ -n "$slug" ]; then printf '"%s"' "$slug"; else printf 'null'; fi
}

# Write the run's tar atomically: a temp file in the same directory, then mv.
# 0: saved. 1: the save failed (tar, zstd, rename, disk). 2: nothing to save.
save_login() {
  [ -d "$PROFILE" ] || return 2
  local slug tarfile
  slug=$(run_login)
  [ -n "$slug" ] || return 2  # a run with no account slug never saves (fresh profile)
  mkdir -p "$LOGIN_DIR" && chmod 700 "$DATA_DIR" "$LOGIN_DIR" || return 1
  tarfile=$(login_tar "$slug")
  local tmp="$tarfile.tmp.$$"
  if tar --zstd -C "$ROOT" -cf "$tmp" \
    --exclude='profile/Singleton*' --exclude='profile/DevToolsActivePort' \
    --exclude='*/Cache' --exclude='*/Code Cache' --exclude='*/GPUCache' --exclude='*/DawnCache' \
    --exclude='*/GrShaderCache' --exclude='*/GraphiteDawnCache' --exclude='*/ShaderCache' \
    --exclude='*/component_crx_cache' --exclude='*/optimization_guide_model_store' \
    --exclude='*/Service Worker/CacheStorage' --exclude='*/Crashpad' \
    --exclude='*/Login Data*' --exclude='*/Web Data*' --exclude='*/Affiliation Database*' \
    profile 2>/dev/null; then
    chmod 600 "$tmp" && mv -f "$tmp" "$tarfile" && return 0
  fi
  rm -f "$tmp"
  return 1
}

stop_chromium() {  # TERM (Chromium writes its cookies on a clean exit), then KILL
  local pid
  pid=$(running_pid)
  [ -n "$pid" ] || return 0
  kill -TERM "$pid" 2>/dev/null
  local i=0
  while [ "$i" -lt $((STOP_WAIT_S * 2)) ] && kill -0 "$pid" 2>/dev/null; do
    sleep 0.5
    i=$((i + 1))
  done
  kill -0 "$pid" 2>/dev/null && kill -KILL "$pid" 2>/dev/null
  sleep 0.5
  return 0
}

# No password manager and no autofill: a password that a person types in noVNC must
# not go into Login Data (with --password-store=basic, anyone with the file can read
# it), and Chromium must not fill it in front of the agent.
no_saved_passwords() {
  mkdir -p "$PROFILE/Default" || return 0
  python3 - "$PROFILE/Default/Preferences" <<'PY' 2>/dev/null || true
import json, os, sys
path = sys.argv[1]
try:
    with open(path) as f:
        prefs = json.load(f)
except (OSError, ValueError):
    prefs = {}
prefs["credentials_enable_service"] = False
prefs.setdefault("profile", {})["password_manager_enabled"] = False
autofill = prefs.setdefault("autofill", {})
autofill["profile_enabled"] = False
autofill["credit_card_enabled"] = False
tmp = path + ".tmp"
with open(tmp, "w") as f:
    json.dump(prefs, f)
os.replace(tmp, path)
PY
  rm -f "$PROFILE/Default/Login Data"* "$PROFILE/Default/Web Data"*  # from a tar of an older version
}

do_stop() {  # do_stop <save: 0|1> [token] [login]. Returns 6 when the save failed.
  local save="$1" token="${2:-}" login="${3:-}" saved=false had=false held
  held=$(run_token)
  if [ -z "$token" ] && [ -d "$ROOT" ] && [ -n "$held" ]; then
    # A stop with no token cannot tell its own run from the next command's: a finish
    # that came late stopped the Chromium of a command that had started since.
    busy "the run holds a token: --stop needs --token"
  fi
  if [ -n "$token" ] && [ -d "$ROOT" ] && [ "$held" != "$token" ]; then
    reply '{"stopped":false,"saved":false}'  # another command's run: not ours to stop
    return 0
  fi
  # The caller names the account it worked on: a run of another account must not save into it.
  if [ -n "$login" ] && [ "$login" != "$(run_login)" ]; then save=0; fi
  [ -n "$(running_pid)" ] && had=true
  stop_chromium
  if [ "$save" = 1 ] && [ -d "$PROFILE" ]; then
    if [ "$(cookies_sha)" != "$(cat "$COOKIES_SHA" 2>/dev/null)" ]; then
      save_login
      case $? in
        0) saved=true ;;
        1)
          # Keep the profile: it holds the only copy of a login that changed. The next
          # --start tries the save again before it removes anything.
          reply "{\"stopped\":$had,\"saved\":false,\"error\":\"the login of $(run_login) was not saved (tar, zstd, rename or disk): its profile stays in $ROOT\"}"
          return 6
          ;;
      esac
    fi
  fi
  rm -rf -- "/dev/shm/pi-mint"
  reply "{\"stopped\":$had,\"saved\":$saved}"
}

do_start() {  # do_start <token> <login>
  local token="$1" login="$2" pid
  pid=$(running_pid)
  if [ -n "$pid" ]; then
    if [ -n "$token" ] && [ "$(cat "$TOKENFILE" 2>/dev/null)" = "$token" ]; then
      # The same command asked again (its first ssh call dropped): report the same Chromium.
      reply "{\"pid\":$pid,\"restored_login\":false,\"cdp_port\":$CDP_PORT,\"login\":$(login_json)}"
      return 0
    fi
    if [ -f "$HANDOFF" ]; then
      # A person's session: keep its login, then start a new one. Its own token, so
      # the stop is not refused as a tokenless one.
      do_stop 1 "$(run_token)" >/dev/null ||
        fail 6 "the login of the handed-off run ($(run_login)) was not saved: its profile stays in $ROOT"
    else
      busy "busy (pid $pid)"
    fi
  fi
  if port_in_use; then
    fail 7 "port $CDP_PORT is held by a process that is not the run's Chromium (find it with: ss -ltnp)"
  fi
  # No Chromium runs, but a profile is here: a person closed the window after a hand-off
  # (or Chromium crashed). Keep a login that changed before the profile goes. save_login
  # reads the slug of THAT run from $LOGINFILE, so it goes to its own account's tar.
  if [ -d "$PROFILE" ] && [ "$(cookies_sha)" != "$(cat "$COOKIES_SHA" 2>/dev/null)" ]; then
    save_login
    if [ $? = 1 ]; then
      # Never remove the only copy of a changed login. Free the disk and start again,
      # or drop that login on purpose: --stop --token <its token> (no --save-login).
      fail 6 "the login of an earlier run ($(run_login), token $(run_token)) was not saved: its profile stays in $ROOT"
    fi
  fi
  rm -rf -- "/dev/shm/pi-mint"
  mkdir -p "$ROOT" "$PROFILE" "$CACHE" || fail 5 "cannot make $ROOT"
  printf '%s' "$login" >"$LOGINFILE"
  local restored=false tarfile=""
  [ -n "$login" ] && tarfile=$(login_tar "$login")
  if [ -n "$tarfile" ] && [ -f "$tarfile" ]; then
    chmod 600 "$tarfile"
    if tar --zstd -C "$ROOT" -xf "$tarfile" 2>/dev/null; then
      restored=true
    else
      rm -rf -- "$PROFILE" && mkdir -p "$PROFILE"
    fi
  fi
  rm -f "$PROFILE"/Singleton* "$PROFILE/DevToolsActivePort"
  no_saved_passwords
  cookies_sha >"$COOKIES_SHA"
  printf '%s' "$token" >"$TOKENFILE"
  # --password-store=basic: no keyring prompt on the desktop, and the saved cookies
  # open again after a reboot. The tar is mode 600 for that reason.
  WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR="/run/user/$(id -u)" setsid "$CHROMIUM" \
    --ozone-platform=wayland \
    --remote-debugging-address=127.0.0.1 --remote-debugging-port="$CDP_PORT" \
    --user-data-dir="$PROFILE" --disk-cache-dir="$CACHE" \
    --no-first-run --no-default-browser-check --password-store=basic --start-maximized \
    about:blank >"$ROOT/chromium.log" 2>&1 </dev/null 9>&- &
  pid=$!
  printf '%s' "$pid" >"$PIDFILE"
  local i=0
  while [ "$i" -lt $((CDP_WAIT_S * 2)) ]; do
    # Chromium 154 on the Pi writes no DevToolsActivePort file for a fixed port, so ask the port itself
    if curl -fs -m 2 "http://127.0.0.1:$CDP_PORT/json/version" >/dev/null 2>&1; then
      reply "{\"pid\":$pid,\"restored_login\":$restored,\"cdp_port\":$CDP_PORT,\"login\":$(login_json)}"
      return 0
    fi
    kill -0 "$pid" 2>/dev/null || break
    sleep 0.5
    i=$((i + 1))
  done
  stop_chromium
  rm -rf -- "/dev/shm/pi-mint"
  fail 4 "chromium did not open CDP in ${CDP_WAIT_S}s"
}

mode="--start"
token=""
login=""
save=0
while [ $# -gt 0 ]; do
  case "$1" in
    --start | --stop | --mark-handoff | --clear-handoff | --status) mode="$1" ;;
    --save-login) save=1 ;;
    --token)
      shift
      token="${1:-}"
      ;;
    --login)
      shift
      login="${1:-}"
      ;;
    *) fail 5 "unknown argument" ;;
  esac
  shift
done
case "$token" in *[!A-Za-z0-9_.-]*) fail 5 "bad token" ;; esac
# The slug names a file: [a-z0-9._-] only, a letter or digit first, so no path and no dotfile.
# The letters are spelled out: a range like [a-z] also takes capitals in some locales.
LOGIN_CHARS=abcdefghijklmnopqrstuvwxyz0123456789._-
case "$login" in *[!$LOGIN_CHARS]* | [._-]*) fail 5 "bad login" ;; esac
[ "${#login}" -le "$LOGIN_MAX" ] || fail 5 "bad login"
# --save-login alone is its own mode; with --stop it is an option of the stop.
if [ "$mode" = "--start" ] && [ "$save" = 1 ]; then mode="--save-login"; fi
[ "$mode" = "--status" ] || take_lock

# A hand-off call with a token changes only the run of that token.
check_owner() {
  if [ -n "$token" ] && [ -d "$ROOT" ] && [ "$(run_token)" != "$token" ]; then
    busy "the run is another command's"
  fi
}

case "$mode" in
  --start) do_start "$token" "$login" ;;
  --stop)
    do_stop "$save" "$token" "$login"
    exit $?
    ;;
  --save-login)
    save_login
    case $? in
      0) reply '{"saved":true}' ;;
      1) fail 6 "the login was not saved (tar, zstd, rename or disk)" ;;
      *) fail 6 "no profile or no login slug to save" ;;
    esac
    ;;
  --mark-handoff)
    check_owner
    if [ -d "$ROOT" ]; then : >"$HANDOFF"; fi
    reply "{\"handed_off\":$([ -f "$HANDOFF" ] && echo true || echo false)}"
    ;;
  --clear-handoff)
    check_owner
    rm -f "$HANDOFF"
    reply '{"handed_off":false}'
    ;;
  --status)
    pid=$(running_pid)
    if [ -n "$pid" ]; then reply "{\"running\":true,\"pid\":$pid}"; else reply '{"running":false}'; fi
    ;;
esac
