# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing classes for generation of signal consistency check report."""
from powertrain_build.html_report import HtmlReport


class SigConsHtmlReportBase(HtmlReport):
    """Generate html report from the signal consistency check result.

    (see :doc:`signal_interfaces`)

    Inherits :doc:`HtmlReport <html_report>`.
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
    _table_unused = """
  <table id="unused">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Configurations</th>
      </tr>
    </thead>
    <tbody>
    """
    _table_incons = """
  <table id="inconsistent">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Variable parameter</th>
        <th>Difference</th>
      </tr>
    </thead>
    <tbody>
    """
    _table_unknown = """
          <table id="unknown">
            <thead>
              <tr>
                <th>Variable</th>
                <th>Units</th>
              </tr>
            </thead>
            <tbody>
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
        super().__init__('Signal consistency report')

    @staticmethod
    def _set_to_str(set_):
        """Convert a set to a sorted string."""
        out = ""
        for conf in sorted(set_):
            out += conf + ', '
        return out[:-2]

    def _gen_missing_sigs(self, unit_data, out=''):
        """Generate the unit specific information for missing signal in a unit."""
        out += self._table_unused
        for var in sorted(unit_data['missing'].keys()):
            configs = unit_data['missing'][var]
            out += '  <tr>\n'
            out += f'        <td>{var}</td>\n'
            out += f'        <td>{self._set_to_str(configs)}</td>\n'
            out += '      </tr>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_unused_sigs(self, unit_data, out=''):
        """Generate the unit specific information for the unused signals wihtin a unit."""
        out += self._table_unused
        for var in sorted(unit_data['unused'].keys()):
            configs = unit_data['unused'][var]
            out += '  <tr>\n'
            out += f'        <td>{var}</td>\n'
            out += f'        <td>{self._set_to_str(configs)}</td>\n'
            out += '      </tr>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_multiple_def_sigs(self, unit_data, out=''):
        """Generate unit specific information for the signals that are generated more than once."""
        out += self._table_unused
        for var in sorted(unit_data['multiple_defs'].keys()):
            configs = unit_data['multiple_defs'][var]
            out += '  <tr>\n'
            out += f'        <td>{var}</td>\n'
            out += f'        <td>{self._set_to_str(configs)}</td>\n'
            out += '      </tr>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_ext_inconsistent_defs(self, unit, out=''):
        """Generate a report of inconsistent variable definition parameters.

        Report inconsistencies between the producing signal definition, and the
        signal definitions in the external interface definition.
        """
        out += self._table_incons
        incons_unit = self._res_dict['sigs']['ext']['inconsistent_defs'][unit]
        for var in sorted(incons_unit.keys()):
            first_cells = f'  <tr>\n        <td>{var}</td>\n'
            for v_par, desc in incons_unit[var].items():
                out += first_cells
                out += f'        <td>{v_par}</td>\n'
                out += f'        <td>{desc}</td>\n'
                out += '      </tr>\n'
                first_cells = '      <tr>\n      <td></td>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out

    def _gen_int_inconsistent_defs(self, unit_data, out=''):
        """Generate a report of inconsistent variable definition parameters.

        Inconsistent for between the producing signal definition, and the
        consuming signal definitions for SPM internal signals.
        """
        out += self._table_incons
        for var in sorted(unit_data['inconsistent_defs'].keys()):
            configs = unit_data['inconsistent_defs'][var]
            first_cells = f'  <tr>\n        <td>{var}</td>\n'
            for v_par, desc in configs.items():
                out += first_cells
                out += f'        <td>{v_par}</td>\n'
                out += f'        <td>{desc}</td>\n'
                out += '      </tr>\n'
                first_cells = '      <tr>\n      <td></td>\n'
        out += '    </tbody>\n'
        out += '  </table>\n'
        return out
