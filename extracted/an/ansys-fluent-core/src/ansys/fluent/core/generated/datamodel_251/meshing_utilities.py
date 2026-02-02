#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand,
    PyQuery,
    PyArguments,
    PyArgumentsTextualSubItem,
    PyArgumentsNumericalSubItem,
    PyArgumentsDictionarySubItem,
    PyArgumentsParameterSubItem,
    PyArgumentsSingletonSubItem
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.add_labels_on_cell_zones = self.__class__.add_labels_on_cell_zones(service, rules, "add_labels_on_cell_zones", path)
        self.add_labels_on_edge_zones = self.__class__.add_labels_on_edge_zones(service, rules, "add_labels_on_edge_zones", path)
        self.add_labels_on_face_zones = self.__class__.add_labels_on_face_zones(service, rules, "add_labels_on_face_zones", path)
        self.clean_face_zone_names = self.__class__.clean_face_zone_names(service, rules, "clean_face_zone_names", path)
        self.delete_all_sub_domains = self.__class__.delete_all_sub_domains(service, rules, "delete_all_sub_domains", path)
        self.delete_empty_cell_zones = self.__class__.delete_empty_cell_zones(service, rules, "delete_empty_cell_zones", path)
        self.delete_empty_edge_zones = self.__class__.delete_empty_edge_zones(service, rules, "delete_empty_edge_zones", path)
        self.delete_empty_face_zones = self.__class__.delete_empty_face_zones(service, rules, "delete_empty_face_zones", path)
        self.delete_empty_zones = self.__class__.delete_empty_zones(service, rules, "delete_empty_zones", path)
        self.delete_marked_faces_in_zones = self.__class__.delete_marked_faces_in_zones(service, rules, "delete_marked_faces_in_zones", path)
        self.merge_cell_zones = self.__class__.merge_cell_zones(service, rules, "merge_cell_zones", path)
        self.merge_cell_zones_with_same_prefix = self.__class__.merge_cell_zones_with_same_prefix(service, rules, "merge_cell_zones_with_same_prefix", path)
        self.merge_cell_zones_with_same_suffix = self.__class__.merge_cell_zones_with_same_suffix(service, rules, "merge_cell_zones_with_same_suffix", path)
        self.merge_face_zones = self.__class__.merge_face_zones(service, rules, "merge_face_zones", path)
        self.merge_face_zones_of_type = self.__class__.merge_face_zones_of_type(service, rules, "merge_face_zones_of_type", path)
        self.merge_face_zones_with_same_prefix = self.__class__.merge_face_zones_with_same_prefix(service, rules, "merge_face_zones_with_same_prefix", path)
        self.remove_id_suffix_from_face_zones = self.__class__.remove_id_suffix_from_face_zones(service, rules, "remove_id_suffix_from_face_zones", path)
        self.remove_ids_from_zone_names = self.__class__.remove_ids_from_zone_names(service, rules, "remove_ids_from_zone_names", path)
        self.remove_labels_on_cell_zones = self.__class__.remove_labels_on_cell_zones(service, rules, "remove_labels_on_cell_zones", path)
        self.remove_labels_on_edge_zones = self.__class__.remove_labels_on_edge_zones(service, rules, "remove_labels_on_edge_zones", path)
        self.remove_labels_on_face_zones = self.__class__.remove_labels_on_face_zones(service, rules, "remove_labels_on_face_zones", path)
        self.rename_edge_zone = self.__class__.rename_edge_zone(service, rules, "rename_edge_zone", path)
        self.rename_face_zone = self.__class__.rename_face_zone(service, rules, "rename_face_zone", path)
        self.rename_face_zone_label = self.__class__.rename_face_zone_label(service, rules, "rename_face_zone_label", path)
        self.rename_object = self.__class__.rename_object(service, rules, "rename_object", path)
        self.renumber_zone_ids = self.__class__.renumber_zone_ids(service, rules, "renumber_zone_ids", path)
        self.replace_cell_zone_suffix = self.__class__.replace_cell_zone_suffix(service, rules, "replace_cell_zone_suffix", path)
        self.replace_edge_zone_suffix = self.__class__.replace_edge_zone_suffix(service, rules, "replace_edge_zone_suffix", path)
        self.replace_face_zone_suffix = self.__class__.replace_face_zone_suffix(service, rules, "replace_face_zone_suffix", path)
        self.replace_label_suffix = self.__class__.replace_label_suffix(service, rules, "replace_label_suffix", path)
        self.replace_object_suffix = self.__class__.replace_object_suffix(service, rules, "replace_object_suffix", path)
        self.set_number_of_parallel_compute_threads = self.__class__.set_number_of_parallel_compute_threads(service, rules, "set_number_of_parallel_compute_threads", path)
        self.set_object_cell_zone_type = self.__class__.set_object_cell_zone_type(service, rules, "set_object_cell_zone_type", path)
        self.set_quality_measure = self.__class__.set_quality_measure(service, rules, "set_quality_measure", path)
        self._cell_zones_labels_fdl = self.__class__._cell_zones_labels_fdl(service, rules, "_cell_zones_labels_fdl", path)
        self._cell_zones_str_fdl = self.__class__._cell_zones_str_fdl(service, rules, "_cell_zones_str_fdl", path)
        self._edge_zones_labels_fdl = self.__class__._edge_zones_labels_fdl(service, rules, "_edge_zones_labels_fdl", path)
        self._edge_zones_str_fdl = self.__class__._edge_zones_str_fdl(service, rules, "_edge_zones_str_fdl", path)
        self._face_zones_labels_fdl = self.__class__._face_zones_labels_fdl(service, rules, "_face_zones_labels_fdl", path)
        self._face_zones_str_fdl = self.__class__._face_zones_str_fdl(service, rules, "_face_zones_str_fdl", path)
        self._node_zones_labels_fdl = self.__class__._node_zones_labels_fdl(service, rules, "_node_zones_labels_fdl", path)
        self._node_zones_str_fdl = self.__class__._node_zones_str_fdl(service, rules, "_node_zones_str_fdl", path)
        self._object_names_str_fdl = self.__class__._object_names_str_fdl(service, rules, "_object_names_str_fdl", path)
        self._prism_cell_zones_labels_fdl = self.__class__._prism_cell_zones_labels_fdl(service, rules, "_prism_cell_zones_labels_fdl", path)
        self._prism_cell_zones_str_fdl = self.__class__._prism_cell_zones_str_fdl(service, rules, "_prism_cell_zones_str_fdl", path)
        self._regions_str_fdl = self.__class__._regions_str_fdl(service, rules, "_regions_str_fdl", path)
        self._zone_types_fdl = self.__class__._zone_types_fdl(service, rules, "_zone_types_fdl", path)
        self.boundary_zone_exists = self.__class__.boundary_zone_exists(service, rules, "boundary_zone_exists", path)
        self.cell_zone_exists = self.__class__.cell_zone_exists(service, rules, "cell_zone_exists", path)
        self.convert_zone_ids_to_name_strings = self.__class__.convert_zone_ids_to_name_strings(service, rules, "convert_zone_ids_to_name_strings", path)
        self.convert_zone_name_strings_to_ids = self.__class__.convert_zone_name_strings_to_ids(service, rules, "convert_zone_name_strings_to_ids", path)
        self.copy_face_zone_labels = self.__class__.copy_face_zone_labels(service, rules, "copy_face_zone_labels", path)
        self.count_marked_faces = self.__class__.count_marked_faces(service, rules, "count_marked_faces", path)
        self.create_boi_and_size_functions_from_refinement_regions = self.__class__.create_boi_and_size_functions_from_refinement_regions(service, rules, "create_boi_and_size_functions_from_refinement_regions", path)
        self.dump_face_zone_orientation_in_region = self.__class__.dump_face_zone_orientation_in_region(service, rules, "dump_face_zone_orientation_in_region", path)
        self.fill_holes_in_face_zone_list = self.__class__.fill_holes_in_face_zone_list(service, rules, "fill_holes_in_face_zone_list", path)
        self.get_adjacent_cell_zones_for_given_face_zones = self.__class__.get_adjacent_cell_zones_for_given_face_zones(service, rules, "get_adjacent_cell_zones_for_given_face_zones", path)
        self.get_adjacent_face_zones_for_given_cell_zones = self.__class__.get_adjacent_face_zones_for_given_cell_zones(service, rules, "get_adjacent_face_zones_for_given_cell_zones", path)
        self.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones = self.__class__.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(service, rules, "get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones", path)
        self.get_adjacent_zones_by_edge_connectivity = self.__class__.get_adjacent_zones_by_edge_connectivity(service, rules, "get_adjacent_zones_by_edge_connectivity", path)
        self.get_adjacent_zones_by_node_connectivity = self.__class__.get_adjacent_zones_by_node_connectivity(service, rules, "get_adjacent_zones_by_node_connectivity", path)
        self.get_all_objects = self.__class__.get_all_objects(service, rules, "get_all_objects", path)
        self.get_average_bounding_box_center = self.__class__.get_average_bounding_box_center(service, rules, "get_average_bounding_box_center", path)
        self.get_baffles_for_face_zones = self.__class__.get_baffles_for_face_zones(service, rules, "get_baffles_for_face_zones", path)
        self.get_bounding_box_of_zone_list = self.__class__.get_bounding_box_of_zone_list(service, rules, "get_bounding_box_of_zone_list", path)
        self.get_cell_mesh_distribution = self.__class__.get_cell_mesh_distribution(service, rules, "get_cell_mesh_distribution", path)
        self.get_cell_quality_limits = self.__class__.get_cell_quality_limits(service, rules, "get_cell_quality_limits", path)
        self.get_cell_zone_count = self.__class__.get_cell_zone_count(service, rules, "get_cell_zone_count", path)
        self.get_cell_zone_id_list_with_labels = self.__class__.get_cell_zone_id_list_with_labels(service, rules, "get_cell_zone_id_list_with_labels", path)
        self.get_cell_zone_shape = self.__class__.get_cell_zone_shape(service, rules, "get_cell_zone_shape", path)
        self.get_cell_zone_volume = self.__class__.get_cell_zone_volume(service, rules, "get_cell_zone_volume", path)
        self.get_cell_zones = self.__class__.get_cell_zones(service, rules, "get_cell_zones", path)
        self.get_edge_size_limits = self.__class__.get_edge_size_limits(service, rules, "get_edge_size_limits", path)
        self.get_edge_zone_id_list_with_labels = self.__class__.get_edge_zone_id_list_with_labels(service, rules, "get_edge_zone_id_list_with_labels", path)
        self.get_edge_zones = self.__class__.get_edge_zones(service, rules, "get_edge_zones", path)
        self.get_edge_zones_list = self.__class__.get_edge_zones_list(service, rules, "get_edge_zones_list", path)
        self.get_edge_zones_of_object = self.__class__.get_edge_zones_of_object(service, rules, "get_edge_zones_of_object", path)
        self.get_embedded_baffles = self.__class__.get_embedded_baffles(service, rules, "get_embedded_baffles", path)
        self.get_face_mesh_distribution = self.__class__.get_face_mesh_distribution(service, rules, "get_face_mesh_distribution", path)
        self.get_face_quality_limits = self.__class__.get_face_quality_limits(service, rules, "get_face_quality_limits", path)
        self.get_face_zone_area = self.__class__.get_face_zone_area(service, rules, "get_face_zone_area", path)
        self.get_face_zone_count = self.__class__.get_face_zone_count(service, rules, "get_face_zone_count", path)
        self.get_face_zone_id_list_with_labels = self.__class__.get_face_zone_id_list_with_labels(service, rules, "get_face_zone_id_list_with_labels", path)
        self.get_face_zone_node_count = self.__class__.get_face_zone_node_count(service, rules, "get_face_zone_node_count", path)
        self.get_face_zones = self.__class__.get_face_zones(service, rules, "get_face_zones", path)
        self.get_face_zones_by_zone_area = self.__class__.get_face_zones_by_zone_area(service, rules, "get_face_zones_by_zone_area", path)
        self.get_face_zones_of_object = self.__class__.get_face_zones_of_object(service, rules, "get_face_zones_of_object", path)
        self.get_face_zones_with_zone_specific_prisms_applied = self.__class__.get_face_zones_with_zone_specific_prisms_applied(service, rules, "get_face_zones_with_zone_specific_prisms_applied", path)
        self.get_free_faces_count = self.__class__.get_free_faces_count(service, rules, "get_free_faces_count", path)
        self.get_interior_face_zones_for_given_cell_zones = self.__class__.get_interior_face_zones_for_given_cell_zones(service, rules, "get_interior_face_zones_for_given_cell_zones", path)
        self.get_labels = self.__class__.get_labels(service, rules, "get_labels", path)
        self.get_labels_on_cell_zones = self.__class__.get_labels_on_cell_zones(service, rules, "get_labels_on_cell_zones", path)
        self.get_labels_on_edge_zones = self.__class__.get_labels_on_edge_zones(service, rules, "get_labels_on_edge_zones", path)
        self.get_labels_on_face_zones = self.__class__.get_labels_on_face_zones(service, rules, "get_labels_on_face_zones", path)
        self.get_labels_on_face_zones_list = self.__class__.get_labels_on_face_zones_list(service, rules, "get_labels_on_face_zones_list", path)
        self.get_maxsize_cell_zone_by_count = self.__class__.get_maxsize_cell_zone_by_count(service, rules, "get_maxsize_cell_zone_by_count", path)
        self.get_maxsize_cell_zone_by_volume = self.__class__.get_maxsize_cell_zone_by_volume(service, rules, "get_maxsize_cell_zone_by_volume", path)
        self.get_minsize_face_zone_by_area = self.__class__.get_minsize_face_zone_by_area(service, rules, "get_minsize_face_zone_by_area", path)
        self.get_minsize_face_zone_by_count = self.__class__.get_minsize_face_zone_by_count(service, rules, "get_minsize_face_zone_by_count", path)
        self.get_multi_faces_count = self.__class__.get_multi_faces_count(service, rules, "get_multi_faces_count", path)
        self.get_node_zones = self.__class__.get_node_zones(service, rules, "get_node_zones", path)
        self.get_objects = self.__class__.get_objects(service, rules, "get_objects", path)
        self.get_overlapping_face_zones = self.__class__.get_overlapping_face_zones(service, rules, "get_overlapping_face_zones", path)
        self.get_pairs_of_overlapping_face_zones = self.__class__.get_pairs_of_overlapping_face_zones(service, rules, "get_pairs_of_overlapping_face_zones", path)
        self.get_prism_cell_zones = self.__class__.get_prism_cell_zones(service, rules, "get_prism_cell_zones", path)
        self.get_region_volume = self.__class__.get_region_volume(service, rules, "get_region_volume", path)
        self.get_regions = self.__class__.get_regions(service, rules, "get_regions", path)
        self.get_regions_of_face_zones = self.__class__.get_regions_of_face_zones(service, rules, "get_regions_of_face_zones", path)
        self.get_shared_boundary_face_zones_for_given_cell_zones = self.__class__.get_shared_boundary_face_zones_for_given_cell_zones(service, rules, "get_shared_boundary_face_zones_for_given_cell_zones", path)
        self.get_tet_cell_zones = self.__class__.get_tet_cell_zones(service, rules, "get_tet_cell_zones", path)
        self.get_unreferenced_cell_zones = self.__class__.get_unreferenced_cell_zones(service, rules, "get_unreferenced_cell_zones", path)
        self.get_unreferenced_edge_zones = self.__class__.get_unreferenced_edge_zones(service, rules, "get_unreferenced_edge_zones", path)
        self.get_unreferenced_face_zones = self.__class__.get_unreferenced_face_zones(service, rules, "get_unreferenced_face_zones", path)
        self.get_wrapped_face_zones = self.__class__.get_wrapped_face_zones(service, rules, "get_wrapped_face_zones", path)
        self.get_zone_type = self.__class__.get_zone_type(service, rules, "get_zone_type", path)
        self.get_zones = self.__class__.get_zones(service, rules, "get_zones", path)
        self.get_zones_with_free_faces_for_given_face_zones = self.__class__.get_zones_with_free_faces_for_given_face_zones(service, rules, "get_zones_with_free_faces_for_given_face_zones", path)
        self.get_zones_with_marked_faces_for_given_face_zones = self.__class__.get_zones_with_marked_faces_for_given_face_zones(service, rules, "get_zones_with_marked_faces_for_given_face_zones", path)
        self.get_zones_with_multi_faces_for_given_face_zones = self.__class__.get_zones_with_multi_faces_for_given_face_zones(service, rules, "get_zones_with_multi_faces_for_given_face_zones", path)
        self.interior_zone_exists = self.__class__.interior_zone_exists(service, rules, "interior_zone_exists", path)
        self.mark_bad_quality_faces = self.__class__.mark_bad_quality_faces(service, rules, "mark_bad_quality_faces", path)
        self.mark_duplicate_faces = self.__class__.mark_duplicate_faces(service, rules, "mark_duplicate_faces", path)
        self.mark_face_strips_by_height_and_quality = self.__class__.mark_face_strips_by_height_and_quality(service, rules, "mark_face_strips_by_height_and_quality", path)
        self.mark_faces_by_quality = self.__class__.mark_faces_by_quality(service, rules, "mark_faces_by_quality", path)
        self.mark_faces_deviating_from_size_field = self.__class__.mark_faces_deviating_from_size_field(service, rules, "mark_faces_deviating_from_size_field", path)
        self.mark_faces_in_self_proximity = self.__class__.mark_faces_in_self_proximity(service, rules, "mark_faces_in_self_proximity", path)
        self.mark_faces_using_node_degree = self.__class__.mark_faces_using_node_degree(service, rules, "mark_faces_using_node_degree", path)
        self.mark_free_faces = self.__class__.mark_free_faces(service, rules, "mark_free_faces", path)
        self.mark_invalid_normals = self.__class__.mark_invalid_normals(service, rules, "mark_invalid_normals", path)
        self.mark_island_faces = self.__class__.mark_island_faces(service, rules, "mark_island_faces", path)
        self.mark_multi_faces = self.__class__.mark_multi_faces(service, rules, "mark_multi_faces", path)
        self.mark_point_contacts = self.__class__.mark_point_contacts(service, rules, "mark_point_contacts", path)
        self.mark_self_intersecting_faces = self.__class__.mark_self_intersecting_faces(service, rules, "mark_self_intersecting_faces", path)
        self.mark_sliver_faces = self.__class__.mark_sliver_faces(service, rules, "mark_sliver_faces", path)
        self.mark_spikes = self.__class__.mark_spikes(service, rules, "mark_spikes", path)
        self.mark_steps = self.__class__.mark_steps(service, rules, "mark_steps", path)
        self.mesh_check = self.__class__.mesh_check(service, rules, "mesh_check", path)
        self.mesh_exists = self.__class__.mesh_exists(service, rules, "mesh_exists", path)
        self.print_worst_quality_cell = self.__class__.print_worst_quality_cell(service, rules, "print_worst_quality_cell", path)
        self.project_zone_on_plane = self.__class__.project_zone_on_plane(service, rules, "project_zone_on_plane", path)
        self.refine_marked_faces_in_zones = self.__class__.refine_marked_faces_in_zones(service, rules, "refine_marked_faces_in_zones", path)
        self.scale_cell_zones_around_pivot = self.__class__.scale_cell_zones_around_pivot(service, rules, "scale_cell_zones_around_pivot", path)
        self.scale_face_zones_around_pivot = self.__class__.scale_face_zones_around_pivot(service, rules, "scale_face_zones_around_pivot", path)
        self.separate_cell_zone_layers_by_face_zone_using_id = self.__class__.separate_cell_zone_layers_by_face_zone_using_id(service, rules, "separate_cell_zone_layers_by_face_zone_using_id", path)
        self.separate_cell_zone_layers_by_face_zone_using_name = self.__class__.separate_cell_zone_layers_by_face_zone_using_name(service, rules, "separate_cell_zone_layers_by_face_zone_using_name", path)
        self.separate_face_zones_by_cell_neighbor = self.__class__.separate_face_zones_by_cell_neighbor(service, rules, "separate_face_zones_by_cell_neighbor", path)
        self.unpreserve_cell_zones = self.__class__.unpreserve_cell_zones(service, rules, "unpreserve_cell_zones", path)
        super().__init__(service, rules, path)

    class add_labels_on_cell_zones(PyCommand):
        """
        Add labels on the specified cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.add_labels_on_cell_zones(cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"])
        >>> meshing_session.meshing_utilities.add_labels_on_cell_zones(cell_zone_id_list=[87], label_name_list=["87-1"])
        >>> meshing_session.meshing_utilities.add_labels_on_cell_zones(cell_zone_name_pattern="*", label_name_list=["cell-1"])
        """
        class _add_labels_on_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _add_labels_on_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._add_labels_on_cell_zonesArguments(*args)

    class add_labels_on_edge_zones(PyCommand):
        """
        Add labels on the specified edge zones.
        Parameters
        ----------
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        edge_zone_name_pattern : str
            Edge zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.add_labels_on_edge_zones(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21"], label_name_list=["20-1", "21-1"])
        >>> meshing_session.meshing_utilities.add_labels_on_edge_zones(edge_zone_id_list=[22, 23], label_name_list=["22-1", "23-1"])
        >>> meshing_session.meshing_utilities.add_labels_on_edge_zones(edge_zone_name_pattern="cold-inlet*", label_name_list=["26-1"])
        """
        class _add_labels_on_edge_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.edge_zone_name_pattern = self._edge_zone_name_pattern(self, "edge_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _edge_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _add_labels_on_edge_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._add_labels_on_edge_zonesArguments(*args)

    class add_labels_on_face_zones(PyCommand):
        """
        Add labels on the specified face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.add_labels_on_face_zones(face_zone_name_list=["wall-inlet", "wall-elbow"], label_name_list=["wall-inlet-1", "wall-elbow-1"])
        >>> meshing_session.meshing_utilities.add_labels_on_face_zones(face_zone_id_list=[30, 31], label_name_list=["hot-inlet-1", "cold-inlet-1"])
        >>> meshing_session.meshing_utilities.add_labels_on_face_zones(face_zone_name_pattern="out*", label_name_list=["outlet-1"])
        """
        class _add_labels_on_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _add_labels_on_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._add_labels_on_face_zonesArguments(*args)

    class clean_face_zone_names(PyCommand):
        """
        Clean up face zone names by removing IDs wherever possible.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.clean_face_zone_names()
        """
        class _clean_face_zone_namesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _clean_face_zone_namesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._clean_face_zone_namesArguments(*args)

    class delete_all_sub_domains(PyCommand):
        """
        Deletes all sub-domains (all domains other than global).

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.delete_all_sub_domains()
        """
        class _delete_all_sub_domainsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _delete_all_sub_domainsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._delete_all_sub_domainsArguments(*args)

    class delete_empty_cell_zones(PyCommand):
        """
        Delete empty cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.delete_empty_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.delete_empty_cell_zones(cell_zone_name_list=["elbow.87"])
        >>> meshing_session.meshing_utilities.delete_empty_cell_zones(cell_zone_name_pattern="*")
        """
        class _delete_empty_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _delete_empty_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._delete_empty_cell_zonesArguments(*args)

    class delete_empty_edge_zones(PyCommand):
        """
        Delete empty edge zones.
        Parameters
        ----------
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        edge_zone_name_pattern : str
            Edge zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.delete_empty_edge_zones(edge_zone_id_list=[20, 25, 26])
        >>> meshing_session.meshing_utilities.delete_empty_edge_zones("symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21")
        >>> meshing_session.meshing_utilities.delete_empty_edge_zones(edge_zone_name_pattern="*")
        """
        class _delete_empty_edge_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.edge_zone_name_pattern = self._edge_zone_name_pattern(self, "edge_zone_name_pattern", service, rules, path)

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _edge_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_pattern.
                """

        def create_instance(self) -> _delete_empty_edge_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._delete_empty_edge_zonesArguments(*args)

    class delete_empty_face_zones(PyCommand):
        """
        Delete empty face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.delete_empty_face_zones(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.delete_empty_face_zones(face_zone_name_list=["wall-inlet", "wallfluid-new"])
        >>> meshing_session.meshing_utilities.delete_empty_face_zones(face_zone_name_pattern="*")
        """
        class _delete_empty_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _delete_empty_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._delete_empty_face_zonesArguments(*args)

    class delete_empty_zones(PyCommand):
        """
        Delete empty zones based on the zones specified.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.
        zone_name_list : list[str]
            List containing the face or edge or cell or node zone names.
        zone_name_pattern : str
            Face or edge or cell or node zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.delete_empty_zones(zone_id_list=[20, 32, 87])
        >>> meshing_session.meshing_utilities.delete_empty_zones(zone_name_list=["hotfluid-new", "elbow.87"])
        >>> meshing_session.meshing_utilities.delete_empty_zones(zone_name_pattern="*")
        """
        class _delete_empty_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _delete_empty_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._delete_empty_zonesArguments(*args)

    class delete_marked_faces_in_zones(PyCommand):
        """
        Delete marked faces.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.delete_marked_faces_in_zones(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.delete_marked_faces_in_zones(face_zone_name_list=["wall-inlet", "wallfluid-new"])
        >>> meshing_session.meshing_utilities.delete_marked_faces_in_zones(face_zone_name_pattern="*")
        """
        class _delete_marked_faces_in_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _delete_marked_faces_in_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._delete_marked_faces_in_zonesArguments(*args)

    class merge_cell_zones(PyCommand):
        """
        - Merges the specified cell zones.
        - Specify a list of cell zones or name pattern.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.merge_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.merge_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.merge_cell_zones(cell_zone_name_pattern="*")
        """
        class _merge_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _merge_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._merge_cell_zonesArguments(*args)

    class merge_cell_zones_with_same_prefix(PyCommand):
        """
        Merge cell zones containing the specified prefix.
        Parameters
        ----------
        prefix : str
            Cell zone prefix.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.merge_cell_zones_with_same_prefix(prefix="elbow")
        """
        class _merge_cell_zones_with_same_prefixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.prefix = self._prefix(self, "prefix", service, rules, path)

            class _prefix(PyArgumentsTextualSubItem):
                """
                Argument prefix.
                """

        def create_instance(self) -> _merge_cell_zones_with_same_prefixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._merge_cell_zones_with_same_prefixArguments(*args)

    class merge_cell_zones_with_same_suffix(PyCommand):
        """
        Merge cell zones containing the specified suffix.
        Parameters
        ----------
        suffix : str
            Cell zone suffix.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.merge_cell_zones_with_same_suffix(suffix="fluid")
        """
        class _merge_cell_zones_with_same_suffixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.suffix = self._suffix(self, "suffix", service, rules, path)

            class _suffix(PyArgumentsTextualSubItem):
                """
                Argument suffix.
                """

        def create_instance(self) -> _merge_cell_zones_with_same_suffixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._merge_cell_zones_with_same_suffixArguments(*args)

    class merge_face_zones(PyCommand):
        """
        - Merges the specified face zones.
        - Specify a list of zone IDs or name pattern.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.merge_face_zones(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.merge_face_zones(face_zone_name_pattern="wall*")
        """
        class _merge_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _merge_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._merge_face_zonesArguments(*args)

    class merge_face_zones_of_type(PyCommand):
        """
        Merges face zones of a given type based on name pattern.
        Parameters
        ----------
        face_zone_type : str
            Face zone type.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.merge_face_zones_of_type(face_zone_type="velocity-inlet", face_zone_name_pattern="*")
        """
        class _merge_face_zones_of_typeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_type = self._face_zone_type(self, "face_zone_type", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_type(PyArgumentsTextualSubItem):
                """
                Argument face_zone_type.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _merge_face_zones_of_typeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._merge_face_zones_of_typeArguments(*args)

    class merge_face_zones_with_same_prefix(PyCommand):
        """
        Merge face zones containing the specified prefix.
        Parameters
        ----------
        prefix : str
            Face zone prefix.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.merge_face_zones_with_same_prefix(prefix="elbow")
        """
        class _merge_face_zones_with_same_prefixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.prefix = self._prefix(self, "prefix", service, rules, path)

            class _prefix(PyArgumentsTextualSubItem):
                """
                Argument prefix.
                """

        def create_instance(self) -> _merge_face_zones_with_same_prefixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._merge_face_zones_with_same_prefixArguments(*args)

    class remove_id_suffix_from_face_zones(PyCommand):
        """
        Removes the ID suffix from face zone names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.remove_id_suffix_from_face_zones()
        """
        class _remove_id_suffix_from_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _remove_id_suffix_from_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._remove_id_suffix_from_face_zonesArguments(*args)

    class remove_ids_from_zone_names(PyCommand):
        """
        Remove the zone ID from zone ID list.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.

        Returns
        -------
        bool

        Examples
        --------
        >>> meshing_session.meshing_utilities.remove_ids_from_zone_names(zone_id_list=[30, 31, 32])
        """
        class _remove_ids_from_zone_namesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

        def create_instance(self) -> _remove_ids_from_zone_namesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._remove_ids_from_zone_namesArguments(*args)

    class remove_labels_on_cell_zones(PyCommand):
        """
        Removes the specified labels from the cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.remove_labels_on_cell_zones(cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"])
        >>> meshing_session.meshing_utilities.remove_labels_on_cell_zones(cell_zone_id_list=[87], label_name_list=["87-1"])
        >>> meshing_session.meshing_utilities.remove_labels_on_cell_zones(cell_zone_name_pattern="*", label_name_list=["cell-1"])
        """
        class _remove_labels_on_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _remove_labels_on_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._remove_labels_on_cell_zonesArguments(*args)

    class remove_labels_on_edge_zones(PyCommand):
        """
        Removes the specified labels from the edge zones.
        Parameters
        ----------
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        edge_zone_name_pattern : str
            Edge zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.remove_labels_on_edge_zones(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20"], label_name_list=["20-1"])
        >>> meshing_session.meshing_utilities.remove_labels_on_edge_zones(edge_zone_id_list=[22], label_name_list=["22-1"])
        >>> meshing_session.meshing_utilities.remove_labels_on_edge_zones(edge_zone_name_pattern="*", label_name_list=["26-1"])
        """
        class _remove_labels_on_edge_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.edge_zone_name_pattern = self._edge_zone_name_pattern(self, "edge_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _edge_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _remove_labels_on_edge_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._remove_labels_on_edge_zonesArguments(*args)

    class remove_labels_on_face_zones(PyCommand):
        """
        Removes the specified labels from the face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.remove_labels_on_face_zones(face_zone_name_list=["wall-inlet"], label_name_list=["wall-inlet-1"])
        >>> meshing_session.meshing_utilities.remove_labels_on_face_zones(face_zone_id_list=[30], label_name_list=["hot-inlet-1"])
        >>> meshing_session.meshing_utilities.remove_labels_on_face_zones(face_zone_name_pattern="*", label_name_list=["wall-elbow-1"])
        """
        class _remove_labels_on_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _remove_labels_on_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._remove_labels_on_face_zonesArguments(*args)

    class rename_edge_zone(PyCommand):
        """
        Renames an existing edge zone.
        Parameters
        ----------
        zone_id : int
            Edge zone ID.
        zone_name : str
            Edge zone name.
        new_name : str
            New edge zone name.

        Returns
        -------
        bool

        Examples
        --------
        >>> meshing_session.meshing_utilities.rename_edge_zone(zone_id=20, new_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20-new")
        """
        class _rename_edge_zoneArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.zone_name = self._zone_name(self, "zone_name", service, rules, path)
                self.new_name = self._new_name(self, "new_name", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _zone_name(PyArgumentsTextualSubItem):
                """
                Argument zone_name.
                """

            class _new_name(PyArgumentsTextualSubItem):
                """
                Argument new_name.
                """

        def create_instance(self) -> _rename_edge_zoneArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._rename_edge_zoneArguments(*args)

    class rename_face_zone(PyCommand):
        """
        Renames an existing face zone.
        Parameters
        ----------
        zone_id : int
            Face zone ID.
        zone_name : str
            Face zone name.
        new_name : str
            New face zone name.

        Returns
        -------
        bool

        Examples
        --------
        >>> meshing_session.meshing_utilities.rename_face_zone(zone_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20-new", new_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20")
        >>> meshing_session.meshing_utilities.rename_face_zone(zone_id=32, new_name="outlet-32")
        >>> meshing_session.meshing_utilities.rename_face_zone(zone_name="outlet-32", new_name="outlet")
        """
        class _rename_face_zoneArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.zone_name = self._zone_name(self, "zone_name", service, rules, path)
                self.new_name = self._new_name(self, "new_name", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _zone_name(PyArgumentsTextualSubItem):
                """
                Argument zone_name.
                """

            class _new_name(PyArgumentsTextualSubItem):
                """
                Argument new_name.
                """

        def create_instance(self) -> _rename_face_zoneArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._rename_face_zoneArguments(*args)

    class rename_face_zone_label(PyCommand):
        """
        Renames the face zone label.
        Parameters
        ----------
        object_name : str
            Mesh object name.
        old_label_name : str
            Old label name.
        new_label_name : str
            New label name.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.rename_face_zone_label(object_name="elbow-fluid-1", old_label_name="outlet", new_label_name="outlet-new")
        """
        class _rename_face_zone_labelArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name = self._object_name(self, "object_name", service, rules, path)
                self.old_label_name = self._old_label_name(self, "old_label_name", service, rules, path)
                self.new_label_name = self._new_label_name(self, "new_label_name", service, rules, path)

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

            class _old_label_name(PyArgumentsTextualSubItem):
                """
                Argument old_label_name.
                """

            class _new_label_name(PyArgumentsTextualSubItem):
                """
                Argument new_label_name.
                """

        def create_instance(self) -> _rename_face_zone_labelArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._rename_face_zone_labelArguments(*args)

    class rename_object(PyCommand):
        """
        Renames the object.
        Parameters
        ----------
        old_object_name : str
            Old object name.
        new_object_name : str
            New object name.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.rename_object(old_object_name="elbow-fluid", new_object_name="elbow-fluid-1")
        """
        class _rename_objectArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.old_object_name = self._old_object_name(self, "old_object_name", service, rules, path)
                self.new_object_name = self._new_object_name(self, "new_object_name", service, rules, path)

            class _old_object_name(PyArgumentsTextualSubItem):
                """
                Argument old_object_name.
                """

            class _new_object_name(PyArgumentsTextualSubItem):
                """
                Argument new_object_name.
                """

        def create_instance(self) -> _rename_objectArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._rename_objectArguments(*args)

    class renumber_zone_ids(PyCommand):
        """
        Renumber zone IDs starting from the number specified (start_number).
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.
        start_number : int
            Start number.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.renumber_zone_ids(zone_id_list=[30, 31, 32], start_number=1)
        """
        class _renumber_zone_idsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.start_number = self._start_number(self, "start_number", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _start_number(PyArgumentsNumericalSubItem):
                """
                Argument start_number.
                """

        def create_instance(self) -> _renumber_zone_idsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._renumber_zone_idsArguments(*args)

    class replace_cell_zone_suffix(PyCommand):
        """
        - Replace the cell zone suffix to rename cell zones.
        - Specify whether to merge the cell zones being renamed (set merge to True or False).
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        old_suffix : str
            Old cell zone name suffix.
        new_suffix : str
            New cell zone name suffix.
        merge : bool
            Specify whether to merge the cell zones being renamed.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.replace_cell_zone_suffix(cell_zone_id_list=[87], old_suffix="fluid", new_suffix="fluid-new", merge=True)
        >>> meshing_session.meshing_utilities.replace_cell_zone_suffix(cell_zone_name_list=["elbow-fluid-new"], old_suffix="fluid", new_suffix="fluid-new", merge=True)
        """
        class _replace_cell_zone_suffixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.old_suffix = self._old_suffix(self, "old_suffix", service, rules, path)
                self.new_suffix = self._new_suffix(self, "new_suffix", service, rules, path)
                self.merge = self._merge(self, "merge", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _old_suffix(PyArgumentsTextualSubItem):
                """
                Argument old_suffix.
                """

            class _new_suffix(PyArgumentsTextualSubItem):
                """
                Argument new_suffix.
                """

            class _merge(PyArgumentsParameterSubItem):
                """
                Argument merge.
                """

        def create_instance(self) -> _replace_cell_zone_suffixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._replace_cell_zone_suffixArguments(*args)

    class replace_edge_zone_suffix(PyCommand):
        """
        - Replace the edge zone suffix to rename edge zones.
        - Specify whether to merge the edge zones being renamed (set merge to True or False).
        Parameters
        ----------
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        old_suffix : str
            Old edge zone name suffix.
        new_suffix : str
            New edge zone name suffix.
        merge : bool
            Specify whether to merge the edge zones being renamed.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.replace_edge_zone_suffix(edge_zone_id_list=[20], old_suffix="fluid", new_suffix="fluid-new", merge=True)
        >>> meshing_session.meshing_utilities.replace_edge_zone_suffix(edge_zone_name_list=["hot-inlet:wall-inlet:elbow-fluid:feature.21"], old_suffix="fluid", new_suffix="fluid-new", merge=True)
        """
        class _replace_edge_zone_suffixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.old_suffix = self._old_suffix(self, "old_suffix", service, rules, path)
                self.new_suffix = self._new_suffix(self, "new_suffix", service, rules, path)
                self.merge = self._merge(self, "merge", service, rules, path)

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _old_suffix(PyArgumentsTextualSubItem):
                """
                Argument old_suffix.
                """

            class _new_suffix(PyArgumentsTextualSubItem):
                """
                Argument new_suffix.
                """

            class _merge(PyArgumentsParameterSubItem):
                """
                Argument merge.
                """

        def create_instance(self) -> _replace_edge_zone_suffixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._replace_edge_zone_suffixArguments(*args)

    class replace_face_zone_suffix(PyCommand):
        """
        - Replace the face zone suffix to rename face zones.
        - Specify whether to merge the face zones being renamed (set merge to True or False).
        - Note - If an empty string is specified for the separator (' '), the string specified for replace with will be appended to the face zone names.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        separator : str
            Face zone name separator.
        replace_with : str
            New face zone name suffix.
        merge : bool
            Specify whether to merge the face zones being renamed.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.replace_face_zone_suffix(face_zone_id_list=[30, 31, 32], separator="-suffix-", replace_with="-with-", merge=False)
        >>> meshing_session.meshing_utilities.replace_face_zone_suffix(face_zone_name_list=["cold-inlet", "hot-inlet"], separator="-suffix-", replace_with="-with-", merge=False)
        """
        class _replace_face_zone_suffixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.separator = self._separator(self, "separator", service, rules, path)
                self.replace_with = self._replace_with(self, "replace_with", service, rules, path)
                self.merge = self._merge(self, "merge", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _separator(PyArgumentsTextualSubItem):
                """
                Argument separator.
                """

            class _replace_with(PyArgumentsTextualSubItem):
                """
                Argument replace_with.
                """

            class _merge(PyArgumentsParameterSubItem):
                """
                Argument merge.
                """

        def create_instance(self) -> _replace_face_zone_suffixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._replace_face_zone_suffixArguments(*args)

    class replace_label_suffix(PyCommand):
        """
        Rename labels by replacing the label suffix with a new suffix.
        Parameters
        ----------
        object_name_list : list[str]
            List containing the object names.
        separator : str
            Label separator.
        new_suffix : str
            New label suffix.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.replace_label_suffix(object_name_list=["elbow-fluid-1"], separator="-", new_suffix="fluid-new")
        """
        class _replace_label_suffixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name_list = self._object_name_list(self, "object_name_list", service, rules, path)
                self.separator = self._separator(self, "separator", service, rules, path)
                self.new_suffix = self._new_suffix(self, "new_suffix", service, rules, path)

            class _object_name_list(PyArgumentsTextualSubItem):
                """
                Argument object_name_list.
                """

            class _separator(PyArgumentsTextualSubItem):
                """
                Argument separator.
                """

            class _new_suffix(PyArgumentsTextualSubItem):
                """
                Argument new_suffix.
                """

        def create_instance(self) -> _replace_label_suffixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._replace_label_suffixArguments(*args)

    class replace_object_suffix(PyCommand):
        """
        Rename objects by replacing the object suffix with a new suffix.
        Parameters
        ----------
        object_name_list : list[str]
            List containing the object names.
        separator : str
            Mesh object name separator.
        new_suffix : str
            New object name suffix.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.replace_object_suffix(object_name_list=["elbow-fluid"], separator="-", new_suffix="fluid-new")
        """
        class _replace_object_suffixArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name_list = self._object_name_list(self, "object_name_list", service, rules, path)
                self.separator = self._separator(self, "separator", service, rules, path)
                self.new_suffix = self._new_suffix(self, "new_suffix", service, rules, path)

            class _object_name_list(PyArgumentsTextualSubItem):
                """
                Argument object_name_list.
                """

            class _separator(PyArgumentsTextualSubItem):
                """
                Argument separator.
                """

            class _new_suffix(PyArgumentsTextualSubItem):
                """
                Argument new_suffix.
                """

        def create_instance(self) -> _replace_object_suffixArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._replace_object_suffixArguments(*args)

    class set_number_of_parallel_compute_threads(PyCommand):
        """
        - Set the number of compute threads to use for algorithms like mesh check and quality computation.
        - You can use a variable number of compute threads for these algorithms depending on the current machine loads.
        - The number of compute threads is between 2 and the value (maximum-cores-available - 1).
        Parameters
        ----------
        nthreads : int
            Number of compute threads.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.set_number_of_parallel_compute_threads(nthreads=2)
        """
        class _set_number_of_parallel_compute_threadsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.nthreads = self._nthreads(self, "nthreads", service, rules, path)

            class _nthreads(PyArgumentsNumericalSubItem):
                """
                Argument nthreads.
                """

        def create_instance(self) -> _set_number_of_parallel_compute_threadsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._set_number_of_parallel_compute_threadsArguments(*args)

    class set_object_cell_zone_type(PyCommand):
        """
        Set object cell zone type.
        Parameters
        ----------
        object_name : str
            Mesh object name.
        cell_zone_type : str
            Cell zone type.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.set_object_cell_zone_type(object_name="elbow-fluid", cell_zone_type="mixed")
        """
        class _set_object_cell_zone_typeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name = self._object_name(self, "object_name", service, rules, path)
                self.cell_zone_type = self._cell_zone_type(self, "cell_zone_type", service, rules, path)

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

            class _cell_zone_type(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_type.
                """

        def create_instance(self) -> _set_object_cell_zone_typeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._set_object_cell_zone_typeArguments(*args)

    class set_quality_measure(PyCommand):
        """
        - Set the quality measure.
        - Specify the 'measure' as one of the 'Orthogonal Quality', 'Skewness', 'Equiangle Skewness', 'Size Change', 'Edge Ratio', 'Size', 'Aspect Ratio', 'Squish', 'Warp', 'Dihedral Angle', 'ICEMCFD Quality', 'Ortho Skew', 'FLUENT Aspect Ratio', 'Inverse Orthogonal Quality' value.
        Parameters
        ----------
        measure : str
            Quality measure.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.set_quality_measure(measure="Aspect Ratio")
        """
        class _set_quality_measureArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.measure = self._measure(self, "measure", service, rules, path)

            class _measure(PyArgumentsTextualSubItem):
                """
                Argument measure.
                """

        def create_instance(self) -> _set_quality_measureArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._set_quality_measureArguments(*args)

    class _cell_zones_labels_fdl(PyQuery):
        """
        Get a list containing the cell zone labels.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._cell_zones_labels_fdl()
        """
        class __cell_zones_labels_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __cell_zones_labels_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__cell_zones_labels_fdlArguments(*args)

    class _cell_zones_str_fdl(PyQuery):
        """
        Get a list containing the cell zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._cell_zones_str_fdl()
        """
        class __cell_zones_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __cell_zones_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__cell_zones_str_fdlArguments(*args)

    class _edge_zones_labels_fdl(PyQuery):
        """
        Get a list containing the edge zone labels.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._edge_zones_labels_fdl()
        """
        class __edge_zones_labels_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __edge_zones_labels_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__edge_zones_labels_fdlArguments(*args)

    class _edge_zones_str_fdl(PyQuery):
        """
        Get a list containing the edge zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._edge_zones_str_fdl()
        """
        class __edge_zones_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __edge_zones_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__edge_zones_str_fdlArguments(*args)

    class _face_zones_labels_fdl(PyQuery):
        """
        Get a list containing the face zone labels.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._face_zones_labels_fdl()
        """
        class __face_zones_labels_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __face_zones_labels_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__face_zones_labels_fdlArguments(*args)

    class _face_zones_str_fdl(PyQuery):
        """
        Get a list containing the face zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._face_zones_str_fdl()
        """
        class __face_zones_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __face_zones_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__face_zones_str_fdlArguments(*args)

    class _node_zones_labels_fdl(PyQuery):
        """
        Get a list containing the node zone labels.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._node_zones_labels_fdl()
        """
        class __node_zones_labels_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __node_zones_labels_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__node_zones_labels_fdlArguments(*args)

    class _node_zones_str_fdl(PyQuery):
        """
        Get a list containing the node zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._node_zones_str_fdl()
        """
        class __node_zones_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __node_zones_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__node_zones_str_fdlArguments(*args)

    class _object_names_str_fdl(PyQuery):
        """
        Get a list containing the object names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._object_names_str_fdl()
        """
        class __object_names_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __object_names_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__object_names_str_fdlArguments(*args)

    class _prism_cell_zones_labels_fdl(PyQuery):
        """
        Get a list containing the prism cell zone labels.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._prism_cell_zones_labels_fdl()
        """
        class __prism_cell_zones_labels_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __prism_cell_zones_labels_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__prism_cell_zones_labels_fdlArguments(*args)

    class _prism_cell_zones_str_fdl(PyQuery):
        """
        Get a list containing the prism cell zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._prism_cell_zones_str_fdl()
        """
        class __prism_cell_zones_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __prism_cell_zones_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__prism_cell_zones_str_fdlArguments(*args)

    class _regions_str_fdl(PyQuery):
        """
        Get a list containing the region names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._regions_str_fdl()
        """
        class __regions_str_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __regions_str_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__regions_str_fdlArguments(*args)

    class _zone_types_fdl(PyQuery):
        """
        Get a list containing the zone type names.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities._zone_types_fdl()
        """
        class __zone_types_fdlArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> __zone_types_fdlArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self.__zone_types_fdlArguments(*args)

    class boundary_zone_exists(PyQuery):
        """
        Report if the boundary face zone exists.
        Parameters
        ----------
        zone_id : int
            Zone ID.
        zone_name : str
            Zone name.

        Returns
        -------
        bool

        Examples
        --------
        >>> meshing_session.meshing_utilities.boundary_zone_exists(zone_id=31)
        >>> meshing_session.meshing_utilities.boundary_zone_exists(zone_name="wall-inlet")
        """
        class _boundary_zone_existsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.zone_name = self._zone_name(self, "zone_name", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _zone_name(PyArgumentsTextualSubItem):
                """
                Argument zone_name.
                """

        def create_instance(self) -> _boundary_zone_existsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._boundary_zone_existsArguments(*args)

    class cell_zone_exists(PyQuery):
        """
        Report if the volume mesh exists.
        Parameters
        ----------
        zone_id : int
            Cell zone ID.
        zone_name : str
            Cell zone name.

        Returns
        -------
        bool

        Examples
        --------
        >>> meshing_session.meshing_utilities.cell_zone_exists(zone_id=87)
        >>> meshing_session.meshing_utilities.cell_zone_exists(zone_name="elbow.87")
        """
        class _cell_zone_existsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.zone_name = self._zone_name(self, "zone_name", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _zone_name(PyArgumentsTextualSubItem):
                """
                Argument zone_name.
                """

        def create_instance(self) -> _cell_zone_existsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._cell_zone_existsArguments(*args)

    class convert_zone_ids_to_name_strings(PyQuery):
        """
        Convert a list of IDs to a list of names.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.convert_zone_ids_to_name_strings(zone_id_list=[32, 31])
        """
        class _convert_zone_ids_to_name_stringsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

        def create_instance(self) -> _convert_zone_ids_to_name_stringsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._convert_zone_ids_to_name_stringsArguments(*args)

    class convert_zone_name_strings_to_ids(PyQuery):
        """
        Convert a list of zone name strings to a list of IDs.
        Parameters
        ----------
        zone_name_list : list[str]
            List containing the face or edge or cell or node zone names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.convert_zone_name_strings_to_ids(zone_name_list=["outlet", "cold-inlet"])
        """
        class _convert_zone_name_strings_to_idsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

        def create_instance(self) -> _convert_zone_name_strings_to_idsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._convert_zone_name_strings_to_idsArguments(*args)

    class copy_face_zone_labels(PyQuery):
        """
        - Copy labels from one face zone to another.
        - Specify either face zone names or IDs.
        Parameters
        ----------
        from_face_zone_id : int
            Face zone ID.
        from_face_zone_name : str
            Face zone name.
        to_face_zone_id : int
            Face zone ID.
        to_face_zone_name : str
            Face zone name.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.copy_face_zone_labels(from_face_zone_id=33, to_face_zone_id=34)
        """
        class _copy_face_zone_labelsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.from_face_zone_id = self._from_face_zone_id(self, "from_face_zone_id", service, rules, path)
                self.from_face_zone_name = self._from_face_zone_name(self, "from_face_zone_name", service, rules, path)
                self.to_face_zone_id = self._to_face_zone_id(self, "to_face_zone_id", service, rules, path)
                self.to_face_zone_name = self._to_face_zone_name(self, "to_face_zone_name", service, rules, path)

            class _from_face_zone_id(PyArgumentsNumericalSubItem):
                """
                Argument from_face_zone_id.
                """

            class _from_face_zone_name(PyArgumentsTextualSubItem):
                """
                Argument from_face_zone_name.
                """

            class _to_face_zone_id(PyArgumentsNumericalSubItem):
                """
                Argument to_face_zone_id.
                """

            class _to_face_zone_name(PyArgumentsTextualSubItem):
                """
                Argument to_face_zone_name.
                """

        def create_instance(self) -> _copy_face_zone_labelsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._copy_face_zone_labelsArguments(*args)

    class count_marked_faces(PyQuery):
        """
        Returns the count of marked faces for the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.count_marked_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.count_marked_faces(face_zone_name_pattern="*")
        """
        class _count_marked_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _count_marked_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._count_marked_facesArguments(*args)

    class create_boi_and_size_functions_from_refinement_regions(PyQuery):
        """
        - Create bodies of influence and if required body of influence size functions from the mesh refinement regions.
        - Specify the refinement region type (set 'region_type' to 'tet' or 'hexcore').
        - Specify the prefix for the BOI zones ('boi_prefix_string'), and choose whether to create the size functions (set create_size_function to True or False).
        Parameters
        ----------
        region_type : str
            Specify the refinement region type.
        boi_prefix_string : str
            Specify the prefix for the BOI zones.
        create_size_function : bool
            Specify whether to create the size functions.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.create_boi_and_size_functions_from_refinement_regions(region_type="hexcore", boi_prefix_string="wall", create_size_function=True)
        """
        class _create_boi_and_size_functions_from_refinement_regionsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.region_type = self._region_type(self, "region_type", service, rules, path)
                self.boi_prefix_string = self._boi_prefix_string(self, "boi_prefix_string", service, rules, path)
                self.create_size_function = self._create_size_function(self, "create_size_function", service, rules, path)

            class _region_type(PyArgumentsTextualSubItem):
                """
                Argument region_type.
                """

            class _boi_prefix_string(PyArgumentsTextualSubItem):
                """
                Argument boi_prefix_string.
                """

            class _create_size_function(PyArgumentsParameterSubItem):
                """
                Argument create_size_function.
                """

        def create_instance(self) -> _create_boi_and_size_functions_from_refinement_regionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._create_boi_and_size_functions_from_refinement_regionsArguments(*args)

    class dump_face_zone_orientation_in_region(PyQuery):
        """
        Return the face zones and their orientation for the mesh file specified.
        Parameters
        ----------
        file_name : str
            Mesh file name.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.dump_face_zone_orientation_in_region(file_name="facezonetest.txt")
        """
        class _dump_face_zone_orientation_in_regionArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.file_name = self._file_name(self, "file_name", service, rules, path)

            class _file_name(PyArgumentsTextualSubItem):
                """
                Argument file_name.
                """

        def create_instance(self) -> _dump_face_zone_orientation_in_regionArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._dump_face_zone_orientation_in_regionArguments(*args)

    class fill_holes_in_face_zone_list(PyQuery):
        """
        Fill holes associated with free edges for the face zones specified, based on the number of free edges (max_hole_edges).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        max_hole_edges : int
            Number of maximum hole edges.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.fill_holes_in_face_zone_list(face_zone_id_list=[30, 31, 32], max_hole_edges=2)
        >>> meshing_session.meshing_utilities.fill_holes_in_face_zone_list(face_zone_name_list=["wall-inlet", "wallfluid-new"], max_hole_edges=2)
        >>> meshing_session.meshing_utilities.fill_holes_in_face_zone_list(face_zone_name_pattern="wall*", max_hole_edges=2)
        """
        class _fill_holes_in_face_zone_listArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.max_hole_edges = self._max_hole_edges(self, "max_hole_edges", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _max_hole_edges(PyArgumentsNumericalSubItem):
                """
                Argument max_hole_edges.
                """

        def create_instance(self) -> _fill_holes_in_face_zone_listArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._fill_holes_in_face_zone_listArguments(*args)

    class get_adjacent_cell_zones_for_given_face_zones(PyQuery):
        """
        Return adjacent cell zones for given face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(face_zone_name_pattern="*")
        """
        class _get_adjacent_cell_zones_for_given_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_adjacent_cell_zones_for_given_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_adjacent_cell_zones_for_given_face_zonesArguments(*args)

    class get_adjacent_face_zones_for_given_cell_zones(PyQuery):
        """
        Return adjacent boundary face zones for given cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")
        """
        class _get_adjacent_face_zones_for_given_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_adjacent_face_zones_for_given_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_adjacent_face_zones_for_given_cell_zonesArguments(*args)

    class get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(PyQuery):
        """
        Return adjacent interior and boundary face zones for given cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")
        """
        class _get_adjacent_interior_and_boundary_face_zones_for_given_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_adjacent_interior_and_boundary_face_zones_for_given_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_adjacent_interior_and_boundary_face_zones_for_given_cell_zonesArguments(*args)

    class get_adjacent_zones_by_edge_connectivity(PyQuery):
        """
        Return adjacent zones based on edge connectivity.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.
        zone_name_list : list[str]
            List containing the face or edge or cell or node zone names.
        zone_name_pattern : str
            Face or edge or cell or node zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(zone_name_pattern="*")
        """
        class _get_adjacent_zones_by_edge_connectivityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_adjacent_zones_by_edge_connectivityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_adjacent_zones_by_edge_connectivityArguments(*args)

    class get_adjacent_zones_by_node_connectivity(PyQuery):
        """
        Return adjacent zones based on node connectivity.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.
        zone_name_list : list[str]
            List containing the face or edge or cell or node zone names.
        zone_name_pattern : str
            Face or edge or cell or node zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(zone_name_pattern="*")
        """
        class _get_adjacent_zones_by_node_connectivityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_adjacent_zones_by_node_connectivityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_adjacent_zones_by_node_connectivityArguments(*args)

    class get_all_objects(PyQuery):
        """
        Return a list of all objects.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_all_objects()
        """
        class _get_all_objectsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _get_all_objectsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_all_objectsArguments(*args)

    class get_average_bounding_box_center(PyQuery):
        """
        Return a suitable average point based on the zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.

        Returns
        -------
        list[float]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_average_bounding_box_center(face_zone_id_list=[30, 31, 32])
        """
        class _get_average_bounding_box_centerArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

        def create_instance(self) -> _get_average_bounding_box_centerArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_average_bounding_box_centerArguments(*args)

    class get_baffles_for_face_zones(PyQuery):
        """
        Return the baffle zones based on the face zone list specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_baffles_for_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])
        """
        class _get_baffles_for_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

        def create_instance(self) -> _get_baffles_for_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_baffles_for_face_zonesArguments(*args)

    class get_bounding_box_of_zone_list(PyQuery):
        """
        Return the bounding box extents for the list of zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face or edge or cell or node zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_bounding_box_of_zone_list(zone_id_list=[26])
        """
        class _get_bounding_box_of_zone_listArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

        def create_instance(self) -> _get_bounding_box_of_zone_listArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_bounding_box_of_zone_listArguments(*args)

    class get_cell_mesh_distribution(PyQuery):
        """
        - Report the cell mesh distribution based on the specified measure, partitions, and range.
        - Specify the 'measure' as one of the 'Orthogonal Quality', 'Skewness', 'Equiangle Skewness', 'Size Change', 'Edge Ratio', 'Size', 'Aspect Ratio', 'Squish', 'Warp', 'Dihedral Angle', 'ICEMCFD Quality', 'Ortho Skew', 'FLUENT Aspect Ratio', 'Inverse Orthogonal Quality' value.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        measure : str
            Measure.
        partitions : int
            Partitions.
        range : list[float]
            Range.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_mesh_distribution(cell_zone_id_list=[87], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])
        >>> meshing_session.meshing_utilities.get_cell_mesh_distribution(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])
        >>> meshing_session.meshing_utilities.get_cell_mesh_distribution(cell_zone_name_pattern="*", measure="Orthogonal Quality", partitions=2, range=[0.9, 1])
        """
        class _get_cell_mesh_distributionArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.measure = self._measure(self, "measure", service, rules, path)
                self.partitions = self._partitions(self, "partitions", service, rules, path)
                self.range = self._range(self, "range", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _measure(PyArgumentsTextualSubItem):
                """
                Argument measure.
                """

            class _partitions(PyArgumentsNumericalSubItem):
                """
                Argument partitions.
                """

            class _range(PyArgumentsNumericalSubItem):
                """
                Argument range.
                """

        def create_instance(self) -> _get_cell_mesh_distributionArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_mesh_distributionArguments(*args)

    class get_cell_quality_limits(PyQuery):
        """
        - Report the number of cells and the cell quality limits (minimum, maximum, average quality) for the list of zones based on the measure specified.
        - You can also report the cell size limits.
        - Specify the 'measure' as one of the 'Orthogonal Quality', 'Skewness', 'Equiangle Skewness', 'Size Change', 'Edge Ratio', 'Size', 'Aspect Ratio', 'Squish', 'Warp', 'Dihedral Angle', 'ICEMCFD Quality', 'Ortho Skew', 'FLUENT Aspect Ratio', 'Inverse Orthogonal Quality' value.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        measure : str
            Measure.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_quality_limits(cell_zone_id_list=[87], measure="Orthogonal Quality")
        >>> meshing_session.meshing_utilities.get_cell_quality_limits(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality")
        >>> meshing_session.meshing_utilities.get_cell_quality_limits(cell_zone_name_pattern="*", measure="Orthogonal Quality")
        """
        class _get_cell_quality_limitsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.measure = self._measure(self, "measure", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _measure(PyArgumentsTextualSubItem):
                """
                Argument measure.
                """

        def create_instance(self) -> _get_cell_quality_limitsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_quality_limitsArguments(*args)

    class get_cell_zone_count(PyQuery):
        """
        Return count of entities for cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_name_pattern="*")
        """
        class _get_cell_zone_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_cell_zone_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_zone_countArguments(*args)

    class get_cell_zone_id_list_with_labels(PyQuery):
        """
        Returns the list of cell zones (by ID) containing the labels specified.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(cell_zone_id_list=[87], label_name_list=["elbow-1"])
        >>> meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"])
        >>> meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(cell_zone_name_pattern="*", label_name_list=["elbow-1"])
        """
        class _get_cell_zone_id_list_with_labelsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _get_cell_zone_id_list_with_labelsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_zone_id_list_with_labelsArguments(*args)

    class get_cell_zone_shape(PyQuery):
        """
        Return cell zone shape as string.
        Parameters
        ----------
        cell_zone_id : int
            Cell zone ID.

        Returns
        -------
        str

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_zone_shape(cell_zone_id=87)
        """
        class _get_cell_zone_shapeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id = self._cell_zone_id(self, "cell_zone_id", service, rules, path)

            class _cell_zone_id(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id.
                """

        def create_instance(self) -> _get_cell_zone_shapeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_zone_shapeArguments(*args)

    class get_cell_zone_volume(PyQuery):
        """
        Return cell zone volume for the specified zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        float

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_name_pattern="*")
        """
        class _get_cell_zone_volumeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_cell_zone_volumeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_zone_volumeArguments(*args)

    class get_cell_zones(PyQuery):
        """
        - Get cell zones using 1 - maximum_entity_count and only_boundary or 2 - xyz_coordinates or 3 - filter.
        - Return a list of cell zones at or closest to a specified location (xyz_coordinates).
        - Return a list of cell zones with a count below the maximum entity count (maximum_entity_count) specified.
        - You can choose to restrict the report to only boundary cell zones, if required (only_boundary set to True or False).
        - Return a list of zones whose names contain the specified filter string.
        Parameters
        ----------
        maximum_entity_count : float
            Maximum entity count.
        xyz_coordinates : list[float]
            X-Y-Z coordinates.
        filter : str
            Cell zone name filter.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_cell_zones(filter="*")
        >>> meshing_session.meshing_utilities.get_cell_zones(maximum_entity_count=100)
        >>> meshing_session.meshing_utilities.get_cell_zones(xyz_coordinates=[-7, -6, 0.4])
        """
        class _get_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.maximum_entity_count = self._maximum_entity_count(self, "maximum_entity_count", service, rules, path)
                self.xyz_coordinates = self._xyz_coordinates(self, "xyz_coordinates", service, rules, path)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _maximum_entity_count(PyArgumentsNumericalSubItem):
                """
                Argument maximum_entity_count.
                """

            class _xyz_coordinates(PyArgumentsNumericalSubItem):
                """
                Argument xyz_coordinates.
                """

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_cell_zonesArguments(*args)

    class get_edge_size_limits(PyQuery):
        """
        Report the edge size limits for the list of face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[float]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_edge_size_limits(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.get_edge_size_limits(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.get_edge_size_limits(face_zone_name_pattern="*")
        """
        class _get_edge_size_limitsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_edge_size_limitsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_edge_size_limitsArguments(*args)

    class get_edge_zone_id_list_with_labels(PyQuery):
        """
        Returns the list of edge zones (by ID) containing the labels specified.
        Parameters
        ----------
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        edge_zone_name_pattern : str
            Edge zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(edge_zone_id_list=[20, 21], label_name_list=["20-1", "21-1"])
        >>> meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21"], label_name_list=["20-1", "21-1"])
        >>> meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(edge_zone_name_pattern="*", label_name_list=["20-1", "21-1"])
        """
        class _get_edge_zone_id_list_with_labelsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.edge_zone_name_pattern = self._edge_zone_name_pattern(self, "edge_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _edge_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _get_edge_zone_id_list_with_labelsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_edge_zone_id_list_with_labelsArguments(*args)

    class get_edge_zones(PyQuery):
        """
        - Get edge zones using 1 - maximum_entity_count and only_boundary or 2 - filter Return a list of edge zones with a count below the maximum entity count (maximum_entity_count) specified.
        - You can choose to restrict the report to only boundary edge zones, if required (only_boundary set to True or False).
        - Return a list of zones whose names contain the specified filter string.
        Parameters
        ----------
        maximum_entity_count : float
            Maximum entity count.
        only_boundary : bool
            Specify whether to restrict the report to only boundary edge zones.
        filter : str
            Edge zone name filter.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_edge_zones(filter="*")
        >>> meshing_session.meshing_utilities.get_edge_zones(maximum_entity_count=20, only_boundary=False)
        """
        class _get_edge_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.maximum_entity_count = self._maximum_entity_count(self, "maximum_entity_count", service, rules, path)
                self.only_boundary = self._only_boundary(self, "only_boundary", service, rules, path)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _maximum_entity_count(PyArgumentsNumericalSubItem):
                """
                Argument maximum_entity_count.
                """

            class _only_boundary(PyArgumentsParameterSubItem):
                """
                Argument only_boundary.
                """

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_edge_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_edge_zonesArguments(*args)

    class get_edge_zones_list(PyQuery):
        """
        Return a list of edge zones whose names contain the specified filter string.
        Parameters
        ----------
        filter : list[str]
            Edge zone name filter.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_edge_zones_list(filter="*")
        """
        class _get_edge_zones_listArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_edge_zones_listArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_edge_zones_listArguments(*args)

    class get_edge_zones_of_object(PyQuery):
        """
        Return a list of edge zones in the specified object or objects.
        Parameters
        ----------
        objects : list[str]
            List containing the object names list.
        object_name : str
            Mesh object name.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_edge_zones_of_object(objects=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_edge_zones_of_object(object_name="elbow-fluid")
        """
        class _get_edge_zones_of_objectArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.objects = self._objects(self, "objects", service, rules, path)
                self.object_name = self._object_name(self, "object_name", service, rules, path)

            class _objects(PyArgumentsTextualSubItem):
                """
                Argument objects.
                """

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

        def create_instance(self) -> _get_edge_zones_of_objectArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_edge_zones_of_objectArguments(*args)

    class get_embedded_baffles(PyQuery):
        """
        Return the embedded baffle zones.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_embedded_baffles()
        """
        class _get_embedded_bafflesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _get_embedded_bafflesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_embedded_bafflesArguments(*args)

    class get_face_mesh_distribution(PyQuery):
        """
        - Report the face mesh distribution based on the specified measure, partitions, and range.
        - Specify the 'measure' as one of the 'Orthogonal Quality', 'Skewness', 'Equiangle Skewness', 'Size Change', 'Edge Ratio', 'Size', 'Aspect Ratio', 'Squish', 'Warp', 'Dihedral Angle', 'ICEMCFD Quality', 'Ortho Skew', 'FLUENT Aspect Ratio', 'Inverse Orthogonal Quality' value.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        measure : str
            Measure.
        partitions : int
            Partitions.
        range : list[float]
            Range.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_mesh_distribution(face_zone_id_list=[30, 31, 32], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])
        >>> meshing_session.meshing_utilities.get_face_mesh_distribution(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])
        >>> meshing_session.meshing_utilities.get_face_mesh_distribution(face_zone_name_pattern="*", measure="Orthogonal Quality", partitions=2, range=[0.9, 1])
        """
        class _get_face_mesh_distributionArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.measure = self._measure(self, "measure", service, rules, path)
                self.partitions = self._partitions(self, "partitions", service, rules, path)
                self.range = self._range(self, "range", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _measure(PyArgumentsTextualSubItem):
                """
                Argument measure.
                """

            class _partitions(PyArgumentsNumericalSubItem):
                """
                Argument partitions.
                """

            class _range(PyArgumentsNumericalSubItem):
                """
                Argument range.
                """

        def create_instance(self) -> _get_face_mesh_distributionArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_mesh_distributionArguments(*args)

    class get_face_quality_limits(PyQuery):
        """
        - Report the number of faces and the face quality limits (minimum, maximum, average quality) for the list of zones based on the measure specified.
        - You can also report the face size limits.
        - Specify the 'measure' as one of the 'Orthogonal Quality', 'Skewness', 'Equiangle Skewness', 'Size Change', 'Edge Ratio', 'Size', 'Aspect Ratio', 'Squish', 'Warp', 'Dihedral Angle', 'ICEMCFD Quality', 'Ortho Skew', 'FLUENT Aspect Ratio', 'Inverse Orthogonal Quality' value.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        measure : str
            Measure.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_quality_limits(face_zone_id_list=[30, 31, 32], measure="Orthogonal Quality")
        >>> meshing_session.meshing_utilities.get_face_quality_limits(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], measure="Orthogonal Quality")
        >>> meshing_session.meshing_utilities.get_face_quality_limits(face_zone_name_pattern="*", measure="Orthogonal Quality")
        """
        class _get_face_quality_limitsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.measure = self._measure(self, "measure", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _measure(PyArgumentsTextualSubItem):
                """
                Argument measure.
                """

        def create_instance(self) -> _get_face_quality_limitsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_quality_limitsArguments(*args)

    class get_face_zone_area(PyQuery):
        """
        Return face zone area for the specified zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        float

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zone_area(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.get_face_zone_area(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.get_face_zone_area(face_zone_name_pattern="*")
        """
        class _get_face_zone_areaArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_face_zone_areaArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zone_areaArguments(*args)

    class get_face_zone_count(PyQuery):
        """
        Return count of entities for face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zone_count(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.get_face_zone_count(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.get_face_zone_count(face_zone_name_pattern="*")
        """
        class _get_face_zone_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_face_zone_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zone_countArguments(*args)

    class get_face_zone_id_list_with_labels(PyQuery):
        """
        Returns the list of face zones (by ID) containing the labels specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        label_name_list : list[str]
            List containing the label names.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(face_zone_id_list=[33, 34], label_name_list=["wall-inlet-1", "wall-elbow-1"])
        >>> meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(face_zone_name_list=["wall-inlet", "wall-elbow"], label_name_list=["wall-inlet-1", "wall-elbow-1"])
        >>> meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(face_zone_name_pattern="wall*", label_name_list=["wall-inlet-1", "wall-elbow-1"])
        """
        class _get_face_zone_id_list_with_labelsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.label_name_list = self._label_name_list(self, "label_name_list", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _label_name_list(PyArgumentsTextualSubItem):
                """
                Argument label_name_list.
                """

        def create_instance(self) -> _get_face_zone_id_list_with_labelsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zone_id_list_with_labelsArguments(*args)

    class get_face_zone_node_count(PyQuery):
        """
        Returns the node count for the specified face zone.
        Parameters
        ----------
        face_zone_id : int
            Face zone ID.
        face_zone_name : str
            Face zone name.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zone_node_count(face_zone_id=32)
        >>> meshing_session.meshing_utilities.get_face_zone_node_count(face_zone_name="outlet")
        """
        class _get_face_zone_node_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id = self._face_zone_id(self, "face_zone_id", service, rules, path)
                self.face_zone_name = self._face_zone_name(self, "face_zone_name", service, rules, path)

            class _face_zone_id(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id.
                """

            class _face_zone_name(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name.
                """

        def create_instance(self) -> _get_face_zone_node_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zone_node_countArguments(*args)

    class get_face_zones(PyQuery):
        """
        - Get face zones using 1 - maximum_entity_count and only_boundary or 2 - prism_control_name or 3 - xyz_coordinates or 4 - filter.
        - Return a list of face zones at or closest to a specified location (xyz_coordinates - not applicable to polyhedra mesh).
        - Return a list of face zones with a count below the maximum entity count (maximum_entity_count) specified.
        - You can choose to restrict the report to only boundary face zones, if required (only_boundary set to True or False).
        - Return a list of face zones to which the specified prism controls apply.
        - Return a list of zones whose names contain the specified filter string.
        Parameters
        ----------
        maximum_entity_count : float
            Maximum entity count.
        only_boundary : bool
            Specify whether to restrict the report to only boundary face zones.
        prism_control_name : str
            Prism control name.
        xyz_coordinates : list[float]
            X-Y-Z coordinates.
        filter : str
            Face zone name filter.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zones(filter="*")
        >>> meshing_session.meshing_utilities.get_face_zones(prism_control_name="*")
        >>> meshing_session.meshing_utilities.get_face_zones(xyz_coordinates=[1.4, 1.4, 1.4])
        >>> meshing_session.meshing_utilities.get_face_zones(maximum_entity_count=20, only_boundary=True)
        """
        class _get_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.maximum_entity_count = self._maximum_entity_count(self, "maximum_entity_count", service, rules, path)
                self.only_boundary = self._only_boundary(self, "only_boundary", service, rules, path)
                self.prism_control_name = self._prism_control_name(self, "prism_control_name", service, rules, path)
                self.xyz_coordinates = self._xyz_coordinates(self, "xyz_coordinates", service, rules, path)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _maximum_entity_count(PyArgumentsNumericalSubItem):
                """
                Argument maximum_entity_count.
                """

            class _only_boundary(PyArgumentsParameterSubItem):
                """
                Argument only_boundary.
                """

            class _prism_control_name(PyArgumentsTextualSubItem):
                """
                Argument prism_control_name.
                """

            class _xyz_coordinates(PyArgumentsNumericalSubItem):
                """
                Argument xyz_coordinates.
                """

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zonesArguments(*args)

    class get_face_zones_by_zone_area(PyQuery):
        """
        - Return a list of face zones with a maximum zone area below the maximum_zone_area specified.
        - Return a list of face zones with a minimum zone area above the minimum_zone_area specified.
        Parameters
        ----------
        maximum_zone_area : float
            Maximum zone area.
        minimum_zone_area : float
            Minimum zone area.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zones_by_zone_area(maximum_zone_area=100)
        >>> meshing_session.meshing_utilities.get_face_zones_by_zone_area(minimum_zone_area=10)
        """
        class _get_face_zones_by_zone_areaArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.maximum_zone_area = self._maximum_zone_area(self, "maximum_zone_area", service, rules, path)
                self.minimum_zone_area = self._minimum_zone_area(self, "minimum_zone_area", service, rules, path)

            class _maximum_zone_area(PyArgumentsNumericalSubItem):
                """
                Argument maximum_zone_area.
                """

            class _minimum_zone_area(PyArgumentsNumericalSubItem):
                """
                Argument minimum_zone_area.
                """

        def create_instance(self) -> _get_face_zones_by_zone_areaArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zones_by_zone_areaArguments(*args)

    class get_face_zones_of_object(PyQuery):
        """
        - Return a list of face zones using 1 - object_name and regions or 2 - object_name and labels or 3 - object_name and region_type or 4 - object_name or 5 - objects.
        - where region_type is one of the 'fluid-fluid', 'solid-solid', or 'fluid-solid' value.
        Parameters
        ----------
        regions : list[str]
            List containing the region names.
        labels : list[str]
            List containing the face zone labels.
        region_type : str
            Region type.
        objects : list[str]
            List containing the object names.
        object_name : str
            Mesh object name.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid", regions=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid", labels=["outlet"])
        >>> meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid", region_type="elbow-fluid")
        >>> meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid")
        >>> meshing_session.meshing_utilities.get_face_zones_of_object(objects=["elbow-fluid"])
        """
        class _get_face_zones_of_objectArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.regions = self._regions(self, "regions", service, rules, path)
                self.labels = self._labels(self, "labels", service, rules, path)
                self.region_type = self._region_type(self, "region_type", service, rules, path)
                self.objects = self._objects(self, "objects", service, rules, path)
                self.object_name = self._object_name(self, "object_name", service, rules, path)

            class _regions(PyArgumentsTextualSubItem):
                """
                Argument regions.
                """

            class _labels(PyArgumentsTextualSubItem):
                """
                Argument labels.
                """

            class _region_type(PyArgumentsTextualSubItem):
                """
                Argument region_type.
                """

            class _objects(PyArgumentsTextualSubItem):
                """
                Argument objects.
                """

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

        def create_instance(self) -> _get_face_zones_of_objectArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zones_of_objectArguments(*args)

    class get_face_zones_with_zone_specific_prisms_applied(PyQuery):
        """
        Return a list of face zones with zone-specific prism settings applied.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_face_zones_with_zone_specific_prisms_applied()
        """
        class _get_face_zones_with_zone_specific_prisms_appliedArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _get_face_zones_with_zone_specific_prisms_appliedArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_face_zones_with_zone_specific_prisms_appliedArguments(*args)

    class get_free_faces_count(PyQuery):
        """
        Returns the count of free faces for the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_free_faces_count(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.get_free_faces_count(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.get_free_faces_count(face_zone_name_pattern="*")
        """
        class _get_free_faces_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_free_faces_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_free_faces_countArguments(*args)

    class get_interior_face_zones_for_given_cell_zones(PyQuery):
        """
        Returns interior face zones connected to given cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")
        """
        class _get_interior_face_zones_for_given_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_interior_face_zones_for_given_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_interior_face_zones_for_given_cell_zonesArguments(*args)

    class get_labels(PyQuery):
        """
        Return a list of face zone labels in the specified object, whose names contain the specified filter or pattern string.
        Parameters
        ----------
        object_name : str
            Mesh object name.
        filter : str
            Label name filter.
        label_name_pattern : str
            Label name pattern.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid")
        >>> meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid", filter="*")
        >>> meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid", label_name_pattern="*")
        """
        class _get_labelsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name = self._object_name(self, "object_name", service, rules, path)
                self.filter = self._filter(self, "filter", service, rules, path)
                self.label_name_pattern = self._label_name_pattern(self, "label_name_pattern", service, rules, path)

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

            class _label_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument label_name_pattern.
                """

        def create_instance(self) -> _get_labelsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_labelsArguments(*args)

    class get_labels_on_cell_zones(PyQuery):
        """
        Returns the list of labels for the specified cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_labels_on_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_labels_on_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_labels_on_cell_zones(cell_zone_name_pattern="*")
        """
        class _get_labels_on_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_labels_on_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_labels_on_cell_zonesArguments(*args)

    class get_labels_on_edge_zones(PyQuery):
        """
        Returns the list of labels for the specified edge zones.
        Parameters
        ----------
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        edge_zone_name_pattern : str
            Edge zone name pattern.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_labels_on_edge_zones(edge_zone_id_list=[22, 23])
        >>> meshing_session.meshing_utilities.get_labels_on_edge_zones(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21"])
        >>> meshing_session.meshing_utilities.get_labels_on_edge_zones(edge_zone_name_pattern="cold-inlet*")
        """
        class _get_labels_on_edge_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.edge_zone_name_pattern = self._edge_zone_name_pattern(self, "edge_zone_name_pattern", service, rules, path)

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _edge_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_pattern.
                """

        def create_instance(self) -> _get_labels_on_edge_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_labels_on_edge_zonesArguments(*args)

    class get_labels_on_face_zones(PyQuery):
        """
        Returns the list of labels for the specified face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_labels_on_face_zones(face_zone_id_list=[30, 31])
        >>> meshing_session.meshing_utilities.get_labels_on_face_zones(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.get_labels_on_face_zones(face_zone_name_pattern="out*")
        """
        class _get_labels_on_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_labels_on_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_labels_on_face_zonesArguments(*args)

    class get_labels_on_face_zones_list(PyQuery):
        """
        Returns the list of labels for the specified face zones.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_labels_on_face_zones_list(face_zone_id_list=[30, 31])
        """
        class _get_labels_on_face_zones_listArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

        def create_instance(self) -> _get_labels_on_face_zones_listArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_labels_on_face_zones_listArguments(*args)

    class get_maxsize_cell_zone_by_count(PyQuery):
        """
        Return cell zone with maximum count of elements for given list or pattern of cell zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the cell zone IDs.
        zone_name_list : list[str]
            List containing the cell zone names.
        zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        float

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(zone_name_pattern="*")
        """
        class _get_maxsize_cell_zone_by_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_maxsize_cell_zone_by_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_maxsize_cell_zone_by_countArguments(*args)

    class get_maxsize_cell_zone_by_volume(PyQuery):
        """
        Return cell zone with maximum volume for given list or pattern of cell zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the cell zone IDs.
        zone_name_list : list[str]
            List containing the cell zone names.
        zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        float

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(zone_name_pattern="*")
        """
        class _get_maxsize_cell_zone_by_volumeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_maxsize_cell_zone_by_volumeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_maxsize_cell_zone_by_volumeArguments(*args)

    class get_minsize_face_zone_by_area(PyQuery):
        """
        Return face zone with minimum area for given list or pattern of face zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face zone IDs.
        zone_name_list : list[str]
            List containing the face zone names.
        zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        float

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_minsize_face_zone_by_area(zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_minsize_face_zone_by_area(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_minsize_face_zone_by_area(zone_name_pattern="*")
        """
        class _get_minsize_face_zone_by_areaArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_minsize_face_zone_by_areaArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_minsize_face_zone_by_areaArguments(*args)

    class get_minsize_face_zone_by_count(PyQuery):
        """
        Return face zone with minimum count of elements for given list or pattern of face zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the face zone IDs.
        zone_name_list : list[str]
            List containing the face zone names.
        zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        float

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_minsize_face_zone_by_count(zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_minsize_face_zone_by_count(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_minsize_face_zone_by_count(zone_name_pattern="*")
        """
        class _get_minsize_face_zone_by_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_minsize_face_zone_by_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_minsize_face_zone_by_countArguments(*args)

    class get_multi_faces_count(PyQuery):
        """
        Returns the count of multi-connected faces for the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_multi_faces_count(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.get_multi_faces_count(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.get_multi_faces_count(face_zone_name_pattern="*")
        """
        class _get_multi_faces_countArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_multi_faces_countArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_multi_faces_countArguments(*args)

    class get_node_zones(PyQuery):
        """
        Return a list of zones whose names contain the specified filter string.
        Parameters
        ----------
        filter : str
            Node zone name filter.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_node_zones(filter="*")
        """
        class _get_node_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_node_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_node_zonesArguments(*args)

    class get_objects(PyQuery):
        """
        Return a list of objects of the specified type or whose names contain the specified filter string.
        Parameters
        ----------
        type_name : str
            Mesh object type name.
        filter : str
            Mesh object name filter.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_objects(type_name="mesh")
        >>> meshing_session.meshing_utilities.get_objects(filter="*")
        """
        class _get_objectsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.type_name = self._type_name(self, "type_name", service, rules, path)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _type_name(PyArgumentsTextualSubItem):
                """
                Argument type_name.
                """

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_objectsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_objectsArguments(*args)

    class get_overlapping_face_zones(PyQuery):
        """
        Return a list of overlapping face zones based on the area_tolerance and distance_tolerance specified.
        Parameters
        ----------
        face_zone_name_pattern : str
            Face zone name pattern.
        area_tolerance : float
            Area tolerance.
        distance_tolerance : float
            Distance tolerance.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_overlapping_face_zones(face_zone_name_pattern="*", area_tolerance=0.01, distance_tolerance=0.01)
        """
        class _get_overlapping_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.area_tolerance = self._area_tolerance(self, "area_tolerance", service, rules, path)
                self.distance_tolerance = self._distance_tolerance(self, "distance_tolerance", service, rules, path)

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _area_tolerance(PyArgumentsNumericalSubItem):
                """
                Argument area_tolerance.
                """

            class _distance_tolerance(PyArgumentsNumericalSubItem):
                """
                Argument distance_tolerance.
                """

        def create_instance(self) -> _get_overlapping_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_overlapping_face_zonesArguments(*args)

    class get_pairs_of_overlapping_face_zones(PyQuery):
        """
        - Return the pairs of overlapping face zones based on the join tolerance and feature angle.
        - Specify the tolerance value for locating the overlapping faces (join_tolerance).
        - Choose to use an absolute tolerance value or relative to face edges (set absolute_tolerance to True or False).
        - Specify the feature angle to identify features in the overlap region (feature_angle).
        - The default value is 40.
        - Each member in the list returned includes the zone IDs for the overlapping zone pair and the join region represented by the bounding box.
        - The same pair of zones may appear multiple times (with different join region bounding box coordinates) in the returned list.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        join_tolerance : float
            Join tolerance.
        absolute_tolerance : bool
            Specify whether to use an absolute tolerance value or relative to face edges.
        join_angle : float
            Join angle.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(face_zone_id_list=[29, 30, 31, 32, 33], join_tolerance=0.001, absolute_tolerance=True, join_angle=45)
        >>> meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"], join_tolerance=0.001, absolute_tolerance=True, join_angle=45)
        >>> meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(face_zone_name_pattern="*", join_tolerance=0.001, absolute_tolerance=True, join_angle=45)
        """
        class _get_pairs_of_overlapping_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.join_tolerance = self._join_tolerance(self, "join_tolerance", service, rules, path)
                self.absolute_tolerance = self._absolute_tolerance(self, "absolute_tolerance", service, rules, path)
                self.join_angle = self._join_angle(self, "join_angle", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _join_tolerance(PyArgumentsNumericalSubItem):
                """
                Argument join_tolerance.
                """

            class _absolute_tolerance(PyArgumentsParameterSubItem):
                """
                Argument absolute_tolerance.
                """

            class _join_angle(PyArgumentsNumericalSubItem):
                """
                Argument join_angle.
                """

        def create_instance(self) -> _get_pairs_of_overlapping_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_pairs_of_overlapping_face_zonesArguments(*args)

    class get_prism_cell_zones(PyQuery):
        """
        Return a list of prism cell zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the cell zone IDs.
        zone_name_list : list[str]
            List containing the cell zone names.
        zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_prism_cell_zones(zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_prism_cell_zones(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_prism_cell_zones(zone_name_pattern="*")
        """
        class _get_prism_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_prism_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_prism_cell_zonesArguments(*args)

    class get_region_volume(PyQuery):
        """
        - Get region volume using 1 - object_name and region_name or 2 - object_name and order.
        - Return the region volume for the specified region of an object.
        - Returns a sorted list of volumetric regions by volume for the object specified.
        - Specify the order 'ascending' or 'descending'.
        Parameters
        ----------
        object_name : str
            Mesh object name.
        region_name : str
            Region name.
        sorting_order : str
            Region volume sorting order.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_region_volume(object_name="elbow-fluid", sorting_order="ascending")
        >>> meshing_session.meshing_utilities.get_region_volume(object_name="elbow-fluid", region_name="elbow-fluid")
        """
        class _get_region_volumeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name = self._object_name(self, "object_name", service, rules, path)
                self.region_name = self._region_name(self, "region_name", service, rules, path)
                self.sorting_order = self._sorting_order(self, "sorting_order", service, rules, path)

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

            class _region_name(PyArgumentsTextualSubItem):
                """
                Argument region_name.
                """

            class _sorting_order(PyArgumentsTextualSubItem):
                """
                Argument sorting_order.
                """

        def create_instance(self) -> _get_region_volumeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_region_volumeArguments(*args)

    class get_regions(PyQuery):
        """
        Return a list of regions in the specified object, whose names contain the specified filter string or specified name pattern.
        Parameters
        ----------
        object_name : str
            Mesh object name.
        region_name_pattern : str
            Region name pattern.
        filter : str
            Region name filter.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid", region_name_pattern="*")
        >>> meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid", filter="*")
        >>> meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid")
        """
        class _get_regionsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.object_name = self._object_name(self, "object_name", service, rules, path)
                self.region_name_pattern = self._region_name_pattern(self, "region_name_pattern", service, rules, path)
                self.filter = self._filter(self, "filter", service, rules, path)

            class _object_name(PyArgumentsTextualSubItem):
                """
                Argument object_name.
                """

            class _region_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument region_name_pattern.
                """

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

        def create_instance(self) -> _get_regionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_regionsArguments(*args)

    class get_regions_of_face_zones(PyQuery):
        """
        Return a list of regions containing the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[str]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_regions_of_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_regions_of_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_regions_of_face_zones(face_zone_name_pattern="*")
        """
        class _get_regions_of_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_regions_of_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_regions_of_face_zonesArguments(*args)

    class get_shared_boundary_face_zones_for_given_cell_zones(PyQuery):
        """
        Returns the number of faces and the boundary face zones that are shared with the specified cell zones.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")
        """
        class _get_shared_boundary_face_zones_for_given_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _get_shared_boundary_face_zones_for_given_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_shared_boundary_face_zones_for_given_cell_zonesArguments(*args)

    class get_tet_cell_zones(PyQuery):
        """
        Return a list of tet cell zones.
        Parameters
        ----------
        zone_id_list : list[int]
            List containing the cell zone IDs.
        zone_name_list : list[str]
            List containing the cell zone names.
        zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_tet_cell_zones(zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_tet_cell_zones(zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_tet_cell_zones(zone_name_pattern="*")
        """
        class _get_tet_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id_list = self._zone_id_list(self, "zone_id_list", service, rules, path)
                self.zone_name_list = self._zone_name_list(self, "zone_name_list", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument zone_id_list.
                """

            class _zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument zone_name_list.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_tet_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_tet_cell_zonesArguments(*args)

    class get_unreferenced_cell_zones(PyQuery):
        """
        Return a list of unreferenced cell zones by ID, whose names contain the specified pattern or filter.
        Parameters
        ----------
        filter : str
            Cell zone name filter.
        zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_unreferenced_cell_zones()
        >>> meshing_session.meshing_utilities.get_unreferenced_cell_zones(filter="*")
        >>> meshing_session.meshing_utilities.get_unreferenced_cell_zones(zone_name_pattern="*")
        """
        class _get_unreferenced_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.filter = self._filter(self, "filter", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_unreferenced_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_unreferenced_cell_zonesArguments(*args)

    class get_unreferenced_edge_zones(PyQuery):
        """
        Return a list of unreferenced edge zones by ID, whose names contain the specified pattern or filter.
        Parameters
        ----------
        filter : str
            Edge zone name filter.
        zone_name_pattern : str
            Edge zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_unreferenced_edge_zones()
        >>> meshing_session.meshing_utilities.get_unreferenced_edge_zones(filter="*")
        >>> meshing_session.meshing_utilities.get_unreferenced_edge_zones(zone_name_pattern="*")
        """
        class _get_unreferenced_edge_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.filter = self._filter(self, "filter", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_unreferenced_edge_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_unreferenced_edge_zonesArguments(*args)

    class get_unreferenced_face_zones(PyQuery):
        """
        Return a list of unreferenced face zones by ID, whose names contain the specified pattern or filter.
        Parameters
        ----------
        filter : str
            Face zone name filter.
        zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_unreferenced_face_zones()
        >>> meshing_session.meshing_utilities.get_unreferenced_face_zones(filter="*")
        >>> meshing_session.meshing_utilities.get_unreferenced_face_zones(zone_name_pattern="*")
        """
        class _get_unreferenced_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.filter = self._filter(self, "filter", service, rules, path)
                self.zone_name_pattern = self._zone_name_pattern(self, "zone_name_pattern", service, rules, path)

            class _filter(PyArgumentsTextualSubItem):
                """
                Argument filter.
                """

            class _zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument zone_name_pattern.
                """

        def create_instance(self) -> _get_unreferenced_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_unreferenced_face_zonesArguments(*args)

    class get_wrapped_face_zones(PyQuery):
        """
        Return a list of wrapped face zones.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_wrapped_face_zones()
        """
        class _get_wrapped_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _get_wrapped_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_wrapped_face_zonesArguments(*args)

    class get_zone_type(PyQuery):
        """
        Return zone type as integer.
        Parameters
        ----------
        zone_id : int
            Zone ID.
        zone_name : str
            Zone name.

        Returns
        -------
        str

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_zone_type(zone_id=87)
        >>> meshing_session.meshing_utilities.get_zone_type(zone_name="elbow-fluid")
        """
        class _get_zone_typeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.zone_name = self._zone_name(self, "zone_name", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _zone_name(PyArgumentsTextualSubItem):
                """
                Argument zone_name.
                """

        def create_instance(self) -> _get_zone_typeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_zone_typeArguments(*args)

    class get_zones(PyQuery):
        """
        Return a list of zones of the specified default zone type, group or user-defined group.
        Parameters
        ----------
        type_name : str
            Zone type name.
        group_name : str
            Zone group name.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_zones(type_name="velocity-inlet")
        >>> meshing_session.meshing_utilities.get_zones(group_name="inlet")
        """
        class _get_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.type_name = self._type_name(self, "type_name", service, rules, path)
                self.group_name = self._group_name(self, "group_name", service, rules, path)

            class _type_name(PyArgumentsTextualSubItem):
                """
                Argument type_name.
                """

            class _group_name(PyArgumentsTextualSubItem):
                """
                Argument group_name.
                """

        def create_instance(self) -> _get_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_zonesArguments(*args)

    class get_zones_with_free_faces_for_given_face_zones(PyQuery):
        """
        Return a list of zones with free faces for the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(face_zone_id_list=[face_zone_name_pattern="*"])
        """
        class _get_zones_with_free_faces_for_given_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_zones_with_free_faces_for_given_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_zones_with_free_faces_for_given_face_zonesArguments(*args)

    class get_zones_with_marked_faces_for_given_face_zones(PyQuery):
        """
        Return a list of zones with marked faces for the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(face_zone_id_list=[face_zone_name_pattern="*"])
        """
        class _get_zones_with_marked_faces_for_given_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_zones_with_marked_faces_for_given_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_zones_with_marked_faces_for_given_face_zonesArguments(*args)

    class get_zones_with_multi_faces_for_given_face_zones(PyQuery):
        """
        Return a list of zones with multi-connected faces for the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        list[int]

        Examples
        --------
        >>> meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])
        >>> meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])
        >>> meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(face_zone_id_list=[face_zone_name_pattern="*"])
        """
        class _get_zones_with_multi_faces_for_given_face_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _get_zones_with_multi_faces_for_given_face_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._get_zones_with_multi_faces_for_given_face_zonesArguments(*args)

    class interior_zone_exists(PyQuery):
        """
        Report if the interior face zone exists.
        Parameters
        ----------
        zone_id : int
            Zone ID.
        zone_name : str
            Zone name.

        Returns
        -------
        bool

        Examples
        --------
        >>> meshing_session.meshing_utilities.interior_zone_exists(zone_id=31)
        >>> meshing_session.meshing_utilities.interior_zone_exists(zone_name="wall-inlet")
        """
        class _interior_zone_existsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.zone_name = self._zone_name(self, "zone_name", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _zone_name(PyArgumentsTextualSubItem):
                """
                Argument zone_name.
                """

        def create_instance(self) -> _interior_zone_existsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._interior_zone_existsArguments(*args)

    class mark_bad_quality_faces(PyQuery):
        """
        Mark bad quality faces on the boundary face zones specified, based on the quality limit (quality_limit) and number of rings (number_of_rings).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        quality_limit : float
            Quality limit.
        number_of_rings : int
            Number of rings.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_id_list=[30, 31, 32], quality_limit=0.5, number_of_rings=2)
        >>> meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], quality_limit=0.5, number_of_rings=2)
        >>> meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_name_pattern="*", quality_limit=0.5, number_of_rings=2)
        """
        class _mark_bad_quality_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.quality_limit = self._quality_limit(self, "quality_limit", service, rules, path)
                self.number_of_rings = self._number_of_rings(self, "number_of_rings", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _quality_limit(PyArgumentsNumericalSubItem):
                """
                Argument quality_limit.
                """

            class _number_of_rings(PyArgumentsNumericalSubItem):
                """
                Argument number_of_rings.
                """

        def create_instance(self) -> _mark_bad_quality_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_bad_quality_facesArguments(*args)

    class mark_duplicate_faces(PyQuery):
        """
        Mark duplicate faces on the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_duplicate_faces(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.mark_duplicate_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.mark_duplicate_faces(face_zone_name_pattern="*")
        """
        class _mark_duplicate_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _mark_duplicate_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_duplicate_facesArguments(*args)

    class mark_face_strips_by_height_and_quality(PyQuery):
        """
        - Mark face strips based on the strip_type, strip_height, quality_measure, quality_limit, and feature_angle specified.
        - Possible values for strip_type are 1, 2, 3 and 4.
        - 1 - 'boundary-boundary' strip, multi-connected face edges are also considered as boundary here.
        - 2 - feature-feature strip between angle based features, feature edges, multi-connected edges, and free edges are angle based features and boundary edges will be considered features if there is an angle.
        - 3 - 'all-all' strip between all boundaries and features.
        - 4 - 'pure feature-feature' strip, only pure features, boundary edges and multi edges will not be considered as pure feature edges even if there is an angle based feature.
        - The recommended value is 2.
        - Specify the 'quality_measure' as one of the 'Skewness', 'Size Change', 'Edge Ratio', 'Area', 'Aspect Ratio', 'Warp', 'Dihedral Angle', 'Ortho Skew' value.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        strip_type : int
            Strip type.
        strip_height : float
            Strip height.
        quality_measure : str
            Quality measure.
        quality_limit : float
            Quality limit.
        feature_angle : float
            Feature angle.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(face_zone_id_list=[30, 31, 32], strip_type=2, strip_height=2, quality_measure="Size Change", quality_limit=0.5, feature_angle=40)
        >>> meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], strip_type=2, strip_height=2, quality_measure="Size Change", quality_limit=0.5, feature_angle=40)
        >>> meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(face_zone_name_pattern="cold*", strip_type=2, strip_height=2, quality_measure="Size Change", quality_limit=0.5, feature_angle=40)
        """
        class _mark_face_strips_by_height_and_qualityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.strip_type = self._strip_type(self, "strip_type", service, rules, path)
                self.strip_height = self._strip_height(self, "strip_height", service, rules, path)
                self.quality_measure = self._quality_measure(self, "quality_measure", service, rules, path)
                self.quality_limit = self._quality_limit(self, "quality_limit", service, rules, path)
                self.feature_angle = self._feature_angle(self, "feature_angle", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _strip_type(PyArgumentsNumericalSubItem):
                """
                Argument strip_type.
                """

            class _strip_height(PyArgumentsNumericalSubItem):
                """
                Argument strip_height.
                """

            class _quality_measure(PyArgumentsTextualSubItem):
                """
                Argument quality_measure.
                """

            class _quality_limit(PyArgumentsNumericalSubItem):
                """
                Argument quality_limit.
                """

            class _feature_angle(PyArgumentsNumericalSubItem):
                """
                Argument feature_angle.
                """

        def create_instance(self) -> _mark_face_strips_by_height_and_qualityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_face_strips_by_height_and_qualityArguments(*args)

    class mark_faces_by_quality(PyQuery):
        """
        - Mark faces based on the 'quality_measure' and 'quality_limit' specified.
        - Specify whether to append the faces to those previously marked or clear previously marked faces (append_marking set to True or False).
        - Specify the 'quality_measure' as one of the 'Skewness', 'Size Change', 'Edge Ratio', 'Area', 'Aspect Ratio', 'Warp', 'Dihedral Angle', 'Ortho Skew' value.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        quality_measure : str
            Quality measure.
        quality_limit : float
            Quality limit.
        append_marking : bool
            Specify whether to append the faces to those previously marked or clear previously marked faces.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_faces_by_quality(face_zone_id_list=[30, 31, 32], quality_measure="Skewness", quality_limit=0.9, append_marking=False)
        >>> meshing_session.meshing_utilities.mark_faces_by_quality(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], quality_measure="Skewness", quality_limit=0.9, append_marking=False)
        >>> meshing_session.meshing_utilities.mark_faces_by_quality(face_zone_name_pattern="*", quality_measure="Skewness", quality_limit=0.9, append_marking=False)
        """
        class _mark_faces_by_qualityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.quality_measure = self._quality_measure(self, "quality_measure", service, rules, path)
                self.quality_limit = self._quality_limit(self, "quality_limit", service, rules, path)
                self.append_marking = self._append_marking(self, "append_marking", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _quality_measure(PyArgumentsTextualSubItem):
                """
                Argument quality_measure.
                """

            class _quality_limit(PyArgumentsNumericalSubItem):
                """
                Argument quality_limit.
                """

            class _append_marking(PyArgumentsParameterSubItem):
                """
                Argument append_marking.
                """

        def create_instance(self) -> _mark_faces_by_qualityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_faces_by_qualityArguments(*args)

    class mark_faces_deviating_from_size_field(PyQuery):
        """
        - Mark all faces at nodes based on deviation from the size field.
        - Specify the size field type to be used to get size at node.
        - Set 'size_factor_type_to_compare' to 'volumetric' or 'geodesic'.
        - Faces will be marked if the minimum edge length at the node is less than min_size_factor × size_factor_type_to_compare or the maximum edge length is greater than max_size_factor × size_factor_type_to_compare.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        min_size_factor : float
            Minimum size factor.
        max_size_factor : float
            Maximum size factor.
        size_factor_type_to_compare : str
            Size field type to be used to get size at node.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(face_zone_id_list=[30, 31, 32], min_size_factor=0.5, max_size_factor=1.1, size_factor_type_to_compare="geodesic")
        >>> meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(face_zone_name_list=["cold-inlet", "hot-inlet"] min_size_factor=0.5, max_size_factor=1.1, size_factor_type_to_compare="geodesic")
        >>> meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(face_zone_name_pattern="*", min_size_factor=0.5, max_size_factor=1.1, size_factor_type_to_compare="geodesic")
        """
        class _mark_faces_deviating_from_size_fieldArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.min_size_factor = self._min_size_factor(self, "min_size_factor", service, rules, path)
                self.max_size_factor = self._max_size_factor(self, "max_size_factor", service, rules, path)
                self.size_factor_type_to_compare = self._size_factor_type_to_compare(self, "size_factor_type_to_compare", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _min_size_factor(PyArgumentsNumericalSubItem):
                """
                Argument min_size_factor.
                """

            class _max_size_factor(PyArgumentsNumericalSubItem):
                """
                Argument max_size_factor.
                """

            class _size_factor_type_to_compare(PyArgumentsTextualSubItem):
                """
                Argument size_factor_type_to_compare.
                """

        def create_instance(self) -> _mark_faces_deviating_from_size_fieldArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_faces_deviating_from_size_fieldArguments(*args)

    class mark_faces_in_self_proximity(PyQuery):
        """
        - Mark faces in self-proximity on the face zones specified.
        - Specify whether to use relative tolerance (relative_tolerance set to True or False), tolerance value, the angle, and whether to ignore orientation (ignore_orientation set to True or False).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        relative_tolerance : bool
            Specify whether to use relative tolerance.
        tolerance : float
            Tolerance.
        proximity_angle : float
            Proximity angle.
        ignore_orientation : bool
            Specify whether to ignore orientation.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_faces_in_self_proximity(face_zone_id_list=[30, 31, 32], relative_tolerance=True, tolerance=0.05, proximity_angle=40.5, ignore_orientation=False)
        >>> meshing_session.meshing_utilities.mark_faces_in_self_proximity(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], relative_tolerance=True, tolerance=0.05, proximity_angle=40.5, ignore_orientation=False)
        >>> meshing_session.meshing_utilities.mark_faces_in_self_proximity(face_zone_name_pattern="*", relative_tolerance=True, tolerance=0.05, proximity_angle=40.5, ignore_orientation=False)
        """
        class _mark_faces_in_self_proximityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.relative_tolerance = self._relative_tolerance(self, "relative_tolerance", service, rules, path)
                self.tolerance = self._tolerance(self, "tolerance", service, rules, path)
                self.proximity_angle = self._proximity_angle(self, "proximity_angle", service, rules, path)
                self.ignore_orientation = self._ignore_orientation(self, "ignore_orientation", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _relative_tolerance(PyArgumentsParameterSubItem):
                """
                Argument relative_tolerance.
                """

            class _tolerance(PyArgumentsNumericalSubItem):
                """
                Argument tolerance.
                """

            class _proximity_angle(PyArgumentsNumericalSubItem):
                """
                Argument proximity_angle.
                """

            class _ignore_orientation(PyArgumentsParameterSubItem):
                """
                Argument ignore_orientation.
                """

        def create_instance(self) -> _mark_faces_in_self_proximityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_faces_in_self_proximityArguments(*args)

    class mark_faces_using_node_degree(PyQuery):
        """
        - Mark all faces with node degree above the specified threshold.
        - Node degree is defined as the number of edges connected to the node.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        node_degree_threshold : int
            Number of edges connected to the node.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_faces_using_node_degree(face_zone_id_list=[30, 31, 32], node_degree_threshold=2)
        >>> meshing_session.meshing_utilities.mark_faces_using_node_degree(face_zone_name_list=["cold-inlet", "hot-inlet"], node_degree_threshold=2)
        >>> meshing_session.meshing_utilities.mark_faces_using_node_degree(face_zone_name_pattern="*", node_degree_threshold=2)
        """
        class _mark_faces_using_node_degreeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.node_degree_threshold = self._node_degree_threshold(self, "node_degree_threshold", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _node_degree_threshold(PyArgumentsNumericalSubItem):
                """
                Argument node_degree_threshold.
                """

        def create_instance(self) -> _mark_faces_using_node_degreeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_faces_using_node_degreeArguments(*args)

    class mark_free_faces(PyQuery):
        """
        Mark free faces on the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_free_faces(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.mark_free_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.mark_free_faces(face_zone_name_pattern="*")
        """
        class _mark_free_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _mark_free_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_free_facesArguments(*args)

    class mark_invalid_normals(PyQuery):
        """
        Mark invalid normal locations on the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_invalid_normals(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.mark_invalid_normals(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.mark_invalid_normals(face_zone_name_pattern="*")
        """
        class _mark_invalid_normalsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _mark_invalid_normalsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_invalid_normalsArguments(*args)

    class mark_island_faces(PyQuery):
        """
        Mark island faces on the face zones specified, based on the island face count (island_face_count).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        island_face_count : int
            Island face count.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_island_faces(face_zone_id_list=[30, 31, 32], island_face_count=5)
        >>> meshing_session.meshing_utilities.mark_island_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], island_face_count=5)
        >>> meshing_session.meshing_utilities.mark_island_faces(face_zone_name_pattern="cold*", island_face_count=5)
        """
        class _mark_island_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.island_face_count = self._island_face_count(self, "island_face_count", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _island_face_count(PyArgumentsNumericalSubItem):
                """
                Argument island_face_count.
                """

        def create_instance(self) -> _mark_island_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_island_facesArguments(*args)

    class mark_multi_faces(PyQuery):
        """
        Mark multi-connected faces on the face zones specified based on fringe length (fringe_length).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        fringe_length : int
            Fringe length.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_multi_faces(face_zone_id_list=[30, 31, 32], fringe_length=5)
        >>> meshing_session.meshing_utilities.mark_multi_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], fringe_length=5)
        >>> meshing_session.meshing_utilities.mark_multi_faces(face_zone_name_pattern="cold*", fringe_length=5)
        """
        class _mark_multi_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.fringe_length = self._fringe_length(self, "fringe_length", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _fringe_length(PyArgumentsNumericalSubItem):
                """
                Argument fringe_length.
                """

        def create_instance(self) -> _mark_multi_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_multi_facesArguments(*args)

    class mark_point_contacts(PyQuery):
        """
        Mark point contact locations on the face zones specified.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_point_contacts(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.mark_point_contacts(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.mark_point_contacts(face_zone_name_pattern="cold*")
        """
        class _mark_point_contactsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _mark_point_contactsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_point_contactsArguments(*args)

    class mark_self_intersecting_faces(PyQuery):
        """
        - Mark self-intersecting faces on the face zones specified.
        - Specify whether to mark folded faces or not (mark_folded set to True or False).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        mark_folded : bool
            Specify whether to mark folded faces or not.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_self_intersecting_faces(face_zone_id_list=[30, 31, 32], mark_folded=True)
        >>> meshing_session.meshing_utilities.mark_self_intersecting_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], mark_folded=True)
        >>> meshing_session.meshing_utilities.mark_self_intersecting_faces(face_zone_name_pattern="cold*", mark_folded=True)
        """
        class _mark_self_intersecting_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.mark_folded = self._mark_folded(self, "mark_folded", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _mark_folded(PyArgumentsParameterSubItem):
                """
                Argument mark_folded.
                """

        def create_instance(self) -> _mark_self_intersecting_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_self_intersecting_facesArguments(*args)

    class mark_sliver_faces(PyQuery):
        """
        Mark sliver faces on the face zones specified, based on the maximum height (max_height) and skewness limit (skew_limit).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        max_height : float
            Maximum height.
        skew_limit : float
            Skew limit.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_sliver_faces(face_zone_id_list=[30, 31, 32], max_height=2, skew_limit=0.2)
        >>> meshing_session.meshing_utilities.mark_sliver_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], max_height=2, skew_limit=0.2)
        >>> meshing_session.meshing_utilities.mark_sliver_faces(face_zone_name_pattern="cold*", max_height=2, skew_limit=0.2)
        """
        class _mark_sliver_facesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.max_height = self._max_height(self, "max_height", service, rules, path)
                self.skew_limit = self._skew_limit(self, "skew_limit", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _max_height(PyArgumentsNumericalSubItem):
                """
                Argument max_height.
                """

            class _skew_limit(PyArgumentsNumericalSubItem):
                """
                Argument skew_limit.
                """

        def create_instance(self) -> _mark_sliver_facesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_sliver_facesArguments(*args)

    class mark_spikes(PyQuery):
        """
        Mark spikes on the face zones specified, based on the spike angle (spike_angle).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        spike_angle : float
            Spike angle.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_spikes(face_zone_id_list=[30, 31, 32], spike_angle=40.5)
        >>> meshing_session.meshing_utilities.mark_spikes(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], spike_angle=40.5)
        >>> meshing_session.meshing_utilities.mark_spikes(face_zone_name_pattern="cold*", spike_angle=40.5)
        """
        class _mark_spikesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.spike_angle = self._spike_angle(self, "spike_angle", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _spike_angle(PyArgumentsNumericalSubItem):
                """
                Argument spike_angle.
                """

        def create_instance(self) -> _mark_spikesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_spikesArguments(*args)

    class mark_steps(PyQuery):
        """
        Mark steps on the face zones specified, based on the step angle (step_angle) and step width (step_width).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        step_angle : float
            Step angle.
        step_width : float
            Step width.

        Returns
        -------
        int

        Examples
        --------
        >>> meshing_session.meshing_utilities.mark_steps(face_zone_id_list=[30, 31, 32], step_angle=40.5, step_width=3.3)
        >>> meshing_session.meshing_utilities.mark_steps(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], step_angle=40.5, step_width=3.3)
        >>> meshing_session.meshing_utilities.mark_steps(face_zone_name_pattern="cold*", step_angle=40.5, step_width=3.3)
        """
        class _mark_stepsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.step_angle = self._step_angle(self, "step_angle", service, rules, path)
                self.step_width = self._step_width(self, "step_width", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _step_angle(PyArgumentsNumericalSubItem):
                """
                Argument step_angle.
                """

            class _step_width(PyArgumentsNumericalSubItem):
                """
                Argument step_width.
                """

        def create_instance(self) -> _mark_stepsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mark_stepsArguments(*args)

    class mesh_check(PyQuery):
        """
        - Reports the selected mesh check statistics for the zones specified.
        - Specify the 'type_name' as one of the 'bounding-box-statistics', 'volume-statistics', 'face-area-statistics', 'nodes-per-edge', 'nodes-per-face', 'nodes-per-cell', 'faces-or-neighbors-per-cell', 'cell-faces-or-neighbors', 'isolated-cells', 'face-handedness', 'periodic-face-pairs', 'face-children', 'zone-boundary-conditions', 'invalid-node-coordinates', 'poly-cells', 'parallel-invalid-zones', 'parallel-invalid-neighborhood', 'parallel-invalid-interfaces' value.
        Parameters
        ----------
        type_name : str
            Type name.
        edge_zone_id_list : list[int]
            List containing the edge zone IDs.
        edge_zone_name_list : list[str]
            List containing the edge zone names.
        edge_zone_name_pattern : str
            Edge zone name pattern.
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mesh_check(type_name="face-children", edge_zone_id_list=[22, 23], face_zone_id_list=[30, 31, 32], cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.mesh_check(type_name="nodes-per-cell", edge_zone_name_pattern="cold-inlet*", face_zone_id_list=[30, 31, 32], cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.mesh_check(type_name="volume-statistics", edge_zone_id_list=[22, 23], face_zone_name_pattern="*", cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.mesh_check(type_name="nodes-per-cell", edge_zone_name_pattern="cold-inlet*", face_zone_name_pattern="*", cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.mesh_check(type_name="face-children", edge_zone_id_list=[22, 23], face_zone_id_list=[30, 31, 32], cell_zone_name_pattern="*")
        >>> meshing_session.meshing_utilities.mesh_check(type_name="volume-statistics", edge_zone_name_pattern="cold-inlet*", face_zone_name_pattern="*", cell_zone_name_pattern="*")
        """
        class _mesh_checkArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.type_name = self._type_name(self, "type_name", service, rules, path)
                self.edge_zone_id_list = self._edge_zone_id_list(self, "edge_zone_id_list", service, rules, path)
                self.edge_zone_name_list = self._edge_zone_name_list(self, "edge_zone_name_list", service, rules, path)
                self.edge_zone_name_pattern = self._edge_zone_name_pattern(self, "edge_zone_name_pattern", service, rules, path)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _type_name(PyArgumentsTextualSubItem):
                """
                Argument type_name.
                """

            class _edge_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument edge_zone_id_list.
                """

            class _edge_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_list.
                """

            class _edge_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument edge_zone_name_pattern.
                """

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _mesh_checkArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mesh_checkArguments(*args)

    class mesh_exists(PyQuery):
        """
        Report if the volume mesh exists.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.mesh_exists()
        """
        class _mesh_existsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _mesh_existsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._mesh_existsArguments(*args)

    class print_worst_quality_cell(PyQuery):
        """
        - Report the worst quality cell (ID and location) for the cell zones based on the measure specified.
        - Specify the 'measure' as one of the 'Orthogonal Quality', 'Skewness', 'Equiangle Skewness', 'Size Change', 'Edge Ratio', 'Size', 'Aspect Ratio', 'Squish', 'Warp', 'Dihedral Angle', 'ICEMCFD Quality', 'Ortho Skew', 'FLUENT Aspect Ratio', 'Inverse Orthogonal Quality' value.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        measure : str
            Measure.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_id_list=[87], measure="Orthogonal Quality")
        >>> meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality")
        >>> meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_name_pattern="*", measure="Orthogonal Quality")
        """
        class _print_worst_quality_cellArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.measure = self._measure(self, "measure", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _measure(PyArgumentsTextualSubItem):
                """
                Argument measure.
                """

        def create_instance(self) -> _print_worst_quality_cellArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._print_worst_quality_cellArguments(*args)

    class project_zone_on_plane(PyQuery):
        """
        - Project a zone on the plane specified.
        - Specify three points for defining the plane.
        Parameters
        ----------
        zone_id : int
            Zone ID.
        plane : dict[str, Any]

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.project_zone_on_plane(zone_id=87, plane=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        """
        class _project_zone_on_planeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.zone_id = self._zone_id(self, "zone_id", service, rules, path)
                self.plane = self._plane(self, "plane", service, rules, path)

            class _zone_id(PyArgumentsNumericalSubItem):
                """
                Argument zone_id.
                """

            class _plane(PyArgumentsSingletonSubItem):
                """
                Argument plane.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.p2 = self._p2(self, "p2", service, rules, path)
                    self.p3 = self._p3(self, "p3", service, rules, path)
                    self.p1 = self._p1(self, "p1", service, rules, path)

                class _p2(PyArgumentsNumericalSubItem):
                    """
                    Argument p2.
                    """

                class _p3(PyArgumentsNumericalSubItem):
                    """
                    Argument p3.
                    """

                class _p1(PyArgumentsNumericalSubItem):
                    """
                    Argument p1.
                    """

        def create_instance(self) -> _project_zone_on_planeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._project_zone_on_planeArguments(*args)

    class refine_marked_faces_in_zones(PyQuery):
        """
        Refine marked faces.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.refine_marked_faces_in_zones(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.refine_marked_faces_in_zones(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.refine_marked_faces_in_zones(face_zone_name_pattern="cold*")
        """
        class _refine_marked_faces_in_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _refine_marked_faces_in_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._refine_marked_faces_in_zonesArguments(*args)

    class scale_cell_zones_around_pivot(PyQuery):
        """
        - Enables you to scale the cell zones around a pivot point or the bounding box center.
        - Specify the cell zones, the scale factors in the X, Y, Z directions (scale), the pivot point (pivot), and choose whether to use the bounding box center (use_bbox_center set to True or False).
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.
        scale : list[float]
            Scale factors in the X, Y, Z directions.
        pivot : list[float]
            Pivot point.
        use_bbox_center : bool
            Specify whether to use the bounding box center.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.scale_cell_zones_around_pivot(cell_zone_id_list=[87], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)
        >>> meshing_session.meshing_utilities.scale_cell_zones_around_pivot(cell_zone_name_list=["elbow-fluid"], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)
        >>> meshing_session.meshing_utilities.scale_cell_zones_around_pivot(cell_zone_name_pattern="*", scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)
        """
        class _scale_cell_zones_around_pivotArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)
                self.scale = self._scale(self, "scale", service, rules, path)
                self.pivot = self._pivot(self, "pivot", service, rules, path)
                self.use_bbox_center = self._use_bbox_center(self, "use_bbox_center", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

            class _scale(PyArgumentsNumericalSubItem):
                """
                Argument scale.
                """

            class _pivot(PyArgumentsNumericalSubItem):
                """
                Argument pivot.
                """

            class _use_bbox_center(PyArgumentsParameterSubItem):
                """
                Argument use_bbox_center.
                """

        def create_instance(self) -> _scale_cell_zones_around_pivotArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._scale_cell_zones_around_pivotArguments(*args)

    class scale_face_zones_around_pivot(PyQuery):
        """
        - Enables you to scale the face zones around a pivot point or the bounding box center.
        - Specify the face zones, the scale factors in the X, Y, Z directions (scale), the pivot point (pivot), and choose whether to use the bounding box center (use_bbox_center set to True or False).
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        scale : list[float]
            Scale factors in the X, Y, Z directions.
        pivot : list[float]
            Pivot point.
        use_bbox_center : bool
            Specify whether to use the bounding box center.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.scale_face_zones_around_pivot(face_zone_id_list=[30, 31, 32], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)
        >>> meshing_session.meshing_utilities.scale_face_zones_around_pivot(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)
        >>> meshing_session.meshing_utilities.scale_face_zones_around_pivot(face_zone_name_pattern="*", scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)
        """
        class _scale_face_zones_around_pivotArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.scale = self._scale(self, "scale", service, rules, path)
                self.pivot = self._pivot(self, "pivot", service, rules, path)
                self.use_bbox_center = self._use_bbox_center(self, "use_bbox_center", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _scale(PyArgumentsNumericalSubItem):
                """
                Argument scale.
                """

            class _pivot(PyArgumentsNumericalSubItem):
                """
                Argument pivot.
                """

            class _use_bbox_center(PyArgumentsParameterSubItem):
                """
                Argument use_bbox_center.
                """

        def create_instance(self) -> _scale_face_zones_around_pivotArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._scale_face_zones_around_pivotArguments(*args)

    class separate_cell_zone_layers_by_face_zone_using_id(PyQuery):
        """
        - Separates cells that are connected to specified face zones into another cell zone.
        - This separation method applies only to prism cells.
        - Specify the number of layers of cells (nlayers) to be separated.
        Parameters
        ----------
        cell_zone_id : int
            Cell zone ID.
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        nlayers : int
            Number of layers of cells to be separated.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87, face_zone_id_list=[30, 31, 32], nlayers=2)
        >>> meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87, face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], nlayers=2)
        >>> meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87, face_zone_name_pattern="*", nlayers=2)
        """
        class _separate_cell_zone_layers_by_face_zone_using_idArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id = self._cell_zone_id(self, "cell_zone_id", service, rules, path)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.nlayers = self._nlayers(self, "nlayers", service, rules, path)

            class _cell_zone_id(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id.
                """

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _nlayers(PyArgumentsNumericalSubItem):
                """
                Argument nlayers.
                """

        def create_instance(self) -> _separate_cell_zone_layers_by_face_zone_using_idArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._separate_cell_zone_layers_by_face_zone_using_idArguments(*args)

    class separate_cell_zone_layers_by_face_zone_using_name(PyQuery):
        """
        - Separates cells that are connected to specified face zones into another cell zone.
        - This separation method applies only to prism cells.
        - Specify the number of layers of cells (nlayers) to be separated.
        Parameters
        ----------
        cell_zone_name : str
            Cell zone name.
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.
        nlayers : int
            Number of layers of cells to be separated.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid", face_zone_id_list=[30, 31, 32], nlayers=2)
        >>> meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid", face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], nlayers=2)
        >>> meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid", face_zone_name_pattern="*", nlayers=2)
        """
        class _separate_cell_zone_layers_by_face_zone_using_nameArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_name = self._cell_zone_name(self, "cell_zone_name", service, rules, path)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)
                self.nlayers = self._nlayers(self, "nlayers", service, rules, path)

            class _cell_zone_name(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name.
                """

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

            class _nlayers(PyArgumentsNumericalSubItem):
                """
                Argument nlayers.
                """

        def create_instance(self) -> _separate_cell_zone_layers_by_face_zone_using_nameArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._separate_cell_zone_layers_by_face_zone_using_nameArguments(*args)

    class separate_face_zones_by_cell_neighbor(PyQuery):
        """
        Separate face zones based on the cell neighbors.
        Parameters
        ----------
        face_zone_id_list : list[int]
            List containing the face zone IDs.
        face_zone_name_list : list[str]
            List containing the face zone names.
        face_zone_name_pattern : str
            Face zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(face_zone_id_list=[30, 31, 32])
        >>> meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])
        >>> meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(face_zone_name_pattern="cold*")
        """
        class _separate_face_zones_by_cell_neighborArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.face_zone_id_list = self._face_zone_id_list(self, "face_zone_id_list", service, rules, path)
                self.face_zone_name_list = self._face_zone_name_list(self, "face_zone_name_list", service, rules, path)
                self.face_zone_name_pattern = self._face_zone_name_pattern(self, "face_zone_name_pattern", service, rules, path)

            class _face_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument face_zone_id_list.
                """

            class _face_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_list.
                """

            class _face_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument face_zone_name_pattern.
                """

        def create_instance(self) -> _separate_face_zones_by_cell_neighborArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._separate_face_zones_by_cell_neighborArguments(*args)

    class unpreserve_cell_zones(PyQuery):
        """
        Enables you to unpreserve some/all preserved cell zones during the meshing process.
        Parameters
        ----------
        cell_zone_id_list : list[int]
            List containing the cell zone IDs.
        cell_zone_name_list : list[str]
            List containing the cell zone names.
        cell_zone_name_pattern : str
            Cell zone name pattern.

        Returns
        -------
        None

        Examples
        --------
        >>> meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_id_list=[87])
        >>> meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_name_list=["elbow-fluid"])
        >>> meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_name_pattern="*")
        """
        class _unpreserve_cell_zonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.cell_zone_id_list = self._cell_zone_id_list(self, "cell_zone_id_list", service, rules, path)
                self.cell_zone_name_list = self._cell_zone_name_list(self, "cell_zone_name_list", service, rules, path)
                self.cell_zone_name_pattern = self._cell_zone_name_pattern(self, "cell_zone_name_pattern", service, rules, path)

            class _cell_zone_id_list(PyArgumentsNumericalSubItem):
                """
                Argument cell_zone_id_list.
                """

            class _cell_zone_name_list(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_list.
                """

            class _cell_zone_name_pattern(PyArgumentsTextualSubItem):
                """
                Argument cell_zone_name_pattern.
                """

        def create_instance(self) -> _unpreserve_cell_zonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._unpreserve_cell_zonesArguments(*args)

