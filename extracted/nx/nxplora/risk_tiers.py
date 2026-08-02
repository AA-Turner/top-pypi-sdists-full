"""risk_tiers.py — the SINGLE SOURCE OF TRUTH for connected-integration tool risk.

FAIL-CLOSED BY CONSTRUCTION. A tool is SAFE only when it POSITIVELY matches a known-safe shape (a read/analysis,
or a reversible internal create/update on a non-money server). EVERYTHING ELSE — money movement, outward sends,
deletes, permission changes, AND anything unrecognized/new/typo'd — resolves DESTRUCTIVE. This is the inverse of a
blocklist: the guarantee cannot be defeated by a missing string, because the DEFAULT is DESTRUCTIVE.

Two enforcement postures compose the SAME resolver (see is_allowed):
  * interactive operator      → DESTRUCTIVE needs explicit operator approval (the caller gates it y/n).
  * sub-agent (is_subagent)   → DESTRUCTIVE is DENIED outright, no approval path — so a sub-agent's usable tools
    are SAFE-only BY CONSTRUCTION. This is the property the swarm inherits: 15 sub-agents, none can reach money.

No side effects, stdlib-only — meant to be audited in one sitting and composed by both the shipped CLI tool-loop
and (Phase 2) the sub-agent spawn path.
"""
import re as _re
import unicodedata as _ud

SAFE = "SAFE"
DESTRUCTIVE = "DESTRUCTIVE"

# Common Cyrillic / Greek characters that LOOK like ASCII letters — folded to ASCII so a whole-token verb match
# ('charge', 'sign', 'delete') can't be dodged by spelling it with a lookalike (e.g. Cyrillic а/е/о/р/с/х).
_CONFUSABLES = {
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y", "к": "k", "м": "m", "т": "t",
    "н": "h", "в": "b", "ѕ": "s", "і": "i", "ј": "j", "ԁ": "d", "ё": "e", "А": "a", "Е": "e", "О": "o",
    "Р": "p", "С": "c", "Х": "x", "α": "a", "ε": "e", "ο": "o", "ρ": "p", "χ": "x", "υ": "u", "ι": "i",
    "κ": "k", "ν": "v", "τ": "t", "Α": "a", "Ε": "e", "Ο": "o", "Ρ": "p",
}


def _fold(s):
    """Normalize homoglyph / compatibility evasion so whole-token verb matching can't be dodged. STRUCTURAL, not a
    lookalike table: NFKD (folds fullwidth ａ→a), strip combining marks (Mn: í→i) AND format chars (Cf: soft-hyphen,
    ZWSP — invisible word-splitters), then transliterate ANY remaining non-ASCII LETTER via its Unicode NAME's base
    letter — 'LATIN SMALL LETTER DOTLESS I'→i, 'LATIN LETTER SMALL CAPITAL T'→t, 'CYRILLIC SMALL LETTER A'→a. This
    covers dotless-ı, small-caps, Cyrillic/Greek/Armenian/Cherokee lookalikes without enumerating any of them. A
    letter whose name doesn't end in a single ASCII letter is left as-is and caught by the is_read_only non-ASCII
    guard (never auto-fires)."""
    s = _ud.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if _ud.category(c) not in ("Mn", "Cf"))
    out = []
    for c in s:
        if ord(c) < 128:
            out.append(c); continue
        m = _CONFUSABLES.get(c)
        if m:
            out.append(m); continue
        if _ud.category(c).startswith("L"):
            try:
                last = _ud.name(c).split()[-1]
            except (ValueError, Exception):
                last = ""
            if len(last) == 1 and "A" <= last <= "Z":
                out.append(last.lower()); continue
        out.append(c)   # non-letter or unnameable → leave; is_read_only's non-ASCII guard backstops it
    return "".join(out)

