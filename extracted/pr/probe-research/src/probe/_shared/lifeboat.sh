#!/bin/sh
# Probe's lifeboat wrapper (plan fool-proof-updates B1). FROZEN: its bytes are
# pinned by agent/tests/test_lifeboat.py (`FROZEN_WRAPPER`). It is the one piece
# every keeper unit and every session start runs whatever release is installed,
# so change it deliberately, never in passing.
#
#   /bin/sh <L>/lifeboat.sh keeper|session|cli
#
# <L> is ~/.local/state/probe/lifeboat (`probe.service.lifeboat`). It runs the
# lifeboat's own copy of handoff.py, which lives OUTSIDE every release:
# <L>/current/handoff.py, and <L>/known-good/handoff.py when current is
# missing, passes --selftest under none of the pythons below, or exits non-zero.
# Python candidates, in order: env.json's base_python, `uv python find` (asked
# only when the one before did not do), /usr/bin/python3, env.json's
# active_python; the first under which a copy passes --selftest runs it.
#
# A slot's run that started a rescue (state.json's `last_act` changed while it
# ran, and its handoff.py is still the copy that ran) is stamped
# <L>/<slot>/.acted: what promotion of current to known-good asks for.
# Two hours after current's own rescue, with state.json still behind the
# release that rescue went for, current's rescue failed: known-good runs
# instead of it until that changes.
#
# Then, for `keeper`, the active release's keeper (`<python> -I -m
# probe.service.keeper`), as the keeper unit ran it before. Every child is
# bounded, and one that will not die is left behind 30 s past its limit.
# Nothing it starts outlives it but what a hand-off detaches on purpose.
# Always exits 0.

case $1 in keeper|session|cli) trigger=$1 ;; *) exit 0 ;; esac
case $0 in */*) L=${0%/*} ;; *) L=. ;; esac
umask 077
NL='
'

# field <file> <name>: the string value of "<name>" in a small JSON file (the
# writer keeps one key per line; a compact file reads the same). Empty if none.
field() {
    [ -r "$1" ] || return 0
    sed -n 's/.*"'"$2"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$1" 2>/dev/null | head -n 1
}

# The watchdog's tick: a fifth of a second where `sleep` takes fractions (GNU,
# BSD/macOS, busybox), else a second; PER ticks make a second.
if sleep 0.0 2>/dev/null; then TICK=0.2 PER=5; else TICK=1 PER=1; fi

# bounded <seconds> <command...>: its exit status (124: given up); stopped
# (TERM, then KILL 5 s later) once it has run <seconds>, and left behind 30 s
# past them if it is still there (an uninterruptible wait in the kernel).
# Seconds are the wall clock's where `date +%s` answers (a loaded machine's
# ticks run long), never fewer than the ticks counted. This shell waits for
# the watchdog, never for the command: as it waits it reaps the command the
# moment it exits, so the watchdog sees it gone within a tick and ends (0), or
# gives up on it (3) -- no signal that a shell's `wait` may miss. The watchdog
# is never killed and waits for every `sleep` of its own, so nothing outlives
# the wrapper (a sleep left running is a process systemd finds in the stopped
# unit).
bounded() {
    limit=$1
    shift
    "$@" </dev/null &
    child=$!
    (
        began=$(date +%s 2>/dev/null)
        n=0
        spent=0
        termed=
        killed=
        while kill -0 "$child" 2>/dev/null; do
            if [ -z "$termed" ] && [ "$spent" -ge "$limit" ]; then
                kill -TERM "$child" 2>/dev/null
                termed=$spent
            elif [ -n "$termed" ] && [ -z "$killed" ] && [ "$spent" -ge $((termed + 5)) ]; then
                kill -KILL "$child" 2>/dev/null
                killed=1
            elif [ "$spent" -ge $((limit + 30)) ]; then
                exit 3
            fi
            sleep "$TICK"
            n=$((n + 1))
            if [ $((n % PER)) -eq 0 ]; then
                spent=$((n / PER))
                now=$(date +%s 2>/dev/null)
                # Whole seconds: one less than the clocks' difference is never early.
                case $began:$now in
                    *[!0-9:]* | :* | *:) ;;
                    *) [ $((now - began - 1)) -le "$spent" ] || spent=$((now - began - 1)) ;;
                esac
            fi
        done
        exit 0
    ) </dev/null >/dev/null 2>&1 &
    dog=$!
    if wait "$dog"; then
        wait "$child"
        return $?
    fi
    return 124
}

# uv_python: `uv python find`'s answer in UVPY, asked once per run at most.
UVPY=
uv_asked=
uv_python() {
    [ -z "$uv_asked" ] || return 0
    uv_asked=1
    uv=$(field "$L/env.json" uv)
    if [ -z "$uv" ] || [ ! -x "$uv" ]; then
        uv=$(command -v uv 2>/dev/null)
    fi
    if [ -n "$uv" ] && [ -x "$uv" ]; then
        out=$L/.uv-python-find.$$
        bounded 20 /bin/sh -c 'exec "$1" python find >"$2" 2>/dev/null' sh "$uv" "$out" >/dev/null 2>&1
        UVPY=$(head -n 1 "$out" 2>/dev/null)
        rm -f "$out"
    fi
}

# acts: a fingerprint of state.json's `last_act`, which a slot's lifeboat mode
# writes as it starts a rescue (and nothing else writes). Not acted.json: the
# detached rescue writes it later and the service deletes it, both at any time.
acts() {
    sed -n 's/.*"last_act"[[:space:]]*:[[:space:]]*\({[^}]*}\).*/\1/p' "$L/state.json" 2>/dev/null | cksum
}

