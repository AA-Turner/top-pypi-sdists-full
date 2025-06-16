"""
Module with helper functions to render hdfm.spec format specifications to
RST documents.
"""
from hdmf.spec import GroupSpec, DatasetSpec, LinkSpec, AttributeSpec, RefSpec
from .output import PrintHelper
from collections import OrderedDict
from .rst import RSTDocument, RSTTable, RSTSectionLabelHelper
import os


class DataTypeSection(dict):
    """
    Dict describing a set of data_types that should be grouped in a section in the documentation.
    The class also provides functions to sort types from an S

    :ivar title: String with the title for the section
    :ivar data_types: List of strings with the names of the data types to be rendered in this section
    :ivar intro: String (or None) with the introduction text for the section.
    """

    def __init__(self, title, data_types=None, intro=None):
        """

        :param title: String with the title of the section
        :param data_types: List of strings with the names of the data_types included in this section
        :param intro: None or RSTDocument with introductory text for the section.
        """
        self['title'] = title
        self['data_types'] = [] if data_types is None else data_types
        self['intro'] = intro

    @property
    def title(self):
        """Get the title for the section"""
        return self['title']

    @property
    def data_types(self):
        """Get list of strings of the data types in this section"""
        return self['data_types']

    @property
    def intro(self):
        """Get the string with the introduction text for the section"""
        return self['intro']

    @staticmethod
    def sort_types_to_sections(namespace):
        """
        From the namespace create a list with descriptions of how to organize the types into sections.

        The strategy for sorting types to sections is based on source files, i.e., the function
        creates one section per source file. The title and intro for the section are as given
        in the namespace. The title is set to the name of the source file if no dedicated title
        is specified in the namespace. The data types are then placed in the sections based on in
        which source file they are defined in.

        :param namespace: The namespace with all the types to be rendered
        :type namespace: hdmf.spec.SpecNamespace object with the specification of the namespace
        :return: List of DataTypeSections


        """
        # Initialize the sections
        sections = OrderedDict()
        for spec_filename in namespace.get_source_files():
            spec_descr = namespace.get_source_description(spec_filename)
            title = spec_filename if 'title' not in spec_descr else spec_descr['title']
            intro = None if 'doc' not in spec_descr else spec_descr['doc']
            sections[spec_filename] = DataTypeSection(title=title,
                                                      intro=intro,
                                                      data_types=[])

        # Add the individual data types to the corresponding sections
        spec_catalog = namespace.catalog
        for nt in spec_catalog.get_registered_types():
            spec_filename = spec_catalog.get_spec_source_file(nt)
            if spec_filename in namespace.get_source_files():
                sections[spec_filename]['data_types'].append(nt)

        # Return the sections
        return sections

    @staticmethod
    def print_sections(type_sections):
        """
        Helper function to print sorting of data_type to sections

        :param type_sections: OrderedDict of DataTypeSection objects. Created, e.g., by
                              DataTypeSection.sort_types_to_sections(...)
        :return:
        """
        indent = "    "
        for key, sec in type_sections.items():
            PrintHelper.print(sec['title'], PrintHelper.OKBLUE+PrintHelper.BOLD)
            if sec['intro']:
                PrintHelper.print(indent + str(sec['intro']), PrintHelper.GRAY)
            PrintHelper.print(indent + str(list(sec['data_types'])), PrintHelper.OKBLUE)


