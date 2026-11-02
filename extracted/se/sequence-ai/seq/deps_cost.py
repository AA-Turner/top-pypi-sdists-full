"""
What a version's own copy costs, in the words `seq deploy` and `seq policy rm` / `seq benchmark rm` say it
.

A version of your own code keeps a copy of what its build installed - its base included - in your storage, so it can be
built again exactly as it is: your version dependencies, one volume billed by the GB-month, each part kept once however
many versions share it. The platform says what a copy would keep before anything is built (the dry run's
copy_estimate: its base's size read from its registry, how much of it your storage holds already, the name's last
version as measured), what it kept once the version is ready (GET .../fleet?dependencies=true), and what a delete takes
of it.
"""
from __future__ import annotations

from sequence_ai._core.money import money

_WHAT = "its version dependencies (what its build installs, its base included, kept so it can be built again as it is)"


def size(n) -> str:
    """Bytes as `seq volume ls` reads them: "222.3 MB" under a GB, "8.41 GB" from one."""
    n = float(n or 0)
    return f"{n / 1e9:.2f} GB" if n >= 1e9 else f"{n / 1e6:.1f} MB"


def _month(n, rate) -> str:
    return f"~{money(float(n or 0) / 1e9 * float(rate))}/month"


def estimate_lines(est: dict | None) -> list[str]:
    """A dry run's lines for the copy a version would keep (the platform's copy_estimate): nothing for one that keeps
    none."""
    if not est:
        return []
    rate, base, total = est.get("usd_per_gb_month"), est.get("base"), est.get("base_bytes")
    at = f" at {money(float(rate))}/GB-month" if rate is not None else ""
    if total is None:
        said = (f"its base {base} is measured by its first build" if base else
                "what it keeps is measured by its first build")
    else:
        held = est.get("held_bytes") or 0
        if held >= total:
            said = f"its base {base} ({size(total)}) is in your storage already, kept once: nothing more for it"
        elif held:
            said = (f"its base {base} is {size(total)}, {size(held)} of it in your storage already"
                    + (f" ({_month(total - held, rate)} more)" if rate is not None else ""))
        else:
            said = f"its base {base} is {size(total)}" + (f" ({_month(total, rate)})" if rate is not None else "")
    if not est.get("freeze", True):

        return [f"storage     not frozen: --freeze keeps {_WHAT}{at} - {said}, and what its steps install"]
    out = [f"storage     frozen: {_WHAT}{at}: {said}, and what its steps install"]
    last = est.get("last")
    if last and last.get("bytes") is not None:
        new = last.get("new_bytes")
        out.append(f"{'':12}its last version, v{last.get('version')}, kept {size(last['bytes'])}"
                   + (f", {size(new)} of it new to your storage" if new is not None else ""))
    return out


def kept_line(dep: dict | None) -> str | None:
    """After a deploy: the version's own copy as the platform says it (GET .../fleet?dependencies=true) - kept whole and
    what of it was new, still being kept and what its base is expected to take, or not whole and why."""
    if not dep:
        return None
    rate = dep.get("usd_per_gb_month")
    state = dep.get("dependencies_state")
    if state == "kept":
        new = dep.get("new_bytes")
        cost = f" ({_month(new, rate)} more at {money(float(rate))}/GB-month)" if rate is not None and new else ""
        return (f"  plus {_WHAT}: frozen, kept whole in your storage, {size(dep.get('dependencies_bytes'))}"
                + (f", {size(new)} of it new" if new is not None else "") + cost)
    if state == "copying":
        est = dep.get("estimate") or {}
        base = (f": its base {est['base']} is {size(est['base_bytes'])}, plus what its steps installed"
                if est.get("base") and est.get("base_bytes") is not None else "")
        at = f" at {money(float(rate))}/GB-month" if rate is not None else ""
        return f"  plus {_WHAT}: being frozen in your storage now{at}{base}"
    missing = "; ".join(str(m) for m in dep.get("not_self_contained") or []) or "not all of it could be kept"
    return f"  {_WHAT}: not fully frozen - {missing}"


def delete_line(d: dict | None) -> str | None:
    """What a delete takes of its versions' copies: all of them, but for parts another version still uses."""
    if not d or not d.get("versions"):
        return None
    each = ", ".join(f"v{r.get('version')} ({size(r.get('bytes'))})" for r in d["versions"])
    return f"delete its version dependencies - {each}; parts another version still uses stay"
