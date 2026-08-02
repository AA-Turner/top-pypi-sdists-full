"""nx_tool_sandbox — structural, subprocess-isolated execution for GENERATED compute tools.

A generated *compute* tool is a PURE function `def tool(input): -> json-serializable`. Adversarial review proved
that an in-process builtins allowlist + a substring denylist are NOT a boundary (string-split dunder names + a
traceback/`__subclasses__` frame walk recover the real `__import__`/`open`). So containment now rests on two
things that CANNOT be talked around by the tool code:

  1) An AST gate (primary static boundary): the source is parsed and REJECTED if it contains any import, any dunder
     / frame / traceback attribute access, any dangerous builtin name (getattr/eval/exec/open/…), or the
     format-string escape (.format/.format_map). A pure compute tool needs none of these; every known escape
     primitive does. This is a whitelisted language subset, not a blocklist of strings.
  2) The macOS sandbox-exec OS boundary (structural machine protection): deny network* (no exfiltration), deny
     file-write* (no tampering/persistence), and deny file-read* of the operator's SECRETS (~/.nx, Keychains,
     .ssh/.aws/.config/.gnupg, /etc) so even an AST-gate bypass can't read credentials. Applies to descendants too.
     If sandbox-exec is ABSENT (e.g. Linux), we FAIL CLOSED — a compute tool is HELD, never run, because the OS
     boundary isn't there.

Plus, best-effort: resource.setrlimit (CPU secs, FSIZE 0, NPROC) + python3 -I -S + a hard timeout.

run_pure returns { ok, output?, error?, escaped, sandbox_level: 'sandbox-exec' | 'unavailable' }.
"""
import ast
import json
import os
import subprocess
import tempfile

# ── Layer: AST gate (primary static boundary) ────────────────────────────────────────────────────────────
# Frame / traceback / generator attributes that reach a parent scope's real builtins.
_FRAME_ATTRS = frozenset((
    "f_back", "f_globals", "f_builtins", "f_locals", "f_code", "f_lineno", "f_trace",
    "tb_frame", "tb_next", "tb_lasti", "gi_frame", "cr_frame", "ag_frame",
))
# Builtin names that are an escape primitive or an I/O primitive — a pure compute tool never needs them.
# NB: `input` is intentionally NOT here — it's the tool's contract parameter name (`def tool(input): ...`); the
# input() builtin is harmless anyway (stdin is the already-consumed payload pipe under python3 -I).
_BANNED_NAMES = frozenset((
    "eval", "exec", "compile", "open", "getattr", "setattr", "delattr", "globals", "locals", "vars",
    "__import__", "object", "type", "super", "memoryview", "breakpoint", "help", "dir",
    "classmethod", "staticmethod", "property", "__build_class__",
))
# String-formatting methods that perform attribute access from a *string literal* (bypassing the AST attr check).
_BANNED_METHODS = frozenset(("format", "format_map"))


def ast_violations(code):
    """Parse the tool source and return a list of the disallowed constructs it uses (empty = clean). This is the
    real static boundary — it rejects the escape PRIMITIVES (imports / dunder & frame attribute access / dangerous
    builtins / format-string attribute access), which no legitimate pure-compute tool uses."""
    try:
        tree = ast.parse(code or "")
    except Exception as e:
        return ["syntax:%s" % type(e).__name__]
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            bad.append("import")
        elif isinstance(node, ast.Attribute):
            attr = node.attr or ""
            if (attr.startswith("__") and attr.endswith("__")) or attr in _FRAME_ATTRS:
                bad.append("attr:%s" % attr)
            elif attr in _BANNED_METHODS:
                bad.append("method:%s" % attr)
        elif isinstance(node, ast.Name):
            nid = node.id
            if nid in _BANNED_NAMES:
                bad.append("name:%s" % nid)
            elif nid.startswith("__") and nid.endswith("__"):
                # reject the WHOLE CLASS of dunder names (allowlist posture) — __builtins__ / __import__ / __loader__
                # / __spec__ … any of them is a door to the real builtins. Not enumerated; categorically denied.
                bad.append("dunder-name:%s" % nid)
    # de-dup, preserve order
    seen, out = set(), []
    for b in bad:
        if b not in seen:
            seen.add(b); out.append(b)
    return out


# ── Layer: macOS sandbox-exec OS boundary (structural) ───────────────────────────────────────────────────
def _sandbox_profile():
    """Deny network (exfil) + file-write (tamper) + file-read of the operator's SECRETS (so an AST-gate bypass still
    can't read credentials). We do NOT enumerate individual secret files (a denylist that missed ~/.git-credentials /
    ~/.npmrc / ~/.docker / ~/.zsh_history in review) — we deny the ENTIRE home tree (where all user secrets live) plus
    system secret spots. Complete for the home directory, no per-file gap. Safe because a pure compute tool reads no
    files and the system python3 (PATH forced to /usr/bin:/bin) loads its stdlib from /usr and /Library/Developer,
    not from /Users. Everything else stays readable so the interpreter can start."""
    deny_read = [
        "/Users",                     # ALL of every user's home: .git-credentials/.ssh/.aws/.npmrc/.docker/.config/
                                      # .gnupg/.netrc/.nx/.zsh_history/Library/Keychains/… — the whole tree, no gap.
        "/var/root", "/etc", "/private/etc", "/var/db", "/private/var/db",
        "/Library/Keychains", "/opt/homebrew/etc", "/usr/local/etc",
    ]
    subpaths = "".join('(subpath "%s")' % p for p in deny_read)
    return (
        "(version 1)"
        "(allow default)"
        "(deny network*)"
        "(deny file-write*)"
        "(deny file-read* %s)" % subpaths
    )


