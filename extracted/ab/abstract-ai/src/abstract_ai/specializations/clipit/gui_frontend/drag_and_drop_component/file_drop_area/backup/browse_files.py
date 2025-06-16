# ───────────────────────── browse dialog ────────────────────
def browse_files(self):
    files, _ = QtWidgets.QFileDialog.getOpenFileNames(
        self,
        "Select Files",
        "",
        "All Supported Files (*.txt *.md *.csv *.tsv *.log "
        "*.xls *.xlsx *.ods *.parquet *.geojson *.shp);;All Files (*)"
    )
    input(files)
    if files:
        
        self._log(f"browse_files: selected {len(files)} path(s)")
        self.process_files(files)