# ── POSITIVE safe signals — a tool is SAFE only if one of its name-tokens is in one of these sets ─────────────
# Reads + non-mutating analysis (broad, so ordinary reads aren't needlessly gated — but still a closed set).
_SAFE_READ = frozenset((
    "get", "list", "search", "read", "fetch", "find", "query", "retrieve", "describe", "show", "count", "view",
    "lookup", "export", "whoami", "history", "summary", "info", "details", "detail", "status", "balance",
    "account", "me", "self", "hierarchy", "research", "analyze", "analyse", "summarize", "summarise", "preview",
    "check", "inspect", "audit", "monitor", "measure", "ping", "resolve", "validate", "verify", "explore",
    "scan", "discover", "browse", "compare", "diff", "stat", "stats", "metrics", "report", "download", "current",
    "filter",   # non-mutating: returns a subset of records (clickup_filter_tasks etc.) — a read, not a write.
))
# Reversible INTERNAL writes — only trusted on NON money/send servers (on money/send, only a read is auto-safe).
_SAFE_WRITE = frozenset((
    "create", "update", "add", "save", "new", "edit", "comment", "upload", "set", "append", "tag", "label",
    "mark", "assign", "draft", "note", "attach", "duplicate", "rename", "generate", "render", "compose",
    "format", "convert", "reply", "annotate", "move",
))
# Whole-token destructive/outward verbs — DESTRUCTIVE on ANY server even if a safe token co-occurs (e.g.
# get_and_delete). Whole-token (not substring) so a READ like get_closed_deals / list_refunds is NOT tripped.
_DESTRUCTIVE_TOKENS = frozenset((
    "delete", "destroy", "purge", "truncate", "erase", "wipe", "revoke", "deactivate", "disable", "suspend",
    "terminate", "send", "email", "publish", "dispatch", "sms", "cancel", "void", "unsubscribe", "remove",
    "archive", "trash", "grant", "ban", "kick", "invite", "merge", "overwrite", "chargeback", "refund",
    "payout", "transfer", "withdraw", "charge", "capture", "checkout", "pay", "payment", "wire", "disburse",
    "share", "revoked", "deprovision", "unpublish", "block",
))
# Servers where a MUTATION moves money / sends outward / is public — on these, ONLY a clear read is SAFE.
_MONEY_SEND_SERVERS = (
    "stripe", "paypal", "square", "mercury", "brex", "ramp", "quickbooks", "xero", "plaid", "wise", "gusto",
    "bill", "billcom", "adyen", "checkout", "gocardless", "melio", "tipalti",
    "rippling", "gmail", "googlemail", "google", "outlook", "sendgrid", "mailgun", "mailchimp", "twilio",
    "slack", "discord", "telegram", "whatsapp", "twitter", "linkedin", "facebook", "instagram", "tiktok",
    "youtube", "ebay", "shopify",
)
# Mutation / money-payload hints scanned in the ARGS of a call (op names, HTTP verbs, AND money-transfer field
# names). A plain read of charges won't match; a transfer payload ({amount, destination, recipient, iban, …}) WILL,
# so a benign-NAMED op that carries a money payload still re-arms the T3 gate.
_MONEY_MUTATE = (
    "create", "update", "delete", "cancel", "refund", "capture", "confirm", "void", "payout", "transfer",
    "checkout", "subscription", "\"post\"", "\"put\"", "\"patch\"", "\"delete\"", "method\":\"post",
    "method\":\"put", "method\":\"patch", "method\":\"delete",
    # money-transfer PAYLOAD field names — the presence of these in the args means real value is moving.
    "amount", "destination", "recipient", "payee", "beneficiary", "iban", "routing", "sortcode", "sort_code",
    "swift", "accountnumber", "account_number", "walletaddress", "wallet_address", "quantity_usd", "notional",
)


def resolve_tier(server, tool, args=""):
    """SAFE vs DESTRUCTIVE — FAIL CLOSED (unknown / unrecognized → DESTRUCTIVE)."""
    tool, server, args = _fold(tool), _fold(server), _fold(args)   # defeat homoglyph/compat evasion first
    a = str(args or "").lower()
    s = _re.sub(r"[^a-z0-9]", "", str(server or "").lower())
    _camel = _re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(tool or ""))   # split camelCase (authStatus → auth Status)
    tokens = frozenset(x.lower() for x in _re.split(r"[^A-Za-z0-9]+", _camel) if x)
    read_ish = bool(tokens & _SAFE_READ)
    money = any(s == m or s.startswith(m) for m in _MONEY_SEND_SERVERS)
    # 1) money/send server: SAFE only for a clear read with no mutation hinted in the args; else DESTRUCTIVE.
    if money:
        return SAFE if (read_ish and not any(k in a for k in _MONEY_MUTATE)) else DESTRUCTIVE
    # 2) any explicit destructive/outward verb token → DESTRUCTIVE.
    if tokens & _DESTRUCTIVE_TOKENS:
        return DESTRUCTIVE
    # 3) positively safe (a read/analysis, or a reversible internal write) → SAFE.
    if read_ish or (tokens & _SAFE_WRITE):
        return SAFE
    # 4) UNRECOGNIZED / new / typo'd tool → FAIL CLOSED.
    return DESTRUCTIVE


