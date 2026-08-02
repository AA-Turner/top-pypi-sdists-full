# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing classes for generation of signal consistency check report."""
from powertrain_build.signal_incons_html_rep_base import SigConsHtmlReportBase


class SigConsHtmlReport(SigConsHtmlReportBase):
    """Generate html report from the signal consistency check result.

    (see :doc:`signal_interfaces`)

    Inherits :doc:`SigConsHtmlReportBase <signal_incons_html_rep_base>`.
    """

    __intro = """<h2 class="nocount">Table of contents</h2>
    <ol>
      <li><a href="#introduction">Introduction</a></li>
      <li><a href="#unit_details">Detailed unit information</a></li>
      <li><a href="#ext_sigs">External signals</a>
      <ol>
        <li><a href="#ext_missing">Missing external signals</a></li>
        <li><a href="#ext_unused">Unused external signals</a></li>
      </ol></li>
      <li><a href="#unit_index">Unit index</a></li>
    </ol>
    <h2 id="introduction">Introduction</h2>
    <p>This documents lists inconsistencies in the internal and external signal configuration.</p>
    """

    def __init__(self, res_dict=None):
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
                }
            }
        """
        super().__init__(res_dict)
        self.set_res_dict(res_dict)

    def _gen_unit_toc(self):
        """Generate a unit TOC for the unit with signal inconsistencies.

        Hyperlinks to more in depth unit information.
        """
        out = '  <h2 id="unit_index">Unit index</h2>\n'
        for unit in sorted(self._ext_units | self._int_units):
            out += f'  <div><a href="#{unit}">{unit}</a></div>\n'
        return out

    def _gen_units(self):
        """Generate all the information regarding all the units."""
        out = '  <h2 id="unit_details">Detailed Unit Information</h2>\n'
        for unit in sorted(self._ext_units | self._int_units):
            out += self._gen_unit(unit)
        return out

    def _gen_unit(self, unit):
        """Generate the html-report for the unit specific information."""
        out = f'  <h3 id="{unit}">{unit}</h3>\n'
        if unit in self._int_units:
            unit_data = self._res_dict['sigs']['int'][unit]
            out += self._gen_missing_sigs(unit_data)
            out += self._gen_unused_sigs(unit_data)
            out += self._gen_multiple_def_sigs(unit_data)
            out += self._gen_int_inconsistent_defs(unit_data)
        if unit in self._ext_units:
            out += self._gen_ext_inconsistent_defs(unit)
        return out

    def _gen_missing_sigs(self, unit_data, out=''):
        """Generate the unit specific information for missing signal in a unit."""
        out = '  <h4>Missing signals</h4>\n' \
              '  <p>Inports whose signals are not generated in the ' \
              'listed configuration(s).</p>'
        return super()._gen_missing_sigs(unit_data, out)

    def _gen_unused_sigs(self, unit_data, out=''):
        """Generate the unit specific information for the unused signals wihtin a unit."""
        out = '  <h4>Unused signals</h4>\n' \
              '  <p>Outports that are generated, but not used in the ' \
              'listed configuration(s).</p>'
        return super()._gen_unused_sigs(unit_data, out)

    def _gen_multiple_def_sigs(self, unit_data, out=''):
        """Generate unit specific information for the signals that are generated more than once."""
        out = '  <h4>Multiple defined signals</h4>\n' \
              '  <p>Outports that are generated more than once in ' \
              'the listed configuration(s).</p>'
        return super()._gen_multiple_def_sigs(unit_data, out)

    def _gen_ext_inconsistent_defs(self, unit, out=''):
        """Generate a report of inconsistent variable definition parameters.

        Report inconsistencies between the producing signal definition, and the
        signal definitions in the external interface definition.
        """
        out = '  <h4>External signal inconsistencies</h4>\n' \
              '  <p>In-/Out-ports that have different variable definitions ' \
              'than in the interface definition file.</p>'
        return super()._gen_ext_inconsistent_defs(unit, out)

    def _gen_int_inconsistent_defs(self, unit_data, out=''):
        """Generate a report of inconsistent variable definition parameters.

        Inconsistent for between the producing signal definition, and the
        consuming signal definitions for SPM internal signals.
        """
        out = '  <h4>Internal signal inconsistencies</h4>\n' \
              '  <p>Inports that have different variable definitions ' \
              'than the producing outport.</p>'
        return super()._gen_int_inconsistent_defs(unit_data, out)

    def _gen_ext_signals_report(self, type_, comment):
        """Generate report for external signals."""
        out = f'  <h3 id="ext_{type_}">{type_.capitalize()} external signals</h3>\n'
        out += f'<p>{comment}</p>'
        try:
            ext_data = self._res_dict['sigs']['ext'][type_]
            out += self._table_unused
            for var in sorted(ext_data.keys()):
                configs = ext_data[var]
                out += '  <tr>\n'
                out += f'        <td>{var}</td>\n'
                out += f'        <td>{self._set_to_str(configs)}</td>\n'
                out += '      </tr>\n'
            out += '    </tbody>\n'
            out += '  </table>\n'
        except KeyError:
            pass
        return out

    def set_res_dict(self, res_dict):
        """Set the result dictionary used to generate the html-report.

        Args:
            res_dict (dict): result dict from the signal interface consistency check

        See class constructor for dict structure.
        """
        self._res_dict = res_dict
        self._ext_units = set()
        self._int_units = set()
        if res_dict is not None and 'sigs' in res_dict:
            if 'ext' in res_dict['sigs'] and 'inconsistent_defs' in res_dict['sigs']['ext']:
                self._ext_units = set(self._res_dict['sigs']['ext']['inconsistent_defs'].keys())
            if 'int' in res_dict['sigs']:
                self._int_units = set(self._res_dict['sigs']['int'].keys())

    def gen_contents(self):
        """Generate report contents from the signal inconsistency check result dictionary.

        Overrides HtmlReport.gen_contents()
        """
        html = []
        html += self.__intro
        html += self._gen_units()
        html += '  <h2 id="ext_sigs">Signals missing and unused in the ' \
                'interface definition</h2>\n'
        html += self._gen_ext_signals_report('missing', 'Signals not generated by '
                                                        'Vcc SW, but are defined in '
                                                        'the Interface definition to be '
                                                        'generated')
        html += self._gen_ext_signals_report('unused', 'Signals defined to be generated by '
                                                       'supplier SW, but are not used '
                                                       'by VCC SW')
        html += self._gen_unit_toc()
        return ''.join(html)
