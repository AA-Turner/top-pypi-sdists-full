"""What the console asks Core for.

The console (@hugpy/ui, built in site/) is the user's screen of the wrappers. It asks its backend by the routes it
always has (/api/...), and Core answers them here. Every answer is shaped from what a wrapper itself published or
answers now: nothing about a host is kept or decided in Core.

    feeds     the live feeds (GET /api/llm/snapshot, and pushed over GET /api/llm/events): each wrapper as a
              worker row with its cards, memory and what is loaded, and the wrapper's own live resources report
    catalog   the models (GET /api/models) and the raw call log (GET /api/llm/calls/raw)
    grading   test fire (the Compute tab) and the Metrics and Grader tabs: rounds of grading calls and what the
              call log says came of them
    modelsdb  the Databases tab: every model the wrappers' Discoveries have recorded, and one model's tables,
              read where they are (its wrapper, the call log)
    database  the Database panel: every connected wrapper's database, every table of it browsed read-only through
              the wrapper's own browser (GET /api/llm/db/...)

A route of the console that is not here yet answers 404; which ones are is said by the browser check
(tools/live-checks/hugpy-core/console_in_a_browser.mjs).
"""
from . import catalog, database, feeds, grading, modelsdb

__all__ = ['catalog', 'database', 'feeds', 'grading', 'modelsdb']
