"""Efterlev Studio — the visual compliance map (DECISIONS 2026-05-22).

A local browser app (served on 127.0.0.1): the evidence flow streams into a
theme-grouped grid of verdict-colored KSI tiles that settles into a live
dashboard. `server.py` serves the page, `web_data.py` assembles its payload,
`poster.py` exports a static SVG. The event spine is in `efterlev.events`.
"""
