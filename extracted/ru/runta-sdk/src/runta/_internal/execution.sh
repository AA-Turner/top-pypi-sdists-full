#!/bin/sh
# SDK task supervisor. Never receives user environment variables itself.
set -u
umask 077
mode=$1
d=$2
prefix=RUNTA_EXEC_V1

identity() {
    p=$1
    [ -r "/proc/$p/stat" ] || return 1
    IFS= read -r line < "/proc/$p/stat" || return 1
    # comm may contain spaces and parentheses; starttime is field 20 after comm.
    line=${line##*) }
    set -- $line
    [ "$1" != Z ] || return 1
    shift 19
    IFS= read -r boot < /proc/sys/kernel/random/boot_id
    printf '%s %s %s\n' "$p" "$1" "$boot"
}

alive() {
    [ -f "$1" ] || return 1
    IFS=' ' read -r p ticks boot < "$1" || return 1
    current=$(identity "$p") || return 1
    [ "$current" = "$p $ticks $boot" ]
}

signal_command() {
    if alive "$d/command.identity"; then
        IFS=' ' read -r p rest < "$d/command.identity"
        # The runner stays alive after publishing its exit code, preventing PID
        # reuse while its process group (including descendants) is reclaimed.
        kill "-$1" -- "-$p" 2>/dev/null || /bin/kill "-$1" -- "-$p" 2>/dev/null || :
    fi
}

signal_reader() {
    stream=$2
    if alive "$d/$stream.reader.identity"; then
        IFS=' ' read -r p rest < "$d/$stream.reader.identity"
        kill "-$1" -- "-$p" 2>/dev/null || /bin/kill "-$1" -- "-$p" 2>/dev/null || :
    fi
}

can_cleanup_incomplete() {
    [ -f "$d/stdin.incomplete" ] && [ -f "$d/bootstrap.identity" ] &&
        ! alive "$d/bootstrap.identity" && ! alive "$d/supervisor.identity" &&
        ! alive "$d/command.identity"
}

inspect() {
    if [ -f "$d/stdin.incomplete" ]; then
        # Publishing failure precedes bootstrap exit. Keep observers waiting
        # until cleanup can safely reclaim its files, using the same startup
        # bound as an initial bootstrap (never launch the command again).
        if alive "$d/bootstrap.identity"; then
            printf '%s unknown\n' "$prefix"
        else
            printf '%s lost\n' "$prefix"
        fi
    elif [ -f "$d/result" ]; then
        cat "$d/result"
    elif [ -f "$d/supervisor.identity" ]; then
        if alive "$d/supervisor.identity"; then
            printf '%s running\n' "$prefix"
        else
            printf '%s lost\n' "$prefix"
        fi
    else
        printf '%s unknown\n' "$prefix"
    fi
}

collect() {
    stream=$1
    limit=$2
    # Read at most limit+1 bytes, then drain everything else without storing it.
    # The extra byte makes exact-boundary truncation detection unambiguous.
    # Flush every write so output() can see small writes while the task runs.
    { stdbuf -o0 head -c "$((limit + 1))" > "$d/$stream.raw"; cat > /dev/null; } < "$d/$stream.fifo"
}

finalize() {
    stream=$1
    limit=$2
    n=$(wc -c < "$d/$stream.raw")
    truncated=0
    [ "$n" -le "$limit" ] || truncated=1
    head -c "$limit" "$d/$stream.raw" > "$d/$stream"
    printf '%s\n' "$truncated" > "$d/$stream.truncated"
    rm -f "$d/$stream.raw" "$d/$stream.fifo"
}

case "$mode" in
    bootstrap_identity)
        identity "$3" > "$d/bootstrap.identity.tmp" || exit 1
        mv "$d/bootstrap.identity.tmp" "$d/bootstrap.identity"
        ;;
    collect)
        stream=$3
        trap 'exit 0' TERM INT HUP
        identity "$$" > "$d/$stream.reader.identity.tmp" || exit 1
        mv "$d/$stream.reader.identity.tmp" "$d/$stream.reader.identity"
        collect "$stream" "$4"
        ;;
    run)
        # Keep the group leader alive until the supervisor reclaims the group,
        # even if descendants ignore TERM. A caught (not ignored) signal is
        # reset to its default disposition when the user command is exec'd.
        trap ':' TERM INT HUP
        identity "$$" > "$d/command.identity.tmp" || exit 1
        mv "$d/command.identity.tmp" "$d/command.identity"
        while [ ! -f "$d/go" ]; do sleep 0.05; done
        sh "$d/command.sh" < "$d/stdin" > "$d/stdout.fifo" 2> "$d/stderr.fifo"
        rc=$?
        printf '%s\n' "$rc" > "$d/exit.tmp"
        mv "$d/exit.tmp" "$d/exit"
        while :; do sleep 1; done
        ;;
    supervise)
        limit=$3
        task_timeout=$4
        reason=completed
        out_reader=
        err_reader=
        runner=
        watchdog=
        # Failure during startup must not leave pipe readers or a runner behind.
        trap 'signal_command KILL; signal_reader KILL stdout; signal_reader KILL stderr; for child in "$out_reader" "$err_reader" "$runner" "$watchdog"; do [ -z "$child" ] || kill "$child" 2>/dev/null || :; done' 0
        trap 'reason=timed_out' USR1
        trap 'reason=cancelled' TERM INT HUP
        identity "$$" > "$d/supervisor.identity.tmp" || exit 1
        mv "$d/supervisor.identity.tmp" "$d/supervisor.identity"
        [ -f "$d/stdin.complete" ] && [ ! -f "$d/stdin.incomplete" ] || exit 1
        mkfifo "$d/stdout.fifo" "$d/stderr.fifo" || exit 1
        : > "$d/stdout.raw"
        : > "$d/stderr.raw"
        setsid sh "$d/control.sh" collect "$d" stdout "$limit" & out_reader=$!
        setsid sh "$d/control.sh" collect "$d" stderr "$limit" & err_reader=$!
        count=0
        while [ ! -f "$d/stdout.reader.identity" ] || [ ! -f "$d/stderr.reader.identity" ]; do
            count=$((count + 1))
            [ "$count" -lt 200 ] && kill -0 "$out_reader" 2>/dev/null && kill -0 "$err_reader" 2>/dev/null || exit 1
            sleep 0.05
        done
        setsid sh "$d/control.sh" run "$d" < /dev/null > /dev/null 2>&1 & runner=$!
        count=0
        while [ ! -f "$d/command.identity" ]; do
            count=$((count + 1))
            [ "$count" -lt 200 ] && kill -0 "$runner" 2>/dev/null || exit 1
            sleep 0.05
        done
        read -r started rest < /proc/uptime
        : > "$d/go"
        watchdog=
        if [ "$task_timeout" != none ]; then
            sh "$d/control.sh" deadline "$d" "$task_timeout" < /dev/null > /dev/null 2>&1 & watchdog=$!
        fi
        while [ ! -f "$d/exit" ] && [ "$reason" = completed ]; do
            if [ -f "$d/cancel" ]; then reason=cancelled; break; fi
            alive "$d/command.identity" || { reason=lost; break; }
            sleep 0.1
        done
        if [ "$reason" != completed ]; then
            signal_command TERM
            count=0
            while [ ! -f "$d/exit" ] && alive "$d/command.identity" && [ "$count" -lt 50 ]; do
                sleep 0.1
                count=$((count + 1))
            done
        fi
        signal_command KILL
        if [ -n "$watchdog" ]; then kill "$watchdog" 2>/dev/null || :; wait "$watchdog" 2>/dev/null || :; fi
        wait "$runner" 2>/dev/null || :
        # Escaped descendants can retain FIFO writers after the runner exits.
        # Give readers one second to drain, then close their owned groups and
        # finalize the bytes already captured independently of FIFO EOF.
        count=0
        while alive "$d/stdout.reader.identity" || alive "$d/stderr.reader.identity"; do
            [ "$count" -lt 20 ] || break
            sleep 0.05
            count=$((count + 1))
        done
        out_stopped=0
        err_stopped=0
        if alive "$d/stdout.reader.identity"; then out_stopped=1; signal_reader TERM stdout; fi
        if alive "$d/stderr.reader.identity"; then err_stopped=1; signal_reader TERM stderr; fi
        count=0
        while alive "$d/stdout.reader.identity" || alive "$d/stderr.reader.identity"; do
            [ "$count" -lt 10 ] || break
            sleep 0.02
            count=$((count + 1))
        done
        signal_reader KILL stdout
        signal_reader KILL stderr
        wait "$out_reader" || [ "$out_stopped" -eq 1 ] || exit 1
        wait "$err_reader" || [ "$err_stopped" -eq 1 ] || exit 1
        finalize stdout "$limit"
        finalize stderr "$limit"
        if [ "$reason" = lost ]; then
            printf '%s lost\n' "$prefix" > "$d/result.tmp"
            mv "$d/result.tmp" "$d/result"
            exit 0
        fi
        case "$reason" in
            completed) read -r rc < "$d/exit" ;;
            timed_out) rc=124 ;;
            cancelled) rc=143 ;;
            *) rc=125 ;;
        esac
        read -r out_truncated < "$d/stdout.truncated"
        read -r err_truncated < "$d/stderr.truncated"
        if [ "$reason" = timed_out ]; then
            { cat "$d/stderr"; printf 'Command timed out after %s seconds.' "$task_timeout"; } | head -c "$((limit + 1))" > "$d/stderr.raw"
            n=$(wc -c < "$d/stderr.raw")
            [ "$n" -le "$limit" ] || err_truncated=1
            head -c "$limit" "$d/stderr.raw" > "$d/stderr"
            rm -f "$d/stderr.raw"
        fi
        read -r finished rest < /proc/uptime
        duration=$(awk -v a="$started" -v b="$finished" 'BEGIN {printf "%.3f", b-a}')
        printf '%s %s %s %s %s %s\n' "$prefix" "$reason" "$rc" "$out_truncated" "$err_truncated" "$duration" > "$d/result.tmp"
        mv "$d/result.tmp" "$d/result"
        trap - 0
        ;;
    deadline)
        timer=
        trap '[ -z "$timer" ] || { kill "$timer" 2>/dev/null || :; wait "$timer" 2>/dev/null || :; }; exit 0' TERM INT HUP
        timeout --foreground --kill-after=1s "${3}s" sleep infinity & timer=$!
        wait "$timer"
        rc=$?
        if [ "$rc" -eq 124 ] && alive "$d/supervisor.identity"; then
            read -r parent rest < "$d/supervisor.identity"
            kill -USR1 "$parent"
        fi
        ;;
    watch)
        # A reconnect may race with the initial bootstrap. Wait a bounded time
        # for its supervisor, but never submit the command again.
        count=0
        while :; do
            state=$(inspect)
            case "$state" in
                "$prefix unknown")
                    count=$((count + 1))
                    if [ "$count" -ge 15 ]; then printf '%s\n' "$state"; exit 1; fi
                    printf '%s starting\n' "$prefix"
                    ;;
                "$prefix running") printf '%s\n' "$state" ;;
                "$prefix completed "*|"$prefix timed_out "*|"$prefix cancelled "*)
                    out_size=$(wc -c < "$d/stdout")
                    err_size=$(wc -c < "$d/stderr")
                    printf 'RUNTA_EXEC_RESULT_V2 %s %s %s\n' "${state#"$prefix "}" "$out_size" "$err_size"
                    cat "$d/stdout" "$d/stderr"
                    exit 0
                    ;;
                *) printf '%s\n' "$state"; exit 0 ;;
            esac
            sleep 1
        done
        ;;
    status) inspect ;;
    cancel)
        [ -f "$d/result" ] && exit 0
        alive "$d/supervisor.identity" || exit 1
        : > "$d/cancel"
        ;;
    cleanup|cleanup_incomplete)
        if [ "$mode" = cleanup_incomplete ] && [ ! -f "$d/stdin.incomplete" ]; then exit 0; fi
        if [ "$mode" = cleanup ] && [ -f "$d/result" ]; then
            :
        elif can_cleanup_incomplete; then
            read -r expected received < "$d/stdin.incomplete" || exit 1
        else
            printf 'Cannot clean up an unfinished task\n' >&2
            exit 1
        fi
        rm -rf -- "$d" || exit 1
        if [ "$mode" = cleanup_incomplete ]; then
            printf 'Incomplete execution stdin: expected %s bytes, received %s\n' "$expected" "$received"
        fi
        ;;
    *) exit 2 ;;
esac