def is_read_only(server, tool, args=""):
    """A CLEAR read — the ONLY thing an autonomous loop fires. True iff a _SAFE_READ token is present AND no
    destructive/outward verb co-occurs AND (on a money/send server) no mutation is hinted in the args. A
    reversible SAFE *write* (create / update / add / …) returns False — resolve_tier calls it SAFE, but the
    loop must STAGE it, not fire it. This is stricter than SAFE: SAFE = read ∪ reversible-write; read_only = read."""
    # Check the ORIGINAL name for ANY non-ASCII BEFORE folding: a homoglyph that folds cleanly to a benign-looking
    # ASCII word (get_traınsfer → get_trainsfer) would otherwise pass the post-fold guard AND dodge the money vocab
    # → autonomous FIRE_T1. Any non-ASCII in the raw tool name = obfuscation → never auto-fire (stage it). Structural.
    if any(ord(c) > 127 for c in str(tool or "")):
        return False
    tool, server, args = _fold(tool), _fold(server), _fold(args)   # defeat homoglyph/compat evasion first
    # STRUCTURAL FAIL-CLOSE on the single autonomous-fire gate: a tool name that still holds a NON-ASCII letter
    # after folding is a homoglyph/obfuscation we can't cleanly classify (ᴛransfer, ᴡire, small-cap/phonetic
    # Unicode) — NEVER auto-fire it; let it STAGE for approval instead. Closes the whole unicode-evasion→T1 class
    # without enumerating every confusable.
    if any(ord(c) > 127 for c in str(tool or "")):
        return False
    a = str(args or "").lower()
    s = _re.sub(r"[^a-z0-9]", "", str(server or "").lower())
    _camel = _re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(tool or ""))
    if _has_money_substr(tool):
        return False   # a money word ANYWHERE in the name (incl. a glued compound like get_sendwire) → never auto-fire
    tokens = frozenset(x.lower() for x in _re.split(r"[^A-Za-z0-9]+", _camel) if x)
    # STRUCTURAL: the single autonomous-fire gate requires a read VERB (get/list/fetch/…), NOT merely a read NOUN.
    # A read noun alone (account/balance/status) paired with ANY unrecognized verb — garnish_account, seize_account,
    # levy_account, a treasury/legal verb the money lexicon hasn't enumerated — must NOT auto-fire. This closes the
    # whole "read-noun makes an unrecognized mover fire T1" CLASS without enumerating money verbs (the lesson: the
    # money lexicon can lag, but the FIRE path must never fire on an unrecognized verb — only on a recognized read).
    # The LEADING token must be a read VERB (get_/list_/fetch_/…). A non-read leading verb means it's an ACTION on a
    # target, not a read of one — issue_check / draft_check / garnish_account / remunerate_x lead with a non-read
    # verb, so they never qualify as a read. Positional (not set membership) so a money noun that's also a read verb
    # elsewhere can't launder by position.
    _ordered = [x.lower() for x in _re.split(r"[^A-Za-z0-9]+", _camel) if x]
    if not _ordered or _ordered[0] not in _SAFE_READ_VERBS:
        return False
    if tokens & _DESTRUCTIVE_TOKENS:
        return False                                   # a read token co-occurring with delete/send/… → not read-only
    # A money mutation OR a money-shaped PAYLOAD in the args → NOT an autonomous-fire read, on ANY server (a benign
    # read-verb name like get_result carrying {debitAccount, creditAccount, value, currency} is a laundered transfer).
    if any(k in a for k in _MONEY_MUTATE) or _args_look_monetary(a):
        return False
    # FAIL-CLOSED ALLOWLIST (the structural end of glued-money laundering): EVERY token must be a recognized-safe read
    # token. A glued/unknown compound (sendwire / payinvoice / buyshares) is NOT in _READ_SHAPE_OK, so a get_-prefixed
    # money action can NEVER auto-fire — no money-word enumeration required. Missing a benign noun over-STAGES a read
    # (safe); it can never fire an unrecognized op. This is the inverse of the money denylist that kept losing.
    if tokens - _READ_SHAPE_OK:
        return False
    return True


