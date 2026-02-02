#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import PyMenu
from typing import Any


class Root(PyMenu):

    def add_labels_on_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def add_labels_on_edge_zones(
        self,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        edge_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def add_labels_on_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def clean_face_zone_names(
        self,
        ) -> None: ...

    def delete_all_sub_domains(
        self,
        ) -> None: ...

    def delete_empty_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def delete_empty_edge_zones(
        self,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        edge_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def delete_empty_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def delete_empty_zones(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def delete_marked_faces_in_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def merge_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> None: ...

    def merge_cell_zones_with_same_prefix(
        self,
        prefix: str | None = None,
        ) -> None: ...

    def merge_cell_zones_with_same_suffix(
        self,
        suffix: str | None = None,
        ) -> None: ...

    def merge_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> None: ...

    def merge_face_zones_of_type(
        self,
        face_zone_type: str | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> None: ...

    def merge_face_zones_with_same_prefix(
        self,
        prefix: str | None = None,
        ) -> None: ...

    def remove_id_suffix_from_face_zones(
        self,
        ) -> None: ...

    def remove_ids_from_zone_names(
        self,
        zone_id_list: list[int] | None = None,
        ) -> bool: ...

    def remove_labels_on_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> None: ...

    def remove_labels_on_edge_zones(
        self,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        edge_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> None: ...

    def remove_labels_on_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> None: ...

    def rename_edge_zone(
        self,
        zone_id: int | None = None,
        zone_name: str | None = None,
        new_name: str | None = None,
        ) -> bool: ...

    def rename_face_zone(
        self,
        zone_id: int | None = None,
        zone_name: str | None = None,
        new_name: str | None = None,
        ) -> bool: ...

    def rename_face_zone_label(
        self,
        object_name: str | None = None,
        old_label_name: str | None = None,
        new_label_name: str | None = None,
        ) -> None: ...

    def rename_object(
        self,
        old_object_name: str | None = None,
        new_object_name: str | None = None,
        ) -> None: ...

    def renumber_zone_ids(
        self,
        zone_id_list: list[int] | None = None,
        start_number: int | None = None,
        ) -> None: ...

    def replace_cell_zone_suffix(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        old_suffix: str | None = None,
        new_suffix: str | None = None,
        merge: bool | None = None,
        ) -> None: ...

    def replace_edge_zone_suffix(
        self,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        old_suffix: str | None = None,
        new_suffix: str | None = None,
        merge: bool | None = None,
        ) -> None: ...

    def replace_face_zone_suffix(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        separator: str | None = None,
        replace_with: str | None = None,
        merge: bool | None = None,
        ) -> None: ...

    def replace_label_suffix(
        self,
        object_name_list: list[str] | None = None,
        separator: str | None = None,
        new_suffix: str | None = None,
        ) -> None: ...

    def replace_object_suffix(
        self,
        object_name_list: list[str] | None = None,
        separator: str | None = None,
        new_suffix: str | None = None,
        ) -> None: ...

    def set_number_of_parallel_compute_threads(
        self,
        nthreads: int | None = None,
        ) -> None: ...

    def set_object_cell_zone_type(
        self,
        object_name: str | None = None,
        cell_zone_type: str | None = None,
        ) -> None: ...

    def set_quality_measure(
        self,
        measure: str | None = None,
        ) -> None: ...

    def _cell_zones_labels_fdl(
        self,
        ) -> None: ...

    def _cell_zones_str_fdl(
        self,
        ) -> None: ...

    def _edge_zones_labels_fdl(
        self,
        ) -> None: ...

    def _edge_zones_str_fdl(
        self,
        ) -> None: ...

    def _face_zones_labels_fdl(
        self,
        ) -> None: ...

    def _face_zones_str_fdl(
        self,
        ) -> None: ...

    def _node_zones_labels_fdl(
        self,
        ) -> None: ...

    def _node_zones_str_fdl(
        self,
        ) -> None: ...

    def _object_names_str_fdl(
        self,
        ) -> None: ...

    def _prism_cell_zones_labels_fdl(
        self,
        ) -> None: ...

    def _prism_cell_zones_str_fdl(
        self,
        ) -> None: ...

    def _regions_str_fdl(
        self,
        ) -> None: ...

    def _zone_types_fdl(
        self,
        ) -> None: ...

    def boundary_zone_exists(
        self,
        zone_id: int | None = None,
        zone_name: str | None = None,
        ) -> bool: ...

    def cell_zone_exists(
        self,
        zone_id: int | None = None,
        zone_name: str | None = None,
        ) -> bool: ...

    def convert_zone_ids_to_name_strings(
        self,
        zone_id_list: list[int] | None = None,
        ) -> list[str]: ...

    def convert_zone_name_strings_to_ids(
        self,
        zone_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def copy_face_zone_labels(
        self,
        from_face_zone_id: int | None = None,
        from_face_zone_name: str | None = None,
        to_face_zone_id: int | None = None,
        to_face_zone_name: str | None = None,
        ) -> None: ...

    def count_marked_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def create_boi_and_size_functions_from_refinement_regions(
        self,
        region_type: str | None = None,
        boi_prefix_string: str | None = None,
        create_size_function: bool | None = None,
        ) -> None: ...

    def dump_face_zone_orientation_in_region(
        self,
        file_name: str | None = None,
        ) -> None: ...

    def fill_holes_in_face_zone_list(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        max_hole_edges: int | None = None,
        ) -> None: ...

    def get_adjacent_cell_zones_for_given_face_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_adjacent_face_zones_for_given_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_adjacent_zones_by_edge_connectivity(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_adjacent_zones_by_node_connectivity(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_all_objects(
        self,
        ) -> list[str]: ...

    def get_average_bounding_box_center(
        self,
        face_zone_id_list: list[int] | None = None,
        ) -> list[float]: ...

    def get_baffles_for_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        ) -> list[int]: ...

    def get_bounding_box_of_zone_list(
        self,
        zone_id_list: list[int] | None = None,
        ) -> None: ...

    def get_cell_mesh_distribution(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        measure: str | None = None,
        partitions: int | None = None,
        range: list[float] | None = None,
        ) -> None: ...

    def get_cell_quality_limits(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        measure: str | None = None,
        ) -> None: ...

    def get_cell_zone_count(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> int: ...

    def get_cell_zone_id_list_with_labels(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def get_cell_zone_shape(
        self,
        cell_zone_id: int | None = None,
        ) -> str: ...

    def get_cell_zone_volume(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> float: ...

    def get_cell_zones(
        self,
        maximum_entity_count: float | None = None,
        xyz_coordinates: list[float] | None = None,
        filter: str | None = None,
        ) -> None: ...

    def get_edge_size_limits(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[float]: ...

    def get_edge_zone_id_list_with_labels(
        self,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        edge_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def get_edge_zones(
        self,
        maximum_entity_count: float | None = None,
        only_boundary: bool | None = None,
        filter: str | None = None,
        ) -> list[int]: ...

    def get_edge_zones_list(
        self,
        filter: list[str] | None = None,
        ) -> None: ...

    def get_edge_zones_of_object(
        self,
        objects: list[str] | None = None,
        object_name: str | None = None,
        ) -> list[int]: ...

    def get_embedded_baffles(
        self,
        ) -> list[int]: ...

    def get_face_mesh_distribution(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        measure: str | None = None,
        partitions: int | None = None,
        range: list[float] | None = None,
        ) -> None: ...

    def get_face_quality_limits(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        measure: str | None = None,
        ) -> None: ...

    def get_face_zone_area(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> float: ...

    def get_face_zone_count(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def get_face_zone_id_list_with_labels(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        label_name_list: list[str] | None = None,
        ) -> list[int]: ...

    def get_face_zone_node_count(
        self,
        face_zone_id: int | None = None,
        face_zone_name: str | None = None,
        ) -> int: ...

    def get_face_zones(
        self,
        maximum_entity_count: float | None = None,
        only_boundary: bool | None = None,
        prism_control_name: str | None = None,
        xyz_coordinates: list[float] | None = None,
        filter: str | None = None,
        ) -> None: ...

    def get_face_zones_by_zone_area(
        self,
        maximum_zone_area: float | None = None,
        minimum_zone_area: float | None = None,
        ) -> list[int]: ...

    def get_face_zones_of_object(
        self,
        regions: list[str] | None = None,
        labels: list[str] | None = None,
        region_type: str | None = None,
        objects: list[str] | None = None,
        object_name: str | None = None,
        ) -> list[int]: ...

    def get_free_faces_count(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def get_interior_face_zones_for_given_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_labels(
        self,
        object_name: str | None = None,
        filter: str | None = None,
        label_name_pattern: str | None = None,
        ) -> list[str]: ...

    def get_labels_on_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[str]: ...

    def get_labels_on_edge_zones(
        self,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        edge_zone_name_pattern: str | None = None,
        ) -> list[str]: ...

    def get_labels_on_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[str]: ...

    def get_labels_on_face_zones_list(
        self,
        face_zone_id_list: list[int] | None = None,
        ) -> None: ...

    def get_maxsize_cell_zone_by_count(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> float: ...

    def get_maxsize_cell_zone_by_volume(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> float: ...

    def get_minsize_face_zone_by_area(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> float: ...

    def get_minsize_face_zone_by_count(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> float: ...

    def get_multi_faces_count(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def get_node_zones(
        self,
        filter: str | None = None,
        ) -> list[int]: ...

    def get_objects(
        self,
        type_name: str | None = None,
        filter: str | None = None,
        ) -> list[str]: ...

    def get_overlapping_face_zones(
        self,
        face_zone_name_pattern: str | None = None,
        area_tolerance: float | None = None,
        distance_tolerance: float | None = None,
        ) -> list[int]: ...

    def get_pairs_of_overlapping_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        join_tolerance: float | None = None,
        absolute_tolerance: bool | None = None,
        join_angle: float | None = None,
        ) -> list[int]: ...

    def get_prism_cell_zones(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_region_volume(
        self,
        object_name: str | None = None,
        region_name: str | None = None,
        sorting_order: str | None = None,
        ) -> None: ...

    def get_regions(
        self,
        object_name: str | None = None,
        region_name_pattern: str | None = None,
        filter: str | None = None,
        ) -> list[str]: ...

    def get_regions_of_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[str]: ...

    def get_shared_boundary_face_zones_for_given_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_tet_cell_zones(
        self,
        zone_id_list: list[int] | None = None,
        zone_name_list: list[str] | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_unreferenced_cell_zones(
        self,
        filter: str | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_unreferenced_edge_zones(
        self,
        filter: str | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_unreferenced_face_zones(
        self,
        filter: str | None = None,
        zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_wrapped_face_zones(
        self,
        ) -> list[int]: ...

    def get_zone_type(
        self,
        zone_id: int | None = None,
        zone_name: str | None = None,
        ) -> str: ...

    def get_zones(
        self,
        type_name: str | None = None,
        group_name: str | None = None,
        ) -> list[int]: ...

    def get_zones_with_free_faces_for_given_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_zones_with_marked_faces_for_given_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def get_zones_with_multi_faces_for_given_face_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> list[int]: ...

    def interior_zone_exists(
        self,
        zone_id: int | None = None,
        zone_name: str | None = None,
        ) -> bool: ...

    def mark_bad_quality_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        quality_limit: float | None = None,
        number_of_rings: int | None = None,
        ) -> int: ...

    def mark_duplicate_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def mark_face_strips_by_height_and_quality(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        strip_type: int | None = None,
        strip_height: float | None = None,
        quality_measure: str | None = None,
        quality_limit: float | None = None,
        feature_angle: float | None = None,
        ) -> int: ...

    def mark_faces_by_quality(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        quality_measure: str | None = None,
        quality_limit: float | None = None,
        append_marking: bool | None = None,
        ) -> None: ...

    def mark_faces_deviating_from_size_field(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        min_size_factor: float | None = None,
        max_size_factor: float | None = None,
        size_factor_type_to_compare: str | None = None,
        ) -> int: ...

    def mark_faces_in_self_proximity(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        relative_tolerance: bool | None = None,
        tolerance: float | None = None,
        proximity_angle: float | None = None,
        ignore_orientation: bool | None = None,
        ) -> None: ...

    def mark_faces_using_node_degree(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        node_degree_threshold: int | None = None,
        ) -> None: ...

    def mark_free_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def mark_invalid_normals(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> int: ...

    def mark_island_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        island_face_count: int | None = None,
        ) -> None: ...

    def mark_multi_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        fringe_length: int | None = None,
        ) -> int: ...

    def mark_point_contacts(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> None: ...

    def mark_self_intersecting_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        mark_folded: bool | None = None,
        ) -> int: ...

    def mark_sliver_faces(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        max_height: float | None = None,
        skew_limit: float | None = None,
        ) -> int: ...

    def mark_spikes(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        spike_angle: float | None = None,
        ) -> int: ...

    def mark_steps(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        step_angle: float | None = None,
        step_width: float | None = None,
        ) -> int: ...

    def mesh_check(
        self,
        type_name: str | None = None,
        edge_zone_id_list: list[int] | None = None,
        edge_zone_name_list: list[str] | None = None,
        edge_zone_name_pattern: str | None = None,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> None: ...

    def mesh_exists(
        self,
        ) -> None: ...

    def print_worst_quality_cell(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        measure: str | None = None,
        ) -> None: ...

    def project_zone_on_plane(
        self,
        zone_id: int | None = None,
        plane: dict[str, Any] | None = None,
        ) -> None: ...

    def refine_marked_faces_in_zones(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> None: ...

    def scale_cell_zones_around_pivot(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        scale: list[float] | None = None,
        pivot: list[float] | None = None,
        use_bbox_center: bool | None = None,
        ) -> None: ...

    def scale_face_zones_around_pivot(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        scale: list[float] | None = None,
        pivot: list[float] | None = None,
        use_bbox_center: bool | None = None,
        ) -> None: ...

    def separate_cell_zone_layers_by_face_zone(
        self,
        prism_cell_zone_id_list: list[int] | None = None,
        prism_cell_zone_name: str | None = None,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        nlayers: int | None = None,
        ) -> None: ...

    def separate_face_zones_by_cell_neighbor(
        self,
        face_zone_id_list: list[int] | None = None,
        face_zone_name_list: list[str] | None = None,
        face_zone_name_pattern: str | None = None,
        ) -> None: ...

    def unpreserve_cell_zones(
        self,
        cell_zone_id_list: list[int] | None = None,
        cell_zone_name_list: list[str] | None = None,
        cell_zone_name_pattern: str | None = None,
        ) -> None: ...
