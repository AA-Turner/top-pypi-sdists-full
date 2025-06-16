"""
Generate figures and RST documents from the HDMF YAML specification for the format specification documentation
"""

# TODO Make SpecToRST.render_namespace.type_hierarchy_include_html and type_hierarchy_include_latex configurable


from hdmf.spec import GroupSpec, DatasetSpec, NamespaceCatalog, SpecNamespace
import warnings
import traceback
import os

from .doctools.rst import RSTSectionLabelHelper as LabelHelper
from .doctools.rst import RSTDocument, RSTFigure
from .doctools.renderrst import SpecToRST, DataTypeSection
from .doctools.output import PrintHelper, GitHashHelper

############################################################################
# Import settings from the configuration file and define default settings
###########################################################################
try:
    from conf_doc_autogen import spec_show_yaml_src, \
        spec_generate_src_file, \
        spec_show_hierarchy_plots, \
        spec_file_per_type, \
        spec_show_subgroups_in_seperate_table, \
        spec_appreviate_main_object_doc_in_tables, \
        spec_show_title_for_tables, \
        spec_table_depth_char, \
        spec_add_latex_clearpage_after_ndt_sections, \
        spec_resolve_type_inc, \
        spec_output_dir, \
        spec_clean_output_dir_if_old_git_hash, \
        spec_skip_doc_autogen_if_current_git_hash, \
        spec_input_spec_dir, \
        spec_output_doc_filename, \
        spec_output_src_filename, \
        spec_output_master_filename, \
        spec_output_doc_type_hierarchy_filename, \
        spec_input_namespace_filename, \
        spec_input_default_namespace
    # Optional settings parameters set to defaults if setting is not available
    try:
        from conf_doc_autogen import spec_default_type_map
    except ImportError:
        warnings.warn("spec_default_type_map not set. Using None as default.")
        spec_default_type_map = None
    try:
        from conf_doc_autogen import spec_group_spec_cls
    except ImportError:
        warnings.warn("spec_group_spec_cls not set. Using HDMF GroupSpec class as default.")
        spec_group_spec_cls = GroupSpec
    spec_type_key = spec_group_spec_cls.type_key()
    spec_inc_key = spec_group_spec_cls.inc_key()
    spec_def_key = spec_group_spec_cls.def_key()
    try:
        from conf_doc_autogen import spec_dataset_spec_cls
    except ImportError:
        warnings.warn("spec_dataset_spec_cls not set. Using HDMF DatasetSpec class as default.")
        spec_dataset_spec_cls = DatasetSpec
    try:
        from conf_doc_autogen import spec_namespace_spec_cls
    except ImportError:
        warnings.warn("spec_namespace_spec_cls not set. Using HDMF SpecNamespace class as default.")
        spec_namespace_spec_cls = SpecNamespace
except ImportError:
    print("Could not import SPHINX conf_doc_autogen.py file. Please add the PYTHONPATH " +
          "to the source directory where the conf_doc_autogen.py file is located")
    exit(0)

try:
    # Force matplotlib to use Agg backend. Added to make the build work on ReadTheDocs
    import matplotlib

    matplotlib.use('Agg')
    # make sure that we can import pyplot an networkX
    from matplotlib import pyplot as plt
    from .doctools.render import NXGraphHierarchyDescription, HierarchyDescription

    # If all the imports worked then we can render the plots
    INCLUDE_GRAPHS = True
except ImportError:
    # Some import failed so disable rendering of plots
    INCLUDE_GRAPHS = False
    warnings.warn('DISABLING RENDERING OF SPEC GRAPHS DUE TO IMPORT ERROR')


CUSTOM_LATEX_TABLE_COLUMNS = "|p{4cm}|p{1cm}|p{10cm}|"