def is_allowed(server, tool, args="", is_subagent=False):
    """(allowed_without_approval: bool, tier: str).
    SAFE                      → (True,  SAFE)         runs freely.
    DESTRUCTIVE + is_subagent → (False, DESTRUCTIVE)  HARD DENY — no approval path (the structural sub-agent wall).
    DESTRUCTIVE + interactive → (False, DESTRUCTIVE)  caller must gate through operator approval."""
    tier = resolve_tier(server, tool, args)
    return (tier == SAFE), tier


# ── T3 UNTOUCHABLES — money MOVEMENT + signing / legal execution ──────────────────────────────────────────────
# These are NOT merely DESTRUCTIVE (which is per-op approvable): they MOVE REAL FUNDS or LEGALLY BIND, so they
# are FOUNDER-ONLY and must NEVER fire autonomously — no agent / --approve / lane / flight / tier can authorize
# one. This is the READY structural guard the autonomy loop (grail phase #4) is born on: the caller checks
# is_untouchable() FIRST at the single execution chokepoint, so money/signing is unreachable-by-construction from
# any autonomous context. FAIL-SAFE toward T3 on the money/signing surface (unknown money/signing-ish → T3), but
# a CLEAR READ is never T3.
#
# Distinct from _MONEY_SEND_SERVERS (which also lists outward-SEND like gmail/slack — those are T2, per-op, not
# fund movement): _MONEY_MOVE_SERVERS is ONLY the actual fund-movers (banks / PSPs / payroll / ledgers).
_MONEY_MOVE_SERVERS = (
    "stripe", "paypal", "square", "mercury", "brex", "ramp", "quickbooks", "xero", "plaid", "wise", "gusto",
    "rippling", "revolut", "adyen", "gocardless", "razorpay", "coinbase", "moderntreasury", "airwallex",
    "melio", "billcom", "dwolla", "checkoutcom", "braintree", "chargebee", "recurly", "paddle", "lemonsqueezy",
    "column", "unit", "increase", "marqeta", "nium", "currencycloud", "wire", "ach",
)
# E-signature / legal-execution platforms — a NON-READ op here is binding-adjacent → T3.
_SIGNING_SERVERS = (
    "docusign", "hellosign", "dropboxsign", "adobesign", "adobeacrobatsign", "acrobatsign", "pandadoc",
    "signrequest", "signeasy", "echosign", "eversign", "signnow", "onespan", "signwell", "docsketch", "concord",
)
# Whole-token money-MOVEMENT verbs — moving real funds. Money NOUNS (payment/charge) also appear in READS
# (get_charge); is_untouchable exempts a clear read BEFORE checking these, so a lookup is never tripped.
_MONEY_MOVE_TOKENS = frozenset((
    "charge", "charges", "transfer", "transfers", "wire", "wires", "payout", "payouts", "disburse",
    "disbursement", "disbursements", "chargeback", "refund", "refunds", "remit", "remittance", "payroll",
    "payrun", "ach", "sepa", "swift", "withdrawal", "topup", "payment", "payments", "pay", "deposit", "wired",
))   # 'capture'/'settle' intentionally OMITTED here (ambiguous: capture-screenshot); the fund-mover-server
     # rule (§4) still catches capture_payment / settle_batch on a real PSP — so they're T3 where it matters.
# Whole-token signing / legal-execution verbs → T3 on ANY server (whole-token so 'assign'/'redesign' don't trip).
_SIGNING_TOKENS = frozenset((
    "sign", "signed", "esign", "esignature", "countersign", "notarize", "notarise", "signature", "signatures",
))
# The MOVEMENT verbs among the money tokens — everything EXCEPT the pure lookup-NOUNS (charge/payment), which legit
# reads use (get_charge / list_payments). A read token does NOT exempt when one of THESE co-occurs (a 'get' prefix
# can't launder 'refund'/'wire'/'payout'/'payroll'/…). Nouns stay readable; movement never gets exempted.
_MONEY_MOVE_VERBS = _MONEY_MOVE_TOKENS - frozenset(("charge", "charges", "payment", "payments"))

