# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing classes for the signal interfaces report."""
from collections import defaultdict
from powertrain_build.html_report import HtmlReport


class SigIfHtmlReportAll(HtmlReport):
    """Signal interface html report.

    Inherits class :doc:`HtmlReport <html_report>`.
    """

    __intro = """
    <h2 id="introduction">Introduction</h2>
    <p>This documents lists the signal interfaces.</p>
    """

    __signal_info = """<h2 class="nocount">Table of contents</h2>
    <ol>
    <li><a href="#signal_details">Detailed signal information</a></li>
    <li><a href="#signal_index">Signal index</a></li>
    </ol>
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

    def __init__(self, build_cfg, unit_cfgs, sig_ifs):
        """Initialize class instance.

        Args:
            build_cfg (BuildProjConfig): holds all the build configs
            unit_cfg (UnitConfigs): object holding all unit interfaces
            sig_if (CsvSignalInterfaces): object holding signal interface information
        """
        super().__init__('Signal interface report')

        self._build_cfg = build_cfg
        self._unit_cfg_all = unit_cfgs
        self._sig_if_all = sig_ifs

        self._format_unit_data()

    def _gen_sigs_details(self):
        """Generate detailed signal information."""
        self._out_all_sd = {}

        for prj, ifin in self._if_all.items():
            out = ''
            self._if = ifin
            self._sig_if = self._sig_if_all.get(prj)
            out += '  <h2 id="signal_details">Detailed Signal Information</h2>\n'
            for signal in sorted(self._if.keys()):
                out += self._gen_sig_details(signal, prj)
            self._out_all_sd.update({prj: out})

        return self._out_all_sd

    def _gen_sig_details(self, signal, prj):
        """Generate detailed signal information."""
        out = f'  <h3 id="{signal}">{signal}</h3>\n'
        try:
            unit = tuple(self._if[signal]['def'].keys())[0]  # ugly! use the first defining unit.

            # Check that it is a unit, and not from the interface definition
            self._unit_cfg = self._unit_cfg_all.get(prj)
            if unit[:2] == 'Vc':
                per_unit_config = self._unit_cfg.get_per_unit_cfg('all')[unit]['outports'][signal]
                sig_def = defaultdict(lambda: '-', per_unit_config)
                out += f"  <p>{sig_def['description']}</p>"
                out += self.__table_detailed_sig_desc
                out += "      <tr>\n"
                out += f"        <td>{sig_def['unit']}</td>\n"
                out += f"        <td>{sig_def['type']}</td>\n"
                out += f"        <td>{sig_def['class']}</td>\n"
                out += f"        <td>{sig_def['min']}</td>\n"
                out += f"        <td>{sig_def['max']}</td>\n"
                out += f"        <td>{sig_def['lsb']}</td>\n"
                out += f"        <td>{sig_def['offset']}</td>\n"
                out += f"        <td>{sig_def['configs']}</td>\n"
                out += "      </tr>\n"
                out += "    </tbody>\n"
                out += "  </table>\n  <p></p>\n"
            else:
                sig_def = defaultdict(lambda: '-', self._sig_if.get_raw_io_cnfg()[unit][signal])
                out += f"  <p>{sig_def['description']}</p>"
                out += self.__table_detailed_sig_desc_ext
                out += "      <tr>\n"
                out += f"        <td>{sig_def['unit']}</td>\n"
                out += f"        <td>{sig_def['type']}</td>\n"
                out += f"        <td>{sig_def['init']}</td>\n"
                out += f"        <td>{sig_def['min']}</td>\n"
                out += f"        <td>{sig_def['max']}</td>\n"
                out += f"        <td>{unit}</td>\n"
                out += "      </tr>\n"
                out += "    </tbody>\n"
                out += "  </table>\n  <p></p>\n"
        except KeyError:
            pass

        out += self.__table_detailed_sig_def
        prj_str = ""
        unit_str = ""
        for cur_prj, ifin in self._if_all.items():
            self._if = ifin
            prj_str += f"  {cur_prj}"
            try:
                unit_str = ""
                for unit in self._if[signal]['def']:
                    unit_str += '  '.join(unit)
            except KeyError:
                continue
        out += "      <tr>\n"
        out += f"        <td>{unit_str}</td>\n"
        out += f"        <td>{prj_str}</td>\n"
        out += "      </tr>\n"
        out += "    </tbody>\n"
        out += "  </table>\n"

        out += self.__table_detailed_sig_cons
        prj_str = ""
        units_str = ""
        for cur_prj, ifin in self._if_all.items():
            self._if = ifin
            try:
                if 'consumers' in self._if[signal]:
                    prj_str += f"  {cur_prj}"
                    out += "  <p></p>\n"
                    units_str = ""
                    for units in self._if[signal]['consumers']:
                        units_str += '  '.join(units)
            except KeyError:
                continue
        out += "      <tr>\n"
        out += f"        <td>{units_str}</td>\n"
        out += f"        <td>{prj_str}</td>\n"
        out += "      </tr>\n"
        out += "    </tbody>\n"
        out += "  </table>\n"
        return out

    def _format_unit_data(self):
        """Format data per unit."""
        self._if_all = {}
        for prj, unit_cfg in self._unit_cfg_all.items():
            self._if = {}
            self._unit_cfg = unit_cfg
            prj_cfg = self._unit_cfg.get_per_cfg_unit_cfg(prj)
            sig_if = self._sig_if_all.get(prj)
            self._sig_if = sig_if

            # internal signals
            ext_out_prj = self._sig_if.get_external_outputs(prj)
            if 'outports' in prj_cfg:
                for sig, data in prj_cfg['outports'].items():
                    prod_unit = list(data.keys())[0]
                    self._if.setdefault(sig, {}).setdefault('def', {}).setdefault(prod_unit, []).append(prj)
                    cons_units = []
                    for sig_type, osig in ext_out_prj.items():
                        if sig in osig:
                            cons_units = [sig_type]
                            break
                    if sig in prj_cfg['inports']:
                        cons_units.extend(list(prj_cfg['inports'][sig].keys()))
                    if cons_units:
                        self._if[sig].setdefault('consumers', {}).setdefault(tuple(sorted(cons_units)), []).append(prj)

            # external signals
            ext_in_prj = self._sig_if.get_external_inputs(prj)
            for sig_type, osig in ext_in_prj.items():
                for sig, data in osig.items():
                    self._if.setdefault(sig, {}).setdefault('def', {}).setdefault(sig_type, []).append(prj)
                    if 'inports' in prj_cfg and sig in prj_cfg['inports']:
                        (self._if[sig].setdefault('consumers', {})
                                      .setdefault(tuple(sorted(prj_cfg['inports'][sig].keys())), [])
                                      .append(prj))
            self._if_all.update({prj: self._if})
        return self._if_all

    def _gen_signal_toc(self):
        """Generate a signal TOC for the unit with signal inconsistencies.

        Hyperlinks to more in depth signal information.
        """
        self._out_all_st = {}
        for prj, ifin in self._if_all.items():
            out = ''
            self._if = ifin
            out += '  <h2 id="signal_index">Signal index</h2>\n'
            for signal in sorted(self._if.keys()):
                out += f'  <div><a href="#{signal}">{signal}</a></div>\n'
            self._out_all_st.update({prj: out})

        return self._out_all_st

    def _gen_contents_intro(self):
        """Generate report contents from the signal interfaces data.

        Specialises HtmlReport.gen_contents()
        """
        html = []
        html += self.__intro
        return ''.join(html)

    def _gen_contents_signal_info(self):
        """Generate report contents from the signal interfaces data.

        Specialises HtmlReport.gen_contents()
        """
        html = []
        html += self.__signal_info
        return ''.join(html)

    def _generate_report_string_intro(self):
        """Generate a html report as string."""
        html = []
        html += self._gen_header()
        html += self._gen_contents_intro()
        html += self._gen_end()
        return ''.join(html)

    def generate_report_file_if(self, filename):
        """Generate a html report and save to file."""
        filename_intro = filename + '_intro.html'
        with open(filename_intro, 'w', encoding="utf-8") as fhndl:
            fhndl.write(self._generate_report_string_intro())

        self._gen_sigs_details()
        self._gen_signal_toc()
        for prj, out in self._out_all_sd.items():
            html = []
            html += self._gen_header()
            html += self._gen_contents_signal_info()
            html += out
            html += self._out_all_st.get(prj)
            html += self._gen_end()
            with open(f'{filename}_{prj}.html', 'w', encoding="utf-8") as fhndl:
                fhndl.write(''.join(html))
