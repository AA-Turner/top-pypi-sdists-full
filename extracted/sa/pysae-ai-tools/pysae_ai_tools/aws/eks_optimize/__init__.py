"""Optimize EKS node groups by a global weighted score over every signal.

For each managed node group (SPOT and ON_DEMAND) in the region, this gathers the
set of **compatible** instance types (same vCPU/RAM shape and architecture;
GPU/accelerated families are dropped as never a fit) and scores each on three
axes combined into one 0-100 score (see ``scoring``):

* **reliability** — observed interruption rate (evictions/launches, our own
  history) and the Spot Advisor predictive rate (global, weaker). Neither
  *excludes* a type; they only weigh it.
* **cost** — average spot $/h (``describe-spot-price-history``) for SPOT groups,
  on-demand $/h (Price List API) for ON_DEMAND groups.
* **performance** — ``vCPU × clock × IPC`` (clock from ``describe-instance-types``,
  IPC per CPU microarchitecture), i.e. effective compute.

The package is split into :mod:`model` (domain dataclasses), :mod:`plan`
(attribution, scoring, mix selection — pure functions), :mod:`render` (Markdown /
JSON) and :mod:`cli` (option parsing + AWS/Datadog gathering, exposing ``main``).
Greenfield mode (``--cpu/--ram``) designs a brand-new node group.
"""
