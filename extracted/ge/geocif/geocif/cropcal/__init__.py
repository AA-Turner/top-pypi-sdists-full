"""Crop-calendar validation: do NDVI phenological transitions agree with the
GEOGLAM Crop Monitor calendar?

One row per (country, crop, season, calendar region). Two transitions are
compared against a Fourier-fitted NDVI climatology:

* **mid-greenup** -- end of calendar stage 1 vs. the steepest rise
* **mid-greendown** -- end of calendar stage 2 vs. the steepest fall

The result is a signed difference in days per transition, an agreement class,
and a pass/fail assessment, plus per-crop summary statistics, per-region
diagnostic figures and global delta maps.

This is a port of ``GEOGLAM/Code/Code/CropCalendar/`` re-based on
geoprepare's per-region EO extraction, running at **crop-calendar-region**
scale rather than admin-1. ``DEVIATIONS.md`` in this package records every
place the numerics intentionally differ from the original.
"""
