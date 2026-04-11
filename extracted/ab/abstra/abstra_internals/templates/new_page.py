import random
from datetime import datetime, timedelta

from abstra.pages import register_function

# ============================================================
# Treasury Dashboard - Sample Page
# ============================================================
# This template demonstrates key Page features:
#   - @register_function: exposes Python functions to the browser
#   - register_static(): serves local files (JS, CSS, images) with
#     content-hashed URLs — call inside __render__ for fresh URLs
#   - __render__(): special function that returns HTML (called on GET)
#   - Other functions: callable from the browser via auto-generated JS
#   - get_user() / get_query_params(): authentication and URL params
# ============================================================


# --- Fake data generators (replace with real integrations) ---


def _random_currency_rate(base: float, spread: float = 0.02):
    return round(base * (1 + random.uniform(-spread, spread)), 4)


def _random_cash_flow():
    categories = [
        ("Accounts Receivable", "inflow"),
        ("Loan Repayment", "outflow"),
        ("Supplier Payment", "outflow"),
        ("Investment Return", "inflow"),
        ("Payroll", "outflow"),
        ("Service Revenue", "inflow"),
        ("Tax Payment", "outflow"),
        ("Client Deposit", "inflow"),
    ]
    name, direction = random.choice(categories)
    amount = round(random.uniform(10_000, 500_000), 2)
    due = datetime.now() + timedelta(days=random.randint(0, 30))
    return {
        "description": name,
        "direction": direction,
        "amount": amount,
        "due_date": due.strftime("%Y-%m-%d"),
    }


# --- Registered functions (callable from the browser) -------


@register_function
def get_dashboard_data():
    """Returns all dashboard data in a single call."""
    balance = round(random.uniform(2_000_000, 8_000_000), 2)
    inflows_today = round(random.uniform(200_000, 900_000), 2)
    outflows_today = round(random.uniform(100_000, 600_000), 2)
    pending_approvals = random.randint(2, 12)

    return {
        "summary": {
            "balance": balance,
            "inflows_today": inflows_today,
            "outflows_today": outflows_today,
            "net_today": round(inflows_today - outflows_today, 2),
            "pending_approvals": pending_approvals,
        },
        "rates": {
            "USD/BRL": _random_currency_rate(5.12),
            "EUR/BRL": _random_currency_rate(5.54),
            "GBP/BRL": _random_currency_rate(6.41),
            "USD/EUR": _random_currency_rate(0.92),
        },
        "cash_flow": [_random_cash_flow() for _ in range(8)],
        "updated_at": datetime.now().strftime("%H:%M:%S"),
    }


@register_function
def approve_payment(payment_index: int):
    """Simulates approving a payment."""
    return {"status": "approved", "payment_index": payment_index}


# --- __render__: returns the HTML for the page ---------------
# This function is called on every GET request.
# It must return a string (HTML). It cannot receive parameters.
# It is NOT exposed as a JS function in the browser.


