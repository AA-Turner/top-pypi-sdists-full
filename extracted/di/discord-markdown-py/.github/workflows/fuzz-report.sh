#!/usr/bin/env bash
#
# Summarize a honggfuzz run and decide the job's verdict.
#
# honggfuzz only *nominates*: it finds candidates inside a ptraced, coverage-instrumented,
# persistent-mode process, where the fuzz target's wall-clock guard can trip on a scheduler or
# tracer stall that has nothing to do with parse cost. Every saved input is therefore replayed
# here against an uninstrumented build (fuzz/src/bin/replay.rs), and the job fails only when that
# replay reproduces. Candidates that do not reproduce are still uploaded and summarized, as a
# warning, so they can be triaged without being a red build.
#
# Usage: fuzz-report.sh <workspace-name> <replay-budget-ms>

set -uo pipefail

target=$1
budget_ms=$2

crashes="fuzz/hfuzz_workspace/crashes"
report="fuzz/hfuzz_workspace/$target/HONGGFUZZ.REPORT.TXT"
replay="./fuzz/target/release/replay"
summary="${GITHUB_STEP_SUMMARY:-/dev/stdout}"

shopt -s nullglob
inputs=("$crashes"/*)

if [ ${#inputs[@]} -eq 0 ]; then
	echo "### fuzz \`$target\`: no candidates" >> "$summary"
	exit 0
fi

reproduced=0
verdicts=()

for input in "${inputs[@]}"; do
	# `timeout` bounds an input that hangs outright; the replay aborts by itself on a panic.
	out=$(timeout 120 "$replay" "$budget_ms" "$input" 2>&1)
	status=$?
	case $status in
		0) verdict="did not reproduce" ;;
		1) verdict="**SLOW** (over ${budget_ms}ms)"; reproduced=1 ;;
		124) verdict="**HANG** (over 120s)"; reproduced=1 ;;
		*) verdict="**CRASH**"; reproduced=1 ;;
	esac
	# On a clean exit `out` is "<elapsed-ms> <bytes> <parsed-ok>"; on an abort it is whatever the
	# panic printed, which belongs in the log rather than the table.
	if [ $status -le 1 ]; then
		read -r ms bytes _ <<< "$out"
		elapsed="${ms}ms"
	else
		elapsed="n/a" bytes=$(wc -c < "$input" 2>/dev/null | tr -d ' ')
		echo "$out"
	fi
	verdicts+=("| $verdict | $elapsed | ${bytes:-?}B | \`$(basename "$input")\` |")
done

{
	if [ "$reproduced" -eq 1 ]; then
		echo "### fuzz \`$target\`: reproduced on an uninstrumented build"
	else
		echo "### fuzz \`$target\`: ${#inputs[@]} candidate(s), none reproduced"
	fi
	echo
	echo "| verdict | replay time | size | input |"
	echo "| --- | --- | --- | --- |"
	printf '%s\n' "${verdicts[@]}"
	echo
	echo "The full workspace, including every input below verbatim, is attached to this run as the"
	echo "\`fuzz-$target\` artifact."
} >> "$summary"

# Inputs are arbitrary bytes: `cat -v` keeps terminal escapes out of the log, and the base64 is
# what you feed back to `replay` locally.
for input in "${inputs[@]}"; do
	echo "::group::$(basename "$input")"
	cat -v -- "$input"
	echo
	echo "base64: $(base64 < "$input" | tr -d '\n')"
	echo "::endgroup::"
done

if [ "$reproduced" -eq 0 ]; then
	echo "::warning::fuzz $target nominated ${#inputs[@]} candidate(s), none of which reproduced" \
		"on an uninstrumented replay. Not failing the build; see the fuzz-$target artifact."
	exit 0
fi

if [ -f "$report" ]; then
	echo "::group::HONGGFUZZ.REPORT.TXT"
	cat -- "$report"
	echo "::endgroup::"
fi

echo "::error::fuzz $target found an input that reproduces on an uninstrumented replay."
exit 1