# The VERB subset of _SAFE_READ (the action words that make an op a read) vs the NOUN subset (targets/context).
# On a fund-mover / signing server we require a read VERB + a fully-recognized shape — a read NOUN alone
# (account/balance/status) must NOT exempt, or 'fund_account' / 'account_sweep' launder a move past T3.
_SAFE_READ_VERBS = frozenset((
    "get", "list", "search", "read", "fetch", "find", "query", "retrieve", "describe", "show", "count", "view",
    "lookup", "export", "research", "analyze", "analyse", "summarize", "summarise", "preview", "inspect",
    "audit", "monitor", "measure", "ping", "resolve", "validate", "verify", "explore", "scan", "discover",
    "browse", "compare", "diff", "report", "download", "filter",
    # NB: 'check' deliberately EXCLUDED — it is a payment INSTRUMENT (a bank check/cheque), so issue_check /
    # draft_check / check_run would satisfy a read-verb requirement and fire a fund-move. Use get_status not check_.
))
_READ_NOUNS = _SAFE_READ - _SAFE_READ_VERBS       # whoami/history/summary/info/status/balance/account/me/self/…
# On the money/signing surface, exempt ONLY ops whose EVERY token is one of these (a recognized read shape). This is
# an ALLOWLIST — an unrecognized verb (fund/sweep/debit/settle/release/execute/finalize/move/convert/…) fails CLOSED
# to T3, instead of us trying to enumerate every dangerous verb (which is what let the launder through).
_READ_SHAPE_OK = (_SAFE_READ_VERBS | _READ_NOUNS
                  # money NOUNS are legit read TARGETS (get_invoice / list_payouts / get_wire are reads) — the danger
                  # is the VERB (create/send/fund/sweep, none of which are read verbs), not naming the noun.
                  | frozenset(("charge", "charges", "payment", "payments", "invoice", "invoices", "transfer",
                               "transfers", "payout", "payouts", "deposit", "deposits", "wire", "wires", "refund",
                               "refunds", "withdrawal", "withdrawals", "ledger", "wallet", "statement", "settlement",
                               "disbursement", "chargeback", "remittance", "reimbursement", "payroll", "funds"))
                  # common BENIGN read-target nouns, so ordinary finance reads (list_transactions / get_customer /
                  # list_subscriptions / get_invoice) stay auto-exempt on a money server rather than over-staging.
                  | frozenset(("transaction", "transactions", "statement", "statements", "receipt", "receipts",
                               "activity", "activities", "subscription", "subscriptions", "customer", "customers",
                               "plan", "plans", "price", "prices", "product", "products", "order", "orders",
                               "item", "items", "record", "records", "entry", "entries", "list", "detail", "details",
                               "order", "orders", "trade", "trades", "position", "positions", "shares", "stock",
                               "portfolio", "holding", "holdings", "asset", "assets"))
                  # common BENIGN software/business read-target nouns. This set is a fail-CLOSED allowlist: the AUTONOMOUS
                  # fire gate (is_read_only) requires EVERY token to be in _READ_SHAPE_OK, so a glued/unknown compound
                  # (get_sendwire / get_payinvoice / get_buyshares) can NEVER auto-fire — it isn't recognized. Missing a
                  # benign noun over-STAGES a read (safe); it can never under-block a money op (the enumeration that keeps
                  # failing is the money one — this is the inverse: enumerate the KNOWN-SAFE, default everything else to STAGE).
                  | frozenset((
                      "repo", "repos", "repository", "repositories", "user", "users", "member", "members", "team",
                      "teams", "org", "orgs", "organization", "group", "groups", "role", "roles", "permission",
                      "permissions", "issue", "issues", "ticket", "tickets", "task", "tasks", "project", "projects",
                      "page", "pages", "file", "files", "folder", "folders", "document", "message", "messages",
                      "comment", "comments", "thread", "threads", "post", "posts", "note", "notes", "event", "events",
                      "log", "logs", "audit", "session", "sessions", "contact", "contacts", "lead", "leads", "deal",
                      "deals", "opportunity", "opportunities", "company", "companies", "label", "labels", "tag", "tags",
                      "category", "categories", "channel", "channels", "board", "boards", "card", "cards", "column",
                      "row", "rows", "table", "tables", "field", "fields", "form", "forms", "view", "views", "report",
                      "reports", "dashboard", "metric", "meeting", "meetings", "calendar", "appointment", "email",
                      "emails", "inbox", "conversation", "conversations", "article", "articles", "review", "reviews",
                      "rating", "form", "workspace", "workspaces", "app", "apps", "plugin", "integration", "integrations",
                      "connection", "connections", "webhook", "webhooks", "workflow", "workflows", "automation", "rule",
                      "rules", "trigger", "triggers", "step", "steps", "run", "runs", "job", "jobs", "build", "builds",
                      "pipeline", "deployment", "deployments", "release", "releases", "version", "versions", "branch",
                      "branches", "commit", "commits", "tag", "artifact", "artifacts", "image", "images", "container",
                      "service", "services", "endpoint", "endpoints", "function", "functions", "node", "nodes",
                      "cluster", "config", "configs", "configuration", "setting", "settings", "profile", "profiles",
                      "name", "names", "type", "types", "kind", "slug", "url", "urls", "link", "links", "path", "route",
                      "routes", "key", "keys", "value", "values", "field", "meta", "metadata", "schema", "definition",
                      "template", "templates", "draft", "drafts", "attachment", "attachments", "media", "asset",
                      "gallery", "photo", "photos", "video", "videos", "audio", "avatar", "icon", "banner", "brand",
                      "campaign", "campaigns", "audience", "segment", "segments", "list", "lists", "feed", "feeds",
                      "notification", "notifications", "alert", "alerts", "reminder", "reminders", "milestone",
                      "milestones", "sprint", "sprints", "epic", "epics", "story", "stories", "backlog", "board",
                      "goal", "goals", "objective", "kpi", "kpis", "score", "scores", "insight", "insights", "trend",
                      "trends", "pattern", "patterns", "signal", "signals", "world", "worlds", "brain", "memory",
                      "memories", "skill", "skills", "agent", "agents", "tool", "tools", "capability", "capabilities",
                  ))
                  | frozenset(("by", "for", "of", "the", "all", "my", "a", "an", "and", "to", "with", "on", "in",
                               "from", "id", "ids", "recent", "latest", "last", "first", "open", "active", "pending",
                               "count", "total", "single", "single", "own", "current", "default", "public", "private")))

