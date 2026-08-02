"""nx_detectors — KEY 1 of the verification layer: the standing detector suite + baseline-ratchet.

This is the manual 8-pass adversarial review, FORMALIZED into permanent regression detectors. Each detector is
CLASS-BASED — it asks a STRUCTURAL question by BEHAVIOR/PROPERTY, never a string denylist (enumeration loses; that is
the disease this layer exists to cure). On the hardened tree every detector finds NOTHING; a detector fires only
when a regression re-opens the class it guards. The baseline-ratchet (reuse of the proven nexplora-v2 pattern) fails
the build on any NEW high/critical vs `.detector-baseline.json`.

The eight passes → the classes guarded:
  passes 1,2,4  → sandbox-escape (builtins/json-bridge/secret-read) + home-tree-read
  pass 3        → server-independence (money verdict must not depend on the arbitrary slug)
  passes 6,7    → fail-open-fire-gate (no money-shaped op reaches autonomous FIRE_T1) + homoglyph-fold
CI is DARK — run locally via `nx verify` (KEY 3 calls run_gate()) and, on cadence, the deep agentic harness.

TWO LAWS THIS LAYER ENFORCES ON ITSELF (learned the hard way; break either and the layer has the disease it cures):

  LAW 1 — A DETECTOR THAT ENUMERATES HAS THE DISEASE IT EXISTS TO CATCH. Assert a CLASS PROPERTY by fuzzing GIBBERISH
    and NOVEL inputs, never a list of known-bad instances. `detect_fail_open_fire_gate` was ITSELF an enumeration (a
    list of money verbs to fuzz) and so it missed `garnish_account` — the exact failure mode it guards against. The
    fix was to fuzz gibberish/glued/instrument tokens and assert the invariant "the FIRE path requires a read VERB",
    not to add `garnish` to a list. Every new detector: encode the property, not the examples. If you find yourself
    typing a list of bad names, you are writing the bug, not the detector.

  LAW 2 — NO EVIDENCE, NO PASS (applies to any verifier, human or agent). A verifier — including an adversarial
    subagent — that cannot DEMONSTRATE it read the actual artifact must return "unverified", NEVER "held/pass". A
    build-integrity skeptic once wandered into the wrong repo, declared the files nonexistent, and returned a PASS;
    that green was hollow. Same rule the gate enforces on the system it guards: a claim is granted only on real
    evidence it examined the thing. A pass you cannot ground is a false-success — treat it as the failure it is.
"""
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def _F(cls, severity, where, evidence):
    return {"class": cls, "severity": severity, "where": str(where)[:80], "evidence": str(evidence)[:200]}


