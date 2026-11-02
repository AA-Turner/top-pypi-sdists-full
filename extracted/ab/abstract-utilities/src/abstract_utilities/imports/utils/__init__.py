"""Intentionally empty.

This subpackage previously held a vendored copy of yt_dlp's internal ``utils``
module (which itself imported ``yt_dlp``). It was an unused artifact — none of
its names are referenced anywhere in abstract_utilities — and it made
``import abstract_utilities`` require yt_dlp. It has been removed.

The submodule is kept (empty) so that lingering ``from ...imports import utils``
references still resolve.
"""
