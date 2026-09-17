"""Growing-season phenology from daily rasters: onset, cessation, length.

Pixel-level agroclimatic season onset / cessation / length computed from the
daily CHIRPS / CHIRTS-ERA5 / NCEP-ETref intermediate rasters that geoprepare
writes, referenced against the GEOGLAM Crop Monitor calendars, and scored
for the current season by :mod:`geocif.season_monitor`.

See ``DESIGN.md`` in this package for the contract every module follows.
"""
