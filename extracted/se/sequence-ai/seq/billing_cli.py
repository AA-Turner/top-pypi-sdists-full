"""
`seq billing top-up | redeem | credits | plan | invoices | details` and seq.billing_top_up / redeem_promo_code /
billing_credits / billing_plan / billing_invoices / billing_details: the console's Billing page from the command line -
the payment page for a top-up and the wait for its credit, a promotion code redeemed, the credits added, the plan and a
move to another, the invoices, and the details invoices print. Each needs you signed in (`seq login`): a key cannot pay or change the account. A card number never passes
through here - the payment page takes it.


In one sentence: each function asks the platform as you (deployments_cli._call with person=True) for what the Billing
page shows or does - a top-up's payment page, opened in your browser, then the balance read every 5 s until the credit
lands - and returns it; nothing is printed unless asked (`echo`).

    seq.billing_top_up(50)          # {"url": ..., "balance_usd": 68.86, "landed": True} once it lands
"""
from __future__ import annotations

import time
import webbrowser
from datetime import datetime, timedelta
from typing import Any, Callable
from urllib.parse import quote

from seq.deployments_cli import _call
from sequence_ai._core.money import money, whole

Echo = Callable[[str], Any] | None

KIND_WORDS = {"card": "card", "invoice": "invoice payment", "starting_credit": "starting credit",
              "credit_grant": "credit grant", "promotion_code": "promotion code"}
PAID_KINDS = ("card", "invoice")
WAIT_EVERY_S = 5.0
WAIT_AT_MOST_S = 30 * 60.0
PER_PAGE = 20
PER_PAGE_LOOKED = 20


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def _count(n: int, noun: str) -> str:
    return f"{n} {noun}" + ("" if n == 1 else "s")


def _usd(v: Any) -> str:
    """An amount by the docs' one rule, as every other command and the console say it (sequence_ai money: four decimals
    under $1, a negative one's sign first); "—" for one the platform did not say. Before, two decimals always - a
    $0.0042 line read $0.00 - and a minus sign of its own."""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return "—"
    return money(x)


def _balance(base_url: str | None) -> float | None:
    """The account's balance now, as `seq account` reads it (GET /v1/account), as you."""
    out = _call("GET", "/v1/account", base_url, person=True) or {}
    bal = (out.get("balance") or {}).get("balance") if isinstance(out.get("balance"), dict) else out.get("balance")
    return float(bal) if isinstance(bal, (int, float)) else None


def _open(url: str, echo: Echo, opener: Callable[[str], Any] | None) -> None:
    """A page's link said, then the page opened in this machine's browser when it has one (`opener`, its default
    browser by default): the link first, whatever a browser does after - a machine with none, or one it hangs on,
    still shows it - and none opened in a shell over SSH, where it would not be in front of whoever reads this (the
    replay player's own check, as `seq login` does it).
"""
    _say(echo, f"  {url}")
    from seq._replay_player.cli import _remote

    if not url or _remote():
        return
    try:
        if (opener or webbrowser.open)(url):
            _say(echo, "  (opened in your browser)")
    except Exception:
        pass


def _card_credits(base_url: str | None) -> list[dict]:
    """The newest card credits - top-ups paid on the payment page, or waiting for it (GET /v1/billing/credits), as
    you."""
    out = _call("GET", f"/v1/billing/credits?limit={PER_PAGE_LOOKED}&offset=0", base_url, person=True) or {}
    return [r for r in out.get("data") or [] if r.get("kind") == "card"]


def billing_top_up(amount_usd: float, *, wait: bool = True, base_url: str | None = None, echo: Echo = None,
                   opener: Callable[[str], Any] | None = None, sleep: Callable[[float], Any] = time.sleep,
                   clock: Callable[[], float] = time.monotonic, wait_s: float = WAIT_AT_MOST_S,
                   link_echo: Echo = None) -> dict:
    """The payment page for adding `amount_usd` ($5 at least, as the console) - its link, opened in your browser - and,
    with `wait`, the credits read every 5 s until this top-up's lands (30 minutes at most): {"url", "amount_usd",
    "balance_usd" (once it landed), "landed"}. Landed is a card credit of that amount, paid, that was not there before
    it was asked - never a balance that rose for another reason (an eval's hold let go). Paying is done on that page;
    stopping the wait stops nothing of the payment. `link_echo` says the link and the wait where `echo` says nothing
    (seq --json: on stderr, its stdout the JSON alone).
"""
    from seq import clock as times

    def newest(rows: list[dict]) -> Any:
        seen = [t for t in (times.instant(r.get("created_at")) for r in rows) if t is not None]
        return max(seen) if seen else None

    say = link_echo or echo
    before = newest(_card_credits(base_url)) if wait else None
    out = _call("POST", "/v1/billing/top-up", base_url, {"amount_usd": amount_usd}, person=True) or {}
    url = out.get("url")
    _say(say, f"pay {_usd(amount_usd)} on the payment page:")
    _open(url, say, opener)
    got = {"url": url, "amount_usd": amount_usd, "balance_usd": None, "landed": False}
    if not wait:
        return got
    _say(say, "waiting for it to land… (Ctrl-C stops waiting; the payment still goes through)")
    end = clock() + wait_s
    while clock() < end:
        sleep(WAIT_EVERY_S)
        for r in _card_credits(base_url):
            t = times.instant(r.get("created_at"))
            if (t is not None and (before is None or t > before) and r.get("status") == "paid"
                    and abs(float(r.get("amount_usd") or 0) - float(amount_usd)) < 0.005):
                now = _balance(base_url)
                _say(say, f"landed: {_usd(amount_usd)} paid, balance {_usd(now)}")
                return {**got, "balance_usd": now, "landed": True}
    _say(say, "not landed yet after 30 minutes: `seq billing credits` shows it when it does")
    return got


