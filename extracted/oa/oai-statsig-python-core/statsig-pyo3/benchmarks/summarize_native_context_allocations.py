"""Symbolize native allocation stacks using the recorded ELF load bias.

The benchmark/probe must produce sdk-{baseline,candidate}.stacks and .maps.
"""

import argparse
import collections
import json
import pathlib
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("artifact_directory", type=pathlib.Path)
root = parser.parse_args().artifact_directory
for variant in ("baseline", "candidate"):
    stack_path = root / f"sdk-{variant}.stacks"
    maps = []
    for line in pathlib.Path(str(stack_path) + ".maps").read_text().splitlines():
        parts = line.split(maxsplit=5)
        if len(parts) == 6 and "statsig_python_core.abi3.so" in parts[-1]:
            left, right = (int(v, 16) for v in parts[0].split("-"))
            maps.append((left, right, int(parts[2], 16), parts[-1]))
    assert maps and maps[0][2] == 0, "Expected a zero-offset ELF mapping"
    stacks = []
    addresses = set()
    for line in stack_path.read_text().splitlines():
        size, *raw = line.split()
        native = []
        for value in raw:
            if value == "(nil)":
                continue
            address = int(value, 16)
            for left, right, offset, binary in maps:
                if left <= address < right:
                    relative = address - maps[0][0] - 1
                    native.append(relative)
                    addresses.add(relative)
                    break
        stacks.append((int(size), native))
    addresses = sorted(addresses)
    result = subprocess.run(
        ["addr2line", "-f", "-C", "-e", maps[0][3]],
        input="\n".join(hex(a) for a in addresses) + "\n",
        text=True,
        check=True,
        capture_output=True,
    ).stdout.splitlines()
    symbols = {
        addr: {"function": result[2 * i], "source": result[2 * i + 1]}
        for i, addr in enumerate(addresses)
    }
    innermost = collections.Counter()
    constructor = 0
    native_samples = 0
    expanded = []
    for size, stack in stacks:
        functions = [symbols[addr]["function"] for addr in stack]
        if functions:
            native_samples += 1
            innermost[functions[0]] += 1
        if any("newfunc::inner" in f for f in functions):
            constructor += 1
        expanded.append(
            {"requested_bytes": size, "stack": [symbols[addr] for addr in stack]}
        )
    summary = {
        "variant": variant,
        "sampled_allocation_requests": len(stacks),
        "native_stack_samples": native_samples,
        "python_native_constructor_boundary_samples": constructor,
        "metadata_converter_inclusive_samples": sum(
            any("pyo_utils::" in f["function"] for f in row["stack"])
            for row in expanded
        ),
        "innermost_native_frame_counts": innermost.most_common(30),
        "native_symbol_addresses": len(symbols),
    }
    (root / f"sdk-{variant}-allocation-profile-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    (root / f"sdk-{variant}-allocation-stacks-symbolized.json").write_text(
        json.dumps(expanded, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))
