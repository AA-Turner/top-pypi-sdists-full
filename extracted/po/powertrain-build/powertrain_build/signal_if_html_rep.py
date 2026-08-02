# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing classes for the signal interfaces report."""
from collections import defaultdict
from powertrain_build.html_report import HtmlReport


class SigIfHtmlReport(HtmlReport):
    """Signal interface html report.

    Inherits class :doc:`HtmlReport <html_report>`.
    """

    __intro = """<h2 class="nocount">Table of contents</h2>
    <ol>
      <li><a href="#introduction">Introduction</a></li>
      <li><a href="#signal_details">Detailed signal information</a></li>
      <li><a href="#signal_index">Signal index</a></li>
    </ol>
    <h2 id="introduction">Introduction</h2>
    <p>This documents lists the signal interfaces.</p>
    """

    __table_unused = """
  <table id="unused">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Configurations</th>
      </tr>
    </thead>
    <tbody>
"""

    __table_detailed_sig_desc = """
  <table id="sig_desc">
    <thead>
      <tr>
        <th>Unit</th>
        <th>Type</th>
        <th>Class</th>
        <th>Min</th>
        <th>Max</th>
        <th>Lsb</th>
        <th>Offset</th>
        <th>Configs</th>
      </tr>
    </thead>
    <tbody>
"""

    __table_detailed_sig_desc_ext = """
  <table id="sig_desc">
    <thead>
      <tr>
        <th>Unit</th>
        <th>Type</th>
        <th>Init Value</th>
        <th>Min</th>
        <th>Max</th>
        <th>Config Doc</th>
      </tr>
    </thead>
    <tbody>
"""

    __table_detailed_sig_def = """
  <table id="detailed_sig_def">
    <thead>
      <tr>
        <th>Defined in unit</th>
        <th>in projects</th>
      </tr>
    </thead>
    <tbody>
"""

    __table_detailed_sig_cons = """
  <table id="detailed_sig_cons">
    <thead>
      <tr>
        <th>Consumed by units</th>
        <th>in projects</th>
      </tr>
    </thead>
    <tbody>
"""

    def __init__(self, build_cfg, unit_cfg, sig_if):
        """Initialize class instance.

        Args:
            build_cfg (BuildProjConfig): holds all the build configs
            unit_cfg (UnitConfigs): object holding all unit interfaces
            sig_if (SignalInterfaces): object holding signal interface information
        """
        super().__init__('Signal interface report')
        self._build_cfg = build_cfg
        self._unit_cfg = unit_cfg
        self._sig_if = sig_if
        self._format_unit_data()

    def _gen_sigs_details(self):
        """Generate detailed signal information."""
        out = '  <h2 id="signal_details">Detailed Signal Information</h2>\n'
        for signal in sorted(self._if.keys()):
            out += self._gen_sig_details(signal)
        return out

    def _gen_sig_details(self, signal):
        """Generate detailed signal information."""
        out = f'  <h3 id="{signal}">{signal}</h3>\n'
        unit = tuple(self._if[signal]['def'].keys())[0]  # ugly! use the first defining unit.
        # Check that it is a unit, and not from the inteface definition
        if unit[:2] == 'Vc':
            sig_def = defaultdict(lambda: '-', self._unit_cfg.get_per_unit_cfg()[unit]['outports'][signal])
            out += f'  <p>{sig_def["description"]}</p>'
            out += self.__table_detailed_sig_desc
            out += '      <tr>\n'
            out += f'        <td>{sig_def["unit"]}</td>\n'
            out += f'        <td>{sig_def["type"]}</td>\n'
            out += f'        <td>{sig_def["class"]}</td>\n'
            out += f'        <td>{sig_def["min"]}</td>\n'
            out += f'        <td>{sig_def["max"]}</td>\n'
            out += f'        <td>{sig_def["lsb"]}</td>\n'
            out += f'        <td>{sig_def["offset"]}</td>\n'
            out += f'        <td>{sig_def["configs"]}</td>\n'
            out += '      </tr>\n'
            out += '    </tbody>\n'
            out += '  </table>\n  <p></p>\n'
        else:
            sig_def = defaultdict(lambda: '-', self._sig_if.get_raw_io_cnfg()[unit][signal])
            out += f'  <p>{sig_def["description"]}</p>'
            out += self.__table_detailed_sig_desc_ext
            out += '      <tr>\n'
            out += f'        <td>{sig_def["unit"]}</td>\n'
            out += f'        <td>{sig_def["type"]}</td>\n'
            out += f'        <td>{sig_def["init"]}</td>\n'
            out += f'        <td>{sig_def["min"]}</td>\n'
            out += f'        <td>{sig_def["max"]}</td>\n'
            out += f'        <td>{unit}</td>\n'
            out += '      </tr>\n'
            out += '    </tbody>\n'
            out += '  </table>\n  <p></p>\n'

        out += self.__table_detailed_sig_def
        for unit, prjs in self._if[signal]['def'].items():
            out += '      <tr>\n'
            out += f'        <td>{unit}</td>\n'
            out += f'        <td>{prjs}</td>\n'
            out += '      </tr>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'

        if 'consumers' in self._if[signal]:
            out += '  <p></p>\n'
            out += self.__table_detailed_sig_cons
            for units, prjs in self._if[signal]['consumers'].items():
                out += '      <tr>\n'
                out += f'        <td>{units}</td>\n'
                out += f'        <td>{prjs}</td>\n'
                out += '      </tr>\n'
            out += '    </tbody>\n'
            out += '  </table>\n'
        return out

    def _format_unit_data(self):
        """Format data per unit."""
        self._if = {}
        prj_name = self._build_cfg.get_prj_config()
        # internal signals
        prj_cfg = self._unit_cfg.get_per_cfg_unit_cfg()
        ext_out_prj = self._sig_if.get_external_outputs()
        if 'outports' in prj_cfg:
            for sig, data in prj_cfg['outports'].items():
                prod_unit = list(data.keys())[0]
                self._if.setdefault(sig, {}).setdefault('def', {}).setdefault(prod_unit, []).append(prj_name)
                cons_units = []
                for sig_type, osig in ext_out_prj.items():
                    if sig in osig:
                        cons_units = [sig_type]
                        break
                if sig in prj_cfg['inports']:
                    cons_units.extend(list(prj_cfg['inports'][sig].keys()))
                if cons_units:
                    (self._if[sig].setdefault('consumers', {})
                                  .setdefault(tuple(sorted(cons_units)), [])
                                  .append(prj_name))

        # external signals
        prj_cfg = self._unit_cfg.get_per_cfg_unit_cfg()
        ext_in_prj = self._sig_if.get_external_inputs()
        for sig_type, osig in ext_in_prj.items():
            for sig, data in osig.items():
                self._if.setdefault(sig, {}).setdefault('def', {}).setdefault(sig_type, []).append(prj_name)
                if 'inports' in prj_cfg and sig in prj_cfg['inports']:
                    (self._if[sig].setdefault('consumers', {})
                                  .setdefault(tuple(sorted(prj_cfg['inports'][sig].keys())), [])
                                  .append(prj_name))

    def _gen_signal_toc(self):
        """Generate a signal TOC for the unit with signal inconsistencies.

        Hyperlinks to more in depth signal information.
        """
        out = '  <h2 id="signal_index">Signal index</h2>\n'
        for signal in sorted(self._if.keys()):
            out += f'  <div><a href="#{signal}">{signal}</a></div>\n'
        return out

    def gen_contents(self):
        """Generate report contents from the signal interfaces data.

        Overrides HtmlReport.gen_contents()
        """
        html = []
        html += self.__intro
        html += self._gen_sigs_details()
        html += self._gen_signal_toc()
        return ''.join(html)