class SpecToRST(object):
    """
    Class with mostly static methods for generatinc RST compliant strings for format specifications
    based on the the hdmf.spec classes.
    """

    # Custom columns for latex used for creating tables for specs
    CUSTOM_LATEX_TABLE_COLUMNS = "|p{4cm}|p{1cm}|p{10cm}|"

    @staticmethod
    def spec_basetype_name(spec):
        """
        Given a spec get a string indicating the primitive type of the spec

        :param spec: The spec object

        :return: String indicating the primitive type (e.g., Dataset, Group, Attribute, Link, Ref, etc.)
        """
        if isinstance(spec, GroupSpec):
            return 'Group'
        elif isinstance(spec, DatasetSpec):
            return 'Dataset'
        elif isinstance(spec, AttributeSpec):
            return 'Attribute'
        elif isinstance(spec, LinkSpec):
            return 'Link'
        elif isinstance(spec, RefSpec):
            return 'Ref'
        else:
            raise ValueError("Unknown specification object type")

    @staticmethod
    def quantity_to_string(quantity):
        """
        Helper function to convert a quantity identifier from the schema to a consistent
        string for in RST documentation

        :param quantity: Quantity string used in the format specification
        :return: String describing the quantity
        """
        qdict = {
            '*': '0 or more',
            'zero_or_more': '0 or more',
            '+': '1 or more',
            'one_or_more': '1 or more',
            '?': '0 or 1',
            'zero_or_one': '0 or 1'
        }
        if isinstance(quantity, int):
            return str(quantity)
        else:
            return qdict[quantity]

    @staticmethod
    def clean_schema_doc_string(doc_str, add_prefix=None, add_postfix=None, rst_format='**', remove_html_tags=True):
        """
        Given a doc string from a schema do basic cleaning operations to improve discplay in RST documents.
        Some of the operations performed are:
        *  Replace COMMENT, NOTE, MORE_INFO qualifiers
        *  Replace html tags from the original spec with corresponding  RST-style text so
           that it renders correctly in the Sphinx docs.

        :param doc_str: The documentation string to be processed
        :type doc_str: str
        :param add_prefix: Prefix string to be added before Comment, Note, etc. substrings.
                           Useful, e.g., to add newlines before the different sections of the doc string.
        :type add_prefix: str or None
        :param add_postfix: Postfix string to be added after Comment, Note, etc. substrings.
        :type add_postfix: str or None
        :param rst_format: RST formatting to be used for Comment, Note et.c headings. Default='**' for bold text.
        :type rst_format: str
        :param remove_html_tags: Boolean indicating whether the function should try to replace html tags with rst
                                 tags if possible
        :type remove_html_tags: bool

        :return: Cleaned doc RST string
        """
        prefix = ' ' if add_prefix is None else add_prefix
        clean_doc_str = doc_str
        if remove_html_tags:
            clean_doc_str = clean_doc_str.replace('&lt;', '<')
            clean_doc_str = clean_doc_str.replace('&gt;', '>')
            clean_doc_str = clean_doc_str.replace('<b>', ' **')
            clean_doc_str = clean_doc_str.replace('</b>', '** ')
            clean_doc_str = clean_doc_str.replace('<i>', ' *')
            clean_doc_str = clean_doc_str.replace('</i>', '* ')
            clean_doc_str = clean_doc_str.replace(':blue:', '')

        clean_doc_str = clean_doc_str.replace('COMMENT:', '%s%sComment:%s ' %
                                              (prefix, rst_format, rst_format))
        clean_doc_str = clean_doc_str.replace('MORE_INFO:', '%s%sAdditional Information:%s ' %
                                              (prefix, rst_format, rst_format))
        clean_doc_str = clean_doc_str.replace('NOTE:', '%s %sAdditional Information:%s ' %
                                              (prefix, rst_format, rst_format))
        if add_postfix is not None:
            clean_doc_str += add_postfix
        return clean_doc_str

    @staticmethod
    def render_inherits_from(spec_catalog, data_type, prefix=None, ignore_self=True):
        """
        Render an RST string with a list of all the types the data_type inherits from with links to
        the corresponding sections.
        :param spec_catalog: The SpecCatalog with all the types
        :type spec_catalog: hdmf.spec.catalog.SpecCatalog
        :param data_type: String with the name of the data type
        :param prefix: String with the RST prefix to be added to the list
        :param ignore_self: Bool indicating whether data_type should removed from the list.
        :type data_type: str

        :return: RST formatted strings with list of all the types the data_type inherits from.
                 None is returned in case no elements would be rendered to the list.
        """
        ancestry = spec_catalog.get_hierarchy(data_type)
        if len(ancestry) == 0 or (len(ancestry) == 1 and ignore_self):
            return None
        re = prefix if prefix is not None else ""
        start_index = 1 if ignore_self else 0
        re += ", ".join([RSTDocument.get_reference(RSTSectionLabelHelper.get_section_label(ct), ct)
                           for ct in ancestry[start_index:]])
        return re

    @staticmethod
    def render_subtypes(spec_catalog, data_type, prefix=None):
        """
        Render an RST string with a list of all the subtypes of the given data_type with links to
        the corresponding sections
        :param spec_catalog: The SpecCatalog with all the types
        :type spec_catalog: hdmf.spec.catalog.SpecCatalog
        :param data_type: String with the name of the data type
        :param prefix: String with the RST prefix to be added to the list
        :param ignore_self: Bool indicating whether data_type should removed from the list.
        :type data_type: str

        :return: RST formatted strings with list of all the subtypes of data_type.
                 None is returned in case no elements would be rendered to the list.
        """
        subtypes = spec_catalog.get_subtypes(data_type)
        if len(subtypes) == 0:
            return None
        re = prefix if prefix is not None else ""
        re += ", ".join([RSTDocument.get_reference(RSTSectionLabelHelper.get_section_label(ct), ct)
                           for ct in subtypes])
        return re

    @staticmethod
    def render_data_type(dtype):
        """
        Create a text representation of the data type

        :param dtype: data type object as returned by hdmf.spec.spec.DatasetSpec['dtype'].
        :type dtype: Either: 1) a list (in the case of compound types), 2) a dict in the case of reference types,
                     or 3) a string in the case of primitive types.
        :return: RST string describing the data type.
        """
        if isinstance(dtype, list):
            res = "Compound data type with the following elements: \n"
            for item in dtype:
                res += "    * **%s:** %s (*dtype=* %s ) \n" % (item['name'],
                                                               item['doc'],
                                                               SpecToRST.render_data_type(item['dtype']))
            res += "\n"
            return res
        elif isinstance(dtype, RefSpec):
            res = "%s reference to %s" % (dtype['reftype'],
                                          RSTDocument.get_reference(
                                              RSTSectionLabelHelper.get_section_label(dtype['target_type']),
                                              dtype['target_type']))
            return res
        else:
            return str(dtype)

    @staticmethod
    def render_namespace(namespace_catalog,
                         namespace_name=None,
                         desc_doc=None,
                         src_doc=None,
                         show_yaml_src=True,
                         file_dir=None,
                         file_per_type=False,
                         type_hierarchy_include_html=None,
                         type_hierarchy_include_latex=None,
                         print_status=True):
        """
        Render the description of a single namespace

        :param namespace_catalog: NamespaceCatalog object with the namespaces
        :type namespace_catalog: NamespaceCatalog
        :param namespace_name: Name of the namespace to be rendered. Set to None to use the default namespace.
        :type namespace_name: str or None
        :param desc_doc: RSTDocument where the description should be rendered.
                         Set to None to not render a description.
        :type desc_doc: RSTDocument
        :param src_doc: RSTDocument where the sources of the namespace should be rendered.
                        Set to None to not render the source.
        :type src_doc: RSTDocument
        :param show_yaml_src: Boolean indicating that we should render the YAML source in the src_doc
        :type show_yaml_src" bool
        :param file_dir: Directory where output RST docs should be stored. Required if file_per_type is True.
        :type file_dir: str or None
        :param file_per_type: Generate a separate rst files for each data_type and include them
                              in the src_doc and desc_doc (True). If set to False then write the
                              contents to src_doc and desc_doc directly.
        :type file_per_type: book
        :param type_hierarchy_include_html: Optional path to the RST file with the hierarchy of types in the namespace
                               to be included in the html docs.
        :type type_hierarchy_include: str or None
        :param type_hierarchy_include_latex: Optional path to the RST file with the hierarchy of types in the namespace
                               to be included in the html docs.
        :type type_hierarchy_include: str or None
        :param print_status: Bool indicating whether status messages should be printed to standard out
        :type print_status: bool

        """
        # Determine file settings
        if src_doc is None:
            seperate_src_file = False
            if show_yaml_src:
                src_doc = desc_doc
        else:
            seperate_src_file = True

        # Create target RST files if necessary
        ns_desc_doc = desc_doc if not file_per_type else RSTDocument()
        ns_src_doc = src_doc if not file_per_type else RSTDocument()
        ns_desc_label = "hdmf-type-namespace-doc"
        ns_src_label = "hdmf-type-namespace-src"
        # Create the target doc
        if namespace_name is None:
            namespace_name = namespace_catalog.default_namespace
        curr_namespace = namespace_catalog.get_namespace(namespace_name)
        # Section heading

        subsec_heading = "Namespace -- %s" % curr_namespace['full_name'] \
            if 'full_name' in curr_namespace \
            else curr_namespace['name']
        # Render the description of the namespace
        if desc_doc:
            # Add section heading
            ns_desc_doc.add_section("Format Overview")
            # Add a subsection for the Namespace
            ns_desc_doc.add_label(ns_desc_label)
            ns_desc_doc.add_subsection(subsec_heading)
            # Add a link to the source specification
            if seperate_src_file:
                ns_src_doc.add_text('**Source Specification:** see %s %s %s' %
                                    (ns_src_doc.get_numbered_reference(ns_src_label),
                                     ns_src_doc.newline,
                                     ns_src_doc.newline))
            # Create a list with further details about the namespace, e.g., name, version, authors etc.
            desc_list = []
            if 'doc' in curr_namespace:
                desc_list.append('**Description:** %s' % str(curr_namespace['doc']))
            if 'name' in curr_namespace:
                desc_list.append('**Name:** %s' % str(curr_namespace['name']))
            if 'full_name' in curr_namespace:
                desc_list.append('**Full Name:** %s' % str(curr_namespace['full_name']))
            if 'version' in curr_namespace:
                desc_list.append('**Version:** %s' % str(curr_namespace['version']))
            if 'date' in curr_namespace:
                desc_list.append('**Date:** %s' % str(curr_namespace['date']))
            if 'author' in curr_namespace:
                if isinstance(curr_namespace['author'], list):
                    desc_list.append('**Authors:**')
                    desc_list.append(curr_namespace['author'])
                else:
                    desc_list.append('**Author:** %s' % str(curr_namespace['author']))
            if 'contact' in curr_namespace:
                if isinstance(curr_namespace['contact'], list):
                    desc_list.append('**Contacts:**')
                    desc_list.append(curr_namespace['contact'])
                else:
                    desc_list.append('**Contact:** %s' % str(curr_namespace['contact']))
            if 'schema' in curr_namespace:
                desc_list.append('**Schema:**')
                schema_list = []
                for s in curr_namespace['schema']:
                    if isinstance(s, dict):
                        for k, v in s.items():
                            schema_list.append('**%s:** %s ' % (str(k), str(v)))
                    else:
                        schema_list.append(s)
                desc_list.append(schema_list)
            # Render the list with the descripiton of the namespace
            if len(desc_list) > 0:
                ns_desc_doc.add_list(desc_list,
                                     item_symbol='-'
                                     )
        # Include the type hierarchy document if requested
        if type_hierarchy_include_html is not None or type_hierarchy_include_latex is not None:
            # If latex and html are the same then just do one general include
            if type_hierarchy_include_html == type_hierarchy_include_latex:
                ns_desc_doc.add_include(type_hierarchy_include_html)
            # If latex and html are different
            else:
                # Do a HTML specific include if necessary
                if type_hierarchy_include_html is not None:
                    ns_desc_doc.add_text('.. only:: html %s%s' % (ns_desc_doc.newline, ns_desc_doc.newline))
                    ns_desc_doc.add_include(type_hierarchy_include_html, indent='    ')
                    ns_desc_doc.add_text(ns_desc_doc.newline)
                # Do a LaTeX specific include if necessary
                if type_hierarchy_include_latex is not None:
                    ns_desc_doc.add_text('.. only:: latex %s%s' % (ns_desc_doc.newline, ns_desc_doc.newline))
                    ns_desc_doc.add_include(type_hierarchy_include_html, indent='    ')
                    ns_desc_doc.add_text(ns_desc_doc.newline)

        if src_doc:
            if seperate_src_file:
                ns_src_doc.add_label(ns_src_label)
                ns_src_doc.add_subsection(subsec_heading)
                ns_src_doc.add_text('**Description:** see ' +
                                    ns_src_doc.get_numbered_reference(ns_desc_label) +
                                    ns_src_doc.newline +
                                    ns_src_doc.newline)
            if show_yaml_src:
                ns_src_doc.add_text('**YAML Specification:**' + ns_src_doc.newline + ns_src_doc.newline)
                ns_src_doc.add_spec(curr_namespace)

        # Save the output files if necessary
        if file_per_type and file_dir is not None:
            # Write the files for the source and description
            ns_src_filename = os.path.join(file_dir, '%s_namespace_source.inc' % namespace_name)
            ns_desc_filename = os.path.join(file_dir, '%s_namespace_description.inc' % namespace_name)
            if desc_doc:
                ns_desc_doc.write(ns_desc_filename, 'w')
                if print_status:
                    PrintHelper.print("    " + namespace_name + '-- WRITE NAMESPACE DESCRIPTION DOC OK.',
                                      PrintHelper.OKGREEN)
                # Include the files in the main documents
                desc_doc.add_include(os.path.basename(file_dir) + "/" + os.path.basename(ns_desc_filename))
            if src_doc:
                ns_src_doc.write(ns_src_filename, 'w')
                if print_status:
                    PrintHelper.print("    " + namespace_name + '-- WRITE NAMESPACE SOURCE DOC OK.',
                                      PrintHelper.OKGREEN)
                # Include the files in the main documents
                src_doc.add_include(os.path.basename(file_dir) + "/" + os.path.basename(ns_src_filename))

    @staticmethod
    def render_type_hierarchy(spec_catalog,
                              target_doc=None,
                              section_label='data_type_hierarchy',
                              subsection_title='Type Hierarchy'):
        """
        Render the flattened type hierarchy to an RSTDocument

        :param spec_catalog: The spec catalog with all the types we should render the hierarchy for
        :type spec_catalog: hdmf.spec.catalog.SpecCatalog
        :param target_doc: Target RST document where the type hierarchy should be rendered to or None if a new document
                           should be created.
        :type target_doc: RSTDocument or Non
        :param section_label: String with the label for the section (or None if no label should be added)
        :param subsection_title: String with the title for the section (or None if no section should be added)

        :returns: Tuple with: 1) RSTDocument with the type hierarchy,
                  2) OrderedDict with the type hierarchy itself as generated by SpecCatalog.get_full_hierarchy()
        """
        # Compute the type hierarchy
        type_hierarchy = spec_catalog.get_full_hierarchy()

        # Crate the target document
        target_doc = RSTDocument() if target_doc is None else target_doc
        if section_label:
            target_doc.add_label(section_label)
        if subsection_title:
            target_doc.add_subsection(subsection_title)

        def add_sub_hierarchy(outdoc, type_hierarchy, depth=0, indent_step='   '):
            """
            Helper function used to print a hierarchy of data_types
            :param type_hierarchy: Hierarchical OrderedDict containing for each type a an OrderedDict with its substypes
            :param depth: Recursion depth of the print used to indent the hierarchy
            """
            for k, v in type_hierarchy.items():
                type_list_item = indent_step*depth + '* '
                type_list_item += outdoc.get_reference(RSTSectionLabelHelper.get_section_label(k), k)
                type_list_item += outdoc.newline
                outdoc.add_text(type_list_item)
                if len(v) > 0:
                    outdoc.add_text(outdoc.newline)
                    add_sub_hierarchy(outdoc=outdoc,
                                      type_hierarchy=v,
                                      depth=depth+1,
                                      indent_step=indent_step)

        # Render the hierarchy
        add_sub_hierarchy(outdoc=target_doc,
                          type_hierarchy=type_hierarchy)
        target_doc.add_text(target_doc.newline + target_doc.newline)

        # return the document and type hierarchy
        return target_doc, type_hierarchy

    @staticmethod
    def render_specification_properties(spec, newline='\n', ignore_props=None, prepend_items=None, append_items=None):
        """
        Create RST document string with and RST list of the properties from the spec

        :param spec: The GroupSpec, DatasetSpec, AttributeSpec, or LinkSpec object
        :type: GroupSepc, DatasetSpec, AttributeSpec, LinkSpec
        :param newline: String to be used for newline
        :param ignore_props: List of strings of property keys we should ignore
        :param prepend_items: List of strings with additional items to be added to the beginning of the properties list
        :param append_items: List of strings with additional items to be added to the end of the properties list
        :return: String with the rendered list of properties of the specification
        """

        spec_prop_list = []
        if prepend_items is not None:
            spec_prop_list += prepend_items
        ignore_keys = [] if ignore_props is None else ignore_props
        # Add link properties
        if isinstance(spec, LinkSpec):
            spec_prop_list.append('**Target Type** %s' %
                                  RSTDocument.get_reference(RSTSectionLabelHelper.get_section_label(
                                      spec['target_type']),
                                      spec['target_type']))
        # Add dataset properties
        if isinstance(spec, DatasetSpec):
            if spec.data_type_def is not None and spec.def_key() not in ignore_keys:
                spec_prop_list.append('**Neurodata Type:** %s' % str(spec.data_type_def))
            if spec.data_type_inc is not None and spec.inc_key() not in ignore_keys:
                extend_type = str(spec.data_type_inc)
                spec_prop_list.append('**Extends:** %s' %
                                      RSTDocument.get_reference(
                                          RSTSectionLabelHelper.get_section_label(extend_type),
                                          extend_type))
            if 'primitive_type' not in ignore_keys:
                spec_prop_list.append('**Primitive Type:** %s' % SpecToRST.spec_basetype_name(spec))
            if spec.get('quantity', None) is not None and 'quantity' not in ignore_keys:
                spec_prop_list.append('**Quantity:** %s' % SpecToRST.quantity_to_string(spec['quantity']))
            if spec.get('dtype', None) is not None and 'dtype' not in ignore_keys:
                spec_prop_list.append('**Data Type:** %s' % SpecToRST.render_data_type(spec['dtype']))
            if spec.get('dims', None) is not None and 'dims' not in ignore_keys:
                spec_prop_list.append('**Dimensions:** %s' % str(spec['dims']))
            if spec.get('shape', None) is not None and 'shape' not in ignore_keys:
                spec_prop_list.append('**Shape:** %s' % str(spec['shape']))
            if spec.get('linkable', None) is not None and 'linnkable' not in ignore_keys:
                spec_prop_list.append('**Linkable:** %s' % str(spec['linkable']))
        # Add group properties
        if isinstance(spec, GroupSpec):
            if spec.data_type_def is not None and spec.def_key() not in ignore_keys:
                ntype = str(spec.data_type_def)
                spec_prop_list.append('**Neurodata Type:** %s' %
                                      RSTDocument.get_reference(
                                          RSTSectionLabelHelper.get_section_label(ntype),
                                          ntype))
            if spec.data_type_inc is not None and spec.inc_key() not in ignore_keys:
                extend_type = str(spec.data_type_inc)
                spec_prop_list.append('**Extends:** %s' %
                                      RSTDocument.get_reference(
                                          RSTSectionLabelHelper.get_section_label(extend_type),
                                          extend_type))
            if 'primitive_type' not in ignore_keys:
                spec_prop_list.append('**Primitive Type:** %s' % SpecToRST.spec_basetype_name(spec))
            if spec.get('quantity', None) is not None and 'quantity' not in ignore_keys:
                spec_prop_list.append('**Quantity:** %s' % SpecToRST.quantity_to_string(spec['quantity']))
            if spec.get('linkable', None) is not None and 'linkable' not in ignore_keys:
                spec_prop_list.append('**Linkable:** %s' % str(spec['linkable']))
        # Add attribute spec properties
        if isinstance(spec, AttributeSpec):
            if 'primitive_type' not in ignore_keys:
                spec_prop_list.append('**Primitive Type:** %s' % SpecToRST.spec_basetype_name(spec))
            if spec.get('dtype', None) is not None and 'dtype' not in ignore_keys:
                spec_prop_list.append('**Data Type:** %s' % SpecToRST.render_data_type(spec['dtype']))
            if spec.get('dims', None) is not None and 'dims' not in ignore_keys:
                spec_prop_list.append('**Dimensions:** %s' % str(spec['dims']))
            if spec.get('shape', None) is not None and 'shape' not in ignore_keys:
                spec_prop_list.append('**Shape:** %s' % str(spec['shape']))
            if spec.get('required', None) is not None and 'required' not in ignore_keys:
                spec_prop_list.append('**Required:** %s' % str(spec['required']))
            if spec.get('value', None) is not None and 'value' not in ignore_keys:
                spec_prop_list.append('**Value:** %s' % str(spec['value']))
            if spec.get('default_value', None) is not None and 'default_value' not in ignore_keys:
                spec_prop_list.append('**Default Value:** %s' % str(spec['default_value']))

        # Add common properties
        if spec.get('default_name', None) is not None:
                spec_prop_list.append('**Default Name:** %s' % str(spec['default_name']))
        if spec.get('name', None) is not None:
            spec_prop_list.append('**Name:** %s' % str(spec['name']))

        # Add custom items if necessary
        if append_items is not None:
            spec_prop_list += append_items

        # Render the specification properties list
        spec_doc = ''
        if len(spec_prop_list) > 0:
            spec_doc += newline
            for dp in spec_prop_list:
                spec_doc += newline + '- ' + dp
            spec_doc += newline
        # Return the rendered list
        return spec_doc

    @staticmethod
    def render_spec_table(spec,
                          rst_table=None,
                          depth_char=".",
                          depth=0,
                          show_subattributes=True,
                          show_subdatasets=True,
                          show_sublinks=True,
                          show_subgroups=False,
                          recursive_subgroups=False,
                          appreviate_main_object_doc=True):
        """
        Create an RSTTable with an overview of the specification for the given spec

        :param spec: The specification to be rendered
        :type spec: GroupSpec, DatasetSpec, LinkSpec, AttributeSpec
        :param rst_table: The RSTTable to be expanded. This argument is used internally to recursively fill the
                          table and will usually be left as None when called externally.
        :param depth_char: String used to indicate the depth in the hierarchy as part of the table. Default is '.'
        :param depth: The depth at which the current spec should appear in the table. This argument is used to
                      recursively fill the table and will typically left as 0 when called externally.
        :param show_subattributes: Boolean indicating whether the subattributes of the given DatasetSpec of
                                   GroupSpec should be rendered recursively in the table.
        :param show_subdatasets: Boolean indicating whether the subdatasets of the given GroupSpec should
                                 be listed recursively in the table.
        :param show_sublinks: Boolean indicating whether the sublinks of the given GroupSpec should
                              be listed recursively in the table.
        :param show_subgroups: Boolean indicating whether to recursively include subgroups (default=False)
        :param recursive_subgroups: Boolean indicating for show_subgroups whether we should recurse or not.

        :return: RSTTable that can be rendered into and RSTDocuement via the RSTTable.render(...) function.
        """
        # Create a new table if necessary
        rst_table = rst_table if rst_table is not None else RSTTable(cols=['Id', 'Type', 'Description'])

        ###########################################
        #  Render the row for the current object
        ###########################################
        # Determine the type of the object
        spec_type = SpecToRST.spec_basetype_name(spec)

        # Determine the name of the object
        depth_str = depth_char * depth
        spec_name = depth_str
        if spec.get('name', None) is not None:
            spec_name += spec.name
        elif isinstance(spec, LinkSpec):
            spec_name += '<%s>' % RSTDocument.get_reference(
                RSTSectionLabelHelper.get_section_label(spec.target_type),
                spec.target_type)
        elif spec.data_type_def is not None:
            spec_name += '<%s>' % spec.data_type_def
        elif spec.data_type_inc is not None:
            spec_name += '<%s>' % RSTDocument.get_reference(
                RSTSectionLabelHelper.get_section_label(spec.data_type_inc),
                spec.data_type_inc)
        else:
            spec_type_key = spec.type_key()
            spec_name += '<%s>' % RSTDocument.get_reference(
                RSTSectionLabelHelper.get_section_label(spec[spec_type_key]),
                spec[spec_type_key])

        # Create the doc description of the spec
        if appreviate_main_object_doc and depth == 0:
            # Create the appreviated description of the main object
            spec_doc = "Top level %s for %s" % (spec_type, spec_name.lstrip(depth_str))
            spec_doc += SpecToRST.render_specification_properties(spec=spec,
                                                                  newline=rst_table.newline,
                                                                  ignore_props=['primitive_type'])
        else:
            # Create the description for the object
            spec_doc = SpecToRST.clean_schema_doc_string(doc_str=spec.doc,
                                                         add_prefix=rst_table.newline + rst_table.newline)
            # Create the list of additional object properties to be added as a list to the doc
            spec_doc += SpecToRST.render_specification_properties(spec=spec,
                                                                  newline=rst_table.newline,
                                                                  ignore_props=['primitive_type'])

        # Render the object to the table
        rst_table.add_row(row_values=[spec_name, spec_type, spec_doc],
                          replace_none='',
                          convert_to_str=True)

        ################################################
        #  Recursively add the subobjects if requested
        ################################################
        # Recursively add all attributes of the current spec
        if (isinstance(spec, DatasetSpec) or isinstance(spec, GroupSpec)) and show_subattributes:
            for a in spec.attributes:
                SpecToRST.render_spec_table(spec=a,
                                            rst_table=rst_table,
                                            depth_char=depth_char,
                                            depth=depth + 1)
        # Recursively add all Datasets of the current spec
        if isinstance(spec, GroupSpec) and show_subdatasets:
            for d in spec.datasets:
                SpecToRST.render_spec_table(spec=d,
                                            rst_table=rst_table,
                                            depth_char=depth_char,
                                            depth=depth + 1)
        # Recursively add all Links for the current spec
        if isinstance(spec, GroupSpec) and show_sublinks:
            for link in spec.links:
                SpecToRST.render_spec_table(spec=link,
                                            rst_table=rst_table,
                                            depth_char=depth_char,
                                            depth=depth + 1)
        # Recursively add all subgroups if requested
        if show_subgroups and isinstance(spec, GroupSpec):
            if recursive_subgroups:
                for g in spec.groups:
                    SpecToRST.render_spec_table(spec=g,
                                                rst_table=rst_table,
                                                depth_char=depth_char,
                                                depth=depth+1,
                                                show_subgroups=show_subgroups,
                                                show_subdatasets=show_subdatasets,
                                                show_subattributes=show_subattributes)
            else:
                for g in spec.groups:
                    SpecToRST.render_spec_table(spec=g,
                                                rst_table=rst_table,
                                                depth_char=depth_char,
                                                depth=depth+1,
                                                recursive_subgroups=recursive_subgroups,
                                                show_subgroups=False,
                                                show_subattributes=False,
                                                show_subdatasets=False)
        # Return the created table
        return rst_table

    @staticmethod
    def render_group_spec(group_spec,
                          depth_char='.',
                          show_table_titles=True,
                          appreviate_main_object_doc=True,
                          show_subgroups_in_seperate_table=True,
                          sectype='par',
                          rst_doc=None,
                          parent=None,):
        """
        Render the specification of a group to the RST document
        :param group_spec: GroupSpec with the spec of the group
        :type group_spec: GroupSpec
        :param depth_char: String used to indicate the depth in the hierarchy as part of the table. Default is '.'
        :param show_table_titles: Bool indicating whether table titles should be rendered
        :param appreviate_main_object_doc:  Abbreviate the documentation of the main object for which a table
                        is rendered in the table. This is commonly set to True as doc of the main object is already
                        rendered as the main intro for the section describing the object
        :param show_subgroups_in_seperate_table: Should top-level subgroups be listed in a separate table or as part
                        of the main dataset and attributes table
        :param sectype: The kind of section to be used for rendering the group spec. Allowable values are
                        'par' for paragraph, 'sec' for section, 'chp' for chapter, 'subsec' for subsection,
                        'subsubsec' for subsubsection, 'prt' for part. Default is 'par' for paragraph.
        :param rst_doc: RSTDocument to render the group spec to or None in case a new RSTDocument should be created
        :param parent: Internal argument used to recursively render subgroups of this group
        :raises ValueError: if the name of the group cannot be determined. For a valid spec this should not happen.

        :return: RSTDocument
        """

        rst_doc = rst_doc if rst_doc is not None else RSTDocument()
        parent = parent if parent is not None else ''

        # Determine the name of the group
        group_name = None
        if group_spec.get('name', None) is not None:
            group_name = group_spec.name
        elif group_spec.data_type_def is not None:
            group_name = "<%s>" % group_spec.data_type_def
        elif group_spec.data_type_inc is not None:
            group_name = "<%s>" % group_spec.data_type_inc
        if group_name is None:
            raise ValueError("Could not determine name for group %s" % str(group_spec))

        # Add paragraph for the group
        title = "Groups: %s%s" % (parent, group_name)
        if sectype == 'par':
            rst_doc.add_paragraph(title)
        elif sectype == 'sec':
            rst_doc.add_section(title)
        elif sectype == 'chp':
            rst_doc.add_chapter(title)
        elif sectype == 'subsec':
            rst_doc.add_subsection(title)
        elif sectype == 'subsubsec':
            rst_doc.add_subsubsection(title)
        elif sectype == 'prt':
            rst_doc.add_part(title)

        # Compile the documentation for the group and add it to the RST document
        gdoc = SpecToRST.clean_schema_doc_string(group_spec.doc,
                                                 add_prefix=rst_doc.newline+rst_doc.newline,
                                                 add_postfix=rst_doc.newline,
                                                 rst_format='**')
        gdoc += rst_doc.newline
        gdoc += SpecToRST.render_specification_properties(group_spec, rst_doc.newline, ignore_props=['primitive_type'])
        gdoc += rst_doc.newline
        rst_doc.add_text(gdoc)

        # Create the table with the dataset and attributes specifications for the group
        group_spec_data_table = SpecToRST.render_spec_table(
            spec=group_spec,
            depth_char=depth_char,
            show_subgroups=not show_subgroups_in_seperate_table,
            appreviate_main_object_doc=appreviate_main_object_doc)  # table_class='longtable', widths=[15, 15, 60 ,10])
        # Add the table for the group spec only if there is more than one entry, i.e.,  only if there is additional
        # information in the table about the content of the group, rather than just only the group itself in the table
        if group_spec_data_table.num_rows() > 1:
            group_spec_data_table_title = None
            if show_table_titles:
                if not show_subgroups_in_seperate_table:
                    group_spec_data_table_title = "Groups, Datasets, and Attributes contained in ``%s%s``" % \
                                                  (parent, group_name)
                else:
                    group_spec_data_table_title = "Datasets, Links, and Attributes contained in ``%s%s``" % \
                                                  (parent, group_name)
            rst_doc.add_table(rst_table=group_spec_data_table,
                              title=group_spec_data_table_title,
                              latex_tablecolumns=SpecToRST.CUSTOM_LATEX_TABLE_COLUMNS)

        # Add a table with all the subgroups of this group
        if show_subgroups_in_seperate_table:
            group_spec_groups_table = SpecToRST.render_spec_table(
                spec=group_spec,
                depth_char=depth_char,
                show_subattributes=False,
                show_subdatasets=False,
                show_subgroups=True,
                recursive_subgroups=False,
                appreviate_main_object_doc=appreviate_main_object_doc)
            # Only show the subgroups if it contains additional information
            if group_spec_groups_table.num_rows() > 1:
                group_spec_groups_table_title = None
                if show_table_titles:
                    group_spec_groups_table_title = "Groups contained in <%s>" % group_name
                rst_doc.add_table(group_spec_groups_table,
                                  title=group_spec_groups_table_title,
                                  latex_tablecolumns=SpecToRST.CUSTOM_LATEX_TABLE_COLUMNS)

        # Recursively render paragraphs for all the subgroups of this group
        for sg in group_spec.groups:
            SpecToRST.render_group_spec(group_spec=sg,
                                        depth_char=depth_char,
                                        show_table_titles=show_table_titles,
                                        appreviate_main_object_doc=appreviate_main_object_doc,
                                        show_subgroups_in_seperate_table=show_subgroups_in_seperate_table,
                                        rst_doc=rst_doc,
                                        parent=parent + group_name + '/')
        # Return the rst doc
        return rst_doc
