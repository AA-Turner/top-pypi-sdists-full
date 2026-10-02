#!/usr/bin/python3
"""Check every wrapper calls its own module, with options it accepts.

    python check_wrappers.py pikobs/script

Two wrappers turned out to be copies of another module's: run_cardio.sh
was run_zone.sh and run_flags.sh was run_mapobs.sh, header and all. Both
had been there for months, because a wrapper that calls the wrong module
still runs -- it just produces the wrong thing, or dies on an option the
module has never heard of.

For each run_<name>*.sh this reads which arg_call it invokes and which
options it passes, and compares them with what that module's arg_call
actually declares. It reports three things:

  calls <other>     the wrapper runs a different module than its name says
  unknown option    an option the module's parser would reject
  header says       the banner at the top names another wrapper
  how-to names      a wget, chmod +x or ./ line of the comments names
                    another wrapper (the banner can be right and the
                    instructions still send people to the wrong file)

It only reads; nothing is modified.
"""

import os
import re
import sys
import textwrap


def module_options(module: str):
    """Every option the module's parser accepts.

    Read with ast, not with a regular expression: pikobsburp2rdb and
    spatial write their add_argument calls across several lines and with
    keywords in between, and a pattern that misses them makes the check
    shout at wrappers that are perfectly fine. A checker that cries wolf
    gets ignored, which is worse than having none.
    """
    import ast
    import importlib
    import inspect
    try:
        mod = importlib.import_module(f"pikobs.{module}")
        src = inspect.getsource(mod.arg_call)
    except Exception as exc:
        return None, f"cannot read pikobs.{module}.arg_call ({exc})"
    try:
        tree = ast.parse(textwrap.dedent(src))
    except SyntaxError as exc:
        return None, f"cannot parse pikobs.{module}.arg_call ({exc})"
    opts = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if getattr(node.func, 'attr', None) != 'add_argument':
            continue
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) \
                    and arg.value.startswith('--'):
                opts.add(arg.value)
        # --foo declared only through dest=
        for kw in node.keywords:
            if kw.arg == 'dest' and isinstance(kw.value, ast.Constant):
                opts.add('--' + str(kw.value.value))
    return opts, None


def main(argv=None) -> int:
    folder = (argv or sys.argv[1:] or ["pikobs/script"])[0]
    cache = {}
    problems = 0

    for name in sorted(os.listdir(folder)):
        if not (name.startswith("run_") and name.endswith(".sh")):
            continue
        path = os.path.join(folder, name)
        src = open(path).read()
        called = re.search(r"pikobs\.([a-z0-9_]+)\.arg_call", src)
        if not called:
            continue
        module = called.group(1)

        # the name the wrapper claims, stripped of the usual suffixes
        stem = re.sub(r"^run_|\.sh$", "", name)
        stem = re.sub(r"_(exp|cont_exp|check|radar|para|sky|lco\d*|ic5.*|"
                      r"\d+|[a-z]{1,3}\d*)$", "", stem)

        notes = []
        if stem and stem != module and not stem.startswith(module):
            notes.append(f"calls {module}, its name says {stem}")

        header = re.search(r"^# (run_[a-z0-9_]+\.sh)\s*$", src, re.M)
        if header and header.group(1) != name:
            notes.append(f"header says {header.group(1)}")

        # the "How to run" block: every wget / chmod / ./ in the comments
        # must name this very file. Twelve pair wrappers had the right
        # banner and still told people to fetch the plain run_<module>.sh.
        howto = set(re.findall(
            r"^#.*?(?:/|chmod \+x |\./)(run_[a-z0-9_]+\.sh)\b", src, re.M))
        others = sorted(howto - {name})
        if others:
            notes.append("how-to names " + ", ".join(others))

        if module not in cache:
            cache[module] = module_options(module)
        opts, err = cache[module]
        if err:
            notes.append(err)
        else:
            passed = set(re.findall(r"^\s+(--[a-z_0-9]+)", src, re.M))
            unknown = sorted(passed - opts)
            if unknown:
                notes.append("unknown option(s): " + ", ".join(unknown))

        if notes:
            problems += 1
            print(f"{name}")
            for n in notes:
                print(f"    {n}")

    print(f"\n{problems} wrapper(s) worth a look")
    return 0


if __name__ == "__main__":
    sys.exit(main())