def load_namespace(namespace_file,
                   default_namespace='core',
                   resolve=True,
                   default_type_map=None,
                   group_spec_cls=GroupSpec,
                   dataset_spec_cls=DatasetSpec,
                   spec_namespace_cls=SpecNamespace):
    """
    Helper function used to load namespace from file

    :param namespace_file: String with the path to the YAML specification of the namespace
    :param default_namespace: String with the name of the default namespace
    :param resolve: Bool indicating whether the type inclusions should be resolved in the namespace
    :param default_type_map: The default TypeMap to be used for loading namespaces. This is useful, e.g., when we have
                             an API (e.g., PyNWB) where we have type map that we want to extend/reuse.

    :return: NamespaceCatalog
    """
    # Default load when documenting extensions
    namespace_catalog = None
    if default_type_map is not None:
        try:
            default_type_map.load_namespaces(namespace_file, resolve=resolve)
            namespace_catalog = default_type_map.namespace_catalog
        # When rendering the core spec we'll get a KeyError because it already exists
        # so we'll load the namespace separately
        except KeyError:
            pass
    # Load the namespace separately if it already exists or we don't have a default type map specified
    if namespace_catalog is None:
        namespace_catalog = NamespaceCatalog(default_namespace,
                                             group_spec_cls=group_spec_cls,
                                             dataset_spec_cls=dataset_spec_cls,
                                             spec_namespace_cls=spec_namespace_cls)
        namespace_catalog.load_namespaces(namespace_file, resolve=resolve)

    return namespace_catalog


