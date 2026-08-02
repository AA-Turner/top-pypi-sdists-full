# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing classes for generation of scheduling call points."""
from os.path import join as pjoin
from os.path import split as psplit

import powertrain_build.build_defs as build_defs
from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.unit_configs import UnitConfigs


class SchedFuncs(ProblemLogger):
    """Generate scheduling functions for all unit initialisation and unit scheduling functions.

    Generates VcExtINI.c containing one function, VcExtINI, that calls all included units' initialisation
    (RESTART) functions.

    Generates one VcExt*.c file per configured scheduling raster containing one function collecting
    all unit scheduling functions for the specified time-raster.

    TODO: Add the debug functions
    """

    # Not included in VcExtINI.c and VcUnitTsDefines.h.
    RESTART_FNC_EXCLUDE = ('VcDebug', 'VcDebugOutput', 'VcDebugSafe', 'VcDebugOutputSafe')

    def __init__(self, build_proj_cfg, unit_cfg, dbg_dict):
        """Constructor.

        Args:
            build_proj_cfg (BuildProjConfig): project configuration.
            unit_cfg (UnitConfigs): Class holding all unit interfaces.
            dbg_dict (dict): Dictionary containing debug information, keys in RESTART_FNC_EXCLUDE.
        """
        super().__init__()

        if isinstance(build_proj_cfg, BuildProjConfig) and isinstance(unit_cfg, UnitConfigs):
            self._prj_cfg = build_proj_cfg
            self._unit_cfg = unit_cfg
            self._dbg_dict = dbg_dict
        else:
            err = (
                'Input arguments should be an instance of:'
                f'BuildProjConfig, not {type(build_proj_cfg)}'
                f'AND/OR UnitConfigs, not {type(unit_cfg)}'
            )
            raise TypeError(err)

    def generate_sched_c_fncs(self, generate_rte_checkpoint_calls):
        """Generate a c-files.

        One per scheduling raster and
        one for the running the Init functions

        TODO: Do the suppliers need a header per scheduling function?

        Args:
            generate_rte_checkpoint_calls (bool): Generate RTE function checkpoint calls.
        """
        dst_dir = self._prj_cfg.get_src_code_dst_dir()
        unit_raster_cfg = self._prj_cfg.get_units_raster_cfg()
        per_unit_cfg = self._unit_cfg.get_per_unit_cfg()
        prefix = self._prj_cfg.get_scheduler_prefix()
        unit_counter = 1
        rte_checkpoint_id_size = self._prj_cfg.get_code_generation_config("rteCheckpointIdSize")
        if rte_checkpoint_id_size is None:
            if generate_rte_checkpoint_calls:
                self.warning("RTE checkpoint ID size not set, assuming size is the same as the number of units.")
            rte_checkpoint_id_size = 0
            for units_in_raster in unit_raster_cfg['Rasters'].values():
                rte_checkpoint_id_size += len(units_in_raster)
        include_name = self._prj_cfg.get_composition_config("softwareComponentName")
        function_name = self._prj_cfg.get_composition_config("compositionName")
        if function_name is None:
            function_name = include_name

        init_ext_def_s = ""
        init_call_s = f'#include "{build_defs.CVC_CODE_START}"\n\n'
        init_call_s += f'void {prefix}VcExtINI(void)\n{{\n'
        for raster in unit_raster_cfg['SampleTimes']:
            if raster == "init":
                for unit in unit_raster_cfg['Rasters'][raster]:
                    if unit not in SchedFuncs.RESTART_FNC_EXCLUDE and 'code_generator' in per_unit_cfg[unit]:
                        code_generator = per_unit_cfg[unit]['code_generator']
                    else:
                        code_generator = 'target_link'

                    unit_name = unit.rsplit('__', 1)[0]
                    if code_generator == 'embedded_coder':
                        init_ext_def_s += f'extern void {unit_name}_initialize(void);\n'
                    else:
                        init_ext_def_s += f'extern void RESTART_{unit_name}(void);\n'

                    if unit_name not in SchedFuncs.RESTART_FNC_EXCLUDE:
                        if code_generator == 'embedded_coder':
                            init_call_s += f'  {unit_name}_initialize();\n'
                        else:
                            init_call_s += f'  RESTART_{unit_name}();\n'
            else:
                includes = ""
                rteCheckpointEntityName = self._prj_cfg.get_code_generation_config(
                    "customRteCheckpointEntityName"
                ).format(raster=raster)
                if generate_rte_checkpoint_calls:
                    includes += f'#include "Rte_{include_name}.h"\n'
                if includes:
                    includes += '\n'
                ext_def_str = ""
                call_str = f'#include "{build_defs.CVC_CODE_START}"\n'
                call_str += f'void {prefix}{raster}(void)\n{{\n'
                for unit in unit_raster_cfg['Rasters'][raster]:
                    if unit_counter > rte_checkpoint_id_size:
                        self.critical(
                            'RTE checkpoint ID size %d is smaller than the number of units.', rte_checkpoint_id_size
                        )
                    if unit not in SchedFuncs.RESTART_FNC_EXCLUDE and 'code_generator' in per_unit_cfg[unit]:
                        code_generator = per_unit_cfg[unit]['code_generator']
                    else:
                        code_generator = 'target_link'

                    unit_name = unit.rsplit('__', 1)[0]
                    if code_generator == 'embedded_coder':
                        if unit_name not in SchedFuncs.RESTART_FNC_EXCLUDE:
                            init_ext_def_s += f'extern void {unit_name}_initialize(void);\n'
                            init_call_s += f'  {unit_name}_initialize();\n'
                            ext_def_str += f'extern void {unit_name}_step(void);\n'
                            call_str += f'  {unit_name}_step();\n'
                        elif self._dbg_dict[unit_name]:
                            ext_def_str += f'extern void {unit_name}_step(void);\n'
                            call_str += f'  {unit_name}_step();\n'
                    else:
                        if generate_rte_checkpoint_calls:
                            call_str += (
                                '  (void)Rte_Call_alive_WdgMSupervisedEntity_'
                                f'{rteCheckpointEntityName}({unit_counter + 1}U);\n'  # Function IDs start at 2
                            )
                        if unit_name not in SchedFuncs.RESTART_FNC_EXCLUDE:
                            init_ext_def_s += f'extern void RESTART_{unit_name}(void);\n'
                            init_call_s += f'  RESTART_{unit_name}();\n'
                            ext_def_str += f'extern void {unit_name}(void);\n'
                            call_str += f'  {unit_name}();\n'
                        elif self._dbg_dict[unit_name]:
                            ext_def_str += f'extern void {unit_name}(void);\n'
                            call_str += f'  {unit_name}();\n'
                    unit_counter += 1
                if generate_rte_checkpoint_calls:
                    # Also call remaining dummy IDs
                    for i in range(unit_counter, rte_checkpoint_id_size + 1):
                        call_str += (
                            '  (void)Rte_Call_alive_WdgMSupervisedEntity_'
                            f'{rteCheckpointEntityName}({i + 1}U);\n'  # Function IDs start at 2 (same as above)
                        )
                ext_def_str += '\n'
                call_str += '}\n'
                call_str += f'#include "{build_defs.CVC_CODE_END}"\n\n'

                file_name = pjoin(dst_dir, f'{raster}.c')
                with open(file_name, 'w', encoding="utf-8") as fhndl:
                    fhndl.write(includes)
                    fhndl.write(ext_def_str)
                    fhndl.write(call_str)
                    self.info(f'generated {file_name}')
                file_name = pjoin(dst_dir, f'{raster}.h')
                with open(file_name, 'w', encoding="utf-8") as f_h:
                    f_h.write(f'#ifndef {raster.upper()}_H\n')
                    f_h.write(f'#define {raster.upper()}_H\n\n')
                    f_h.write(f'void {prefix}{raster}(void);\n\n')
                    f_h.write(f'#endif //{raster.upper()}_H\n')
        init_ext_def_s += '\n'
        init_call_s += '}\n\n'
        init_call_s += f'#include "{build_defs.CVC_CODE_END}"\n\n'
        file_name = pjoin(dst_dir, 'VcExtINI.c')
        with open(file_name, 'w', encoding="utf-8") as fhndl:
            fhndl.write(init_ext_def_s)
            fhndl.write(init_call_s)
            self.info('generated %s', file_name)

        file_name = pjoin(dst_dir, 'VcExtINI.h')
        with open(file_name, 'w', encoding="utf-8") as f_h:
            f_h.write('#ifndef VCEXTINI_H\n')
            f_h.write('#define VCEXTINI_H\n')
            f_h.write(f'void {prefix}VcExtINI(void);\n')
            f_h.write('#endif\n')

    def generate_ts_defines(self, file_name):
        """Generate the ts defines.

        Generates defines needed for all units, and
        writes it to a file with the supplied filename.

        Args:
            file_name (str): ts header file name
        """
        with open(file_name, 'w', encoding="utf-8") as fhndl:
            fhndl.write('/* Autogenerated by build system */\n')
            def_name = psplit(file_name)[1].replace('.', '_').upper()
            fhndl.write(f'#ifndef {def_name}\n')
            fhndl.write(f'#define {def_name}\n')
            unit_raster_cfg = self._prj_cfg.get_units_raster_cfg()
            for raster in unit_raster_cfg['SampleTimes']:
                fhndl.write(f'\n/**** raster {raster} *****/\n\n')
                for unit in unit_raster_cfg['Rasters'][raster]:
                    if unit not in SchedFuncs.RESTART_FNC_EXCLUDE:
                        t_sample = unit_raster_cfg['SampleTimes'][raster]
                        fhndl.write(f'#define ts_{unit} ((Float32) {t_sample}F)\n')
            fhndl.write(f'#endif /* {def_name} */\n')
            self.info('generated %s', file_name)
