"""The router — central's dispatcher and headless mode (folded into hugpy-core 0.4: one
process, one database, one derivation). One OpenAI-compatible /v1 in front of every box:
pick by central's own allocation, proxy (streaming, uploads, binary), one route_log row
per decision, API keys for machine clients; each box's wrapper API relayed under /v1/boxes."""