def render_data_type_section(section,
                             spec_catalog,
                             desc_doc,
                             src_doc,
                             file_dir,
                             show_hierarchy_plots=True,
                             show_yaml_src=True,
                             file_per_type=False,
                             print_status=True):
    """
    Render the documentation for a set of data_types defined in a spec_catalog

    :param section: The DataTypeSection to be rendered to the given RST documents
    :param spec_catalog: Catalog of specifications
    :param desc_doc: RSTDocument where the descriptions of the documents should be rendered
    :param src_doc: RSTDocument where the YAML sources of the data_types should be rendered. Set to None
                    if sources should be rendered in the desc_doc directly.
    :param file_dir: Directory where figures and outpy RST docs should be stored
    :param show_hierarchy_plots: Create figures showing the hierarchy defined by the spec
    :param show_yaml_src: Boolean indicating that we should render the YAML source in the src_doc
    :param file_per_type: Generate a separate rst files for each data_type and include them
                          in the src_doc and desc_doc (True). If set to False then write the
                          contents to src_doc and desc_doc directly.
    :param print_status: Bool indicating whether to print progress and debugging messages to standard out

    """
    # Determine where the YAML source should be rendered
    if src_doc is None:
        seperate_src_file = False
        src_doc = desc_doc
    else:
        seperate_src_file = True

    # Render the heading for the section
    # Add labels and tile for the subsections in the description and source RSTDocuments
    desc_doc.add_label(section.title.replace(' ', '_'))
    desc_doc.add_subsection(section.title)
    if seperate_src_file:
        src_doc.add_label(section.title.replace(' ', '_') + '_src')
        src_doc.add_subsection(section.title)

    # Render the introduction for the section
    if section.intro is not None and section.intro != '':
        desc_doc.add_text(section.intro)
        desc_doc.add_text(desc_doc.newline + desc_doc.newline)
        if seperate_src_file:
            src_doc.add_text(section.intro)
            src_doc.add_text(src_doc.newline + desc_doc.newline)

    # Render the subsubsections for all the individual data types
    for rt in section.data_types:
        if print_status:
            PrintHelper.print("BUILDING %s" % rt, PrintHelper.BOLD)
        # Get the spec
        rt_spec = spec_catalog.get_spec(rt)
        rt_source_file = spec_catalog.get_spec_source_file(rt)
        # Check if the spec extends another spec
        extend_type = rt_spec.get(spec_inc_key, None)
        # Define the docs we need to write to
        type_desc_doc = desc_doc if not file_per_type else RSTDocument()
        type_src_doc = src_doc if not file_per_type else RSTDocument()

        #######################################################
        #  Create the base documentation for the current type
        #######################################################
        # Create the section heading and label
        type_desc_doc.add_label(LabelHelper.get_section_label(rt))
        section_heading = rt
        type_desc_doc.add_subsubsection(section_heading)
        type_desc_doc.add_text('**Overview:** ')
        # Add the document string for the data_type to the document
        rt_clean_doc = SpecToRST.clean_schema_doc_string(rt_spec['doc'],
                                                         add_prefix=type_desc_doc.newline+type_desc_doc.newline,
                                                         add_postfix=type_desc_doc.newline,
                                                         rst_format='**')
        type_desc_doc.add_text(rt_clean_doc)
        type_desc_doc.add_text(type_desc_doc.newline + type_desc_doc.newline)
        # Add note if necessary to indicate that the following documentation only shows changes to the parent class
        if extend_type is not None:
            extend_type = rt_spec[spec_inc_key]
            sentence_end = " with the following additions or changes." \
                if not spec_resolve_type_inc \
                else ". The following is a description of the complete structure of" + \
                     "``%s`` including all inherited components." % rt
            type_desc_doc.add_text("``%s`` extends ``%s`` and includes all elements of %s%s" %
                                   (rt,
                                    extend_type,
                                    type_desc_doc.get_reference(LabelHelper.get_section_label(extend_type),
                                                                extend_type),
                                    sentence_end))
            type_desc_doc.add_text(type_desc_doc.newline + type_desc_doc.newline)

        # Define the additional details about the doc to be rendered in the overview
        ignore_props = [spec_def_key, 'default_name', 'name']   # Properties from the spec to be ignored here
        additional_props = []  # Additional properties that should be shown
        # Add list of the types this type inherits from. The ancestry always includes the type itself as first
        # entry, so we ignore the inheritance if the ancestry is only the type itself.
        inherits_from_str = SpecToRST.render_inherits_from(spec_catalog=spec_catalog,
                                                           data_type=rt,
                                                           prefix="**Inherits from:** ",
                                                           ignore_self=True)
        if inherits_from_str is not None:
            additional_props.append(inherits_from_str)
        # Add list of all the subtypes of this type
        subtypes_str = SpecToRST.render_subtypes(spec_catalog=spec_catalog,
                                         data_type=rt,
                                         prefix="**Subtypes:** ")
        if subtypes_str is not None:
            additional_props.append(subtypes_str)
        # Add name of the source file
        additional_props.append('**Source filename:** %s' % rt_source_file)
        # Add a link to the source if rendered separately
        if seperate_src_file:
            additional_props.append(
                '**Source Specification:** see %s' %
                type_desc_doc.get_numbered_reference(
                    label=LabelHelper.get_src_section_label(rt,
                                                            spec_generate_src_file, spec_show_yaml_src)))

        # Render the properties of the spec as part of the overview
        type_desc_doc.add_text(SpecToRST.render_specification_properties(rt_spec,
                                                                         type_desc_doc.newline,
                                                                         ignore_props=ignore_props,
                                                                         append_items=additional_props))
        type_desc_doc.add_text(type_desc_doc.newline)

        ##################################################
        # Render the graph for the spec if necessary
        #################################################
        if INCLUDE_GRAPHS:
            try:
                if show_hierarchy_plots:
                    temp = HierarchyDescription.from_spec(rt_spec)
                    temp_graph = NXGraphHierarchyDescription(temp)
                    temp_figsize = temp_graph.suggest_figure_size()
                    temp_xlim = temp_graph.suggest_xlim()
                    temp_ylim = None  # temp_graph.suggest_ylim()
                    if len(temp_graph.graph.nodes(data=False)) > 2:
                        fig = temp_graph.draw(show_plot=False,     # noqa F841
                                              figsize=temp_figsize,
                                              xlim=temp_xlim,
                                              ylim=temp_ylim,
                                              label_font_size=10)
                        plt.savefig(os.path.join(file_dir, '%s.pdf' % rt),
                                    format='pdf',
                                    bbox_inches='tight',
                                    pad_inches=0)
                        plt.savefig(os.path.join(file_dir, '%s.png' % rt),
                                    format='png',
                                    dpi=300,
                                    bbox_inches='tight',
                                    pad_inches=0)
                        plt.close()
                        type_desc_doc.add_figure(RSTFigure(image_path='./_format_auto_docs/'+rt+".*", alt=rt))
                        if print_status:
                            PrintHelper.print("    " + rt + '-- RENDER OK.',
                                              PrintHelper.OKGREEN)
                    else:
                        if print_status:
                            PrintHelper.print("    " + rt + '-- SKIPPED RENDER HIERARCHY. TWO OR FEWER NODES.',
                                              PrintHelper.OKBLUE)
                else:
                    if print_status:
                        PrintHelper.print("    " + rt + '-- SKIPPED RENDER HIERARCHY. See conf.py',
                                          PrintHelper.OKBLUE)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                PrintHelper.print(rt + '-- RENDER HIERARCHY FAILED: ' + traceback.format_exc(),
                                  PrintHelper.FAIL)
        else:
            if show_hierarchy_plots:
                PrintHelper.print(rt + '-- RENDER HIERARCHY FAILED DUE TO MISSING PACKAGES',
                                  PrintHelper.FAIL)

        ####################################################################
        #  Add the YAML sources to the document if requested
        ####################################################################
        # If the YAML are shown in a separate chapter than add section headings
        if seperate_src_file:
            # Add a section to the file for the sources
            src_sec_lable = LabelHelper.get_src_section_label(rt, spec_generate_src_file, spec_show_yaml_src)
            type_src_doc.add_label(src_sec_lable)
            type_src_doc.add_subsubsection(section_heading)
            if extend_type is not None:
                type_src_doc.add_text('**Extends:** %s' %
                                      type_src_doc.get_reference(LabelHelper.get_section_label(extend_type),
                                                                 extend_type) +
                                      type_src_doc.newline +
                                      type_src_doc.newline)
            type_src_doc.add_text('**Description:** see %s' %
                                  type_src_doc.get_numbered_reference(LabelHelper.get_section_label(rt)) +
                                  type_src_doc.newline +
                                  type_src_doc.newline)

        # Add the YAML for the current spec
        if show_yaml_src:
            type_src_doc.add_text('**YAML Specification:**' + type_src_doc.newline + type_src_doc.newline)
            type_src_doc.add_spec(rt_spec)

        #############################################################################
        #  Add table with dataset and attribute descriptions for the data_type
        ############################################################################
        type_desc_doc.add_text(type_desc_doc.newline)
        rt_spec_data_table = SpecToRST.render_spec_table(
            spec=rt_spec,
            depth_char=spec_table_depth_char,
            show_subgroups=not spec_show_subgroups_in_seperate_table,
            appreviate_main_object_doc=spec_appreviate_main_object_doc_in_tables)
        # Only show the datasets and attributes table if it contains additional information
        if rt_spec_data_table.num_rows() > 1:
            rt_spec_data_table_title = None
            if spec_show_title_for_tables:
                if not spec_show_subgroups_in_seperate_table:
                    rt_spec_data_table_title = "Groups, Datasets, Links, and Attributes contained in <%s>" % rt
                else:
                    rt_spec_data_table_title = "Datasets, Links, and Attributes contained in <%s>" % rt
            type_desc_doc.add_table(rt_spec_data_table,
                                    title=rt_spec_data_table_title,
                                    table_ref=LabelHelper.get_data_table_label(rt),
                                    latex_tablecolumns=CUSTOM_LATEX_TABLE_COLUMNS)

        #############################################################################
        #  Add table with the main subgroups for the data_type
        ############################################################################
        if spec_show_subgroups_in_seperate_table:
            type_desc_doc.add_text(type_desc_doc.newline)
            rt_spec_group_table = SpecToRST.render_spec_table(
                spec=rt_spec,
                depth_char=spec_table_depth_char,
                show_subattributes=False,
                show_subdatasets=False,
                show_subgroups=True,
                recursive_subgroups=False,
                appreviate_main_object_doc=spec_appreviate_main_object_doc_in_tables)
            # Only show the datasets and attributes table if it contains additional information
            if rt_spec_group_table.num_rows() > 1:
                rt_spec_group_table_title = None
                if spec_show_title_for_tables:
                    rt_spec_group_table_title = "Groups contained in <%s>" % rt
                type_desc_doc.add_table(rt_spec_group_table,
                                        title=rt_spec_group_table_title,
                                        table_ref=LabelHelper.get_group_table_label(rt),
                                        latex_tablecolumns=CUSTOM_LATEX_TABLE_COLUMNS)

        ######################################################
        # Add tables for all subgroups
        #####################################################
        if isinstance(rt_spec, GroupSpec):
            for g in rt_spec.groups:
                SpecToRST.render_group_spec(group_spec=g,
                                            depth_char=spec_table_depth_char,
                                            show_table_titles=spec_show_title_for_tables,
                                            appreviate_main_object_doc=spec_appreviate_main_object_doc_in_tables,
                                            show_subgroups_in_seperate_table=spec_show_subgroups_in_seperate_table,
                                            rst_doc=type_desc_doc,
                                            parent='' if rt != 'NWBFile' else '/')

        ########################################
        #  Write the type-specific files
        #########################################
        # Add includes for the type-specific inc files if necessary
        if file_per_type:
            # Write the files for the source and description
            type_src_filename = os.path.join(file_dir, '%s_source.inc' % rt)
            type_desc_filename = os.path.join(file_dir, '%s_description.inc' % rt)
            type_desc_doc.write(type_desc_filename, 'w')
            if print_status:
                PrintHelper.print("    " + rt + '-- WRITE DESCRIPTION DOC OK.', PrintHelper.OKGREEN)
            type_src_doc.write(type_src_filename, 'w')
            if print_status:
                PrintHelper.print("    " + rt + '-- WRITE SOURCE DOC OK.', PrintHelper.OKGREEN)
            # Include the files in the main documents
            desc_doc.add_include(os.path.basename(file_dir) + "/" + os.path.basename(type_desc_filename))
            src_doc.add_include(os.path.basename(file_dir) + "/" + os.path.basename(type_src_filename))

        #####################################
        # Add a clearpage command for latex
        #######################################
        # to avoid possible troubles with figure placement outside of the current section we add a new page in
        # LaTeX after each main section
        if spec_add_latex_clearpage_after_ndt_sections:
            if seperate_src_file:
                src_doc.add_latex_clearpage()
            desc_doc.add_latex_clearpage()