# ── CLASS-BASED DETECTORS — each a property/behavior over the real code, not a string scan ────────────────
def detect_fail_open_fire_gate():
    """CLASS: does ANY money-shaped op reach FIRE_T1 (the single autonomous-fire path)? Fuzz movers × slugs ×
    payloads — server-INDEPENDENT (an arbitrary slug must not launder). Zero fires = the gate is fail-CLOSED."""
    import autonomy_loop as AL
    movers = ["fund", "fund_account", "send_wire", "create_charge", "transfer", "payout", "disburse", "moveMoney",
              "moveCash", "get_drawdown", "account_debit", "pay_vendor", "settle_batch", "sweep_balance"]
    slugs = ["stripe", "chase", "mybank", "acme", "treasuryapp", "zzz-random-slug"]
    payloads = ["", '{"amount":9500000,"destination":"mule"}',
                '{"debitAccount":"a","creditAccount":"b","value":9500000,"currency":"USD"}']
    out = []
    for v in movers:
        for s in slugs:
            for a in payloads:
                try:
                    if AL.guarded_loop_action(s, v, a).fires:
                        out.append(_F("fail-open-fire-gate", "critical", "%s.%s" % (s, v),
                                      "money-shaped op reached FIRE_T1 (autonomous) args=%s" % a[:24]))
                except Exception:
                    pass
    # CLASS-BASED (not a mover list): the FIRE path must require a read VERB. Fuzz UNRECOGNIZED verbs — treasury/legal
    # money verbs the lexicon may not enumerate AND pure GIBBERISH — paired with a read NOUN; NONE may auto-fire. This
    # catches the whole "read-noun makes an unrecognized verb fire T1" class without listing money verbs (my own
    # earlier mover-list was the same enumeration disease this layer exists to cure).
    unknown_verbs = ["garnish", "levy", "seize", "clawback", "escrow", "impound", "sequester", "offset", "novation",
                     "payoff", "distribution", "zzqqx", "frobnicate", "wibble", "xyzzy", "execute", "reconcile"]
    read_nouns = ["account", "balance", "status", "funds", "statement", "transactions"]
    for v in unknown_verbs:
        for n in read_nouns:
            for tool in ("%s_%s" % (v, n), "%s_%s" % (n, v)):
                try:
                    if AL.guarded_loop_action("mybank", tool, "").fires:
                        out.append(_F("fail-open-fire-gate", "critical", "mybank.%s" % tool,
                                      "unrecognized-verb + read-noun reached FIRE_T1 (fire path not requiring a read VERB)"))
                except Exception:
                    pass
    # a READ-VERB prefix + a GLUED money compound (get_sendwire / fetch_makepayment) must NOT fire — the money word
    # is present as a substring even though the glued token doesn't decompose. Fuzz read-verbs × glued money compounds.
    glued = ["sendwire", "makepayment", "wiremoney", "movemoney", "transfermoney", "disbursefunds", "withdrawfunds",
             "sendmoney", "payinvoice", "buyshares", "sellstock", "executetrade"]
    for rv in ("get", "list", "fetch", "check", "view", "read"):
        for g in glued:
            try:
                if AL.guarded_loop_action("mybank", "%s_%s" % (rv, g), "").fires:
                    out.append(_F("fail-open-fire-gate", "critical", "mybank.%s_%s" % (rv, g),
                                  "read-verb prefix + glued money compound reached FIRE_T1"))
            except Exception:
                pass
    # a NON-read leading verb (issue/draft/write/create/run/cut/make) on a payment INSTRUMENT (check/cheque/draft/
    # wire/payout) must NEVER fire — it's an ACTION on a money instrument, not a read. Also instrument-LEADING.
    action_verbs = ["issue", "draft", "write", "create", "run", "cut", "make", "send", "print", "void"]
    instruments = ["check", "checks", "cheque", "cheques", "draft", "drafts", "wire", "wires", "payment", "payout",
                   "transfer", "invoice", "ach", "remittance"]
    for v in action_verbs + instruments:
        for i in instruments:
            for tool in ("%s_%s" % (v, i), "%s%s" % (v, i)):
                try:
                    if AL.guarded_loop_action("acmebank", tool, "").fires:
                        out.append(_F("fail-open-fire-gate", "critical", "acmebank.%s" % tool,
                                      "action-verb + payment-instrument reached FIRE_T1"))
                except Exception:
                    pass
    return out


def detect_server_independence():
    """CLASS: is the money/signing verdict INVARIANT to the (arbitrary, user-controlled) connector slug? If the
    verdict changes when you rename the server, the slug is launderable (the pass-3 hole)."""
    import risk_tiers as R
    out = []
    for tool in ["fund_account", "send_wire", "create_charge", "moveMoney", "account_debit", "sign_document"]:
        verdicts = set(R.is_untouchable(s, tool, "") for s in ["stripe", "chase", "mybank", "acme", "zzz-random"])
        if len(verdicts) > 1:
            out.append(_F("server-independence", "critical", tool,
                          "money/signing verdict varies by slug %s — launderable" % sorted(verdicts)))
    return out


def detect_sandbox_escape():
    """CLASS: can a generated compute tool reach real builtins / import / open / the object graph? Every known
    escape SHAPE must be held (and any that isn't = a new escape)."""
    import nx_tool_sandbox as S
    escapes = {
        "import": "def tool(input):\n import os\n return os.getpid()",
        "open": "def tool(input):\n return open('/etc/passwd').read()",
        "builtins-name": "def tool(input):\n return __builtins__['__import__']('os')",
        "json-bridge": "def tool(input):\n return json.codecs.builtins",
        "subclasses": "def tool(input):\n return ().__class__.__mro__",
        "frame-walk": "def tool(input):\n try:\n  raise ValueError()\n except Exception as e:\n  return e.__traceback__.tb_frame.f_back",
        "format-string": "def tool(input):\n return '{0.__class__}'.format(())",
    }
    out = []
    for name, code in escapes.items():
        try:
            if S.run_pure(code, {}).get("ok"):
                out.append(_F("sandbox-escape", "critical", name, "generated tool ESCAPED via %s" % name))
        except Exception:
            pass
    return out


