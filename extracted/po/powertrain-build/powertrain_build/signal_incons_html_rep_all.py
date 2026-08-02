# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing classes for generation of signal consistency check report."""
import json

from powertrain_build.signal_incons_html_rep_base import SigConsHtmlReportBase


class SigConsHtmlReportAll(SigConsHtmlReportBase):
    """Generate html report from the signal consistency check result.

    (see :doc:`signal_interfaces`)

    Inherits :doc:`HtmlReport <html_report>`.
    """

    __intro_all = """<h2 id="introduction">Introduction</h2>
    <p>This documents lists inconsistencies in the internal and external signal configuration.</p>
"""
    __table_incons = """  <table id="inconsistent">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Variable parameter</th>
        <th>Difference</th>
        <th>Configurations</th>
      </tr>
    </thead>
    <tbody>"""

    __toc_ext_sig = """<h2 class="nocount">Table of contents</h2>'
    <ol>
    <li><a href="#ext_sigs">External signals</a>
    <ol>
    <li><a href="#ext_missing">Missing external signals</a></li>
    <li><a href="#ext_unused">Unused external signals</a></li>
    </ol></li>
    <h2 id="ext_sigs">Signals missing and unused in the interface definition</h2>\n
    """

    _toc_unit_details = """<h2 class="nocount">Table of contents</h2>
    <ol>
    <li><a href="#unit_details">Detailed unit information</a></li>
    <li><a href="#unit_index">Unit index</a></li>
    </ol>
    """

    def __init__(self, res_dicts=None):
        """Initialize class instance.

        Args:
            res_dict (dict): result dict from the signal interface consistency check

        The dict shall have the following format::

            {
                "sigs": { "ext": {"missing": {},
                                  "unused": {},
                                  "inconsistent_defs": {}},
                          "int": {"UNIT_NAME": {"missing": {},
                                                "unused": {},
                                                "multiple_defs": {}
                                                "inconsistent_defs": {}}
                },
                "never_active_signals": {
                    "UNIT_NAME": [signal_one, ...]
                }
            }
        """
        super().__init__(res_dicts)
        self.set_res_dict(res_dicts)

    def _gen_unit_toc(self):
        """Generate a unit TOC for the unit with signal inconsistencies.

        Hyperlinks to more in depth unit information.
        """
        self._out_all_unit_toc = {}
        for prj, units in self._all_units.items():
            out = '  <h2 id="unit_index">Unit index</h2>\n'
            for unit in sorted(units):
                out += f'  <div><a href="#{unit}">{unit}</a></div>\n'
            self._out_all_unit_toc.update({prj: out})

    def _gen_units(self):
        """Generate all the information regarding all the units."""
        self._out_all_units = {}
        self._prj = ''
        for prj, units in self._all_units.items():
            out = '  <h2 id="unit_details">Detailed Unit Information</h2>\n'
            for unit in sorted(units):
                out += self._gen_unit(prj, unit)
            self._out_all_units.update({prj: out})
        return self._out_all_units

    def _gen_unit(self, project, unit):
        """Generate the html-report for the unit specific information."""
        unit_data_all = {}
        out = f'  <h3 id="{unit}">{unit}</h3>\n'
        if project in self._int_units_all and unit in self._int_units_all[project]:
            for prj, res_dict in self._res_dict_all.items():
                if unit in res_dict['sigs']['int']:
                    unit_data = res_dict['sigs']['int'][unit]
                    unit_data_all.update({prj: unit_data})
            _res_dict = self._res_dict_all.get(project)
            unit_data = _res_dict['sigs']['int'][unit]
            out += '  <h4>Missing signals</h4>\n' \
                   '  <p>Inports whose signals are not generated in the ' \
                   'listed configuration(s).</p>'
            out += self._gen_missing_sigs(unit_data, unit_data_all)
            out += '  <h4>Unused signals</h4>\n' \
                   '  <p>Outports that are generated, but not used in the ' \
                   'listed configuration(s).</p>'
            out += self._gen_unused_sigs(unit_data, unit_data_all)
            out += '  <h4>Multiple defined signals</h4>\n' \
                   '  <p>Outports that are generated more than once in ' \
                   'the listed configuration(s).</p>'
            out += self._gen_multiple_def_sigs(unit_data, unit_data_all)
            out += '  <h4>Internal signal inconsistencies</h4>\n' \
                   '  <p>Inports that have different variable definitions ' \
                   'than the producing outport.</p>'
            out += self._gen_int_inconsistent_defs(unit_data, unit_data_all)
        if project in self._ext_units_all and unit in self._ext_units_all[project]:
            out += self._gen_unit_ext(project, unit)
        if project in self._res_dict_all and \
            'never_active_signals' in self._res_dict_all[project] and \
                unit in self._res_dict_all[project]['never_active_signals']:
            out += '  <h4>Never active signals</h4>\n' \
                   '  <p>Never active signals will not appear in generated .c file, ' \
                   'signals probablty lead to terminators in Simulink model.</p>'
            out += self._gen_never_active_sigs(self._res_dict_all[project]['never_active_signals'][unit])
        return out

    def _gen_unit_ext(self, project, unit):
        out = ''
        self._unit_data_all = {}
        if unit in self._res_dict_all[project]['sigs']['ext']['inconsistent_defs'].keys():
            out += '  <h4>External signal inconsistencies</h4>\n' \
                   '  <p>In-/Out-ports that have different variable definitions ' \
                   'than in the interface definition file.</p>'
            out += self._gen_ext_inconsistent_defs(project, unit)
        return out

    def _gen_signals_table(self, unit_data, unit_data_all, key, out=''):
        """Generate the unit specific information for KEY in a unit."""

        if key not in unit_data:
            return out

        out += self._table_unused
        for var in sorted(unit_data[key]):
            configs_str = ""
            for unit_data_cfg in unit_data_all.values():
                if key in unit_data_cfg and var in unit_data_cfg[key]:
                    configs = unit_data_cfg[key][var]
                    configs_str += f"  {self._set_to_str(configs)}"
            out += '  <tr>\n'
            out += f'        <td>{var}</td>\n'
            out += f'        <td>{configs_str}</td>\n'
            out += '      </tr>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_missing_sigs(self, unit_data, unit_data_all, out=''):
        """Generate the unit specific information for missing signal in a unit."""
        return self._gen_signals_table(unit_data, unit_data_all, key='missing', out=out)

    def _gen_unused_sigs(self, unit_data, unit_data_all, out=''):
        """Generate the unit specific information for the unused signals wihtin a unit."""
        return self._gen_signals_table(unit_data, unit_data_all, key='unused', out=out)

    def _gen_multiple_def_sigs(self, unit_data, unit_data_all, out=''):
        """Generate unit specific information for the signals that are generated more than once."""
        return self._gen_signals_table(unit_data, unit_data_all, key='multiple_defs', out=out)

    def _gen_never_active_sigs(self, never_active_signals):
        """Generate unit specific information for the signals that are never active."""
        out = self._table_unused
        for signal in never_active_signals:
            out += '  <tr>\n'
            out += f'        <td>{signal}</td>\n'
            out += '        <td></td>\n'
            out += '      </tr>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_ext_inconsistent_defs(self, project, unit, out=''):
        """Generate a report of inconsistent variable definition parameters.

        Report inconsistencies between the producing signal definition, and the
        signal definitions in the external interface definition.
        """
        inconsistent_defs_key = 'inconsistent_defs'
        if inconsistent_defs_key not in self._res_dict_all[project]['sigs']['ext']:
            return out

        out += self.__table_incons
        incons_unit = self._res_dict_all[project]['sigs']['ext'][inconsistent_defs_key][unit]
        for var in sorted(incons_unit.keys()):
            first_cells = f'\n      <tr>\n        <td>{var}</td>\n'
            for v_par, desc in incons_unit[var].items():
                out += first_cells
                out += f'        <td>{v_par}</td>\n'
                out += f'        <td>{desc}</td>\n'
                out += f'        <td>{project}</td>\n'
                out += '      </tr>\n'
                first_cells = '      <tr>\n      <td></td>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_int_inconsistent_defs(self, unit_data, unit_data_all, out=''):
        """Generate a report of inconsistent variable definition parameters.

        Inconsistent for between the producing signal definition, and the
        consuming signal definitions for SPM internal signals.
        """
        inconsistent_defs_key = 'inconsistent_defs'
        if inconsistent_defs_key not in unit_data:
            return out

        out += self.__table_incons
        for var in sorted(unit_data[inconsistent_defs_key].keys()):
            configs_str = ""
            for prj_cfg in unit_data_all.keys():
                configs_str += f"  {prj_cfg}"
            first_cells = f'\n      <tr>\n        <td>{var}</td>\n'
            configs = unit_data[inconsistent_defs_key][var]
            for v_par, desc in configs.items():
                out += first_cells
                out += f'        <td>{v_par}</td>\n'
                out += f'        <td>{desc}</td>\n'
                out += f'        <td>{configs_str}</td>\n'
                out += '      </tr>\n'
                first_cells = '      <tr>\n      <td></td>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_ext_signals_report(self, type_, comment):
        """Generate report for external signals."""
        out = f'  <h3 id="ext_{type_}">{type_.capitalize()} external signals</h3>\n'
        out += f'<p>{comment}</p>'
        try:
            res_dict = self._res_dict_all.get(self._prj)
            out += self._table_unused
            ext_data = res_dict['sigs']['ext'][type_]
            for var in sorted(ext_data.keys()):
                configs_str = ""
                for res_dict_cfg in self._res_dict_all.values():
                    if type_ in res_dict_cfg['sigs']['ext']:
                        ext_data_cfg = res_dict_cfg['sigs']['ext'][type_]
                        configs = ext_data_cfg[var]
                        configs_str += "  " + self._set_to_str(configs)
                out += '  <tr>\n'
                out += f'        <td>{var}</td>\n'
                out += f'        <td>{configs_str}</td>\n'
                out += '      </tr>\n'
            out += '    </tbody>\n'
            out += '  </table>\n'
        except KeyError:
            pass
        return out

    def set_res_dict(self, res_dicts):
        """Set the result dictionary used to generate the html-report.

        Args:
            res_dicts (dict): result dict from the signal interface consistency check

        See class constructor for dict structure.
        """
        # nesting defaultdicts is bad so we use this hack
        regular_res_dicts = json.loads(json.dumps(res_dicts))
        self._res_dict_all = regular_res_dicts
        self._ext_units_all = {}
        self._int_units_all = {}
        self._all_units = {}
        for prj, res_dict in self._res_dict_all.items():
            _ext_units = set()
            _int_units = set()
            _units_with_never_active_signals = set()
            if res_dict is not None and 'sigs' in res_dict:
                if 'ext' in res_dict['sigs'] and 'inconsistent_defs' in res_dict['sigs']['ext']:
                    _ext_units = set(res_dict['sigs']['ext']['inconsistent_defs'].keys())
                    self._ext_units_all.update({prj: _ext_units})
                if 'int' in res_dict['sigs']:
                    _int_units = set(res_dict['sigs']['int'].keys())
                    self._int_units_all.update({prj: _int_units})
                if 'never_active_signals' in res_dict:
                    _units_with_never_active_signals = res_dict['never_active_signals'].keys()
            self._all_units[prj] = _ext_units | _int_units | _units_with_never_active_signals

    def _gen_contents_intro(self):
        """Generate report contents from the signal interfaces data."""
        html = []
        html += self.__intro_all
        return ''.join(html)

    def _gen_contents_toc_ext_sig(self):
        """Generate report contents from the signal interfaces data.

        Specialises HtmlReport.gen_contents()
        """
        html = []
        html += self.__toc_ext_sig
        return ''.join(html)

    def _gen_contents_toc_unit_details(self):
        """Generate report contents from the signal interfaces data.

        Specialises HtmlReport.gen_contents()
        """
        html = []
        html += self._toc_unit_details
        return ''.join(html)

    def _gen_contents_ext_signals(self):
        """Generate report contents from the signal inconsistency check result dictionary."""
        html = []
        html += self._gen_contents_toc_ext_sig()
        html += self._gen_ext_signals_report('missing', 'Signals not generated by '
                                                        'Vcc SW, but are defined in '
                                                        'the Interface definition to be '
                                                        'generated')
        html += self._gen_ext_signals_report('unused', 'Signals defined to be generated by '
                                                       'supplier SW, but are not used '
                                                       'by VCC SW')
        return ''.join(html)

    def _generate_report_string_intro(self):
        """Generate a html report as string."""
        html = []
        html += self._gen_header()
        html += self._gen_contents_intro()
        html += self._gen_end()
        return ''.join(html)

    def _generate_report_string_ext_signals(self):
        """Generate a html report as string."""
        html = []
        html += self._gen_header()
        html += self._gen_contents_ext_signals()
        html += self._gen_end()
        return ''.join(html)

    def generate_report_file_signal_check(self, filename):
        """Generate a html report and save to file."""
        filename_intro = filename + '_intro.html'
        with open(filename_intro, 'w', encoding="utf-8") as fhndl:
            fhndl.write(self._generate_report_string_intro())

        self._gen_units()
        self._gen_unit_toc()
        for key, out in self._out_all_units.items():
            html = []
            html += self._gen_header()
            html += self._gen_contents_toc_unit_details()
            html += out
            html += self._out_all_unit_toc.get(key, '')
            html += self._gen_end()
            with open(f'{filename}_{key}.html', 'w', encoding="utf-8") as fhndl:
                fhndl.write(''.join(html))