# ── Server-INDEPENDENT money / signing SURFACE — the load-bearing safety insight. A connection SLUG is user-
# controlled + arbitrary (mystripe, chase, mybank, a custom name all defeat a hardcoded server list), so whether an
# op MOVES REAL FUNDS or LEGALLY BINDS must be decided by the ACTION — a money noun, a money verb, a signing token,
# or a money hint in the args — NOT by recognizing the connector. The server lists below are only a BONUS trigger. ──
_MONEY_NOUNS = frozenset((
    "balance", "balances", "funds", "payment", "payments", "charge", "charges", "invoice", "invoices", "wire",
    "wires", "payout", "payouts", "transfer", "transfers", "deposit", "deposits", "withdrawal", "withdrawals",
    "ledger", "wallet", "payroll", "refund", "refunds", "remittance", "disbursement", "chargeback", "settlement",
    "iban", "ach", "sepa", "swift", "reimbursement",
    # the literal money WORDS (moveMoney / send_cash / release_capital — the plain-English movers must register)
    "money", "monies", "cash", "capital", "dollars", "dollar", "euros", "euro", "fiat", "crypto", "bitcoin",
    "btc", "eth", "usd", "eur", "gbp", "stablecoin", "coin", "coins",
))  # NB: 'account' is deliberately NOT here (too broad — github/aws accounts); fund/debit/sweep verbs catch fund ops.
# Securities / trading nouns — trading them MOVES value (buy/sell/execute), so they're a money surface; but a READ of
# them (get_order / list_positions) still fires, because they're also in _READ_SHAPE_OK.
_SECURITIES_NOUNS = frozenset((
    "order", "orders", "trade", "trades", "position", "positions", "shares", "share", "stock", "stocks",
    "security", "securities", "asset", "assets", "option", "options", "future", "futures", "portfolio",
    "holding", "holdings", "bond", "bonds", "equity", "equities", "derivative", "derivatives",
))
_MONEY_VERBS_HARD = frozenset((   # money on ANY server, unconditionally (rarely non-money in an operator context)
    "transfer", "transfers", "wire", "wires", "payout", "payouts", "disburse", "disbursement", "remit",
    "remittance", "payroll", "payrun", "refund", "refunds", "chargeback", "withdraw", "withdrawal", "deposit",
    "debit", "credit", "fund", "funding", "ach", "sepa", "swift", "settle", "sweep", "topup", "reimburse",
    # banking / treasury money-movement terms (plain ASCII — these MOVE value, get_-prefix must not make them reads)
    "drawdown", "drawdowns", "disbursal", "disbursals", "disburses", "advance", "advances", "prefund", "prefunding",
    "liquidate", "liquidation", "remittances", "wiretransfer", "moneytransfer", "fundtransfer", "cashout", "payin",
    "payin", "collect", "collections", "chargecard", "capturepayment", "sendmoney", "sendfunds", "sendpayment",
    "pay", "pays", "paid", "prepay", "prepaid", "repay", "repayment", "payback", "paydown",   # the canonical pay verb
    # treasury / collections / legal-finance movers (seizure, garnishment, escrow, offset, novation, distributions)
    "garnish", "garnishment", "garnishments", "levy", "levies", "seize", "seizure", "clawback", "clawbacks",
    "escrow", "escrows", "impound", "sequester", "offset", "offsets", "novation", "payoff", "payoffs", "distribution",
    "distributions", "remitter", "wages", "collections", "recoup",   # clearly-financial (collect/recover excluded: ambiguous)
    "buy", "sell", "trade", "swap", "rebalance", "allocate", "short", "long", "invest", "divest", "redeem",   # securities/treasury
))
_AMBIG_MOVE_VERBS = frozenset((   # money ONLY when a money noun / money args / money server ALSO present
    "capture", "execute", "release", "move", "finalize", "convert", "process", "reconcile", "authorize", "authorise",
    "confirm", "approve", "complete",
))
_SIGNING_SURFACE = frozenset((    # signing / legal-execution tokens (server-independent)
    "sign", "signed", "esign", "esignature", "countersign", "notarize", "notarise", "signature", "signatures",
    "envelope", "envelopes",
))
_SIGN_BIND_VERBS = frozenset(("finalize", "execute", "complete", "countersign", "send", "issue"))
_SIGN_DOC_NOUNS = frozenset(("document", "documents", "contract", "contracts", "agreement", "agreements", "nda", "deed"))

