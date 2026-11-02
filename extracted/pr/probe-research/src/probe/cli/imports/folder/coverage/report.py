"""where each file is filed (placements, unfiled, refused) and the bucket report written beside the store."""

from __future__ import annotations


class CoverageReport(dict):
    """The bucket mapping, plus whether it was read mid-census.

    A plain dict to every existing caller -- they index fixed keys -- with one
    attribute added, because a census that has hashed half a folder reports the
    other half as `vanished`. That is correct DURING the pass and a lie
    afterwards, so a reader has to be able to tell which it is holding.
    """

    partial: bool = False