# run_slot <slot>: 0 when the slot's handoff.py passed --selftest under one of
# the candidates and then ran in lifeboat mode with it and exited 0.
run_slot() {
    name=$1
    script=$L/$name/handoff.py
    [ -f "$script" ] || return 1
    tried=$NL
    for which in base uv system active; do
        case $which in
            base) py=$(field "$L/env.json" base_python) ;;
            uv) uv_python; py=$UVPY ;;
            system) py=/usr/bin/python3 ;;
            *) py=$(field "$L/env.json" active_python) ;;
        esac
        case $py in /*) ;; *) continue ;; esac
        case $tried in *"$NL$py$NL"*) continue ;; esac
        tried=$tried$py$NL
        [ -f "$py" ] && [ -x "$py" ] || continue
        if bounded 30 "$py" -I -S "$script" --selftest >/dev/null 2>&1; then
            copy=$(cksum <"$script" 2>/dev/null)
            before=$(acts)
            bounded 300 "$py" -I -S "$script" --lifeboat --trigger "$trigger"
            rc=$?
            if [ "$(acts)" != "$before" ] && [ "$(cksum <"$script" 2>/dev/null)" = "$copy" ]; then
                : >"$L/$name/.acted" 2>/dev/null
            fi
            return "$rc"
        fi
    done
    return 1
}

first=current
if [ -f "$L/current/.acted" ] && [ "$L/current/.acted" -nt "$L/current/handoff.py" ] \
        && [ -n "$(find "$L/current/.acted" -mmin +120 2>/dev/null)" ]; then
    behind=$(field "$L/state.json" behind_version)
    if [ -n "$behind" ] && [ "$behind" = "$(field "$L/state.json" to)" ]; then
        first=known-good
    fi
fi
if [ "$first" = known-good ]; then
    run_slot known-good || run_slot current
elif ! run_slot current; then
    run_slot known-good
fi

if [ "$trigger" = keeper ]; then
    keeper=$(field "$L/env.json" active_python)
    if [ -z "$keeper" ] || [ ! -x "$keeper" ]; then
        keeper=$(field "$L/../service/runtime.json" python)
    fi
    if [ -z "$keeper" ] || [ ! -x "$keeper" ]; then
        keeper=$HOME/.local/share/uv/tools/probe-research/bin/python
    fi
    if [ -x "$keeper" ]; then
        bounded 300 "$keeper" -I -m probe.service.keeper
    fi
fi
exit 0