# STRUCTURAL: a read-shape token must NEVER be an ACTION verb. Subtract every money/ambiguous/destructive/signing
# VERB from the fire allowlist, so a word that is BOTH a benign noun AND a money-capable verb (e.g. 'release' — a
# software release AND 'release funds') can NEVER make a get_-prefixed op auto-fire. This guards against accidentally
# adding a money-capable word to the benign list (the 'get_release fires on a bank' hole). Money/securities NOUNS
# stay (they're read targets: get_invoice / get_order); only the VERBS are removed.
_READ_SHAPE_OK = _READ_SHAPE_OK - _AMBIG_MOVE_VERBS - _MONEY_VERBS_HARD - _DESTRUCTIVE_TOKENS - _SIGNING_SURFACE


def _server_hit(s, servers):
    """Boundary-ish membership for the connector slug (alnum-stripped) — catches decoration on the canonical name
    (stripe_prod / prod-stripe / mystripe). Only a BONUS money/signing signal; the action-token surface is the real
    gate, so an over-match here just fails safe (T3)."""
    return any(s == m or s.startswith(m) or s.endswith(m) for m in servers)


# Money PAYLOAD detection by SHAPE, not by an enumerated field-name list (which missed debitAccount/creditAccount/
# value/currency). A transaction payload has a VALUE field + a DESTINATION/account field, OR two account fields
# (debit+credit), OR value+currency. Field-name-INDEPENDENT enough to catch novel payloads; substrings are matched
# against the folded, lower-cased args JSON.
_ARG_VALUE = ("amount", "value", "notional", "cents", "principal", "\"sum\"", "\"total\"", "units", "qty", "quantity")
_ARG_DEST = ("destination", "recipient", "payee", "beneficiary", "creditaccount", "debitaccount", "creditor",
             "debtor", "counterparty", "toaccount", "fromaccount", "destaccount", "iban", "wallet", "rail",
             "routing", "sortcode", "\"swift\"", "acct", "\"account\"", "accountid", "accountnumber")
_ARG_CCY = ("currency", "\"ccy\"", "\"usd\"", "\"eur\"", "\"gbp\"", "\"jpy\"", "\"chf\"", "\"cad\"", "\"aud\"")


def _args_look_monetary(a):
    """True if the request args LOOK like a value-moving payload (shape-based, so novel field names still trip it)."""
    al = str(a or "").lower()
    has_val = any(k in al for k in _ARG_VALUE)
    has_dest = any(k in al for k in _ARG_DEST)
    has_ccy = any(k in al for k in _ARG_CCY)
    two_acct = al.count("account") >= 2                       # debit + credit = a transfer
    return two_acct or (has_val and has_dest) or (has_val and has_ccy) or (has_dest and has_ccy)


