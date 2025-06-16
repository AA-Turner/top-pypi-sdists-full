def _apply_ext_filter(self):
    """
    Called when any extension‐checkbox toggles.
    Simply re-process the last raw paths, but skip rebuilding the ext‐row.
    """
    if not self._last_raw_paths:
        return
    log_it(self, self._last_raw_paths)
  
    self.process_files(self._last_raw_paths, rebuild_ext_row=False)