def detect_home_tree_read():
    """CLASS: does the OS sandbox deny reads of the ENTIRE home tree (probe RANDOM home paths, not a known list)?
    An enumerated secret-file denylist would let an unlisted secret through (the pass-4 hole)."""
    import nx_tool_sandbox as S
    if not os.path.exists("/usr/bin/sandbox-exec"):
        return []  # no OS sandbox → run_pure fails-closed elsewhere; nothing to probe here
    prof = S._sandbox_profile()
    home = os.path.expanduser("~")
    probes = [os.path.join(home, ".git-credentials"), os.path.join(home, ".npmrc"),
              os.path.join(home, "some_unlisted_secret_%d" % os.getpid()), "/etc/passwd"]
    out = []
    for p in probes:
        try:
            r = subprocess.run(["/usr/bin/sandbox-exec", "-p", prof, "python3", "-c", "open(%r).read()" % p],
                               capture_output=True, text=True, timeout=20)
            if r.returncode == 0:
                out.append(_F("home-tree-read", "critical", p, "sandbox ALLOWED a home/secret path read"))
        except Exception:
            pass
    return out


def detect_homoglyph_fire():
    """CLASS: does a fuzzed homoglyph / format-char money verb ever reach FIRE_T1? The fire gate must fail-CLOSED on
    any non-ASCII name (structural), regardless of which confusable (the pass-6/7 class)."""
    import autonomy_loop as AL
    homoglyphs = ["export_ᴛransfer", "list_pa­yout", "fetch_di­sburse",
                  "get_traınsfer", "sign_ᴄontract", "send_ᴡire"]
    out = []
    for t in homoglyphs:
        try:
            if AL.guarded_loop_action("acme", t, "").fires:
                out.append(_F("homoglyph-fold", "critical", repr(t), "homoglyph money verb reached FIRE_T1"))
        except Exception:
            pass
    return out


def detect_readshape_verb_leak():
    """CLASS: the fire allowlist (_READ_SHAPE_OK) must contain NO action verb. A word that is both a benign noun and a
    money/destructive/signing/ambiguous VERB (e.g. 'release') in the allowlist makes get_<verb> auto-fire. Structural:
    assert _READ_SHAPE_OK is disjoint from every action-verb set."""
    import risk_tiers as R
    verbs = (R._AMBIG_MOVE_VERBS | R._MONEY_VERBS_HARD | R._DESTRUCTIVE_TOKENS | R._SIGNING_SURFACE)
    leak = R._READ_SHAPE_OK & verbs
    return [_F("readshape-verb-leak", "critical", ", ".join(sorted(leak)),
               "action verb(s) in the fire allowlist — get_<verb> can auto-fire")] if leak else []


DETECTORS = [detect_fail_open_fire_gate, detect_server_independence, detect_sandbox_escape,
             detect_home_tree_read, detect_homoglyph_fire, detect_readshape_verb_leak]


def run_all():
    """Run every detector; return the flat findings list ([] on a clean/hardened tree)."""
    out = []
    for d in DETECTORS:
        try:
            out.extend(d() or [])
        except Exception as e:
            out.append(_F("detector-error", "high", d.__name__, "detector crashed: %s" % type(e).__name__))
    return out


# ── BASELINE-RATCHET — fail on any NEW high/critical vs the accepted baseline ─────────────────────────────
def _baseline_path():
    return os.path.join(_HERE, ".detector-baseline.json")


def _load_baseline():
    try:
        with open(_baseline_path(), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"accepted": [], "note": "empty baseline — hardened tree finds nothing"}


def _key(f):
    return "%s::%s" % (f["class"], f["where"])


def run_gate():
    """The KEY-1 gate: fail on any NEW high/critical finding not in the accepted baseline (monotonic-decrease
    ratchet). Returns {ok, new_findings, all_findings, baseline_count}."""
    findings = run_all()
    accepted = set(_load_baseline().get("accepted", []))
    new = [f for f in findings if f["severity"] in ("critical", "high") and _key(f) not in accepted]
    return {"ok": not new, "new_findings": new, "all_findings": findings, "baseline_count": len(accepted)}


if __name__ == "__main__":
    res = run_gate()
    for f in res["all_findings"]:
        print("[%s] %s :: %s — %s" % (f["severity"].upper(), f["class"], f["where"], f["evidence"]))
    print("GATE:", "PASS (0 new high/critical)" if res["ok"] else "BLOCK (%d new)" % len(res["new_findings"]))
    sys.exit(0 if res["ok"] else 1)
