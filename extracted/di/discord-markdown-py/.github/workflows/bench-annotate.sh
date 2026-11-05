#!/usr/bin/env bash
#
# Post the instruction count headline of a gungraun baseline comparison as a run annotation,
# listing the five largest moves each way. Benchmarks with no main baseline count as new.
#
# Usage: bench-annotate.sh

set -euo pipefail

find target/gungraun -name summary.json -exec cat {} + | jq -rs '
  def pct: (. * 100 | round / 100) as $p | (if $p > 0 then "+" else "" end) + "\($p)%";
  def line: "  \(.diff | pct) \(.name)";
  [ .[]
    | { name: (.module_path + (if .id then "::" + .id else "" end)),
        change: (.profiles[] | select(.tool == "Callgrind") | .data.total.metrics.Ir.change) }
    | .diff = (.change.diff_pct | if . then tonumber else null end)
    | .factor = (.change.factor | if . then tonumber else null end) ]
  | map(select(.diff)) as $compared
  | ($compared | map(select(.diff > 0)) | sort_by(-.diff)) as $worse
  | ($compared | map(select(.diff < 0)) | sort_by(.diff)) as $better
  | ([ "Instructions vs main: \($worse | length) regressed, \($better | length) improved, \($compared | length - ($worse | length) - ($better | length)) unchanged"
       + (if $compared | length > 0
          then ", geomean \(($compared | map(.factor | log) | add / length | exp - 1) * 100 | pct)"
          else "" end)
       + (length - ($compared | length) | if . > 0 then ", \(.) new" else "" end) ]
     + (if $worse | length > 0 then ["", "Regressed:"] + ($worse[:5] | map(line)) else [] end)
     + (if $better | length > 0 then ["", "Improved:"] + ($better[:5] | map(line)) else [] end))
  | join("\n")
  | "::notice title=Bench comparison::" + (gsub("%"; "%25") | gsub("\r"; "%0D") | gsub("\n"; "%0A"))
'