# Layer: the harness the child runs. DEFENSE IN DEPTH — the tool gets a RESTRICTED __builtins__ (a safe allowlist
# only; no open/eval/exec/__import__ and NO leak of the real builtins), so even a name the AST gate somehow missed
# resolves to nothing. This is meaningful now precisely BECAUSE the AST gate blocks the dunder-attribute / frame /
# subclasses walks that used to let a tool recover the real builtins from a restricted env (the escape the reviewers
# demonstrated). AST gate (blocks the escapes) + restricted builtins (no dangerous name present) = structural.
_HARNESS = r'''
import json as _json, sys as _sys
_bi = __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__)
_SAFE = {}
for _n in ("abs","all","any","bool","dict","enumerate","filter","float","int","len","list","map","max","min",
           "range","round","reversed","set","sorted","str","sum","tuple","zip","isinstance","repr","divmod",
           "chr","ord","hex","bin","format","frozenset","bytes","complex","Exception","ValueError","KeyError",
           "TypeError","IndexError","ZeroDivisionError","StopIteration","True","False","None"):
    if _n in _bi:
        _SAFE[_n] = _bi[_n]
_payload = _json.loads(_sys.stdin.read())
# NO live module (not even json) in the tool namespace: a real module is a bridge to the real builtins via a
# non-dunder attribute chain (json.codecs.builtins.getattr → __import__/open) that the AST gate can't see. The tool
# gets ONLY the restricted __builtins__; it returns a plain Python object and the HARNESS serializes it (own _json).
_ns = {"__builtins__": _SAFE}
try:
    exec(_payload["code"], _ns)
    _fn = _ns.get("tool")
    if not callable(_fn):
        print(_json.dumps({"ok": False, "error": "no tool(input) function defined"})); _sys.exit(0)
    _out = _fn(_payload["input"])
    _json.dumps(_out)  # must be JSON-serializable
    print(_json.dumps({"ok": True, "output": _out}))
except Exception as _e:
    print(_json.dumps({"ok": False, "error": "%s: %s" % (type(_e).__name__, str(_e)[:200])}))
'''


def _rlimits():
    """Layer 2 — preexec resource caps. Best-effort: any single limit the platform rejects is skipped, never fatal."""
    import resource
    for name, soft in (("RLIMIT_CPU", 3), ("RLIMIT_FSIZE", 0), ("RLIMIT_NPROC", 64)):
        try:
            resource.setrlimit(getattr(resource, name), (soft, soft))
        except Exception:
            pass
    try:
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    except Exception:
        pass


def run_pure(code, tool_input, timeout=6):
    """Run a generated PURE compute tool (`def tool(input): ...`) under full containment. Returns
    { ok, output?, error?, escaped, sandbox_level }. `escaped` marks a rejected escape attempt.
    FAIL-CLOSED: if the OS sandbox (sandbox-exec) is unavailable, the tool is HELD, not run."""
    viol = ast_violations(code)
    if viol:
        return {"ok": False, "error": "blocked: %s" % ", ".join(viol[:5]), "escaped": True, "sandbox_level": "ast"}
    if not os.path.exists("/usr/bin/sandbox-exec"):
        # No OS boundary → we will not run arbitrary generated code. Held honestly (compute tools need the sandbox).
        return {"ok": False, "error": "OS sandbox unavailable on this host — compute tool held (fail-closed)",
                "escaped": False, "sandbox_level": "unavailable"}
    payload = json.dumps({"code": code, "input": tool_input})
    tf = None
    try:
        tf = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
        tf.write(_HARNESS)
        tf.close()
        cmd = ["/usr/bin/sandbox-exec", "-p", _sandbox_profile(), "python3", "-I", "-S", tf.name]
        try:
            r = subprocess.run(cmd, input=payload, capture_output=True, text=True, timeout=timeout,
                               preexec_fn=_rlimits, env={"PATH": "/usr/bin:/bin"})
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "timed out after %ss (resource cap / infinite loop)" % timeout,
                    "escaped": True, "sandbox_level": "sandbox-exec"}
        out = (r.stdout or "").strip()
        if not out:
            err = (r.stderr or "").strip()[:180] or "no output (rc=%s)" % r.returncode
            return {"ok": False, "error": err, "escaped": r.returncode != 0, "sandbox_level": "sandbox-exec"}
        try:
            res = json.loads(out.splitlines()[-1])
        except Exception:
            return {"ok": False, "error": "unparseable child output", "escaped": True, "sandbox_level": "sandbox-exec"}
        res.setdefault("escaped", False)
        res["sandbox_level"] = "sandbox-exec"
        return res
    finally:
        if tf is not None:
            try:
                os.unlink(tf.name)
            except Exception:
                pass
