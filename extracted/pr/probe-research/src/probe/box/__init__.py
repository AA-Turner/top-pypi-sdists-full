"""The node agent: the part of Probe that is not inside the job.

Everything else in this client runs as the researcher's process, or as a
thread in it, and therefore ends when it ends. That is a hard limit on what
the client can ever explain: a process cannot report its own death.

This package is the exception. `registry` is how a running job says which
process on this machine is it; `watch` is a separate process that reads those
declarations, notices when one stops existing, and records that against the
run. Later phases add the evidence only the box holds -- kernel
out-of-memory lines, a scheduler's termination reason, a card's ECC counters.

Opt-in (`PROBE_BOX=1`), fail-open everywhere, and read-only with respect to
every process it watches.
"""