@register_function
def __render__():
    # --- Static files (uncomment to use) ---
    # css_url = register_static("static/styles.css")
    # js_url = register_static("static/app.js")
    # logo_url = register_static("assets/logo.png")
    #
    # Then reference in your HTML with an f-string:
    #   <link rel="stylesheet" href="{css_url}">
    #   <script src="{js_url}"></script>
    #   <img src="{logo_url}">

    return """
<script src="https://cdn.tailwindcss.com"></script>
<style>
  body { margin: 0; font-family: 'Inter', system-ui, sans-serif; background: #f1f5f9; }
  .fade-in { animation: fadeIn 0.3s ease-in; }
  @keyframes fadeIn { from { opacity: 0.5; } to { opacity: 1; } }
</style>

<div id="app" class="min-h-screen p-6 max-w-7xl mx-auto">
  <!-- Header -->
  <div class="flex items-center justify-between mb-8">
    <div>
      <h1 class="text-2xl font-bold text-slate-800">Treasury Dashboard</h1>
      <p class="text-sm text-slate-500">Last updated: <span id="updated-at" class="font-medium">--:--:--</span></p>
    </div>
    <button onclick="refreshData()"
      class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
      <svg id="refresh-icon" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
      </svg>
      Refresh
    </button>
  </div>

  <!-- Summary Cards -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <div class="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
      <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Total Balance</p>
      <p id="balance" class="text-2xl font-bold text-slate-800">--</p>
    </div>
    <div class="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
      <p class="text-xs font-semibold text-emerald-500 uppercase tracking-wide mb-1">Inflows Today</p>
      <p id="inflows" class="text-2xl font-bold text-emerald-600">--</p>
    </div>
    <div class="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
      <p class="text-xs font-semibold text-rose-400 uppercase tracking-wide mb-1">Outflows Today</p>
      <p id="outflows" class="text-2xl font-bold text-rose-600">--</p>
    </div>
    <div class="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
      <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Pending Approvals</p>
      <p id="pending" class="text-2xl font-bold text-amber-600">--</p>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Cash Flow Table -->
    <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
      <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="font-semibold text-slate-800">Upcoming Cash Flow</h2>
        <span id="net-badge" class="text-xs font-bold px-2.5 py-1 rounded-full">--</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-xs font-semibold text-slate-400 uppercase tracking-wide border-b border-slate-50">
              <th class="px-5 py-3">Description</th>
              <th class="px-5 py-3">Due Date</th>
              <th class="px-5 py-3 text-right">Amount (BRL)</th>
              <th class="px-5 py-3 text-center">Action</th>
            </tr>
          </thead>
          <tbody id="cash-flow-body"></tbody>
        </table>
      </div>
    </div>

    <!-- Exchange Rates -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-100">
      <div class="px-5 py-4 border-b border-slate-100">
        <h2 class="font-semibold text-slate-800">Exchange Rates</h2>
      </div>
      <div id="rates-list" class="divide-y divide-slate-50"></div>
    </div>
  </div>
</div>

<script>
  const fmt = (n) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(n);

  async function refreshData() {
    const icon = document.getElementById('refresh-icon');
    icon.classList.add('animate-spin');

    try {
      const data = await get_dashboard_data();

      document.getElementById('balance').textContent = fmt(data.summary.balance);
      document.getElementById('inflows').textContent = fmt(data.summary.inflows_today);
      document.getElementById('outflows').textContent = fmt(data.summary.outflows_today);
      document.getElementById('pending').textContent = data.summary.pending_approvals;
      document.getElementById('updated-at').textContent = data.updated_at;

      const badge = document.getElementById('net-badge');
      const net = data.summary.net_today;
      badge.textContent = (net >= 0 ? '+' : '') + fmt(net);
      badge.className = net >= 0
        ? 'text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700'
        : 'text-xs font-bold px-2.5 py-1 rounded-full bg-rose-50 text-rose-700';

      const tbody = document.getElementById('cash-flow-body');
      tbody.innerHTML = data.cash_flow.map((item, i) => `
        <tr class="border-b border-slate-50 hover:bg-slate-50 transition-colors fade-in">
          <td class="px-5 py-3 font-medium text-slate-700">${item.description}</td>
          <td class="px-5 py-3 text-slate-500">${item.due_date}</td>
          <td class="px-5 py-3 text-right font-mono ${item.direction === 'inflow' ? 'text-emerald-600' : 'text-rose-600'}">
            ${item.direction === 'inflow' ? '+' : '-'} ${fmt(item.amount)}
          </td>
          <td class="px-5 py-3 text-center">
            ${item.direction === 'outflow' ? `
              <button onclick="handleApprove(${i})"
                class="text-xs bg-indigo-50 text-indigo-700 hover:bg-indigo-100 font-medium px-3 py-1 rounded-md transition-colors">
                Approve
              </button>` : '<span class="text-xs text-slate-300">-</span>'}
          </td>
        </tr>
      `).join('');

      const ratesList = document.getElementById('rates-list');
      ratesList.innerHTML = Object.entries(data.rates).map(([pair, rate]) => `
        <div class="px-5 py-3.5 flex items-center justify-between fade-in">
          <span class="text-sm font-medium text-slate-700">${pair}</span>
          <span class="text-sm font-mono font-semibold text-slate-800">${Number(rate).toFixed(4)}</span>
        </div>
      `).join('');

    } finally {
      icon.classList.remove('animate-spin');
    }
  }

  async function handleApprove(index) {
    const result = await approve_payment(index);
    if (result.status === 'approved') {
      await refreshData();
    }
  }

  refreshData();
  setInterval(refreshData, 10000);
</script>
"""