def redeem_promo_code(code: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Redeem a promotion code from our team, as the Add credits dialog does: its free credit added to your balance,
    once per account (any case; spaces around it dropped). Returns {"code": the code as the platform keeps it,
    "amount_usd": the credit added}. A refusal raises the platform's error, its `details["reason"]` naming it:
    InvalidRequest "invalid" (an unknown, turned-off or expired code, all alike), Conflict "already_redeemed" or
    "used_up", Unavailable "too_many_tries" (ten failed tries this hour; its `retry_after_s` says when to try again).
    
"""
    out = _call("POST", "/v1/credits/redeem", base_url, {"code": str(code).strip()}, person=True) or {}
    _say(echo, f"redeemed {out.get('code')}: {_usd(out.get('amount_usd'))} of free credit added to your balance")
    return out


def _status_word(row: dict) -> str:
    """A credit's status as this CLI says it: "added" for one nobody paid for - a grant, a starting credit, a promotion
    code - as the console's Billing page says it. The API's status stays "paid", which a top-up's wait reads.
    """
    status = str(row.get("status") or "")
    return "added" if status == "paid" and str(row.get("kind") or "card") not in PAID_KINDS else status


def _bill_day(at: Any) -> str:
    """A day of the bill - a credit's, a plan's end - the UTC day, said so: "2026-12-01 UTC"; '—' for none. Before, a
    credit's was this machine's day and a plan's end the first ten characters of what the platform sent, neither said
    which zone.
"""
    from seq import clock

    day = clock.day_of(at, utc=True)
    return f"{day} UTC" if clock.instant(at) else day


def _period(start: Any, end: Any) -> str:
    """A bill's period as the console says one, its last day its end, its days the UTC days: "Oct 1 – Oct 31, 2026 UTC".
    An invoice keeps the first day after it as period_end.
"""
    from seq import clock

    first = clock.instant(start, utc=True) or datetime.strptime(str(start)[:10], "%Y-%m-%d")
    last = (clock.instant(end, utc=True) or datetime.strptime(str(end)[:10], "%Y-%m-%d")) - timedelta(days=1)
    head = f"{first:%b} {first.day}" + ("" if first.year == last.year else f", {first.year}")
    return f"{head} – {last:%b} {last.day}, {last.year} UTC"


def billing_credits(*, page: int = 1, per_page: int = PER_PAGE, base_url: str | None = None, echo: Echo = None) -> dict:
    """The credits added to the account, newest first, `per_page` a page: each one's day, amount (a refund negative),
    status (paid, or added where nobody paid for it; pending and failed ones count for nothing) and kind - a card, an
    invoice payment, the starting credit, a credit grant. {"data", "total"}."""
    page = max(1, int(page))
    out = _call("GET", f"/v1/billing/credits?limit={per_page}&offset={(page - 1) * per_page}", base_url,
                person=True) or {}
    rows = out.get("data") or []
    for r in rows:

        _say(echo, f"  {_bill_day(r.get('paid_at') or r.get('created_at')):14}  {_usd(r.get('amount_usd')):>10}  "
                   f"{_status_word(r):8}  {KIND_WORDS.get(str(r.get('kind') or ''), 'card')}")
    total = int(out.get("total") or len(rows))
    if not rows:
        _say(echo, "no credit added yet" if page == 1 else f"no page {page}: {_count(total, 'credit')} in all")
    elif total > page * per_page:
        _say(echo, f"page {page} of {(total + per_page - 1) // per_page} - `seq billing credits --page {page + 1}`")
    return out


def billing_plan(plan: str | None = None, *, base_url: str | None = None, echo: Echo = None,
                 opener: Callable[[str], Any] | None = None) -> dict:
    """With no `plan`: the account's plan and every plan with what it costs a month and its free credit. With
    "team" or "starter": the move the Billing page's buttons make - Starter to Team on its payment page (its link,
    opened in your browser), Team to Starter at the period's end, Team set to end kept on. A Custom plan changes with
    us."""
    if plan is None:
        out = _call("GET", "/v1/billing/plan", base_url, person=True) or {}
        mine = out.get("plan")
        sub = out.get("subscription") or {}
        _say(echo, f"plan      {str(mine or '—').capitalize()}"
                   + (f" - ends {_bill_day(sub.get('current_period_end'))}, Starter from then"
                      if sub.get("cancel_at_period_end") else ""))


        order = ("starter", "team", "custom")
        plans = sorted(out.get("plans") or [], key=lambda p: order.index(p.get("plan")) if p.get("plan") in order
                       else len(order))
        for p in plans:
            mark = "*" if p.get("plan") == mine else " "
            name = f"  {mark} {str(p.get('display_name') or p.get('plan') or ''):10} "
            if p.get("plan") == "custom":





                _say(echo, name + "agreed per account: volume prices, a monthly limit and limits agreed for your fleet")
                continue
            _say(echo, name + f"{whole(p.get('monthly_fee_usd'))}/month, {whole(p.get('monthly_free_credit_usd'))} "
                              f"free credit a month, {p.get('max_policies', '—')} policies, {p.get('max_gpus', '—')} GPUs")
        return out
    out = _call("POST", "/v1/billing/plan", base_url, {"plan": plan}, person=True) or {}
    if out.get("url"):
        _say(echo, "move to Team on its payment page:")
        _open(out["url"], echo, opener)
    elif out.get("action") == "cancel":
        _say(echo, f"Team ends {_bill_day(out.get('current_period_end'))}: Starter from then")
    elif out.get("action") == "resume":
        _say(echo, "Team goes on")
    return out


def billing_invoices(number: str | None = None, *, page: int = 1, per_page: int = PER_PAGE, base_url: str | None = None,
                     echo: Echo = None) -> dict:
    """With no `number`: the month so far as the next invoice will have it, and the invoices issued, newest first,
    `per_page` a page. With one: that invoice whole - its lines, its totals, whom it bills."""
    if number:
        out = _call("GET", f"/v1/billing/invoices/{quote(number, safe='')}", base_url, person=True) or {}
        _say(echo, f"invoice   {out.get('number')}  {_period(out.get('period_start'), out.get('period_end'))}")
        for ln in out.get("lines") or []:
            _say(echo, f"  {str(ln.get('description') or ln.get('label') or ''):48} {_usd(ln.get('amount_usd'))}")
        _say(echo, f"usage {_usd(out.get('usage_usd'))}  credits added {_usd(out.get('payments_usd'))}  "
                   f"closing balance {_usd(out.get('closing_balance_usd'))}  due {_usd(out.get('amount_due_usd'))}")
        return out
    page = max(1, int(page))
    out = _call("GET", f"/v1/billing/invoices?limit={per_page}&offset={(page - 1) * per_page}", base_url,
                person=True) or {}
    month = out.get("month_so_far") or {}
    if isinstance(month, dict) and month:
        _say(echo, f"this month so far  usage {_usd(month.get('usage_usd'))}")
    rows = out.get("data") or []
    from seq import clock

    for r in rows:

        start = clock.instant(r.get("period_start"), utc=True)
        month = f"{start:%Y-%m} UTC" if start else str(r.get("period_start") or "")[:7]
        _say(echo, f"  {str(r.get('number') or ''):16} {month}  usage "
                   f"{_usd(r.get('usage_usd'))}  due {_usd(r.get('amount_due_usd'))}")
    total = int(out.get("total") or len(rows))
    if not rows:
        _say(echo, "no invoice issued yet" if page == 1 else f"no page {page}: {_count(total, 'invoice')} in all")
    elif total > page * per_page:
        _say(echo, f"page {page} of {(total + per_page - 1) // per_page} - `seq billing invoices --page {page + 1}`")
    return out


def billing_details(change: bool = False, *, base_url: str | None = None, echo: Echo = None,
                    opener: Callable[[str], Any] | None = None) -> dict:
    """The details invoices print - the company, its address, its tax id - or, with `change`, the page where they are
    changed (its link, opened in your browser)."""
    if change:
        out = _call("POST", "/v1/billing/details", base_url, person=True) or {}
        _say(echo, "change the details invoices print on this page:")
        _open(out.get("url"), echo, opener)
        return out
    out = _call("GET", "/v1/billing/details", base_url, person=True) or {}
    det = out.get("details") or {}
    if not det:
        _say(echo, out.get("note") or "no billing details yet")
    for k in ("name", "email", "address", "tax_ids", "phone"):
        if det.get(k):
            v = det[k]
            v = ", ".join(str(x) for x in v.values() if x) if isinstance(v, dict) else \
                ", ".join(str(x.get("value", x)) if isinstance(x, dict) else str(x) for x in v) if isinstance(v, list) \
                else v
            _say(echo, f"{k.replace('_', ' '):9} {v}")
    if out.get("can_change"):
        _say(echo, "`seq billing details --change` opens the page to change them")
    return out


def billing_card(*, base_url: str | None = None, echo: Echo = None, opener: Callable[[str], Any] | None = None) -> dict:
    """`seq billing card`: the payment method this month's bill goes to, added or made the default on the page the
    platform hands it (POST /v1/billing/details, the page `seq billing details --change` opens too) - opened in your
    browser, as a top-up's payment page is: no card is ever typed here. Billing is postpaid: usage past the monthly
    credit needs one.

"""
    out = _call("POST", "/v1/billing/details", base_url, person=True) or {}
    _say(echo, "add the payment method your month's bill goes to, or make another the default, on this page:")
    _open(out.get("url"), echo, opener)
    return out
