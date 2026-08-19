# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Azure scale-benchmark workbench.

A repeatable, checked-in harness that exercises Geneva filtered/incremental blob
backfill at scale on Azure against the confirmed 50B MMLB dataset and
configurable compute. The source dataset stays read-only; all benchmark writes go
to a shallow clone. See ``README.md`` for usage.
"""