def nwb_main():
    warnings.warn("nwb_generate_format_docs is deprecated. Please use hdmf_generate_format_docs", DeprecationWarning)
    return main()


def main():

    # Set the output path for the doc sources to be generated
    file_dir = spec_output_dir
    # Set the dir where the input YAML files are located
    spec_dir = spec_input_spec_dir
    # Set the names of the main output files
    doc_filename = os.path.join(file_dir, spec_output_doc_filename)  # Name of the file with main documentation
    # Name of the file where the YAML sources are rendered
    srcdoc_filename = os.path.join(file_dir, spec_output_src_filename) if spec_generate_src_file else None
    master_filename = os.path.join(file_dir, spec_output_master_filename)
    type_hierarchy_doc_filename = os.path.join(file_dir, spec_output_doc_type_hierarchy_filename)
    core_namespace_file = os.path.join(spec_dir, spec_input_namespace_filename)
    git_hash_filename = os.path.join(file_dir, 'git_hash.txt')

    # Clean up the output directory if necessary
    if spec_clean_output_dir_if_old_git_hash:
        if os.path.exists(file_dir):
            if not GitHashHelper.git_hash_match(git_hash_filename):
                import shutil
                shutil.rmtree(file_dir)
                PrintHelper.print('Removed old sources at: %s' % file_dir, col=PrintHelper.OKGREEN)

    # Create the output directory if necessary
    if not os.path.exists(file_dir):
        PrintHelper.print('Generating output directory: %s' % file_dir, col=PrintHelper.OKGREEN)
        os.mkdir(file_dir)
        git_hash_file = open(git_hash_filename, 'wb')
        git_hash_file.write(GitHashHelper.get_git_revision_hash())
        git_hash_file.close()
    else:
        PrintHelper.print('Output directory already exists: %s' % file_dir, col=PrintHelper.OKGREEN)
        if spec_skip_doc_autogen_if_current_git_hash:
            if GitHashHelper.git_hash_match(git_hash_filename):
                PrintHelper.print('Git hash of sources already up-to-date. Skip autogenerate of sources.',
                                  col=PrintHelper.OKGREEN)
                return

    # Load the default namespace to be rendered
    namespace_catalog = load_namespace(namespace_file=core_namespace_file,
                                       default_namespace=spec_input_default_namespace,
                                       resolve=spec_resolve_type_inc,
                                       default_type_map=spec_default_type_map,
                                       group_spec_cls=spec_group_spec_cls,
                                       dataset_spec_cls=spec_dataset_spec_cls,
                                       spec_namespace_cls=spec_namespace_spec_cls)
    default_namespace = namespace_catalog.get_namespace(spec_input_default_namespace)
    spec_catalog = default_namespace.catalog

    # Sort types into sections
    print()
    PrintHelper.print("SORTING TYPES INTO SECTIONS", PrintHelper.BOLD)
    PrintHelper.print("---------------------------", PrintHelper.BOLD)
    type_sections = DataTypeSection.sort_types_to_sections(default_namespace)
    DataTypeSection.print_sections(type_sections)

    # Create the documentation RST file
    desc_doc = RSTDocument()

    # Create the RST file for source files or use the main document in case sources
    # should be included in the main doc directly
    if spec_generate_src_file:
        src_doc = RSTDocument()
        src_doc.add_label("hdmf-type-specification-sources")
        src_doc.add_section("Schema Sources")
    else:
        src_doc = None

    # Create the master document
    masterdoc = RSTDocument()
    masterdoc.add_include(os.path.basename(file_dir) + "/" + os.path.basename(doc_filename))
    if src_doc is not None:
        masterdoc.add_include(os.path.basename(file_dir) + "/" + os.path.basename(srcdoc_filename))

    # Create and render the type hierarchy to RST
    PrintHelper.print("RENDERING TYPE HIERARCHY", PrintHelper.BOLD)
    PrintHelper.print("------------------------", PrintHelper.BOLD)
    type_hierarchy_doc, type_hierarchy = SpecToRST.render_type_hierarchy(spec_catalog)
    type_hierarchy_doc.write(type_hierarchy_doc_filename, 'w')
    PrintHelper.print_type_hierarchy(type_hierarchy)  # Print the hierarchy to the command line for debugging

    # Render the namespace specification
    PrintHelper.print("RENDERING NAMESPACE SPECIFICATION", PrintHelper.BOLD)
    PrintHelper.print("---------------------------------", PrintHelper.BOLD)
    # Create the namespace document
    SpecToRST.render_namespace(
        namespace_catalog=namespace_catalog,
        namespace_name=spec_input_default_namespace,
        desc_doc=desc_doc,
        src_doc=src_doc,
        show_yaml_src=spec_show_yaml_src,
        file_dir=file_dir,
        file_per_type=spec_file_per_type,
        type_hierarchy_include_html=os.path.basename(file_dir) + "/" + os.path.basename(type_hierarchy_doc_filename),
        type_hierarchy_include_latex=None,  # Don't show type hierarchy in tex to avoid deep nesting.
        print_status=True
      )

    # Create the section for the format specification
    PrintHelper.print("RENDERING TYPE SPECIFICATIONS", PrintHelper.BOLD)
    PrintHelper.print("------------------------------", PrintHelper.BOLD)
    # Add a clearpage command for latex to avoid possible troubles with figure placement outside of the current section
    desc_doc.add_latex_clearpage()
    desc_doc.add_label("hdmf-type-specifications")
    desc_doc.add_section("Type Specifications")

    # Render all the sections with the different types
    sec_index = 0
    for key, sec in type_sections.items():
        # Add a latex clearpage for subsequent sections to improve layout of figures and tables
        if sec_index > 0:
            desc_doc.add_latex_clearpage()
        # Render all registered documents for the current section
        render_data_type_section(section=sec,
                                 spec_catalog=spec_catalog,
                                 desc_doc=desc_doc,
                                 src_doc=src_doc,
                                 file_dir=file_dir,
                                 show_hierarchy_plots=spec_show_hierarchy_plots,
                                 show_yaml_src=spec_show_yaml_src,
                                 file_per_type=spec_file_per_type,
                                 print_status=True)
        sec_index += 1

    # Write the RST documents to file
    def write_rst_doc(document, filename, mode='w'):
        if document is not None and filename is not None:
            document.write(filename=filename, mode=mode)
            PrintHelper.print("Write %s" % filename, PrintHelper.OKGREEN)
    write_rst_doc(desc_doc, doc_filename)      # Write the description RST document
    write_rst_doc(src_doc, srcdoc_filename)    # Write the source RST document
    write_rst_doc(masterdoc, master_filename)  # Write the master RST document


if __name__ == "__main__":
    main()