# Money SUBSTRINGS — a GLUED lowercase compound ("makepayment", "sendwire", "wiremoney", "disbursefunds") has no
# camelCase boundary or delimiter, so it tokenizes as ONE unrecognized token and dodges whole-token money matching.
# But it still CONTAINS the money word. These are ≥5-char (or distinctive) money terms whose substring presence is a
# strong money signal with few false positives (short ambiguous ones like 'pay'→display are deliberately excluded).
_MONEY_SUBSTRINGS = (
    "money", "payment", "payout", "transfer", "disburse", "disbursal", "withdraw", "deposit", "remit", "remittance",
    "garnish", "levy", "seizure", "clawback", "escrow", "impound", "sequester", "novation", "settle", "settlement",
    "payroll", "refund", "chargeback", "wallet", "drawdown", "liquidat", "reimburse", "wiremoney", "sendwire",
    "sendmoney", "sendfunds", "sendpayment", "movemoney", "wirefunds", "fundwallet",
)


def _has_money_substr(tool):
    """True if the (folded) tool name CONTAINS a money term as a substring — catches glued compounds that tokenize as
    one word and evade whole-token matching."""
    t = str(tool or "").lower()
    return any(sub in t for sub in _MONEY_SUBSTRINGS)


def is_untouchable(server, tool, args=""):
    """T3 predicate — does this MOVE REAL FUNDS or LEGALLY BIND? Founder-only, NEVER autonomous.

    FAIL-SAFE: on the money/signing surface, an unknown/ambiguous op resolves T3 (blocked), never a lower tier —
    a misclassification or a brand-new money/signing tool fails SAFE. A CLEAR READ (get/list/retrieve with no
    mutation hinted) is never T3. This is a POSITIVE, structural guard: the caller must reserve T3 for a
    founder-only path; no autonomous context is meant to satisfy it."""
    tool, server, args = _fold(tool), _fold(server), _fold(args)   # defeat homoglyph/compat evasion first (#7)
    a = str(args or "").lower()
    s = _re.sub(r"[^a-z0-9]", "", str(server or "").lower())
    _camel = _re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(tool or ""))
    tokens = frozenset(x.lower() for x in _re.split(r"[^A-Za-z0-9]+", _camel) if x)

    money_args = any(k in a for k in _MONEY_MUTATE) or _args_look_monetary(a)
    money_server = _server_hit(s, _MONEY_MOVE_SERVERS)
    sign_server = _server_hit(s, _SIGNING_SERVERS)
    # SURFACE — server-INDEPENDENT: does the ACTION move money or legally bind? Detected from the tool's tokens +
    # args, NOT from recognizing the (arbitrary, user-controlled) connector slug. The server hit is only a bonus.
    on_money = (money_server or money_args or _has_money_substr(tool)
                or bool(tokens & _MONEY_NOUNS) or bool(tokens & _SECURITIES_NOUNS) or bool(tokens & _MONEY_VERBS_HARD)
                or (bool(tokens & _AMBIG_MOVE_VERBS) and bool(tokens & _MONEY_NOUNS)))
    on_signing = (sign_server or bool(tokens & _SIGNING_SURFACE)
                  or (bool(tokens & _SIGN_BIND_VERBS) and bool(tokens & _SIGN_DOC_NOUNS)))

    if on_money or on_signing:
        # FAIL-CLOSED on the money / signing surface: T3 is the default; the ONLY exemption is an unambiguous read
        # SHAPE — a read VERB present, EVERY token a recognized read-verb / read-noun / money-noun / connector, and
        # NO money mutation hinted in the args. A read NOUN alone (balance/status) does NOT exempt, an unrecognized
        # or movement verb does NOT (fund/sweep/debit/capture/…), and a money PAYLOAD in the args (transfer/amount)
        # blocks even a benign-named read. This is un-launderable by slug name, tool name, or noun.
        if (bool(tokens & _SAFE_READ_VERBS) and tokens <= _READ_SHAPE_OK and not money_args):
            return False
        return True
    # Not a money/signing surface → not an untouchable (resolve_tier handles SAFE vs DESTRUCTIVE for the rest).
    return False
