from PyQt6.QtWidgets import QFileDialog,QListWidgetItem
from abstract_utilities.robust_readers import define_defaults
import os,sys
# — UI helpers —
def browse_dir(self):
    d = QFileDialog.getExistingDirectory(self, "Choose directory", self.dir_in.text() or os.getcwd())
    if d:
        self.dir_in.setText(d)
  
def make_params(self):
    directory = self.dir_in.text().strip()
    if not directory or not os.path.isdir(directory):
        raise ValueError("Directory is missing or not a valid folder.")
    # strings
    s_raw = [s.strip() for s in self.strings_in.text().split(",") if s.strip()]
    # allowed_exts: allow "ts,tsx" or "ts|tsx"
    e_raw = self.allowed_exts_in.text().strip()
    allowed_exts: Union[bool, Set[str]] = False
    if e_raw:
        splitter = '|' if '|' in e_raw else ','
        exts_list = [e.strip() for e in e_raw.split(splitter) if e.strip()]
        allowed_exts = {'.' + e if not e.startswith('.') else e for e in exts_list}
    # unallowed_exts similar
    ue_raw = self.unallowed_exts_in.text().strip()
    unallowed_exts: Union[bool, Set[str]] = False
    if ue_raw:
        splitter = '|' if '|' in ue_raw else ','
        exts_list = [e.strip() for e in ue_raw.split(splitter) if e.strip()]
        unallowed_exts = {'.' + e if not e.startswith('.') else e for e in exts_list}
    # exclude_types
    et_raw = self.exclude_types_in.text().strip()
    exclude_types: Union[bool, Set[str]] = False
    if et_raw:
        exclude_types = {e.strip() for e in et_raw.split(',') if e.strip()}
    # exclude_dirs
    ed_raw = self.exclude_dirs_in.text().strip()
    exclude_dirs: Union[bool, List[str]] = False
    if ed_raw:
        exclude_dirs = [e.strip() for e in ed_raw.split(',') if e.strip()]
    # exclude_patterns
    ep_raw = self.exclude_patterns_in.text().strip()
    exclude_patterns: Union[bool, List[str]] = False
    if ep_raw:
        exclude_patterns = [e.strip() for e in ep_raw.split(',') if e.strip()]
    # add
    add = self.chk_add.isChecked()
    # spec_line
    spec_line = self.spec_spin.value()
    spec_line = False if spec_line == 0 else int(spec_line)
    recursive=self.chk_recursive.isChecked()
    strings=s_raw
    total_strings=self.chk_total.isChecked()
    parse_lines=self.chk_parse.isChecked()
    spec_line=spec_line
    get_lines=self.chk_getlines.isChecked()
    cfg = define_defaults(
                allowed_exts=allowed_exts,
                unallowed_exts=unallowed_exts,
                exclude_types=exclude_types,
                exclude_dirs=exclude_dirs,
                exclude_patterns=exclude_patterns,
                add=add
            )
    
    return {
        "directory":directory,
        "get_lines":get_lines,
        "spec_line":spec_line,
        "parse_lines":parse_lines,
        "total_strings":total_strings,
        "strings":strings,
        "recursive":recursive,
        "cfg":cfg
     }
