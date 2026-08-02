# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module for a2l-file generation."""

import sys
import re
import logging
from string import Template
from pprint import pformat
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.types import a2l_type, a2l_range

LOG = logging.getLogger()


class A2l(ProblemLogger):
    """Class for a2l-file generation."""

    def __init__(self, var_data_dict, prj_cfg):
        """Generate a2l-file from provided data dictionary.

        Args:
            var_data_dict (dict): dict defining all variables and parameters in a2l

        Sample indata structure:
        ::

            {
                "function": "rVcAesSupM",
                "vars": {
                    "rVcAesSupM_p_SupMonrSCTarDly": {
                        "var": {
                            "type": "Float32",
                            "cvc_type": "CVC_DISP"
                        },
                        "a2l_data": {
                            "unit": "kPa",
                            "description": "Low pass filtered supercharger target pressure",
                            "max": "300",
                            "min": "0",
                            "lsb": "1",
                            "offset": "0",
                            "bitmask": None,
                            "x_axis": None,
                            "y_axis": None,
                        },
                        "array": None
                    }
                }
            }
        """
        super().__init__()
        self._var_dd = var_data_dict
        self._prj_cfg = prj_cfg
        self._axis_ref = None
        self._axis_data = None
        self._compu_meths = None
        self._rec_layouts = None
        self._fnc_outputs = None
        self._fnc_inputs = None
        self._fnc_locals = None
        self._fnc_char = None
        # generate the a2l string
        self._gen_a2l()

    def gen_a2l(self, filename):
        """Write a2l-data to file.

        Args:
            filename (str): Name of the generated a2l-file.
        """
        with open(filename, 'w', encoding="utf-8") as a2l:
            a2l.write(self._a2lstr)
            self.debug('Generated %s', filename)

    def _gen_a2l(self):
        """Generate an a2l-file based on the supplied data dictionary."""
        self._gen_compu_methods()
        # self.debug('_compu_meths')
        # self.debug(pp.pformat(self._compu_meths))
        self._find_axis_ref()
        # self.debug("_axis_ref")
        # self.debug(pp.pformat(self._axis_ref))
        self._find_axis_data()
        self._gen_record_layouts_data()
        # self.debug("_axis_data")
        # self.debug(pp.pformat(self._axis_data))
        # self.debug("_rec_layouts")
        # self.debug(pp.pformat(self._rec_layouts))
        self._check_axis_ref()

        output_meas = ''
        output_char = ''
        output_axis = ''

        self._fnc_outputs = []
        self._fnc_inputs = []
        self._fnc_locals = []
        self._fnc_char = []

        for var, data in self._var_dd['vars'].items():
            try:
                cvc_type = data['var']['cvc_type']
                if 'CVC_DISP' in cvc_type:
                    output_meas += self._gen_a2l_measurement_blk(var, data)
                    self._fnc_locals.append(var)
                elif 'CVC_CAL' in cvc_type:
                    self._fnc_char.append(var)
                    srch = re.search('_[rcxyXY]$', var)
                    if srch is None:
                        output_char += self._gen_a2l_characteristic_blk(var, data)
                    else:
                        output_axis += self._gen_a2l_axis_pts_blk(var, data)
                elif cvc_type == 'CVC_NVM':
                    output_meas += self._gen_a2l_measurement_blk(var, data)
                    self._fnc_locals.append(var)
                elif cvc_type == 'CVC_IN':
                    self._outputs = None
                    self._inputs = None
                    self._fnc_inputs.append(var)
                elif cvc_type == 'CVC_OUT':
                    self._fnc_outputs.append(var)
            except TypeError:
                self.warning("Warning: %s has no A2l-data", var)
            except Exception as e:
                self.critical("Unexpected error: %s", sys.exc_info()[0])
                raise e
        # generate COMPU_METHS
        output_compu_m = ''
        for k in self._compu_meths:
            output_compu_m += self._gen_a2l_compu_metod_blk(k)

        # generate FUNCTIONS
        output_funcs = self._gen_a2l_function_blk()

        # generate RECORD_LAYOUTS
        output_recl = ''
        for k in self._rec_layouts:
            output_recl += self._gen_a2l_rec_layout_blk(k)

        output = output_char + output_axis + output_meas + \
            output_compu_m + output_funcs + output_recl
        # self.debug(pp.pformat(self._var_dd))
        # self.debug('Output:')
        # self.debug(output)
        self._a2lstr = output

    def _find_axis_data(self):
        """Parse all variables and identify axis points.

        TODO: Change this function to check for names with _r | _c
              suffixes
        """
        self._axis_data = {}
        variable_names = self._var_dd['vars'].keys()
        for name in variable_names:
            x_nm = y_nm = None
            if name + '_x' in variable_names:
                x_nm = name + '_x'
            if name + '_y' in variable_names:
                y_nm = name + '_x'
            if x_nm is not None or y_nm is not None:
                self._axis_data[name] = (x_nm, y_nm)

    def _find_axis_ref(self):
        """Parse all variables and identify which are defined as axis points."""
        self._axis_ref = {}

        for var, data in self._var_dd['vars'].items():
            if data.get('a2l_data') is not None:
                x_axis = data['a2l_data'].get('x_axis')
                y_axis = data['a2l_data'].get('y_axis')
                if x_axis is not None:
                    if x_axis in self._axis_ref:
                        self._axis_ref[x_axis]['used_in'].append((var, 'x'))
                    else:
                        self._axis_ref[x_axis] = {'used_in': [(var, 'x')]}
                if y_axis is not None:
                    if y_axis in self._axis_ref:
                        self._axis_ref[y_axis]['used_in'].append((var, 'y'))
                    else:
                        self._axis_ref[y_axis] = {'used_in': [(var, 'y')]}

    @classmethod
    def _get_a2d_minmax(cls, a2d, ctype=None):
        """Get min max limits from a2l data.

        Gives max limits if min/max limits are undefined.
        """
        typelim = a2l_range(ctype)
        minlim = a2d.get('min')
        if minlim is None or minlim == '-':
            minlim = typelim[0]
        maxlim = a2d.get('max')
        if maxlim is None or maxlim == '-':
            maxlim = typelim[1]
        return minlim, maxlim

    def _check_axis_ref(self):
        """Check that the axis definitions are defined in the code."""
        undef_axis = [ax for ax in self._axis_ref
                      if ax not in self._var_dd['vars']]
        if undef_axis:
            self.warning(f'Undefined axis {pformat(undef_axis)}')

    def _gen_compu_methods(self):
        """Generate COMPU_METHOD data, and add it into the var_data_dict."""
        self._compu_meths = {}
        for var, data in self._var_dd['vars'].items():
            a2d = data.get('a2l_data')
            if a2d is not None:

                lsb = self._calc_lsb(a2d['lsb'])
                offset_str = str(a2d['offset'])
                is_offset_num = bool(re.match('[0-9]', offset_str))
                if is_offset_num:
                    offset = float(offset_str)
                else:
                    offset = 0
                key = (lsb, offset, a2d['unit'])
                self._var_dd['vars'][var]['compu_meth'] = key
                name = self._compu_key_2_name(key)
                if key in self._compu_meths:
                    self._compu_meths[key]['vars'].append(var)
                else:
                    self._compu_meths[key] = {'name': name,
                                              'vars': [var],
                                              'coeffs': self._get_coefs_str(lsb,
                                                                            offset)}

    def _compu_key_2_name(self, key):
        """Generate a COMPU_METHOD name from the keys in the name.

        Args:
            key (tuple): a list with compumethod keys (lsb, offset, unit)
        """
        conversion_list = [(r'[\./]', '_'), ('%', 'percent'),
                           ('-', 'None'), (r'\W', '_')]
        name = f"{self._var_dd['function']}_{key[0]}_{key[1]}_{key[2]}"
        for frm, to_ in conversion_list:
            name = re.sub(frm, to_, name)
        return name

    @staticmethod
    def _array_to_a2l_string(array):
        """Convert c-style array definitions to A2L MATRIX_DIM style."""
        if not isinstance(array, list):
            array = [array]
        dims = [1, 1, 1]
        for i, res in enumerate(array):
            dims[i] = res
        return f"MATRIX_DIM {dims[0]} {dims[1]} {dims[2]}"

    @staticmethod
    def _get_coefs_str(lsb, offset):
        """Calculate the a2l-coeffs from the lsb and offs fields.

        The fields are defined in the a2l_data dictionary.
        """
        return f"COEFFS 0 1 {offset} 0 0 {lsb}"

    @staticmethod
    def _calc_lsb(lsb):
        """Convert 2^-2, style lsbs to numericals."""
        if isinstance(lsb, str):
            if lsb == '-':
                return 1
            shift = re.match(r'(\d+)\^([\-+0-9]+)', lsb)
            if shift is not None:
                lsb_num = pow(int(shift.group(1)), int(shift.group(2)))
            else:
                lsb_num = float(lsb)
            return lsb_num
        return lsb

    def _gen_record_layouts_data(self):
        """Generate record layouts."""
        self._rec_layouts = {}
        for var, data in self._var_dd['vars'].items():
            if data.get('a2l_data') is not None:
                a2l_unit = a2l_type(data['var']['type'])
                # if calibration data has a suffix of _x of _y it is a axis_pts
                srch = re.search('_[xyXY]$', var)
                if srch is not None:
                    name = a2l_unit + "_X_INCR_DIRECT"
                    self._rec_layouts[name] = f"AXIS_PTS_X 1 {a2l_unit} INDEX_INCR DIRECT"
                    data['rec_layout'] = name
                else:
                    name = a2l_type(data['var']['type']) + "_COL_DIRECT"
                    self._rec_layouts[name] = f"FNC_VALUES 1 {a2l_unit} COLUMN_DIR DIRECT"
                    data['rec_layout'] = name

    def _get_inpq_data(self, inp_quant):
        """Get the necessary InputQuantity parameters."""
        if inp_quant is not None:
            if inp_quant in self._var_dd['vars']:
                return inp_quant
        return 'NO_INPUT_QUANTITY'

    # Bosh template
    _meas_tmplt = Template("""
    /begin MEASUREMENT
        $Name /* Name */
        "$LongIdent" /* LongIdentifier */
        $Datatype   /* Datatype */
        $Conversion   /* Conversion */
        1   /* Resolution */
        0   /* Accuracy */
        $LowerLimit   /* LowerLimit */
        $UpperLimit   /* UpperLimit */
        $OptionalData
        ECU_ADDRESS 0x00000000
    /end MEASUREMENT
""")

    # Denso template
    _meas_tmplt_nvm = Template("""
    /begin MEASUREMENT
        $Name /* Name */
        "$LongIdent" /* LongIdentifier */
        $Datatype   /* Datatype */
        $Conversion   /* Conversion */
        1   /* Resolution */
        0   /* Accuracy */
        $LowerLimit   /* LowerLimit */
        $UpperLimit   /* UpperLimit */
        $OptionalData
    /end MEASUREMENT
""")

    def _gen_a2l_measurement_blk(self, var_name, data):
        """Generate an a2l MEASUREMENT block."""
        opt_data = 'READ_WRITE'
        a2d = data.get('a2l_data')
        if a2d is not None:
            c_type = data['var']['type']
            # if c_type == 'Bool':
            #     opt_data += '\n' + ' ' * 8 + "BIT_MASK 0x1"
            if a2d.get('bitmask') is not None:
                opt_data += '\n' + ' ' * 8 + "BIT_MASK %s" % a2d['bitmask']
            if data.get('array'):
                opt_data += '\n' + ' ' * 8 + \
                    self._array_to_a2l_string(data['array'])

            use_symbol_links = self._prj_cfg.get_code_generation_config(item='useA2lSymbolLinks')
            if a2d.get('symbol'):
                if use_symbol_links:
                    opt_data += '\n' + ' ' * 8 + 'SYMBOL_LINK "%s" %s' % (a2d['symbol'], a2d.get('symbol_offset'))
                    LOG.debug('This a2l is using SYMBOL_LINK for %s', opt_data)
                else:
                    var_name = a2d['symbol'] + '._' + var_name
                    LOG.debug('This a2l is not using SYMBOL_LINK for %s', var_name)

            dtype = a2l_type(c_type)
            minlim, maxlim = self._get_a2d_minmax(a2d, c_type)
            conv = self._compu_meths[data['compu_meth']]['name']

            if a2d.get('symbol') and use_symbol_links:
                res = self._meas_tmplt_nvm.substitute(Name=var_name,
                                                      LongIdent=a2d['description'].replace('"', '\\"'),
                                                      Datatype=dtype,
                                                      Conversion=conv,
                                                      LowerLimit=minlim,
                                                      UpperLimit=maxlim,
                                                      OptionalData=opt_data)
            else:
                res = self._meas_tmplt.substitute(Name=var_name,
                                                  LongIdent=a2d['description'].replace('"', '\\"'),
                                                  Datatype=dtype,
                                                  Conversion=conv,
                                                  LowerLimit=minlim,
                                                  UpperLimit=maxlim,
                                                  OptionalData=opt_data)
            return res
        return None

    _char_tmplt = Template("""
    /begin CHARACTERISTIC
        $Name /* Name */
        "$LongIdent" /* LongIdentifier */
        $Type   /* Datatype */
        0x00000000    /* address: $Name */
        $Deposit   /* Deposit */
        0   /* MaxDiff */
        $Conversion   /* Conversion */
        $LowerLimit   /* LowerLimit */
        $UpperLimit   /* UpperLimit */$OptionalData
    /end CHARACTERISTIC
""")

    def _gen_a2l_characteristic_blk(self, var, data):
        """Generate an a2l CHARACTERISTIC block."""
        opt_data = ''
        a2d = data.get('a2l_data')
        type_ = 'WRONG_TYPE'
        if a2d is not None:
            arr = data.get('array')
            if arr is not None:
                arr_dim = len(arr)
            else:
                arr_dim = 0
            # Check is axis_pts are defined for the axis, if not make the
            # type a VAL_BLK with matrix dimension, otherwise set
            # a CURVE or MAP type

            # If arr_dim is 0 the CHARACTERISTIC is a value
            if arr_dim == 0:
                type_ = 'VALUE'
            elif arr_dim == 1:
                x_axis_name = var + '_x'
                # Check if axis variable is defined
                if x_axis_name in self._var_dd['vars'].keys():
                    type_ = 'CURVE'
                    opt_data += self._gen_a2l_axis_desc_blk(self._get_inpq_data(a2d.get('x_axis')),
                                                            x_axis_name)
                else:
                    type_ = 'VAL_BLK'
                    opt_data += self._array_to_a2l_string(data['array'])
            elif arr_dim == 2:
                x_axis_name = var + '_x'
                y_axis_name = var + '_y'
                # Check if axis variable is defined
                nbr_def_axis = 0
                if x_axis_name in self._var_dd['vars'].keys():
                    nbr_def_axis += 1
                if y_axis_name in self._var_dd['vars'].keys():
                    nbr_def_axis += 1
                if nbr_def_axis == 2:
                    type_ = 'MAP'
                    inpq_x = self._get_inpq_data(a2d['x_axis'])
                    opt_data += self._gen_a2l_axis_desc_blk(inpq_x, x_axis_name)
                    inpq_y = self._get_inpq_data(a2d['y_axis'])
                    opt_data += self._gen_a2l_axis_desc_blk(inpq_y, y_axis_name)
                elif nbr_def_axis == 0:
                    type_ = 'VAL_BLK'
                    opt_data += self._array_to_a2l_string(data['array'])
                else:
                    self.warning(
                        'MAP %s has only one AXIS_PTS defined, shall be none or two', var)

            minlim, maxlim = self._get_a2d_minmax(a2d)

            res = self._char_tmplt.substitute(Name=var,
                                              LongIdent=a2d['description'].replace('"', '\\"'),
                                              Type=type_,
                                              Deposit=data['rec_layout'],
                                              Conversion=self._compu_meths[data['compu_meth']]['name'],
                                              LowerLimit=minlim,
                                              UpperLimit=maxlim,
                                              OptionalData=opt_data)
            return res
        self.warning("%s has no A2L-data", var)
        return None
        # Types ASCII CURVE MAP VAL_BLK VALUE

    _axis_desc_tmplt = Template("""
        /begin AXIS_DESCR
            COM_AXIS    /* Attribute */
            $inp_quant   /* InputQuantity */
            $conv  /* Conversion */
            $maxaxispts  /* MaxAxisPoints */
            $minlim  /* LowerLimit */
            $maxlim   /* UpperLimit */
            AXIS_PTS_REF $axis_pts_ref
            DEPOSIT ABSOLUTE
        /end AXIS_DESCR""")

    def _gen_a2l_axis_desc_blk(self, inp_quant, axis_pts_ref):
        """Generate an a2l AXIS_DESCR block.

        TODO: Check that the AXIS_PTS_REF blocks are defined
        """
        out = ''
        inp_quant_txt = self._get_inpq_data(inp_quant)
        axis_pts = self._var_dd['vars'][axis_pts_ref]
        conv = self._compu_meths[axis_pts['compu_meth']]['name']
        max_axis_pts = axis_pts['array'][0]
        min_lim, max_lim = self._get_a2d_minmax(axis_pts['a2l_data'])
        out += self._axis_desc_tmplt.substitute(inp_quant=inp_quant_txt,
                                                conv=conv,
                                                maxaxispts=max_axis_pts,
                                                minlim=min_lim,
                                                maxlim=max_lim,
                                                axis_pts_ref=axis_pts_ref)
        return out

    _compu_meth_tmplt = Template("""
    /begin COMPU_METHOD
        $name   /* Name */
        "$longident"    /* LongIdentifier */
        RAT_FUNC    /* ConversionType */
        "$format"   /* Format */
        "$unit" /* Unit */
        $coeffs
    /end COMPU_METHOD
""")

    def _gen_a2l_compu_metod_blk(self, key):
        """Generate an a2l COMPU_METHOD block."""
        cmeth = self._compu_meths[key]
        name = self._compu_key_2_name(key)
        out = self._compu_meth_tmplt.substitute(name=name,
                                                longident='',
                                                format='%11.3',
                                                unit=key[2],
                                                coeffs=cmeth['coeffs'])
        return out

    _axis_tmplt = Template("""
    /begin AXIS_PTS
        $name   /* Name */
        "$longident"   /* LongIdentifier */
        0x00000000
        NO_INPUT_QUANTITY   /* InputQuantity */
        $deposit  /* Deposit */
        0   /* MaxDiff */
        $convert  /* Conversion */
        $max_ax_pts  /* MaxAxisPoints */
        $minlim   /* LowerLimit */
        $maxlim   /* UpperLimit */
        DEPOSIT ABSOLUTE
    /end AXIS_PTS
""")

    def _gen_a2l_axis_pts_blk(self, var, data):
        """Generate an a2l AXIS_PTS block."""
        deposit = data['rec_layout']
        conv = self._compu_meths[data['compu_meth']]['name']
        max_axis_pts = data['array'][0]
        min_lim, max_lim = self._get_a2d_minmax(data['a2l_data'])
        out = self._axis_tmplt.substitute(name=var,
                                          longident=data['a2l_data']['description'],
                                          deposit=deposit,
                                          convert=conv,
                                          max_ax_pts=max_axis_pts,
                                          minlim=min_lim,
                                          maxlim=max_lim)
        return out

    _rec_layout_tmplt = Template("""
    /begin RECORD_LAYOUT
        $name /* Name */
        $string
    /end RECORD_LAYOUT
""")

    def _gen_a2l_rec_layout_blk(self, key):
        """Generate an a2l AXIS_PTS block."""
        string = self._rec_layouts[key]
        out = self._rec_layout_tmplt.substitute(name=key,
                                                string=string)
        return out

    def _gen_a2l_function_blk(self):
        """Generate an a2l FUNCTION block."""
        out = '\n    /begin FUNCTION\n'
        out += f'        {self._var_dd["function"]} /* Name */\n'
        out += '        ""  /* LongIdentifier */\n'
        if self._fnc_char:
            out += '        /begin DEF_CHARACTERISTIC\n'
            for idf in self._fnc_char:
                out += f'            {idf} /* Identifier */\n'
            out += '        /end DEF_CHARACTERISTIC\n'
        if self._fnc_inputs:
            out += '        /begin IN_MEASUREMENT\n'
            for idf in self._fnc_inputs:
                out += f'            {idf} /* Identifier */\n'
            out += '        /end IN_MEASUREMENT\n'
        if self._fnc_locals:
            out += '        /begin LOC_MEASUREMENT\n'
            for idf in self._fnc_locals:
                out += f'            {idf} /* Identifier */\n'
            out += '        /end LOC_MEASUREMENT\n'
        if self._fnc_outputs:
            out += '        /begin OUT_MEASUREMENT\n'
            for idf in self._fnc_outputs:
                out += f'            {idf} /* Identifier */\n'
            out += '        /end OUT_MEASUREMENT\n'
        out += '    /end FUNCTION\n'
        return out
