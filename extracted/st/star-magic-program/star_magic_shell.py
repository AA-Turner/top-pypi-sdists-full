"""star_magic_shell - the ONE WINDOW (v0.412.0, Daniel's 'GO Qt'):
Papers | Wells | Gate | Export. Optional by construction (gui extra);
everything it shows is the same gate-verified machinery the CLI uses,
and every physics number carries its LIVE / INHERITED / MISMATCH flag -
the window never hides what the terminal admits.
"""
from __future__ import annotations

import csv
import sys

import uqff_paths


def _require_qt():
    try:
        from PyQt6 import QtWidgets  # noqa: F401
        return True
    except ImportError:
        return False


def main() -> int:
    if not _require_qt():
        print('star-magic gui needs PyQt6:  pip install "star-magic-program[gui]"')
        return 3
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                                 QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
                                 QTextEdit, QPushButton, QLabel, QFileDialog)
    import uqff_calculator as C

    def results_rows_for(pid):
        rows = []
        try:
            with open(uqff_paths.results_table(), encoding='utf-8', newline='') as f:
                for r in csv.DictReader(f):
                    if pid in ' '.join(str(v) for v in r.values()):
                        rows.append(r)
        except FileNotFoundError:
            pass
        return rows

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle('Star-Magic v%s — UQFF calculator + subsurface surveying' % C.VERSION)
    tabs = QTabWidget()

    # ---- Papers tab ----
    papers = QWidget(); pl = QHBoxLayout(papers)
    left = QVBoxLayout()
    search = QLineEdit(); search.setPlaceholderText('search 2,309 wired papers…')
    plist = QListWidget()
    all_papers = C.list_wired()
    plist.addItems(all_papers)
    left.addWidget(search); left.addWidget(plist)
    detail = QTextEdit(); detail.setReadOnly(True)
    pl.addLayout(left, 1); pl.addWidget(detail, 2)

    def do_search(text):
        plist.clear()
        t = text.strip().upper()
        plist.addItems([p for p in all_papers if t in p] if t else all_papers)
    search.textChanged.connect(do_search)

    def show_paper(item):
        pid = item.text()
        try:
            r = C.calc(pid)
        except Exception as e:
            detail.setPlainText('%s\nDISPATCH ERROR: %s' % (pid, e))
            return
        lines = [pid, '=' * len(pid), '',
                 'value:        %s' % r.get('value'),
                 'formula:      %s' % r.get('formula'),
                 'residual_pct: %s' % r.get('residual_pct'),
                 'status:       %s' % r.get('status', 'WIRED'), '',
                 'RESULTS-TABLE VERIFICATION (the honesty flags):']
        rows = results_rows_for(pid)
        if not rows:
            lines.append('  no physics results-table row cites this paper directly')
        for row in rows:
            lines.append('  %s = %s  [%s]%s' % (
                row.get('constant'), row.get('uqff_value'), row.get('live_status'),
                ('  live=' + row['live_value']) if row.get('live_value') else ''))
        lines += ['', 'VERIFIED_LIVE = re-derived from primitives at generation time',
                  'INHERITED_CARRIED = baseline value, NOT re-derived here',
                  'LIVE_MISMATCH = both values shown, nothing silently replaced']
        detail.setPlainText('\n'.join(lines))
    plist.itemClicked.connect(show_paper)
    tabs.addTab(papers, 'Papers')

    # ---- Wells tab (existing geology surface + catalogue browser) ----
    wells = QWidget(); wl = QHBoxLayout(wells)
    try:
        from uqff_downhole_simulator.uqff_profile_catalog import CATALOG
        wlist = QListWidget(); wlist.addItems(sorted(CATALOG))
        wdetail = QTextEdit(); wdetail.setReadOnly(True)

        def show_well(item):
            e = CATALOG[item.text()]
            prov = e.provenance
            wdetail.setPlainText('\n'.join('%s: %s' % kv for kv in sorted(prov.items())))
        wlist.itemClicked.connect(show_well)
        wl.addWidget(wlist, 1); wl.addWidget(wdetail, 2)
    except Exception as e:
        wl.addWidget(QLabel('catalogue unavailable: %s' % e))
    tabs.addTab(wells, 'Wells')

    # ---- Gate tab ----
    gate = QWidget(); gl = QVBoxLayout(gate)
    gout = QTextEdit(); gout.setReadOnly(True)
    gbtn = QPushButton('Run full fidelity gate (6,000+ assertions — takes ~1 min)')

    def run_gate():
        import subprocess
        gout.setPlainText('running…')
        app.processEvents()
        p = subprocess.run([sys.executable, str(uqff_paths.resolve('uqff_fidelity_tests.py'))],
                           capture_output=True, text=True)
        gout.setPlainText((p.stdout or '') + (p.stderr or ''))
    gbtn.clicked.connect(run_gate)
    gl.addWidget(gbtn); gl.addWidget(gout)
    tabs.addTab(gate, 'Gate')

    # ---- Export tab ----
    exp = QWidget(); el = QVBoxLayout(exp)
    einfo = QLabel('Export the selected paper as CSV: value + formula + residual + citation + honesty flag.')
    ebtn = QPushButton('Export selected paper…')

    def do_export():
        item = plist.currentItem()
        if not item:
            einfo.setText('select a paper on the Papers tab first')
            return
        pid = item.text()
        path, _ = QFileDialog.getSaveFileName(win, 'Export', pid + '.csv', 'CSV (*.csv)')
        if not path:
            return
        r = C.calc(pid)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(['paper', 'value', 'formula', 'residual_pct', 'status', 'constant', 'table_value', 'live_status'])
            rows = results_rows_for(pid) or [{}]
            for row in rows:
                w.writerow([pid, r.get('value'), r.get('formula'), r.get('residual_pct'),
                            r.get('status', 'WIRED'), row.get('constant', ''),
                            row.get('uqff_value', ''), row.get('live_status', '')])
        einfo.setText('exported: %s' % path)
    ebtn.clicked.connect(do_export)
    el.addWidget(einfo); el.addWidget(ebtn); el.addStretch(1)
    tabs.addTab(exp, 'Export')

    # geology tab from the existing operator surface, if renderers available
    try:
        from uqff_downhole_simulator.uqff_project import build_geology_tab
        tabs.addTab(build_geology_tab(), 'Geology')
    except Exception:
        pass

    win.setCentralWidget(tabs)
    win.resize(1100, 700)
    win.show()
    return app.exec()


if __name__ == '__main__':
    raise SystemExit(main())
