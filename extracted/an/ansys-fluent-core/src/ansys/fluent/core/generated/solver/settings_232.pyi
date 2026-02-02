#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _NonCreatableNamedObjectMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
    _FlStringConstant,
)

from typing import Any, Final

class single_precision_coordinates(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class binary_legacy_files(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cff_files(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convert_hanging_nodes_during_read(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class async_optimize(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class write_pdat(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class confirm_overwrite(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class case_frequency(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class data_frequency(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class root_name(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class retain_most_recent_files(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_files(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class file_suffix_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class file_decimal_digit(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class append_file_name_with(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    file_suffix_type: file_suffix_type
    file_decimal_digit: file_decimal_digit
    return_type: str

class frequency_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class save_frequency(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class save_data_file_every(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    frequency_type: frequency_type
    save_frequency: save_frequency
    return_type: str

class auto_save(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    case_frequency: case_frequency
    data_frequency: data_frequency
    root_name: root_name
    retain_most_recent_files: retain_most_recent_files
    max_files: max_files
    append_file_name_with: append_file_name_with
    save_data_file_every: save_data_file_every
    return_type: str

class enable_auto_creation_of_scp_file(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sc_def_file_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    enable_auto_creation_of_scp_file: enable_auto_creation_of_scp_file
    def write_sc_file(self, file_name: str, overwrite: bool):
        """
        Write a Fluent Input File for System Coupling.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def set_cgns_export_filetype(self, set_filetype: bool):
        """
        Select HDF5 or ADF as file format for CGNS.
        
        Parameters
        ----------
            set_filetype : bool
                'set_filetype' child.
        """
    return_type: str

class export(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    sc_def_file_settings: sc_def_file_settings
    settings: settings
    def abaqus(self, name: str, surface_name_list: list[str], structural_analysis: bool, write_loads: bool, loads: list[str]):
        """
        Write an ABAQUS file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : List
                'surface_name_list' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : List
                'loads' child.
        """
    def mechanical_apdl(self, name: str, thread_name_list: list[str]):
        """
        Write an Mechanical APDL file.
        
        Parameters
        ----------
            name : str
                'name' child.
            thread_name_list : List
                'thread_name_list' child.
        """
    def mechanical_apdl_input(self, name: str, surface_name_list: list[str], structural_analysis: bool, write_loads: bool, loads: list[str]):
        """
        Write an Mechanical APDL Input file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : List
                'surface_name_list' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : List
                'loads' child.
        """
    def ascii(self, name: str, surface_name_list: list[str], delimiter: str, cell_func_domain: list[str], location: str):
        """
        Write an ASCII file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : List
                List of surfaces to export.
            delimiter : str
                'delimiter' child.
            cell_func_domain : List
                'cell_func_domain' child.
            location : str
                'location' child.
        """
    def avs(self, name: str, cell_func_domain_export: list[str]):
        """
        Write an AVS UCD file.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def ensight(self, name: str, cell_func_domain_export: list[str]):
        """
        Write EnSight 6 geometry, velocity, and scalar files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def ensight_gold(self, name: str, cell_func_domain_export: list[str]):
        """
        Write EnSight Gold geometry, velocity, and scalar files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def fieldview(self, name: str, cell_func_domain_export: list[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def fieldview_data(self, name: str, cell_func_domain_export: list[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def gambit(self, name: str, cell_func_domain_export: list[str]):
        """
        Write a Gambit neutral file.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def cgns(self, name: str, scope: str, cell_zones: list[str], surfaces: list[str], cell_centered: bool, format_class: str, cgns_scalar: list[str]):
        """
        Write a CGNS file.
        
        Parameters
        ----------
            name : str
                'name' child.
            scope : str
                'scope' child.
            cell_zones : List
                'cell_zones' child.
            surfaces : List
                'surfaces' child.
            cell_centered : bool
                'cell_centered' child.
            format_class : str
                'format_class' child.
            cgns_scalar : List
                'cgns_scalar' child.
        """
    def custom_heat_flux(self, name: str, wall_function: bool, surface_name_list: list[str]):
        """
        Write a generic file for heat transfer.
        
        Parameters
        ----------
            name : str
                'name' child.
            wall_function : bool
                'wall_function' child.
            surface_name_list : List
                'surface_name_list' child.
        """
    def dx(self, name: str, surfaces: list[str], techplot_scalars: list[str]):
        """
        Write an IBM Data Explorer format file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                'surfaces' child.
            techplot_scalars : List
                'techplot_scalars' child.
        """
    def ensight_gold_parallel_surfaces(self, name: str, binary_format: bool, surfaces: list[str], cell_centered: bool, cell_function: list[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            name : str
                'name' child.
            binary_format : bool
                'binary_format' child.
            surfaces : List
                'surfaces' child.
            cell_centered : bool
                'cell_centered' child.
            cell_function : List
                'cell_function' child.
        """
    def ensight_gold_parallel_volume(self, name: str, binary_format: bool, cellzones: list[str], cell_centered: bool, cell_function: list[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            name : str
                'name' child.
            binary_format : bool
                'binary_format' child.
            cellzones : List
                'cellzones' child.
            cell_centered : bool
                'cell_centered' child.
            cell_function : List
                'cell_function' child.
        """
    def icemcfd_for_icepak(self, name: str):
        """
        Write a binary ICEMCFD domain file.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    def fast_mesh(self, name: str):
        """
        Write a FAST/Plot3D unstructured mesh file.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    def fast_solution(self, name: str):
        """
        Write a FAST/Plot3D unstructured solution file.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    def fast_velocity(self, name: str):
        """
        Write a FAST/Plot3D unstructured vector function file.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    def taitherm(self, name: str, surface_name_list: list[str], wall_function: bool, htc_on_walls: bool):
        """
        Write a TAITherm file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : List
                'surface_name_list' child.
            wall_function : bool
                'wall_function' child.
            htc_on_walls : bool
                'htc_on_walls' child.
        """
    def fieldview_unstruct(self, name: str, surfaces: list[str], cellzones: list[str], cell_func_domain: list[str]):
        """
        Write a Fieldview unstructured combined file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                List of surfaces to export.
            cellzones : List
                List of cell zones to export.
            cell_func_domain : List
                'cell_func_domain' child.
        """
    def fieldview_unstruct_mesh(self, name: str, surfaces: list[str], cellzones: list[str], cell_func_domain: list[str]):
        """
        Write a Fieldview unstructured mesh only file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                List of surfaces to export.
            cellzones : List
                List of cell zones to export.
            cell_func_domain : List
                'cell_func_domain' child.
        """
    def fieldview_unstruct_data(self, name: str, surfaces: list[str], cellzones: list[str], cell_func_domain: list[str]):
        """
        Write a Fieldview unstructured results only file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                List of surfaces to export.
            cellzones : List
                List of cell zones to export.
            cell_func_domain : List
                'cell_func_domain' child.
        """
    def fieldview_unstruct_surfaces(self, options: str, name: str, surfaces: list[str], cell_func_domain: list[str]):
        """
        Write a Fieldview unstructured surface mesh, data.
        
        Parameters
        ----------
            options : str
                'options' child.
            name : str
                'name' child.
            surfaces : List
                'surfaces' child.
            cell_func_domain : List
                'cell_func_domain' child.
        """
    def ideas(self, name: str, surfaces: list[str], structural_analysis: bool, write_loads: bool, loads: list[str], cell_func_domain_export: list[str]):
        """
        Write an IDEAS universal file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                List of surfaces to export.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : List
                'loads' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def nastran(self, name: str, bndry_threads: list[str], surfaces: list[str], structural_analysis: bool, write_loads: bool, loads: list[str], cell_func_domain_export: list[str]):
        """
        Write a NASTRAN file.
        
        Parameters
        ----------
            name : str
                'name' child.
            bndry_threads : List
                'bndry_threads' child.
            surfaces : List
                'surfaces' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : List
                'loads' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def patran_neutral(self, name: str, surfaces: list[str], structural_analysis: bool, write_loads: bool, loads: list[str], cell_func_domain_export: list[str]):
        """
        Write a PATRAN neutral file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                'surfaces' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : List
                'loads' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def patran_nodal(self, name: str, surfaces: list[str], cell_func_domain_export: list[str]):
        """
        Write a PATRAN nodal results file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                'surfaces' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    def tecplot(self, name: str, surfaces: list[str], cell_func_domain_export: list[str]):
        """
        Write a Tecplot+3DV format file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : List
                'surfaces' child.
            cell_func_domain_export : List
                'cell_func_domain_export' child.
        """
    return_type: str

class create_zones_from_ccl(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class import_(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    create_zones_from_ccl: create_zones_from_ccl
    def read(self, file_type: str, file_name: str):
        """
        'read' command.
        """
    def chemkin_report_each_line(self, report_each_line: bool):
        """
        'chemkin_report_each_line' command.
        """
    def import_fmu(self, file_name: str):
        """
        Import a FMU file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    return_type: str

class parametric_project(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def new(self, project_filename: str):
        """
        Create New Project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        """
    def open(self, project_filename: str, load_case: bool):
        """
        Open project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
            load_case : bool
                'load_case' child.
        """
    def save(self):
        """
        Save Project.
        """
    def save_as(self, project_filename: str):
        """
        Save As Project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        """
    def save_as_copy(self, project_filename: str, convert_to_managed: bool):
        """
        Save As Project.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
            convert_to_managed : bool
                'convert_to_managed' child.
        """
    def archive(self, archive_name: str):
        """
        Archive Project.
        
        Parameters
        ----------
            archive_name : str
                'archive_name' child.
        """
    return_type: str

class io_mode(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class compression_level(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class single_precision_data(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cffio_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    io_mode: io_mode
    compression_level: compression_level
    single_precision_data: single_precision_data
    return_type: str

class file(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    single_precision_coordinates: single_precision_coordinates
    binary_legacy_files: binary_legacy_files
    cff_files: cff_files
    convert_hanging_nodes_during_read: convert_hanging_nodes_during_read
    async_optimize: async_optimize
    write_pdat: write_pdat
    confirm_overwrite: confirm_overwrite
    auto_save: auto_save
    export: export
    import_: import_
    parametric_project: parametric_project
    cffio_options: cffio_options
    def define_macro(self, filename: str):
        """
        Save input to a named macro.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        """
    def execute_macro(self, macro_filename: str):
        """
        Run a previously defined macro.
        
        Parameters
        ----------
            macro_filename : str
                'macro_filename' child.
        """
    def read_macros(self, file_name: str):
        """
        Read macro definitions from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read' command.
        """
    def read_case(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case' command.
        """
    def read_case_data(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case_data' command.
        """
    def read_case_setting(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case_setting' command.
        """
    def read_data(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_data' command.
        """
    def read_mesh(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_mesh' command.
        """
    def read_journal(self, file_name_list: list[str]):
        """
        Read a journal file.
        
        Parameters
        ----------
            file_name_list : List
                'file_name_list' child.
        """
    def start_journal(self, file_name: str):
        """
        Start recording all input in a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def stop_journal(self):
        """
        Stop recording input and close the journal file.
        """
    def replace_mesh(self, file_name: str):
        """
        'replace_mesh' command.
        """
    def write(self, file_type: str, file_name: str):
        """
        'write' command.
        """
    def read_settings(self, file_name: str):
        """
        Read and set boundary conditions from specified file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read_field_functions(self, file_name: str):
        """
        Read custom field-function definitions from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read_injections(self, file_name: str):
        """
        Read all DPM injections from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read_profile(self, file_name: str):
        """
        Read boundary profile data (\\*.prof, \\*.csv). Default is \\*.prof.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read_pdf(self, file_name: str):
        """
        Read a PDF file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read_isat_table(self, file_name: str):
        """
        Read an ISAT table.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def show_configuration(self):
        """
        Display current release and version information.
        """
    def stop_macro(self):
        """
        Stop recording input to a macro.
        """
    def start_transcript(self, file_name: str):
        """
        Start recording input and output in a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def stop_transcript(self):
        """
        Stop recording input and output and close the transcript file.
        """
    def data_file_options(self, reset_defined_derived_quantities: bool, derived_quantities: list[str]):
        """
        Set derived quantities to be written in data file.
        
        Parameters
        ----------
            reset_defined_derived_quantities : bool
                'reset_defined_derived_quantities' child.
            derived_quantities : List
                'derived_quantities' child.
        """
    return_type: str

class refinement_criteria(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsening_criteria(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class manual_refinement_criteria(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class manual_coarsening_criteria(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class adaption_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class prismatic_boundary_zones(StringList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cell_zones_1(StringList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_adaption_frequency(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class encapsulate_children(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_refinement_level(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minimum_edge_length(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minimum_cell_quality(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_cell_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class additional_refinement_layers(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class prismatic_adaption(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class prismatic_split_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class overset_adapt_dead_cells(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    adaption_method: adaption_method
    prismatic_boundary_zones: prismatic_boundary_zones
    cell_zones: cell_zones_1
    dynamic_adaption_frequency: dynamic_adaption_frequency
    verbosity: verbosity
    encapsulate_children: encapsulate_children
    maximum_refinement_level: maximum_refinement_level
    minimum_edge_length: minimum_edge_length
    minimum_cell_quality: minimum_cell_quality
    maximum_cell_count: maximum_cell_count
    additional_refinement_layers: additional_refinement_layers
    prismatic_adaption: prismatic_adaption
    prismatic_split_ratio: prismatic_split_ratio
    overset_adapt_dead_cells: overset_adapt_dead_cells
    def dynamic_adaption(self, enable: bool):
        """
        Adapt the mesh during solution.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
        """
    return_type: str

class profile(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def enable(self):
        """
        Enable adaption profiling.
        """
    def disable(self):
        """
        Disable adaption profiling.
        """
    def print(self):
        """
        Print adaption profiling results.
        """
    def clear(self):
        """
        Clear adaption profiling counters.
        """
    return_type: str

class free_hierarchy(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class growth_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class growth_ratio_refinement(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    growth_ratio: growth_ratio
    return_type: str

class type(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    growth_ratio_refinement: growth_ratio_refinement
    return_type: str

class layer_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_list(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multi_layer_refinement(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    type: type
    layer_count: layer_count
    boundary_list: boundary_list
    def refine_mesh(self):
        """
        Refine the mesh for multiple boundary layers.
        """
    return_type: str

class reconstruct_geometry(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geometry(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    reconstruct_geometry: reconstruct_geometry
    return_type: str

class adapt(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    refinement_criteria: refinement_criteria
    coarsening_criteria: coarsening_criteria
    manual_refinement_criteria: manual_refinement_criteria
    manual_coarsening_criteria: manual_coarsening_criteria
    set: set
    profile: profile
    free_hierarchy: free_hierarchy
    multi_layer_refinement: multi_layer_refinement
    geometry: geometry
    def adapt_mesh(self):
        """
        Adapt the mesh based on set refinement/coarsening criterion.
        """
    def display_adaption_cells(self):
        """
        Display cells marked for refinement/coarsening.
        """
    def list_adaption_cells(self):
        """
        List the number of cells marked for refinement/coarsening.
        """
    return_type: str

class coarsen(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class refine(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class swap(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class move(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class operations(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    coarsen: coarsen
    refine: refine
    swap: swap
    move: move
    return_type: str

class iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_zones(StringList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class indicator_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class single_scalar_fn(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multi_scalar_fn(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class indicator(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    indicator_type: indicator_type
    single_scalar_fn: single_scalar_fn
    multi_scalar_fn: multi_scalar_fn
    return_type: str

class target_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_cells(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class factor_of_cells(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class target(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    target_type: target_type
    number_of_cells: number_of_cells
    factor_of_cells: factor_of_cells
    return_type: str

class anisotropic_adaption(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    operations: operations
    iterations: iterations
    fixed_zones: fixed_zones
    indicator: indicator
    target: target
    def adapt_mesh(self):
        """
        Adapt the mesh based on specified anisotropic adaption setup.
        """
    return_type: str

class check_before_solve(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class check_verbosity(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enhanced_orthogonal_quality(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class matching_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class show_periodic_shadow_zones(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reorder(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def band_width(self):
        """
        Print cell bandwidth.
        """
    def reorder_domain(self):
        """
        Reorder cells and faces by reverse Cuthill-McKee.
        """
    def reorder_zones(self):
        """
        Reorder zones by partition, type, and id.
        """
    return_type: str

class allow_repair_at_boundaries(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class include_local_polyhedra_conversion_in_repair(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class repair_improve(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    allow_repair_at_boundaries: allow_repair_at_boundaries
    include_local_polyhedra_conversion_in_repair: include_local_polyhedra_conversion_in_repair
    def repair_poor_elements(self):
        """
        Report invalid and poor quality elements.
        """
    def improve_quality(self):
        """
        Tries to improve the mesh quality.
        """
    def repair(self):
        """
        Tries to repair mesh problems identified by mesh check.
        """
    def repair_face_handedness(self, repair: bool, disable_repair: bool):
        """
        Correct face handedness at left handed faces if possible.
        
        Parameters
        ----------
            repair : bool
                'repair' child.
            disable_repair : bool
                'disable_repair' child.
        """
    def repair_face_node_order(self):
        """
        Reverse order of face nodes if needed.
        """
    def repair_wall_distance(self, repair: bool):
        """
        Correct wall distance at very high aspect ratio hexahedral/polyhedral cells.
        
        Parameters
        ----------
            repair : bool
                'repair' child.
        """
    return_type: str

class surface_mesh(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def delete(self, surface: str):
        """
        Delete surface mesh.
        
        Parameters
        ----------
            surface : str
                'surface' child.
        """
    def display(self):
        """
        Display surface meshes.
        """
    def read(self, filename: str, unit: str):
        """
        Read surface meshes.
        
        Parameters
        ----------
            filename : str
                'filename' child.
            unit : str
                'unit' child.
        """
    return_type: str

class migrate_and_reorder(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class preserve_boundary_layer(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class preserve_interior_zones(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    migrate_and_reorder: migrate_and_reorder
    preserve_boundary_layer: preserve_boundary_layer
    preserve_interior_zones: preserve_interior_zones
    return_type: str

class polyhedra(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    options: options_1
    def convert_domain(self):
        """
        Convert entire domain to polyhedra cells.
        """
    def convert_hanging_nodes(self):
        """
        Convert cells with hanging nodes and faces to polyhedra.
        """
    def convert_hanging_node_zones(self):
        """
        Convert selected cell zones with hanging nodes and faces to polyhedra. 
        The selected cell zones cannot be connected to other zones.
        """
    def convert_skewed_cells(self, cell_thread_list: list[str], max_cell_skewness: float | str, convert_skewed_cells: bool):
        """
        'convert_skewed_cells' command.
        """
    return_type: str

class wall_distance_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mesh(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    adapt: adapt
    anisotropic_adaption: anisotropic_adaption
    check_before_solve: check_before_solve
    check_verbosity: check_verbosity
    enhanced_orthogonal_quality: enhanced_orthogonal_quality
    matching_tolerance: matching_tolerance
    show_periodic_shadow_zones: show_periodic_shadow_zones
    reorder: reorder
    repair_improve: repair_improve
    surface_mesh: surface_mesh
    polyhedra: polyhedra
    wall_distance_method: wall_distance_method
    def adjacency(self):
        """
        View and rename face zones adjacent to selected cell zones.
        """
    def check(self):
        """
        Perform various mesh consistency checks.
        """
    def memory_usage(self):
        """
        Report solver memory use.
        """
    def mesh_info(self, print_level: int):
        """
        Print zone information size.
        
        Parameters
        ----------
            print_level : int
                Print zone information size.
        """
    def quality(self):
        """
        Perform analysis of mesh quality.
        """
    def rotate(self, angle: float | str, origin: list[float | str], axis_components: list[float | str]):
        """
        Rotate the mesh.
        
        Parameters
        ----------
            angle : real
                'angle' child.
            origin : List
                'origin' child.
            axis_components : List
                'axis_components' child.
        """
    def scale(self, x_scale: float | str, y_scale: float | str, z_scale: float | str):
        """
        'scale' command.
        """
    def size_info(self):
        """
        Print mesh size.
        """
    def redistribute_boundary_layer(self, thread_id: int, growth_rate: float | str):
        """
        Enforce growth rate in boundary layer.
        
        Parameters
        ----------
            thread_id : int
                'thread_id' child.
            growth_rate : real
                'growth_rate' child.
        """
    def swap_mesh_faces(self):
        """
        Swap mesh faces.
        """
    def smooth_mesh(self, type_of_smoothing: str, number_of_iterations: int, relaxtion_factor: float | str, percentage_of_cells: float | str, skewness_threshold: float | str):
        """
        Smooth the mesh using quality-based, Laplace or skewness methods.
        
        Parameters
        ----------
            type_of_smoothing : str
                'type_of_smoothing' child.
            number_of_iterations : int
                'number_of_iterations' child.
            relaxtion_factor : real
                'relaxtion_factor' child.
            percentage_of_cells : real
                'percentage_of_cells' child.
            skewness_threshold : real
                'skewness_threshold' child.
        """
    def replace(self, name: str, zones: bool):
        """
        Replace mesh and interpolate data.
        
        Parameters
        ----------
            name : str
                'name' child.
            zones : bool
                'zones' child.
        """
    def translate(self, offset: list[float | str]):
        """
        Translate the mesh.
        
        Parameters
        ----------
            offset : List
                'offset' child.
        """
    return_type: str

class web_server(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    query_names: list[str]
    def start(self, session_name: str, port: int, port_span: int, job_service_url: str):
        """
        Start the web server.
        
        Parameters
        ----------
            session_name : str
                Name for the web server.
            port : int
                Listening port for the web server.
            port_span : int
                Number of ports to try starting from given 'port' for the web server.
            job_service_url : str
                Job service URL to register Fluent.
        """
    def stop(self):
        """
        Stop the web server.
        """
    def print_server_info(self):
        """
        Print the web server information.
        """
    def get_server_info(self):
        """
        Get the web server information.
        """
    return_type: str

class server(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    web_server: web_server
    return_type: str

class type_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class two_dim_space(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity_formulation(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solver(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    type: type_1
    two_dim_space: two_dim_space
    velocity_formulation: velocity_formulation
    time: time
    return_type: str

class adjust_solver_defaults_based_on_setup(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class components(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gravity_mrf_behavior(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gravity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_2
    components: components
    gravity_mrf_behavior: gravity_mrf_behavior
    return_type: str

class real_gas_state(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class operating_pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_pressure_location(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_pressure_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_3(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class value(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class operating_density(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    enable: enable_3
    method: method
    value: value
    def print(self):
        """
        Print operating density value.
        """
    return_type: str

class operating_temperature(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class operating_conditions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    gravity: gravity
    real_gas_state: real_gas_state
    operating_pressure: operating_pressure
    reference_pressure_location: reference_pressure_location
    reference_pressure_method: reference_pressure_method
    operating_density: operating_density
    operating_temperature: operating_temperature
    def used_ref_pressure_location(self):
        """
        See the actual coordinates of reference pressure used.
        """
    def use_inlet_temperature_for_operating_density(self, zone_name: str):
        """
        Use Inlet Temperature to calculate Opearating Density.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
        """
    return_type: str

class general(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    solver: solver
    adjust_solver_defaults_based_on_setup: adjust_solver_defaults_based_on_setup
    operating_conditions: operating_conditions
    return_type: str

class models_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vaporization_pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class non_condensable_gas(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class liquid_surface_tension(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bubble_number_density(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_phases(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_eulerian_discrete_phases(IntegerList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multiphase(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    models: models_1
    vaporization_pressure: vaporization_pressure
    non_condensable_gas: non_condensable_gas
    liquid_surface_tension: liquid_surface_tension
    bubble_number_density: bubble_number_density
    number_of_phases: number_of_phases
    number_of_eulerian_discrete_phases: number_of_eulerian_discrete_phases
    return_type: str

class enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscous_dissipation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_work(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kinetic_energy(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inlet_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class energy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled
    viscous_dissipation: viscous_dissipation
    pressure_work: pressure_work
    kinetic_energy: kinetic_energy
    inlet_diffusion: inlet_diffusion
    return_type: str

class model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscous_heating(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class low_pressure_boundary_slip(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class curvature_correction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class corner_flow_correction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class production_kato_launder(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_buoyancy_effects(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kw_buoyancy_effects(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_geko(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    viscous_heating: viscous_heating
    low_pressure_boundary_slip: low_pressure_boundary_slip
    curvature_correction: curvature_correction
    corner_flow_correction: corner_flow_correction
    production_kato_launder: production_kato_launder
    turb_buoyancy_effects: turb_buoyancy_effects
    kw_buoyancy_effects: kw_buoyancy_effects
    enable_geko: enable_geko
    return_type: str

class spalart_allmaras_production(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class k_epsilon_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class k_omega_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kw_low_re_correction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kw_shear_correction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_compressibility(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class k_omega_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    kw_low_re_correction: kw_low_re_correction
    kw_shear_correction: kw_shear_correction
    turb_compressibility: turb_compressibility
    return_type: str

class differential_viscosity_model(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class swirl_dominated_flow(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rng_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    differential_viscosity_model: differential_viscosity_model
    swirl_dominated_flow: swirl_dominated_flow
    return_type: str

class wall_treatment(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_gradient_effects(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thermal_effects(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enhanced_wall_treatment_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pressure_gradient_effects: pressure_gradient_effects
    thermal_effects: thermal_effects
    return_type: str

class wall_omega_treatment(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class near_wall_treatment(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    wall_treatment: wall_treatment
    user_defined: user_defined_1
    enhanced_wall_treatment_options: enhanced_wall_treatment_options
    wall_omega_treatment: wall_omega_treatment
    return_type: str

class reynolds_stress_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class subgrid_scale_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_stress(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_energy_flux(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_scalar_flux(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class subgrid_dynamic_fvar(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cvreman(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class csigma(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_model(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cw1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cw2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_model_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    dynamic_stress: dynamic_stress
    dynamic_energy_flux: dynamic_energy_flux
    dynamic_scalar_flux: dynamic_scalar_flux
    subgrid_dynamic_fvar: subgrid_dynamic_fvar
    cvreman: cvreman
    csigma: csigma
    wall_model: wall_model
    cw1: cw1
    cw2: cw2
    return_type: str

class solve_tke(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_echo(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reynolds_stress_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    solve_tke: solve_tke
    wall_echo: wall_echo
    return_type: str

class rans_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class all_len_modified(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class des_limiter_option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class des_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    all_len_modified: all_len_modified
    des_limiter_option: des_limiter_option
    return_type: str

class transition_module(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class f_length(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class re_theta_c(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class re_theta_t(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_transition(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    f_length: f_length
    re_theta_c: re_theta_c
    re_theta_t: re_theta_t
    return_type: str

class dispersion_force_in_momentum(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dispersion_in_relative_velocity(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multiphase_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    dispersion_force_in_momentum: dispersion_force_in_momentum
    dispersion_in_relative_velocity: dispersion_in_relative_velocity
    return_type: str

class turbulence_multiphase_models(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rsm_multiphase_models(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class subgrid_turbulence_contribution_aiad(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multiphase_turbulence(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    multiphase_options: multiphase_options
    turbulence_multiphase_models: turbulence_multiphase_models
    rsm_multiphase_models: rsm_multiphase_models
    subgrid_turbulence_contribution_aiad: subgrid_turbulence_contribution_aiad
    return_type: str

class low_re_ke(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class low_re_ke_index(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kato_launder_model(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_prod_limiter(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clip_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class production_limiter(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_prod_limiter: enable_prod_limiter
    clip_factor: clip_factor
    return_type: str

class kw_vorticity_based_production(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kw_add_sas(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kw_add_des(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_add_sbes_sdes(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sbes_sdes_hybrid_model_optn(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sbes_sdes_hybrid_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    sbes_sdes_hybrid_model_optn: sbes_sdes_hybrid_model_optn
    user_defined: user_defined_2
    return_type: str

class sbes_update_interval_k_omega(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sbes_sgs_option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sbes_les_subgrid_dynamic_fvar(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_turb_damping(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_damping_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulence_damping(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_turb_damping: enable_turb_damping
    turb_damping_factor: turb_damping_factor
    return_type: str

class rke_cmu_rotation_term(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_non_newtonian(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class non_newtonian_modification(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_pk_compressible(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thermal_p_function(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class restore_sst_v61(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulence_expert(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    low_re_ke: low_re_ke
    low_re_ke_index: low_re_ke_index
    kato_launder_model: kato_launder_model
    production_limiter: production_limiter
    kw_vorticity_based_production: kw_vorticity_based_production
    kw_add_sas: kw_add_sas
    kw_add_des: kw_add_des
    turb_add_sbes_sdes: turb_add_sbes_sdes
    sbes_sdes_hybrid_model: sbes_sdes_hybrid_model
    sbes_update_interval_k_omega: sbes_update_interval_k_omega
    sbes_sgs_option: sbes_sgs_option
    sbes_les_subgrid_dynamic_fvar: sbes_les_subgrid_dynamic_fvar
    turbulence_damping: turbulence_damping
    rke_cmu_rotation_term: rke_cmu_rotation_term
    turb_non_newtonian: turb_non_newtonian
    non_newtonian_modification: non_newtonian_modification
    turb_pk_compressible: turb_pk_compressible
    thermal_p_function: thermal_p_function
    restore_sst_v61: restore_sst_v61
    return_type: str

class wall_distance_free(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cjet(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class creal(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cnw_sub(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cjet_aux(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cbf_lam(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cbf_tur(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geko_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    wall_distance_free: wall_distance_free
    cjet: cjet
    creal: creal
    cnw_sub: cnw_sub
    cjet_aux: cjet_aux
    cbf_lam: cbf_lam
    cbf_tur: cbf_tur
    def geko_defaults(self):
        """
        Set GEKO options to default.
        """
    return_type: str

class crossflow_transition(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class critical_reynolds_number_correlation(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clambda_scale(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class capg_hightu(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cfpg_hightu(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class capg_lowtu(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cfpg_lowtu(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ctu_hightu(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ctu_lowtu(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rec_max(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rec_c1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rec_c2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cbubble_c1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cbubble_c2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rv1_switch(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class transition_model_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    crossflow_transition: crossflow_transition
    critical_reynolds_number_correlation: critical_reynolds_number_correlation
    clambda_scale: clambda_scale
    capg_hightu: capg_hightu
    cfpg_hightu: cfpg_hightu
    capg_lowtu: capg_lowtu
    cfpg_lowtu: cfpg_lowtu
    ctu_hightu: ctu_hightu
    ctu_lowtu: ctu_lowtu
    rec_max: rec_max
    rec_c1: rec_c1
    rec_c2: rec_c2
    cbubble_c1: cbubble_c1
    cbubble_c2: cbubble_c2
    rv1_switch: rv1_switch
    return_type: str

class enable_roughness_correlation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class roughness_correlation_fcn(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geometric_roughness_ht_val(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class transition_sst_option(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_roughness_correlation: enable_roughness_correlation
    roughness_correlation_fcn: roughness_correlation_fcn
    geometric_roughness_ht_val: geometric_roughness_ht_val
    return_type: str

class subgrid_scale_turb_visc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_visc_func_mf_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_visc_func_mf(NamedObject[turb_visc_func_mf_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: turb_visc_func_mf_child
    return_type: str

class turb_visc_func(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tke_prandtl(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tdr_prandtl(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sdr_prandtl(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class energy_prandtl(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_prandtl(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_schmidt(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    subgrid_scale_turb_visc: subgrid_scale_turb_visc
    turb_visc_func_mf: turb_visc_func_mf
    turb_visc_func: turb_visc_func
    tke_prandtl: tke_prandtl
    tdr_prandtl: tdr_prandtl
    sdr_prandtl: sdr_prandtl
    energy_prandtl: energy_prandtl
    wall_prandtl: wall_prandtl
    turbulent_schmidt: turbulent_schmidt
    return_type: str

class sa_enhanced_wall_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sa_damping(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscous(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    model: model
    options: options_2
    spalart_allmaras_production: spalart_allmaras_production
    k_epsilon_model: k_epsilon_model
    k_omega_model: k_omega_model
    k_omega_options: k_omega_options
    rng_options: rng_options
    near_wall_treatment: near_wall_treatment
    reynolds_stress_model: reynolds_stress_model
    subgrid_scale_model: subgrid_scale_model
    les_model_options: les_model_options
    reynolds_stress_options: reynolds_stress_options
    rans_model: rans_model
    des_options: des_options
    transition_module: transition_module
    user_defined_transition: user_defined_transition
    multiphase_turbulence: multiphase_turbulence
    turbulence_expert: turbulence_expert
    geko_options: geko_options
    transition_model_options: transition_model_options
    transition_sst_option: transition_sst_option
    user_defined: user_defined
    sa_enhanced_wall_treatment: sa_enhanced_wall_treatment
    sa_damping: sa_damping
    return_type: str

class model_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sun_direction_vector(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class piecewise_linear_child(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class piecewise_linear(ListObject[piecewise_linear_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: piecewise_linear_child
    return_type: str

class number_of_coefficients(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coefficients(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class polynomial(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    number_of_coefficients: number_of_coefficients
    coefficients: coefficients
    return_type: str

class user_defined_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class direct_solar_irradiation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    constant: constant
    piecewise_linear: piecewise_linear
    polynomial: polynomial
    user_defined: user_defined_3
    return_type: str

class user_defined_4(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diffuse_solar_irradiation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    constant: constant
    piecewise_linear: piecewise_linear
    polynomial: polynomial
    user_defined: user_defined_4
    return_type: str

class spectral_fraction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class illumination_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    direct_solar_irradiation: direct_solar_irradiation
    diffuse_solar_irradiation: diffuse_solar_irradiation
    spectral_fraction: spectral_fraction
    return_type: str

class quad_tree_parameters(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ground_reflectivity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scattering_fraction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_on_adjacent_fluid(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class direction_from_solar_calculator(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_load_frequency(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class latitude(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class longitude(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class timezone(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class north_x(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class north_y(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class north_z(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class north_direction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    north_x: north_x
    north_y: north_y
    north_z: north_z
    return_type: str

class east_x(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class east_y(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class east_z(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class east_direction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    east_x: east_x
    east_y: east_y
    east_z: east_z
    return_type: str

class day(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class month(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hour(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minute(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class date_and_time(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    day: day
    month: month
    hour: hour
    minute: minute
    return_type: str

class calculator_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sunshine_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_calculator(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    latitude: latitude
    longitude: longitude
    timezone: timezone
    north_direction: north_direction
    east_direction: east_direction
    date_and_time: date_and_time
    calculator_method: calculator_method
    sunshine_factor: sunshine_factor
    return_type: str

class apply_full_solar_irradiation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_frequency_data(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_filename(Filename):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class autoread_solar_data(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    solar_frequency_data: solar_frequency_data
    solar_filename: solar_filename
    return_type: str

class use_binary_format(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class autosave_solar_data(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    solar_frequency_data: solar_frequency_data
    solar_filename: solar_filename
    use_binary_format: use_binary_format
    return_type: str

class solar_load(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    solar_model: solar_model
    sun_direction_vector: sun_direction_vector
    illumination_parameters: illumination_parameters
    quad_tree_parameters: quad_tree_parameters
    ground_reflectivity: ground_reflectivity
    scattering_fraction: scattering_fraction
    solar_on_adjacent_fluid: solar_on_adjacent_fluid
    direction_from_solar_calculator: direction_from_solar_calculator
    solar_load_frequency: solar_load_frequency
    solar_calculator: solar_calculator
    apply_full_solar_irradiation: apply_full_solar_irradiation
    autoread_solar_data: autoread_solar_data
    autosave_solar_data: autosave_solar_data
    def solar_on_demand(self):
        """
        Enable  solar load on demand.
        """
    return_type: str

class n_theta_divisions(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class n_phi_divisions(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class n_theta_pixels(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class n_phi_pixels(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class do_acceleration(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_4(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solution_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class do_energy_coupling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_4
    solution_method: solution_method
    return_type: str

class method_partially_specular_wall(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fast_second_order_discrete_ordinate(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blending_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class discrete_ordinates(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    n_theta_divisions: n_theta_divisions
    n_phi_divisions: n_phi_divisions
    n_theta_pixels: n_theta_pixels
    n_phi_pixels: n_phi_pixels
    do_acceleration: do_acceleration
    do_energy_coupling: do_energy_coupling
    method_partially_specular_wall: method_partially_specular_wall
    fast_second_order_discrete_ordinate: fast_second_order_discrete_ordinate
    blending_factor: blending_factor
    return_type: str

class number_of_histories(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class under_relaxation(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class target_cells_per_volume_cluster(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class monte_carlo(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    number_of_histories: number_of_histories
    under_relaxation: under_relaxation
    target_cells_per_volume_cluster: target_cells_per_volume_cluster
    return_type: str

class basis(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class method_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surfaces_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class smoothing(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class resolution(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class separation(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class subdivide(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class non_participating_zone_temperature(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viewfactor_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    basis: basis
    method: method_1
    surfaces: surfaces_2
    smoothing: smoothing
    resolution: resolution
    separation: separation
    subdivide: subdivide
    non_participating_zone_temperature: non_participating_zone_temperature
    return_type: str

class enable_mesh_interface_clustering(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class split_angle(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clustering_algorithm(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class global_faces_per_surface_cluster(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_faces_per_surface_cluster(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class faces_per_cluster(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_1
    global_faces_per_surface_cluster: global_faces_per_surface_cluster
    maximum_faces_per_surface_cluster: maximum_faces_per_surface_cluster
    return_type: str

class clustering_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    enable_mesh_interface_clustering: enable_mesh_interface_clustering
    split_angle: split_angle
    clustering_algorithm: clustering_algorithm
    faces_per_cluster: faces_per_cluster
    def print_thread_clusters(self):
        """
        Prints the following for all boundary threads: thread-id, number of faces, faces per surface cluster, and the number of surface clusters.
        """
    return_type: str

class maximum_radiation_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class residual_convergence_criteria(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radiosity_solver_control(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    maximum_radiation_iterations: maximum_radiation_iterations
    residual_convergence_criteria: residual_convergence_criteria
    return_type: str

class s2s(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    viewfactor_settings: viewfactor_settings
    clustering_settings: clustering_settings
    radiosity_solver_control: radiosity_solver_control
    def compute_write_vf(self, file_name: str):
        """
        Compute/write surface clusters and view factors for S2S radiation model.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def compute_vf_accelerated(self, file_name: str):
        """
        Compute/Write view factors from existing surface clusters.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def compute_clusters_and_vf_accelerated(self, file_name: str):
        """
        Compute/Write surface cluster first and then view factors.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def compute_vf_only(self, file_name: str):
        """
        Compute/write view factors only.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def read_vf_file(self, file_name: str):
        """
        Read an S2S file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    return_type: str

class start_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class end(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multiband_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    start: start_1
    end: end
    return_type: str

class multiband(NamedObject[multiband_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: multiband_child
    return_type: str

class method_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_interval(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iteration_interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solve_frequency(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    time_step_interval: time_step_interval
    time_interval: time_interval
    iteration_interval: iteration_interval
    return_type: str

class radiation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    model: model_1
    solar_load: solar_load
    discrete_ordinates: discrete_ordinates
    monte_carlo: monte_carlo
    s2s: s2s
    multiband: multiband
    solve_frequency: solve_frequency
    return_type: str

class material(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_material_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_material(NamedObject[phase_material_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_material_child
    return_type: str

class model_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    material: material
    phase_material: phase_material
    return_type: str

class inlet_diffusion_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thermal_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thickened_flame_model(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diffusion_energy_source(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multi_component_diffusion_mf_child(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multi_component_diffusion_mf(NamedObject[multi_component_diffusion_mf_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: multi_component_diffusion_mf_child
    return_type: str

class multi_component_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class liquid_energy_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class save_gradients(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_migration(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_transport_expert(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    inlet_diffusion: inlet_diffusion_1
    thermal_diffusion: thermal_diffusion
    thickened_flame_model: thickened_flame_model
    diffusion_energy_source: diffusion_energy_source
    multi_component_diffusion_mf: multi_component_diffusion_mf
    multi_component_diffusion: multi_component_diffusion
    liquid_energy_diffusion: liquid_energy_diffusion
    save_gradients: save_gradients
    species_migration: species_migration
    species_transport_expert: species_transport_expert
    return_type: str

class enable_volumetric_reactions(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_wall_surface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_particle_surface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_electrochemical_surface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reactions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_volumetric_reactions: enable_volumetric_reactions
    enable_wall_surface: enable_wall_surface
    enable_particle_surface: enable_particle_surface
    enable_electrochemical_surface: enable_electrochemical_surface
    return_type: str

class heat_of_surface_reactions(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mass_deposition_source(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reaction_diffusion_balance(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_reaction_aggresiveness_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_reaction_rate_temperature_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_reaction_solid_fraction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_surface_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    heat_of_surface_reactions: heat_of_surface_reactions
    mass_deposition_source: mass_deposition_source
    reaction_diffusion_balance: reaction_diffusion_balance
    surface_reaction_aggresiveness_factor: surface_reaction_aggresiveness_factor
    surface_reaction_rate_temperature_factor: surface_reaction_rate_temperature_factor
    surface_reaction_solid_fraction: surface_reaction_solid_fraction
    return_type: str

class turb_chem_interaction_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chemistry_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aggresiveness_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class transport_time_scale_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_temperature(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_chem_interaction_model_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    chemistry_iterations: chemistry_iterations
    aggresiveness_factor: aggresiveness_factor
    transport_time_scale_factor: transport_time_scale_factor
    min_temperature: min_temperature
    return_type: str

class linearize_convection_source(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class linearize_diffusion_source(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blending(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minimum_cell_quality_threshold(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_transport_expert_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    linearize_convection_source: linearize_convection_source
    linearize_diffusion_source: linearize_diffusion_source
    blending: blending
    minimum_cell_quality_threshold: minimum_cell_quality_threshold
    return_type: str

class edc_choice(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_fraction_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_scale_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edc_constant_coefficient_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    volume_fraction_constant: volume_fraction_constant
    time_scale_constant: time_scale_constant
    return_type: str

class edc_pasr_mixing_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mixing_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fractal_dimension(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edc_pasr_model_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    edc_pasr_mixing_model: edc_pasr_mixing_model
    mixing_constant: mixing_constant
    fractal_dimension: fractal_dimension
    return_type: str

class user_defined_edc_scales(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edc_model_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    edc_choice: edc_choice
    edc_constant_coefficient_options: edc_constant_coefficient_options
    edc_pasr_model_options: edc_pasr_model_options
    user_defined_edc_scales: user_defined_edc_scales
    return_type: str

class efficiency_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_points_in_flame(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class integral_length_scale(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sensor_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sensor_reaction_index(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beta_factor_omega_equation(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sensor_num_smooths(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tfm_model_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    efficiency_function: efficiency_function
    number_of_points_in_flame: number_of_points_in_flame
    integral_length_scale: integral_length_scale
    sensor_method: sensor_method
    sensor_reaction_index: sensor_reaction_index
    beta_factor_omega_equation: beta_factor_omega_equation
    sensor_num_smooths: sensor_num_smooths
    return_type: str

class chemistry_solver(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class integration_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class absolute_ode_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relative_ode_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class integration_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    absolute_ode_tolerance: absolute_ode_tolerance
    relative_ode_tolerance: relative_ode_tolerance
    return_type: str

class isat_error_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class isat_table_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class isat_verbosity(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class isat_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    isat_error_tolerance: isat_error_tolerance
    isat_table_size: isat_table_size
    isat_verbosity: isat_verbosity
    def clear_isat_table(self):
        """
        Clear the current ISAT table.
        """
    return_type: str

class chemistry_agglomeration(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chemistry_agglomeration_error_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chemistry_agglomeration_temperature_bin(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chemistry_agglomeration_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    chemistry_agglomeration_error_tolerance: chemistry_agglomeration_error_tolerance
    chemistry_agglomeration_temperature_bin: chemistry_agglomeration_temperature_bin
    return_type: str

class turbulent_rate_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chemical_rate_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fuel_species(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class equilibrium_rich_flammability(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rich_equivalence_ratio_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exponential_factor_beta(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class equilibrium_rich_flammability_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    rich_equivalence_ratio_limit: rich_equivalence_ratio_limit
    exponential_factor_beta: exponential_factor_beta
    return_type: str

class relax_to_equilibrium_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    turbulent_rate_constant: turbulent_rate_constant
    chemical_rate_constant: chemical_rate_constant
    fuel_species: fuel_species
    equilibrium_rich_flammability: equilibrium_rich_flammability
    equilibrium_rich_flammability_options: equilibrium_rich_flammability_options
    return_type: str

class dynamic_mechanism_reduction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mechanism_reduction_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mechanism_reduction_expert(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mechanism_reduction_min_target(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mechanism_reduction_target_threshold(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mechanism_reduction_targets(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mechanism_reduction_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    dynamic_mechanism_reduction_tolerance: dynamic_mechanism_reduction_tolerance
    dynamic_mechanism_reduction_expert: dynamic_mechanism_reduction_expert
    dynamic_mechanism_reduction_min_target: dynamic_mechanism_reduction_min_target
    dynamic_mechanism_reduction_target_threshold: dynamic_mechanism_reduction_target_threshold
    dynamic_mechanism_reduction_targets: dynamic_mechanism_reduction_targets
    return_type: str

class dimension_reduction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_represented_species(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class full_mechanism_material_name(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fuel_oxidizer_species(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dimension_reduction_mixture_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    number_of_represented_species: number_of_represented_species
    full_mechanism_material_name: full_mechanism_material_name
    fuel_oxidizer_species: fuel_oxidizer_species
    return_type: str

class integration_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    integration_method: integration_method
    integration_options: integration_options
    isat_options: isat_options
    chemistry_agglomeration: chemistry_agglomeration
    chemistry_agglomeration_options: chemistry_agglomeration_options
    relax_to_equilibrium_options: relax_to_equilibrium_options
    dynamic_mechanism_reduction: dynamic_mechanism_reduction
    dynamic_mechanism_reduction_options: dynamic_mechanism_reduction_options
    dimension_reduction: dimension_reduction
    dimension_reduction_mixture_options: dimension_reduction_mixture_options
    return_type: str

class species(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    model: model_2
    options: options_3
    reactions: reactions
    wall_surface_options: wall_surface_options
    turb_chem_interaction_model: turb_chem_interaction_model
    turb_chem_interaction_model_options: turb_chem_interaction_model_options
    species_transport_expert_options: species_transport_expert_options
    edc_model_options: edc_model_options
    tfm_model_options: tfm_model_options
    chemistry_solver: chemistry_solver
    integration_parameters: integration_parameters
    return_type: str

class contour_plotting_option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_update_every_iteration_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interaction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_2
    source_update_every_iteration_enabled: source_update_every_iteration_enabled
    iteration_interval: iteration_interval
    return_type: str

class option_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_creation_every_particle_step_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_time_step(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class n_time_steps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unsteady_tracking(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    option: option_3
    particle_creation_every_particle_step_enabled: particle_creation_every_particle_step_enabled
    dpm_time_step: dpm_time_step
    n_time_steps: n_time_steps
    def clear_particles_from_domain(self):
        """
        Clear all particles currently in the domain.
        """
    return_type: str

class general_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    contour_plotting_option: contour_plotting_option
    interaction: interaction
    unsteady_tracking: unsteady_tracking
    return_type: str

class particle_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_frame(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_streams(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inject_as_film(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class injection_type(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    cone_type: cone_type
    inject_as_film: inject_as_film
    return_type: str

class continuous_phase(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_rough_wall_treatment(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ddpm_phase(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_displacement(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    ddpm_phase: ddpm_phase
    return_type: str

class interaction_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    continuous_phase: continuous_phase
    enable_rough_wall_treatment: enable_rough_wall_treatment
    volume_displacement: volume_displacement
    return_type: str

class const_number_in_parcel(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class const_parcel_mass(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class const_parcel_diameter(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class parcel_method(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    const_number_in_parcel: const_number_in_parcel
    const_parcel_mass: const_parcel_mass
    const_parcel_diameter: const_parcel_diameter
    return_type: str

class enable_5(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_delay(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_reinjector(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_5
    time_delay: time_delay
    return_type: str

class shape_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cunningham_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_drag(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    shape_factor: shape_factor
    cunningham_factor: cunningham_factor
    return_type: str

class drag_law(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lift_law(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_rotation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_5
    drag_law: drag_law
    lift_law: lift_law
    return_type: str

class const_htc(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class const_nu(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class heat_exchange(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    const_htc: const_htc
    const_nu: const_nu
    return_type: str

class law_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_4(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_5(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_6(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_7(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_8(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_9(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class law_10(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class switch(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class custom_laws(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    law_1: law_1
    law_2: law_2
    law_3: law_3
    law_4: law_4
    law_5: law_5
    law_6: law_6
    law_7: law_7
    law_8: law_8
    law_9: law_9
    law_10: law_10
    switch: switch
    return_type: str

class random_eddy_lifetime(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_tries(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_scale_constant_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_dispersion(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    random_eddy_lifetime: random_eddy_lifetime
    number_of_tries: number_of_tries
    time_scale_constant: time_scale_constant_1
    return_type: str

class constant_y0(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_child_droplets(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_b1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_b0(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_cl(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_ctau(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_crt(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class critical_weber_number(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class core_b1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_xi(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class target_number_in_parcel(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_c0(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class column_drag_coeff(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ligament_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class jet_diameter(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_k1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_k2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_tb(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class droplet_breakup(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    constant_y0: constant_y0
    number_of_child_droplets: number_of_child_droplets
    constant_b1: constant_b1
    constant_b0: constant_b0
    constant_cl: constant_cl
    constant_ctau: constant_ctau
    constant_crt: constant_crt
    critical_weber_number: critical_weber_number
    core_b1: core_b1
    constant_xi: constant_xi
    target_number_in_parcel: target_number_in_parcel
    constant_c0: constant_c0
    column_drag_coeff: column_drag_coeff
    ligament_factor: ligament_factor
    jet_diameter: jet_diameter
    constant_k1: constant_k1
    constant_k2: constant_k2
    constant_tb: constant_tb
    return_type: str

class physical_models_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    particle_drag: particle_drag
    particle_rotation: particle_rotation
    heat_exchange: heat_exchange
    custom_laws: custom_laws
    turbulent_dispersion: turbulent_dispersion
    droplet_breakup: droplet_breakup
    return_type: str

class x(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class azimuthal_start_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class azimuthal_stop_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class injection_surfaces(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class random_surface_inj(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class location_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x: x
    x_2: x_2
    y: y
    y_2: y_2
    z: z
    z_2: z_2
    azimuthal_start_angle: azimuthal_start_angle
    azimuthal_stop_angle: azimuthal_stop_angle
    injection_surfaces: injection_surfaces
    random_surface_inj: random_surface_inj
    return_type: str

class r(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x: x
    y: y
    z: z
    return_type: str

class u(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x: x
    y: y
    z: z
    return_type: str

class matrix(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    r: r
    u: u
    return_type: str

class half_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dispersion_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inner_radius(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class outer_radius(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_axis(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_axis(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_axis(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    half_angle: half_angle
    dispersion_angle: dispersion_angle
    inner_radius: inner_radius
    outer_radius: outer_radius
    x_axis: x_axis
    y_axis: y_axis
    z_axis: z_axis
    return_type: str

class x_velocity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_velocity_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_velocity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_velocity_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_velocity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_velocity_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class magnitude(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class swirl_fraction(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_face_normal_direction(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_velocity: x_velocity
    x_velocity_2: x_velocity_2
    y_velocity: y_velocity
    y_velocity_2: y_velocity_2
    z_velocity: z_velocity
    z_velocity_2: z_velocity_2
    magnitude: magnitude
    swirl_fraction: swirl_fraction
    use_face_normal_direction: use_face_normal_direction
    return_type: str

class angular_velocity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x: x
    x_2: x_2
    y: y
    y_2: y_2
    z: z
    z_2: z_2
    magnitude: magnitude
    return_type: str

class flow_rate(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_rate_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class total_flow_rate(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_by_area(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mass_flow_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    flow_rate: flow_rate
    flow_rate_2: flow_rate_2
    total_flow_rate: total_flow_rate
    scale_by_area: scale_by_area
    return_type: str

class start_time(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stop_time(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class times(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    start_time: start_time
    stop_time: stop_time
    return_type: str

class diameter(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diameter_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_diam(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_diam(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mean_diam(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spread(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_diameters(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rosin_rammler_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    min_diam: min_diam
    max_diam: max_diam
    mean_diam: mean_diam
    spread: spread
    number_of_diameters: number_of_diameters
    return_type: str

class table_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class column_with_diameters(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class column_with_number_fractions(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class column_with_mass_fractions(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class accumulated_number_fraction(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class accumulated_mass_fraction(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tabulated_size_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    table_name: table_name
    column_with_diameters: column_with_diameters
    column_with_number_fractions: column_with_number_fractions
    column_with_mass_fractions: column_with_mass_fractions
    accumulated_number_fraction: accumulated_number_fraction
    accumulated_mass_fraction: accumulated_mass_fraction
    return_type: str

class particle_size(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    diameter: diameter
    diameter_2: diameter_2
    option: option
    rosin_rammler_settings: rosin_rammler_settings
    tabulated_size_settings: tabulated_size_settings
    return_type: str

class temperature(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_props(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    location: location_1
    matrix: matrix
    cone_settings: cone_settings
    velocity: velocity
    angular_velocity: angular_velocity
    mass_flow_rate: mass_flow_rate
    times: times
    particle_size: particle_size
    temperature: temperature
    temperature_2: temperature_2
    return_type: str

class injections_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    particle_type: particle_type
    material: material
    reference_frame: reference_frame
    number_of_streams: number_of_streams
    injection_type: injection_type
    interaction: interaction_1
    parcel_method: parcel_method
    particle_reinjector: particle_reinjector
    physical_models: physical_models_1
    initial_props: initial_props
    return_type: str

class injections(NamedObject[injections_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: injections_child
    return_type: str

class node_based_averaging_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_term_averaging_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class averaging_every_step_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kernel(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gaussian_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class averaging_kernel(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    kernel: kernel
    gaussian_factor: gaussian_factor
    return_type: str

class averaging(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    node_based_averaging_enabled: node_based_averaging_enabled
    source_term_averaging_enabled: source_term_averaging_enabled
    averaging_every_step_enabled: averaging_every_step_enabled
    averaging_kernel: averaging_kernel
    return_type: str

class keep_linearized_source_terms_constant(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_term_linearization_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enhanced_linearization_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class linearized_source_terms_limiter(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class linearization(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    keep_linearized_source_terms_constant: keep_linearized_source_terms_constant
    source_term_linearization_enabled: source_term_linearization_enabled
    enhanced_linearization_enabled: enhanced_linearization_enabled
    linearized_source_terms_limiter: linearized_source_terms_limiter
    return_type: str

class implicit_momentum_coupling(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class implicit_source_term_coupling(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class linear_growth_of_dpm_source_terms(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reset_sources_at_timestep(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class underrelaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class second_order_time_accurate_sources_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_terms(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    linearization: linearization
    implicit_momentum_coupling: implicit_momentum_coupling
    implicit_source_term_coupling: implicit_source_term_coupling
    linear_growth_of_dpm_source_terms: linear_growth_of_dpm_source_terms
    reset_sources_at_timestep: reset_sources_at_timestep
    underrelaxation_factor: underrelaxation_factor
    second_order_time_accurate_sources_enabled: second_order_time_accurate_sources_enabled
    return_type: str

class scheme(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class low_order_scheme(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class high_order_scheme(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_4(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_number_of_refinements(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_cells_to_cross(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class accuracy_control(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_4
    tolerance: tolerance
    max_number_of_refinements: max_number_of_refinements
    number_of_cells_to_cross: number_of_cells_to_cross
    return_type: str

class tracking_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    scheme: scheme
    low_order_scheme: low_order_scheme
    high_order_scheme: high_order_scheme
    accuracy_control: accuracy_control
    return_type: str

class numerics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    averaging: averaging
    source_terms: source_terms
    tracking: tracking_1
    return_type: str

class option_5(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class parallel_verbosity_level(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class crossover_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expert_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    parallel_verbosity_level: parallel_verbosity_level
    crossover_tolerance: crossover_tolerance
    return_type: str

class option_6(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partitioning_method_for_dpm_domain(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_domain(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_6
    partitioning_method_for_dpm_domain: partitioning_method_for_dpm_domain
    return_type: str

class ordered_accumulation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hybrid_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    dpm_domain: dpm_domain
    ordered_accumulation: ordered_accumulation
    return_type: str

class parallel_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_5
    expert_options: expert_options
    hybrid_options: hybrid_options
    return_type: str

class option_7(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_gradient_force(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_7
    return_type: str

class option_8(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class virtual_mass_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class virtual_mass_force(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_8
    virtual_mass_factor: virtual_mass_factor
    return_type: str

class option_9(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_vf_allowed_for_blocking(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class drag_scaling_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_term_scaling_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_displacement_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_9
    max_vf_allowed_for_blocking: max_vf_allowed_for_blocking
    drag_scaling_enabled: drag_scaling_enabled
    source_term_scaling_enabled: source_term_scaling_enabled
    return_type: str

class enable_6(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_approximation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convective_heat_transfer(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_6
    turbulent_approximation: turbulent_approximation
    return_type: str

class include_convective_heat_transfer(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class condensing_film(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class all_film(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_movement(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    condensing_film: condensing_film
    all_film: all_film
    return_type: str

class lwf_particle_inclusion_in_dpm_concentration_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class limiter_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class report_leidenfrost_temperature(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class offset_above_film_boiling_temperature(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_film_temperature_limiter(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    limiter_enabled: limiter_enabled
    report_leidenfrost_temperature: report_leidenfrost_temperature
    offset_above_film_boiling_temperature: offset_above_film_boiling_temperature
    return_type: str

class wall_film(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    convective_heat_transfer: convective_heat_transfer
    include_convective_heat_transfer: include_convective_heat_transfer
    film_movement: film_movement
    lwf_particle_inclusion_in_dpm_concentration_enabled: lwf_particle_inclusion_in_dpm_concentration_enabled
    wall_film_temperature_limiter: wall_film_temperature_limiter
    return_type: str

class physical_models(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pressure_gradient_force: pressure_gradient_force
    virtual_mass_force: virtual_mass_force
    volume_displacement: volume_displacement_1
    wall_film: wall_film
    return_type: str

class high_res_tracking_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class re_randomization_every_iteration_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class re_randomization_every_timestep_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tracking_statistics_format(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expert_options_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    re_randomization_every_iteration_enabled: re_randomization_every_iteration_enabled
    re_randomization_every_timestep_enabled: re_randomization_every_timestep_enabled
    tracking_statistics_format: tracking_statistics_format
    verbosity: verbosity_1
    return_type: str

class always_use_face_centroid_with_periodics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_cp_interpolation_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_density_interpolation_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_gradient_interpolation_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_viscosity_interpolation_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_temperature_interpolation_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zero_nodal_velocities_on_walls(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interpolation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    flow_cp_interpolation_enabled: flow_cp_interpolation_enabled
    flow_density_interpolation_enabled: flow_density_interpolation_enabled
    flow_gradient_interpolation_enabled: flow_gradient_interpolation_enabled
    flow_viscosity_interpolation_enabled: flow_viscosity_interpolation_enabled
    flow_temperature_interpolation_enabled: flow_temperature_interpolation_enabled
    zero_nodal_velocities_on_walls: zero_nodal_velocities_on_walls
    return_type: str

class boundary_layer_tracking(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class check_subtet_validity(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class automatic_intersection_tolerance_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class barycentric_intersection_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enhanced_cell_relocation_method(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class load_legacy_particles(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class overset_relocation_robustness_level(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class legacy_particle_location_method_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_relocation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enhanced_cell_relocation_method: enhanced_cell_relocation_method
    load_legacy_particles: load_legacy_particles
    overset_relocation_robustness_level: overset_relocation_robustness_level
    legacy_particle_location_method_enabled: legacy_particle_location_method_enabled
    return_type: str

class stuck_particle_removal_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class barycentric_sampling_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class quad_face_use_centroid_enabled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class high_res_tracking_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    always_use_face_centroid_with_periodics: always_use_face_centroid_with_periodics
    interpolation: interpolation
    boundary_layer_tracking: boundary_layer_tracking
    check_subtet_validity: check_subtet_validity
    automatic_intersection_tolerance_enabled: automatic_intersection_tolerance_enabled
    barycentric_intersection_enabled: barycentric_intersection_enabled
    particle_relocation: particle_relocation
    stuck_particle_removal_enabled: stuck_particle_removal_enabled
    barycentric_sampling_enabled: barycentric_sampling_enabled
    quad_face_use_centroid_enabled: quad_face_use_centroid_enabled
    return_type: str

class control_by(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_number_of_steps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class length_scale(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class step_length_factor(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tracking_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    control_by: control_by
    max_number_of_steps: max_number_of_steps
    length_scale: length_scale
    step_length_factor: step_length_factor
    return_type: str

class track_in_absolute_frame(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tracking(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    high_res_tracking_enabled: high_res_tracking_enabled
    expert_options: expert_options_1
    high_res_tracking_options: high_res_tracking_options
    tracking_parameters: tracking_parameters
    track_in_absolute_frame: track_in_absolute_frame
    return_type: str

class body_force_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class erosion_accretion_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class output_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scalar_update_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class collision_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_time_step_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class impingement_model_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_regime_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class splashing_distribution_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_scalars(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interpolation_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_udf_species(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_functions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    body_force_function: body_force_function
    source_function: source_function
    erosion_accretion_function: erosion_accretion_function
    output_function: output_function
    scalar_update_function: scalar_update_function
    collision_function: collision_function
    dpm_time_step_function: dpm_time_step_function
    impingement_model_function: impingement_model_function
    film_regime_function: film_regime_function
    splashing_distribution_function: splashing_distribution_function
    number_of_scalars: number_of_scalars
    interpolation_function: interpolation_function
    maximum_udf_species: maximum_udf_species
    return_type: str

class discrete_phase(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    general_settings: general_settings
    injections: injections
    numerics: numerics
    parallel: parallel_1
    physical_models: physical_models
    tracking: tracking
    user_defined_functions: user_defined_functions
    return_type: str

class enable_7(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mode(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_blades(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotor_speed(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tip_radius(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class root_radius(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class basic_info(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    number_of_blades: number_of_blades
    rotor_speed: rotor_speed
    tip_radius: tip_radius
    root_radius: root_radius
    return_type: str

class disk_origin_x(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_origin_y(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_origin_z(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_origin(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    disk_origin_x: disk_origin_x
    disk_origin_y: disk_origin_y
    disk_origin_z: disk_origin_z
    return_type: str

class terminology(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_normal_x(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_normal_y(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_normal_z(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_pitch_angle(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_bank_angle(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_orientation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    terminology: terminology
    disk_normal_x: disk_normal_x
    disk_normal_y: disk_normal_y
    disk_normal_z: disk_normal_z
    disk_pitch_angle: disk_pitch_angle
    disk_bank_angle: disk_bank_angle
    return_type: str

class embedded_face_zone(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class floating_surface_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disk_id(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    embedded_face_zone: embedded_face_zone
    floating_surface_name: floating_surface_name
    def create_floating_disk(self):
        """
        'create_floating_disk' command.
        """
    return_type: str

class blade_pitch_collective(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blade_pitch_cyclic_sin(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blade_pitch_cyclic_cos(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blade_pitch_angles(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    blade_pitch_collective: blade_pitch_collective
    blade_pitch_cyclic_sin: blade_pitch_cyclic_sin
    blade_pitch_cyclic_cos: blade_pitch_cyclic_cos
    return_type: str

class blade_flapping_cone(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blade_flapping_cyclic_sin(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blade_flapping_cyclic_cos(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blade_flap_angles(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    blade_flapping_cone: blade_flapping_cone
    blade_flapping_cyclic_sin: blade_flapping_cyclic_sin
    blade_flapping_cyclic_cos: blade_flapping_cyclic_cos
    return_type: str

class model_tip_loss(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tip_loss_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class prandtl_tuning_coefficient(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tip_loss(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    model_tip_loss: model_tip_loss
    tip_loss_limit: tip_loss_limit
    prandtl_tuning_coefficient: prandtl_tuning_coefficient
    return_type: str

class general_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    basic_info: basic_info
    disk_origin: disk_origin
    disk_orientation: disk_orientation
    disk_id: disk_id
    blade_pitch_angles: blade_pitch_angles
    blade_flap_angles: blade_flap_angles
    tip_loss: tip_loss
    return_type: str

class radius_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chord(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class twist(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class airfoil_data_file(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geometry_2_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    radius_ratio: radius_ratio
    chord: chord
    twist: twist
    airfoil_data_file: airfoil_data_file
    return_type: str

class geometry_2(NamedObject[geometry_2_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: geometry_2_child
    return_type: str

class trim_option(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class update_frequency(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class damping_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thrust_coef(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pitch_moment_coef(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class roll_moment_coef(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class trimming(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    trim_option: trim_option
    update_frequency: update_frequency
    damping_factor: damping_factor
    thrust_coef: thrust_coef
    pitch_moment_coef: pitch_moment_coef
    roll_moment_coef: roll_moment_coef
    return_type: str

class rotor_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    general: general_1
    geometry: geometry_2
    trimming: trimming
    return_type: str

class rotor(NamedObject[rotor_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: rotor_child
    return_type: str

class virtual_blade_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    enable: enable_7
    mode: mode
    rotor: rotor
    def apply(self):
        """
        Read and apply VBM setting.
        """
    return_type: str

class enable_8(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ray_points_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beam_vector(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beams_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    ap_face_zone: ap_face_zone
    beam_length: beam_length
    ray_points_count: ray_points_count
    beam_vector: beam_vector
    return_type: str

class beams(NamedObject[beams_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def copy(self, orig_beam_name: str, beam_name: str, ap_face_zone: str, beam_length: float | str, ray_npoints: int, x_beam_vector: float | str, y_beam_vector: float | str, z_beam_vector: float | str):
        """
        Copy optical beam grid.
        
        Parameters
        ----------
            orig_beam_name : str
                The name for the optical beam to be copied.
            beam_name : str
                A unique name for each optical beam.
            ap_face_zone : str
                The wall face zones to specify the optical aperture surface.
            beam_length : real
                The length of optical beam propagation.
            ray_npoints : int
                The number of grid point in each ray of the optical beam.
            x_beam_vector : real
                The x-component of the beam propagation vector.
            y_beam_vector : real
                The y-component of the beam propagation vector.
            z_beam_vector : real
                The z-component of the beam propagation vector.
        """
    child_object_type: beams_child
    return_type: str

class reset_statistics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class statistics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    reset_statistics: reset_statistics
    def statistics_controls(self, method: int, samp_time_period: float | str, samp_time_steps: int, avg_time_period: float | str, avg_time_steps: int):
        """
        'statistics_controls' command.
        """
    return_type: str

class sampling_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class index_of_refraction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class report_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class optics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_8
    beams: beams
    statistics: statistics
    sampling_iterations: sampling_iterations
    index_of_refraction: index_of_refraction
    report: report_1
    verbosity: verbosity_2
    return_type: str

class thermal_effects_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_4(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    thermal_effects: thermal_effects_1
    return_type: str

class numerical_damping_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enhanced_strain(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unsteady_damping_rayleigh(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class amg_stabilization(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_iter(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    numerical_damping_factor: numerical_damping_factor
    enhanced_strain: enhanced_strain
    unsteady_damping_rayleigh: unsteady_damping_rayleigh
    amg_stabilization: amg_stabilization
    max_iter: max_iter
    return_type: str

class include_pop_in_fsi_force(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class steady_2way_fsi(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class include_viscous_fsi_force(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class explicit_fsi_force(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class starting_t_re_initialization(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expert(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    include_pop_in_fsi_force: include_pop_in_fsi_force
    steady_2way_fsi: steady_2way_fsi
    include_viscous_fsi_force: include_viscous_fsi_force
    explicit_fsi_force: explicit_fsi_force
    starting_t_re_initialization: starting_t_re_initialization
    return_type: str

class structure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    model: model
    options: options_4
    controls: controls
    expert: expert
    return_type: str

class enabled_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_1
    return_type: str

class models(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    multiphase: multiphase
    energy: energy
    viscous: viscous
    radiation: radiation
    species: species
    discrete_phase: discrete_phase
    virtual_blade_model: virtual_blade_model
    optics: optics
    structure: structure
    ablation: ablation
    return_type: str

class database_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class database(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    database_type: database_type
    def copy_by_formula(self, type: str, formula: str):
        """
        Copy a material from the database (pick by formula).
        
        Parameters
        ----------
            type : str
                'type' child.
            formula : str
                'formula' child.
        """
    def copy_by_name(self, type: str, name: str):
        """
        Copy a material from the database (pick by name).
        
        Parameters
        ----------
            type : str
                'type' child.
            name : str
                'name' child.
        """
    def list_materials(self):
        """
        List all materials in the database.
        """
    def list_properties(self, name: str):
        """
        List the properties of a material in the database.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    return_type: str

class name_2(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class chemical_formula(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_10(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nist_fluid(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lookup_table(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_points(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_minimum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_maximum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_points(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_minimum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_maximum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class saturation_points(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class real_gas_nist(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    nist_fluid: nist_fluid
    lookup_table: lookup_table
    pressure_points: pressure_points
    pressure_minimum: pressure_minimum
    pressure_maximum: pressure_maximum
    temperature_points: temperature_points
    temperature_minimum: temperature_minimum
    temperature_maximum: temperature_maximum
    saturation_points: saturation_points
    return_type: str

class value_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_density(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_bulk_modulus(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density_exponent(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_density_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minimum_density_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class compressible_liquid(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    reference_pressure: reference_pressure
    reference_density: reference_density
    reference_bulk_modulus: reference_bulk_modulus
    density_exponent: density_exponent
    maximum_density_ratio: maximum_density_ratio
    minimum_density_ratio: minimum_density_ratio
    return_type: str

class minimum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class piecewise_polynomial_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    minimum: minimum
    maximum: maximum
    number_of_coefficients: number_of_coefficients
    coefficients: coefficients
    return_type: str

class piecewise_polynomial(ListObject[piecewise_polynomial_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: piecewise_polynomial_child
    return_type: str

class expression(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rgp_table(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    real_gas_nist: real_gas_nist
    value: value_1
    compressible_liquid: compressible_liquid
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    rgp_table: rgp_table
    return_type: str

class b(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_viscosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_temperature_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_exponent(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class power_law(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    b: b
    reference_viscosity: reference_viscosity
    reference_temperature: reference_temperature_1
    temperature_exponent: temperature_exponent
    return_type: str

class a(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class c(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blottner_curve_fit(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    a: a
    b: b
    c: c
    return_type: str

class gupta_curve_fit_viscosity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    a: a
    b: b
    c: c
    return_type: str

class c1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class c2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class effective_temperature(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sutherland(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    c1: c1
    c2: c2
    reference_viscosity: reference_viscosity
    reference_temperature: reference_temperature_1
    effective_temperature: effective_temperature
    return_type: str

class zero_shear_viscosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class power_law_index(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class activation_energy(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cross(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    zero_shear_viscosity: zero_shear_viscosity
    power_law_index: power_law_index
    time_constant: time_constant
    reference_temperature: reference_temperature_1
    activation_energy: activation_energy
    return_type: str

class consistency_index(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class yield_stress_threshold(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class critical_shear_rate(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class herschel_bulkley(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    consistency_index: consistency_index
    power_law_index: power_law_index
    yield_stress_threshold: yield_stress_threshold
    critical_shear_rate: critical_shear_rate
    reference_temperature: reference_temperature_1
    activation_energy: activation_energy
    return_type: str

class infinite_shear_viscosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class carreau(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    time_constant: time_constant
    power_law_index: power_law_index
    zero_shear_viscosity: zero_shear_viscosity
    infinite_shear_viscosity: infinite_shear_viscosity
    reference_temperature: reference_temperature_1
    activation_energy: activation_energy
    return_type: str

class minimum_viscosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_viscosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class non_newtonian_power_law(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    consistency_index: consistency_index
    power_law_index: power_law_index
    minimum_viscosity: minimum_viscosity
    maximum_viscosity: maximum_viscosity
    reference_temperature: reference_temperature_1
    activation_energy: activation_energy
    return_type: str

class viscosity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    power_law: power_law
    blottner_curve_fit: blottner_curve_fit
    gupta_curve_fit_viscosity: gupta_curve_fit_viscosity
    sutherland: sutherland
    cross: cross
    herschel_bulkley: herschel_bulkley
    carreau: carreau
    non_newtonian_power_law: non_newtonian_power_law
    user_defined_function: user_defined_function
    rgp_table: rgp_table
    real_gas_nist: real_gas_nist
    return_type: str

class nasa_9_piecewise_polynomial_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    minimum: minimum
    maximum: maximum
    number_of_coefficients: number_of_coefficients
    coefficients: coefficients
    return_type: str

class nasa_9_piecewise_polynomial(ListObject[nasa_9_piecewise_polynomial_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: nasa_9_piecewise_polynomial_child
    return_type: str

class specific_heat(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial
    user_defined_function: user_defined_function
    rgp_table: rgp_table
    real_gas_nist: real_gas_nist
    return_type: str

class d(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class e(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gupta_curve_fit_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    a: a
    b: b
    c: c
    d: d
    e: e
    return_type: str

class thermal_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    gupta_curve_fit_conductivity: gupta_curve_fit_conductivity
    expression: expression
    user_defined_function: user_defined_function
    rgp_table: rgp_table
    real_gas_nist: real_gas_nist
    return_type: str

class molecular_weight(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    rgp_table: rgp_table
    return_type: str

class combustion_mixture(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class premix_laminar_speed(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    combustion_mixture: combustion_mixture
    return_type: str

class premix_critical_strain(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class premix_unburnt_temp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class premix_unburnt_density(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class premix_heat_trans_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class premix_heat_of_comb(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class premix_unburnt_fuel_mf(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class premix_adiabatic_temp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class therm_exp_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class vibrational_temperature_mode_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vibrational_degeneracy_mode_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vibrational_temperature_mode_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vibrational_degeneracy_mode_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vibrational_temperature_mode_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vibrational_degeneracy_mode_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vibrational_modes(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    vibrational_temperature_mode_1: vibrational_temperature_mode_1
    vibrational_degeneracy_mode_1: vibrational_degeneracy_mode_1
    vibrational_temperature_mode_2: vibrational_temperature_mode_2
    vibrational_degeneracy_mode_2: vibrational_degeneracy_mode_2
    vibrational_temperature_mode_3: vibrational_temperature_mode_3
    vibrational_degeneracy_mode_3: vibrational_degeneracy_mode_3
    return_type: str

class characteristic_vibrational_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    vibrational_modes: vibrational_modes
    value: value_1
    return_type: str

class gray_band_coefficients(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class absorption_coefficient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    gray_band_coefficients: gray_band_coefficients
    user_defined_function: user_defined_function
    return_type: str

class melting_heat(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class tsolidus(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class tliqidus(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class liquidus_slope(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class partition_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class eutectic_mf(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class solid_diffusion(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class solut_exp_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class scattering_coefficient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    return_type: str

class forward_scattering_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class asymmetry_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class delta_eddington(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    forward_scattering_factor: forward_scattering_factor
    asymmetry_factor: asymmetry_factor
    return_type: str

class scattering_phase_function(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    delta_eddington: delta_eddington
    user_defined_function: user_defined_function
    return_type: str

class refractive_index(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    gray_band_coefficients: gray_band_coefficients
    return_type: str

class formation_entropy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class formation_enthalpy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class reference_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class lennard_jones_length(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class lennard_jones_energy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class thermal_accom_coefficient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class velocity_accom_coefficient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class degrees_of_freedom(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class matrix_component(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class anisotropic(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    matrix_component: matrix_component
    diffusivity: diffusivity
    return_type: str

class direction_0(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class direction_1(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diffusivity_0(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class diffusivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class diffusivity_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class orthotropic(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    direction_0: direction_0
    direction_1: direction_1
    diffusivity_0: diffusivity_0
    diffusivity_1: diffusivity_1
    diffusivity_2: diffusivity_2
    return_type: str

class axis_origin(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_direction(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radial_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class tangential_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class axial_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class cyl_orthotropic(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    axis_origin: axis_origin
    axis_direction: axis_direction
    radial_diffusivity: radial_diffusivity
    tangential_diffusivity: tangential_diffusivity
    axial_diffusivity: axial_diffusivity
    return_type: str

class uds_diffusivities_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    expression: expression
    polynomial: polynomial
    user_defined_function: user_defined_function
    anisotropic: anisotropic
    orthotropic: orthotropic
    cyl_orthotropic: cyl_orthotropic
    return_type: str

class uds_diffusivities(NamedObject[uds_diffusivities_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: uds_diffusivities_child
    return_type: str

class uds_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    uds_diffusivities: uds_diffusivities
    user_defined_function: user_defined_function
    return_type: str

class electric_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    return_type: str

class dual_electric_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    return_type: str

class lithium_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    return_type: str

class magnetic_permeability(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class speed_of_sound(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    return_type: str

class critical_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class critical_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class critical_volume(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class acentric_factor(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class latent_heat(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class saturation_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    return_type: str

class vaporization_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class charge(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class fluid_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density
    viscosity: viscosity
    specific_heat: specific_heat
    thermal_conductivity: thermal_conductivity
    molecular_weight: molecular_weight
    premix_laminar_speed: premix_laminar_speed
    premix_critical_strain: premix_critical_strain
    premix_unburnt_temp: premix_unburnt_temp
    premix_unburnt_density: premix_unburnt_density
    premix_heat_trans_coeff: premix_heat_trans_coeff
    premix_heat_of_comb: premix_heat_of_comb
    premix_unburnt_fuel_mf: premix_unburnt_fuel_mf
    premix_adiabatic_temp: premix_adiabatic_temp
    therm_exp_coeff: therm_exp_coeff
    characteristic_vibrational_temperature: characteristic_vibrational_temperature
    absorption_coefficient: absorption_coefficient
    melting_heat: melting_heat
    tsolidus: tsolidus
    tliqidus: tliqidus
    liquidus_slope: liquidus_slope
    partition_coeff: partition_coeff
    eutectic_mf: eutectic_mf
    solid_diffusion: solid_diffusion
    solut_exp_coeff: solut_exp_coeff
    scattering_coefficient: scattering_coefficient
    scattering_phase_function: scattering_phase_function
    refractive_index: refractive_index
    formation_entropy: formation_entropy
    formation_enthalpy: formation_enthalpy
    reference_temperature: reference_temperature
    lennard_jones_length: lennard_jones_length
    lennard_jones_energy: lennard_jones_energy
    thermal_accom_coefficient: thermal_accom_coefficient
    velocity_accom_coefficient: velocity_accom_coefficient
    degrees_of_freedom: degrees_of_freedom
    uds_diffusivity: uds_diffusivity
    electric_conductivity: electric_conductivity
    dual_electric_conductivity: dual_electric_conductivity
    lithium_diffusivity: lithium_diffusivity
    magnetic_permeability: magnetic_permeability
    speed_of_sound: speed_of_sound
    critical_temperature: critical_temperature
    critical_pressure: critical_pressure
    critical_volume: critical_volume
    acentric_factor: acentric_factor
    latent_heat: latent_heat
    saturation_pressure: saturation_pressure
    vaporization_temperature: vaporization_temperature
    charge: charge
    return_type: str

class fluid(NamedObject[fluid_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: fluid_child
    return_type: str

class density_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    value: value_1
    return_type: str

class specific_heat_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial
    return_type: str

class planar_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class transverse_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class biaxial(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    planar_conductivity: planar_conductivity
    transverse_conductivity: transverse_conductivity
    return_type: str

class radial_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class tangential_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class axial_conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class cyl_orthotropic_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    axis_origin: axis_origin
    axis_direction: axis_direction
    radial_conductivity: radial_conductivity
    tangential_conductivity: tangential_conductivity
    axial_conductivity: axial_conductivity
    return_type: str

class conductivity_0(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class conductivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class conductivity_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class orthotropic_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    direction_0: direction_0
    direction_1: direction_1
    conductivity_0: conductivity_0
    conductivity_1: conductivity_1
    conductivity_2: conductivity_2
    return_type: str

class principal_axes(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class principal_values(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class conductivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class principal_axes_values(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    principal_axes: principal_axes
    principal_values: principal_values
    conductivity: conductivity
    return_type: str

class anisotropic_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    matrix_component: matrix_component
    conductivity: conductivity
    return_type: str

class thermal_conductivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    biaxial: biaxial
    cyl_orthotropic: cyl_orthotropic_1
    orthotropic: orthotropic_1
    principal_axes_values: principal_axes_values
    anisotropic: anisotropic_1
    user_defined_function: user_defined_function
    return_type: str

class atomic_number(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class scattering_coefficient_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    gray_band_coefficients: gray_band_coefficients
    user_defined_function: user_defined_function
    return_type: str

class uds_diffusivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    uds_diffusivities: uds_diffusivities
    user_defined_function: user_defined_function
    return_type: str

class youngs_modulus_0(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class youngs_modulus_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class youngs_modulus_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class shear_modulus_01(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class shear_modulus_12(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class shear_modulus_02(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class orthotropic_structure_ym(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    direction_0: direction_0
    direction_1: direction_1
    youngs_modulus_0: youngs_modulus_0
    youngs_modulus_1: youngs_modulus_1
    youngs_modulus_2: youngs_modulus_2
    shear_modulus_01: shear_modulus_01
    shear_modulus_12: shear_modulus_12
    shear_modulus_02: shear_modulus_02
    return_type: str

class struct_youngs_modulus(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    orthotropic_structure_ym: orthotropic_structure_ym
    user_defined_function: user_defined_function
    return_type: str

class poisson_ratio_01(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class poisson_ratio_12(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class poisson_ratio_02(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class orthotropic_structure_nu(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    poisson_ratio_01: poisson_ratio_01
    poisson_ratio_12: poisson_ratio_12
    poisson_ratio_02: poisson_ratio_02
    return_type: str

class struct_poisson_ratio(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    orthotropic_structure_nu: orthotropic_structure_nu
    user_defined_function: user_defined_function
    return_type: str

class struct_start_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class thermal_expansion_0(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class thermal_expansion_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class thermal_expansion_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class orthotropic_structure_te(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    thermal_expansion_0: thermal_expansion_0
    thermal_expansion_1: thermal_expansion_1
    thermal_expansion_2: thermal_expansion_2
    return_type: str

class struct_thermal_expansion(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    orthotropic_structure_te: orthotropic_structure_te
    user_defined_function: user_defined_function
    return_type: str

class struct_damping_alpha(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class struct_damping_beta(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class solid_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_1
    specific_heat: specific_heat_1
    thermal_conductivity: thermal_conductivity_1
    atomic_number: atomic_number
    absorption_coefficient: absorption_coefficient
    scattering_coefficient: scattering_coefficient_1
    scattering_phase_function: scattering_phase_function
    refractive_index: refractive_index
    uds_diffusivity: uds_diffusivity_1
    electric_conductivity: electric_conductivity
    dual_electric_conductivity: dual_electric_conductivity
    lithium_diffusivity: lithium_diffusivity
    magnetic_permeability: magnetic_permeability
    struct_youngs_modulus: struct_youngs_modulus
    struct_poisson_ratio: struct_poisson_ratio
    struct_start_temperature: struct_start_temperature
    struct_thermal_expansion: struct_thermal_expansion
    struct_damping_alpha: struct_damping_alpha
    struct_damping_beta: struct_damping_beta
    return_type: str

class solid(NamedObject[solid_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: solid_child
    return_type: str

class composition_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_fractions(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class real_gas_nist_mixture(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    lookup_table: lookup_table
    composition_type: composition_type
    species_fractions: species_fractions
    pressure_points: pressure_points
    pressure_minimum: pressure_minimum
    pressure_maximum: pressure_maximum
    temperature_points: temperature_points
    temperature_minimum: temperature_minimum
    temperature_maximum: temperature_maximum
    return_type: str

class density_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    real_gas_nist_mixture: real_gas_nist_mixture
    user_defined_function: user_defined_function
    return_type: str

class viscosity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    power_law: power_law
    sutherland: sutherland
    user_defined_function: user_defined_function
    real_gas_nist_mixture: real_gas_nist_mixture
    return_type: str

class specific_heat_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial
    real_gas_nist_mixture: real_gas_nist_mixture
    user_defined_function: user_defined_function
    return_type: str

class thermal_conductivity_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    user_defined_function: user_defined_function
    real_gas_nist_mixture: real_gas_nist_mixture
    return_type: str

class premix_laminar_thickness(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class premix_unburnt_temp_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    return_type: str

class premix_unburnt_cp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    return_type: str

class premix_unburnt_density_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    return_type: str

class premix_heat_trans_coeff_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    return_type: str

class path_length(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class absorption_coefficient_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    expression: expression
    path_length: path_length
    gray_band_coefficients: gray_band_coefficients
    user_defined_function: user_defined_function
    return_type: str

class lewis_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_diffusivity_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    polynomial: polynomial
    return_type: str

class species_diffusivity(NamedObject[species_diffusivity_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: species_diffusivity_child
    return_type: str

class multicomponent_child_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    polynomial: polynomial
    return_type: str

class multicomponent_child(NamedObject[multicomponent_child_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: multicomponent_child_child
    return_type: str

class multicomponent(NamedObject[multicomponent_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: multicomponent_child
    return_type: str

class mass_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    lewis_number: lewis_number
    value: value_1
    species_diffusivity: species_diffusivity
    multicomponent: multicomponent
    user_defined_function: user_defined_function
    return_type: str

class volumetric_species_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density
    viscosity: viscosity
    specific_heat: specific_heat
    thermal_conductivity: thermal_conductivity
    molecular_weight: molecular_weight
    premix_laminar_speed: premix_laminar_speed
    premix_critical_strain: premix_critical_strain
    premix_unburnt_temp: premix_unburnt_temp
    premix_unburnt_density: premix_unburnt_density
    premix_heat_trans_coeff: premix_heat_trans_coeff
    premix_heat_of_comb: premix_heat_of_comb
    premix_unburnt_fuel_mf: premix_unburnt_fuel_mf
    premix_adiabatic_temp: premix_adiabatic_temp
    therm_exp_coeff: therm_exp_coeff
    characteristic_vibrational_temperature: characteristic_vibrational_temperature
    absorption_coefficient: absorption_coefficient
    melting_heat: melting_heat
    tsolidus: tsolidus
    tliqidus: tliqidus
    liquidus_slope: liquidus_slope
    partition_coeff: partition_coeff
    eutectic_mf: eutectic_mf
    solid_diffusion: solid_diffusion
    solut_exp_coeff: solut_exp_coeff
    scattering_coefficient: scattering_coefficient
    scattering_phase_function: scattering_phase_function
    refractive_index: refractive_index
    formation_entropy: formation_entropy
    formation_enthalpy: formation_enthalpy
    reference_temperature: reference_temperature
    lennard_jones_length: lennard_jones_length
    lennard_jones_energy: lennard_jones_energy
    thermal_accom_coefficient: thermal_accom_coefficient
    velocity_accom_coefficient: velocity_accom_coefficient
    degrees_of_freedom: degrees_of_freedom
    uds_diffusivity: uds_diffusivity
    electric_conductivity: electric_conductivity
    dual_electric_conductivity: dual_electric_conductivity
    lithium_diffusivity: lithium_diffusivity
    magnetic_permeability: magnetic_permeability
    speed_of_sound: speed_of_sound
    critical_temperature: critical_temperature
    critical_pressure: critical_pressure
    critical_volume: critical_volume
    acentric_factor: acentric_factor
    latent_heat: latent_heat
    saturation_pressure: saturation_pressure
    vaporization_temperature: vaporization_temperature
    charge: charge
    return_type: str

class volumetric_species(NamedObject[volumetric_species_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: volumetric_species_child
    return_type: str

class last_species(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    volumetric_species: volumetric_species
    last_species: last_species
    return_type: str

class reactions_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    return_type: str

class reaction_mechs(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    return_type: str

class thermal_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    species_diffusivity: species_diffusivity
    user_defined_function: user_defined_function
    return_type: str

class tmelt(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class eutectic_temp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class diffusion_collision_integral(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscosity_collision_integral(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class neutral_involved_interaction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    diffusion_collision_integral: diffusion_collision_integral
    viscosity_collision_integral: viscosity_collision_integral
    return_type: str

class charged_particle_interaction(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cross_section_multicomponent_child_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    neutral_involved_interaction: neutral_involved_interaction
    charged_particle_interaction: charged_particle_interaction
    return_type: str

class cross_section_multicomponent_child(NamedObject[cross_section_multicomponent_child_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: cross_section_multicomponent_child_child
    return_type: str

class cross_section_multicomponent(NamedObject[cross_section_multicomponent_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: cross_section_multicomponent_child
    return_type: str

class collision_cross_section(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    cross_section_multicomponent: cross_section_multicomponent
    return_type: str

class mixture_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_2
    viscosity: viscosity_1
    specific_heat: specific_heat_2
    thermal_conductivity: thermal_conductivity_2
    premix_laminar_speed: premix_laminar_speed
    premix_laminar_thickness: premix_laminar_thickness
    premix_unburnt_temp: premix_unburnt_temp_1
    premix_unburnt_cp: premix_unburnt_cp
    premix_unburnt_density: premix_unburnt_density_1
    premix_heat_trans_coeff: premix_heat_trans_coeff_1
    premix_critical_strain: premix_critical_strain
    therm_exp_coeff: therm_exp_coeff
    absorption_coefficient: absorption_coefficient_1
    scattering_coefficient: scattering_coefficient
    scattering_phase_function: scattering_phase_function
    refractive_index: refractive_index
    mass_diffusivity: mass_diffusivity
    species: species_1
    reactions: reactions_1
    reaction_mechs: reaction_mechs
    uds_diffusivity: uds_diffusivity
    thermal_diffusivity: thermal_diffusivity
    tmelt: tmelt
    melting_heat: melting_heat
    eutectic_temp: eutectic_temp
    speed_of_sound: speed_of_sound
    critical_temperature: critical_temperature
    critical_pressure: critical_pressure
    critical_volume: critical_volume
    acentric_factor: acentric_factor
    electric_conductivity: electric_conductivity
    dual_electric_conductivity: dual_electric_conductivity
    lithium_diffusivity: lithium_diffusivity
    collision_cross_section: collision_cross_section
    return_type: str

class mixture(NamedObject[mixture_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mixture_child
    return_type: str

class density_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    compressible_liquid: compressible_liquid
    user_defined_function: user_defined_function
    return_type: str

class specific_heat_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial
    user_defined_function: user_defined_function
    return_type: str

class thermal_conductivity_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class thermophoretic_co(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class scattering_factor(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class emissivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class viscosity_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class dpm_surften(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class electric_conductivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class dual_electric_conductivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class charge_density(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class inert_particle_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_3
    specific_heat: specific_heat_3
    thermal_conductivity: thermal_conductivity_3
    thermophoretic_co: thermophoretic_co
    scattering_factor: scattering_factor
    emissivity: emissivity
    viscosity: viscosity_2
    dpm_surften: dpm_surften
    electric_conductivity: electric_conductivity_1
    dual_electric_conductivity: dual_electric_conductivity_1
    magnetic_permeability: magnetic_permeability
    charge_density: charge_density
    return_type: str

class inert_particle(NamedObject[inert_particle_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: inert_particle_child
    return_type: str

class use_vapor_species_heat_capacity(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diffusion_controlled(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use_vapor_species_heat_capacity: use_vapor_species_heat_capacity
    return_type: str

class variable_lewis_number(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convection_diffusion_controlled(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    variable_lewis_number: variable_lewis_number
    use_vapor_species_heat_capacity: use_vapor_species_heat_capacity
    return_type: str

class vaporization_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    diffusion_controlled: diffusion_controlled
    convection_diffusion_controlled: convection_diffusion_controlled
    return_type: str

class pre_exponential_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class single_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    return_type: str

class particle_thermolysis_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    return_type: str

class film_thermolysis_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    return_type: str

class secondary_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    particle_thermolysis_rate: particle_thermolysis_rate
    film_thermolysis_rate: film_thermolysis_rate
    return_type: str

class thermolysis_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    single_rate: single_rate
    secondary_rate: secondary_rate
    value: value_1
    return_type: str

class latent_heat_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class volatile_fraction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class heat_of_pyrolysis(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class averaging_coefficient(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class binary_diffusivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class film_averaged(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    averaging_coefficient: averaging_coefficient
    binary_diffusivity: binary_diffusivity_1
    return_type: str

class binary_diffusivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    film_averaged: film_averaged
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class diffusivity_reference_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class averaging_coefficient_t(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class averaging_coefficient_y(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class vapor_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    value: value_1
    rgp_table: rgp_table
    user_defined_function: user_defined_function
    return_type: str

class molecular_weight_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class boiling_point(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class scattering_factor_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class emissivity_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class dpm_surften_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    rgp_table: rgp_table
    user_defined_function: user_defined_function
    return_type: str

class droplet_particle_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_3
    thermal_conductivity: thermal_conductivity_3
    vaporization_model: vaporization_model
    thermolysis_model: thermolysis_model
    latent_heat: latent_heat_1
    volatile_fraction: volatile_fraction
    heat_of_pyrolysis: heat_of_pyrolysis
    specific_heat: specific_heat_3
    binary_diffusivity: binary_diffusivity
    diffusivity_reference_pressure: diffusivity_reference_pressure
    averaging_coefficient_t: averaging_coefficient_t
    averaging_coefficient_y: averaging_coefficient_y
    vapor_pressure: vapor_pressure
    molecular_weight: molecular_weight_1
    vaporization_temperature: vaporization_temperature
    boiling_point: boiling_point
    thermophoretic_co: thermophoretic_co
    scattering_factor: scattering_factor_1
    emissivity: emissivity_1
    viscosity: viscosity_2
    dpm_surften: dpm_surften_1
    electric_conductivity: electric_conductivity_1
    dual_electric_conductivity: dual_electric_conductivity_1
    magnetic_permeability: magnetic_permeability
    charge_density: charge_density
    formation_entropy: formation_entropy
    formation_enthalpy: formation_enthalpy
    reference_temperature: reference_temperature
    return_type: str

class droplet_particle(NamedObject[droplet_particle_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: droplet_particle_child
    return_type: str

class density_4(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    piecewise_linear: piecewise_linear
    piecewise_polynomial: piecewise_polynomial
    polynomial: polynomial
    user_defined_function: user_defined_function
    return_type: str

class combustible_fraction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class swelling_coefficient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    user_defined_function: user_defined_function
    return_type: str

class burn_stoichiometry(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class burn_hreact(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class burn_hreact_fraction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    return_type: str

class weighting_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class first_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    weighting_factor: weighting_factor
    return_type: str

class second_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    weighting_factor: weighting_factor
    return_type: str

class two_competing_rates(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    first_rate: first_rate
    second_rate: second_rate
    return_type: str

class initial_fraction_of_bridges_in_coal_lattice(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_fraction_of_char_bridges(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lattice_coordination_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cluster_molecular_weight(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class side_chain_molecular_weight(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cpd_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    initial_fraction_of_bridges_in_coal_lattice: initial_fraction_of_bridges_in_coal_lattice
    initial_fraction_of_char_bridges: initial_fraction_of_char_bridges
    lattice_coordination_number: lattice_coordination_number
    cluster_molecular_weight: cluster_molecular_weight
    side_chain_molecular_weight: side_chain_molecular_weight
    return_type: str

class devolatilization_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    value: value_1
    single_rate: single_rate
    two_competing_rates: two_competing_rates
    cpd_model: cpd_model
    return_type: str

class char_intrinsic_reactivity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class carbon_content_percentage(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cbk(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    char_intrinsic_reactivity: char_intrinsic_reactivity
    carbon_content_percentage: carbon_content_percentage
    return_type: str

class diffusion_rate_constant(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class kinetics_diffusion_limited(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    diffusion_rate_constant: diffusion_rate_constant
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    return_type: str

class char_porosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mean_pore_radius(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class specific_internal_surface_area(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tortuosity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class burning_mode(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class intrinsic_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    diffusion_rate_constant: diffusion_rate_constant
    pre_exponential_factor: pre_exponential_factor
    activation_energy: activation_energy
    char_porosity: char_porosity
    mean_pore_radius: mean_pore_radius
    specific_internal_surface_area: specific_internal_surface_area
    tortuosity: tortuosity
    burning_mode: burning_mode
    return_type: str

class composition_dependent_specific_heat(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class composition_dependent_density(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multiple_surface_reactions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    composition_dependent_specific_heat: composition_dependent_specific_heat
    composition_dependent_density: composition_dependent_density
    return_type: str

class combustion_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    cbk: cbk
    kinetics_diffusion_limited: kinetics_diffusion_limited
    intrinsic_model: intrinsic_model
    multiple_surface_reactions: multiple_surface_reactions
    return_type: str

class combusting_particle_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_4
    thermal_conductivity: thermal_conductivity_3
    latent_heat: latent_heat_1
    volatile_fraction: volatile_fraction
    combustible_fraction: combustible_fraction
    swelling_coefficient: swelling_coefficient
    burn_stoichiometry: burn_stoichiometry
    specific_heat: specific_heat_3
    binary_diffusivity: binary_diffusivity_1
    diffusivity_reference_pressure: diffusivity_reference_pressure
    vaporization_temperature: vaporization_temperature
    thermophoretic_co: thermophoretic_co
    burn_hreact: burn_hreact
    burn_hreact_fraction: burn_hreact_fraction
    devolatilization_model: devolatilization_model
    combustion_model: combustion_model
    scattering_factor: scattering_factor_1
    emissivity: emissivity_1
    return_type: str

class combusting_particle(NamedObject[combusting_particle_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: combusting_particle_child
    return_type: str

class density_5(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    compressible_liquid: compressible_liquid
    user_defined_function: user_defined_function
    value: value_1
    return_type: str

class specific_heat_4(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    value: value_1
    return_type: str

class particle_species_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_3
    thermal_conductivity: thermal_conductivity_3
    vaporization_model: vaporization_model
    thermolysis_model: thermolysis_model
    latent_heat: latent_heat_1
    volatile_fraction: volatile_fraction
    heat_of_pyrolysis: heat_of_pyrolysis
    specific_heat: specific_heat_3
    binary_diffusivity: binary_diffusivity
    diffusivity_reference_pressure: diffusivity_reference_pressure
    averaging_coefficient_t: averaging_coefficient_t
    averaging_coefficient_y: averaging_coefficient_y
    vapor_pressure: vapor_pressure
    molecular_weight: molecular_weight_1
    vaporization_temperature: vaporization_temperature
    boiling_point: boiling_point
    thermophoretic_co: thermophoretic_co
    scattering_factor: scattering_factor_1
    emissivity: emissivity_1
    viscosity: viscosity_2
    dpm_surften: dpm_surften_1
    electric_conductivity: electric_conductivity_1
    dual_electric_conductivity: dual_electric_conductivity_1
    magnetic_permeability: magnetic_permeability
    charge_density: charge_density
    formation_entropy: formation_entropy
    formation_enthalpy: formation_enthalpy
    reference_temperature: reference_temperature
    return_type: str

class particle_species(NamedObject[particle_species_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: particle_species_child
    return_type: str

class species_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    particle_species: particle_species
    last_species: last_species
    return_type: str

class vp_equilib(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    user_defined_function: user_defined_function
    return_type: str

class emissivity_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    return_type: str

class scattering_factor_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    return_type: str

class reaction_model(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_10
    return_type: str

class particle_mixture_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    chemical_formula: chemical_formula
    density: density_5
    specific_heat: specific_heat_4
    species: species_2
    vp_equilib: vp_equilib
    thermal_conductivity: thermal_conductivity_3
    viscosity: viscosity_2
    dpm_surften: dpm_surften
    emissivity: emissivity_2
    scattering_factor: scattering_factor_2
    vaporization_model: vaporization_model
    averaging_coefficient_t: averaging_coefficient_t
    averaging_coefficient_y: averaging_coefficient_y
    thermophoretic_co: thermophoretic_co
    reaction_model: reaction_model
    return_type: str

class particle_mixture(NamedObject[particle_mixture_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: particle_mixture_child
    return_type: str

class materials(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    database: database
    fluid: fluid
    solid: solid
    mixture: mixture
    inert_particle: inert_particle
    droplet_particle: droplet_particle
    combusting_particle: combusting_particle
    particle_mixture: particle_mixture
    def list_materials(self):
        """
        List all locally-stored materials.
        """
    def list_properties(self, name: str):
        """
        List the properties of a locally-stored material.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    return_type: str

class sources(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class profile_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class field_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class udf(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class source_terms_1_child_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class source_terms_1_child(ListObject[source_terms_1_child_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: source_terms_1_child_child
    return_type: str

class source_terms_1(NamedObject[source_terms_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: source_terms_1_child
    return_type: str

class fixed(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cylindrical_fixed_var(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixes_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fixes(NamedObject[fixes_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: fixes_child
    return_type: str

class motion_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relative_to_thread(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class omega(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class axis_origin_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class axis_origin_1(ListObject[axis_origin_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: axis_origin_1_child
    return_type: str

class axis_direction_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class axis_direction_1(ListObject[axis_direction_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: axis_direction_1_child
    return_type: str

class udf_zmotion_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mrf_motion(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mrf_relative_to_thread(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mrf_omega(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class reference_frame_velocity_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class reference_frame_velocity(ListObject[reference_frame_velocity_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: reference_frame_velocity_child
    return_type: str

class reference_frame_axis_origin_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class reference_frame_axis_origin(ListObject[reference_frame_axis_origin_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: reference_frame_axis_origin_child
    return_type: str

class reference_frame_axis_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class reference_frame_axis_direction(ListObject[reference_frame_axis_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: reference_frame_axis_direction_child
    return_type: str

class mrf_udf_zmotion_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mgrid_enable_transient(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mgrid_motion(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mgrid_relative_to_thread(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mgrid_omega(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class moving_mesh_velocity_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class moving_mesh_velocity(ListObject[moving_mesh_velocity_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: moving_mesh_velocity_child
    return_type: str

class moving_mesh_axis_origin_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class moving_mesh_axis_origin(ListObject[moving_mesh_axis_origin_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: moving_mesh_axis_origin_child
    return_type: str

class moving_mesh_axis_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class moving_mesh_axis_direction(ListObject[moving_mesh_axis_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: moving_mesh_axis_direction_child
    return_type: str

class mgrid_udf_zmotion_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_motion(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_relative_to_thread(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_omega(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class solid_motion_velocity_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class solid_motion_velocity(ListObject[solid_motion_velocity_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: solid_motion_velocity_child
    return_type: str

class solid_motion_axis_origin_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class solid_motion_axis_origin(ListObject[solid_motion_axis_origin_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: solid_motion_axis_origin_child
    return_type: str

class solid_motion_axis_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class solid_motion_axis_direction(ListObject[solid_motion_axis_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: solid_motion_axis_direction_child
    return_type: str

class solid_udf_zmotion_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radiating(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_embedded(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class contact_property(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class active_wetsteam_zone(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vapor_phase_realgas(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class laminar(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class laminar_mut_zero(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_embedded_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_embedded_mom_scheme(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_embedded_c_wale(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_embedded_c_smag(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class glass(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class porous(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class conical(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dir_spec_cond(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cursys(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cursys_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class direction_1_x(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_1_y(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_1_z(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_2_x(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_2_y(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_2_z(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class cone_axis_x(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_axis_y(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_axis_z(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_axis_pt_x(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_axis_pt_y(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_axis_pt_z(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cone_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_vel_resistance(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class porous_r_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class porous_r_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class porous_r_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class alt_inertial_form(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class porous_c_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class porous_c_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class porous_c_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class c0(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class c1_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class porosity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class number_of_coeff(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class function_of(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coefficients_1(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minimum_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class piecewise_polynomial_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    minimum: minimum_1
    maximum: maximum_1
    number_of_coeff: number_of_coeff
    coefficients: coefficients_1
    return_type: str

class piecewise_polynomial_1(ListObject[piecewise_polynomial_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: piecewise_polynomial_1_child
    return_type: str

class viscosity_ratio(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class none(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class corey(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stone_1(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stone_2(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_limit_p1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_limit_p2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ref_perm_p1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exp_p1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class res_sat_p1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ref_perm_p2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exp_p2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class res_sat_p2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ref_perm_p3(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exp_p3(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class res_sat_p3(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class capillary_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class max_capillary_pressure(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class van_genuchten_pg(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class van_genuchten_ng(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skjaeveland_nw_pc_coef(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skjaeveland_nw_pc_pwr(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skjaeveland_wet_pc_coef(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skjaeveland_wet_pc_pwr(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class brooks_corey_pe(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class brooks_corey_ng(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class leverett_con_ang(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_tabular_p1(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_table_p1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_satw_p1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_rp_p1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_tabular_p2(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_table_p2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_satw_p2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rel_perm_rp_p2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wetting_phase(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class non_wetting_phase(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class equib_thermal(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class non_equib_thermal(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_material(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class area_density(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class heat_transfer_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fanzone(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_zone_list(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_thickness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_hub_rad(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_tip_rad(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_x_origin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_y_origin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_z_origin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_rot_dir(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_opert_angvel(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_inflection_point(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class limit_flow_fan(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_flow_rate(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_flow_rate(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tan_source_term(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rad_source_term(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axial_source_term(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_axial_source_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_pre_jump(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_curve_fit(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_poly_order(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_ini_flow(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_test_angvel(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_test_temp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_curve_filename(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reaction_mechs_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class react(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_volume_ratio(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class electrolyte(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mp_compressive_beta_max(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mp_boiling_zone(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class numerical_beach(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_id(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_multi_dir(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_damp_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_inlet_bndr(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_fs_level(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_bottom_level(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_dir_ni(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_dir_nj(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_dir_nk(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_damp_len_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_wave_len(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_len_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_start_point(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_end_point(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ni(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nj(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nk(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class xe(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class len(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_dir_list_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    ni: ni
    nj: nj
    nk: nk
    xe: xe
    len: len
    return_type: str

class beach_dir_list(ListObject[beach_dir_list_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: beach_dir_list_child
    return_type: str

class beach_damp_relative(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_damp_resist_lin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class beach_damp_resist(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class porous_structure(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class structure_material(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class anisotropic_spe_diff(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_xx(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_xy(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_xz(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_yx(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_yy(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_yz(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_zx(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_zy(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spe_diff_zz(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    material: material
    sources: sources
    source_terms: source_terms_1
    fixed: fixed
    cylindrical_fixed_var: cylindrical_fixed_var
    fixes: fixes
    motion_spec: motion_spec
    relative_to_thread: relative_to_thread
    omega: omega
    axis_origin: axis_origin_1
    axis_direction: axis_direction_1
    udf_zmotion_name: udf_zmotion_name
    mrf_motion: mrf_motion
    mrf_relative_to_thread: mrf_relative_to_thread
    mrf_omega: mrf_omega
    reference_frame_velocity: reference_frame_velocity
    reference_frame_axis_origin: reference_frame_axis_origin
    reference_frame_axis_direction: reference_frame_axis_direction
    mrf_udf_zmotion_name: mrf_udf_zmotion_name
    mgrid_enable_transient: mgrid_enable_transient
    mgrid_motion: mgrid_motion
    mgrid_relative_to_thread: mgrid_relative_to_thread
    mgrid_omega: mgrid_omega
    moving_mesh_velocity: moving_mesh_velocity
    moving_mesh_axis_origin: moving_mesh_axis_origin
    moving_mesh_axis_direction: moving_mesh_axis_direction
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name
    solid_motion: solid_motion
    solid_relative_to_thread: solid_relative_to_thread
    solid_omega: solid_omega
    solid_motion_velocity: solid_motion_velocity
    solid_motion_axis_origin: solid_motion_axis_origin
    solid_motion_axis_direction: solid_motion_axis_direction
    solid_udf_zmotion_name: solid_udf_zmotion_name
    radiating: radiating
    les_embedded: les_embedded
    contact_property: contact_property
    active_wetsteam_zone: active_wetsteam_zone
    vapor_phase_realgas: vapor_phase_realgas
    laminar: laminar
    laminar_mut_zero: laminar_mut_zero
    les_embedded_spec: les_embedded_spec
    les_embedded_mom_scheme: les_embedded_mom_scheme
    les_embedded_c_wale: les_embedded_c_wale
    les_embedded_c_smag: les_embedded_c_smag
    glass: glass
    porous: porous
    conical: conical
    dir_spec_cond: dir_spec_cond
    cursys: cursys
    cursys_name: cursys_name
    direction_1_x: direction_1_x
    direction_1_y: direction_1_y
    direction_1_z: direction_1_z
    direction_2_x: direction_2_x
    direction_2_y: direction_2_y
    direction_2_z: direction_2_z
    cone_axis_x: cone_axis_x
    cone_axis_y: cone_axis_y
    cone_axis_z: cone_axis_z
    cone_axis_pt_x: cone_axis_pt_x
    cone_axis_pt_y: cone_axis_pt_y
    cone_axis_pt_z: cone_axis_pt_z
    cone_angle: cone_angle
    rel_vel_resistance: rel_vel_resistance
    porous_r_1: porous_r_1
    porous_r_2: porous_r_2
    porous_r_3: porous_r_3
    alt_inertial_form: alt_inertial_form
    porous_c_1: porous_c_1
    porous_c_2: porous_c_2
    porous_c_3: porous_c_3
    c0: c0
    c1: c1_1
    porosity: porosity
    viscosity_ratio: viscosity_ratio
    none: none
    corey: corey
    stone_1: stone_1
    stone_2: stone_2
    rel_perm_limit_p1: rel_perm_limit_p1
    rel_perm_limit_p2: rel_perm_limit_p2
    ref_perm_p1: ref_perm_p1
    exp_p1: exp_p1
    res_sat_p1: res_sat_p1
    ref_perm_p2: ref_perm_p2
    exp_p2: exp_p2
    res_sat_p2: res_sat_p2
    ref_perm_p3: ref_perm_p3
    exp_p3: exp_p3
    res_sat_p3: res_sat_p3
    capillary_pressure: capillary_pressure
    max_capillary_pressure: max_capillary_pressure
    van_genuchten_pg: van_genuchten_pg
    van_genuchten_ng: van_genuchten_ng
    skjaeveland_nw_pc_coef: skjaeveland_nw_pc_coef
    skjaeveland_nw_pc_pwr: skjaeveland_nw_pc_pwr
    skjaeveland_wet_pc_coef: skjaeveland_wet_pc_coef
    skjaeveland_wet_pc_pwr: skjaeveland_wet_pc_pwr
    brooks_corey_pe: brooks_corey_pe
    brooks_corey_ng: brooks_corey_ng
    leverett_con_ang: leverett_con_ang
    rel_perm_tabular_p1: rel_perm_tabular_p1
    rel_perm_table_p1: rel_perm_table_p1
    rel_perm_satw_p1: rel_perm_satw_p1
    rel_perm_rp_p1: rel_perm_rp_p1
    rel_perm_tabular_p2: rel_perm_tabular_p2
    rel_perm_table_p2: rel_perm_table_p2
    rel_perm_satw_p2: rel_perm_satw_p2
    rel_perm_rp_p2: rel_perm_rp_p2
    wetting_phase: wetting_phase
    non_wetting_phase: non_wetting_phase
    equib_thermal: equib_thermal
    non_equib_thermal: non_equib_thermal
    solid_material: solid_material
    area_density: area_density
    heat_transfer_coeff: heat_transfer_coeff
    fanzone: fanzone
    fan_zone_list: fan_zone_list
    fan_thickness: fan_thickness
    fan_hub_rad: fan_hub_rad
    fan_tip_rad: fan_tip_rad
    fan_x_origin: fan_x_origin
    fan_y_origin: fan_y_origin
    fan_z_origin: fan_z_origin
    fan_rot_dir: fan_rot_dir
    fan_opert_angvel: fan_opert_angvel
    fan_inflection_point: fan_inflection_point
    limit_flow_fan: limit_flow_fan
    max_flow_rate: max_flow_rate
    min_flow_rate: min_flow_rate
    tan_source_term: tan_source_term
    rad_source_term: rad_source_term
    axial_source_term: axial_source_term
    fan_axial_source_method: fan_axial_source_method
    fan_pre_jump: fan_pre_jump
    fan_curve_fit: fan_curve_fit
    fan_poly_order: fan_poly_order
    fan_ini_flow: fan_ini_flow
    fan_test_angvel: fan_test_angvel
    fan_test_temp: fan_test_temp
    fan_curve_filename: fan_curve_filename
    reaction_mechs: reaction_mechs_1
    react: react
    surface_volume_ratio: surface_volume_ratio
    electrolyte: electrolyte
    mp_compressive_beta_max: mp_compressive_beta_max
    mp_boiling_zone: mp_boiling_zone
    numerical_beach: numerical_beach
    beach_id: beach_id
    beach_multi_dir: beach_multi_dir
    beach_damp_type: beach_damp_type
    beach_inlet_bndr: beach_inlet_bndr
    beach_fs_level: beach_fs_level
    beach_bottom_level: beach_bottom_level
    beach_dir_ni: beach_dir_ni
    beach_dir_nj: beach_dir_nj
    beach_dir_nk: beach_dir_nk
    beach_damp_len_spec: beach_damp_len_spec
    beach_wave_len: beach_wave_len
    beach_len_factor: beach_len_factor
    beach_start_point: beach_start_point
    beach_end_point: beach_end_point
    beach_dir_list: beach_dir_list
    beach_damp_relative: beach_damp_relative
    beach_damp_resist_lin: beach_damp_resist_lin
    beach_damp_resist: beach_damp_resist
    porous_structure: porous_structure
    structure_material: structure_material
    anisotropic_spe_diff: anisotropic_spe_diff
    spe_diff_xx: spe_diff_xx
    spe_diff_xy: spe_diff_xy
    spe_diff_xz: spe_diff_xz
    spe_diff_yx: spe_diff_yx
    spe_diff_yy: spe_diff_yy
    spe_diff_yz: spe_diff_yz
    spe_diff_zx: spe_diff_zx
    spe_diff_zy: spe_diff_zy
    spe_diff_zz: spe_diff_zz
    return_type: str

class phase(NamedObject[phase_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_child
    return_type: str

class fluid_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase
    name: name_2
    material: material
    sources: sources
    source_terms: source_terms_1
    fixed: fixed
    cylindrical_fixed_var: cylindrical_fixed_var
    fixes: fixes
    motion_spec: motion_spec
    relative_to_thread: relative_to_thread
    omega: omega
    axis_origin: axis_origin_1
    axis_direction: axis_direction_1
    udf_zmotion_name: udf_zmotion_name
    mrf_motion: mrf_motion
    mrf_relative_to_thread: mrf_relative_to_thread
    mrf_omega: mrf_omega
    reference_frame_velocity: reference_frame_velocity
    reference_frame_axis_origin: reference_frame_axis_origin
    reference_frame_axis_direction: reference_frame_axis_direction
    mrf_udf_zmotion_name: mrf_udf_zmotion_name
    mgrid_enable_transient: mgrid_enable_transient
    mgrid_motion: mgrid_motion
    mgrid_relative_to_thread: mgrid_relative_to_thread
    mgrid_omega: mgrid_omega
    moving_mesh_velocity: moving_mesh_velocity
    moving_mesh_axis_origin: moving_mesh_axis_origin
    moving_mesh_axis_direction: moving_mesh_axis_direction
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name
    solid_motion: solid_motion
    solid_relative_to_thread: solid_relative_to_thread
    solid_omega: solid_omega
    solid_motion_velocity: solid_motion_velocity
    solid_motion_axis_origin: solid_motion_axis_origin
    solid_motion_axis_direction: solid_motion_axis_direction
    solid_udf_zmotion_name: solid_udf_zmotion_name
    radiating: radiating
    les_embedded: les_embedded
    contact_property: contact_property
    active_wetsteam_zone: active_wetsteam_zone
    vapor_phase_realgas: vapor_phase_realgas
    laminar: laminar
    laminar_mut_zero: laminar_mut_zero
    les_embedded_spec: les_embedded_spec
    les_embedded_mom_scheme: les_embedded_mom_scheme
    les_embedded_c_wale: les_embedded_c_wale
    les_embedded_c_smag: les_embedded_c_smag
    glass: glass
    porous: porous
    conical: conical
    dir_spec_cond: dir_spec_cond
    cursys: cursys
    cursys_name: cursys_name
    direction_1_x: direction_1_x
    direction_1_y: direction_1_y
    direction_1_z: direction_1_z
    direction_2_x: direction_2_x
    direction_2_y: direction_2_y
    direction_2_z: direction_2_z
    cone_axis_x: cone_axis_x
    cone_axis_y: cone_axis_y
    cone_axis_z: cone_axis_z
    cone_axis_pt_x: cone_axis_pt_x
    cone_axis_pt_y: cone_axis_pt_y
    cone_axis_pt_z: cone_axis_pt_z
    cone_angle: cone_angle
    rel_vel_resistance: rel_vel_resistance
    porous_r_1: porous_r_1
    porous_r_2: porous_r_2
    porous_r_3: porous_r_3
    alt_inertial_form: alt_inertial_form
    porous_c_1: porous_c_1
    porous_c_2: porous_c_2
    porous_c_3: porous_c_3
    c0: c0
    c1: c1_1
    porosity: porosity
    viscosity_ratio: viscosity_ratio
    none: none
    corey: corey
    stone_1: stone_1
    stone_2: stone_2
    rel_perm_limit_p1: rel_perm_limit_p1
    rel_perm_limit_p2: rel_perm_limit_p2
    ref_perm_p1: ref_perm_p1
    exp_p1: exp_p1
    res_sat_p1: res_sat_p1
    ref_perm_p2: ref_perm_p2
    exp_p2: exp_p2
    res_sat_p2: res_sat_p2
    ref_perm_p3: ref_perm_p3
    exp_p3: exp_p3
    res_sat_p3: res_sat_p3
    capillary_pressure: capillary_pressure
    max_capillary_pressure: max_capillary_pressure
    van_genuchten_pg: van_genuchten_pg
    van_genuchten_ng: van_genuchten_ng
    skjaeveland_nw_pc_coef: skjaeveland_nw_pc_coef
    skjaeveland_nw_pc_pwr: skjaeveland_nw_pc_pwr
    skjaeveland_wet_pc_coef: skjaeveland_wet_pc_coef
    skjaeveland_wet_pc_pwr: skjaeveland_wet_pc_pwr
    brooks_corey_pe: brooks_corey_pe
    brooks_corey_ng: brooks_corey_ng
    leverett_con_ang: leverett_con_ang
    rel_perm_tabular_p1: rel_perm_tabular_p1
    rel_perm_table_p1: rel_perm_table_p1
    rel_perm_satw_p1: rel_perm_satw_p1
    rel_perm_rp_p1: rel_perm_rp_p1
    rel_perm_tabular_p2: rel_perm_tabular_p2
    rel_perm_table_p2: rel_perm_table_p2
    rel_perm_satw_p2: rel_perm_satw_p2
    rel_perm_rp_p2: rel_perm_rp_p2
    wetting_phase: wetting_phase
    non_wetting_phase: non_wetting_phase
    equib_thermal: equib_thermal
    non_equib_thermal: non_equib_thermal
    solid_material: solid_material
    area_density: area_density
    heat_transfer_coeff: heat_transfer_coeff
    fanzone: fanzone
    fan_zone_list: fan_zone_list
    fan_thickness: fan_thickness
    fan_hub_rad: fan_hub_rad
    fan_tip_rad: fan_tip_rad
    fan_x_origin: fan_x_origin
    fan_y_origin: fan_y_origin
    fan_z_origin: fan_z_origin
    fan_rot_dir: fan_rot_dir
    fan_opert_angvel: fan_opert_angvel
    fan_inflection_point: fan_inflection_point
    limit_flow_fan: limit_flow_fan
    max_flow_rate: max_flow_rate
    min_flow_rate: min_flow_rate
    tan_source_term: tan_source_term
    rad_source_term: rad_source_term
    axial_source_term: axial_source_term
    fan_axial_source_method: fan_axial_source_method
    fan_pre_jump: fan_pre_jump
    fan_curve_fit: fan_curve_fit
    fan_poly_order: fan_poly_order
    fan_ini_flow: fan_ini_flow
    fan_test_angvel: fan_test_angvel
    fan_test_temp: fan_test_temp
    fan_curve_filename: fan_curve_filename
    reaction_mechs: reaction_mechs_1
    react: react
    surface_volume_ratio: surface_volume_ratio
    electrolyte: electrolyte
    mp_compressive_beta_max: mp_compressive_beta_max
    mp_boiling_zone: mp_boiling_zone
    numerical_beach: numerical_beach
    beach_id: beach_id
    beach_multi_dir: beach_multi_dir
    beach_damp_type: beach_damp_type
    beach_inlet_bndr: beach_inlet_bndr
    beach_fs_level: beach_fs_level
    beach_bottom_level: beach_bottom_level
    beach_dir_ni: beach_dir_ni
    beach_dir_nj: beach_dir_nj
    beach_dir_nk: beach_dir_nk
    beach_damp_len_spec: beach_damp_len_spec
    beach_wave_len: beach_wave_len
    beach_len_factor: beach_len_factor
    beach_start_point: beach_start_point
    beach_end_point: beach_end_point
    beach_dir_list: beach_dir_list
    beach_damp_relative: beach_damp_relative
    beach_damp_resist_lin: beach_damp_resist_lin
    beach_damp_resist: beach_damp_resist
    porous_structure: porous_structure
    structure_material: structure_material
    anisotropic_spe_diff: anisotropic_spe_diff
    spe_diff_xx: spe_diff_xx
    spe_diff_xy: spe_diff_xy
    spe_diff_xz: spe_diff_xz
    spe_diff_yx: spe_diff_yx
    spe_diff_yy: spe_diff_yy
    spe_diff_yz: spe_diff_yz
    spe_diff_zx: spe_diff_zx
    spe_diff_zy: spe_diff_zy
    spe_diff_zz: spe_diff_zz
    return_type: str

class fluid_1(NamedObject[fluid_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: fluid_1_child
    return_type: str

class pcb_model(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ecad_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class choice(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rows(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class columns(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ref_frame(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pwr_names(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pcb_zone_info(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    ecad_name: ecad_name
    choice: choice
    rows: rows
    columns: columns
    ref_frame: ref_frame
    pwr_names: pwr_names
    return_type: str

class phase_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    material: material
    sources: sources
    source_terms: source_terms_1
    fixed: fixed
    cylindrical_fixed_var: cylindrical_fixed_var
    fixes: fixes
    motion_spec: motion_spec
    relative_to_thread: relative_to_thread
    omega: omega
    axis_origin: axis_origin_1
    axis_direction: axis_direction_1
    udf_zmotion_name: udf_zmotion_name
    mrf_motion: mrf_motion
    mrf_relative_to_thread: mrf_relative_to_thread
    mrf_omega: mrf_omega
    reference_frame_velocity: reference_frame_velocity
    reference_frame_axis_origin: reference_frame_axis_origin
    reference_frame_axis_direction: reference_frame_axis_direction
    mrf_udf_zmotion_name: mrf_udf_zmotion_name
    mgrid_enable_transient: mgrid_enable_transient
    mgrid_motion: mgrid_motion
    mgrid_relative_to_thread: mgrid_relative_to_thread
    mgrid_omega: mgrid_omega
    moving_mesh_velocity: moving_mesh_velocity
    moving_mesh_axis_origin: moving_mesh_axis_origin
    moving_mesh_axis_direction: moving_mesh_axis_direction
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name
    solid_motion: solid_motion
    solid_relative_to_thread: solid_relative_to_thread
    solid_omega: solid_omega
    solid_motion_velocity: solid_motion_velocity
    solid_motion_axis_origin: solid_motion_axis_origin
    solid_motion_axis_direction: solid_motion_axis_direction
    solid_udf_zmotion_name: solid_udf_zmotion_name
    radiating: radiating
    les_embedded: les_embedded
    contact_property: contact_property
    active_wetsteam_zone: active_wetsteam_zone
    vapor_phase_realgas: vapor_phase_realgas
    cursys: cursys
    cursys_name: cursys_name
    pcb_model: pcb_model
    pcb_zone_info: pcb_zone_info
    return_type: str

class phase_1(NamedObject[phase_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_1_child
    return_type: str

class solid_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_1
    name: name_2
    material: material
    sources: sources
    source_terms: source_terms_1
    fixed: fixed
    cylindrical_fixed_var: cylindrical_fixed_var
    fixes: fixes
    motion_spec: motion_spec
    relative_to_thread: relative_to_thread
    omega: omega
    axis_origin: axis_origin_1
    axis_direction: axis_direction_1
    udf_zmotion_name: udf_zmotion_name
    mrf_motion: mrf_motion
    mrf_relative_to_thread: mrf_relative_to_thread
    mrf_omega: mrf_omega
    reference_frame_velocity: reference_frame_velocity
    reference_frame_axis_origin: reference_frame_axis_origin
    reference_frame_axis_direction: reference_frame_axis_direction
    mrf_udf_zmotion_name: mrf_udf_zmotion_name
    mgrid_enable_transient: mgrid_enable_transient
    mgrid_motion: mgrid_motion
    mgrid_relative_to_thread: mgrid_relative_to_thread
    mgrid_omega: mgrid_omega
    moving_mesh_velocity: moving_mesh_velocity
    moving_mesh_axis_origin: moving_mesh_axis_origin
    moving_mesh_axis_direction: moving_mesh_axis_direction
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name
    solid_motion: solid_motion
    solid_relative_to_thread: solid_relative_to_thread
    solid_omega: solid_omega
    solid_motion_velocity: solid_motion_velocity
    solid_motion_axis_origin: solid_motion_axis_origin
    solid_motion_axis_direction: solid_motion_axis_direction
    solid_udf_zmotion_name: solid_udf_zmotion_name
    radiating: radiating
    les_embedded: les_embedded
    contact_property: contact_property
    active_wetsteam_zone: active_wetsteam_zone
    vapor_phase_realgas: vapor_phase_realgas
    cursys: cursys
    cursys_name: cursys_name
    pcb_model: pcb_model
    pcb_zone_info: pcb_zone_info
    return_type: str

class solid_1(NamedObject[solid_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: solid_1_child
    return_type: str

class cell_zone_conditions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    fluid: fluid_1
    solid: solid_1
    def copy(self, from_: str, to: list[str], verbosity: bool):
        """
        'copy' command.
        """
    def change_type(self, zone_list: list[str], new_type: str):
        """
        'change_type' command.
        """
    def activate_cell_zone(self, cell_zone_list: list[str]):
        """
        'activate_cell_zone' command.
        """
    def mrf_to_sliding_mesh(self, zone_id: int):
        """
        Change motion specification from MRF to moving mesh.
        
        Parameters
        ----------
            zone_id : int
                'zone_id' child.
        """
    def convert_all_solid_mrf_to_solid_motion(self):
        """
        Change all solid zones motion specification from MRF to solid motion.
        """
    def copy_mrf_to_mesh_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            overwrite : bool
                'overwrite' child.
        """
    def copy_mesh_to_mrf_motion(self, zone_name: str, overwrite: bool):
        """
        Copy motion variable values for origin, axis and velocities from Mesh Motion to Frame Motion.
        
        Parameters
        ----------
            zone_name : str
                'zone_name' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class geom_disable(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geom_dir_spec(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geom_dir_x(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geom_dir_y(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geom_dir_z(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geom_levels(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geom_bgthread(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_2_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class phase_2(NamedObject[phase_2_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_2_child
    return_type: str

class axis_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_2
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class axis(NamedObject[axis_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: axis_child
    return_type: str

class degassing_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_2
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class degassing(NamedObject[degassing_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: degassing_child
    return_type: str

class open_channel(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class outlet_number(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure_spec_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class press_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class frame_of_reference(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ht_local(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class gauge_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class p_profile_multiplier(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ht_bottom(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class den_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class t0(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coordinate_system(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class flow_direction(ListObject[flow_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: flow_direction_child
    return_type: str

class axis_direction_2_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_direction_2(ListObject[axis_direction_2_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: axis_direction_2_child
    return_type: str

class axis_origin_2_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_origin_2(ListObject[axis_origin_2_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: axis_origin_2_child
    return_type: str

class ke_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nut(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class kl(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class intermit(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class k(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class e_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class o(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class v2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class turb_intensity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_length_scale(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_hydraulic_diam(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_viscosity_ratio(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_viscosity_ratio_profile(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class rst_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class uu(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class vv(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ww(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class uv(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class vw(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class uw(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ksgs_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ksgs(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class sgs_turb_intensity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radiation_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radial_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class radial_direction(ListObject[radial_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: radial_direction_child
    return_type: str

class coll_dtheta(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coll_dphi(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class band_q_irrad_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class band_q_irrad(NamedObject[band_q_irrad_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: band_q_irrad_child
    return_type: str

class band_q_irrad_diffuse_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class band_q_irrad_diffuse(NamedObject[band_q_irrad_diffuse_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: band_q_irrad_diffuse_child
    return_type: str

class parallel_collimated_beam(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_direction(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_irradiation(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class t_b_b_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class t_b_b(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class in_emiss(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fmean(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fmean2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fvar(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fvar2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class granular_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class iac(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class lsfun(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class vof_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_fraction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class species_in_mole_fractions(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mf_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class mf(NamedObject[mf_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mf_child
    return_type: str

class elec_potential_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class potential_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class dual_potential_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dual_potential_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class x_displacement_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_displacement_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class y_displacement_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_displacement_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class z_displacement_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_displacement_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class prob_mode_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class prob_mode_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class prob_mode_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class premixc(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class premixc_var(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ecfm_sigma(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class inert(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_no(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hcn(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_nh3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_n2o(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_urea(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hnco(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_nco(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_so2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_h2s(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_so3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_sh(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_so(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_soot(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_nuclei(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_ctar(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hg(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hgcl2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hcl(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hgo(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_cl(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_cl2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hgcl(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pollut_hocl(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class tss_scalar_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class tss_scalar(NamedObject[tss_scalar_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: tss_scalar_child
    return_type: str

class fensapice_flow_bc_subtype(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class uds_bc_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class uds_bc(NamedObject[uds_bc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: uds_bc_child
    return_type: str

class uds_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class uds(NamedObject[uds_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: uds_child
    return_type: str

class pb_disc_bc_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pb_disc_bc(NamedObject[pb_disc_bc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_disc_bc_child
    return_type: str

class pb_disc_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pb_disc(NamedObject[pb_disc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_disc_child
    return_type: str

class pb_qmom_bc_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pb_qmom_bc(NamedObject[pb_qmom_bc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_qmom_bc_child
    return_type: str

class pb_qmom_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pb_qmom(NamedObject[pb_qmom_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_qmom_child
    return_type: str

class pb_qbmm_bc_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pb_qbmm_bc(NamedObject[pb_qbmm_bc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_qbmm_bc_child
    return_type: str

class pb_qbmm_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pb_qbmm(NamedObject[pb_qbmm_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_qbmm_child
    return_type: str

class pb_smm_bc_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pb_smm_bc(NamedObject[pb_smm_bc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_smm_bc_child
    return_type: str

class pb_smm_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pb_smm(NamedObject[pb_smm_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_smm_child
    return_type: str

class pb_dqmom_bc_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pb_dqmom_bc(NamedObject[pb_dqmom_bc_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_dqmom_bc_child
    return_type: str

class pb_dqmom_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pb_dqmom(NamedObject[pb_dqmom_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pb_dqmom_child
    return_type: str

class dpm_bc_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_collision_partner(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reinj_inj(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_udf(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mixing_plane_thread(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ac_options(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p_backflow_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p_backflow_spec_gen(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class impedance_0(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pole(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class amplitude(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class impedance_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pole: pole
    amplitude: amplitude
    return_type: str

class impedance_1(ListObject[impedance_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: impedance_1_child
    return_type: str

class pole_real(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pole_imag(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class amplitude_real(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class amplitude_imag(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class impedance_2_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pole_real: pole_real
    pole_imag: pole_imag
    amplitude_real: amplitude_real
    amplitude_imag: amplitude_imag
    return_type: str

class impedance_2(ListObject[impedance_2_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: impedance_2_child
    return_type: str

class ac_wave(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class prevent_reverse_flow(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radial(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class avg_press_spec(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class press_averaging_method(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class targeted_mf_boundary(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class targeted_mf(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class targeted_mf_pmax(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class targeted_mf_pmin(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class gen_nrbc_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wsf(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wsb(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wsn(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class solar_fluxes(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solar_shining_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radiating_s2s_surface(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class a_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class strength(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class new_fan_definition(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_3_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    outlet_number: outlet_number
    pressure_spec_method: pressure_spec_method
    press_spec: press_spec
    frame_of_reference: frame_of_reference
    phase_spec: phase_spec
    ht_local: ht_local
    gauge_pressure: gauge_pressure
    p_profile_multiplier: p_profile_multiplier
    ht_bottom: ht_bottom
    den_spec: den_spec
    t0: t0
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fmean2: fmean2
    fvar: fvar
    fvar2: fvar2
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    vof_spec: vof_spec
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    ac_options: ac_options
    p_backflow_spec: p_backflow_spec
    p_backflow_spec_gen: p_backflow_spec_gen
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    prevent_reverse_flow: prevent_reverse_flow
    radial: radial
    avg_press_spec: avg_press_spec
    press_averaging_method: press_averaging_method
    targeted_mf_boundary: targeted_mf_boundary
    targeted_mf: targeted_mf
    targeted_mf_pmax: targeted_mf_pmax
    targeted_mf_pmin: targeted_mf_pmin
    gen_nrbc_spec: gen_nrbc_spec
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    a: a_1
    strength: strength
    new_fan_definition: new_fan_definition
    return_type: str

class phase_3(NamedObject[phase_3_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_3_child
    return_type: str

class exhaust_fan_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_3
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    outlet_number: outlet_number
    pressure_spec_method: pressure_spec_method
    press_spec: press_spec
    frame_of_reference: frame_of_reference
    phase_spec: phase_spec
    ht_local: ht_local
    gauge_pressure: gauge_pressure
    p_profile_multiplier: p_profile_multiplier
    ht_bottom: ht_bottom
    den_spec: den_spec
    t0: t0
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fmean2: fmean2
    fvar: fvar
    fvar2: fvar2
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    vof_spec: vof_spec
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    ac_options: ac_options
    p_backflow_spec: p_backflow_spec
    p_backflow_spec_gen: p_backflow_spec_gen
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    prevent_reverse_flow: prevent_reverse_flow
    radial: radial
    avg_press_spec: avg_press_spec
    press_averaging_method: press_averaging_method
    targeted_mf_boundary: targeted_mf_boundary
    targeted_mf: targeted_mf
    targeted_mf_pmax: targeted_mf_pmax
    targeted_mf_pmin: targeted_mf_pmin
    gen_nrbc_spec: gen_nrbc_spec
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    a: a_1
    strength: strength
    new_fan_definition: new_fan_definition
    return_type: str

class exhaust_fan(NamedObject[exhaust_fan_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: exhaust_fan_child
    return_type: str

class porous_jump_turb_wall_treatment(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dir(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class average_dp(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class c_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class limit_range(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class v_min(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class v_max(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class profile_dp(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dp_profile(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class swirl_model(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_vr(RealList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fr(RealList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hub(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class profile_vt(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vt_profile(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class profile_vr(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vr_profile(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class swirl_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_4_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment
    dir: dir
    average_dp: average_dp
    c: c_1
    limit_range: limit_range
    v_min: v_min
    v_max: v_max
    strength: strength
    profile_dp: profile_dp
    dp_profile: dp_profile
    swirl_model: swirl_model
    fan_vr: fan_vr
    fr: fr
    hub: hub
    axis_origin: axis_origin_2
    axis_direction: axis_direction_2
    profile_vt: profile_vt
    vt_profile: vt_profile
    profile_vr: profile_vr
    vr_profile: vr_profile
    swirl_factor: swirl_factor
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    new_fan_definition: new_fan_definition
    return_type: str

class phase_4(NamedObject[phase_4_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_4_child
    return_type: str

class fan_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_4
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment
    dir: dir
    average_dp: average_dp
    c: c_1
    limit_range: limit_range
    v_min: v_min
    v_max: v_max
    strength: strength
    profile_dp: profile_dp
    dp_profile: dp_profile
    swirl_model: swirl_model
    fan_vr: fan_vr
    fr: fr
    hub: hub
    axis_origin: axis_origin_2
    axis_direction: axis_direction_2
    profile_vt: profile_vt
    vt_profile: vt_profile
    profile_vr: profile_vr
    vr_profile: vr_profile
    swirl_factor: swirl_factor
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    new_fan_definition: new_fan_definition
    return_type: str

class fan(NamedObject[fan_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: fan_child
    return_type: str

class geometry_3_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_2
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class geometry_3(NamedObject[geometry_3_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: geometry_3_child
    return_type: str

class inlet_number(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gauge_total_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class flow_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ht_total(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class vmag(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_vector_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class direction_vector(ListObject[direction_vector_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: direction_vector_child
    return_type: str

class les_spec_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rfg_number_of_modes(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vm_number_of_vortices(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vm_streamwise_fluct(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vm_mass_conservation(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stg_scale_limiter_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stg_ti_limiter(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stg_tvr_limiter(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stg_dw_limiter(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volumetric_synthetic_turbulence_generator(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volumetric_synthetic_turbulence_generator_option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volumetric_synthetic_turbulence_generator_option_thickness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class equ_required(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_bccustom(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_lwc(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_dtemp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_ddiam(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_dv(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_dx(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_dy(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_dz(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_dpm_surface_injection(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_dpm_inj_nstream(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_icc(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_ctemp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_cmelt(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_cdiam(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_cv(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_cx(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_cy(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_cz(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_vrh(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_vrh_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_vc(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class b_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class phase_5_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    frame_of_reference: frame_of_reference
    gauge_total_pressure: gauge_total_pressure
    gauge_pressure: gauge_pressure
    t0: t0
    direction_spec: direction_spec
    flow_spec: flow_spec
    ht_local: ht_local
    ht_total: ht_total
    vmag: vmag
    ht_bottom: ht_bottom
    den_spec: den_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    prevent_reverse_flow: prevent_reverse_flow
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    b: b_1
    strength: strength
    return_type: str

class phase_5(NamedObject[phase_5_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_5_child
    return_type: str

class inlet_vent_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_5
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    frame_of_reference: frame_of_reference
    gauge_total_pressure: gauge_total_pressure
    gauge_pressure: gauge_pressure
    t0: t0
    direction_spec: direction_spec
    flow_spec: flow_spec
    ht_local: ht_local
    ht_total: ht_total
    vmag: vmag
    ht_bottom: ht_bottom
    den_spec: den_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    prevent_reverse_flow: prevent_reverse_flow
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    b: b_1
    strength: strength
    return_type: str

class inlet_vent(NamedObject[inlet_vent_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: inlet_vent_child
    return_type: str

class fan_omega(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_origin_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fan_origin(ListObject[fan_origin_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: fan_origin_child
    return_type: str

class phase_6_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    frame_of_reference: frame_of_reference
    gauge_total_pressure: gauge_total_pressure
    gauge_pressure: gauge_pressure
    t0: t0
    direction_spec: direction_spec
    flow_spec: flow_spec
    ht_local: ht_local
    ht_total: ht_total
    vmag: vmag
    ht_bottom: ht_bottom
    den_spec: den_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    prevent_reverse_flow: prevent_reverse_flow
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    a: a_1
    swirl_model: swirl_model
    swirl_factor: swirl_factor
    fan_omega: fan_omega
    fan_origin: fan_origin
    strength: strength
    new_fan_definition: new_fan_definition
    return_type: str

class phase_6(NamedObject[phase_6_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_6_child
    return_type: str

class intake_fan_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_6
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    frame_of_reference: frame_of_reference
    gauge_total_pressure: gauge_total_pressure
    gauge_pressure: gauge_pressure
    t0: t0
    direction_spec: direction_spec
    flow_spec: flow_spec
    ht_local: ht_local
    ht_total: ht_total
    vmag: vmag
    ht_bottom: ht_bottom
    den_spec: den_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    prevent_reverse_flow: prevent_reverse_flow
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    a: a_1
    swirl_model: swirl_model
    swirl_factor: swirl_factor
    fan_omega: fan_omega
    fan_origin: fan_origin
    strength: strength
    new_fan_definition: new_fan_definition
    return_type: str

class intake_fan(NamedObject[intake_fan_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: intake_fan_child
    return_type: str

class non_overlap_zone_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_7_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    non_overlap_zone_name: non_overlap_zone_name
    return_type: str

class phase_7(NamedObject[phase_7_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_7_child
    return_type: str

class interface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_7
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    non_overlap_zone_name: non_overlap_zone_name
    return_type: str

class interface(NamedObject[interface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: interface_child
    return_type: str

class is_not_a_rans_les_interface(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_8_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    is_not_a_rans_les_interface: is_not_a_rans_les_interface
    return_type: str

class phase_8(NamedObject[phase_8_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_8_child
    return_type: str

class interior_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_8
    name: name_2
    is_not_a_rans_les_interface: is_not_a_rans_les_interface
    return_type: str

class interior(NamedObject[interior_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: interior_child
    return_type: str

class mass_flow(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ec_mass_flow(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class mass_flux(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class mass_flux_ave(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tref(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pref(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class upstream_torque(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class upstream_t_enthalpy(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class slip_velocity(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity_ratio(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class volume_frac(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class phase_9_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    ht_local: ht_local
    ht_bottom: ht_bottom
    den_spec: den_spec
    frame_of_reference: frame_of_reference
    flow_spec: flow_spec
    mass_flow: mass_flow
    ec_mass_flow: ec_mass_flow
    mass_flux: mass_flux
    mass_flux_ave: mass_flux_ave
    tref: tref
    pref: pref
    upstream_torque: upstream_torque
    upstream_t_enthalpy: upstream_t_enthalpy
    t0: t0
    gauge_pressure: gauge_pressure
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    swirl_model: swirl_model
    swirl_factor: swirl_factor
    fan_origin: fan_origin
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    tss_scalar: tss_scalar
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    slip_velocity: slip_velocity
    velocity_ratio: velocity_ratio
    volume_frac: volume_frac
    granular_temperature: granular_temperature
    iac: iac
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    return_type: str

class phase_9(NamedObject[phase_9_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_9_child
    return_type: str

class mass_flow_inlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_9
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    ht_local: ht_local
    ht_bottom: ht_bottom
    den_spec: den_spec
    frame_of_reference: frame_of_reference
    flow_spec: flow_spec
    mass_flow: mass_flow
    ec_mass_flow: ec_mass_flow
    mass_flux: mass_flux
    mass_flux_ave: mass_flux_ave
    tref: tref
    pref: pref
    upstream_torque: upstream_torque
    upstream_t_enthalpy: upstream_t_enthalpy
    t0: t0
    gauge_pressure: gauge_pressure
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    swirl_model: swirl_model
    swirl_factor: swirl_factor
    fan_origin: fan_origin
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    tss_scalar: tss_scalar
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    slip_velocity: slip_velocity
    velocity_ratio: velocity_ratio
    volume_frac: volume_frac
    granular_temperature: granular_temperature
    iac: iac
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    return_type: str

class mass_flow_inlet(NamedObject[mass_flow_inlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mass_flow_inlet_child
    return_type: str

class mass_flow_outlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_9
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    ht_local: ht_local
    ht_bottom: ht_bottom
    den_spec: den_spec
    frame_of_reference: frame_of_reference
    flow_spec: flow_spec
    mass_flow: mass_flow
    ec_mass_flow: ec_mass_flow
    mass_flux: mass_flux
    mass_flux_ave: mass_flux_ave
    tref: tref
    pref: pref
    upstream_torque: upstream_torque
    upstream_t_enthalpy: upstream_t_enthalpy
    t0: t0
    gauge_pressure: gauge_pressure
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    swirl_model: swirl_model
    swirl_factor: swirl_factor
    fan_origin: fan_origin
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    tss_scalar: tss_scalar
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    slip_velocity: slip_velocity
    velocity_ratio: velocity_ratio
    volume_frac: volume_frac
    granular_temperature: granular_temperature
    iac: iac
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    return_type: str

class mass_flow_outlet(NamedObject[mass_flow_outlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mass_flow_outlet_child
    return_type: str

class phase_10_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    return_type: str

class phase_10(NamedObject[phase_10_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_10_child
    return_type: str

class network_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_10
    name: name_2
    return_type: str

class network(NamedObject[network_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: network_child
    return_type: str

class thermal_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class q(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class phase_11_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    thermal_bc: thermal_bc
    temperature: temperature_1
    q: q
    return_type: str

class phase_11(NamedObject[phase_11_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_11_child
    return_type: str

class network_end_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_11
    name: name_2
    thermal_bc: thermal_bc
    temperature: temperature_1
    q: q
    return_type: str

class network_end(NamedObject[network_end_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: network_end_child
    return_type: str

class flowrate_frac(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_12_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    flowrate_frac: flowrate_frac
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    uds_bc: uds_bc
    uds: uds
    radiation_bc: radiation_bc
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    return_type: str

class phase_12(NamedObject[phase_12_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_12_child
    return_type: str

class outflow_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_12
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    flowrate_frac: flowrate_frac
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    uds_bc: uds_bc
    uds: uds
    radiation_bc: radiation_bc
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    return_type: str

class outflow(NamedObject[outflow_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: outflow_child
    return_type: str

class phase_13_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    outlet_number: outlet_number
    pressure_spec_method: pressure_spec_method
    press_spec: press_spec
    frame_of_reference: frame_of_reference
    phase_spec: phase_spec
    ht_local: ht_local
    gauge_pressure: gauge_pressure
    p_profile_multiplier: p_profile_multiplier
    ht_bottom: ht_bottom
    den_spec: den_spec
    t0: t0
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fmean2: fmean2
    fvar: fvar
    fvar2: fvar2
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    vof_spec: vof_spec
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    ac_options: ac_options
    p_backflow_spec: p_backflow_spec
    p_backflow_spec_gen: p_backflow_spec_gen
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    prevent_reverse_flow: prevent_reverse_flow
    radial: radial
    avg_press_spec: avg_press_spec
    press_averaging_method: press_averaging_method
    targeted_mf_boundary: targeted_mf_boundary
    targeted_mf: targeted_mf
    targeted_mf_pmax: targeted_mf_pmax
    targeted_mf_pmin: targeted_mf_pmin
    gen_nrbc_spec: gen_nrbc_spec
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    b: b_1
    strength: strength
    return_type: str

class phase_13(NamedObject[phase_13_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_13_child
    return_type: str

class outlet_vent_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_13
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    outlet_number: outlet_number
    pressure_spec_method: pressure_spec_method
    press_spec: press_spec
    frame_of_reference: frame_of_reference
    phase_spec: phase_spec
    ht_local: ht_local
    gauge_pressure: gauge_pressure
    p_profile_multiplier: p_profile_multiplier
    ht_bottom: ht_bottom
    den_spec: den_spec
    t0: t0
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fmean2: fmean2
    fvar: fvar
    fvar2: fvar2
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    vof_spec: vof_spec
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    ac_options: ac_options
    p_backflow_spec: p_backflow_spec
    p_backflow_spec_gen: p_backflow_spec_gen
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    prevent_reverse_flow: prevent_reverse_flow
    radial: radial
    avg_press_spec: avg_press_spec
    press_averaging_method: press_averaging_method
    targeted_mf_boundary: targeted_mf_boundary
    targeted_mf: targeted_mf
    targeted_mf_pmax: targeted_mf_pmax
    targeted_mf_pmin: targeted_mf_pmin
    gen_nrbc_spec: gen_nrbc_spec
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    b: b_1
    strength: strength
    return_type: str

class outlet_vent(NamedObject[outlet_vent_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: outlet_vent_child
    return_type: str

class overset_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_2
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class overset(NamedObject[overset_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: overset_child
    return_type: str

class angular(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p_jump(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ai(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aj(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ak(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_origin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_origin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_origin(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class shift_x(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class shift_y(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class shift_z(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class per_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_14_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    angular: angular
    p_jump: p_jump
    ai: ai
    aj: aj
    ak: ak
    x_origin: x_origin
    y_origin: y_origin
    z_origin: z_origin
    shift_x: shift_x
    shift_y: shift_y
    shift_z: shift_z
    per_angle: per_angle
    return_type: str

class phase_14(NamedObject[phase_14_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_14_child
    return_type: str

class periodic_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_14
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    angular: angular
    p_jump: p_jump
    ai: ai
    aj: aj
    ak: ak
    x_origin: x_origin
    y_origin: y_origin
    z_origin: z_origin
    shift_x: shift_x
    shift_y: shift_y
    shift_z: shift_z
    per_angle: per_angle
    return_type: str

class periodic(NamedObject[periodic_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: periodic_child
    return_type: str

class alpha(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dm(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class c2_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thermal_ctk(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class v_absp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ir_absp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ir_trans(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class v_trans(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class jump_adhesion(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class adhesion_constrained(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class adhesion_angle_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class adhesion_angle(NamedObject[adhesion_angle_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: adhesion_angle_child
    return_type: str

class phase_15_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment
    alpha: alpha
    dm: dm
    c2: c2_1
    thermal_ctk: thermal_ctk
    solar_fluxes: solar_fluxes
    v_absp: v_absp
    ir_absp: ir_absp
    ir_trans: ir_trans
    v_trans: v_trans
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    strength: strength
    jump_adhesion: jump_adhesion
    adhesion_constrained: adhesion_constrained
    adhesion_angle: adhesion_angle
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    return_type: str

class phase_15(NamedObject[phase_15_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_15_child
    return_type: str

class porous_jump_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_15
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment
    alpha: alpha
    dm: dm
    c2: c2_1
    thermal_ctk: thermal_ctk
    solar_fluxes: solar_fluxes
    v_absp: v_absp
    ir_absp: ir_absp
    ir_trans: ir_trans
    v_trans: v_trans
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    strength: strength
    jump_adhesion: jump_adhesion
    adhesion_constrained: adhesion_constrained
    adhesion_angle: adhesion_angle
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    return_type: str

class porous_jump(NamedObject[porous_jump_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: porous_jump_child
    return_type: str

class m(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class t(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class non_equil_boundary(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tve(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ni_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class nj_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class nk_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class phase_16_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    gauge_pressure: gauge_pressure
    m: m
    t: t
    non_equil_boundary: non_equil_boundary
    tve: tve
    coordinate_system: coordinate_system
    ni: ni_1
    nj: nj_1
    nk: nk_1
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    uds_bc: uds_bc
    uds: uds
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    return_type: str

class phase_16(NamedObject[phase_16_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_16_child
    return_type: str

class pressure_far_field_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_16
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    gauge_pressure: gauge_pressure
    m: m
    t: t
    non_equil_boundary: non_equil_boundary
    tve: tve
    coordinate_system: coordinate_system
    ni: ni_1
    nj: nj_1
    nk: nk_1
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    uds_bc: uds_bc
    uds: uds
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    return_type: str

class pressure_far_field(NamedObject[pressure_far_field_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pressure_far_field_child
    return_type: str

class phase_17_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    frame_of_reference: frame_of_reference
    gauge_total_pressure: gauge_total_pressure
    gauge_pressure: gauge_pressure
    t0: t0
    direction_spec: direction_spec
    flow_spec: flow_spec
    ht_local: ht_local
    ht_total: ht_total
    vmag: vmag
    ht_bottom: ht_bottom
    den_spec: den_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    prevent_reverse_flow: prevent_reverse_flow
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    return_type: str

class phase_17(NamedObject[phase_17_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_17_child
    return_type: str

class pressure_inlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_17
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    inlet_number: inlet_number
    phase_spec: phase_spec
    frame_of_reference: frame_of_reference
    gauge_total_pressure: gauge_total_pressure
    gauge_pressure: gauge_pressure
    t0: t0
    direction_spec: direction_spec
    flow_spec: flow_spec
    ht_local: ht_local
    ht_total: ht_total
    vmag: vmag
    ht_bottom: ht_bottom
    den_spec: den_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    prevent_reverse_flow: prevent_reverse_flow
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    return_type: str

class pressure_inlet(NamedObject[pressure_inlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pressure_inlet_child
    return_type: str

class phase_18_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    outlet_number: outlet_number
    pressure_spec_method: pressure_spec_method
    press_spec: press_spec
    frame_of_reference: frame_of_reference
    phase_spec: phase_spec
    ht_local: ht_local
    gauge_pressure: gauge_pressure
    p_profile_multiplier: p_profile_multiplier
    ht_bottom: ht_bottom
    den_spec: den_spec
    t0: t0
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fmean2: fmean2
    fvar: fvar
    fvar2: fvar2
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    vof_spec: vof_spec
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    ac_options: ac_options
    p_backflow_spec: p_backflow_spec
    p_backflow_spec_gen: p_backflow_spec_gen
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    prevent_reverse_flow: prevent_reverse_flow
    radial: radial
    avg_press_spec: avg_press_spec
    press_averaging_method: press_averaging_method
    targeted_mf_boundary: targeted_mf_boundary
    targeted_mf: targeted_mf
    targeted_mf_pmax: targeted_mf_pmax
    targeted_mf_pmin: targeted_mf_pmin
    gen_nrbc_spec: gen_nrbc_spec
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    return_type: str

class phase_18(NamedObject[phase_18_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_18_child
    return_type: str

class pressure_outlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_18
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel: open_channel
    outlet_number: outlet_number
    pressure_spec_method: pressure_spec_method
    press_spec: press_spec
    frame_of_reference: frame_of_reference
    phase_spec: phase_spec
    ht_local: ht_local
    gauge_pressure: gauge_pressure
    p_profile_multiplier: p_profile_multiplier
    ht_bottom: ht_bottom
    den_spec: den_spec
    t0: t0
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fmean2: fmean2
    fvar: fvar
    fvar2: fvar2
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    vof_spec: vof_spec
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    tss_scalar: tss_scalar
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    mixing_plane_thread: mixing_plane_thread
    ac_options: ac_options
    p_backflow_spec: p_backflow_spec
    p_backflow_spec_gen: p_backflow_spec_gen
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    prevent_reverse_flow: prevent_reverse_flow
    radial: radial
    avg_press_spec: avg_press_spec
    press_averaging_method: press_averaging_method
    targeted_mf_boundary: targeted_mf_boundary
    targeted_mf: targeted_mf
    targeted_mf_pmax: targeted_mf_pmax
    targeted_mf_pmin: targeted_mf_pmin
    gen_nrbc_spec: gen_nrbc_spec
    wsf: wsf
    wsb: wsb
    wsn: wsn
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    return_type: str

class pressure_outlet(NamedObject[pressure_outlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: pressure_outlet_child
    return_type: str

class kc(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class hc(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class t_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class q_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_19_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment
    kc: kc
    hc: hc
    t: t_1
    q: q_1
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    strength: strength
    return_type: str

class phase_19(NamedObject[phase_19_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_19_child
    return_type: str

class radiator_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_19
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment
    kc: kc
    hc: hc
    t: t_1
    q: q_1
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    strength: strength
    return_type: str

class radiator(NamedObject[radiator_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: radiator_child
    return_type: str

class vm_nvortices(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class les_embedded_fluctuations(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_20_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_nvortices: vm_nvortices
    les_embedded_fluctuations: les_embedded_fluctuations
    return_type: str

class phase_20(NamedObject[phase_20_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_20_child
    return_type: str

class rans_les_interface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_20
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_nvortices: vm_nvortices
    les_embedded_fluctuations: les_embedded_fluctuations
    return_type: str

class rans_les_interface(NamedObject[rans_les_interface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: rans_les_interface_child
    return_type: str

class pid(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class temperature_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_rise(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class heat_source(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class tinf(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mass_flow_multiplier_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class mass_flow_multiplier(NamedObject[mass_flow_multiplier_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mass_flow_multiplier_child
    return_type: str

class phase_21_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    pid: pid
    temperature_spec: temperature_spec
    temperature_rise: temperature_rise
    heat_source: heat_source
    tinf: tinf
    hc: hc
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    mass_flow_multiplier: mass_flow_multiplier
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    return_type: str

class phase_21(NamedObject[phase_21_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_21_child
    return_type: str

class recirculation_inlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_21
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    pid: pid
    temperature_spec: temperature_spec
    temperature_rise: temperature_rise
    heat_source: heat_source
    tinf: tinf
    hc: hc
    direction_spec: direction_spec
    coordinate_system: coordinate_system
    flow_direction: flow_direction
    direction_vector: direction_vector
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    mass_flow_multiplier: mass_flow_multiplier
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    return_type: str

class recirculation_inlet(NamedObject[recirculation_inlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: recirculation_inlet_child
    return_type: str

class phase_22_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    flow_spec: flow_spec
    mass_flow: mass_flow
    mass_flux: mass_flux
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    return_type: str

class phase_22(NamedObject[phase_22_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_22_child
    return_type: str

class recirculation_outlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_22
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    flow_spec: flow_spec
    mass_flow: mass_flow
    mass_flux: mass_flux
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    return_type: str

class recirculation_outlet(NamedObject[recirculation_outlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: recirculation_outlet_child
    return_type: str

class shadow_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_2
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class shadow(NamedObject[shadow_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: shadow_child
    return_type: str

class symmetry_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_2
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    return_type: str

class symmetry(NamedObject[symmetry_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: symmetry_child
    return_type: str

class open_channel_wave_bc(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ocw_vel_segregated(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_velocity_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class avg_flow_velocity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ocw_ship_vel_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ocw_ship_vmag(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class moving_object_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class moving_object_direction(ListObject[moving_object_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: moving_object_direction_child
    return_type: str

class ocw_sp_vel_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ocw_sp_vmag(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class secondary_phase_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class secondary_phase_direction(ListObject[secondary_phase_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: secondary_phase_direction_child
    return_type: str

class ocw_pp_vel_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ocw_pp_ref_ht(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ocw_pp_power_coeff(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ocw_pp_vmag(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ocw_pp_vmag_ref(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class primary_phase_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class primary_phase_direction(ListObject[primary_phase_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: primary_phase_direction_child
    return_type: str

class initial_gauge_pressure(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class velocity_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class velocity_1(ListObject[velocity_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: velocity_1_child
    return_type: str

class omega_swirl(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_bc_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_dir_spec(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class reference_direction(ListObject[reference_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: reference_direction_child
    return_type: str

class wave_modeling_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class theory(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_ht(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_len(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class phase_diff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class heading_angle(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_list_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    theory: theory
    wave_ht: wave_ht
    wave_len: wave_len
    phase_diff: phase_diff
    heading_angle: heading_angle
    return_type: str

class wave_list(ListObject[wave_list_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: wave_list_child
    return_type: str

class offset_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_list_shallow_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    theory: theory
    wave_ht: wave_ht
    wave_len: wave_len
    offset: offset_1
    heading_angle: heading_angle
    return_type: str

class wave_list_shallow(ListObject[wave_list_shallow_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: wave_list_shallow_child
    return_type: str

class wave_spect_method_freq(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_spect_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_spect_sig_wave_ht(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_spect_peak_freq(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_spect_min_freq(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_spect_max_freq(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_spect_freq_components(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_spect_method_dir(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_spect_s(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wave_spect_mean_angle(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_spect_deviation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wave_spect_dir_components(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mean_and_std_deviation(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pb_disc_components_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class pb_disc_components(ListObject[pb_disc_components_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: pb_disc_components_child
    return_type: str

class pb_disc_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    mean_and_std_deviation: mean_and_std_deviation
    pb_disc_components: pb_disc_components
    return_type: str

class phase_23_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel_wave_bc: open_channel_wave_bc
    ocw_vel_segregated: ocw_vel_segregated
    velocity_spec: velocity_spec
    frame_of_reference: frame_of_reference
    vmag: vmag
    wave_velocity_spec: wave_velocity_spec
    avg_flow_velocity: avg_flow_velocity
    ocw_ship_vel_spec: ocw_ship_vel_spec
    ocw_ship_vmag: ocw_ship_vmag
    moving_object_direction: moving_object_direction
    ocw_sp_vel_spec: ocw_sp_vel_spec
    ocw_sp_vmag: ocw_sp_vmag
    secondary_phase_direction: secondary_phase_direction
    ocw_pp_vel_spec: ocw_pp_vel_spec
    ocw_pp_ref_ht: ocw_pp_ref_ht
    ocw_pp_power_coeff: ocw_pp_power_coeff
    ocw_pp_vmag: ocw_pp_vmag
    ocw_pp_vmag_ref: ocw_pp_vmag_ref
    primary_phase_direction: primary_phase_direction
    initial_gauge_pressure: initial_gauge_pressure
    coordinate_system: coordinate_system
    velocity: velocity_1
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    omega_swirl: omega_swirl
    phase_spec: phase_spec
    wave_bc_type: wave_bc_type
    ht_local: ht_local
    ht_bottom: ht_bottom
    wave_dir_spec: wave_dir_spec
    reference_direction: reference_direction
    wave_modeling_type: wave_modeling_type
    wave_list: wave_list
    wave_list_shallow: wave_list_shallow
    wave_spect_method_freq: wave_spect_method_freq
    wave_spect_factor: wave_spect_factor
    wave_spect_sig_wave_ht: wave_spect_sig_wave_ht
    wave_spect_peak_freq: wave_spect_peak_freq
    wave_spect_min_freq: wave_spect_min_freq
    wave_spect_max_freq: wave_spect_max_freq
    wave_spect_freq_components: wave_spect_freq_components
    wave_spect_method_dir: wave_spect_method_dir
    wave_spect_s: wave_spect_s
    wave_spect_mean_angle: wave_spect_mean_angle
    wave_spect_deviation: wave_spect_deviation
    wave_spect_dir_components: wave_spect_dir_components
    t: t
    non_equil_boundary: non_equil_boundary
    tve: tve
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc_1
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    gauge_pressure: gauge_pressure
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    return_type: str

class phase_23(NamedObject[phase_23_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_23_child
    return_type: str

class velocity_inlet_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_23
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    open_channel_wave_bc: open_channel_wave_bc
    ocw_vel_segregated: ocw_vel_segregated
    velocity_spec: velocity_spec
    frame_of_reference: frame_of_reference
    vmag: vmag
    wave_velocity_spec: wave_velocity_spec
    avg_flow_velocity: avg_flow_velocity
    ocw_ship_vel_spec: ocw_ship_vel_spec
    ocw_ship_vmag: ocw_ship_vmag
    moving_object_direction: moving_object_direction
    ocw_sp_vel_spec: ocw_sp_vel_spec
    ocw_sp_vmag: ocw_sp_vmag
    secondary_phase_direction: secondary_phase_direction
    ocw_pp_vel_spec: ocw_pp_vel_spec
    ocw_pp_ref_ht: ocw_pp_ref_ht
    ocw_pp_power_coeff: ocw_pp_power_coeff
    ocw_pp_vmag: ocw_pp_vmag
    ocw_pp_vmag_ref: ocw_pp_vmag_ref
    primary_phase_direction: primary_phase_direction
    initial_gauge_pressure: initial_gauge_pressure
    coordinate_system: coordinate_system
    velocity: velocity_1
    flow_direction: flow_direction
    axis_direction: axis_direction_2
    axis_origin: axis_origin_2
    omega_swirl: omega_swirl
    phase_spec: phase_spec
    wave_bc_type: wave_bc_type
    ht_local: ht_local
    ht_bottom: ht_bottom
    wave_dir_spec: wave_dir_spec
    reference_direction: reference_direction
    wave_modeling_type: wave_modeling_type
    wave_list: wave_list
    wave_list_shallow: wave_list_shallow
    wave_spect_method_freq: wave_spect_method_freq
    wave_spect_factor: wave_spect_factor
    wave_spect_sig_wave_ht: wave_spect_sig_wave_ht
    wave_spect_peak_freq: wave_spect_peak_freq
    wave_spect_min_freq: wave_spect_min_freq
    wave_spect_max_freq: wave_spect_max_freq
    wave_spect_freq_components: wave_spect_freq_components
    wave_spect_method_dir: wave_spect_method_dir
    wave_spect_s: wave_spect_s
    wave_spect_mean_angle: wave_spect_mean_angle
    wave_spect_deviation: wave_spect_deviation
    wave_spect_dir_components: wave_spect_dir_components
    t: t
    non_equil_boundary: non_equil_boundary
    tve: tve
    les_spec_name: les_spec_name
    rfg_number_of_modes: rfg_number_of_modes
    vm_number_of_vortices: vm_number_of_vortices
    vm_streamwise_fluct: vm_streamwise_fluct
    vm_mass_conservation: vm_mass_conservation
    stg_scale_limiter_type: stg_scale_limiter_type
    stg_ti_limiter: stg_ti_limiter
    stg_tvr_limiter: stg_tvr_limiter
    stg_dw_limiter: stg_dw_limiter
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness
    ke_spec: ke_spec
    nut: nut
    kl: kl
    intermit: intermit
    k: k
    e: e_1
    o: o
    v2: v2
    turb_intensity: turb_intensity
    turb_length_scale: turb_length_scale
    turb_hydraulic_diam: turb_hydraulic_diam
    turb_viscosity_ratio: turb_viscosity_ratio
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile
    rst_spec: rst_spec
    uu: uu
    vv: vv
    ww: ww
    uv: uv
    vw: vw
    uw: uw
    ksgs_spec: ksgs_spec
    ksgs: ksgs
    sgs_turb_intensity: sgs_turb_intensity
    granular_temperature: granular_temperature
    iac: iac
    lsfun: lsfun
    volume_fraction: volume_fraction
    species_in_mole_fractions: species_in_mole_fractions
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    prob_mode_1: prob_mode_1
    prob_mode_2: prob_mode_2
    prob_mode_3: prob_mode_3
    equ_required: equ_required
    uds_bc: uds_bc
    uds: uds
    pb_disc_bc: pb_disc_bc
    pb_disc: pb_disc_1
    pb_qmom_bc: pb_qmom_bc
    pb_qmom: pb_qmom
    pb_qbmm_bc: pb_qbmm_bc
    pb_qbmm: pb_qbmm
    pb_smm_bc: pb_smm_bc
    pb_smm: pb_smm
    pb_dqmom_bc: pb_dqmom_bc
    pb_dqmom: pb_dqmom
    gauge_pressure: gauge_pressure
    premixc: premixc
    premixc_var: premixc_var
    ecfm_sigma: ecfm_sigma
    inert: inert
    pollut_no: pollut_no
    pollut_hcn: pollut_hcn
    pollut_nh3: pollut_nh3
    pollut_n2o: pollut_n2o
    pollut_urea: pollut_urea
    pollut_hnco: pollut_hnco
    pollut_nco: pollut_nco
    pollut_so2: pollut_so2
    pollut_h2s: pollut_h2s
    pollut_so3: pollut_so3
    pollut_sh: pollut_sh
    pollut_so: pollut_so
    pollut_soot: pollut_soot
    pollut_nuclei: pollut_nuclei
    pollut_ctar: pollut_ctar
    pollut_hg: pollut_hg
    pollut_hgcl2: pollut_hgcl2
    pollut_hcl: pollut_hcl
    pollut_hgo: pollut_hgo
    pollut_cl: pollut_cl
    pollut_cl2: pollut_cl2
    pollut_hgcl: pollut_hgcl
    pollut_hocl: pollut_hocl
    radiation_bc: radiation_bc
    radial_direction: radial_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    parallel_collimated_beam: parallel_collimated_beam
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    t_b_b_spec: t_b_b_spec
    t_b_b: t_b_b
    in_emiss: in_emiss
    fmean: fmean
    fvar: fvar
    fmean2: fmean2
    fvar2: fvar2
    tss_scalar: tss_scalar
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_udf: dpm_bc_udf
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_drop_bccustom: fensapice_drop_bccustom
    fensapice_drop_lwc: fensapice_drop_lwc
    fensapice_drop_dtemp: fensapice_drop_dtemp
    fensapice_drop_ddiam: fensapice_drop_ddiam
    fensapice_drop_dv: fensapice_drop_dv
    fensapice_drop_dx: fensapice_drop_dx
    fensapice_drop_dy: fensapice_drop_dy
    fensapice_drop_dz: fensapice_drop_dz
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream
    fensapice_drop_icc: fensapice_drop_icc
    fensapice_drop_ctemp: fensapice_drop_ctemp
    fensapice_drop_cmelt: fensapice_drop_cmelt
    fensapice_drop_cdiam: fensapice_drop_cdiam
    fensapice_drop_cv: fensapice_drop_cv
    fensapice_drop_cx: fensapice_drop_cx
    fensapice_drop_cy: fensapice_drop_cy
    fensapice_drop_cz: fensapice_drop_cz
    fensapice_drop_vrh: fensapice_drop_vrh
    fensapice_drop_vrh_1: fensapice_drop_vrh_1
    fensapice_drop_vc: fensapice_drop_vc
    mixing_plane_thread: mixing_plane_thread
    solar_fluxes: solar_fluxes
    solar_shining_factor: solar_shining_factor
    radiating_s2s_surface: radiating_s2s_surface
    ac_options: ac_options
    impedance_0: impedance_0
    impedance_1: impedance_1
    impedance_2: impedance_2
    ac_wave: ac_wave
    les_spec: les_spec
    return_type: str

class velocity_inlet(NamedObject[velocity_inlet_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: velocity_inlet_child
    return_type: str

class d_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class q_dot(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class h(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class tinf_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class planar_conduction(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thickness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class qdot(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class shell_conduction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    thickness: thickness
    material: material
    qdot: qdot
    return_type: str

class shell_conduction(ListObject[shell_conduction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: shell_conduction_child
    return_type: str

class thin_wall_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    thickness: thickness
    material: material
    qdot: qdot
    return_type: str

class thin_wall(ListObject[thin_wall_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: thin_wall_child
    return_type: str

class motion_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class shear_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rough_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class moving(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relative(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotating(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_translation_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_translation(ListObject[wall_translation_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: wall_translation_child
    return_type: str

class components_1(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ex_emiss(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class trad(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class int_rad(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class trad_internal(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class area_enhancement_factor(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class rough_option(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rough_nasa(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rough_shin_et_al(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rough_data(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class roughness_height(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class roughness_const(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class roughness_height_cp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class roughness_const_cp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class roughness_const_nasa(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class roughness_const_shin(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class roughness_const_data(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class variable_roughness(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class free_stream_velocity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class free_stream_temp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class characteristic_length(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class free_stream_temp_cp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class characteristic_length_cp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class liquid_content(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class liquid_content_cp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class droplet_diameter(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class dpm_bc_norm_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class dpm_bc_tang_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class dpm_bc_frictn_coeff(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class dpm_film_splash_nsamp(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_crit_temp_option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_critical_temp_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_calibratable_temp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_impingement_splashing_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_upper_deposition_limit_offset(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_deposition_delta_t(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_laplace_number_constant(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_partial_evaporation_ratio(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ra_roughness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rz_roughness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rq_roughness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rsm_roughness(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_generic(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class dpm_bc_erosion_c(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class dpm_bc_erosion_n(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_2
    number_of_coeff: number_of_coeff
    function_of: function_of
    coefficients: coefficients_1
    value: value_1
    piecewise_polynomial: piecewise_polynomial_1
    piecewise_linear: piecewise_linear
    return_type: str

class dpm_bc_erosion_finnie(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_finnie_k(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_finnie_vel_exp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_finnie_max_erosion_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_a(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_vel_exp(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_transition_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_b(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_c(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_w(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_x(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_mclaury_y(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_e90(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_hv(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_n1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_n2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_k2(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_k3(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_dref(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_oka_vref(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_dnv(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_dnv_k(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_dnv_n(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_dnv_ductile(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_shear(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_shear_v(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_shear_c(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_shear_packing_limit(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_bc_erosion_shielding(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_wall_heat_exchange(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_film_condensation(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_film_bl_model(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_particle_stripping(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_critical_shear_stress(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_film_separation_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_critical_we_number(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_film_separation_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_allow_lwf_to_vof(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_allow_vof_to_lwf(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_initialize_lwf(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_initial_height(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_velocity_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_velocity(ListObject[film_velocity_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: film_velocity_child
    return_type: str

class dpm_initial_temperature(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_initial_injection(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_parcel_surface_area_density(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minimum_number_of_parcels_per_face(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class band_in_emiss_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class band_in_emiss(NamedObject[band_in_emiss_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: band_in_emiss_child
    return_type: str

class mc_bsource_p(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mc_poldfun_p(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class polar_func_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mc_polar_expr(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class polar_real_angle(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class polar_real_intensity(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class polar_pair_list_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    polar_real_angle: polar_real_angle
    polar_real_intensity: polar_real_intensity
    return_type: str

class polar_pair_list(ListObject[polar_pair_list_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: polar_pair_list_child
    return_type: str

class pold_pair_list_rad(RealList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radiation_direction_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class radiation_direction(ListObject[radiation_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: radiation_direction_child
    return_type: str

class band_diffuse_frac_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class band_diffuse_frac(NamedObject[band_diffuse_frac_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: band_diffuse_frac_child
    return_type: str

class critical_zone(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fpsc(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class v_transmissivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ir_transmissivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class v_opq_absorbtivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ir_opq_absorbtivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class v_st_absorbtivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ir_st_absorbtivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class d_st_absorbtivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class d_transmissivity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fsi_interface(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partially_catalytic(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partially_catalytic_material(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partially_catalytic_recombination_coefficient_o(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class partially_catalytic_recombination_coefficient_n(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class partially_catalytic_recombination_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_spec_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_spec(NamedObject[species_spec_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: species_spec_child
    return_type: str

class elec_potential_jump(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class elec_potential_resistance(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class echem_reaction(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class elec_potential_mechs(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class faradaic_heat(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class li_ion_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class li_ion_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class per_dispx(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class per_dispy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class per_dispz(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class per_imagx(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class per_imagy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class per_imagz(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class freq(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class amp(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class nodal_diam(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pass_number(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class fwd(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aero(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cmplx(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class norm(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class method_4(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gtemp_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class g_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class g_qflux(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class wall_restitution_coeff(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotation_axis_origin_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotation_axis_origin(ListObject[rotation_axis_origin_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: rotation_axis_origin_child
    return_type: str

class rotation_axis_direction_child(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotation_axis_direction(ListObject[rotation_axis_direction_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: rotation_axis_direction_child
    return_type: str

class specified_shear(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class shear_stress_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class shear_stress(ListObject[shear_stress_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: shear_stress_child
    return_type: str

class fslip(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class eslip(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surf_tens_grad(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class contact_resistance(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class surf_washcoat_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_deposition_height(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_species_density(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation_select_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation_vielle_a(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation_vielle_n(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation_flux(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation_surfacerxn_density(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ablation_species_mf_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class ablation_species_mf(NamedObject[ablation_species_mf_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: ablation_species_mf_child
    return_type: str

class specular_coeff(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mom_accom_coef(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class therm_accom_coef(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class eve_accom_coef(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_wall(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_wall_bc(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_height(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class flux_momentum_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class flux_momentum(ListObject[flux_momentum_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: flux_momentum_child
    return_type: str

class film_relative_vel(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_bc_imp_press(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_temperature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_scalar(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_source(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_h_src(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class momentum_source_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class momentum_source(ListObject[momentum_source_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: momentum_source_child
    return_type: str

class film_t_src(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_s_src(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_phase_change(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_phase_change_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_cond_const(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vapo_const(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_cond_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_vapo_rate(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_momentum_coupling(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_splash_wall(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_boundary_separation(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_impinge_model(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_splash_nparc(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_crit_temp_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_roughness_ra(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_roughness_rz(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_upper_deposition_limit_offset(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_deposition_delta_t(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_laplace_number_constant(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_partial_evap_ratio(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_contact_angle(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_contact_angle_mean(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class film_contact_angle_rstd(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_contact_angle_beta(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vof_coupling_high(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vof_trans_high(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vof_trans_high_relax(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vof_coupling_low(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vof_trans_low(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class film_vof_trans_low_relax(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class caf(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    value: value_1
    profile_name: profile_name
    field_name: field_name
    udf: udf
    return_type: str

class thermal_stabilization(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_factor(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stab_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_ice_icing_mode(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_ice_hflux(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_ice_hflux_1(Real, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_drop_vwet(Boolean, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_dpm_wall_condition(Integer, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_dpm_bc_norm_coeff(RealList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fensapice_dpm_bc_tang_coeff(RealList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_24_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    d: d_1
    q_dot: q_dot
    material: material
    thermal_bc: thermal_bc
    t: t
    q: q
    h: h
    tinf: tinf_1
    planar_conduction: planar_conduction
    shell_conduction: shell_conduction
    thin_wall: thin_wall
    motion_bc: motion_bc
    shear_bc: shear_bc
    rough_bc: rough_bc
    moving: moving
    relative: relative
    rotating: rotating
    vmag: vmag
    wall_translation: wall_translation
    components: components_1
    velocity: velocity_1
    in_emiss: in_emiss
    ex_emiss: ex_emiss
    trad: trad
    int_rad: int_rad
    trad_internal: trad_internal
    area_enhancement_factor: area_enhancement_factor
    rough_option: rough_option
    rough_nasa: rough_nasa
    rough_shin_et_al: rough_shin_et_al
    rough_data: rough_data
    roughness_height: roughness_height
    roughness_const: roughness_const
    roughness_height_cp: roughness_height_cp
    roughness_const_cp: roughness_const_cp
    roughness_const_nasa: roughness_const_nasa
    roughness_const_shin: roughness_const_shin
    roughness_const_data: roughness_const_data
    variable_roughness: variable_roughness
    free_stream_velocity: free_stream_velocity
    free_stream_temp: free_stream_temp
    characteristic_length: characteristic_length
    free_stream_temp_cp: free_stream_temp_cp
    characteristic_length_cp: characteristic_length_cp
    liquid_content: liquid_content
    liquid_content_cp: liquid_content_cp
    droplet_diameter: droplet_diameter
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_norm_coeff: dpm_bc_norm_coeff
    dpm_bc_tang_coeff: dpm_bc_tang_coeff
    dpm_bc_frictn_coeff: dpm_bc_frictn_coeff
    dpm_bc_udf: dpm_bc_udf
    dpm_film_splash_nsamp: dpm_film_splash_nsamp
    dpm_crit_temp_option: dpm_crit_temp_option
    dpm_critical_temp_factor: dpm_critical_temp_factor
    dpm_calibratable_temp: dpm_calibratable_temp
    dpm_impingement_splashing_model: dpm_impingement_splashing_model
    dpm_upper_deposition_limit_offset: dpm_upper_deposition_limit_offset
    dpm_deposition_delta_t: dpm_deposition_delta_t
    dpm_laplace_number_constant: dpm_laplace_number_constant
    dpm_partial_evaporation_ratio: dpm_partial_evaporation_ratio
    ra_roughness: ra_roughness
    rz_roughness: rz_roughness
    rq_roughness: rq_roughness
    rsm_roughness: rsm_roughness
    dpm_bc_erosion_generic: dpm_bc_erosion_generic
    dpm_bc_erosion: dpm_bc_erosion
    dpm_bc_erosion_c: dpm_bc_erosion_c
    dpm_bc_erosion_n: dpm_bc_erosion_n
    dpm_bc_erosion_finnie: dpm_bc_erosion_finnie
    dpm_bc_erosion_finnie_k: dpm_bc_erosion_finnie_k
    dpm_bc_erosion_finnie_vel_exp: dpm_bc_erosion_finnie_vel_exp
    dpm_bc_erosion_finnie_max_erosion_angle: dpm_bc_erosion_finnie_max_erosion_angle
    dpm_bc_erosion_mclaury: dpm_bc_erosion_mclaury
    dpm_bc_erosion_mclaury_a: dpm_bc_erosion_mclaury_a
    dpm_bc_erosion_mclaury_vel_exp: dpm_bc_erosion_mclaury_vel_exp
    dpm_bc_erosion_mclaury_transition_angle: dpm_bc_erosion_mclaury_transition_angle
    dpm_bc_erosion_mclaury_b: dpm_bc_erosion_mclaury_b
    dpm_bc_erosion_mclaury_c: dpm_bc_erosion_mclaury_c
    dpm_bc_erosion_mclaury_w: dpm_bc_erosion_mclaury_w
    dpm_bc_erosion_mclaury_x: dpm_bc_erosion_mclaury_x
    dpm_bc_erosion_mclaury_y: dpm_bc_erosion_mclaury_y
    dpm_bc_erosion_oka: dpm_bc_erosion_oka
    dpm_bc_erosion_oka_e90: dpm_bc_erosion_oka_e90
    dpm_bc_erosion_oka_hv: dpm_bc_erosion_oka_hv
    dpm_bc_erosion_oka_n1: dpm_bc_erosion_oka_n1
    dpm_bc_erosion_oka_n2: dpm_bc_erosion_oka_n2
    dpm_bc_erosion_oka_k2: dpm_bc_erosion_oka_k2
    dpm_bc_erosion_oka_k3: dpm_bc_erosion_oka_k3
    dpm_bc_erosion_oka_dref: dpm_bc_erosion_oka_dref
    dpm_bc_erosion_oka_vref: dpm_bc_erosion_oka_vref
    dpm_bc_erosion_dnv: dpm_bc_erosion_dnv
    dpm_bc_erosion_dnv_k: dpm_bc_erosion_dnv_k
    dpm_bc_erosion_dnv_n: dpm_bc_erosion_dnv_n
    dpm_bc_erosion_dnv_ductile: dpm_bc_erosion_dnv_ductile
    dpm_bc_erosion_shear: dpm_bc_erosion_shear
    dpm_bc_erosion_shear_v: dpm_bc_erosion_shear_v
    dpm_bc_erosion_shear_c: dpm_bc_erosion_shear_c
    dpm_bc_erosion_shear_packing_limit: dpm_bc_erosion_shear_packing_limit
    dpm_bc_erosion_shielding: dpm_bc_erosion_shielding
    dpm_wall_heat_exchange: dpm_wall_heat_exchange
    dpm_film_condensation: dpm_film_condensation
    dpm_film_bl_model: dpm_film_bl_model
    dpm_particle_stripping: dpm_particle_stripping
    dpm_critical_shear_stress: dpm_critical_shear_stress
    dpm_film_separation_model: dpm_film_separation_model
    dpm_critical_we_number: dpm_critical_we_number
    dpm_film_separation_angle: dpm_film_separation_angle
    dpm_allow_lwf_to_vof: dpm_allow_lwf_to_vof
    dpm_allow_vof_to_lwf: dpm_allow_vof_to_lwf
    dpm_initialize_lwf: dpm_initialize_lwf
    dpm_initial_height: dpm_initial_height
    film_velocity: film_velocity
    dpm_initial_temperature: dpm_initial_temperature
    dpm_initial_injection: dpm_initial_injection
    film_parcel_surface_area_density: film_parcel_surface_area_density
    minimum_number_of_parcels_per_face: minimum_number_of_parcels_per_face
    band_in_emiss: band_in_emiss
    radiation_bc: radiation_bc
    mc_bsource_p: mc_bsource_p
    mc_poldfun_p: mc_poldfun_p
    polar_func_type: polar_func_type
    mc_polar_expr: mc_polar_expr
    polar_pair_list: polar_pair_list
    pold_pair_list_rad: pold_pair_list_rad
    radiation_direction: radiation_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    band_diffuse_frac: band_diffuse_frac
    radiating_s2s_surface: radiating_s2s_surface
    critical_zone: critical_zone
    fpsc: fpsc
    parallel_collimated_beam: parallel_collimated_beam
    solar_fluxes: solar_fluxes
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    v_transmissivity: v_transmissivity
    ir_transmissivity: ir_transmissivity
    v_opq_absorbtivity: v_opq_absorbtivity
    ir_opq_absorbtivity: ir_opq_absorbtivity
    v_st_absorbtivity: v_st_absorbtivity
    ir_st_absorbtivity: ir_st_absorbtivity
    d_st_absorbtivity: d_st_absorbtivity
    d_transmissivity: d_transmissivity
    fsi_interface: fsi_interface
    react: react
    partially_catalytic: partially_catalytic
    partially_catalytic_material: partially_catalytic_material
    partially_catalytic_recombination_coefficient_o: partially_catalytic_recombination_coefficient_o
    partially_catalytic_recombination_coefficient_n: partially_catalytic_recombination_coefficient_n
    partially_catalytic_recombination_model: partially_catalytic_recombination_model
    species_spec: species_spec
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    elec_potential_jump: elec_potential_jump
    elec_potential_resistance: elec_potential_resistance
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    echem_reaction: echem_reaction
    elec_potential_mechs: elec_potential_mechs
    faradaic_heat: faradaic_heat
    li_ion_type: li_ion_type
    li_ion_value: li_ion_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    per_dispx: per_dispx
    per_dispy: per_dispy
    per_dispz: per_dispz
    per_imagx: per_imagx
    per_imagy: per_imagy
    per_imagz: per_imagz
    freq: freq
    amp: amp
    nodal_diam: nodal_diam
    pass_number: pass_number
    fwd: fwd
    aero: aero
    cmplx: cmplx
    norm: norm
    method: method_4
    uds_bc: uds_bc
    uds: uds
    gtemp_bc: gtemp_bc
    g_temperature: g_temperature
    g_qflux: g_qflux
    wall_restitution_coeff: wall_restitution_coeff
    omega: omega
    rotation_axis_origin: rotation_axis_origin
    rotation_axis_direction: rotation_axis_direction
    adhesion_angle: adhesion_angle
    specified_shear: specified_shear
    shear_stress: shear_stress
    fslip: fslip
    eslip: eslip
    surf_tens_grad: surf_tens_grad
    contact_resistance: contact_resistance
    reaction_mechs: reaction_mechs_1
    surf_washcoat_factor: surf_washcoat_factor
    initial_deposition_height: initial_deposition_height
    solid_species_density: solid_species_density
    ablation_select_model: ablation_select_model
    ablation_vielle_a: ablation_vielle_a
    ablation_vielle_n: ablation_vielle_n
    ablation_flux: ablation_flux
    ablation_surfacerxn_density: ablation_surfacerxn_density
    ablation_species_mf: ablation_species_mf
    specular_coeff: specular_coeff
    mom_accom_coef: mom_accom_coef
    therm_accom_coef: therm_accom_coef
    eve_accom_coef: eve_accom_coef
    film_wall: film_wall
    film_wall_bc: film_wall_bc
    film_height: film_height
    flux_momentum: flux_momentum
    film_relative_vel: film_relative_vel
    film_bc_imp_press: film_bc_imp_press
    film_temperature: film_temperature
    film_scalar: film_scalar
    film_source: film_source
    film_h_src: film_h_src
    momentum_source: momentum_source
    film_t_src: film_t_src
    film_s_src: film_s_src
    film_phase_change: film_phase_change
    film_phase_change_model: film_phase_change_model
    film_cond_const: film_cond_const
    film_vapo_const: film_vapo_const
    film_cond_rate: film_cond_rate
    film_vapo_rate: film_vapo_rate
    film_momentum_coupling: film_momentum_coupling
    film_splash_wall: film_splash_wall
    film_boundary_separation: film_boundary_separation
    film_impinge_model: film_impinge_model
    film_splash_nparc: film_splash_nparc
    film_crit_temp_factor: film_crit_temp_factor
    film_roughness_ra: film_roughness_ra
    film_roughness_rz: film_roughness_rz
    film_upper_deposition_limit_offset: film_upper_deposition_limit_offset
    film_deposition_delta_t: film_deposition_delta_t
    film_laplace_number_constant: film_laplace_number_constant
    film_partial_evap_ratio: film_partial_evap_ratio
    film_contact_angle: film_contact_angle
    film_contact_angle_mean: film_contact_angle_mean
    film_contact_angle_rstd: film_contact_angle_rstd
    film_contact_angle_beta: film_contact_angle_beta
    film_vof_coupling_high: film_vof_coupling_high
    film_vof_trans_high: film_vof_trans_high
    film_vof_trans_high_relax: film_vof_trans_high_relax
    film_vof_coupling_low: film_vof_coupling_low
    film_vof_trans_low: film_vof_trans_low
    film_vof_trans_low_relax: film_vof_trans_low_relax
    caf: caf
    thermal_stabilization: thermal_stabilization
    scale_factor: scale_factor
    stab_method: stab_method
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_ice_icing_mode: fensapice_ice_icing_mode
    fensapice_ice_hflux: fensapice_ice_hflux
    fensapice_ice_hflux_1: fensapice_ice_hflux_1
    fensapice_drop_vwet: fensapice_drop_vwet
    fensapice_dpm_wall_condition: fensapice_dpm_wall_condition
    fensapice_dpm_bc_norm_coeff: fensapice_dpm_bc_norm_coeff
    fensapice_dpm_bc_tang_coeff: fensapice_dpm_bc_tang_coeff
    return_type: str

class phase_24(NamedObject[phase_24_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_24_child
    return_type: str

class wall_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    phase: phase_24
    name: name_2
    geom_disable: geom_disable
    geom_dir_spec: geom_dir_spec
    geom_dir_x: geom_dir_x
    geom_dir_y: geom_dir_y
    geom_dir_z: geom_dir_z
    geom_levels: geom_levels
    geom_bgthread: geom_bgthread
    d: d_1
    q_dot: q_dot
    material: material
    thermal_bc: thermal_bc
    t: t
    q: q
    h: h
    tinf: tinf_1
    planar_conduction: planar_conduction
    shell_conduction: shell_conduction
    thin_wall: thin_wall
    motion_bc: motion_bc
    shear_bc: shear_bc
    rough_bc: rough_bc
    moving: moving
    relative: relative
    rotating: rotating
    vmag: vmag
    wall_translation: wall_translation
    components: components_1
    velocity: velocity_1
    in_emiss: in_emiss
    ex_emiss: ex_emiss
    trad: trad
    int_rad: int_rad
    trad_internal: trad_internal
    area_enhancement_factor: area_enhancement_factor
    rough_option: rough_option
    rough_nasa: rough_nasa
    rough_shin_et_al: rough_shin_et_al
    rough_data: rough_data
    roughness_height: roughness_height
    roughness_const: roughness_const
    roughness_height_cp: roughness_height_cp
    roughness_const_cp: roughness_const_cp
    roughness_const_nasa: roughness_const_nasa
    roughness_const_shin: roughness_const_shin
    roughness_const_data: roughness_const_data
    variable_roughness: variable_roughness
    free_stream_velocity: free_stream_velocity
    free_stream_temp: free_stream_temp
    characteristic_length: characteristic_length
    free_stream_temp_cp: free_stream_temp_cp
    characteristic_length_cp: characteristic_length_cp
    liquid_content: liquid_content
    liquid_content_cp: liquid_content_cp
    droplet_diameter: droplet_diameter
    dpm_bc_type: dpm_bc_type
    dpm_bc_collision_partner: dpm_bc_collision_partner
    reinj_inj: reinj_inj
    dpm_bc_norm_coeff: dpm_bc_norm_coeff
    dpm_bc_tang_coeff: dpm_bc_tang_coeff
    dpm_bc_frictn_coeff: dpm_bc_frictn_coeff
    dpm_bc_udf: dpm_bc_udf
    dpm_film_splash_nsamp: dpm_film_splash_nsamp
    dpm_crit_temp_option: dpm_crit_temp_option
    dpm_critical_temp_factor: dpm_critical_temp_factor
    dpm_calibratable_temp: dpm_calibratable_temp
    dpm_impingement_splashing_model: dpm_impingement_splashing_model
    dpm_upper_deposition_limit_offset: dpm_upper_deposition_limit_offset
    dpm_deposition_delta_t: dpm_deposition_delta_t
    dpm_laplace_number_constant: dpm_laplace_number_constant
    dpm_partial_evaporation_ratio: dpm_partial_evaporation_ratio
    ra_roughness: ra_roughness
    rz_roughness: rz_roughness
    rq_roughness: rq_roughness
    rsm_roughness: rsm_roughness
    dpm_bc_erosion_generic: dpm_bc_erosion_generic
    dpm_bc_erosion: dpm_bc_erosion
    dpm_bc_erosion_c: dpm_bc_erosion_c
    dpm_bc_erosion_n: dpm_bc_erosion_n
    dpm_bc_erosion_finnie: dpm_bc_erosion_finnie
    dpm_bc_erosion_finnie_k: dpm_bc_erosion_finnie_k
    dpm_bc_erosion_finnie_vel_exp: dpm_bc_erosion_finnie_vel_exp
    dpm_bc_erosion_finnie_max_erosion_angle: dpm_bc_erosion_finnie_max_erosion_angle
    dpm_bc_erosion_mclaury: dpm_bc_erosion_mclaury
    dpm_bc_erosion_mclaury_a: dpm_bc_erosion_mclaury_a
    dpm_bc_erosion_mclaury_vel_exp: dpm_bc_erosion_mclaury_vel_exp
    dpm_bc_erosion_mclaury_transition_angle: dpm_bc_erosion_mclaury_transition_angle
    dpm_bc_erosion_mclaury_b: dpm_bc_erosion_mclaury_b
    dpm_bc_erosion_mclaury_c: dpm_bc_erosion_mclaury_c
    dpm_bc_erosion_mclaury_w: dpm_bc_erosion_mclaury_w
    dpm_bc_erosion_mclaury_x: dpm_bc_erosion_mclaury_x
    dpm_bc_erosion_mclaury_y: dpm_bc_erosion_mclaury_y
    dpm_bc_erosion_oka: dpm_bc_erosion_oka
    dpm_bc_erosion_oka_e90: dpm_bc_erosion_oka_e90
    dpm_bc_erosion_oka_hv: dpm_bc_erosion_oka_hv
    dpm_bc_erosion_oka_n1: dpm_bc_erosion_oka_n1
    dpm_bc_erosion_oka_n2: dpm_bc_erosion_oka_n2
    dpm_bc_erosion_oka_k2: dpm_bc_erosion_oka_k2
    dpm_bc_erosion_oka_k3: dpm_bc_erosion_oka_k3
    dpm_bc_erosion_oka_dref: dpm_bc_erosion_oka_dref
    dpm_bc_erosion_oka_vref: dpm_bc_erosion_oka_vref
    dpm_bc_erosion_dnv: dpm_bc_erosion_dnv
    dpm_bc_erosion_dnv_k: dpm_bc_erosion_dnv_k
    dpm_bc_erosion_dnv_n: dpm_bc_erosion_dnv_n
    dpm_bc_erosion_dnv_ductile: dpm_bc_erosion_dnv_ductile
    dpm_bc_erosion_shear: dpm_bc_erosion_shear
    dpm_bc_erosion_shear_v: dpm_bc_erosion_shear_v
    dpm_bc_erosion_shear_c: dpm_bc_erosion_shear_c
    dpm_bc_erosion_shear_packing_limit: dpm_bc_erosion_shear_packing_limit
    dpm_bc_erosion_shielding: dpm_bc_erosion_shielding
    dpm_wall_heat_exchange: dpm_wall_heat_exchange
    dpm_film_condensation: dpm_film_condensation
    dpm_film_bl_model: dpm_film_bl_model
    dpm_particle_stripping: dpm_particle_stripping
    dpm_critical_shear_stress: dpm_critical_shear_stress
    dpm_film_separation_model: dpm_film_separation_model
    dpm_critical_we_number: dpm_critical_we_number
    dpm_film_separation_angle: dpm_film_separation_angle
    dpm_allow_lwf_to_vof: dpm_allow_lwf_to_vof
    dpm_allow_vof_to_lwf: dpm_allow_vof_to_lwf
    dpm_initialize_lwf: dpm_initialize_lwf
    dpm_initial_height: dpm_initial_height
    film_velocity: film_velocity
    dpm_initial_temperature: dpm_initial_temperature
    dpm_initial_injection: dpm_initial_injection
    film_parcel_surface_area_density: film_parcel_surface_area_density
    minimum_number_of_parcels_per_face: minimum_number_of_parcels_per_face
    band_in_emiss: band_in_emiss
    radiation_bc: radiation_bc
    mc_bsource_p: mc_bsource_p
    mc_poldfun_p: mc_poldfun_p
    polar_func_type: polar_func_type
    mc_polar_expr: mc_polar_expr
    polar_pair_list: polar_pair_list
    pold_pair_list_rad: pold_pair_list_rad
    radiation_direction: radiation_direction
    coll_dtheta: coll_dtheta
    coll_dphi: coll_dphi
    band_q_irrad: band_q_irrad
    band_q_irrad_diffuse: band_q_irrad_diffuse
    band_diffuse_frac: band_diffuse_frac
    radiating_s2s_surface: radiating_s2s_surface
    critical_zone: critical_zone
    fpsc: fpsc
    parallel_collimated_beam: parallel_collimated_beam
    solar_fluxes: solar_fluxes
    solar_direction: solar_direction
    solar_irradiation: solar_irradiation
    v_transmissivity: v_transmissivity
    ir_transmissivity: ir_transmissivity
    v_opq_absorbtivity: v_opq_absorbtivity
    ir_opq_absorbtivity: ir_opq_absorbtivity
    v_st_absorbtivity: v_st_absorbtivity
    ir_st_absorbtivity: ir_st_absorbtivity
    d_st_absorbtivity: d_st_absorbtivity
    d_transmissivity: d_transmissivity
    fsi_interface: fsi_interface
    react: react
    partially_catalytic: partially_catalytic
    partially_catalytic_material: partially_catalytic_material
    partially_catalytic_recombination_coefficient_o: partially_catalytic_recombination_coefficient_o
    partially_catalytic_recombination_coefficient_n: partially_catalytic_recombination_coefficient_n
    partially_catalytic_recombination_model: partially_catalytic_recombination_model
    species_spec: species_spec
    mf: mf
    elec_potential_type: elec_potential_type
    potential_value: potential_value
    elec_potential_jump: elec_potential_jump
    elec_potential_resistance: elec_potential_resistance
    dual_potential_type: dual_potential_type
    dual_potential_value: dual_potential_value
    echem_reaction: echem_reaction
    elec_potential_mechs: elec_potential_mechs
    faradaic_heat: faradaic_heat
    li_ion_type: li_ion_type
    li_ion_value: li_ion_value
    x_displacement_type: x_displacement_type
    x_displacement_value: x_displacement_value
    y_displacement_type: y_displacement_type
    y_displacement_value: y_displacement_value
    z_displacement_type: z_displacement_type
    z_displacement_value: z_displacement_value
    per_dispx: per_dispx
    per_dispy: per_dispy
    per_dispz: per_dispz
    per_imagx: per_imagx
    per_imagy: per_imagy
    per_imagz: per_imagz
    freq: freq
    amp: amp
    nodal_diam: nodal_diam
    pass_number: pass_number
    fwd: fwd
    aero: aero
    cmplx: cmplx
    norm: norm
    method: method_4
    uds_bc: uds_bc
    uds: uds
    gtemp_bc: gtemp_bc
    g_temperature: g_temperature
    g_qflux: g_qflux
    wall_restitution_coeff: wall_restitution_coeff
    omega: omega
    rotation_axis_origin: rotation_axis_origin
    rotation_axis_direction: rotation_axis_direction
    adhesion_angle: adhesion_angle
    specified_shear: specified_shear
    shear_stress: shear_stress
    fslip: fslip
    eslip: eslip
    surf_tens_grad: surf_tens_grad
    contact_resistance: contact_resistance
    reaction_mechs: reaction_mechs_1
    surf_washcoat_factor: surf_washcoat_factor
    initial_deposition_height: initial_deposition_height
    solid_species_density: solid_species_density
    ablation_select_model: ablation_select_model
    ablation_vielle_a: ablation_vielle_a
    ablation_vielle_n: ablation_vielle_n
    ablation_flux: ablation_flux
    ablation_surfacerxn_density: ablation_surfacerxn_density
    ablation_species_mf: ablation_species_mf
    specular_coeff: specular_coeff
    mom_accom_coef: mom_accom_coef
    therm_accom_coef: therm_accom_coef
    eve_accom_coef: eve_accom_coef
    film_wall: film_wall
    film_wall_bc: film_wall_bc
    film_height: film_height
    flux_momentum: flux_momentum
    film_relative_vel: film_relative_vel
    film_bc_imp_press: film_bc_imp_press
    film_temperature: film_temperature
    film_scalar: film_scalar
    film_source: film_source
    film_h_src: film_h_src
    momentum_source: momentum_source
    film_t_src: film_t_src
    film_s_src: film_s_src
    film_phase_change: film_phase_change
    film_phase_change_model: film_phase_change_model
    film_cond_const: film_cond_const
    film_vapo_const: film_vapo_const
    film_cond_rate: film_cond_rate
    film_vapo_rate: film_vapo_rate
    film_momentum_coupling: film_momentum_coupling
    film_splash_wall: film_splash_wall
    film_boundary_separation: film_boundary_separation
    film_impinge_model: film_impinge_model
    film_splash_nparc: film_splash_nparc
    film_crit_temp_factor: film_crit_temp_factor
    film_roughness_ra: film_roughness_ra
    film_roughness_rz: film_roughness_rz
    film_upper_deposition_limit_offset: film_upper_deposition_limit_offset
    film_deposition_delta_t: film_deposition_delta_t
    film_laplace_number_constant: film_laplace_number_constant
    film_partial_evap_ratio: film_partial_evap_ratio
    film_contact_angle: film_contact_angle
    film_contact_angle_mean: film_contact_angle_mean
    film_contact_angle_rstd: film_contact_angle_rstd
    film_contact_angle_beta: film_contact_angle_beta
    film_vof_coupling_high: film_vof_coupling_high
    film_vof_trans_high: film_vof_trans_high
    film_vof_trans_high_relax: film_vof_trans_high_relax
    film_vof_coupling_low: film_vof_coupling_low
    film_vof_trans_low: film_vof_trans_low
    film_vof_trans_low_relax: film_vof_trans_low_relax
    caf: caf
    thermal_stabilization: thermal_stabilization
    scale_factor: scale_factor
    stab_method: stab_method
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype
    fensapice_ice_icing_mode: fensapice_ice_icing_mode
    fensapice_ice_hflux: fensapice_ice_hflux
    fensapice_ice_hflux_1: fensapice_ice_hflux_1
    fensapice_drop_vwet: fensapice_drop_vwet
    fensapice_dpm_wall_condition: fensapice_dpm_wall_condition
    fensapice_dpm_bc_norm_coeff: fensapice_dpm_bc_norm_coeff
    fensapice_dpm_bc_tang_coeff: fensapice_dpm_bc_tang_coeff
    return_type: str

class wall(NamedObject[wall_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: wall_child
    return_type: str

class boundary_conditions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    axis: axis
    degassing: degassing
    exhaust_fan: exhaust_fan
    fan: fan
    geometry: geometry_3
    inlet_vent: inlet_vent
    intake_fan: intake_fan
    interface: interface
    interior: interior
    mass_flow_inlet: mass_flow_inlet
    mass_flow_outlet: mass_flow_outlet
    network: network
    network_end: network_end
    outflow: outflow
    outlet_vent: outlet_vent
    overset: overset
    periodic: periodic
    porous_jump: porous_jump
    pressure_far_field: pressure_far_field
    pressure_inlet: pressure_inlet
    pressure_outlet: pressure_outlet
    radiator: radiator
    rans_les_interface: rans_les_interface
    recirculation_inlet: recirculation_inlet
    recirculation_outlet: recirculation_outlet
    shadow: shadow
    symmetry: symmetry
    velocity_inlet: velocity_inlet
    wall: wall
    def copy(self, from_: str, to: list[str], verbosity: bool):
        """
        'copy' command.
        """
    def change_type(self, zone_list: list[str], new_type: str):
        """
        'change_type' command.
        """
    def slit_face_zone(self, zone_id: int):
        """
        Slit a two-sided wall into two connected wall zones.
        
        Parameters
        ----------
            zone_id : int
                'zone_id' child.
        """
    def slit_interior_between_diff_solids(self):
        """
        Slit interior created between different solids into coupled walls.
        """
    def create_all_shell_threads(self):
        """
        Mark all finite thickness wall for shell creation. Shell zones will be created at the start of iterations.
        """
    def recreate_all_shells(self):
        """
        Create shell on all the walls where which were deleted using the command delete-all-shells.
        """
    def delete_all_shells(self):
        """
        'delete_all_shells' command.
        """
    def orient_face_zone(self, face_zone_id: int):
        """
        Orient the face zone.
        
        Parameters
        ----------
            face_zone_id : int
                'face_zone_id' child.
        """
    return_type: str

class area(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class depth(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density_6(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enthalpy(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class length(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class temperature_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class yplus(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscosity_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_values(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    area: area
    depth: depth
    density: density_6
    enthalpy: enthalpy
    length: length
    pressure: pressure
    temperature: temperature_3
    yplus: yplus
    velocity: velocity_2
    viscosity: viscosity_3
    zone: zone
    def compute(self, from_zone_type: str, from_zone_name: str, phase: str):
        """
        'compute' command.
        """
    def list_val(self):
        """
        'list_val' command.
        """
    return_type: str

class definition(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class description(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class parameterid(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class parametername(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unit_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class input_parameter(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class output_parameter(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class named_expressions_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    query_names: list[str]
    name: name_1
    definition: definition
    description: description
    parameterid: parameterid
    parametername: parametername
    unit: unit_1
    input_parameter: input_parameter
    output_parameter: output_parameter
    def get_value(self):
        """
        'get_value' query.
        """
    return_type: str

class named_expressions(NamedObject[named_expressions_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: named_expressions_child
    return_type: str

class proximity_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_default_name_prefix(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_one_to_one_pairing_tolerance(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pairing_between_different_cell_zones_only(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pairing_between_interface_zones_only(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class keep_empty_interface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    proximity_tolerance: proximity_tolerance
    set_default_name_prefix: set_default_name_prefix
    set_one_to_one_pairing_tolerance: set_one_to_one_pairing_tolerance
    pairing_between_different_cell_zones_only: pairing_between_different_cell_zones_only
    pairing_between_interface_zones_only: pairing_between_interface_zones_only
    keep_empty_interface: keep_empty_interface
    def naming_option(self, option: int, change_all_o2o_si_names: bool):
        """
        Specify whether or not to include an informative suffix to the mesh interface name.
        
        Parameters
        ----------
            option : int
                'option' child.
            change_all_o2o_si_names : bool
                'change_all_o2o_si_names' child.
        """
    return_type: str

class interface_names(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone_names(StringList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone1(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone2(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class new_zones(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mapped(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_local_mapped_tolerance(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_local_edge_length_factor(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class local_relative_mapped_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class local_absolute_mapped_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class periodic_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbo(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pitch_change_types(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mixing_plane(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbo_non_overlap(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coupled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class matching(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class static(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ignore_diff(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interface_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    interface_names: interface_names
    zone_names: zone_names
    zone1: zone1
    zone2: zone2
    new_zones: new_zones
    mapped: mapped
    enable_local_mapped_tolerance: enable_local_mapped_tolerance
    use_local_edge_length_factor: use_local_edge_length_factor
    local_relative_mapped_tolerance: local_relative_mapped_tolerance
    local_absolute_mapped_tolerance: local_absolute_mapped_tolerance
    periodic: periodic_1
    turbo: turbo
    pitch_change_types: pitch_change_types
    mixing_plane: mixing_plane
    turbo_non_overlap: turbo_non_overlap
    coupled: coupled
    matching: matching
    static: static
    ignore_diff: ignore_diff
    return_type: str

class interface_1(NamedObject[interface_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: interface_1_child
    return_type: str

class zone1_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone2_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbo_interface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    zone1: zone1_1
    zone2: zone2_1
    pitch_change_types: pitch_change_types
    mixing_plane: mixing_plane
    turbo_non_overlap: turbo_non_overlap
    return_type: str

class turbo_interface(NamedObject[turbo_interface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: turbo_interface_child
    return_type: str

class continuity_after_bc(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_4(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class si_with_nodes(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coupled_wall_between_solids(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_visualization_of_interfaces(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mapped_interface_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def solution_controls(self, mf: int, urf: float | str):
        """
        Specification of mapped frequency and under-relaxation factor for mapped interfaces.
        
        Parameters
        ----------
            mf : int
                'mf' child.
            urf : real
                'urf' child.
        """
    def tolerance(self, use_local_edge_length_factor: bool, tolerance1: float | str, tolerance2: float | str, update: bool):
        """
        Specification of mapped interface tolerance.
        
        Parameters
        ----------
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            tolerance1 : real
                'tolerance1' child.
            tolerance2 : real
                'tolerance2' child.
            update : bool
                Update mapped interface with new tolerance.
        """
    def convert_to_mapped_interface(self, all: bool, auto: bool, use_local_edge_length_factor: bool, tolerance1: float | str, tolerance2: float | str):
        """
        Convert non-conformal mesh interface to mapped mesh interfaces.
        
        Parameters
        ----------
            all : bool
                Convert all mesh interfaces to mapped mesh interfaces.
            auto : bool
                Convert poorly matching mesh interfaces to mapped mesh interfaces.
            use_local_edge_length_factor : bool
                Enable tolerance based on local edge length factor instead of absolute tolerance.
            tolerance1 : real
                'tolerance1' child.
            tolerance2 : real
                'tolerance2' child.
        """
    return_type: str

class non_conformal_interface_numerics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def change_numerics(self, use_sided_area_vector: bool, use_nci_sided_area_vectors: bool, recrete: bool):
        """
        Enable modified non-conformal interface numerics.
        
        Parameters
        ----------
            use_sided_area_vector : bool
                'use_sided_area_vector' child.
            use_nci_sided_area_vectors : bool
                'use_nci_sided_area_vectors' child.
            recrete : bool
                'recrete' child.
        """
    return_type: str

class mesh_interfaces(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    query_names: list[str]
    auto_options: auto_options
    interface: interface_1
    turbo_interface: turbo_interface
    continuity_after_bc: continuity_after_bc
    verbosity: verbosity_4
    si_with_nodes: si_with_nodes
    coupled_wall_between_solids: coupled_wall_between_solids
    enable_visualization_of_interfaces: enable_visualization_of_interfaces
    mapped_interface_options: mapped_interface_options
    non_conformal_interface_numerics: non_conformal_interface_numerics
    def delete(self, si_delete: str):
        """
        Delete a mesh interface.
        
        Parameters
        ----------
            si_delete : str
                'si_delete' child.
        """
    def display(self, zones: list[int]):
        """
        Display specified mesh interface zone.
        
        Parameters
        ----------
            zones : List
                'zones' child.
        """
    def list(self):
        """
        List all mesh-interfaces.
        """
    def make_phaselag_from_boundaries(self, sb0: int, sb1: int, angle: float | str, pl_name: str):
        """
        Make interface zones phase lagged.
        
        Parameters
        ----------
            sb0 : int
                Id/name of zone to convert to phase lag side 1.
            sb1 : int
                Id/name of zone to convert to phase lag side 2.
            angle : real
                'angle' child.
            pl_name : str
                'pl_name' child.
        """
    def make_phaselag_from_periodic(self, per_id: int):
        """
        Convert periodic interface to phase lagged.
        
        Parameters
        ----------
            per_id : int
                'per_id' child.
        """
    def delete_all(self):
        """
        Delete all mesh interfaces.
        """
    def improve_quality(self, check_mapped_interface_quality: bool, complete: bool, tol_percentage_increment: float | str):
        """
        Improve mesh interface quality.
        
        Parameters
        ----------
            check_mapped_interface_quality : bool
                Check Mapped Interface Qaulity.
            complete : bool
                Continue to improve the mapped interface quality.
            tol_percentage_increment : real
                'tol_percentage_increment' child.
        """
    def enable_one_to_one_pairing(self, o2o_flag: bool, toggle: bool, delete_empty: bool):
        """
        Use the default one-to-one interface creation method?.
        
        Parameters
        ----------
            o2o_flag : bool
                Use the default one-to-one interface creation method?.
            toggle : bool
                Would you like to proceed?.
            delete_empty : bool
                Delete empty interface interior zones from non-overlapping interfaces?.
        """
    def auto_pairing(self, all: bool, one_to_one_pairing: bool, new_si_id: list[str], si_create: bool, si_name: str, apply_mapped: bool, static_interface: bool):
        """
        Automatically pair and create mesh interfaces for some or all interface zones.
        
        Parameters
        ----------
            all : bool
                'all' child.
            one_to_one_pairing : bool
                'one_to_one_pairing' child.
            new_si_id : List
                Unintersected interface zones for pairing.
            si_create : bool
                'si_create' child.
            si_name : str
                The prefix for mesh interface names.
            apply_mapped : bool
                Apply Mapped option at solids.
            static_interface : bool
                'static_interface' child.
        """
    def enable_motion_transfer_across_interfaces(self, enabled: bool, option_name: str):
        """
        Transfer motion from one side of the interface to the other when only one side undergoes user-defined or system-coupling motion.
        
        Parameters
        ----------
            enabled : bool
                'enabled' child.
            option_name : str
                'option_name' child.
        """
    def remove_left_handed_interface_faces(self, enable: bool, update: bool):
        """
        Remove left-handed faces during mesh interface creation.
        
        Parameters
        ----------
            enable : bool
                Remove left-handed faces on mesh interfaces.
            update : bool
                'update' child.
        """
    def get_non_overlapping_zone_name(self, zone_name: str):
        """
        Get non-overlapping zone name from the associated interface zone.
        
        Parameters
        ----------
            zone_name : str
                Zone name.
        """
    return_type: str

class faces_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self):
        """
        'list_properties' command.
        """
    return_type: str

class faces(NamedObject[faces_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def list_face(self, face_name: str):
        """
        'list_face' command.
        """
    child_object_type: faces_child
    return_type: str

class bodies_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    faces: faces
    def list_properties(self):
        """
        'list_properties' command.
        """
    return_type: str

class bodies(NamedObject[bodies_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: bodies_child
    return_type: str

class components_2(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class groups_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    components: components_2
    def list_properties(self):
        """
        'list_properties' command.
        """
    return_type: str

class groups(NamedObject[groups_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: groups_child
    return_type: str

class parts_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    bodies: bodies
    groups: groups
    return_type: str

class parts(NamedObject[parts_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: parts_child
    return_type: str

class geometry_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    parts: parts
    def list_topology(self):
        """
        'list_topology' command.
        """
    return_type: str

class type_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class type_4(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class locations(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundaries_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    type: type_4
    locations: locations
    return_type: str

class boundaries(NamedObject[boundaries_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: boundaries_child
    return_type: str

class volumes_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    type: type_3
    boundaries: boundaries
    locations: locations
    return_type: str

class volumes(NamedObject[volumes_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: volumes_child
    return_type: str

class type_5(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class periodicity(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mesh_connectivity(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interfaces_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    type: type_5
    boundary_1: boundary_1
    boundary_2: boundary_2
    periodicity: periodicity
    mesh_connectivity: mesh_connectivity
    return_type: str

class interfaces(NamedObject[interfaces_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: interfaces_child
    return_type: str

class physics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    volumes: volumes
    interfaces: interfaces
    def list_physics(self):
        """
        'list_physics' command.
        """
    return_type: str

class motion_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class linear_velocity(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class speed(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotation_axis(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotational_velocity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    speed: speed
    rotation_axis: rotation_axis
    return_type: str

class constant_velocity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    linear_velocity: linear_velocity
    rotational_velocity: rotational_velocity
    return_type: str

class track_zone(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone_track(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    track_zone: track_zone
    return_type: str

class motion(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    motion_type: motion_type
    constant_velocity: constant_velocity
    zone_track: zone_track
    return_type: str

class parent_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class direction_option(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vector(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class point(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_label(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_from(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    direction_option: direction_option
    vector: vector
    point: point
    axis_label: axis_label
    return_type: str

class axis_to(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    direction_option: direction_option
    vector: vector
    point: point
    axis_label: axis_label
    return_type: str

class first_axis(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    axis_from: axis_from
    axis_to: axis_to
    return_type: str

class second_axis(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    axis_from: axis_from
    axis_to: axis_to
    return_type: str

class auto_second_axis(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class orientation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    first_axis: first_axis
    second_axis: second_axis
    auto_second_axis: auto_second_axis
    return_type: str

class initial_state(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    origin: origin
    orientation: orientation
    return_type: str

class display_state(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_frames_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    motion: motion
    parent_1: parent_1
    initial_state: initial_state
    display_state: display_state
    return_type: str

class reference_frames(NamedObject[reference_frames_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display_frame(self, name: str):
        """
        Display Reference Frame.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    def hide_frame(self, name: str):
        """
        Hide Reference Frame.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    child_object_type: reference_frames_child
    return_type: str

class setup(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    general: general
    models: models
    materials: materials
    cell_zone_conditions: cell_zone_conditions
    boundary_conditions: boundary_conditions
    reference_values: reference_values
    named_expressions: named_expressions
    mesh_interfaces: mesh_interfaces
    geometry: geometry_1
    physics: physics
    reference_frames: reference_frames
    return_type: str

class flow_scheme(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coupled_form(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solve_n_phase(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p_v_coupling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    flow_scheme: flow_scheme
    coupled_form: coupled_form
    solve_n_phase: solve_n_phase
    return_type: str

class flux_type_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dbns_cases(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    flux_type: flux_type_1
    return_type: str

class flux_auto_select(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flux_type_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pbns_cases(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    flux_auto_select: flux_auto_select
    flux_type: flux_type_2
    return_type: str

class flux_type(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    dbns_cases: dbns_cases
    pbns_cases: pbns_cases
    return_type: str

class discretization_scheme_child(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class discretization_scheme(NamedObject[discretization_scheme_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: discretization_scheme_child
    return_type: str

class coupled_solver(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class segregated_solver(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density_based_solver(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class formulation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    coupled_solver: coupled_solver
    segregated_solver: segregated_solver
    density_based_solver: density_based_solver
    return_type: str

class relaxation_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convergence_acceleration_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class casm_cutoff_multiplier(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convergence_acceleration_for_stretched_meshes_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    convergence_acceleration_type: convergence_acceleration_type
    casm_cutoff_multiplier: casm_cutoff_multiplier
    return_type: str

class pseudo_time_method(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    formulation: formulation
    relaxation_method: relaxation_method
    convergence_acceleration_for_stretched_meshes: convergence_acceleration_for_stretched_meshes_1
    def relaxation_bounds(self, relaxation_bounding_method: str, default_min_max_relaxation_limits: bool, minimum_allowed_effctive_relaxation: float | str, maximum_allowed_effctive_relaxation: float | str):
        """
        Select relaxation bounding scheme for pseudo time method.
        
        Parameters
        ----------
            relaxation_bounding_method : str
                'relaxation_bounding_method' child.
            default_min_max_relaxation_limits : bool
                'default_min_max_relaxation_limits' child.
            minimum_allowed_effctive_relaxation : real
                'minimum_allowed_effctive_relaxation' child.
            maximum_allowed_effctive_relaxation : real
                'maximum_allowed_effctive_relaxation' child.
        """
    return_type: str

class unsteady_1st_order(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unsteady_2nd_order(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unsteady_2nd_order_bounded(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unsteady_global_time(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class accelerated_non_iterative_time_marching(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class casm_cutoff_multiplier_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convergence_acceleration_for_stretched_meshes(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    convergence_acceleration_type: convergence_acceleration_type
    casm_cutoff_multiplier: casm_cutoff_multiplier_1
    return_type: str

class reactions_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reaction_source_term_relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class implicit_bodyforce_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class physical_velocity_formulation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class disable_rhie_chow_flux(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class presto_pressure_scheme(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class first_to_second_order_blending(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class alternate_diffusion_for_porous_region_solids(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class numerics_pbns(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    implicit_bodyforce_treatment: implicit_bodyforce_treatment
    velocity_formulation: velocity_formulation
    physical_velocity_formulation: physical_velocity_formulation
    disable_rhie_chow_flux: disable_rhie_chow_flux
    presto_pressure_scheme: presto_pressure_scheme
    first_to_second_order_blending: first_to_second_order_blending
    alternate_diffusion_for_porous_region_solids: alternate_diffusion_for_porous_region_solids
    return_type: str

class first_to_second_order_blending_dbns(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class numerics_dbns(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    first_to_second_order_blending_dbns: first_to_second_order_blending_dbns
    return_type: str

class expert_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    reactions: reactions_2
    reaction_source_term_relaxation_factor: reaction_source_term_relaxation_factor
    numerics_pbns: numerics_pbns
    numerics_dbns: numerics_dbns
    return_type: str

class frozen_flux(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gradient_scheme(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_10(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class select_variables(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class type_6(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_5(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    relaxation_factor: relaxation_factor
    select_variables: select_variables
    type: type_6
    return_type: str

class high_order_term_relaxation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_10
    options: options_5
    return_type: str

class relative_permeability(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class capillary_pressure_as_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class porous_media(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    relative_permeability: relative_permeability
    capillary_pressure_as_diffusion: capillary_pressure_as_diffusion
    return_type: str

class enhanced_numerics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class alternate_bc_formulation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class analytical_thermodynamic_derivatives(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class compressible_flow(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enhanced_numerics: enhanced_numerics
    alternate_bc_formulation: alternate_bc_formulation
    analytical_thermodynamic_derivatives: analytical_thermodynamic_derivatives
    return_type: str

class thin_film(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class liquid_vof_factor(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boiling_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    thin_film: thin_film
    liquid_vof_factor: liquid_vof_factor
    return_type: str

class viscosity_averaging(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turb_visc_based_damping(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density_func_expo(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density_ratio_cutoff(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class n_smooth_for_interfacial_regims(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sm_relax_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscous_func_options(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class density_func_options(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exponent_smoothing_func(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exponent_density_func(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundry_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class near_wall_treatment_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interfacial_artificial_viscosity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    n_smooth_for_interfacial_regims: n_smooth_for_interfacial_regims
    sm_relax_factor: sm_relax_factor
    viscous_func_options: viscous_func_options
    density_func_options: density_func_options
    exponent_smoothing_func: exponent_smoothing_func
    exponent_density_func: exponent_density_func
    boundry_treatment: boundry_treatment
    near_wall_treatment: near_wall_treatment_1
    return_type: str

class viscous_flow(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    viscosity_averaging: viscosity_averaging
    turb_visc_based_damping: turb_visc_based_damping
    density_func_expo: density_func_expo
    density_ratio_cutoff: density_ratio_cutoff
    interfacial_artificial_viscosity: interfacial_artificial_viscosity
    return_type: str

class schnerr_evap_coeff(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class schnerr_cond_coeff(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_vapor_pressure_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_vapor_pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class display_clipped_pressure(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class old_treatment_for_turbulent_diffusion(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cavitation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    schnerr_evap_coeff: schnerr_evap_coeff
    schnerr_cond_coeff: schnerr_cond_coeff
    max_vapor_pressure_ratio: max_vapor_pressure_ratio
    min_vapor_pressure: min_vapor_pressure
    display_clipped_pressure: display_clipped_pressure
    turbulent_diffusion: turbulent_diffusion
    old_treatment_for_turbulent_diffusion: old_treatment_for_turbulent_diffusion
    return_type: str

class vof_from_min_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vof_from_max_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vof_to_min_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vof_to_max_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ia_norm_min_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_rel_humidity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class evaporation_condensation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    vof_from_min_limit: vof_from_min_limit
    vof_from_max_limit: vof_from_max_limit
    vof_to_min_limit: vof_to_min_limit
    vof_to_max_limit: vof_to_max_limit
    ia_norm_min_limit: ia_norm_min_limit
    max_rel_humidity: max_rel_humidity
    return_type: str

class heat_flux_relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class show_expert_options(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class two_resistance_boiling_framework(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boiling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    heat_flux_relaxation_factor: heat_flux_relaxation_factor
    show_expert_options: show_expert_options
    two_resistance_boiling_framework: two_resistance_boiling_framework
    return_type: str

class vof_min_seeding(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ia_grad_sym(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class area_density_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    vof_min_seeding: vof_min_seeding
    ia_grad_sym: ia_grad_sym
    return_type: str

class alternative_energy_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class heat_mass_transfer(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    cavitation: cavitation
    evaporation_condensation: evaporation_condensation
    boiling: boiling
    area_density: area_density_1
    alternative_energy_treatment: alternative_energy_treatment
    return_type: str

class smoothed_density_stabilization_method(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class num_of_density_smoothing(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class false_time_step_linearization(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_11(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dt_init_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dt_max(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dt_factor_min(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dt_factor_max(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_velocity_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_dt_advanced_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_11
    dt_init_limit: dt_init_limit
    dt_max: dt_max
    dt_factor_min: dt_factor_min
    dt_factor_max: dt_factor_max
    max_velocity_ratio: max_velocity_ratio
    return_type: str

class pseudo_transient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    smoothed_density_stabilization_method: smoothed_density_stabilization_method
    num_of_density_smoothing: num_of_density_smoothing
    false_time_step_linearization: false_time_step_linearization
    auto_dt_advanced_controls: auto_dt_advanced_controls
    return_type: str

class buoyancy_force_linearization(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blended_treatment_for_buoyancy_forces(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coupled_vof(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    buoyancy_force_linearization: buoyancy_force_linearization
    blended_treatment_for_buoyancy_forces: blended_treatment_for_buoyancy_forces
    return_type: str

class low_order_rhie_chow(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rhie_chow_flux(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    low_order_rhie_chow: low_order_rhie_chow
    return_type: str

class limit_pressure_correction_gradient(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skewness_correction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    limit_pressure_correction_gradient: limit_pressure_correction_gradient
    return_type: str

class p_v_coupling_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    coupled_vof: coupled_vof
    rhie_chow_flux: rhie_chow_flux
    skewness_correction: skewness_correction
    return_type: str

class outer_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_time_steps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_outer_iter(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_outer_iterations(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    initial_time_steps: initial_time_steps
    initial_outer_iter: initial_outer_iter
    return_type: str

class enable_instability_detector(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_cfl_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_cfl_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_velocity_limit(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unstable_event_outer_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class instability_detector(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_instability_detector: enable_instability_detector
    set_cfl_limit: set_cfl_limit
    set_cfl_type: set_cfl_type
    set_velocity_limit: set_velocity_limit
    unstable_event_outer_iterations: unstable_event_outer_iterations
    return_type: str

class hybrid_nita(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    outer_iterations: outer_iterations
    initial_outer_iterations: initial_outer_iterations
    instability_detector: instability_detector
    return_type: str

class solve_flow_last(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solve_exp_vof_at_end(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class equation_order(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    solve_flow_last: solve_flow_last
    solve_exp_vof_at_end: solve_exp_vof_at_end
    return_type: str

class enable_dynamic_strength(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_dynamic_strength_exponent(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_maximum_dynamic_strength(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class anti_diffusion(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_dynamic_strength: enable_dynamic_strength
    set_dynamic_strength_exponent: set_dynamic_strength_exponent
    set_maximum_dynamic_strength: set_maximum_dynamic_strength
    return_type: str

class advanced_stability_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pseudo_transient: pseudo_transient
    p_v_coupling: p_v_coupling_1
    hybrid_nita: hybrid_nita
    equation_order: equation_order
    anti_diffusion: anti_diffusion
    return_type: str

class recommended_defaults_for_existing_cases(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class old_default_of_operating_density_method(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class old_default_of_volume_fraction_smoothing(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class old_variant_of_pesto_for_cases_using_structured_mesh(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class revert_to_pre_r20_1_default_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    old_default_of_operating_density_method: old_default_of_operating_density_method
    old_default_of_volume_fraction_smoothing: old_default_of_volume_fraction_smoothing
    old_variant_of_pesto_for_cases_using_structured_mesh: old_variant_of_pesto_for_cases_using_structured_mesh
    return_type: str

class default_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    recommended_defaults_for_existing_cases: recommended_defaults_for_existing_cases
    revert_to_pre_r20_1_default_settings: revert_to_pre_r20_1_default_settings
    return_type: str

class pressure_corr_grad(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class face_pressure_calculation_method(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class exclude_transient_term_in_face_pressure_calc(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class face_pressure_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pressure_corr_grad: pressure_corr_grad
    face_pressure_calculation_method: face_pressure_calculation_method
    exclude_transient_term_in_face_pressure_calc: exclude_transient_term_in_face_pressure_calc
    return_type: str

class face_pressure_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    face_pressure_options: face_pressure_options
    return_type: str

class execute_settings_optimization(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class execute_advanced_stabilization(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class blended_compressive_scheme(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pseudo_time_stabilization(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class additional_stabilization_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    blended_compressive_scheme: blended_compressive_scheme
    pseudo_time_stabilization: pseudo_time_stabilization
    return_type: str

class execute_additional_stability_controls(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_velocity_limiting(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_vol_mag(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vol_frac_cutoff(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_velocity_and_vof_cutoffs_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    max_vol_mag: max_vol_mag
    vol_frac_cutoff: vol_frac_cutoff
    return_type: str

class set_velocity_and_vof_cutoffs(NamedObject[set_velocity_and_vof_cutoffs_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: set_velocity_and_vof_cutoffs_child
    return_type: str

class set_damping_strengths_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_damping_strengths(NamedObject[set_damping_strengths_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: set_damping_strengths_child
    return_type: str

class set_velocity_cutoff(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_damping_strength(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_5(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity_limiting_treatment(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_velocity_limiting: enable_velocity_limiting
    set_velocity_and_vof_cutoffs: set_velocity_and_vof_cutoffs
    set_damping_strengths: set_damping_strengths
    set_velocity_cutoff: set_velocity_cutoff
    set_damping_strength: set_damping_strength
    verbosity: verbosity_5
    return_type: str

class solution_stabilization(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    execute_settings_optimization: execute_settings_optimization
    execute_advanced_stabilization: execute_advanced_stabilization
    additional_stabilization_controls: additional_stabilization_controls
    execute_additional_stability_controls: execute_additional_stability_controls
    velocity_limiting_treatment: velocity_limiting_treatment
    return_type: str

class multiphase_numerics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    porous_media: porous_media
    compressible_flow: compressible_flow
    boiling_parameters: boiling_parameters
    viscous_flow: viscous_flow
    heat_mass_transfer: heat_mass_transfer
    advanced_stability_controls: advanced_stability_controls
    default_controls: default_controls
    face_pressure_controls: face_pressure_controls
    solution_stabilization: solution_stabilization
    return_type: str

class nb_gradient(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nb_gradient_dbns(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nb_gradient_boundary_option(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    nb_gradient: nb_gradient
    nb_gradient_dbns: nb_gradient_dbns
    return_type: str

class nita(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_6(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skewness_neighbor_coupling(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_12(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_6(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multi_phase_setting(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable: enable_12
    options: options_6
    return_type: str

class single_phase_setting(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hybrid_nita_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    multi_phase_setting: multi_phase_setting
    single_phase_setting: single_phase_setting
    return_type: str

class nita_expert_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    verbosity: verbosity_6
    skewness_neighbor_coupling: skewness_neighbor_coupling
    hybrid_nita_settings: hybrid_nita_settings
    return_type: str

class high_order_pressure(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interpolation_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class orphan_cell_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mass_flux_correction_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hybrid_mode_selection(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expert_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    mass_flux_correction_method: mass_flux_correction_method
    hybrid_mode_selection: hybrid_mode_selection
    return_type: str

class overset_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    high_order_pressure: high_order_pressure
    interpolation_method: interpolation_method
    orphan_cell_treatment: orphan_cell_treatment
    expert: expert_2
    return_type: str

class phase_based_vof_discretization_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_based_vof_discretization(NamedObject[phase_based_vof_discretization_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: phase_based_vof_discretization_child
    return_type: str

class reduced_rank_extrapolation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class subspace_size(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skip_iter_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reduced_rank_extrapolation_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    subspace_size: subspace_size
    skip_iter_count: skip_iter_count
    return_type: str

class residual_smoothing_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class residual_smoothing_iter_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class residual_smoothing(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    residual_smoothing_factor: residual_smoothing_factor
    residual_smoothing_iter_count: residual_smoothing_iter_count
    return_type: str

class high_order_rc(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class high_order_rc_hybrid_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class force_treatment_of_unsteady_rc(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class unstructured_var_presto_scheme(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class new_framework_for_vof_specific_node_based_treatment(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vof_numerics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    high_order_rc: high_order_rc
    high_order_rc_hybrid_treatment: high_order_rc_hybrid_treatment
    force_treatment_of_unsteady_rc: force_treatment_of_unsteady_rc
    unstructured_var_presto_scheme: unstructured_var_presto_scheme
    new_framework_for_vof_specific_node_based_treatment: new_framework_for_vof_specific_node_based_treatment
    return_type: str

class turbulence_options(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class warped_face_gradient_correction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    turbulence_options: turbulence_options
    def enable(self, enable: bool, gradient_correction_mode: str):
        """
        Enable Warped-Face Gradient Correction.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
            gradient_correction_mode : str
                'gradient_correction_mode' child.
        """
    return_type: str

class methods(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    p_v_coupling: p_v_coupling
    flux_type: flux_type
    discretization_scheme: discretization_scheme
    pseudo_time_method: pseudo_time_method
    unsteady_1st_order: unsteady_1st_order
    unsteady_2nd_order: unsteady_2nd_order
    unsteady_2nd_order_bounded: unsteady_2nd_order_bounded
    unsteady_global_time: unsteady_global_time
    accelerated_non_iterative_time_marching: accelerated_non_iterative_time_marching
    convergence_acceleration_for_stretched_meshes: convergence_acceleration_for_stretched_meshes
    expert: expert_1
    frozen_flux: frozen_flux
    gradient_scheme: gradient_scheme
    high_order_term_relaxation: high_order_term_relaxation
    multiphase_numerics: multiphase_numerics
    nb_gradient_boundary_option: nb_gradient_boundary_option
    nita: nita
    nita_expert_controls: nita_expert_controls
    overset: overset_1
    phase_based_vof_discretization: phase_based_vof_discretization
    reduced_rank_extrapolation: reduced_rank_extrapolation
    reduced_rank_extrapolation_options: reduced_rank_extrapolation_options
    residual_smoothing: residual_smoothing
    vof_numerics: vof_numerics
    warped_face_gradient_correction: warped_face_gradient_correction
    def set_solution_methods_to_default(self):
        """
        Set solution methods to default values.
        """
    return_type: str

class courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skewness_correction_itr_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class neighbor_correction_itr_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skewness_neighbor_coupling_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vof_correction_itr_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_fraction_courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class explicit_momentum_under_relaxation(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class explicit_pressure_under_relaxation(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class explicit_volume_fraction_under_relaxation(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p_v_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    skewness_correction_itr_count: skewness_correction_itr_count
    neighbor_correction_itr_count: neighbor_correction_itr_count
    skewness_neighbor_coupling: skewness_neighbor_coupling_1
    vof_correction_itr_count: vof_correction_itr_count
    flow_courant_number: flow_courant_number
    volume_fraction_courant_number: volume_fraction_courant_number
    explicit_momentum_under_relaxation: explicit_momentum_under_relaxation
    explicit_pressure_under_relaxation: explicit_pressure_under_relaxation
    explicit_volume_fraction_under_relaxation: explicit_volume_fraction_under_relaxation
    return_type: str

class relaxation_factor_1_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relaxation_factor_1(NamedObject[relaxation_factor_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: relaxation_factor_1_child
    return_type: str

class under_relaxation_1_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class under_relaxation_1(NamedObject[under_relaxation_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: under_relaxation_1_child
    return_type: str

class pseudo_time_courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pseudo_time_step_method_solid_zone(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_size_scale_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pseudo_time_method_local_time_step(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pseudo_time_courant_number: pseudo_time_courant_number
    pseudo_time_step_method_solid_zone: pseudo_time_step_method_solid_zone
    time_step_size_scale_factor: time_step_size_scale_factor
    return_type: str

class local_dt_dualts_relax_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class local_dt_dualts_relax(NamedObject[local_dt_dualts_relax_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: local_dt_dualts_relax_child
    return_type: str

class global_dt_pseudo_relax_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class global_dt_pseudo_relax(NamedObject[global_dt_pseudo_relax_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: global_dt_pseudo_relax_child
    return_type: str

class pseudo_time_explicit_relaxation_factor(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    local_dt_dualts_relax: local_dt_dualts_relax
    global_dt_pseudo_relax: global_dt_pseudo_relax
    return_type: str

class under_relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class explicit_relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expert_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    under_relaxation_factor: under_relaxation_factor
    explicit_relaxation_factor: explicit_relaxation_factor
    return_type: str

class relative_convergence_criterion(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_iter_per_timestep_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class acoustics_wave_eqn_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    expert: expert_3
    relative_convergence_criterion: relative_convergence_criterion
    max_iter_per_timestep_count: max_iter_per_timestep_count
    return_type: str

class solution_stabilization_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_7(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iter_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solution_stabilization_persistence(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class persistence_fixed_time_steps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class persistence_fixed_duration(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class extrapolation_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    iter_count: iter_count
    solution_stabilization_persistence: solution_stabilization_persistence
    persistence_fixed_time_steps: persistence_fixed_time_steps
    persistence_fixed_duration: persistence_fixed_duration
    extrapolation_method: extrapolation_method
    return_type: str

class first_to_second_order_blending_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class first_to_second_order_blending_list(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scheme_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_skew_diffusion_exclude(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scalars_skew_diffusion_exclude(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rhie_chow_flux_specify(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rhie_chow_method(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spatial(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    first_to_second_order_blending: first_to_second_order_blending_1
    first_to_second_order_blending_list: first_to_second_order_blending_list
    scheme: scheme_1
    flow_skew_diffusion_exclude: flow_skew_diffusion_exclude
    scalars_skew_diffusion_exclude: scalars_skew_diffusion_exclude
    rhie_chow_flux_specify: rhie_chow_flux_specify
    rhie_chow_method: rhie_chow_method
    return_type: str

class transient_parameters_specify(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class transient_scheme(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_scale_modification_method(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_scale_modification_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class transient(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    transient_parameters_specify: transient_parameters_specify
    transient_scheme: transient_scheme
    time_scale_modification_method: time_scale_modification_method
    time_scale_modification_factor: time_scale_modification_factor
    return_type: str

class enforce_laplace_coarsening(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class increase_pre_sweeps(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pre_sweeps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class specify_coarsening_rate(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_rate(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class amg(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enforce_laplace_coarsening: enforce_laplace_coarsening
    increase_pre_sweeps: increase_pre_sweeps
    pre_sweeps: pre_sweeps
    specify_coarsening_rate: specify_coarsening_rate
    coarsen_rate: coarsen_rate
    return_type: str

class model_ramping(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ramp_flow(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ramp_turbulence(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ramp_scalars(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class models_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    model_ramping: model_ramping
    ramp_flow: ramp_flow
    ramp_turbulence: ramp_turbulence
    ramp_scalars: ramp_scalars
    return_type: str

class pv_coupling_controls(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pv_coupling_method(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gradient_controls(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class specify_gradient_method(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class methods_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pv_coupling_controls: pv_coupling_controls
    pv_coupling_method: pv_coupling_method
    gradient_controls: gradient_controls
    specify_gradient_method: specify_gradient_method
    return_type: str

class compute_statistics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class statistics_level(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class miscellaneous(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    compute_statistics: compute_statistics
    statistics_level: statistics_level
    return_type: str

class contact_solution_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    solution_stabilization: solution_stabilization_1
    verbosity: verbosity_7
    parameters: parameters
    spatial: spatial
    transient: transient
    amg: amg
    models: models_2
    methods: methods_1
    miscellaneous: miscellaneous
    def set_settings_to_default(self):
        """
        Set contact solution stabilization to default.
        """
    return_type: str

class equations_child(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class equations(NamedObject[equations_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: equations_child
    return_type: str

class min_pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_pressure(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_temperature_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_temperature(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_tke(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_lam_tke(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_des_tke(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_epsilon(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_des_epsilon(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_v2f_tke(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_v2f_epsilon(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_vel_var_scale(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_elliptic_relax_func(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_omega(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_des_omega(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_turb_visc_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class positivity_rate(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_vol_frac_for_matrix_sol(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class limits(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    min_pressure: min_pressure
    max_pressure: max_pressure
    min_temperature: min_temperature_1
    max_temperature: max_temperature
    min_tke: min_tke
    min_lam_tke: min_lam_tke
    min_des_tke: min_des_tke
    min_epsilon: min_epsilon
    min_des_epsilon: min_des_epsilon
    min_v2f_tke: min_v2f_tke
    min_v2f_epsilon: min_v2f_epsilon
    min_vel_var_scale: min_vel_var_scale
    min_elliptic_relax_func: min_elliptic_relax_func
    min_omega: min_omega
    min_des_omega: min_des_omega
    max_turb_visc_ratio: max_turb_visc_ratio
    positivity_rate: positivity_rate
    min_vol_frac_for_matrix_sol: min_vol_frac_for_matrix_sol
    return_type: str

class cycle_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class termination_criteria(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class residual_reduction_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stabilization(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mg_controls_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    cycle_type: cycle_type
    termination_criteria: termination_criteria
    residual_reduction_tolerance: residual_reduction_tolerance
    method: method_2
    stabilization: stabilization
    return_type: str

class mg_controls(NamedObject[mg_controls_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mg_controls_child
    return_type: str

class pre_sweeps_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class post_sweeps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_cycle(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_cycle_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_sweeps: pre_sweeps_1
    post_sweeps: post_sweeps
    max_cycle: max_cycle
    return_type: str

class max_coarse_levels(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_by_interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class conservative_coarsening(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aggressive_coarsening(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class laplace_coarsening(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsening_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    max_coarse_levels: max_coarse_levels
    coarsen_by_interval: coarsen_by_interval
    conservative_coarsening: conservative_coarsening
    aggressive_coarsening: aggressive_coarsening
    laplace_coarsening: laplace_coarsening
    return_type: str

class smoother_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scalar_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    fixed_cycle_parameters: fixed_cycle_parameters
    coarsening_parameters: coarsening_parameters
    smoother_type: smoother_type
    return_type: str

class pre_sweeps_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class post_sweeps_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_cycle_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_cycle_parameters_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_sweeps: pre_sweeps_2
    post_sweeps: post_sweeps_1
    max_cycle: max_cycle_1
    return_type: str

class max_coarse_levels_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_by_interval_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aggressive_coarsening_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsening_parameters_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    max_coarse_levels: max_coarse_levels_1
    coarsen_by_interval: coarsen_by_interval_1
    conservative_coarsening: conservative_coarsening
    aggressive_coarsening: aggressive_coarsening_1
    laplace_coarsening: laplace_coarsening
    return_type: str

class smoother_type_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coupled_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    fixed_cycle_parameters: fixed_cycle_parameters_1
    coarsening_parameters: coarsening_parameters_1
    smoother_type: smoother_type_1
    return_type: str

class max_fine_relaxations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_coarse_relaxations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flexible_cycle_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    max_fine_relaxations: max_fine_relaxations
    max_coarse_relaxations: max_coarse_relaxations
    return_type: str

class verbosity_8(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_7(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    verbosity: verbosity_8
    return_type: str

class amg_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    scalar_parameters: scalar_parameters
    coupled_parameters: coupled_parameters
    flexible_cycle_parameters: flexible_cycle_parameters
    options: options_7
    return_type: str

class pre_sweeps_3(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class post_sweeps_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_cycle_parameters_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pre_sweeps: pre_sweeps_3
    post_sweeps: post_sweeps_2
    return_type: str

class max_coarse_levels_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_by_interval_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsening_parameters_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    max_coarse_levels: max_coarse_levels_2
    coarsen_by_interval: coarsen_by_interval_2
    return_type: str

class courant_number_reduction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class correction_reduction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class correction_smoothing(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_correction_reduction(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relaxation_factor_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    courant_number_reduction: courant_number_reduction
    correction_reduction: correction_reduction
    correction_smoothing: correction_smoothing
    species_correction_reduction: species_correction_reduction
    return_type: str

class fas_mg_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    fixed_cycle_parameters: fixed_cycle_parameters_2
    coarsening_parameters: coarsening_parameters_2
    relaxation_factor: relaxation_factor_2
    options: options_7
    return_type: str

class enable_gpu(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class term_criterion(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solver_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_num_cycle(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_by_size(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pre_sweep(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class post_sweep(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class smoother(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class amg_gpgpu_options_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_gpu: enable_gpu
    term_criterion: term_criterion
    solver: solver_1
    max_num_cycle: max_num_cycle
    coarsen_by_size: coarsen_by_size
    pre_sweep: pre_sweep
    post_sweep: post_sweep
    smoother: smoother
    return_type: str

class amg_gpgpu_options(NamedObject[amg_gpgpu_options_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: amg_gpgpu_options_child
    return_type: str

class multi_grid(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    mg_controls: mg_controls
    amg_controls: amg_controls
    fas_mg_controls: fas_mg_controls
    amg_gpgpu_options: amg_gpgpu_options
    return_type: str

class coefficient(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class update_dissipation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class update_viscous(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multi_stage_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    coefficient: coefficient
    update_dissipation: update_dissipation
    update_viscous: update_viscous
    return_type: str

class multi_stage(ListObject[multi_stage_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: multi_stage_child
    return_type: str

class limiter_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cell_to_limiting(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class limiter_filter(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class spatial_discretization_limiter(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    limiter_type: limiter_type
    cell_to_limiting: cell_to_limiting
    limiter_filter: limiter_filter
    return_type: str

class enable_pseudo_time_method(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pseudo_time_scale_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class implicit_under_relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class local_dt_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_pseudo_time_method: enable_pseudo_time_method
    pseudo_time_scale_factor: pseudo_time_scale_factor
    implicit_under_relaxation_factor: implicit_under_relaxation_factor
    return_type: str

class local_dt(NamedObject[local_dt_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: local_dt_child
    return_type: str

class global_dt_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_pseudo_time_method: enable_pseudo_time_method
    pseudo_time_scale_factor: pseudo_time_scale_factor
    implicit_under_relaxation_factor: implicit_under_relaxation_factor
    return_type: str

class global_dt(NamedObject[global_dt_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: global_dt_child
    return_type: str

class pseudo_time_method_usage(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    local_dt: local_dt
    global_dt: global_dt
    return_type: str

class expert_4(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    spatial_discretization_limiter: spatial_discretization_limiter
    pseudo_time_method_usage: pseudo_time_method_usage
    return_type: str

class two_stage(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class default_multi_stage(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class runge_kutta(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    two_stage: two_stage
    default_multi_stage: default_multi_stage
    return_type: str

class fast_transient_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    runge_kutta: runge_kutta
    return_type: str

class relaxation_method_1(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class correction_tolerance_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class correction_tolerance(NamedObject[correction_tolerance_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: correction_tolerance_child
    return_type: str

class flux(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gradient(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class anisotropic_solid_heat_transfer(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    flux: flux
    gradient: gradient
    return_type: str

class advanced(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    multi_grid: multi_grid
    multi_stage: multi_stage
    expert: expert_4
    fast_transient_settings: fast_transient_settings
    relaxation_method: relaxation_method_1
    correction_tolerance: correction_tolerance
    anisotropic_solid_heat_transfer: anisotropic_solid_heat_transfer
    return_type: str

class controls_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    courant_number: courant_number
    p_v_controls: p_v_controls
    relaxation_factor: relaxation_factor_1
    under_relaxation: under_relaxation_1
    pseudo_time_method_local_time_step: pseudo_time_method_local_time_step
    pseudo_time_explicit_relaxation_factor: pseudo_time_explicit_relaxation_factor
    acoustics_wave_eqn_controls: acoustics_wave_eqn_controls
    contact_solution_controls: contact_solution_controls
    equations: equations
    limits: limits
    advanced: advanced
    def reset_solution_controls(self):
        """
        'reset_solution_controls' command.
        """
    def reset_amg_controls(self):
        """
        'reset_amg_controls' command.
        """
    def reset_multi_stage_parameters(self):
        """
        'reset_multi_stage_parameters' command.
        """
    def reset_limits(self):
        """
        'reset_limits' command.
        """
    def reset_pseudo_time_method_generic(self):
        """
        'reset_pseudo_time_method_generic' command.
        """
    def reset_pseudo_time_method_equations(self):
        """
        'reset_pseudo_time_method_equations' command.
        """
    def reset_pseudo_time_method_relaxations(self):
        """
        'reset_pseudo_time_method_relaxations' command.
        """
    def reset_pseudo_time_method_scale_factors(self):
        """
        'reset_pseudo_time_method_scale_factors' command.
        """
    return_type: str

class zone_ids(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class retain_instantaneous_values(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class old_props(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone_names_1(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class average_over(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class per_zone(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mesh_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    zone_ids: zone_ids
    retain_instantaneous_values: retain_instantaneous_values
    old_props: old_props
    zone_names: zone_names_1
    zone_list: zone_list
    average_over: average_over
    per_zone: per_zone
    return_type: str

class mesh_1(NamedObject[mesh_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: mesh_1_child
    return_type: str

class report_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class custom_vector(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class field(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surfaces_3(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class geometry_4(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class physics_1(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_26(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class per_surface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_names(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_ids(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    custom_vector: custom_vector
    field: field
    surfaces: surfaces_3
    geometry: geometry_4
    physics: physics_1
    retain_instantaneous_values: retain_instantaneous_values
    phase: phase_26
    average_over: average_over
    per_surface: per_surface
    old_props: old_props
    surface_names: surface_names
    surface_ids: surface_ids
    return_type: str

class surface_1(NamedObject[surface_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: surface_1_child
    return_type: str

class expr_list(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    geometry: geometry_4
    physics: physics_1
    field: field
    retain_instantaneous_values: retain_instantaneous_values
    phase: phase_26
    average_over: average_over
    per_zone: per_zone
    old_props: old_props
    zone_names: zone_names_1
    expr_list: expr_list
    zone_list: zone_list
    return_type: str

class volume(NamedObject[volume_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: volume_child
    return_type: str

class scaled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thread_names(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thread_ids(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class force_vector(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class force_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    geometry: geometry_4
    physics: physics_1
    retain_instantaneous_values: retain_instantaneous_values
    scaled: scaled
    average_over: average_over
    per_zone: per_zone
    thread_names: thread_names
    thread_ids: thread_ids
    old_props: old_props
    reference_frame: reference_frame
    force_vector: force_vector
    return_type: str

class force(NamedObject[force_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: force_child
    return_type: str

class lift_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    geometry: geometry_4
    physics: physics_1
    retain_instantaneous_values: retain_instantaneous_values
    scaled: scaled
    average_over: average_over
    per_zone: per_zone
    thread_names: thread_names
    thread_ids: thread_ids
    old_props: old_props
    reference_frame: reference_frame
    force_vector: force_vector
    return_type: str

class lift(NamedObject[lift_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: lift_child
    return_type: str

class drag_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    geometry: geometry_4
    physics: physics_1
    retain_instantaneous_values: retain_instantaneous_values
    scaled: scaled
    average_over: average_over
    per_zone: per_zone
    thread_names: thread_names
    thread_ids: thread_ids
    old_props: old_props
    reference_frame: reference_frame
    force_vector: force_vector
    return_type: str

class drag(NamedObject[drag_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: drag_child
    return_type: str

class mom_axis(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mom_center(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class moment_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    retain_instantaneous_values: retain_instantaneous_values
    scaled: scaled
    average_over: average_over
    per_zone: per_zone
    thread_names: thread_names
    thread_ids: thread_ids
    old_props: old_props
    reference_frame: reference_frame
    mom_axis: mom_axis
    mom_center: mom_center
    return_type: str

class moment(NamedObject[moment_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: moment_child
    return_type: str

class flux_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    geometry: geometry_4
    physics: physics_1
    retain_instantaneous_values: retain_instantaneous_values
    phase: phase_26
    average_over: average_over
    per_zone: per_zone
    old_props: old_props
    zone_names: zone_names_1
    zone_ids: zone_ids
    return_type: str

class flux_1(NamedObject[flux_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: flux_1_child
    return_type: str

class user_specified_origin_and_axis(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_1(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mass_criterion(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_zones_names(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_zones(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inj_mass_rate_last_tstp(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inj_mass_rate_last_flow(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inj_mass_rate_prev_mass(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inj_mass_rate_prev_time(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class show_unsteady_rate(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class per_injection(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class injection_list(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class injection_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    user_specified_origin_and_axis: user_specified_origin_and_axis
    origin: origin
    axis: axis_1
    mass_criterion: mass_criterion
    physics: physics_1
    boundary_zones_names: boundary_zones_names
    boundary_zones: boundary_zones
    retain_instantaneous_values: retain_instantaneous_values
    inj_mass_rate_last_tstp: inj_mass_rate_last_tstp
    inj_mass_rate_last_flow: inj_mass_rate_last_flow
    inj_mass_rate_prev_mass: inj_mass_rate_prev_mass
    inj_mass_rate_prev_time: inj_mass_rate_prev_time
    show_unsteady_rate: show_unsteady_rate
    old_props: old_props
    average_over: average_over
    per_injection: per_injection
    injection_list: injection_list
    return_type: str

class injection(NamedObject[injection_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: injection_child
    return_type: str

class input_params(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class function_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_5_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    retain_instantaneous_values: retain_instantaneous_values
    input_params: input_params
    function_name: function_name
    average_over: average_over
    old_props: old_props
    return_type: str

class user_defined_5(NamedObject[user_defined_5_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: user_defined_5_child
    return_type: str

class realcomponent(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nodal_diameters(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class normalization(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class integrate_over(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aeromechanics_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    realcomponent: realcomponent
    nodal_diameters: nodal_diameters
    normalization: normalization
    integrate_over: integrate_over
    average_over: average_over
    per_zone: per_zone
    old_props: old_props
    thread_names: thread_names
    thread_ids: thread_ids
    return_type: str

class aeromechanics(NamedObject[aeromechanics_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: aeromechanics_child
    return_type: str

class icing_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    report_type: report_type
    old_props: old_props
    return_type: str

class icing(NamedObject[icing_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: icing_child
    return_type: str

class list_valid_report_names(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class define(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expr_value(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class expression_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    list_valid_report_names: list_valid_report_names
    define: define
    expr_value: expr_value
    average_over: average_over
    old_props: old_props
    return_type: str

class expression_1(NamedObject[expression_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: expression_1_child
    return_type: str

class single_val_expression_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    retain_instantaneous_values: retain_instantaneous_values
    list_valid_report_names: list_valid_report_names
    define: define
    average_over: average_over
    old_props: old_props
    return_type: str

class single_val_expression(NamedObject[single_val_expression_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: single_val_expression_child
    return_type: str

class custom_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    return_type: str

class custom(NamedObject[custom_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: custom_child
    return_type: str

class report_definitions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    mesh: mesh_1
    surface: surface_1
    volume: volume
    force: force
    lift: lift
    drag: drag
    moment: moment
    flux: flux_1
    injection: injection
    user_defined: user_defined_5
    aeromechanics: aeromechanics
    icing: icing
    expression: expression_1
    single_val_expression: single_val_expression
    custom: custom
    def compute(self, report_defs: list[str]):
        """
        'compute' command.
        """
    def copy(self, copy_from: str, copy_to: str):
        """
        'copy' command.
        """
    def list(self):
        """
        'list' command.
        """
    return_type: str

class file_name_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class frequency(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_frequency(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class itr_index(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class run_index(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class frequency_of(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class print_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class active(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class write_instantaneous_values(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class report_files_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_1
    old_props: old_props
    file_name: file_name_2
    frequency: frequency
    flow_frequency: flow_frequency
    itr_index: itr_index
    run_index: run_index
    frequency_of: frequency_of
    report_defs: report_defs
    print: print_2
    active: active
    write_instantaneous_values: write_instantaneous_values
    return_type: str

class report_files(NamedObject[report_files_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: report_files_child
    return_type: str

class plot_window(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class title(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_label(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_label(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class evaluate(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class plot_instantaneous_values(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class report_plots_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_1
    plot_window: plot_window
    old_props: old_props
    frequency: frequency
    flow_frequency: flow_frequency
    frequency_of: frequency_of
    report_defs: report_defs
    print: print_2
    title: title
    x_label: x_label
    y_label: y_label
    active: active
    evaluate: evaluate
    plot_instantaneous_values: plot_instantaneous_values
    return_type: str

class report_plots(NamedObject[report_plots_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: report_plots_child
    return_type: str

class previous_values_to_consider(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_values_to_ignore(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iteration_at_creation_or_edit(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stop_criterion(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class report_defs_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class plot(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cov(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class previous_values(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convergence_reports_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_1
    old_props: old_props
    previous_values_to_consider: previous_values_to_consider
    initial_values_to_ignore: initial_values_to_ignore
    iteration_at_creation_or_edit: iteration_at_creation_or_edit
    stop_criterion: stop_criterion
    report_defs: report_defs_1
    print: print_2
    plot: plot
    cov: cov
    active: active
    x_label: x_label
    previous_values: previous_values
    return_type: str

class convergence_reports(NamedObject[convergence_reports_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: convergence_reports_child
    return_type: str

class frequency_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class condition(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class check_for(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class convergence_conditions(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    convergence_reports: convergence_reports
    frequency: frequency_1
    condition: condition
    check_for: check_for
    return_type: str

class monitor(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    report_files: report_files
    report_plots: report_plots
    convergence_conditions: convergence_conditions
    return_type: str

class python_name_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_point(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_point(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inside(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class create_volume_surface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hexahedron(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    min_point: min_point
    max_point: max_point
    inside: inside
    create_volume_surface: create_volume_surface
    return_type: str

class center(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class radius(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sphere(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    center: center
    radius: radius
    inside: inside
    create_volume_surface: create_volume_surface
    return_type: str

class axis_begin(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_end(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cylinder(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    axis_begin: axis_begin
    axis_end: axis_end
    radius: radius
    inside: inside
    create_volume_surface: create_volume_surface
    return_type: str

class cell_distance(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class normal_distance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_volume(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_growth(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_distance(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    boundary_volume: boundary_volume
    volume_growth: volume_growth
    return_type: str

class distance_option(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    cell_distance: cell_distance
    normal_distance: normal_distance
    volume_distance: volume_distance
    return_type: str

class boundary(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    distance_option: distance_option
    boundary_list: boundary_list
    create_volume_surface: create_volume_surface
    return_type: str

class limiters(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_max(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class value1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class value2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class in_range(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    value1: value1
    value2: value2
    return_type: str

class except_in_range(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    value1: value1
    value2: value2
    return_type: str

class top_value_cells(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class low_value_cells(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class less_than(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class more_than(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lower(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class upper(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class between_std_dev(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    lower: lower
    upper: upper
    return_type: str

class outside_std_dev(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    lower: lower
    upper: upper
    return_type: str

class less_than_std_dev(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class more_than_std_dev(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_12(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    min_max: min_max
    in_range: in_range
    except_in_range: except_in_range
    top_value_cells: top_value_cells
    low_value_cells: low_value_cells
    less_than: less_than
    more_than: more_than
    between_std_dev: between_std_dev
    outside_std_dev: outside_std_dev
    less_than_std_dev: less_than_std_dev
    more_than_std_dev: more_than_std_dev
    return_type: str

class none_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_by_global_average(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_by_zone_average(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_by_global_maximum(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_by_zone_maximum(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scaling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    none: none_1
    scale_by_global_average: scale_by_global_average
    scale_by_zone_average: scale_by_zone_average
    scale_by_global_maximum: scale_by_global_maximum
    scale_by_zone_maximum: scale_by_zone_maximum
    return_type: str

class gradient_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class curvature(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hessian(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class derivative(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    none: none_1
    gradient: gradient_1
    curvature: curvature
    hessian: hessian
    return_type: str

class size_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class field_value(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    field: field
    option: option_12
    scaling: scaling
    derivative: derivative
    size_ratio: size_ratio
    create_volume_surface: create_volume_surface
    return_type: str

class equation_for_residual(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class threshold(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class residual(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    equation_for_residual: equation_for_residual
    threshold: threshold
    return_type: str

class volume_magnitude(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_change(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class volume_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    volume_magnitude: volume_magnitude
    volume_change: volume_change
    return_type: str

class yplus_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ystar(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_13(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    yplus: yplus_1
    ystar: ystar
    return_type: str

class min_allowed(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_allowed(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_zones(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class phase_27(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class yplus_star(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_13
    min_allowed: min_allowed
    max_allowed: max_allowed
    wall_zones: wall_zones
    phase: phase_27
    return_type: str

class yplus_ystar(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_13
    min_allowed: min_allowed
    max_allowed: max_allowed
    wall_zones: wall_zones
    phase: phase_27
    return_type: str

class type_7(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    hexahedron: hexahedron
    sphere: sphere
    cylinder: cylinder
    boundary: boundary
    limiters: limiters
    field_value: field_value
    residual: residual
    volume: volume_1
    yplus_star: yplus_star
    yplus_ystar: yplus_ystar
    return_type: str

class draw_mesh(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class filled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class marker(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class marker_symbol(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class marker_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wireframe(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class display_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    draw_mesh: draw_mesh
    filled: filled
    marker: marker
    marker_symbol: marker_symbol
    marker_size: marker_size
    wireframe: wireframe
    color: color
    return_type: str

class cell_registers_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_1
    python_name_1: python_name_1
    type: type_7
    display_options: display_options
    return_type: str

class cell_registers(NamedObject[cell_registers_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: cell_registers_child
    return_type: str

class initialization_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reference_frame_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class defaults_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class defaults(NamedObject[defaults_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: defaults_child
    return_type: str

class viscous_terms(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_reactions(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_turbulent_viscosity_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reset_to_defaults(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fmg_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    viscous_terms: viscous_terms
    species_reactions: species_reactions
    set_turbulent_viscosity_ratio: set_turbulent_viscosity_ratio
    reset_to_defaults: reset_to_defaults
    return_type: str

class enabled_3(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_intensity(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_viscosity_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class localized_turb_init(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_3
    turbulent_intensity: turbulent_intensity
    turbulent_viscosity_ratio: turbulent_viscosity_ratio
    return_type: str

class iter_count_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class explicit_urf(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_pressure(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class external_aero(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class const_velocity(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class general_settings_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    iter_count: iter_count_1
    explicit_urf: explicit_urf
    reference_frame: reference_frame_1
    initial_pressure: initial_pressure
    external_aero: external_aero
    const_velocity: const_velocity
    return_type: str

class averaged_turbulent_parameters(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscosity_ratio_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class turbulent_setting(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    averaged_turbulent_parameters: averaged_turbulent_parameters
    turbulent_intensity: turbulent_intensity
    viscosity_ratio: viscosity_ratio_1
    return_type: str

class user_specified_species(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_3_child_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_3_child(NamedObject[species_3_child_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: species_3_child_child
    return_type: str

class species_3(NamedObject[species_3_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: species_3_child
    return_type: str

class species_setting(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    user_specified_species: user_specified_species
    species: species_3
    return_type: str

class hybrid_init_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    general_settings: general_settings_1
    turbulent_setting: turbulent_setting
    species_setting: species_setting
    return_type: str

class patch_reconstructed_interface(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_volumetric_smoothing(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class smoothing_relaxation_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vof_smooth_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    patch_reconstructed_interface: patch_reconstructed_interface
    use_volumetric_smoothing: use_volumetric_smoothing
    smoothing_relaxation_factor: smoothing_relaxation_factor
    def execute_smoothing(self):
        """
        Execute volumetric smoothing for volume fraction.
        """
    return_type: str

class patch(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    vof_smooth_options: vof_smooth_options
    def calculate_patch(self, domain: str, cell_zones: list[str], register_id: list[str], variable: str, patch_velocity: bool, use_custom_field_function: bool, custom_field_function_name: str, value: float | str):
        """
        Patch a value for a flow variable in the domain.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            cell_zones : List
                'cell_zones' child.
            register_id : List
                'register_id' child.
            variable : str
                'variable' child.
            patch_velocity : bool
                'patch_velocity' child.
            use_custom_field_function : bool
                'use_custom_field_function' child.
            custom_field_function_name : str
                'custom_field_function_name' child.
            value : real
                'value' child.
        """
    return_type: str

class boundary_thread(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flat_init(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wavy_surface_init(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class open_channel_auto_init(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    boundary_thread: boundary_thread
    flat_init: flat_init
    wavy_surface_init: wavy_surface_init
    return_type: str

class fmg_courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_fmg_verbose(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fmg_initialization(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    fmg_courant_number: fmg_courant_number
    enable_fmg_verbose: enable_fmg_verbose
    def customize_fmg_initialization(self, multi_level_grid: int, residual_reduction_level: list[float | str], cycle_count: list[float | str]):
        """
        'customize_fmg_initialization' command.
        """
    return_type: str

class initialization(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    initialization_type: initialization_type
    reference_frame: reference_frame_1
    defaults: defaults
    fmg_options: fmg_options
    localized_turb_init: localized_turb_init
    hybrid_init_options: hybrid_init_options
    patch: patch
    open_channel_auto_init: open_channel_auto_init
    fmg_initialization: fmg_initialization
    def initialize(self):
        """
        'initialize' command.
        """
    def compute_defaults(self, from_zone_type: str, from_zone_name: str, phase: str):
        """
        'compute_defaults' command.
        """
    def fmg_initialize(self):
        """
        Initialize using the full-multigrid initialization (FMG).
        """
    def standard_initialize(self):
        """
        Initialize the flow field with the current default values.
        """
    def hybrid_initialize(self):
        """
        Initialize using the hybrid initialization method.
        """
    def list_defaults(self):
        """
        List default values.
        """
    def init_turb_vel_fluctuations(self):
        """
        Initialize turbulent velocity fluctuations.
        """
    def init_flow_statistics(self):
        """
        Initialize statistics.
        """
    def show_iterations_sampled(self):
        """
        'show_iterations_sampled' command.
        """
    def show_time_sampled(self):
        """
        Display the amount of simulated time covered by the data sampled for unsteady statistics.
        """
    def dpm_reset(self):
        """
        Reset discrete phase source terms to zero.
        """
    def lwf_reset(self):
        """
        Delete wall film particles and initialize wall film variables to zero.
        """
    def init_acoustics_options(self, set_ramping_length: bool, time_step_count: int):
        """
        'init_acoustics_options' command.
        """
    def levelset_auto_init(self):
        """
        'levelset_auto_init' command.
        """
    return_type: str

class execute_commands(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def enable(self, command_name: str):
        """
        Enable an execute-command.
        """
    def disable(self, command_name: str):
        """
        Disable an execute-command.
        """
    def copy(self, command_name: str):
        """
        Copy an execute-command.
        """
    def delete(self, command_name: str):
        """
        Delete an execute-command.
        """
    def export(self, command_name: list[str], tsv_file_name: str):
        """
        Export execute-commands to a TSV file.
        """
    def import_(self, tsv_file_name: str):
        """
        Import execute-commands from a TSV file.
        """
    return_type: str

class animate_on(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class flow_time_frequency(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class storage_type(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class storage_dir(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class window_id(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class view(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_raytracing(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solution_animations_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    animate_on: animate_on
    frequency: frequency_1
    flow_time_frequency: flow_time_frequency
    frequency_of: frequency_of
    storage_type: storage_type
    storage_dir: storage_dir
    window_id: window_id
    view: view
    use_raytracing: use_raytracing
    def display(self):
        """
        'display' command.
        """
    return_type: str

class solution_animations(NamedObject[solution_animations_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: solution_animations_child
    return_type: str

class name_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class register(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class option_14(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iterations_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_steps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class frequency_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option_14
    iterations: iterations_1
    time_steps: time_steps
    return_type: str

class active_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_9(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class monitor_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class register_based_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_3
    register: register
    frequency: frequency_2
    active: active_1
    verbosity: verbosity_9
    monitor: monitor_1
    return_type: str

class register_based(NamedObject[register_based_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        List the names of the definitions for poor mesh numerics.
        """
    def list_properties_1(self, register_name: str):
        """
        List the properties of a definition for poor mesh numerics.
        
        Parameters
        ----------
            register_name : str
                'register_name' child.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def set(self):
        """
        'set' command.
        """
    child_object_type: register_based_child
    return_type: str

class poor_mesh_numerics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    register_based: register_based
    return_type: str

class calculation_activity(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    execute_commands: execute_commands
    solution_animations: solution_animations
    poor_mesh_numerics: poor_mesh_numerics
    def enable_strategy(self, enable: bool):
        """
        Specify whether automatic initialization and case modification should be enabled.
        
        Parameters
        ----------
            enable : bool
                'enable' child.
        """
    def copy_modification(self, mod_name: str):
        """
        Copy a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        """
    def delete_modification(self, mod_name: str):
        """
        Delete a single case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        """
    def enable_modification(self, mod_name: str):
        """
        Enable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        """
    def disable_modification(self, mod_name: str):
        """
        Disable a single defined case modification.
        
        Parameters
        ----------
            mod_name : str
                'mod_name' child.
        """
    def import_modifications(self, filename: str):
        """
        Import a list of case modifications from a tsv file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        """
    def export_modifications(self, command_list: list[str], filename: str):
        """
        Export all case modifications to a tsv file.
        """
    def continue_strategy_execution(self):
        """
        Continue execution of the automatic initialization and case modification strategy defined at present.
        """
    return_type: str

class verbosity_10(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_method_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pseudo_time_step_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class length_scale_methods(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_size_scale_factor_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class length_scale_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_time_size_calc_solid_zone(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_solid_scale_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_size_for_solid_zone(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_method(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    time_step_method: time_step_method_1
    pseudo_time_step_size: pseudo_time_step_size
    length_scale_methods: length_scale_methods
    time_step_size_scale_factor: time_step_size_scale_factor_1
    length_scale: length_scale_1
    auto_time_size_calc_solid_zone: auto_time_size_calc_solid_zone
    time_solid_scale_factor: time_solid_scale_factor
    time_step_size_for_solid_zone: time_step_size_for_solid_zone
    return_type: str

class pseudo_time_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    verbosity: verbosity_10
    time_step_method: time_step_method
    return_type: str

class iter_count_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_timestep(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class error_tolerance(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_end(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_time_step(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_time_step(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_step_change_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_step_change_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_time_step_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class adaptive_time_stepping(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_2
    user_defined_timestep: user_defined_timestep
    error_tolerance: error_tolerance
    time_end: time_end
    min_time_step: min_time_step
    max_time_step: max_time_step
    min_step_change_factor: min_step_change_factor
    max_step_change_factor: max_step_change_factor
    fixed_time_step_count: fixed_time_step_count
    return_type: str

class enalbled(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class desired_cfl(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_time_step(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_fixed_time_step(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class update_interval_time_step_size(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cfl_based_adaptive_time_stepping(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enalbled: enalbled
    user_defined_timestep: user_defined_timestep
    desired_cfl: desired_cfl
    time_end: time_end
    initial_time_step: initial_time_step
    max_fixed_time_step: max_fixed_time_step
    update_interval_time_step_size: update_interval_time_step_size
    min_time_step: min_time_step
    max_time_step: max_time_step
    min_step_change_factor: min_step_change_factor
    max_step_change_factor: max_step_change_factor
    return_type: str

class reporting_interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_count_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class specified_time_step(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class incremental_time(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_iter_per_time_step(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_count_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class total_time_step_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class total_time(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solution_status(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class extrapolate_vars(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_flow_time(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class control_time_step_size_variation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_average_cfl(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cfl_type(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class courant_number_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class initial_time_step_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_time_step_size(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_time_step_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_time_step_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class update_interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cfl_based_time_stepping(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    courant_number: courant_number_1
    initial_time_step_size: initial_time_step_size
    fixed_time_step_size: fixed_time_step_size
    min_time_step_size: min_time_step_size
    max_time_step_size: max_time_step_size
    min_step_change_factor: min_step_change_factor
    max_step_change_factor: max_step_change_factor
    update_interval: update_interval
    return_type: str

class error_tolerance_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class error_based_time_stepping(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    error_tolerance: error_tolerance_1
    initial_time_step_size: initial_time_step_size
    fixed_time_step_size: fixed_time_step_size
    min_time_step_size: min_time_step_size
    max_time_step_size: max_time_step_size
    min_step_change_factor: min_step_change_factor
    max_step_change_factor: max_step_change_factor
    update_interval: update_interval
    return_type: str

class undo_timestep(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class predict_next(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rotating_mesh_flow_predictor(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class global_courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mp_specific_time_stepping(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_2
    global_courant_number: global_courant_number
    initial_time_step_size: initial_time_step_size
    fixed_time_step_size: fixed_time_step_size
    min_time_step_size: min_time_step_size
    max_time_step_size: max_time_step_size
    min_step_change_factor: min_step_change_factor
    max_step_change_factor: max_step_change_factor
    update_interval: update_interval
    return_type: str

class udf_hook(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_periodic_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_periodic_type(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_periodic_type_value(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class times_step_periods(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class total_period_run(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_periodic(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    fixed_periodic: fixed_periodic_1
    fixed_periodic_type: fixed_periodic_type
    fixed_periodic_type_value: fixed_periodic_type_value
    times_step_periods: times_step_periods
    total_period_run: total_period_run
    return_type: str

class duration_specification_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class moving_mesh_constraint(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mesh_courant_number(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class moving_mesh_cfl_constraint(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    moving_mesh_constraint: moving_mesh_constraint
    mesh_courant_number: mesh_courant_number
    return_type: str

class physics_based_constraint(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class viscous_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gravity_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_tension_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class acoustic_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_scale_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    viscous_scale: viscous_scale
    gravity_scale: gravity_scale
    surface_tension_scale: surface_tension_scale
    acoustic_scale: acoustic_scale
    return_type: str

class verbosity_11(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class multiphase_specific_time_constraints(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    moving_mesh_cfl_constraint: moving_mesh_cfl_constraint
    physics_based_constraint: physics_based_constraint
    time_scale_options: time_scale_options
    verbosity: verbosity_11
    return_type: str

class enable_solid_time_step(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class choose_auto_time_stepping(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_step_size_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_time_step_size(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enable_solid_time_step: enable_solid_time_step
    choose_auto_time_stepping: choose_auto_time_stepping
    time_step_size: time_step_size_1
    return_type: str

class time_step_size_for_acoustic_export(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class extrapolate_eqn_vars_child(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class extrapolate_eqn_vars(NamedObject[extrapolate_eqn_vars_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: extrapolate_eqn_vars_child
    return_type: str

class transient_controls(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    type: type_2
    method: method_2
    specified_time_step: specified_time_step
    incremental_time: incremental_time
    max_iter_per_time_step: max_iter_per_time_step
    time_step_count: time_step_count_2
    total_time_step_count: total_time_step_count
    total_time: total_time
    time_step_size: time_step_size
    solution_status: solution_status
    extrapolate_vars: extrapolate_vars
    max_flow_time: max_flow_time
    control_time_step_size_variation: control_time_step_size_variation
    use_average_cfl: use_average_cfl
    cfl_type: cfl_type
    cfl_based_time_stepping: cfl_based_time_stepping
    error_based_time_stepping: error_based_time_stepping
    undo_timestep: undo_timestep
    predict_next: predict_next
    rotating_mesh_flow_predictor: rotating_mesh_flow_predictor
    mp_specific_time_stepping: mp_specific_time_stepping
    udf_hook: udf_hook
    fixed_periodic: fixed_periodic
    duration_specification_method: duration_specification_method
    multiphase_specific_time_constraints: multiphase_specific_time_constraints
    solid_time_step_size: solid_time_step_size
    time_step_size_for_acoustic_export: time_step_size_for_acoustic_export
    extrapolate_eqn_vars: extrapolate_eqn_vars
    return_type: str

class data_sampling_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sampling_interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class statistics_shear_stress(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class statistics_heat_flux(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_statistics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class force_statistics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_statistics_dpm(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class species_list(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class statistics_mixture_fraction(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class statistics_reaction_progress(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class save_cff_unsteady_statistics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class udf_cf_names(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class data_sampling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    data_sampling: data_sampling_1
    sampling_interval: sampling_interval
    statistics_shear_stress: statistics_shear_stress
    statistics_heat_flux: statistics_heat_flux
    wall_statistics: wall_statistics
    force_statistics: force_statistics
    time_statistics_dpm: time_statistics_dpm
    species_list: species_list
    statistics_mixture_fraction: statistics_mixture_fraction
    statistics_reaction_progress: statistics_reaction_progress
    save_cff_unsteady_statistics: save_cff_unsteady_statistics
    udf_cf_names: udf_cf_names
    return_type: str

class data_sampling_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def remove_dataset(self, name: str):
        """
        Remove dataset.
        
        Parameters
        ----------
            name : str
                'name' child.
        """
    def list_datasets(self):
        """
        List dataset.
        """
    return_type: str

class residual_verbosity(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class run_calculation(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    query_names: list[str]
    pseudo_time_settings: pseudo_time_settings
    iter_count: iter_count_2
    adaptive_time_stepping: adaptive_time_stepping
    cfl_based_adaptive_time_stepping: cfl_based_adaptive_time_stepping
    reporting_interval: reporting_interval
    time_step_count: time_step_count_1
    transient_controls: transient_controls
    data_sampling: data_sampling
    data_sampling_options: data_sampling_options
    residual_verbosity: residual_verbosity
    def calculate(self):
        """
        'calculate' command.
        """
    def interrupt(self, end_of_timestep: bool):
        """
        Interrupt the iterations.
        
        Parameters
        ----------
            end_of_timestep : bool
                'end_of_timestep' child.
        """
    def dual_time_iterate(self, total_period_count: int, time_step_count: int, total_time_step_count: int, total_time: float | str, incremental_time: float | str, max_iter_per_step: int, postprocess: bool, post_iter_per_time_step_count: int):
        """
        Perform unsteady iterations.
        
        Parameters
        ----------
            total_period_count : int
                Number of total periods.
            time_step_count : int
                Inceremtal number of Time steps.
            total_time_step_count : int
                Total number of Time steps.
            total_time : real
                Total Simulation Time.
            incremental_time : real
                Incremental Time.
            max_iter_per_step : int
                Maximum Number of iterations per time step.
            postprocess : bool
                Enable/Disable Postprocess pollutant solution?.
            post_iter_per_time_step_count : int
                Number of post-processing iterations per time step.
        """
    def iterate(self, iter_count: int):
        """
        Perform a specified number of iterations.
        
        Parameters
        ----------
            iter_count : int
                Incremental number of time steps.
        """
    def iterating(self):
        """
        'iterating' query.
        """
    return_type: str

class solution(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    methods: methods
    controls: controls_1
    report_definitions: report_definitions
    monitor: monitor
    cell_registers: cell_registers
    initialization: initialization
    calculation_activity: calculation_activity
    run_calculation: run_calculation
    return_type: str

class snap_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class point_surface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    reference_frame: reference_frame
    point: point
    snap_method: snap_method
    return_type: str

class point_surface(NamedObject[point_surface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: point_surface_child
    return_type: str

class p0(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p1(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class line_surface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    p0: p0
    p1: p1
    return_type: str

class line_surface(NamedObject[line_surface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: line_surface_child
    return_type: str

class number_of_points(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rake_surface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    p0: p0
    p1: p1
    number_of_points: number_of_points
    return_type: str

class rake_surface(NamedObject[rake_surface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: rake_surface_child
    return_type: str

class surface_2(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class zone_1(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iso_value(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iso_surface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    field: field
    surface: surface_2
    zone: zone_1
    min: min
    max: max
    iso_value: iso_value
    return_type: str

class iso_surface(NamedObject[iso_surface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: iso_surface_child
    return_type: str

class x_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class point_vector(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class point_normal(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class compute_from_view_plane(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_aligned_normal(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class p2(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bounded(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sample_point(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edges(IntegerList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class plane_surface_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_2
    method: method_2
    x: x_1
    y: y_1
    z: z_1
    point_vector: point_vector
    point_normal: point_normal
    compute_from_view_plane: compute_from_view_plane
    surface_aligned_normal: surface_aligned_normal
    p0: p0
    p1: p1
    p2: p2
    bounded: bounded
    sample_point: sample_point
    edges: edges
    return_type: str

class plane_surface(NamedObject[plane_surface_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: plane_surface_child
    return_type: str

class surfaces_4(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    point_surface: point_surface
    line_surface: line_surface
    rake_surface: rake_surface
    iso_surface: iso_surface
    plane_surface: plane_surface
    return_type: str

class nodes(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edges_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class faces_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partitions(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class overset_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gap(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_8(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    nodes: nodes
    edges: edges_1
    faces: faces_1
    partitions: partitions
    overset: overset_2
    gap: gap
    return_type: str

class all_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class feature_angle(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class feature(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    feature_angle: feature_angle
    return_type: str

class outline(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edge_type(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    all: all_2
    feature: feature
    outline: outline
    return_type: str

class shrink_factor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surfaces_list(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class type_8(Group):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class id(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class normal(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partition(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class automatic(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    type: type_8
    id: id
    normal: normal
    partition: partition
    return_type: str

class faces_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class edges_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nodes_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class material_color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class manual(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    faces: faces_2
    edges: edges_2
    nodes: nodes_1
    material_color: material_color
    return_type: str

class coloring(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    automatic: automatic
    manual: manual
    return_type: str

class display_state_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class mesh_2_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    options: options_8
    edge_type: edge_type
    shrink_factor: shrink_factor
    surfaces_list: surfaces_list
    coloring: coloring
    display_state_name: display_state_name
    physics: physics_1
    geometry: geometry_4
    surfaces: surfaces_3
    def display(self):
        """
        'display' command.
        """
    return_type: str

class mesh_2(NamedObject[mesh_2_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: mesh_2_child
    return_type: str

class boundary_values(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class contour_lines(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class node_values(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class global_range(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_range_on(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    global_range: global_range
    return_type: str

class clip_to_range(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_range_off(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    clip_to_range: clip_to_range
    minimum: minimum_1
    maximum: maximum_1
    return_type: str

class range_option(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    auto_range_on: auto_range_on
    auto_range_off: auto_range_off
    return_type: str

class smooth(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class banded(Group):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coloring_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    smooth: smooth
    banded: banded
    return_type: str

class visible(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class size(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class log_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class format(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_skip(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class show_all(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class position(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class font_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class font_automatic(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class font_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class length_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class width(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bground_transparent(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bground_color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class title_elements(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class color_map(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    visible: visible
    size: size
    color: color
    log_scale: log_scale
    format: format
    user_skip: user_skip
    show_all: show_all
    position: position
    font_name: font_name
    font_automatic: font_automatic
    font_size: font_size
    length: length_1
    width: width
    bground_transparent: bground_transparent
    bground_color: bground_color
    title_elements: title_elements
    return_type: str

class mesh_object(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class deformation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class deformation_scale(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class contour_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    field: field
    filled: filled
    boundary_values: boundary_values
    contour_lines: contour_lines
    node_values: node_values
    surfaces_list: surfaces_list
    range_option: range_option
    coloring: coloring_1
    color_map: color_map
    draw_mesh: draw_mesh
    mesh_object: mesh_object
    display_state_name: display_state_name
    physics: physics_1
    geometry: geometry_4
    surfaces: surfaces_3
    deformation: deformation
    deformation_scale: deformation_scale
    def display(self):
        """
        'display' command.
        """
    def update_min_max(self):
        """
        'update_min_max' command.
        """
    return_type: str

class contour(NamedObject[contour_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: contour_child
    return_type: str

class vector_field(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_f(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    auto_scale: auto_scale
    scale_f: scale_f
    return_type: str

class style(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skip(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class in_plane(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_length(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_comp(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_comp(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_comp(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_head(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vector_opt(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    in_plane: in_plane
    fixed_length: fixed_length
    x_comp: x_comp
    y_comp: y_comp
    z_comp: z_comp
    scale_head: scale_head
    color: color
    return_type: str

class vector_1_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    field: field
    vector_field: vector_field
    surfaces_list: surfaces_list
    scale: scale_1
    style: style
    skip: skip
    vector_opt: vector_opt
    range_option: range_option
    color_map: color_map
    draw_mesh: draw_mesh
    mesh_object: mesh_object
    display_state_name: display_state_name
    physics: physics_1
    geometry: geometry_4
    surfaces: surfaces_3
    def display(self):
        """
        'display' command.
        """
    def update_min_max(self):
        """
        'update_min_max' command.
        """
    return_type: str

class vector_1(NamedObject[vector_1_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: vector_1_child
    return_type: str

class uid(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class oil_flow(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reverse(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class node_values_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class relative_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_9(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    oil_flow: oil_flow
    reverse: reverse
    node_values: node_values_1
    relative: relative_1
    return_type: str

class auto_range(Group):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class min_value(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_value(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clip_to_range_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    min_value: min_value
    max_value: max_value
    return_type: str

class range(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    auto_range: auto_range
    clip_to_range: clip_to_range_1
    return_type: str

class line_width(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class arrow_space(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class arrow_scale(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sphere_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sphere_lod(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scalefactor(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ribbon(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    field: field
    scalefactor: scalefactor
    return_type: str

class style_attribute(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    style: style
    line_width: line_width
    arrow_space: arrow_space
    arrow_scale: arrow_scale
    marker_size: marker_size
    sphere_size: sphere_size
    sphere_lod: sphere_lod
    radius: radius
    ribbon: ribbon
    return_type: str

class step_size(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class tolerance_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class accuracy_control_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    step_size: step_size
    tolerance: tolerance_2
    return_type: str

class x_axis_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class plot_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_axis_function: x_axis_function
    enabled: enabled_2
    return_type: str

class step(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class onzone(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class onphysics(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class velocity_domain(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_format(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_axis_precision(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_format(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_axis_precision(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class numbers(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_format: x_format
    x_axis_precision: x_axis_precision
    y_format: y_format
    y_axis_precision: y_axis_precision
    return_type: str

class draw_major_rules(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class major_rule_weight(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class major_rule_line_color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class draw_minor_rules(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minor_rule_weight(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class minor_rule_line_color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_axis_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    draw_major_rules: draw_major_rules
    major_rule_weight: major_rule_weight
    major_rule_line_color: major_rule_line_color
    draw_minor_rules: draw_minor_rules
    minor_rule_weight: minor_rule_weight
    minor_rule_line_color: minor_rule_line_color
    return_type: str

class y_axis_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    draw_major_rules: draw_major_rules
    major_rule_weight: major_rule_weight
    major_rule_line_color: major_rule_line_color
    draw_minor_rules: draw_minor_rules
    minor_rule_weight: minor_rule_weight
    minor_rule_line_color: minor_rule_line_color
    return_type: str

class rules(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_axis: x_axis_1
    y_axis: y_axis_1
    return_type: str

class x_axis_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_axis_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class log_scale_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_axis: x_axis_2
    y_axis: y_axis_2
    return_type: str

class x_axis_min(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_axis_max(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_axis_min(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_axis_max(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_scale_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_axis: x_axis_2
    x_axis_min: x_axis_min
    x_axis_max: x_axis_max
    y_axis: y_axis_2
    y_axis_min: y_axis_min
    y_axis_max: y_axis_max
    return_type: str

class x_axis_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_axis_3(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class labels(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_axis: x_axis_3
    y_axis: y_axis_3
    return_type: str

class axes(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    numbers: numbers
    rules: rules
    log_scale: log_scale_1
    auto_scale: auto_scale_1
    labels: labels
    return_type: str

class pattern(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class weight(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lines_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    pattern: pattern
    weight: weight
    color: color
    return_type: str

class lines(ListObject[lines_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: lines_child
    return_type: str

class symbol(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class size_1(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class markers_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    symbol: symbol
    size: size_1
    color: color
    return_type: str

class markers(ListObject[markers_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: markers_child
    return_type: str

class curves(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    lines: lines
    markers: markers
    return_type: str

class pathline_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    uid: uid
    options: options_9
    range: range
    style_attribute: style_attribute
    accuracy_control: accuracy_control_1
    plot: plot_2
    step: step
    skip: skip
    coarsen: coarsen_1
    onzone: onzone
    onphysics: onphysics
    field: field
    surfaces_list: surfaces_list
    velocity_domain: velocity_domain
    color_map: color_map
    draw_mesh: draw_mesh
    mesh_object: mesh_object
    display_state_name: display_state_name
    physics: physics_1
    geometry: geometry_4
    surfaces: surfaces_3
    axes: axes
    curves: curves
    def display(self):
        """
        'display' command.
        """
    def update_min_max(self):
        """
        'update_min_max' command.
        """
    return_type: str

class pathline(NamedObject[pathline_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: pathline_child
    return_type: str

class options_10(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    node_values: node_values_1
    return_type: str

class inside_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class outside(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_11(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    inside: inside_1
    outside: outside
    return_type: str

class filter_minimum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class filter_maximum(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class filter_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    field: field
    options: options_11
    enabled: enabled_2
    filter_minimum: filter_minimum
    filter_maximum: filter_maximum
    return_type: str

class ribbon_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    field: field
    scalefactor: scalefactor
    return_type: str

class scale_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diameter_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class constant_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    diameter: diameter_1
    return_type: str

class size_by(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class variable_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    size_by: size_by
    range: range
    return_type: str

class options_12(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    constant: constant_1
    variable: variable_1
    return_type: str

class sphere_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    scale: scale_2
    sphere_lod: sphere_lod
    options: options_12
    return_type: str

class style_attribute_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    style: style
    line_width: line_width
    arrow_space: arrow_space
    arrow_scale: arrow_scale
    marker_size: marker_size
    sphere_size: sphere_size
    sphere_lod: sphere_lod
    radius: radius
    ribbon_settings: ribbon_settings
    sphere_settings: sphere_settings
    return_type: str

class constant_length(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class variable_length(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vector_length(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    constant_length: constant_length
    variable_length: variable_length
    return_type: str

class constant_color(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_2
    color: color
    return_type: str

class vector_of(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class length_to_head_ratio(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class vector_settings(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    style: style
    vector_length: vector_length
    constant_color: constant_color
    vector_of: vector_of
    scale: scale_2
    length_to_head_ratio: length_to_head_ratio
    return_type: str

class stream_id(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class track_single_particle_stream(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_2
    stream_id: stream_id
    return_type: str

class injections_list(StringList, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class free_stream_particles(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_film_particles(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class track_pdf_particles(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_track_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    uid: uid
    options: options_10
    filter_settings: filter_settings
    range: range
    style_attribute: style_attribute_1
    vector_settings: vector_settings
    plot: plot_2
    track_single_particle_stream: track_single_particle_stream
    skip: skip
    coarsen: coarsen_1
    field: field
    injections_list: injections_list
    free_stream_particles: free_stream_particles
    wall_film_particles: wall_film_particles
    track_pdf_particles: track_pdf_particles
    color_map: color_map
    draw_mesh: draw_mesh
    mesh_object: mesh_object
    display_state_name: display_state_name
    axes: axes
    curves: curves
    def display(self):
        """
        'display' command.
        """
    def update_min_max(self):
        """
        'update_min_max' command.
        """
    return_type: str

class particle_track(NamedObject[particle_track_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: particle_track_child
    return_type: str

class vector_phase(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_color_by_field(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_oriented(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_normalize(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_pixel_interpolation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_max_steps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class texture_spacing(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class texture_size(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_intensity_factor(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_image_filter(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_intensity_alpha(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_fast(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class gray_scale(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class image_to_display(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lic_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    field: field
    vector_field: vector_field
    vector_phase: vector_phase
    surfaces_list: surfaces_list
    surfaces: surfaces_3
    lic_color_by_field: lic_color_by_field
    lic_color: lic_color
    lic_oriented: lic_oriented
    lic_normalize: lic_normalize
    lic_pixel_interpolation: lic_pixel_interpolation
    lic_max_steps: lic_max_steps
    texture_spacing: texture_spacing
    texture_size: texture_size
    lic_intensity_factor: lic_intensity_factor
    lic_image_filter: lic_image_filter
    lic_intensity_alpha: lic_intensity_alpha
    lic_fast: lic_fast
    gray_scale: gray_scale
    image_to_display: image_to_display
    range_option: range_option
    color_map: color_map
    draw_mesh: draw_mesh
    mesh_object: mesh_object
    display_state_name: display_state_name
    def display(self):
        """
        'display' command.
        """
    def update_min_max(self):
        """
        'update_min_max' command.
        """
    return_type: str

class lic(NamedObject[lic_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: lic_child
    return_type: str

class olic_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    field: field
    vector_field: vector_field
    vector_phase: vector_phase
    surfaces_list: surfaces_list
    surfaces: surfaces_3
    lic_color_by_field: lic_color_by_field
    lic_color: lic_color
    lic_oriented: lic_oriented
    lic_normalize: lic_normalize
    lic_pixel_interpolation: lic_pixel_interpolation
    lic_max_steps: lic_max_steps
    texture_spacing: texture_spacing
    texture_size: texture_size
    lic_intensity_factor: lic_intensity_factor
    lic_image_filter: lic_image_filter
    lic_intensity_alpha: lic_intensity_alpha
    lic_fast: lic_fast
    gray_scale: gray_scale
    image_to_display: image_to_display
    range_option: range_option
    color_map: color_map
    draw_mesh: draw_mesh
    mesh_object: mesh_object
    display_state_name: display_state_name
    def display(self):
        """
        'display' command.
        """
    return_type: str

class olic(NamedObject[olic_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: olic_child
    return_type: str

class auto_scale_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clip_to_range_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surfaces_5(StringList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class filled_contours(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class global_range_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class line_contours(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class log_scale_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class n_contour(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class node_values_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class render_mesh(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class banded_coloring(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class number_of_bands(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coloring_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    banded_coloring: banded_coloring
    number_of_bands: number_of_bands
    return_type: str

class contours(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    auto_scale: auto_scale_2
    clip_to_range: clip_to_range_2
    surfaces: surfaces_5
    filled_contours: filled_contours
    global_range: global_range_1
    line_contours: line_contours
    log_scale: log_scale_2
    n_contour: n_contour
    node_values: node_values_2
    render_mesh: render_mesh
    coloring: coloring_2
    return_type: str

class display_4(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class history_filename(Filename):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class report_default_variables(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class track_single_particle_stream_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class arrow_scale_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class arrow_space_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class coarsen_factor(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class line_width_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_tracks(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    display: display_4
    history_filename: history_filename
    report_default_variables: report_default_variables
    track_single_particle_stream: track_single_particle_stream_1
    arrow_scale: arrow_scale_1
    arrow_space: arrow_space_1
    coarsen_factor: coarsen_factor
    line_width: line_width_1
    return_type: str

class background(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class color_by_type(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class foreground(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class only_list_case_boundaries(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_inherent_material_color(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class by_type(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    only_list_case_boundaries: only_list_case_boundaries
    use_inherent_material_color: use_inherent_material_color
    def reset(self, reset_color: bool):
        """
        Reset colors and/or materials to the defaults.
        
        Parameters
        ----------
            reset_color : bool
                'reset_color' child.
        """
    return_type: str

class use_inherent_material_color_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class by_surface(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    use_inherent_material_color: use_inherent_material_color_1
    def reset(self, reset_color: bool):
        """
        Reset colors and/or materials to the defaults.
        
        Parameters
        ----------
            reset_color : bool
                'reset_color' child.
        """
    def list_surfaces_by_color(self):
        """
        List the surfaces by its color.
        """
    def list_surfaces_by_material(self):
        """
        List the surfaces by its material.
        """
    return_type: str

class far_field_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class inlet_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interior_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class internal_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class outlet_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class overset_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class periodic_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rans_les_interface_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class symmetry_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axis_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class free_surface_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class traction_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class wall_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interface_faces(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class surface_3(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class skip_label(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class automatic_skip(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class colors(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    background: background
    color_by_type: color_by_type
    foreground: foreground
    by_type: by_type
    by_surface: by_surface
    far_field_faces: far_field_faces
    inlet_faces: inlet_faces
    interior_faces: interior_faces
    internal_faces: internal_faces
    outlet_faces: outlet_faces
    overset_faces: overset_faces
    periodic_faces: periodic_faces
    rans_les_interface_faces: rans_les_interface_faces
    symmetry_faces: symmetry_faces
    axis_faces: axis_faces
    free_surface_faces: free_surface_faces
    traction_faces: traction_faces
    wall_faces: wall_faces
    interface_faces: interface_faces
    surface: surface_3
    skip_label: skip_label
    automatic_skip: automatic_skip
    def reset_colors(self):
        """
        Reset individual mesh surface colors to the defaults.
        """
    def list_colors(self):
        """
        List available colors.
        """
    return_type: str

class ambient_color(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class headlight_setting(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lights_on(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lighting_interpolation(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lights(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    ambient_color: ambient_color
    headlight_setting: headlight_setting
    lights_on: lights_on
    lighting_interpolation: lighting_interpolation
    def set_light(self, light_number: int, light_on: bool, rgb_vector: list[float | str], use_view_factor: bool, change_light_direction: bool, direction_vector: list[float | str]):
        """
        'set_light' command.
        """
    return_type: str

class raytracer_image(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class color_mode(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hardcopy_format(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hardcopy_options(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class window_dump_cmd(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class post_format(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class driver_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    hardcopy_format: hardcopy_format
    hardcopy_options: hardcopy_options
    window_dump_cmd: window_dump_cmd
    post_format: post_format
    def current_driver(self):
        """
        'current_driver' command.
        """
    return_type: str

class invert_background(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class landscape(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class x_resolution(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_resolution(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpi(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_window_resolution(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class standard_resolution(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class jpeg_hardcopy_quality(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class picture(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    raytracer_image: raytracer_image
    color_mode: color_mode
    driver_options: driver_options
    invert_background: invert_background
    landscape: landscape
    x_resolution: x_resolution
    y_resolution: y_resolution
    dpi: dpi
    use_window_resolution: use_window_resolution
    standard_resolution: standard_resolution
    jpeg_hardcopy_quality: jpeg_hardcopy_quality
    def preview(self):
        """
        Display a preview image of a hardcopy.
        """
    def save_picture(self, file_name: str):
        """
        'save_picture' command.
        """
    def list_color_mode(self):
        """
        'list_color_mode' command.
        """
    return_type: str

class camera(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def dolly(self, right: float | str, up: float | str, in_: float | str):
        """
        Adjust the camera position and target.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
            in_ : real
                'in' child.
        """
    def field(self, width: float | str, height: float | str):
        """
        Set the field of view (width and height).
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        """
    def orbit(self, right: float | str, up: float | str):
        """
        Adjust the camera position without modifying the target.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
        """
    def pan(self, right: float | str, up: float | str):
        """
        Adjust the camera position without modifying the position.
        
        Parameters
        ----------
            right : real
                'right' child.
            up : real
                'up' child.
        """
    def position(self, xyz: list[float | str]):
        """
        Set the camera position.
        
        Parameters
        ----------
            xyz : List
                'xyz' child.
        """
    def projection(self, type: str):
        """
        Set the camera projection.
        
        Parameters
        ----------
            type : str
                'type' child.
        """
    def roll(self, counter_clockwise: float | str):
        """
        Adjust the camera up-vector.
        
        Parameters
        ----------
            counter_clockwise : real
                'counter_clockwise' child.
        """
    def target(self, xyz: list[float | str]):
        """
        Set the point to be the center of the camera view.
        
        Parameters
        ----------
            xyz : List
                'xyz' child.
        """
    def up_vector(self, xyz: list[float | str]):
        """
        Set the camera up-vector.
        
        Parameters
        ----------
            xyz : List
                'xyz' child.
        """
    def zoom(self, factor: float | str):
        """
        Adjust the camera field of view.
        
        Parameters
        ----------
            factor : real
                'factor' child.
        """
    return_type: str

class front_faces_transparent(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class projection_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axes_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ruler(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class boundary_marker(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class anti_aliasing(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class reflections(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class static_shadows(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_shadows(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class grid_plane(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class headlights(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class lighting(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class view_name(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class display_states_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    front_faces_transparent: front_faces_transparent
    projection: projection_1
    axes: axes_1
    ruler: ruler
    title: title
    boundary_marker: boundary_marker
    anti_aliasing: anti_aliasing
    reflections: reflections
    static_shadows: static_shadows
    dynamic_shadows: dynamic_shadows
    grid_plane: grid_plane
    headlights: headlights
    lighting: lighting
    view_name: view_name
    return_type: str

class display_states(NamedObject[display_states_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def use_active(self, state_name: str):
        """
        'use_active' command.
        """
    def restore_state(self, state_name: str):
        """
        Apply a display state to the active window.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        """
    def copy(self, state_name: str):
        """
        Create a new display state with settings copied from an existing display state.
        
        Parameters
        ----------
            state_name : str
                'state_name' child.
        """
    def read(self, file_name: str):
        """
        Read display states from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        """
    def write(self, file_name: str, state_name: list[str]):
        """
        Write display states to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            state_name : List
                'state_name' child.
        """
    child_object_type: display_states_child
    return_type: str

class views(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    camera: camera
    display_states: display_states
    def auto_scale(self):
        """
        'auto_scale' command.
        """
    def reset_to_default_view(self):
        """
        Reset view to front and center.
        """
    def delete_view(self, view_name: str):
        """
        Remove a view from the list.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        """
    def last_view(self):
        """
        Return to the camera position before the last manipulation.
        """
    def next_view(self):
        """
        Return to the camera position after the current position in the stack.
        """
    def list_views(self):
        """
        List predefined and saved views.
        """
    def restore_view(self, view_name: str):
        """
        Use a saved view.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        """
    def read_views(self, filename: str):
        """
        Read views from a view file.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        """
    def save_view(self, view_name: str):
        """
        Save the current view to the view list.
        
        Parameters
        ----------
            view_name : str
                'view_name' child.
        """
    def write_views(self, file_name: str, view_list: list[str]):
        """
        Write selected views to a view file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            view_list : List
                'view_list' child.
        """
    return_type: str

class border(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bottom(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clear_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class left(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class right_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class top(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class visible_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class axes_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    border: border
    bottom: bottom
    clear: clear_1
    left: left
    right: right_1
    top: top
    visible: visible_1
    return_type: str

class border_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bottom_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class left_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class right_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class top_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class visible_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class main(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    border: border_1
    bottom: bottom_1
    left: left_1
    right: right_2
    top: top_1
    visible: visible_2
    return_type: str

class border_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bottom_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clear_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class format_1(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class font_size_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class left_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class margin(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class right_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class top_2(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class visible_3(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    border: border_2
    bottom: bottom_2
    clear: clear_2
    format: format_1
    font_size: font_size_1
    left: left_2
    margin: margin
    right: right_3
    top: top_2
    visible: visible_3
    return_type: str

class application(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class border_3(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bottom_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class clear_3(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class company(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class date(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class left_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class right_4(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class top_3(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class visible_4(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class alignment(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class text(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    application: application
    border: border_3
    bottom: bottom_3
    clear: clear_3
    company: company
    date: date
    left: left_3
    right: right_4
    top: top_3
    visible: visible_4
    alignment: alignment
    return_type: str

class background_1(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class color_filter(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class foreground_1(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class on(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class width_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class height_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class margin_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pixel_size(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    width: width_1
    height: height_1
    margin: margin_1
    return_type: str

class video(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    background: background_1
    color_filter: color_filter
    foreground: foreground_1
    on: on
    pixel_size: pixel_size
    return_type: str

class border_4(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bottom_4(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class left_4(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class right_5(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class top_4(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class visible_5(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class xy(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    border: border_4
    bottom: bottom_4
    left: left_4
    right: right_5
    top: top_4
    visible: visible_5
    return_type: str

class logo(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class ruler_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class logo_color(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class windows(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    axes: axes_2
    main: main
    scale: scale_3
    text: text
    video: video
    xy: xy
    logo: logo
    ruler: ruler_1
    logo_color: logo_color
    def aspect_ratio(self, width: float | str, height: float | str):
        """
        Set the aspect ratio of the active window.
        
        Parameters
        ----------
            width : real
                'width' child.
            height : real
                'height' child.
        """
    return_type: str

class hide_environment_keep_effects(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class environment_image(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class latitude_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class longitude_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class view_zoom(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class show_backplate(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class backplate_color(IntegerList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class backplate_image(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class background_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    hide_environment_keep_effects: hide_environment_keep_effects
    environment_image: environment_image
    latitude: latitude_1
    longitude: longitude_1
    view_zoom: view_zoom
    show_backplate: show_backplate
    backplate_color: backplate_color
    backplate_image: backplate_image
    return_type: str

class quality_1(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class denoiser(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thread_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_rendering_timeout(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class rendering(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    quality: quality_1
    denoiser: denoiser
    thread_count: thread_count
    max_rendering_timeout: max_rendering_timeout
    return_type: str

class raytracing_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    background: background_2
    rendering: rendering
    def display_live_preview(self):
        """
        Display the raytracing rendering for the active window.
        """
    return_type: str

class graphics(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    mesh: mesh_2
    contour: contour
    vector: vector_1
    pathline: pathline
    particle_track: particle_track
    lic: lic
    olic: olic
    contours: contours
    particle_tracks: particle_tracks
    colors: colors
    lights: lights
    picture: picture
    views: views
    windows: windows
    raytracing_options: raytracing_options
    return_type: str

class position_on_x_axis(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class position_on_y_axis(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class options_13(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    node_values: node_values
    position_on_x_axis: position_on_x_axis
    position_on_y_axis: position_on_y_axis
    return_type: str

class x_component(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class y_component(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class z_component(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class direction_vector_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    x_component: x_component
    y_component: y_component
    z_component: z_component
    return_type: str

class default(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class curve_length(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    default: default
    reverse: reverse
    return_type: str

class plot_direction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    option: option
    direction_vector: direction_vector_2
    curve_length: curve_length
    return_type: str

class y_axis_function(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class xy_plot_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    uid: uid
    options: options_13
    plot_direction: plot_direction
    x_axis_function: x_axis_function
    y_axis_function: y_axis_function
    surfaces_list: surfaces_list
    physics: physics_1
    geometry: geometry_4
    surfaces: surfaces_3
    axes: axes
    curves: curves
    def display(self):
        """
        'display' command.
        """
    return_type: str

class xy_plot(NamedObject[xy_plot_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: xy_plot_child
    return_type: str

class plot_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    xy_plot: xy_plot
    return_type: str

class temporary(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class transparency(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class colormap_position(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class colormap_left(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class colormap_bottom(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class colormap_width(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class colormap_height(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class graphics_objects_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    name: name_1
    transparency: transparency
    colormap_position: colormap_position
    colormap_left: colormap_left
    colormap_bottom: colormap_bottom
    colormap_width: colormap_width
    colormap_height: colormap_height
    return_type: str

class graphics_objects(NamedObject[graphics_objects_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: graphics_objects_child
    return_type: str

class scene_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    name: name_1
    title: title
    temporary: temporary
    graphics_objects: graphics_objects
    display_state_name: display_state_name
    def display(self):
        """
        'display' command.
        """
    return_type: str

class scene(NamedObject[scene_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    def display(self, object_name: str):
        """
        Display graphics object.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def copy(self, from_name: str, new_name: str):
        """
        Copy graphics object.
        
        Parameters
        ----------
            from_name : str
                'from_name' child.
            new_name : str
                'new_name' child.
        """
    def add_to_graphics(self, object_name: str):
        """
        Add graphics object to existing graphics.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    def clear_history(self, object_name: str):
        """
        Clear object history.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        """
    child_object_type: scene_child
    return_type: str

class start_frame(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class end_frame(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class increment(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_custom_frames(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    start_frame: start_frame
    end_frame: end_frame
    increment: increment
    return_type: str

class fps(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class format_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class quality_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class name_4(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_original_resolution(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class scale_4(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_standard_resolution(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class width_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class height_2(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bitrate_scale(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class enable_h264(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class bitrate(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class compression_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class keyframe(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class advance_quality(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    bitrate_scale: bitrate_scale
    enable_h264: enable_h264
    bitrate: bitrate
    compression_method: compression_method
    keyframe: keyframe
    return_type: str

class video_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    fps: fps
    format: format_2
    quality: quality_2
    name: name_4
    use_original_resolution: use_original_resolution
    scale: scale_4
    set_standard_resolution: set_standard_resolution
    width: width_2
    height: height_2
    advance_quality: advance_quality
    return_type: str

class playback(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    set_custom_frames: set_custom_frames
    video: video_1
    def read_animation(self, read_from_file: bool, animation_file_name: str, select_from_available: bool, animation_name: str):
        """
        Read new animation from file or already-defined animations.
        
        Parameters
        ----------
            read_from_file : bool
                'read_from_file' child.
            animation_file_name : str
                'animation_file_name' child.
            select_from_available : bool
                'select_from_available' child.
            animation_name : str
                'animation_name' child.
        """
    def write_animation(self, format_name: str):
        """
        Write animation sequence to the file.
        
        Parameters
        ----------
            format_name : str
                'format_name' child.
        """
    def stored_view(self, view: bool):
        """
        Play the 3D animation sequence using the view stored in the sequence.
        
        Parameters
        ----------
            view : bool
                Yes: "Stored View", no: "Different View".
        """
    return_type: str

class animations(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    playback: playback
    return_type: str

class simulation_reports(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_simulation_reports(self):
        """
        List all report names.
        """
    def generate_simulation_report(self, report_name: str):
        """
        Generate a new simulation report or regenerate an existing simulation report with the provided name.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        """
    def view_simulation_report(self, report_name: str):
        """
        View a simulation report that has already been generated. In batch mode this will print the report's URL.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        """
    def export_simulation_report_as_pdf(self, report_name: str, file_name_path: str):
        """
        Export the provided simulation report as a PDF file.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            file_name_path : str
                'file_name_path' child.
        """
    def export_simulation_report_as_html(self, report_name: str, output_dir: str):
        """
        Export the provided simulation report as HTML.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            output_dir : str
                'output_dir' child.
        """
    def export_simulation_report_as_pptx(self, report_name: str, file_name_path: str):
        """
        Export the provided simulation report as a PPT file.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            file_name_path : str
                'file_name_path' child.
        """
    def write_simulation_report_names_to_file(self, file_path: str):
        """
        Write the list of currently generated report names to a txt file.
        
        Parameters
        ----------
            file_path : str
                'file_path' child.
        """
    def rename_simulation_report(self, report_name: str, new_report_name: str):
        """
        Rename a report which has already been generated.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            new_report_name : str
                'new_report_name' child.
        """
    def duplicate_simulation_report(self, report_name: str):
        """
        Duplicate the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        """
    def reset_report_to_defaults(self, report_name: str):
        """
        Reset all report settings to default for the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        """
    def delete_simulation_report(self, report_name: str):
        """
        Delete the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        """
    def write_simulation_report_template_file(self, file_name_path: str):
        """
        'write_simulation_report_template_file' command.
        """
    def read_simulation_report_template_file(self, file_name_path: str):
        """
        Read a JSON template file with existing Simulation Report settings.
        
        Parameters
        ----------
            file_name_path : str
                'file_name_path' child.
        """
    return_type: str

class auto_range_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class correlation(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class cumulation_curve(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class diameter_statistics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class histogram_mode(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class percentage(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class variable_3(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class logarithmic(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class weighting(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class histogram_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    auto_range: auto_range_1
    correlation: correlation
    cumulation_curve: cumulation_curve
    diameter_statistics: diameter_statistics
    histogram_mode: histogram_mode
    percentage: percentage
    variable_3: variable_3
    logarithmic: logarithmic
    weighting: weighting
    return_type: str

class minimum_val(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class maximum_val(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class division_val(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class histogram_parameters(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    minimum_val: minimum_val
    maximum_val: maximum_val
    division_val: division_val
    return_type: str

class plot_write_sample(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def plot_sample(self, loaded_samples: str, variable_to_sampled: str, weighting_var: str, correlation_var: str, read_fn: str, overwrite: bool):
        """
        'plot_sample' command.
        """
    def write_sample(self, loaded_samples: str, variable_to_sampled: str, weighting_var: str, correlation_var: str, read_fn: str, overwrite: bool):
        """
        'write_sample' command.
        """
    return_type: str

class use_weighting(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class make_steady_from_unsteady_file(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class setup_reduction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    use_weighting: use_weighting
    make_steady_from_unsteady_file: make_steady_from_unsteady_file
    def weighting_variable(self, change_curr_sample: bool, sample: str):
        """
        Choose the weighting variable for the averaging in each bin in the data reduction.
        
        Parameters
        ----------
            change_curr_sample : bool
                'change_curr_sample' child.
            sample : str
                'sample' child.
        """
    def reset_min_and_max(self, sample_var: str, reset_range: bool):
        """
        Reset the min and max values of the range to be considered for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            reset_range : bool
                'reset_range' child.
        """
    def set_minimum(self, sample_var: str, min_val: float | str):
        """
        Set the minimum value of the range to be considered for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            min_val : real
                'min_val' child.
        """
    def set_maximum(self, sample_var: str, max_val: float | str):
        """
        'set_maximum' command.
        """
    def use_logarithmic(self, sample_var: str, enable_log: bool):
        """
        Switch on or off logarithmic scaling to be used for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            enable_log : bool
                'enable_log' child.
        """
    def number_of_bins(self, sample_var: str, num_bins: int):
        """
        Set the number of bins to be used for a specific variable in the data reduction.
        
        Parameters
        ----------
            sample_var : str
                'sample_var' child.
            num_bins : int
                'num_bins' child.
        """
    def all_variables_number_of_bins(self, all_var_num_of_bins: int):
        """
        Set the number of bins to be used for ALL variables in the data reduction.
        
        Parameters
        ----------
            all_var_num_of_bins : int
                'all_var_num_of_bins' child.
        """
    def list_settings(self):
        """
        List all user inputs for the sample picked for data reduction.
        """
    return_type: str

class reduction(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    setup_reduction: setup_reduction
    def pick_sample_to_reduce(self, change_curr_sample: bool, sample: str):
        """
        Pick a sample for which to first set-up and then perform the data reduction.
        
        Parameters
        ----------
            change_curr_sample : bool
                'change_curr_sample' child.
            sample : str
                'sample' child.
        """
    def reduce_picked_sample(self, check_reduction_wt: bool, file_name: str, overwrite: bool):
        """
        Reduce a sample after first picking it and setting up all data-reduction options and parameters.
        
        Parameters
        ----------
            check_reduction_wt : bool
                'check_reduction_wt' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class histogram_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    histogram_options: histogram_options
    histogram_parameters: histogram_parameters
    plot_write_sample: plot_write_sample
    reduction: reduction
    def compute_sample(self, sample: str, variable: str):
        """
        Compute minimum/maximum of a sample variable.
        
        Parameters
        ----------
            sample : str
                'sample' child.
            variable : str
                'variable' child.
        """
    def delete_sample(self, sample: str):
        """
        'delete_sample' command.
        """
    def list_samples(self):
        """
        Show all samples in loaded sample list.
        """
    def read_sample_file(self, sample_file: str):
        """
        Read a sample file and add it to the sample list.
        
        Parameters
        ----------
            sample_file : str
                The name of a sample file to be loaded.
        """
    def dpm_sample_contour_plots(self, sample_name: str, interval_size: float | str):
        """
        Prepare named expressions from data in a DPM sample file (collected at a cut plane surface) for contour plotting.
        
        Parameters
        ----------
            sample_name : str
                'sample_name' child.
            interval_size : real
                'interval_size' child.
        """
    return_type: str

class user_defined_functions_1(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sort_sample_files(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class sample_trajectories(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    user_defined_functions: user_defined_functions_1
    sort_sample_files: sort_sample_files
    def sample(self, injections: list[str], boundaries: list[str], lines: list[str], planes: list[str], op_udf: str, append_sample: bool, accumulate_rates: bool):
        """
        'sample' command.
        """
    return_type: str

class discrete_phase_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    histogram: histogram_1
    sample_trajectories: sample_trajectories
    def summary(self):
        """
        Print discrete phase summary report of particle fates.
        """
    def extended_summary(self, write_summary_to_file: bool, file_name: str, include_in_domains_particles: bool, pick_injection: bool, injection: str):
        """
        Print extended discrete phase summary report of particle fates, with options.
        
        Parameters
        ----------
            write_summary_to_file : bool
                'write_summary_to_file' child.
            file_name : str
                'file_name' child.
            include_in_domains_particles : bool
                'include_in_domains_particles' child.
            pick_injection : bool
                'pick_injection' child.
            injection : str
                'injection' child.
        """
    def zone_summaries_per_injection(self, summary_state: bool, reset_dpm_summaries: bool):
        """
        Enable per-injection zone DPM summaries.
        
        Parameters
        ----------
            summary_state : bool
                'summary_state' child.
            reset_dpm_summaries : bool
                'reset_dpm_summaries' child.
        """
    return_type: str

class fluxes(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def mass_flow(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print mass flow rate at inlets and outlets.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def heat_transfer(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def heat_transfer_sensible(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print sensible heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def rad_heat_trans(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print radiation heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def film_mass_flow(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print film mass flow rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def film_heat_transfer(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print film heat transfer rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def electric_current(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print electric current rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def pressure_work(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print pressure work rate at moving boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def viscous_work(self, domain_val: str, all_bndry_zones: bool, zone_list: list[str], write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Print viscous work rate at boundaries.
        
        Parameters
        ----------
            domain_val : str
                'domain_val' child.
            all_bndry_zones : bool
                All the boundary/interior zones.
            zone_list : List
                'zone_list' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class flow(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def species_mass_flow(self, domain_val: str):
        """
        'species_mass_flow' command.
        """
    def element_mass_flow(self, domain_val: str):
        """
        'element_mass_flow' command.
        """
    def uds_flow(self, domain_val: str):
        """
        'uds_flow' command.
        """
    return_type: str

class modified_setting_options(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def modified_setting(self, setting_type: list[str]):
        """
        Specify which settings will be checked for non-default status for generating the Modified Settings Summary table.
        
        Parameters
        ----------
            setting_type : List
                'setting_type' child.
        """
    def write_user_setting(self, file_name: str, overwrite: bool):
        """
        Write the contents of the Modified Settings Summary table to a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class population_balance(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def moments(self, surface_list: list[str], volume_list: list[str], num_of_moments: int, write_to_file: bool, filename: str, overwrite: bool):
        """
        Set moments for population balance.
        
        Parameters
        ----------
            surface_list : List
                'surface_list' child.
            volume_list : List
                'volume_list' child.
            num_of_moments : int
                'num_of_moments' child.
            write_to_file : bool
                'write_to_file' child.
            filename : str
                'filename' child.
            overwrite : bool
                'overwrite' child.
        """
    def number_density(self, report_type: str, disc_output_type: str, qmom_output_type: str, smm_output_type: str, surface_list: list[str], volume_list: list[str], num_dens_func: str, dia_upper_limit: float | str, file_name: str, overwrite: bool):
        """
        'number_density' command.
        """
    return_type: str

class heat_exchange_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def computed_heat_rejection(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool, overwrite: bool):
        """
        'computed_heat_rejection' command.
        """
    def inlet_temperature(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool, overwrite: bool):
        """
        'inlet_temperature' command.
        """
    def outlet_temperature(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool, overwrite: bool):
        """
        'outlet_temperature' command.
        """
    def mass_flow_rate(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool, overwrite: bool):
        """
        'mass_flow_rate' command.
        """
    def specific_heat(self, heat_exchanger: str, fluid_zone: str, boundary_zone: str, report_type: str, write_to_file: bool, file_name: str, append_file: bool, overwrite: bool):
        """
        'specific_heat' command.
        """
    return_type: str

class system(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def proc_statistics(self):
        """
        Fluent process information.
        """
    def sys_statistics(self):
        """
        System information.
        """
    def gpgpu_statistics(self):
        """
        GPGPU information.
        """
    def time_statistics(self):
        """
        Time usage information.
        """
    return_type: str

class histogram(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def print(self, domain: str, cell_function: str, min_val: float | str, max_val: float | str, num_division: int, set_all_zones: bool, threads_list: list[str], file_name: str, overwrite: bool):
        """
        Print a histogram of a scalar quantity.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            min_val : real
                'min_val' child.
            max_val : real
                'max_val' child.
            num_division : int
                'num_division' child.
            set_all_zones : bool
                'set_all_zones' child.
            threads_list : List
                'threads_list' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        """
    def write(self, domain: str, cell_function: str, min_val: float | str, max_val: float | str, num_division: int, set_all_zones: bool, threads_list: list[str], file_name: str, overwrite: bool):
        """
        Write a histogram of a scalar quantity to a file.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            min_val : real
                'min_val' child.
            max_val : real
                'max_val' child.
            num_division : int
                'num_division' child.
            set_all_zones : bool
                'set_all_zones' child.
            threads_list : List
                'threads_list' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class report(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    simulation_reports: simulation_reports
    discrete_phase: discrete_phase_1
    fluxes: fluxes
    flow: flow
    modified_setting_options: modified_setting_options
    population_balance: population_balance
    heat_exchange: heat_exchange_1
    system: system
    histogram: histogram
    def aero_optical_distortions(self):
        """
        Optics report object.
        """
    def forces(self, options: str, domain_val: str, all_wall_zones: bool, wall_thread_list: list[str], direction_vector: list[float | str], momentum_center: list[float | str], momentum_axis: list[float | str], pressure_coordinate: str, coord_val: float | str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        'forces' command.
        """
    def mphase_summary(self, verbosity_option: str):
        """
        Multiphase Summary and Recommendations.
        
        Parameters
        ----------
            verbosity_option : str
                'verbosity_option' child.
        """
    def particle_summary(self, injection_names: list[str]):
        """
        Print summary report for all current particles.
        
        Parameters
        ----------
            injection_names : List
                'injection_names' child.
        """
    def path_line_summary(self):
        """
        Print path-line-summary report.
        """
    def projected_surface_area(self, surface_id_val: list[int], min_feature_size: float | str, proj_plane_norm_comp: list[float | str]):
        """
        Print total area of the projection of a group of surfaces to a plane.
        
        Parameters
        ----------
            surface_id_val : List
                'surface_id_val' child.
            min_feature_size : real
                'min_feature_size' child.
            proj_plane_norm_comp : List
                'proj_plane_norm_comp' child.
        """
    def summary(self, write_to_file: bool, file_name: str, overwrite: bool):
        """
        Print report summary.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        """
    def surface_integrals(self, report_type: str, surface_id: list[str], add_custom_vector: bool, cust_vec_name: str, domain_cx: str, cell_cx: str, domain_cy: str, cell_cy: str, domain_cz: str, cell_cz: str, cust_vec_func: str, domain_report: str, cell_report: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Create a surface integral report.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            surface_id : List
                'surface_id' child.
            add_custom_vector : bool
                'add_custom_vector' child.
            cust_vec_name : str
                'cust_vec_name' child.
            domain_cx : str
                'domain_cx' child.
            cell_cx : str
                'cell_cx' child.
            domain_cy : str
                'domain_cy' child.
            cell_cy : str
                'cell_cy' child.
            domain_cz : str
                'domain_cz' child.
            cell_cz : str
                'cell_cz' child.
            cust_vec_func : str
                'cust_vec_func' child.
            domain_report : str
                'domain_report' child.
            cell_report : str
                'cell_report' child.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    def volume_integrals(self, report_type: str, thread_id_list: list[str], domain: str, cell_function: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool, overwrite: bool):
        """
        Create a volume integral report.
        
        Parameters
        ----------
            report_type : str
                'report_type' child.
            thread_id_list : List
                'thread_id_list' child.
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
            overwrite : bool
                'overwrite' child.
        """
    return_type: str

class results(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    surfaces: surfaces_4
    graphics: graphics
    plot: plot_1
    scene: scene
    animations: animations
    report: report
    return_type: str

class input_parameters_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class input_parameters(NamedObject[input_parameters_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: input_parameters_child
    return_type: str

class output_parameters_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class output_parameters(NamedObject[output_parameters_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, from_: str, to: str):
        """
        'duplicate' command.
        """
    child_object_type: output_parameters_child
    return_type: str

class write_data_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class capture_simulation_report_data_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class design_points_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    input_parameters: input_parameters
    output_parameters: output_parameters
    write_data: write_data_1
    capture_simulation_report_data: capture_simulation_report_data_1
    return_type: str

class design_points(NamedObject[design_points_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, design_point: str):
        """
        Duplicate Design Point.
        
        Parameters
        ----------
            design_point : str
                'design_point' child.
        """
    def create_1(self, write_data: bool, capture_simulation_report_data: bool):
        """
        Add new Design Point.
        
        Parameters
        ----------
            write_data : bool
                'write_data' child.
            capture_simulation_report_data : bool
                'capture_simulation_report_data' child.
        """
    def load_case_data(self):
        """
        Loads relevant case/data file for current design point.
        """
    def set_as_current(self, design_point: str):
        """
        Set current design point.
        
        Parameters
        ----------
            design_point : str
                'design_point' child.
        """
    def delete_design_points(self, design_points: list[str]):
        """
        Delete Design Points.
        
        Parameters
        ----------
            design_points : List
                'design_points' child.
        """
    def save_journals(self, separate_journals: bool):
        """
        Save Journals.
        
        Parameters
        ----------
            separate_journals : bool
                'separate_journals' child.
        """
    def clear_generated_data(self, design_points: list[str]):
        """
        Clear Generated Data.
        
        Parameters
        ----------
            design_points : List
                'design_points' child.
        """
    def update_current(self):
        """
        Update Current Design Point.
        """
    def update_all(self):
        """
        Update All Design Point.
        """
    def update_selected(self, design_points: list[str]):
        """
        Update Selected Design Points.
        
        Parameters
        ----------
            design_points : List
                'design_points' child.
        """
    child_object_type: design_points_child
    return_type: str

class current_design_point(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class parametric_studies_child(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    design_points: design_points
    current_design_point: current_design_point
    return_type: str

class parametric_studies(NamedObject[parametric_studies_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_1(self):
        """
        'list' command.
        """
    def list_properties_1(self, object_name: str):
        """
        'list_properties' command.
        """
    def duplicate(self, copy_design_points: bool):
        """
        Duplicate Parametric Study.
        
        Parameters
        ----------
            copy_design_points : bool
                'copy_design_points' child.
        """
    def initialize(self, project_filename: str):
        """
        Start Parametric Study.
        
        Parameters
        ----------
            project_filename : str
                'project_filename' child.
        """
    def set_as_current(self, study_name: str):
        """
        Set As Current Study.
        
        Parameters
        ----------
            study_name : str
                'study_name' child.
        """
    def use_base_data(self):
        """
        Use Base Data.
        """
    def export_design_table(self, filepath: str):
        """
        Export Design Point Table.
        
        Parameters
        ----------
            filepath : str
                'filepath' child.
        """
    def import_design_table(self, filepath: str, delete_existing: bool):
        """
        Import Design Point Table.
        
        Parameters
        ----------
            filepath : str
                'filepath' child.
            delete_existing : bool
                'delete_existing' child.
        """
    child_object_type: parametric_studies_child
    return_type: str

class current_parametric_study(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thread_number_method(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fixed_thread_number(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class thread_number_control(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    thread_number_method: thread_number_method
    fixed_thread_number: fixed_thread_number
    return_type: str

class check_verbosity_1(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class across_zones(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class load_vector(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class pre_test(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class auto_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    across_zones: across_zones
    method: method_2
    load_vector: load_vector
    pre_test: pre_test
    def use_case_file_method(self, file_partition_method: bool):
        """
        Enable the use-case-file method for auto partitioning.
        
        Parameters
        ----------
            file_partition_method : bool
                'file_partition_method' child.
        """
    return_type: str

class cell_function_2(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class load_distribution(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class merge_small_regions(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_merge_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class merge(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    merge_small_regions: merge_small_regions
    max_merge_iterations: max_merge_iterations
    return_type: str

class partition_origin_vector_child(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class partition_origin_vector(ListObject[partition_origin_vector_child]):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def list_properties(self, object_at: int):
        """
        'list_properties' command.
        """
    child_object_type: partition_origin_vector_child
    return_type: str

class pre_test_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class smooth_partitioning(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class max_smoothing_iterations(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class smooth_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    smooth_partitioning: smooth_partitioning
    max_smoothing_iterations: max_smoothing_iterations
    return_type: str

class print_verbosity(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class origin_1(RealList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_4(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class laplace_smoothing(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_2
    set: set_4
    return_type: str

class nfaces_as_weights_1(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class user_defined_value(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class nfaces_as_weights(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    nfaces_as_weights: nfaces_as_weights_1
    user_defined_value: user_defined_value
    value: value_1
    return_type: str

class face_area_as_weights(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_layering(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class base_face_zone_for_partitioning(IntegerList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class layering(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use_layering: use_layering
    base_face_zone_for_partitioning: base_face_zone_for_partitioning
    return_type: str

class use(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class use_user_define_value(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class solid_thread_weight(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use: use
    use_user_define_value: use_user_define_value
    value: value_1
    return_type: str

class use_enhancement(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class aspect_ratio_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class stretched_mesh_enhancement(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use_enhancement: use_enhancement
    aspect_ratio: aspect_ratio_1
    return_type: str

class user_defined_6(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class hybrid_optimization(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class particle_weight(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use: use
    user_defined: user_defined_6
    value: value_1
    hybrid_optimization: hybrid_optimization
    return_type: str

class vof_free_surface_weight(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use: use
    user_defined: user_defined_6
    value: value_1
    return_type: str

class isat_weight(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use: use
    user_defined: user_defined_6
    value: value_1
    return_type: str

class fluid_solid_rebalance_after_read_case(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class model_weighted_partition(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class load_balancing(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interval(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dpm_load_balancing(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    load_balancing: load_balancing
    threshold: threshold
    interval: interval
    return_type: str

class set_3(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    cell_function: cell_function_2
    load_distribution: load_distribution
    merge: merge
    partition_origin_vector: partition_origin_vector
    pre_test: pre_test_1
    smooth: smooth_1
    print_verbosity: print_verbosity
    origin: origin_1
    laplace_smoothing: laplace_smoothing
    nfaces_as_weights: nfaces_as_weights
    face_area_as_weights: face_area_as_weights
    layering: layering
    solid_thread_weight: solid_thread_weight
    stretched_mesh_enhancement: stretched_mesh_enhancement
    particle_weight: particle_weight
    vof_free_surface_weight: vof_free_surface_weight
    isat_weight: isat_weight
    fluid_solid_rebalance_after_read_case: fluid_solid_rebalance_after_read_case
    model_weighted_partition: model_weighted_partition
    dpm_load_balancing: dpm_load_balancing
    def across_zones(self, across_zone_boundaries: bool):
        """
        Enable partitioning by zone or by domain.
        
        Parameters
        ----------
            across_zone_boundaries : bool
                'across_zone_boundaries' child.
        """
    def all_off(self):
        """
        Disable all optimization.
        """
    def all_on(self):
        """
        Enable all optimization.
        """
    return_type: str

class partition_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    auto: auto_1
    set: set_3
    def combine_partition(self, number_of_partitions: int):
        """
        Merge every N partitions.
        
        Parameters
        ----------
            number_of_partitions : int
                'number_of_partitions' child.
        """
    def merge_clusters(self, merge_iterations: int):
        """
        Merge partition clusters.
        
        Parameters
        ----------
            merge_iterations : int
                'merge_iterations' child.
        """
    def method(self, partition_method: str, count: int):
        """
        Partition the domain.
        
        Parameters
        ----------
            partition_method : str
                'partition_method' child.
            count : int
                'count' child.
        """
    def print_partitions(self):
        """
        Print partition information.
        """
    def print_active_partitions(self):
        """
        Print active partition information.
        """
    def print_stored_partitions(self):
        """
        Print stored partition information.
        """
    def reorder_partitions(self):
        """
        Reorder partitions.
        """
    def reorder_partitions_to_architecture(self):
        """
        Reorder partitions to architecture.
        """
    def smooth_partition(self, smoothing_iteration: int):
        """
        Smooth partition interface.
        
        Parameters
        ----------
            smoothing_iteration : int
                Maximum number of smoothing iterations.
        """
    def use_stored_partitions(self):
        """
        Use stored partitioning.
        """
    return_type: str

class partition_mask(IntegerList):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class verbosity_12(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class time_out(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class fast_io(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    partition_mask: partition_mask
    verbosity: verbosity_12
    time_out: time_out
    fast_io: fast_io
    return_type: str

class use_multi_physics(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class physical_models_2(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use_multi_physics: use_multi_physics
    threshold: threshold
    interval: interval
    return_type: str

class auto_2(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class dynamic_mesh(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use: use
    auto: auto_2
    threshold: threshold
    interval: interval
    return_type: str

class mesh_adaption(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    use: use
    threshold: threshold
    return_type: str

class load_balance(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    physical_models: physical_models_2
    dynamic_mesh: dynamic_mesh
    mesh_adaption: mesh_adaption
    return_type: str

class enabled_4(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class iter_per_coupling_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class method_6(String, AllowedValuesMixin):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class interval_1(Real):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class single_session_coupling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_6
    type: type_2
    interval: interval_1
    frequency: frequency_1
    return_type: str

class two_session_coupling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    method: method_6
    type: type_2
    frequency: frequency_1
    return_type: str

class coupling(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    iter_per_coupling_count: iter_per_coupling_count
    single_session_coupling: single_session_coupling
    two_session_coupling: two_session_coupling
    return_type: str

class process_count(Integer):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class host_name(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class helper_session_setup(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    process_count: process_count
    host_name: host_name
    return_type: str

class helper_session(Boolean):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class set_5(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    coupling: coupling
    helper_session_setup: helper_session_setup
    helper_session: helper_session
    return_type: str

class conjugate_heat_transfer(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    enabled: enabled_4
    set: set_5
    return_type: str

class solve(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def iterate(self, iter_count: int, time_steps_count: int, fluid_time_step_count: int, iter_per_time_step_count: int):
        """
        Iteration the multidomain conjugate heat transfer.
        
        Parameters
        ----------
            iter_count : int
                'iter_count' child.
            time_steps_count : int
                'time_steps_count' child.
            fluid_time_step_count : int
                'fluid_time_step_count' child.
            iter_per_time_step_count : int
                'iter_per_time_step_count' child.
        """
    def dual_time_iterate(self, iter_count: int, time_steps_count: int, fluid_time_step_count: int, iter_per_time_step_count: int):
        """
        Dual-time iterate the multidomain conjugate heat transfer.
        
        Parameters
        ----------
            iter_count : int
                'iter_count' child.
            time_steps_count : int
                'time_steps_count' child.
            fluid_time_step_count : int
                'fluid_time_step_count' child.
            iter_per_time_step_count : int
                'iter_per_time_step_count' child.
        """
    return_type: str

class multidomain(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    conjugate_heat_transfer: conjugate_heat_transfer
    solve: solve
    return_type: str

class shell_script_path(String):
    _version: str
    fluent_name: str
    _python_name: str
    return_type: str

class network_1(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    shell_script_path: shell_script_path
    def kill_all_nodes(self, invalidate_case: bool, delete_all_compute_nodes: bool):
        """
        Delete all compute nodes from virtual machine.
        
        Parameters
        ----------
            invalidate_case : bool
                'invalidate_case' child.
            delete_all_compute_nodes : bool
                'delete_all_compute_nodes' child.
        """
    def kill_node(self, compute_node: int, invalidate_case: bool):
        """
        'kill_node' command.
        """
    def spawn_node(self, hostname: str, username: str):
        """
        Spawn a compute node process on a specified machine.
        
        Parameters
        ----------
            hostname : str
                'hostname' child.
            username : str
                'username' child.
        """
    def load_hosts(self, host_file: str):
        """
        Read a hosts file.
        
        Parameters
        ----------
            host_file : str
                'host_file' child.
        """
    def save_hosts(self, host_file: str):
        """
        Write a hosts file.
        
        Parameters
        ----------
            host_file : str
                'host_file' child.
        """
    return_type: str

class timer(Group):
    _version: str
    fluent_name: str
    _python_name: str
    command_names: list[str]
    def usage(self):
        """
        Print solver timer.
        """
    def reset(self):
        """
        Reset domain timers.
        """
    return_type: str

class parallel(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    command_names: list[str]
    thread_number_control: thread_number_control
    check_verbosity: check_verbosity_1
    partition: partition_1
    set: set_2
    load_balance: load_balance
    multidomain: multidomain
    network: network_1
    timer: timer
    def check(self):
        """
        Parallel check.
        """
    def show_connectivity(self, compute_node: int):
        """
        Show machine connectivity.
        
        Parameters
        ----------
            compute_node : int
                'compute_node' child.
        """
    def latency(self):
        """
        Show network latency.
        """
    def bandwidth(self):
        """
        Show network bandwidth.
        """
    return_type: str

class root(Group):
    _version: str
    fluent_name: str
    _python_name: str
    child_names: list[str]
    file: file
    mesh: mesh
    server: server
    setup: setup
    solution: solution
    results: results
    parametric_studies: parametric_studies
    current_parametric_study: current_parametric_study
    parallel: parallel
    report: report
    return_type: str

