"""Fluent meshing TUI commands"""
#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_tui import PyMenu, TUIMenu, TUIMethod



class main_menu(TUIMenu):
    """
    Fluent meshing main menu.
    """
    def __init__(self, service, version, mode, path):
        self.boundary = self.__class__.boundary(service, version, mode, path + ["boundary"])
        self.cad_assemblies = self.__class__.cad_assemblies(service, version, mode, path + ["cad_assemblies"])
        self.diagnostics = self.__class__.diagnostics(service, version, mode, path + ["diagnostics"])
        self.display = self.__class__.display(service, version, mode, path + ["display"])
        self.file = self.__class__.file(service, version, mode, path + ["file"])
        self.material_point = self.__class__.material_point(service, version, mode, path + ["material_point"])
        self.mesh = self.__class__.mesh(service, version, mode, path + ["mesh"])
        self.objects = self.__class__.objects(service, version, mode, path + ["objects"])
        self.openmp_controls = self.__class__.openmp_controls(service, version, mode, path + ["openmp_controls"])
        self.parallel = self.__class__.parallel(service, version, mode, path + ["parallel"])
        self.preferences = self.__class__.preferences(service, version, mode, path + ["preferences"])
        self.reference_frames = self.__class__.reference_frames(service, version, mode, path + ["reference_frames"])
        self.report = self.__class__.report(service, version, mode, path + ["report"])
        self.scoped_sizing = self.__class__.scoped_sizing(service, version, mode, path + ["scoped_sizing"])
        self.server = self.__class__.server(service, version, mode, path + ["server"])
        self.size_functions = self.__class__.size_functions(service, version, mode, path + ["size_functions"])
        self.beta_feature_access = self.__class__.beta_feature_access(service, version, mode, path + ["beta_feature_access"])
        self.close_fluent = self.__class__.close_fluent(service, version, mode, path + ["close_fluent"])
        self.print_license_usage = self.__class__.print_license_usage(service, version, mode, path + ["print_license_usage"])
        self.switch_to_solution_mode = self.__class__.switch_to_solution_mode(service, version, mode, path + ["switch_to_solution_mode"])
        super().__init__(service, version, mode, path)
    class beta_feature_access(TUIMethod):
        """
        No help available.
        """
    class close_fluent(TUIMethod):
        """
        Exit Fluent Meshing.
        """
    class print_license_usage(TUIMethod):
        """
        Print license usage information.
        """
    class switch_to_solution_mode(TUIMethod):
        """
        Switch to solution mode.
        """

    class boundary(TUIMenu):
        """
        Enter the boundary menu.
        """
        def __init__(self, service, version, mode, path):
            self.boundary_conditions = self.__class__.boundary_conditions(service, version, mode, path + ["boundary_conditions"])
            self.feature = self.__class__.feature(service, version, mode, path + ["feature"])
            self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
            self.manage = self.__class__.manage(service, version, mode, path + ["manage"])
            self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
            self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
            self.remesh = self.__class__.remesh(service, version, mode, path + ["remesh"])
            self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
            self.shell_boundary_layer = self.__class__.shell_boundary_layer(service, version, mode, path + ["shell_boundary_layer"])
            self.auto_slit_faces = self.__class__.auto_slit_faces(service, version, mode, path + ["auto_slit_faces"])
            self.check_boundary_mesh = self.__class__.check_boundary_mesh(service, version, mode, path + ["check_boundary_mesh"])
            self.check_duplicate_geom = self.__class__.check_duplicate_geom(service, version, mode, path + ["check_duplicate_geom"])
            self.clear_marked_faces = self.__class__.clear_marked_faces(service, version, mode, path + ["clear_marked_faces"])
            self.clear_marked_nodes = self.__class__.clear_marked_nodes(service, version, mode, path + ["clear_marked_nodes"])
            self.coarsen_boundary_faces = self.__class__.coarsen_boundary_faces(service, version, mode, path + ["coarsen_boundary_faces"])
            self.compute_bounding_box = self.__class__.compute_bounding_box(service, version, mode, path + ["compute_bounding_box"])
            self.count_free_nodes = self.__class__.count_free_nodes(service, version, mode, path + ["count_free_nodes"])
            self.count_marked_faces = self.__class__.count_marked_faces(service, version, mode, path + ["count_marked_faces"])
            self.count_unused_bound_node = self.__class__.count_unused_bound_node(service, version, mode, path + ["count_unused_bound_node"])
            self.count_unused_faces = self.__class__.count_unused_faces(service, version, mode, path + ["count_unused_faces"])
            self.count_unused_nodes = self.__class__.count_unused_nodes(service, version, mode, path + ["count_unused_nodes"])
            self.create_bounding_box = self.__class__.create_bounding_box(service, version, mode, path + ["create_bounding_box"])
            self.create_cylinder = self.__class__.create_cylinder(service, version, mode, path + ["create_cylinder"])
            self.create_plane_surface = self.__class__.create_plane_surface(service, version, mode, path + ["create_plane_surface"])
            self.create_revolved_surface = self.__class__.create_revolved_surface(service, version, mode, path + ["create_revolved_surface"])
            self.create_swept_surface = self.__class__.create_swept_surface(service, version, mode, path + ["create_swept_surface"])
            self.delete_all_dup_faces = self.__class__.delete_all_dup_faces(service, version, mode, path + ["delete_all_dup_faces"])
            self.delete_duplicate_faces = self.__class__.delete_duplicate_faces(service, version, mode, path + ["delete_duplicate_faces"])
            self.delete_free_edge_faces = self.__class__.delete_free_edge_faces(service, version, mode, path + ["delete_free_edge_faces"])
            self.delete_island_faces = self.__class__.delete_island_faces(service, version, mode, path + ["delete_island_faces"])
            self.delete_unconnected_faces = self.__class__.delete_unconnected_faces(service, version, mode, path + ["delete_unconnected_faces"])
            self.delete_unused_faces = self.__class__.delete_unused_faces(service, version, mode, path + ["delete_unused_faces"])
            self.delete_unused_nodes = self.__class__.delete_unused_nodes(service, version, mode, path + ["delete_unused_nodes"])
            self.edge_limits = self.__class__.edge_limits(service, version, mode, path + ["edge_limits"])
            self.expand_marked_faces_by_rings = self.__class__.expand_marked_faces_by_rings(service, version, mode, path + ["expand_marked_faces_by_rings"])
            self.face_distribution = self.__class__.face_distribution(service, version, mode, path + ["face_distribution"])
            self.face_skewness = self.__class__.face_skewness(service, version, mode, path + ["face_skewness"])
            self.fix_mconnected_edges = self.__class__.fix_mconnected_edges(service, version, mode, path + ["fix_mconnected_edges"])
            self.improve_surface_mesh = self.__class__.improve_surface_mesh(service, version, mode, path + ["improve_surface_mesh"])
            self.jiggle_boundary_nodes = self.__class__.jiggle_boundary_nodes(service, version, mode, path + ["jiggle_boundary_nodes"])
            self.make_periodic = self.__class__.make_periodic(service, version, mode, path + ["make_periodic"])
            self.mark_bad_quality_faces = self.__class__.mark_bad_quality_faces(service, version, mode, path + ["mark_bad_quality_faces"])
            self.mark_duplicate_nodes = self.__class__.mark_duplicate_nodes(service, version, mode, path + ["mark_duplicate_nodes"])
            self.mark_face_intersection = self.__class__.mark_face_intersection(service, version, mode, path + ["mark_face_intersection"])
            self.mark_face_proximity = self.__class__.mark_face_proximity(service, version, mode, path + ["mark_face_proximity"])
            self.mark_faces_in_region = self.__class__.mark_faces_in_region(service, version, mode, path + ["mark_faces_in_region"])
            self.merge_nodes = self.__class__.merge_nodes(service, version, mode, path + ["merge_nodes"])
            self.merge_small_face_zones = self.__class__.merge_small_face_zones(service, version, mode, path + ["merge_small_face_zones"])
            self.orient_faces_by_point = self.__class__.orient_faces_by_point(service, version, mode, path + ["orient_faces_by_point"])
            self.print_info = self.__class__.print_info(service, version, mode, path + ["print_info"])
            self.project_face_zone = self.__class__.project_face_zone(service, version, mode, path + ["project_face_zone"])
            self.recover_periodic_surfaces = self.__class__.recover_periodic_surfaces(service, version, mode, path + ["recover_periodic_surfaces"])
            self.reset_element_type = self.__class__.reset_element_type(service, version, mode, path + ["reset_element_type"])
            self.resolve_face_intersection = self.__class__.resolve_face_intersection(service, version, mode, path + ["resolve_face_intersection"])
            self.scale_nodes = self.__class__.scale_nodes(service, version, mode, path + ["scale_nodes"])
            self.set_periodicity = self.__class__.set_periodicity(service, version, mode, path + ["set_periodicity"])
            self.slit_boundary_face = self.__class__.slit_boundary_face(service, version, mode, path + ["slit_boundary_face"])
            self.smooth_marked_faces = self.__class__.smooth_marked_faces(service, version, mode, path + ["smooth_marked_faces"])
            self.unmark_faces_in_zones = self.__class__.unmark_faces_in_zones(service, version, mode, path + ["unmark_faces_in_zones"])
            self.unmark_selected_faces = self.__class__.unmark_selected_faces(service, version, mode, path + ["unmark_selected_faces"])
            self.wrapper = self.__class__.wrapper(service, version, mode, path + ["wrapper"])
            super().__init__(service, version, mode, path)
        class auto_slit_faces(TUIMethod):
            """
            Automatically slits all embedded boundary face zones.
            .
            """
        class check_boundary_mesh(TUIMethod):
            """
            Report number of Delaunay violations on surface mesh and unused nodes.
            """
        class check_duplicate_geom(TUIMethod):
            """
            Check duplicated face threads in the geometry.
            """
        class clear_marked_faces(TUIMethod):
            """
            Clear previously marked faces.
            """
        class clear_marked_nodes(TUIMethod):
            """
            Clear previously marked nodes.
            """
        class coarsen_boundary_faces(TUIMethod):
            """
            Coarsen boundary face zones.
            """
        class compute_bounding_box(TUIMethod):
            """
            Computes bounding box for given zones.
            """
        class count_free_nodes(TUIMethod):
            """
            Count number of free nodes.
            """
        class count_marked_faces(TUIMethod):
            """
            Count marked faces.
            """
        class count_unused_bound_node(TUIMethod):
            """
            Count number of unused boundary nodes.
            """
        class count_unused_faces(TUIMethod):
            """
            Count number of unused faces.
            """
        class count_unused_nodes(TUIMethod):
            """
            Count number of unused nodes.
            """
        class create_bounding_box(TUIMethod):
            """
            Create bounding box for given zones.
            """
        class create_cylinder(TUIMethod):
            """
            Create cylinder using two axis end nodes/positions or, three points on the arc defining the cylinder.
            """
        class create_plane_surface(TUIMethod):
            """
            Create plane surface.
            """
        class create_revolved_surface(TUIMethod):
            """
            Create surface by revolving the edge along the vector.
            """
        class create_swept_surface(TUIMethod):
            """
            Create surface by sweeping the edge along the vector.
            """
        class delete_all_dup_faces(TUIMethod):
            """
            Delete all duplicate faces on all boundary zones.
            """
        class delete_duplicate_faces(TUIMethod):
            """
            Delete duplicate faces on specified zones.
            """
        class delete_free_edge_faces(TUIMethod):
            """
            Remove faces with specified number of free edges.
            """
        class delete_island_faces(TUIMethod):
            """
            Delete island faces or cavity.
            """
        class delete_unconnected_faces(TUIMethod):
            """
            Delete unconnected face zones.
            """
        class delete_unused_faces(TUIMethod):
            """
            Delete unused boundary faces.
            """
        class delete_unused_nodes(TUIMethod):
            """
            Delete nodes not belonging to any boundary faces.
            """
        class edge_limits(TUIMethod):
            """
            Print shortest and largest edges on boundary mesh.
            """
        class expand_marked_faces_by_rings(TUIMethod):
            """
            Mark rings of faces around marked faces.
            """
        class face_distribution(TUIMethod):
            """
            Show face quality distribution.
            """
        class face_skewness(TUIMethod):
            """
            Show worse face skewness.
            """
        class fix_mconnected_edges(TUIMethod):
            """
            Fix multi connected edges.
            """
        class improve_surface_mesh(TUIMethod):
            """
            Improve surface mesh by swapping face edges
            where Delaunay violations occur.
            """
        class jiggle_boundary_nodes(TUIMethod):
            """
            Perturb randomly nodal position.
            """
        class make_periodic(TUIMethod):
            """
            Make periodic zone pair.
            """
        class mark_bad_quality_faces(TUIMethod):
            """
            Mark Bad Quality Faces.
            """
        class mark_duplicate_nodes(TUIMethod):
            """
            Mark duplicate nodes.
            """
        class mark_face_intersection(TUIMethod):
            """
            Mark face intersection in face zones.
            """
        class mark_face_proximity(TUIMethod):
            """
            Mark faces that are in proximity.
            """
        class mark_faces_in_region(TUIMethod):
            """
            Mark faces in local region.
            """
        class merge_nodes(TUIMethod):
            """
            Merge duplicate nodes.  If a face has two of
            its nodes merged, then it is deleted.
            """
        class merge_small_face_zones(TUIMethod):
            """
            Merge face zones having area less than min area with largest zone in its neighbor.
            """
        class orient_faces_by_point(TUIMethod):
            """
            Orient Region based on Material Point.
            """
        class print_info(TUIMethod):
            """
            Print node/face/cell info.
            """
        class project_face_zone(TUIMethod):
            """
            Project face zone to a background mesh.
            """
        class recover_periodic_surfaces(TUIMethod):
            """
            Recover periodic surfaces.
            """
        class reset_element_type(TUIMethod):
            """
            Reset the element type (mixed, linear, tri or quad) of a boundary zone.
            """
        class resolve_face_intersection(TUIMethod):
            """
            Resolve face intersection in tri-face zones.
            """
        class scale_nodes(TUIMethod):
            """
            Scale all nodes by the scale factor.
            """
        class set_periodicity(TUIMethod):
            """
            Set size field periodicity.
            """
        class slit_boundary_face(TUIMethod):
            """
            Make slit in mesh at boundary face.
            All faces must have normals oriented in the same direction.
            .
            """
        class smooth_marked_faces(TUIMethod):
            """
            Smooth Marked faces on threads.
            """
        class unmark_faces_in_zones(TUIMethod):
            """
            Unmark faces in zones.
            """
        class unmark_selected_faces(TUIMethod):
            """
            Clear mark on selected faces.
            """
        class wrapper(TUIMethod):
            """
            Enter surface wrapper menu.
            """

        class boundary_conditions(TUIMenu):
            """
            Enter manage boundary conditions menu.
            """
            def __init__(self, service, version, mode, path):
                self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
                self.clear_all = self.__class__.clear_all(service, version, mode, path + ["clear_all"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                super().__init__(service, version, mode, path)
            class clear(TUIMethod):
                """
                Clear boundary conditions.
                """
            class clear_all(TUIMethod):
                """
                Clear all boundary conditions.
                """
            class copy(TUIMethod):
                """
                Copy boundary conditions.
                """

        class feature(TUIMenu):
            """
            Enter bounday feature menu.
            """
            def __init__(self, service, version, mode, path):
                self.copy_edge_zones = self.__class__.copy_edge_zones(service, version, mode, path + ["copy_edge_zones"])
                self.create_edge_zones = self.__class__.create_edge_zones(service, version, mode, path + ["create_edge_zones"])
                self.delete_degenerated_edges = self.__class__.delete_degenerated_edges(service, version, mode, path + ["delete_degenerated_edges"])
                self.delete_edge_zones = self.__class__.delete_edge_zones(service, version, mode, path + ["delete_edge_zones"])
                self.edge_size_limits = self.__class__.edge_size_limits(service, version, mode, path + ["edge_size_limits"])
                self.group = self.__class__.group(service, version, mode, path + ["group"])
                self.intersect_edge_zones = self.__class__.intersect_edge_zones(service, version, mode, path + ["intersect_edge_zones"])
                self.list_edge_zones = self.__class__.list_edge_zones(service, version, mode, path + ["list_edge_zones"])
                self.merge_edge_zones = self.__class__.merge_edge_zones(service, version, mode, path + ["merge_edge_zones"])
                self.orient_edge_direction = self.__class__.orient_edge_direction(service, version, mode, path + ["orient_edge_direction"])
                self.project_edge_zones = self.__class__.project_edge_zones(service, version, mode, path + ["project_edge_zones"])
                self.remesh_edge_zones = self.__class__.remesh_edge_zones(service, version, mode, path + ["remesh_edge_zones"])
                self.reverse_edge_direction = self.__class__.reverse_edge_direction(service, version, mode, path + ["reverse_edge_direction"])
                self.secondary_feature_angle = self.__class__.secondary_feature_angle(service, version, mode, path + ["secondary_feature_angle"])
                self.separate_delete_small_edges = self.__class__.separate_delete_small_edges(service, version, mode, path + ["separate_delete_small_edges"])
                self.separate_edge_zones = self.__class__.separate_edge_zones(service, version, mode, path + ["separate_edge_zones"])
                self.separate_edge_zones_by_seed = self.__class__.separate_edge_zones_by_seed(service, version, mode, path + ["separate_edge_zones_by_seed"])
                self.toggle_edge_type = self.__class__.toggle_edge_type(service, version, mode, path + ["toggle_edge_type"])
                self.ungroup = self.__class__.ungroup(service, version, mode, path + ["ungroup"])
                super().__init__(service, version, mode, path)
            class copy_edge_zones(TUIMethod):
                """
                Copy edge zones.
                """
            class create_edge_zones(TUIMethod):
                """
                Create edge loops of thread based on feature angle.
                """
            class delete_degenerated_edges(TUIMethod):
                """
                Delete from Edge Zones, Edges whose two end nodes are the same.
                """
            class delete_edge_zones(TUIMethod):
                """
                Delete edge zones.
                """
            class edge_size_limits(TUIMethod):
                """
                Report edge size limits.
                """
            class group(TUIMethod):
                """
                Group face and edge zones together.
                """
            class intersect_edge_zones(TUIMethod):
                """
                Intersect edge zones.
                """
            class list_edge_zones(TUIMethod):
                """
                List edge zones.
                """
            class merge_edge_zones(TUIMethod):
                """
                Merge edge zones.
                """
            class orient_edge_direction(TUIMethod):
                """
                Orient edge zone directions.
                """
            class project_edge_zones(TUIMethod):
                """
                Project edge zones on specified face zone.
                """
            class remesh_edge_zones(TUIMethod):
                """
                Remesh edge zones.
                """
            class reverse_edge_direction(TUIMethod):
                """
                Reverse direction of edge loops.
                """
            class secondary_feature_angle(TUIMethod):
                """
                Set secondary feature angle.
                """
            class separate_delete_small_edges(TUIMethod):
                """
                Separates and deletes small edges.
                """
            class separate_edge_zones(TUIMethod):
                """
                Separate edge zones based on connectivity and feature angle.
                """
            class separate_edge_zones_by_seed(TUIMethod):
                """
                Separate edge zones by seed.
                """
            class toggle_edge_type(TUIMethod):
                """
                Toggle edge type between boundary and interior.
                """
            class ungroup(TUIMethod):
                """
                Ungroup previously grouped face and edge zones.
                """

        class improve(TUIMenu):
            """
            Enter Imporve  boundary face zone menu.
            """
            def __init__(self, service, version, mode, path):
                self.collapse_bad_faces = self.__class__.collapse_bad_faces(service, version, mode, path + ["collapse_bad_faces"])
                self.degree_swap = self.__class__.degree_swap(service, version, mode, path + ["degree_swap"])
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                super().__init__(service, version, mode, path)
            class collapse_bad_faces(TUIMethod):
                """
                Collapse short edge of faces with high aspect ratio.
                """
            class degree_swap(TUIMethod):
                """
                Perform swap on boundary mesh based on node degree.
                """
            class improve(TUIMethod):
                """
                Improve skewness of tri boundary face zones.
                """
            class smooth(TUIMethod):
                """
                Smooth  face zones using laplace smoothing.
                .
                """
            class swap(TUIMethod):
                """
                Improve surface mesh by swapping face edges
                where Delaunay violations occur.
                """

        class manage(TUIMenu):
            """
            Enter face zone menu.
            """
            def __init__(self, service, version, mode, path):
                self.user_defined_groups = self.__class__.user_defined_groups(service, version, mode, path + ["user_defined_groups"])
                self.auto_delete_nodes = self.__class__.auto_delete_nodes(service, version, mode, path + ["auto_delete_nodes"])
                self.change_prefix = self.__class__.change_prefix(service, version, mode, path + ["change_prefix"])
                self.change_suffix = self.__class__.change_suffix(service, version, mode, path + ["change_suffix"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.flip = self.__class__.flip(service, version, mode, path + ["flip"])
                self.id = self.__class__.id(service, version, mode, path + ["id"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.name = self.__class__.name(service, version, mode, path + ["name"])
                self.orient = self.__class__.orient(service, version, mode, path + ["orient"])
                self.origin = self.__class__.origin(service, version, mode, path + ["origin"])
                self.remove_suffix = self.__class__.remove_suffix(service, version, mode, path + ["remove_suffix"])
                self.rotate = self.__class__.rotate(service, version, mode, path + ["rotate"])
                self.rotate_model = self.__class__.rotate_model(service, version, mode, path + ["rotate_model"])
                self.scale = self.__class__.scale(service, version, mode, path + ["scale"])
                self.scale_model = self.__class__.scale_model(service, version, mode, path + ["scale_model"])
                self.translate = self.__class__.translate(service, version, mode, path + ["translate"])
                self.translate_model = self.__class__.translate_model(service, version, mode, path + ["translate_model"])
                self.type = self.__class__.type(service, version, mode, path + ["type"])
                super().__init__(service, version, mode, path)
            class auto_delete_nodes(TUIMethod):
                """
                Automatically delete unused nodes after deleting faces.
                """
            class change_prefix(TUIMethod):
                """
                Change the prefix for specified face zones.
                """
            class change_suffix(TUIMethod):
                """
                Change the suffix for specified face zones.
                """
            class copy(TUIMethod):
                """
                Copy all nodes and faces of specified face zones.
                """
            class create(TUIMethod):
                """
                Create new face zone.
                """
            class delete(TUIMethod):
                """
                Delete face zone, leaving nodes.
                """
            class flip(TUIMethod):
                """
                Flip the orientation of all face normals on the face zone.
                """
            class id(TUIMethod):
                """
                Give zone a new id number.
                """
            class list(TUIMethod):
                """
                List boundary face zones.
                """
            class merge(TUIMethod):
                """
                Merge two or more face zones.
                """
            class name(TUIMethod):
                """
                Give zone a new name.
                """
            class orient(TUIMethod):
                """
                Consistently orient zones.
                """
            class origin(TUIMethod):
                """
                Set the origin of the mesh coordinates.
                """
            class remove_suffix(TUIMethod):
                """
                Remove the leftmost ':' and the characters after it in the face zone names.
                """
            class rotate(TUIMethod):
                """
                Rotate all nodes of specified face zones.
                """
            class rotate_model(TUIMethod):
                """
                Rotate all nodes.
                """
            class scale(TUIMethod):
                """
                Scale all nodes of specified face zones.
                """
            class scale_model(TUIMethod):
                """
                Scale all nodes.
                """
            class translate(TUIMethod):
                """
                Translate all nodes of specified face zones.
                """
            class translate_model(TUIMethod):
                """
                Translate all nodes.
                """
            class type(TUIMethod):
                """
                Change face zone type.
                """

            class user_defined_groups(TUIMenu):
                """
                Collect boundary zones to form logical groups.
                """
                def __init__(self, service, version, mode, path):
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.create = self.__class__.create(service, version, mode, path + ["create"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.update = self.__class__.update(service, version, mode, path + ["update"])
                    super().__init__(service, version, mode, path)
                class activate(TUIMethod):
                    """
                    Activate a User Defined Group.
                    """
                class create(TUIMethod):
                    """
                    Create a new User Defined Group.
                    """
                class delete(TUIMethod):
                    """
                    Delete a User Defined Group.
                    """
                class list(TUIMethod):
                    """
                    List User Defined Groups.
                    """
                class update(TUIMethod):
                    """
                    Update a User Defined Group.
                    """

        class modify(TUIMenu):
            """
            Enter boundary modify menu.
            """
            def __init__(self, service, version, mode, path):
                self.analyze_bnd_connectvty = self.__class__.analyze_bnd_connectvty(service, version, mode, path + ["analyze_bnd_connectvty"])
                self.auto_patch_holes = self.__class__.auto_patch_holes(service, version, mode, path + ["auto_patch_holes"])
                self.clear_selections = self.__class__.clear_selections(service, version, mode, path + ["clear_selections"])
                self.clear_skew_faces = self.__class__.clear_skew_faces(service, version, mode, path + ["clear_skew_faces"])
                self.collapse = self.__class__.collapse(service, version, mode, path + ["collapse"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.create_mid_node = self.__class__.create_mid_node(service, version, mode, path + ["create_mid_node"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.delta_move = self.__class__.delta_move(service, version, mode, path + ["delta_move"])
                self.deselect_last = self.__class__.deselect_last(service, version, mode, path + ["deselect_last"])
                self.hole_feature_angle = self.__class__.hole_feature_angle(service, version, mode, path + ["hole_feature_angle"])
                self.list_selections = self.__class__.list_selections(service, version, mode, path + ["list_selections"])
                self.local_remesh = self.__class__.local_remesh(service, version, mode, path + ["local_remesh"])
                self.mark_skew_face = self.__class__.mark_skew_face(service, version, mode, path + ["mark_skew_face"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.move = self.__class__.move(service, version, mode, path + ["move"])
                self.next_skew = self.__class__.next_skew(service, version, mode, path + ["next_skew"])
                self.patch_options = self.__class__.patch_options(service, version, mode, path + ["patch_options"])
                self.rezone = self.__class__.rezone(service, version, mode, path + ["rezone"])
                self.select_entity = self.__class__.select_entity(service, version, mode, path + ["select_entity"])
                self.select_filter = self.__class__.select_filter(service, version, mode, path + ["select_filter"])
                self.select_position = self.__class__.select_position(service, version, mode, path + ["select_position"])
                self.select_probe = self.__class__.select_probe(service, version, mode, path + ["select_probe"])
                self.select_visible_entities = self.__class__.select_visible_entities(service, version, mode, path + ["select_visible_entities"])
                self.select_zone = self.__class__.select_zone(service, version, mode, path + ["select_zone"])
                self.show_filter = self.__class__.show_filter(service, version, mode, path + ["show_filter"])
                self.show_probe = self.__class__.show_probe(service, version, mode, path + ["show_probe"])
                self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                self.skew_report_zone = self.__class__.skew_report_zone(service, version, mode, path + ["skew_report_zone"])
                self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                self.split_face = self.__class__.split_face(service, version, mode, path + ["split_face"])
                self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                self.undo = self.__class__.undo(service, version, mode, path + ["undo"])
                super().__init__(service, version, mode, path)
            class analyze_bnd_connectvty(TUIMethod):
                """
                Find and mark free edges/nodes and mutliple-connected edges/nodes.
                """
            class auto_patch_holes(TUIMethod):
                """
                Patch zone(s) by filling holes.
                """
            class clear_selections(TUIMethod):
                """
                Clear all selections.
                """
            class clear_skew_faces(TUIMethod):
                """
                Clear faces previously marked as skewed.
                """
            class collapse(TUIMethod):
                """
                Collapse pairs of nodes or edges or faces.
                """
            class create(TUIMethod):
                """
                Create either nodes or faces.
                """
            class create_mid_node(TUIMethod):
                """
                Create a node at the midpoint between two selected nodes.
                """
            class delete(TUIMethod):
                """
                Delete either nodes, faces or zones.
                """
            class delta_move(TUIMethod):
                """
                Move nodes to new positions.
                """
            class deselect_last(TUIMethod):
                """
                Deselect last selection.
                """
            class hole_feature_angle(TUIMethod):
                """
                Angle defining boundary of hole.
                """
            class list_selections(TUIMethod):
                """
                List selections.
                """
            class local_remesh(TUIMethod):
                """
                Remesh locally starting from face seeds.
                """
            class mark_skew_face(TUIMethod):
                """
                Mark face to skip when reporting worst skew face.
                """
            class merge(TUIMethod):
                """
                Merge nodes.
                """
            class move(TUIMethod):
                """
                Move nodes to new positions.
                """
            class next_skew(TUIMethod):
                """
                Display the next highest skewed boundary face.
                """
            class patch_options(TUIMethod):
                """
                Settings for Patching zone(s) by filling holes.
                """
            class rezone(TUIMethod):
                """
                Change the zone faces belong to.
                """
            class select_entity(TUIMethod):
                """
                Select a entity.
                """
            class select_filter(TUIMethod):
                """
                Select probe filter.
                """
            class select_position(TUIMethod):
                """
                Select a position.
                """
            class select_probe(TUIMethod):
                """
                Select probe function.
                """
            class select_visible_entities(TUIMethod):
                """
                Set visual selection mode of entities.
                """
            class select_zone(TUIMethod):
                """
                Select a zone.
                """
            class show_filter(TUIMethod):
                """
                Show current probe filter.
                """
            class show_probe(TUIMethod):
                """
                Show current probe function.
                """
            class skew(TUIMethod):
                """
                Display the highest skewed boundary face.
                """
            class skew_report_zone(TUIMethod):
                """
                Face zone for which skewness has to be reported.
                """
            class smooth(TUIMethod):
                """
                Smooth selected nodes.
                """
            class split_face(TUIMethod):
                """
                Split two selected faces into four.
                """
            class swap(TUIMethod):
                """
                Swap edges.
                """
            class undo(TUIMethod):
                """
                Undo last modification.
                """

        class refine(TUIMenu):
            """
            Enter refine boundary face menu.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.auto_refine = self.__class__.auto_refine(service, version, mode, path + ["auto_refine"])
                self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
                self.count = self.__class__.count(service, version, mode, path + ["count"])
                self.limits = self.__class__.limits(service, version, mode, path + ["limits"])
                self.mark = self.__class__.mark(service, version, mode, path + ["mark"])
                self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                super().__init__(service, version, mode, path)
            class auto_refine(TUIMethod):
                """
                Automatically refine faces based on proximity with other faces.
                """
            class clear(TUIMethod):
                """
                Clear the refine flag at the faces.
                """
            class count(TUIMethod):
                """
                Count the number of faces flagged on thread(s).
                """
            class limits(TUIMethod):
                """
                List face zone information on number of faces flagged and range of face size.
                """
            class mark(TUIMethod):
                """
                Mark faces in region for refinement.
                """
            class refine(TUIMethod):
                """
                Refine the flagged faces.
                """

            class local_regions(TUIMenu):
                """
                Enter the refine-local menu.
                """
                def __init__(self, service, version, mode, path):
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class define(TUIMethod):
                    """
                    Define a refinement region's parameters.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region.
                    """
                class init(TUIMethod):
                    """
                    Delete all current regions and add the default refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    List all refinement regions.
                    """

        class remesh(TUIMenu):
            """
            Enter remeshing boundary face zone menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.size_functions = self.__class__.size_functions(service, version, mode, path + ["size_functions"])
                self.clear_marked_faces = self.__class__.clear_marked_faces(service, version, mode, path + ["clear_marked_faces"])
                self.coarsen_and_refine = self.__class__.coarsen_and_refine(service, version, mode, path + ["coarsen_and_refine"])
                self.create_all_intrst_loops = self.__class__.create_all_intrst_loops(service, version, mode, path + ["create_all_intrst_loops"])
                self.create_edge_loops = self.__class__.create_edge_loops(service, version, mode, path + ["create_edge_loops"])
                self.create_intersect_loop = self.__class__.create_intersect_loop(service, version, mode, path + ["create_intersect_loop"])
                self.create_join_loop = self.__class__.create_join_loop(service, version, mode, path + ["create_join_loop"])
                self.create_stitch_loop = self.__class__.create_stitch_loop(service, version, mode, path + ["create_stitch_loop"])
                self.delete_overlapped_edges = self.__class__.delete_overlapped_edges(service, version, mode, path + ["delete_overlapped_edges"])
                self.faceted_stitch_zones = self.__class__.faceted_stitch_zones(service, version, mode, path + ["faceted_stitch_zones"])
                self.insert_edge_zone = self.__class__.insert_edge_zone(service, version, mode, path + ["insert_edge_zone"])
                self.intersect_all_face_zones = self.__class__.intersect_all_face_zones(service, version, mode, path + ["intersect_all_face_zones"])
                self.intersect_face_zones = self.__class__.intersect_face_zones(service, version, mode, path + ["intersect_face_zones"])
                self.join_all_face_zones = self.__class__.join_all_face_zones(service, version, mode, path + ["join_all_face_zones"])
                self.join_face_zones = self.__class__.join_face_zones(service, version, mode, path + ["join_face_zones"])
                self.mark_intersecting_faces = self.__class__.mark_intersecting_faces(service, version, mode, path + ["mark_intersecting_faces"])
                self.mark_join_faces = self.__class__.mark_join_faces(service, version, mode, path + ["mark_join_faces"])
                self.mark_stitch_faces = self.__class__.mark_stitch_faces(service, version, mode, path + ["mark_stitch_faces"])
                self.remesh_constant_size = self.__class__.remesh_constant_size(service, version, mode, path + ["remesh_constant_size"])
                self.remesh_face_zone = self.__class__.remesh_face_zone(service, version, mode, path + ["remesh_face_zone"])
                self.remesh_face_zones_conformally = self.__class__.remesh_face_zones_conformally(service, version, mode, path + ["remesh_face_zones_conformally"])
                self.remesh_marked_faces = self.__class__.remesh_marked_faces(service, version, mode, path + ["remesh_marked_faces"])
                self.remesh_overlapping_zones = self.__class__.remesh_overlapping_zones(service, version, mode, path + ["remesh_overlapping_zones"])
                self.stitch_all_face_zones = self.__class__.stitch_all_face_zones(service, version, mode, path + ["stitch_all_face_zones"])
                self.stitch_face_zones = self.__class__.stitch_face_zones(service, version, mode, path + ["stitch_face_zones"])
                self.stitch_with_preserve_boundary = self.__class__.stitch_with_preserve_boundary(service, version, mode, path + ["stitch_with_preserve_boundary"])
                self.triangulate = self.__class__.triangulate(service, version, mode, path + ["triangulate"])
                super().__init__(service, version, mode, path)
            class clear_marked_faces(TUIMethod):
                """
                Clear previously marked faces.
                """
            class coarsen_and_refine(TUIMethod):
                """
                Coarsen and refine face zones according to size function.
                """
            class create_all_intrst_loops(TUIMethod):
                """
                Create edge loop of intersection for all boundary zones in current domain.
                """
            class create_edge_loops(TUIMethod):
                """
                Create edge loops of thread based on feature angle.
                """
            class create_intersect_loop(TUIMethod):
                """
                Create edge loop of intersection.
                """
            class create_join_loop(TUIMethod):
                """
                Create edge loop of overlap region.
                """
            class create_stitch_loop(TUIMethod):
                """
                Create edge loop of stitch edges.
                """
            class delete_overlapped_edges(TUIMethod):
                """
                Delete edges that overlapped selected loops.
                """
            class faceted_stitch_zones(TUIMethod):
                """
                Stitch free edges on zones.
                """
            class insert_edge_zone(TUIMethod):
                """
                Insert edge into face zonoe.
                """
            class intersect_all_face_zones(TUIMethod):
                """
                Intersect all face zones.
                """
            class intersect_face_zones(TUIMethod):
                """
                Intersection face zones.
                """
            class join_all_face_zones(TUIMethod):
                """
                Intersect all face zones.
                """
            class join_face_zones(TUIMethod):
                """
                Join face zones.
                """
            class mark_intersecting_faces(TUIMethod):
                """
                Mark faces on zones.
                """
            class mark_join_faces(TUIMethod):
                """
                Mark faces on zones.
                """
            class mark_stitch_faces(TUIMethod):
                """
                Mark faces on zones.
                """
            class remesh_constant_size(TUIMethod):
                """
                Retriangulate face zones to constant triangle size while maintaining conformity.
                """
            class remesh_face_zone(TUIMethod):
                """
                Retriangulate a face zone.
                """
            class remesh_face_zones_conformally(TUIMethod):
                """
                Retriangulate face zones while maintaining conformity.
                """
            class remesh_marked_faces(TUIMethod):
                """
                Locally remesh marked faces.
                """
            class remesh_overlapping_zones(TUIMethod):
                """
                Remeshing overlapping face zones.
                """
            class stitch_all_face_zones(TUIMethod):
                """
                Intersect all face zones.
                """
            class stitch_face_zones(TUIMethod):
                """
                Stitch edges on zones.
                """
            class stitch_with_preserve_boundary(TUIMethod):
                """
                Stitch volume to boundary zone at free faces.
                """
            class triangulate(TUIMethod):
                """
                Create triangulation from existing quad face zone.
                """

            class controls(TUIMenu):
                """
                Edge loop tools text menu.
                """
                def __init__(self, service, version, mode, path):
                    self.intersect = self.__class__.intersect(service, version, mode, path + ["intersect"])
                    self.delete_overlapped = self.__class__.delete_overlapped(service, version, mode, path + ["delete_overlapped"])
                    self.direction = self.__class__.direction(service, version, mode, path + ["direction"])
                    self.project_method = self.__class__.project_method(service, version, mode, path + ["project_method"])
                    self.proximity_local_search = self.__class__.proximity_local_search(service, version, mode, path + ["proximity_local_search"])
                    self.quadratic_recon = self.__class__.quadratic_recon(service, version, mode, path + ["quadratic_recon"])
                    self.remesh_method = self.__class__.remesh_method(service, version, mode, path + ["remesh_method"])
                    self.spacing = self.__class__.spacing(service, version, mode, path + ["spacing"])
                    self.tolerance = self.__class__.tolerance(service, version, mode, path + ["tolerance"])
                    super().__init__(service, version, mode, path)
                class delete_overlapped(TUIMethod):
                    """
                    Turn on/off deletion of overlapped edges.
                    """
                class direction(TUIMethod):
                    """
                    Set direction of edge loop projection.
                    """
                class project_method(TUIMethod):
                    """
                    Available methods: 0-closest 1-direction.
                    """
                class proximity_local_search(TUIMethod):
                    """
                    Include selected face for proximity calculation.
                    """
                class quadratic_recon(TUIMethod):
                    """
                    Turn on/off quadratic reconstruction of edge loops.
                    """
                class remesh_method(TUIMethod):
                    """
                    Available methods: 1-constant 2-arithmetic 3-geometric.
                    """
                class spacing(TUIMethod):
                    """
                    Set first and last edge spacing.
                    """
                class tolerance(TUIMethod):
                    """
                    Set intersection tolerance (absolute unit).
                    """

                class intersect(TUIMenu):
                    """
                    Enter the intersect control menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.absolute_tolerance = self.__class__.absolute_tolerance(service, version, mode, path + ["absolute_tolerance"])
                        self.delete_overlap = self.__class__.delete_overlap(service, version, mode, path + ["delete_overlap"])
                        self.feature_angle = self.__class__.feature_angle(service, version, mode, path + ["feature_angle"])
                        self.ignore_parallel_faces = self.__class__.ignore_parallel_faces(service, version, mode, path + ["ignore_parallel_faces"])
                        self.join_match_angle = self.__class__.join_match_angle(service, version, mode, path + ["join_match_angle"])
                        self.join_project_angle = self.__class__.join_project_angle(service, version, mode, path + ["join_project_angle"])
                        self.refine_region = self.__class__.refine_region(service, version, mode, path + ["refine_region"])
                        self.remesh_post_intersection = self.__class__.remesh_post_intersection(service, version, mode, path + ["remesh_post_intersection"])
                        self.retri_improve = self.__class__.retri_improve(service, version, mode, path + ["retri_improve"])
                        self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
                        self.stitch_preserve = self.__class__.stitch_preserve(service, version, mode, path + ["stitch_preserve"])
                        self.tolerance = self.__class__.tolerance(service, version, mode, path + ["tolerance"])
                        self.within_tolerance = self.__class__.within_tolerance(service, version, mode, path + ["within_tolerance"])
                        super().__init__(service, version, mode, path)
                    class absolute_tolerance(TUIMethod):
                        """
                        Turn on/off absolute tolerance.
                        """
                    class delete_overlap(TUIMethod):
                        """
                        Turn on/off deletion of overlapped region.
                        """
                    class feature_angle(TUIMethod):
                        """
                        Angle used to determine angle feature edges.
                        """
                    class ignore_parallel_faces(TUIMethod):
                        """
                        Turn on/off ignore parallel faces.
                        """
                    class join_match_angle(TUIMethod):
                        """
                        Max allowable angle between normals of faces to join.
                        """
                    class join_project_angle(TUIMethod):
                        """
                        Max allowable angle between face normal and project direction for join.
                        """
                    class refine_region(TUIMethod):
                        """
                        Turn on/off refinement of intersection region.
                        """
                    class remesh_post_intersection(TUIMethod):
                        """
                        Remesh after intersection.
                        """
                    class retri_improve(TUIMethod):
                        """
                        Turn on/off mesh improvement.
                        """
                    class separate(TUIMethod):
                        """
                        Turn on/off separation of intersection region.
                        """
                    class stitch_preserve(TUIMethod):
                        """
                        Turn on/off stitch preserve first zone shape.
                        """
                    class tolerance(TUIMethod):
                        """
                        Intersection tolerance.
                        """
                    class within_tolerance(TUIMethod):
                        """
                        Turn on/off tolerant intersection.
                        """

            class size_functions(TUIMenu):
                """
                Enable specification of size functions.
                """
                def __init__(self, service, version, mode, path):
                    self.contours = self.__class__.contours(service, version, mode, path + ["contours"])
                    self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                    self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
                    self.create = self.__class__.create(service, version, mode, path + ["create"])
                    self.create_defaults = self.__class__.create_defaults(service, version, mode, path + ["create_defaults"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
                    self.disable_periodicity_filter = self.__class__.disable_periodicity_filter(service, version, mode, path + ["disable_periodicity_filter"])
                    self.enable_periodicity_filter = self.__class__.enable_periodicity_filter(service, version, mode, path + ["enable_periodicity_filter"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.list_periodicity_filter = self.__class__.list_periodicity_filter(service, version, mode, path + ["list_periodicity_filter"])
                    self.reset_global_controls = self.__class__.reset_global_controls(service, version, mode, path + ["reset_global_controls"])
                    self.set_global_controls = self.__class__.set_global_controls(service, version, mode, path + ["set_global_controls"])
                    self.set_prox_gap_tolerance = self.__class__.set_prox_gap_tolerance(service, version, mode, path + ["set_prox_gap_tolerance"])
                    self.set_scaling_filter = self.__class__.set_scaling_filter(service, version, mode, path + ["set_scaling_filter"])
                    self.triangulate_quad_faces = self.__class__.triangulate_quad_faces(service, version, mode, path + ["triangulate_quad_faces"])
                    self.use_cad_imported_curvature = self.__class__.use_cad_imported_curvature(service, version, mode, path + ["use_cad_imported_curvature"])
                    super().__init__(service, version, mode, path)
                class compute(TUIMethod):
                    """
                    Compute Size-functions.
                    """
                class create(TUIMethod):
                    """
                    Add size function.
                    """
                class create_defaults(TUIMethod):
                    """
                    Creates default curvature & proximty size functions acting on all faces and edges.
                    """
                class delete(TUIMethod):
                    """
                    Delete Size Functions.
                    """
                class delete_all(TUIMethod):
                    """
                    Delete All Size Functions.
                    """
                class disable_periodicity_filter(TUIMethod):
                    """
                    Disable size field periodicity.
                    """
                class enable_periodicity_filter(TUIMethod):
                    """
                    Enable size field periodicity.
                    """
                class list(TUIMethod):
                    """
                    List all Size function parameters.
                    """
                class list_periodicity_filter(TUIMethod):
                    """
                    List periodic in size field.
                    """
                class reset_global_controls(TUIMethod):
                    """
                    Reset controls for global controls.
                    """
                class set_global_controls(TUIMethod):
                    """
                    Set controls for global controls.
                    """
                class set_prox_gap_tolerance(TUIMethod):
                    """
                    Set proximity min gap tolerance relative to global min-size.
                    """
                class set_scaling_filter(TUIMethod):
                    """
                    Set scaling filter on size field.
                    """
                class triangulate_quad_faces(TUIMethod):
                    """
                    Replace non-triangular face zones with triangulated face zones during size field computation.
                    """
                class use_cad_imported_curvature(TUIMethod):
                    """
                    Use curvature data imported from CAD.
                    """

                class contours(TUIMenu):
                    """
                    Menu to contour of size field.
                    """
                    def __init__(self, service, version, mode, path):
                        self.set = self.__class__.set(service, version, mode, path + ["set"])
                        self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                        super().__init__(service, version, mode, path)
                    class draw(TUIMethod):
                        """
                        Draw size field contour on face zones.
                        """

                    class set(TUIMenu):
                        """
                        Set contour options.
                        """
                        def __init__(self, service, version, mode, path):
                            self.refine_facets = self.__class__.refine_facets(service, version, mode, path + ["refine_facets"])
                            super().__init__(service, version, mode, path)
                        class refine_facets(TUIMethod):
                            """
                            Option to refine facets virtually? for better contour resolution.
                            """

                class controls(TUIMenu):
                    """
                    Menu to control different behavior of sf.
                    """
                    def __init__(self, service, version, mode, path):
                        self.curvature_method = self.__class__.curvature_method(service, version, mode, path + ["curvature_method"])
                        self.meshed_sf_behavior = self.__class__.meshed_sf_behavior(service, version, mode, path + ["meshed_sf_behavior"])
                        super().__init__(service, version, mode, path)
                    class curvature_method(TUIMethod):
                        """
                        Option to get facet curvature.
                        """
                    class meshed_sf_behavior(TUIMethod):
                        """
                        Set meshed size function processing to hard.
                        """

        class separate(TUIMenu):
            """
            Enter separate boundary face menu.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.mark_faces_in_region = self.__class__.mark_faces_in_region(service, version, mode, path + ["mark_faces_in_region"])
                self.sep_face_zone_by_angle = self.__class__.sep_face_zone_by_angle(service, version, mode, path + ["sep_face_zone_by_angle"])
                self.sep_face_zone_by_cnbor = self.__class__.sep_face_zone_by_cnbor(service, version, mode, path + ["sep_face_zone_by_cnbor"])
                self.sep_face_zone_by_mark = self.__class__.sep_face_zone_by_mark(service, version, mode, path + ["sep_face_zone_by_mark"])
                self.sep_face_zone_by_region = self.__class__.sep_face_zone_by_region(service, version, mode, path + ["sep_face_zone_by_region"])
                self.sep_face_zone_by_seed = self.__class__.sep_face_zone_by_seed(service, version, mode, path + ["sep_face_zone_by_seed"])
                self.sep_face_zone_by_seed_angle = self.__class__.sep_face_zone_by_seed_angle(service, version, mode, path + ["sep_face_zone_by_seed_angle"])
                self.sep_face_zone_by_shape = self.__class__.sep_face_zone_by_shape(service, version, mode, path + ["sep_face_zone_by_shape"])
                super().__init__(service, version, mode, path)
            class mark_faces_in_region(TUIMethod):
                """
                Mark faces in local region.
                """
            class sep_face_zone_by_angle(TUIMethod):
                """
                Move faces to a new zone based on significant angle.
                """
            class sep_face_zone_by_cnbor(TUIMethod):
                """
                Move faces to a new zone based on cell neighbors.
                """
            class sep_face_zone_by_mark(TUIMethod):
                """
                Move faces marked to new zone.
                """
            class sep_face_zone_by_region(TUIMethod):
                """
                Move non-contiguous faces or faces separated by an intersecting wall to a new zone.
                """
            class sep_face_zone_by_seed(TUIMethod):
                """
                Move faces connected to seed whose angle satisfies given angle constraint.
                """
            class sep_face_zone_by_seed_angle(TUIMethod):
                """
                Move faces connected to seed whose normal fall within the specified cone.
                """
            class sep_face_zone_by_shape(TUIMethod):
                """
                Move faces based on face shape.
                """

            class local_regions(TUIMenu):
                """
                Enter the separate-local menu.
                """
                def __init__(self, service, version, mode, path):
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class define(TUIMethod):
                    """
                    Define a refinement region's parameters.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region.
                    """
                class init(TUIMethod):
                    """
                    Delete all current regions and add the default refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    List all refinement regions.
                    """

        class shell_boundary_layer(TUIMenu):
            """
            Enter the shell boundary layer menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create shell boundary layers from one or more face zones.
                """

            class controls(TUIMenu):
                """
                Shell Boundary Layer Controls.
                """
                def __init__(self, service, version, mode, path):
                    self.zone_specific_growth = self.__class__.zone_specific_growth(service, version, mode, path + ["zone_specific_growth"])
                    super().__init__(service, version, mode, path)

                class zone_specific_growth(TUIMenu):
                    """
                    Shell boundary Layer Growth Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.apply_growth = self.__class__.apply_growth(service, version, mode, path + ["apply_growth"])
                        self.clear_growth = self.__class__.clear_growth(service, version, mode, path + ["clear_growth"])
                        super().__init__(service, version, mode, path)
                    class apply_growth(TUIMethod):
                        """
                        Apply  shell boundary la growth on individual edge zones.
                        """
                    class clear_growth(TUIMethod):
                        """
                        Clear shell boundary layer specific growth on individual edge zones.
                        """

    class cad_assemblies(TUIMenu):
        """
        Menu for cad assemblies.
        """
        def __init__(self, service, version, mode, path):
            self.draw_options = self.__class__.draw_options(service, version, mode, path + ["draw_options"])
            self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
            self.manage_state = self.__class__.manage_state(service, version, mode, path + ["manage_state"])
            self.update_options = self.__class__.update_options(service, version, mode, path + ["update_options"])
            self.add_prefix = self.__class__.add_prefix(service, version, mode, path + ["add_prefix"])
            self.add_to_object = self.__class__.add_to_object(service, version, mode, path + ["add_to_object"])
            self.create_objects = self.__class__.create_objects(service, version, mode, path + ["create_objects"])
            self.delete_cad_assemblies = self.__class__.delete_cad_assemblies(service, version, mode, path + ["delete_cad_assemblies"])
            self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
            self.extract_edges_zones = self.__class__.extract_edges_zones(service, version, mode, path + ["extract_edges_zones"])
            self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
            self.replace_object = self.__class__.replace_object(service, version, mode, path + ["replace_object"])
            self.update_cad_assemblies = self.__class__.update_cad_assemblies(service, version, mode, path + ["update_cad_assemblies"])
            super().__init__(service, version, mode, path)
        class add_prefix(TUIMethod):
            """
            Add Prefix to CAD entity.
            """
        class add_to_object(TUIMethod):
            """
            Add CAD assemblies to existing object.
            """
        class create_objects(TUIMethod):
            """
            Create Objects from CAD assemblies.
            """
        class delete_cad_assemblies(TUIMethod):
            """
            Delete CAD Assemblies.
            """
        class draw(TUIMethod):
            """
            Draw CAD assemblies.
            """
        class extract_edges_zones(TUIMethod):
            """
            Extract feature edges for CAD assemblies.
            """
        class rename(TUIMethod):
            """
            Rename CAD entity.
            """
        class replace_object(TUIMethod):
            """
            Replace CAD assemblies in existing object.
            """
        class update_cad_assemblies(TUIMethod):
            """
            Update CAD assemblies.
            """

        class draw_options(TUIMenu):
            """
            CAD draw options.
            """
            def __init__(self, service, version, mode, path):
                self.add_to_graphics = self.__class__.add_to_graphics(service, version, mode, path + ["add_to_graphics"])
                self.draw_unlabelled_zones = self.__class__.draw_unlabelled_zones(service, version, mode, path + ["draw_unlabelled_zones"])
                self.remove_from_graphics = self.__class__.remove_from_graphics(service, version, mode, path + ["remove_from_graphics"])
                super().__init__(service, version, mode, path)
            class add_to_graphics(TUIMethod):
                """
                Add CAD entity to graphics.
                """
            class draw_unlabelled_zones(TUIMethod):
                """
                Import edge zones for update.
                """
            class remove_from_graphics(TUIMethod):
                """
                Set one object per body, face or object.
                """

        class labels(TUIMenu):
            """
            CAD label options.
            """
            def __init__(self, service, version, mode, path):
                self.add_to_graphics = self.__class__.add_to_graphics(service, version, mode, path + ["add_to_graphics"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                self.remove_from_graphics = self.__class__.remove_from_graphics(service, version, mode, path + ["remove_from_graphics"])
                self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
                super().__init__(service, version, mode, path)
            class add_to_graphics(TUIMethod):
                """
                Add Labels to graphics.
                """
            class delete(TUIMethod):
                """
                Delete Labels.
                """
            class draw(TUIMethod):
                """
                Draw Labels.
                """
            class remove_from_graphics(TUIMethod):
                """
                Remove Labels from graphics.
                """
            class rename(TUIMethod):
                """
                Rename Labels.
                """

        class manage_state(TUIMenu):
            """
            States for CAD assemblies.
            """
            def __init__(self, service, version, mode, path):
                self.suppress = self.__class__.suppress(service, version, mode, path + ["suppress"])
                self.unlock = self.__class__.unlock(service, version, mode, path + ["unlock"])
                self.unsuppress = self.__class__.unsuppress(service, version, mode, path + ["unsuppress"])
                super().__init__(service, version, mode, path)
            class suppress(TUIMethod):
                """
                Suppress CAD assemblies.
                """
            class unlock(TUIMethod):
                """
                Unlock CAD assemblies.
                """
            class unsuppress(TUIMethod):
                """
                Unsuppress CAD assemblies.
                """

        class update_options(TUIMenu):
            """
            Settings for CAD update.
            """
            def __init__(self, service, version, mode, path):
                self.import_edge_zones = self.__class__.import_edge_zones(service, version, mode, path + ["import_edge_zones"])
                self.one_object_per = self.__class__.one_object_per(service, version, mode, path + ["one_object_per"])
                self.one_zone_per = self.__class__.one_zone_per(service, version, mode, path + ["one_zone_per"])
                self.tessellation = self.__class__.tessellation(service, version, mode, path + ["tessellation"])
                super().__init__(service, version, mode, path)
            class import_edge_zones(TUIMethod):
                """
                Import edge zones for update.
                """
            class one_object_per(TUIMethod):
                """
                Set one leaf entity per body, part or file.
                """
            class one_zone_per(TUIMethod):
                """
                Set one object per body, face or object.
                """
            class tessellation(TUIMethod):
                """
                Set tessellation controls for cad import.
                """

    class diagnostics(TUIMenu):
        """
        Diagnostic tools.
        """
        def __init__(self, service, version, mode, path):
            self.face_connectivity = self.__class__.face_connectivity(service, version, mode, path + ["face_connectivity"])
            self.quality = self.__class__.quality(service, version, mode, path + ["quality"])
            self.manage_summary = self.__class__.manage_summary(service, version, mode, path + ["manage_summary"])
            self.modify_defaults = self.__class__.modify_defaults(service, version, mode, path + ["modify_defaults"])
            self.perform_summary = self.__class__.perform_summary(service, version, mode, path + ["perform_summary"])
            self.set_scope = self.__class__.set_scope(service, version, mode, path + ["set_scope"])
            super().__init__(service, version, mode, path)
        class manage_summary(TUIMethod):
            """
            Manage diagnostics summary checks.
            """
        class modify_defaults(TUIMethod):
            """
            Modify diagnostics defaults.
            """
        class perform_summary(TUIMethod):
            """
            Performs diagnostics check and report in console.
            """
        class set_scope(TUIMethod):
            """
            Set Diagnostics scope.
            """

        class face_connectivity(TUIMenu):
            """
            Diagnose-face-connectivity.
            """
            def __init__(self, service, version, mode, path):
                self.add_label_to_small_neighbors = self.__class__.add_label_to_small_neighbors(service, version, mode, path + ["add_label_to_small_neighbors"])
                self.fix_deviations = self.__class__.fix_deviations(service, version, mode, path + ["fix_deviations"])
                self.fix_duplicate_faces = self.__class__.fix_duplicate_faces(service, version, mode, path + ["fix_duplicate_faces"])
                self.fix_free_faces = self.__class__.fix_free_faces(service, version, mode, path + ["fix_free_faces"])
                self.fix_invalid_normals = self.__class__.fix_invalid_normals(service, version, mode, path + ["fix_invalid_normals"])
                self.fix_islands = self.__class__.fix_islands(service, version, mode, path + ["fix_islands"])
                self.fix_multi_faces = self.__class__.fix_multi_faces(service, version, mode, path + ["fix_multi_faces"])
                self.fix_point_contacts = self.__class__.fix_point_contacts(service, version, mode, path + ["fix_point_contacts"])
                self.fix_self_intersections = self.__class__.fix_self_intersections(service, version, mode, path + ["fix_self_intersections"])
                self.fix_slivers = self.__class__.fix_slivers(service, version, mode, path + ["fix_slivers"])
                self.fix_spikes = self.__class__.fix_spikes(service, version, mode, path + ["fix_spikes"])
                self.fix_steps = self.__class__.fix_steps(service, version, mode, path + ["fix_steps"])
                self.remove_label_from_small_islands = self.__class__.remove_label_from_small_islands(service, version, mode, path + ["remove_label_from_small_islands"])
                super().__init__(service, version, mode, path)
            class add_label_to_small_neighbors(TUIMethod):
                """
                Change small connected islands label to input.
                """
            class fix_deviations(TUIMethod):
                """
                Fix deviations
                by imprinting edges for given set of face and edge zones or zones of each object individually.
                """
            class fix_duplicate_faces(TUIMethod):
                """
                Fix duplicate faces
                by deleting duplicate faces of given face zone list or all face zones of given objects.
                """
            class fix_free_faces(TUIMethod):
                """
                Fix free faces using
                merge-nodes - Individually on each object or on given face zone list
                stitch - Individually on each object or on given face zone list
                delete-free-edge-faces - Of given face zone list or all face zones of given objects
                delete-fringes - Of given face zone list or all face zones of given objects
                delete-skewed-faces - Of given face zone list or all face zones of given objects.
                """
            class fix_invalid_normals(TUIMethod):
                """
                Fix invalid normals
                by smoothing invalid normals from given face zone list or all face zones of given objects.
                """
            class fix_islands(TUIMethod):
                """
                Fix spikes
                by removing islands from given face zone list or all face zones of given objects.
                """
            class fix_multi_faces(TUIMethod):
                """
                Fix milti faces using
                delete-fringes - Of given face zone list or all face zones of given objects
                delete-overlaps - Of given face zone list or all face zones of given objects
                disconnect - Given face zone list or all face zones of given objects
                all-above - on given face zone list or all face zones of given objects.
                """
            class fix_point_contacts(TUIMethod):
                """
                Fix point contacts
                by removing point contacts from given face zone list or all face zones of given objects.
                """
            class fix_self_intersections(TUIMethod):
                """
                Fix self intersections
                fix-self-intersections - Of given face zone list or all face zones of given objects
                fix-folded-faces - Smooth folded faces of given face zone list or all face zones of given objects.
                """
            class fix_slivers(TUIMethod):
                """
                Fix Slivers
                by collapsing slivers from given face zone list or all face zones of given objects.
                """
            class fix_spikes(TUIMethod):
                """
                Fix spikes
                by smoothing spikes from given face zone list or all face zones of given objects.
                """
            class fix_steps(TUIMethod):
                """
                Fix steps
                smooth - Steps from given face zone list or all face zones of given objects
                collapse - Steps from given face zone list or all face zones of given objects.
                """
            class remove_label_from_small_islands(TUIMethod):
                """
                Change small disconnected island labels to their connected neighbors.
                """

        class quality(TUIMenu):
            """
            Diagnose-face-quality.
            """
            def __init__(self, service, version, mode, path):
                self.collapse = self.__class__.collapse(service, version, mode, path + ["collapse"])
                self.delaunay_swap = self.__class__.delaunay_swap(service, version, mode, path + ["delaunay_swap"])
                self.general_improve = self.__class__.general_improve(service, version, mode, path + ["general_improve"])
                self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                super().__init__(service, version, mode, path)
            class collapse(TUIMethod):
                """
                Collapse faces from given face zone list or all face zones of given objects.
                """
            class delaunay_swap(TUIMethod):
                """
                Delaunay swap the faces given face zone list or all face zones of given objects.
                """
            class general_improve(TUIMethod):
                """
                General Improve
                on  given face zone list or all face zones of given objects.
                """
            class smooth(TUIMethod):
                """
                Smooth individually on each object or on given face zone list.
                """

    class display(TUIMenu):
        """
        Enter the display menu.
        """
        def __init__(self, service, version, mode, path):
            self.advanced_rendering = self.__class__.advanced_rendering(service, version, mode, path + ["advanced_rendering"])
            self.display_states = self.__class__.display_states(service, version, mode, path + ["display_states"])
            self.objects = self.__class__.objects(service, version, mode, path + ["objects"])
            self.set = self.__class__.set(service, version, mode, path + ["set"])
            self.set_grid = self.__class__.set_grid(service, version, mode, path + ["set_grid"])
            self.update_scene = self.__class__.update_scene(service, version, mode, path + ["update_scene"])
            self.xy_plot = self.__class__.xy_plot(service, version, mode, path + ["xy_plot"])
            self.zones = self.__class__.zones(service, version, mode, path + ["zones"])
            self.all_grid = self.__class__.all_grid(service, version, mode, path + ["all_grid"])
            self.annotate = self.__class__.annotate(service, version, mode, path + ["annotate"])
            self.boundary_cells = self.__class__.boundary_cells(service, version, mode, path + ["boundary_cells"])
            self.boundary_grid = self.__class__.boundary_grid(service, version, mode, path + ["boundary_grid"])
            self.center_view_on = self.__class__.center_view_on(service, version, mode, path + ["center_view_on"])
            self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
            self.clear_annotation = self.__class__.clear_annotation(service, version, mode, path + ["clear_annotation"])
            self.draw_cells_using_faces = self.__class__.draw_cells_using_faces(service, version, mode, path + ["draw_cells_using_faces"])
            self.draw_cells_using_nodes = self.__class__.draw_cells_using_nodes(service, version, mode, path + ["draw_cells_using_nodes"])
            self.draw_face_zones_using_entities = self.__class__.draw_face_zones_using_entities(service, version, mode, path + ["draw_face_zones_using_entities"])
            self.draw_zones = self.__class__.draw_zones(service, version, mode, path + ["draw_zones"])
            self.redisplay = self.__class__.redisplay(service, version, mode, path + ["redisplay"])
            self.save_picture = self.__class__.save_picture(service, version, mode, path + ["save_picture"])
            self.set_list_tree_separator = self.__class__.set_list_tree_separator(service, version, mode, path + ["set_list_tree_separator"])
            self.show_hide_clipping_plane_triad = self.__class__.show_hide_clipping_plane_triad(service, version, mode, path + ["show_hide_clipping_plane_triad"])
            self.update_layout = self.__class__.update_layout(service, version, mode, path + ["update_layout"])
            self.views = self.__class__.views(service, version, mode, path + ["views"])
            super().__init__(service, version, mode, path)
        class all_grid(TUIMethod):
            """
            Display grid zones according to parameters in set-grid.
            """
        class annotate(TUIMethod):
            """
            Add a text annotation string to the active graphics window.
            """
        class boundary_cells(TUIMethod):
            """
            Display boundary cells on the specified face zones.
            """
        class boundary_grid(TUIMethod):
            """
            Display boundary zones on the specified face zones.
            """
        class center_view_on(TUIMethod):
            """
            Set camera target to be center (centroid) of grid node/face/cell.
            """
        class clear(TUIMethod):
            """
            Clear active graphics window.
            """
        class clear_annotation(TUIMethod):
            """
            Delete annotation text.
            """
        class draw_cells_using_faces(TUIMethod):
            """
            Draw cells using selected faces.
            """
        class draw_cells_using_nodes(TUIMethod):
            """
            Draw cells using selected nodes.
            """
        class draw_face_zones_using_entities(TUIMethod):
            """
            Draw face zone connected to node.
            """
        class draw_zones(TUIMethod):
            """
            Draw the specified zones using the default grid parameters.
            """
        class redisplay(TUIMethod):
            """
            Re-display grid.
            """
        class save_picture(TUIMethod):
            """
            Generate a "hardcopy" of the active window.
            """
        class set_list_tree_separator(TUIMethod):
            """
            Set the separator character for list tree.
            """
        class show_hide_clipping_plane_triad(TUIMethod):
            """
            Show/Hide clipping plane triad.
            """
        class update_layout(TUIMethod):
            """
            Update the fluent layout.
            """
        class views(TUIMethod):
            """
            Enter the view menu.
            """

        class advanced_rendering(TUIMenu):
            """
            Enter the advanced rendering menu.
            """
            def __init__(self, service, version, mode, path):
                self.edge_color = self.__class__.edge_color(service, version, mode, path + ["edge_color"])
                self.fast_silhouette_edges = self.__class__.fast_silhouette_edges(service, version, mode, path + ["fast_silhouette_edges"])
                self.max_extent_culling = self.__class__.max_extent_culling(service, version, mode, path + ["max_extent_culling"])
                self.simple_shadow = self.__class__.simple_shadow(service, version, mode, path + ["simple_shadow"])
                self.static_model = self.__class__.static_model(service, version, mode, path + ["static_model"])
                super().__init__(service, version, mode, path)
            class edge_color(TUIMethod):
                """
                Choose between black and body colored edges.
                """
            class fast_silhouette_edges(TUIMethod):
                """
                Enhances viewability by adding fast silhouette edges.
                """
            class max_extent_culling(TUIMethod):
                """
                Truncates zones smaller that the maximum extent culling pixel value.
                """
            class simple_shadow(TUIMethod):
                """
                Enhances viewability by adding a simple shadow.
                """
            class static_model(TUIMethod):
                """
                Static model driver setting.
                """

        class display_states(TUIMenu):
            """
            Enter the display state menu.
            """
            def __init__(self, service, version, mode, path):
                self.apply = self.__class__.apply(service, version, mode, path + ["apply"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.read = self.__class__.read(service, version, mode, path + ["read"])
                self.use_active = self.__class__.use_active(service, version, mode, path + ["use_active"])
                self.write = self.__class__.write(service, version, mode, path + ["write"])
                super().__init__(service, version, mode, path)
            class apply(TUIMethod):
                """
                Apply a display state to the active window.
                """
            class copy(TUIMethod):
                """
                Create a new display state with settings copied from an existing display state.
                """
            class create(TUIMethod):
                """
                Create a new display state.
                """
            class delete(TUIMethod):
                """
                Delete a display state.
                """
            class edit(TUIMethod):
                """
                Edit a particular display state setting.
                """
            class list(TUIMethod):
                """
                Print the names of the available display states to the console.
                """
            class read(TUIMethod):
                """
                Read display states from a file.
                """
            class use_active(TUIMethod):
                """
                Update an existing display state's settings to match those of the active graphics window.
                """
            class write(TUIMethod):
                """
                Write display states to a file.
                """

        class objects(TUIMenu):
            """
            Enter the objects menu.
            """
            def __init__(self, service, version, mode, path):
                self.display_neighborhood = self.__class__.display_neighborhood(service, version, mode, path + ["display_neighborhood"])
                self.display_similar_area = self.__class__.display_similar_area(service, version, mode, path + ["display_similar_area"])
                self.explode = self.__class__.explode(service, version, mode, path + ["explode"])
                self.hide_objects = self.__class__.hide_objects(service, version, mode, path + ["hide_objects"])
                self.implode = self.__class__.implode(service, version, mode, path + ["implode"])
                self.isolate_objects = self.__class__.isolate_objects(service, version, mode, path + ["isolate_objects"])
                self.make_transparent = self.__class__.make_transparent(service, version, mode, path + ["make_transparent"])
                self.select_all_visible = self.__class__.select_all_visible(service, version, mode, path + ["select_all_visible"])
                self.show_all = self.__class__.show_all(service, version, mode, path + ["show_all"])
                self.toggle_color_mode = self.__class__.toggle_color_mode(service, version, mode, path + ["toggle_color_mode"])
                self.toggle_color_palette = self.__class__.toggle_color_palette(service, version, mode, path + ["toggle_color_palette"])
                super().__init__(service, version, mode, path)
            class display_neighborhood(TUIMethod):
                """
                Displays neighboring objects also.
                """
            class display_similar_area(TUIMethod):
                """
                Shows all similar surface area objects.
                """
            class explode(TUIMethod):
                """
                Explode all displayed objects.
                """
            class hide_objects(TUIMethod):
                """
                Hide selected objects from view.
                """
            class implode(TUIMethod):
                """
                Implode all displayed objects.
                """
            class isolate_objects(TUIMethod):
                """
                Hide selected objects from view.
                """
            class make_transparent(TUIMethod):
                """
                Toggle Transparent view based on object selection.
                """
            class select_all_visible(TUIMethod):
                """
                Probe select all visible objects.
                """
            class show_all(TUIMethod):
                """
                Show all displayed objects.
                """
            class toggle_color_mode(TUIMethod):
                """
                Toggles color mode between color by objects/threads.
                """
            class toggle_color_palette(TUIMethod):
                """
                Toggle between default and classic color palettes.
                """

        class set(TUIMenu):
            """
            Menu to set display parameters.
            """
            def __init__(self, service, version, mode, path):
                self.colors = self.__class__.colors(service, version, mode, path + ["colors"])
                self.lights = self.__class__.lights(service, version, mode, path + ["lights"])
                self.picture = self.__class__.picture(service, version, mode, path + ["picture"])
                self.rendering_options = self.__class__.rendering_options(service, version, mode, path + ["rendering_options"])
                self.styles = self.__class__.styles(service, version, mode, path + ["styles"])
                self.edges = self.__class__.edges(service, version, mode, path + ["edges"])
                self.filled_grid = self.__class__.filled_grid(service, version, mode, path + ["filled_grid"])
                self.highlight_tree_selection = self.__class__.highlight_tree_selection(service, version, mode, path + ["highlight_tree_selection"])
                self.line_weight = self.__class__.line_weight(service, version, mode, path + ["line_weight"])
                self.native_display_defaults = self.__class__.native_display_defaults(service, version, mode, path + ["native_display_defaults"])
                self.overlays = self.__class__.overlays(service, version, mode, path + ["overlays"])
                self.quick_moves_algorithm = self.__class__.quick_moves_algorithm(service, version, mode, path + ["quick_moves_algorithm"])
                self.re_render = self.__class__.re_render(service, version, mode, path + ["re_render"])
                self.remote_display_defaults = self.__class__.remote_display_defaults(service, version, mode, path + ["remote_display_defaults"])
                self.reset_graphics = self.__class__.reset_graphics(service, version, mode, path + ["reset_graphics"])
                self.shrink_factor = self.__class__.shrink_factor(service, version, mode, path + ["shrink_factor"])
                self.title = self.__class__.title(service, version, mode, path + ["title"])
                self.windows = self.__class__.windows(service, version, mode, path + ["windows"])
                super().__init__(service, version, mode, path)
            class edges(TUIMethod):
                """
                Turn on/off display of face/cell edges.
                """
            class filled_grid(TUIMethod):
                """
                Turn on/off filled grid option.
                """
            class highlight_tree_selection(TUIMethod):
                """
                Turn on/off outline display of tree selection in graphics window.
                """
            class line_weight(TUIMethod):
                """
                Set the window's line-weight factor.
                """
            class native_display_defaults(TUIMethod):
                """
                Apply display settings recommended for native display.
                """
            class overlays(TUIMethod):
                """
                Turn on/off overlays.
                """
            class quick_moves_algorithm(TUIMethod):
                """
                Select quick moves algorithm for icons and helptext overlay.
                """
            class re_render(TUIMethod):
                """
                Re-render current window after modifying variables in set menu.
                """
            class remote_display_defaults(TUIMethod):
                """
                Apply display settings recommended for remote display.
                """
            class reset_graphics(TUIMethod):
                """
                Reset the graphics system.
                """
            class shrink_factor(TUIMethod):
                """
                Set grid shrink factor.
                """
            class title(TUIMethod):
                """
                Set problem title.
                """
            class windows(TUIMethod):
                """
                Window options menu.
                """

            class colors(TUIMenu):
                """
                Color options menu.
                """
                def __init__(self, service, version, mode, path):
                    self.by_surface = self.__class__.by_surface(service, version, mode, path + ["by_surface"])
                    self.by_type = self.__class__.by_type(service, version, mode, path + ["by_type"])
                    self.automatic_skip = self.__class__.automatic_skip(service, version, mode, path + ["automatic_skip"])
                    self.axis_faces = self.__class__.axis_faces(service, version, mode, path + ["axis_faces"])
                    self.background = self.__class__.background(service, version, mode, path + ["background"])
                    self.color_by = self.__class__.color_by(service, version, mode, path + ["color_by"])
                    self.color_by_type = self.__class__.color_by_type(service, version, mode, path + ["color_by_type"])
                    self.far_field_faces = self.__class__.far_field_faces(service, version, mode, path + ["far_field_faces"])
                    self.foreground = self.__class__.foreground(service, version, mode, path + ["foreground"])
                    self.free_surface_faces = self.__class__.free_surface_faces(service, version, mode, path + ["free_surface_faces"])
                    self.graphics_color_theme = self.__class__.graphics_color_theme(service, version, mode, path + ["graphics_color_theme"])
                    self.grid_inlet = self.__class__.grid_inlet(service, version, mode, path + ["grid_inlet"])
                    self.grid_interior = self.__class__.grid_interior(service, version, mode, path + ["grid_interior"])
                    self.highlight_color = self.__class__.highlight_color(service, version, mode, path + ["highlight_color"])
                    self.inlet_faces = self.__class__.inlet_faces(service, version, mode, path + ["inlet_faces"])
                    self.interface_faces = self.__class__.interface_faces(service, version, mode, path + ["interface_faces"])
                    self.interior_faces = self.__class__.interior_faces(service, version, mode, path + ["interior_faces"])
                    self.internal_faces = self.__class__.internal_faces(service, version, mode, path + ["internal_faces"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.outlet_faces = self.__class__.outlet_faces(service, version, mode, path + ["outlet_faces"])
                    self.overset_faces = self.__class__.overset_faces(service, version, mode, path + ["overset_faces"])
                    self.periodic_faces = self.__class__.periodic_faces(service, version, mode, path + ["periodic_faces"])
                    self.rans_les_interface_faces = self.__class__.rans_les_interface_faces(service, version, mode, path + ["rans_les_interface_faces"])
                    self.reset_colors = self.__class__.reset_colors(service, version, mode, path + ["reset_colors"])
                    self.reset_user_colors = self.__class__.reset_user_colors(service, version, mode, path + ["reset_user_colors"])
                    self.show_user_colors = self.__class__.show_user_colors(service, version, mode, path + ["show_user_colors"])
                    self.skip_label = self.__class__.skip_label(service, version, mode, path + ["skip_label"])
                    self.surface = self.__class__.surface(service, version, mode, path + ["surface"])
                    self.symmetry_faces = self.__class__.symmetry_faces(service, version, mode, path + ["symmetry_faces"])
                    self.traction_faces = self.__class__.traction_faces(service, version, mode, path + ["traction_faces"])
                    self.user_color = self.__class__.user_color(service, version, mode, path + ["user_color"])
                    self.wall_faces = self.__class__.wall_faces(service, version, mode, path + ["wall_faces"])
                    super().__init__(service, version, mode, path)
                class automatic_skip(TUIMethod):
                    """
                    Determine whether to skip labels in the colopmap scale automatically.
                    """
                class axis_faces(TUIMethod):
                    """
                    Set the color of axisymmetric faces.
                    """
                class background(TUIMethod):
                    """
                    Set the background (window) color.
                    """
                class color_by(TUIMethod):
                    """
                    Set the type to color the mesh.
                    """
                class color_by_type(TUIMethod):
                    """
                    Determine whether to color meshes by type or by surface (ID).
                    """
                class far_field_faces(TUIMethod):
                    """
                    Set the color of far field faces.
                    """
                class foreground(TUIMethod):
                    """
                    Set the foreground (text and window frame) color.
                    """
                class free_surface_faces(TUIMethod):
                    """
                    Set the color of free-surface faces.
                    """
                class graphics_color_theme(TUIMethod):
                    """
                    Enter the graphics color theme menu.
                    """
                class grid_inlet(TUIMethod):
                    """
                    Set the color of inlet faces.
                    """
                class grid_interior(TUIMethod):
                    """
                    Set the color of interior faces.
                    """
                class highlight_color(TUIMethod):
                    """
                    Set highlight color.
                    """
                class inlet_faces(TUIMethod):
                    """
                    Set the color of inlet faces.
                    """
                class interface_faces(TUIMethod):
                    """
                    Set the color of mesh Interfaces.
                    """
                class interior_faces(TUIMethod):
                    """
                    Set the color of interior faces.
                    """
                class internal_faces(TUIMethod):
                    """
                    Set the color of internal interface faces.
                    """
                class list(TUIMethod):
                    """
                    List available colors.
                    """
                class outlet_faces(TUIMethod):
                    """
                    Set the color of outlet faces.
                    """
                class overset_faces(TUIMethod):
                    """
                    Set the color of overset faces.
                    """
                class periodic_faces(TUIMethod):
                    """
                    Set the color of periodic faces.
                    """
                class rans_les_interface_faces(TUIMethod):
                    """
                    Set the color of RANS/LES interface faces.
                    """
                class reset_colors(TUIMethod):
                    """
                    Reset individual mesh surface colors to the defaults.
                    """
                class reset_user_colors(TUIMethod):
                    """
                    Reset all user colors.
                    """
                class show_user_colors(TUIMethod):
                    """
                    List currently defined user colors.
                    """
                class skip_label(TUIMethod):
                    """
                    Set the number of labels to be skipped in the colopmap scale.
                    """
                class surface(TUIMethod):
                    """
                    Set the color of surfaces.
                    """
                class symmetry_faces(TUIMethod):
                    """
                    Set the color of symmetric faces.
                    """
                class traction_faces(TUIMethod):
                    """
                    Set the color of traction faces.
                    """
                class user_color(TUIMethod):
                    """
                    Explicitly set color of display zone.
                    """
                class wall_faces(TUIMethod):
                    """
                    Set the color of wall faces.
                    """

                class by_surface(TUIMenu):
                    """
                    Enter the surface(s) color and material assignment menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.list_surfaces_by_color = self.__class__.list_surfaces_by_color(service, version, mode, path + ["list_surfaces_by_color"])
                        self.list_surfaces_by_material = self.__class__.list_surfaces_by_material(service, version, mode, path + ["list_surfaces_by_material"])
                        self.reset = self.__class__.reset(service, version, mode, path + ["reset"])
                        self.surfaces = self.__class__.surfaces(service, version, mode, path + ["surfaces"])
                        self.use_inherent_material_color = self.__class__.use_inherent_material_color(service, version, mode, path + ["use_inherent_material_color"])
                        super().__init__(service, version, mode, path)
                    class list_surfaces_by_color(TUIMethod):
                        """
                        To list the surfaces by its color.
                        """
                    class list_surfaces_by_material(TUIMethod):
                        """
                        To list the surfaces by its material.
                        """
                    class reset(TUIMethod):
                        """
                        To reset colors and/or materials to the defaults.
                        """
                    class surfaces(TUIMethod):
                        """
                        Select the surface(s) to specify colors and/or materials.
                        """
                    class use_inherent_material_color(TUIMethod):
                        """
                        Use inherent material color for surfaces.
                        """

                class by_type(TUIMenu):
                    """
                    Enter the zone type color and material assignment menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.type_name = self.__class__.type_name(service, version, mode, path + ["type_name"])
                        self.only_list_case_boundaries = self.__class__.only_list_case_boundaries(service, version, mode, path + ["only_list_case_boundaries"])
                        self.reset = self.__class__.reset(service, version, mode, path + ["reset"])
                        self.use_inherent_material_color = self.__class__.use_inherent_material_color(service, version, mode, path + ["use_inherent_material_color"])
                        super().__init__(service, version, mode, path)
                    class only_list_case_boundaries(TUIMethod):
                        """
                        Only list the boundary types that are assigned in this case.
                        """
                    class reset(TUIMethod):
                        """
                        To reset colors and/or materials to the defaults.
                        """
                    class use_inherent_material_color(TUIMethod):
                        """
                        Use inherent material color for boundary zones.
                        """

                    class type_name(TUIMenu):
                        """
                        Select the boundary type to specify colors and/or materials.
                        """
                        def __init__(self, service, version, mode, path):
                            self.axis = self.__class__.axis(service, version, mode, path + ["axis"])
                            self.far_field = self.__class__.far_field(service, version, mode, path + ["far_field"])
                            self.free_surface = self.__class__.free_surface(service, version, mode, path + ["free_surface"])
                            self.inlet = self.__class__.inlet(service, version, mode, path + ["inlet"])
                            self.interface = self.__class__.interface(service, version, mode, path + ["interface"])
                            self.interior = self.__class__.interior(service, version, mode, path + ["interior"])
                            self.internal = self.__class__.internal(service, version, mode, path + ["internal"])
                            self.outlet = self.__class__.outlet(service, version, mode, path + ["outlet"])
                            self.overset = self.__class__.overset(service, version, mode, path + ["overset"])
                            self.periodic = self.__class__.periodic(service, version, mode, path + ["periodic"])
                            self.rans_les_interface = self.__class__.rans_les_interface(service, version, mode, path + ["rans_les_interface"])
                            self.surface = self.__class__.surface(service, version, mode, path + ["surface"])
                            self.symmetry = self.__class__.symmetry(service, version, mode, path + ["symmetry"])
                            self.traction = self.__class__.traction(service, version, mode, path + ["traction"])
                            self.wall = self.__class__.wall(service, version, mode, path + ["wall"])
                            super().__init__(service, version, mode, path)

                        class axis(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class far_field(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class free_surface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class inlet(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class interface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class interior(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class internal(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class outlet(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class overset(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class periodic(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class rans_les_interface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class surface(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class symmetry(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class traction(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

                        class wall(TUIMenu):
                            """
                            Set the material and/or color for the selected boundary type.
                            """
                            def __init__(self, service, version, mode, path):
                                self.color = self.__class__.color(service, version, mode, path + ["color"])
                                self.material = self.__class__.material(service, version, mode, path + ["material"])
                                super().__init__(service, version, mode, path)
                            class color(TUIMethod):
                                """
                                Set a color for the selected boundary type.
                                """
                            class material(TUIMethod):
                                """
                                Set a material for the selected boundary type.
                                """

            class lights(TUIMenu):
                """
                Lights menu.
                """
                def __init__(self, service, version, mode, path):
                    self.headlight_on = self.__class__.headlight_on(service, version, mode, path + ["headlight_on"])
                    self.lighting_interpolation = self.__class__.lighting_interpolation(service, version, mode, path + ["lighting_interpolation"])
                    self.lights_on = self.__class__.lights_on(service, version, mode, path + ["lights_on"])
                    self.set_ambient_color = self.__class__.set_ambient_color(service, version, mode, path + ["set_ambient_color"])
                    self.set_light = self.__class__.set_light(service, version, mode, path + ["set_light"])
                    super().__init__(service, version, mode, path)
                class headlight_on(TUIMethod):
                    """
                    Turn the light that moves with the camera on or off.
                    """
                class lighting_interpolation(TUIMethod):
                    """
                    Set lighting interpolation method.
                    """
                class lights_on(TUIMethod):
                    """
                    Turn all active lighting on/off.
                    """
                class set_ambient_color(TUIMethod):
                    """
                    Set the ambient light color for the scene.
                    """
                class set_light(TUIMethod):
                    """
                    Add or modify a directional, colored light.
                    """

            class picture(TUIMenu):
                """
                Hardcopy options menu.
                """
                def __init__(self, service, version, mode, path):
                    self.color_mode = self.__class__.color_mode(service, version, mode, path + ["color_mode"])
                    self.driver = self.__class__.driver(service, version, mode, path + ["driver"])
                    self.dpi = self.__class__.dpi(service, version, mode, path + ["dpi"])
                    self.invert_background = self.__class__.invert_background(service, version, mode, path + ["invert_background"])
                    self.invert_normals_for_avz = self.__class__.invert_normals_for_avz(service, version, mode, path + ["invert_normals_for_avz"])
                    self.jpeg_hardcopy_quality = self.__class__.jpeg_hardcopy_quality(service, version, mode, path + ["jpeg_hardcopy_quality"])
                    self.landscape = self.__class__.landscape(service, version, mode, path + ["landscape"])
                    self.preview = self.__class__.preview(service, version, mode, path + ["preview"])
                    self.raytracer_image = self.__class__.raytracer_image(service, version, mode, path + ["raytracer_image"])
                    self.set_standard_resolution = self.__class__.set_standard_resolution(service, version, mode, path + ["set_standard_resolution"])
                    self.use_window_resolution = self.__class__.use_window_resolution(service, version, mode, path + ["use_window_resolution"])
                    self.x_resolution = self.__class__.x_resolution(service, version, mode, path + ["x_resolution"])
                    self.y_resolution = self.__class__.y_resolution(service, version, mode, path + ["y_resolution"])
                    super().__init__(service, version, mode, path)
                class dpi(TUIMethod):
                    """
                    Set the DPI for EPS and Postscript files, specifies the resolution in dots per inch (DPI) instead of setting the width and height.
                    """
                class invert_background(TUIMethod):
                    """
                    Use a white background when the picture is saved.
                    """
                class invert_normals_for_avz(TUIMethod):
                    """
                    In some cases, images exported to AVZ appear dark and do not match the true colors seen in the graphics window display. Enable 'invert-normals-for-avz' if you experience this issue.
                    """
                class jpeg_hardcopy_quality(TUIMethod):
                    """
                    To set jpeg hardcopy quality.
                    """
                class landscape(TUIMethod):
                    """
                    Plot hardcopies in landscape or portrait orientation.
                    """
                class preview(TUIMethod):
                    """
                    Display a preview image of a hardcopy.
                    """
                class raytracer_image(TUIMethod):
                    """
                    Enable raytracering rendering.
                    """
                class set_standard_resolution(TUIMethod):
                    """
                    Select from pre-defined resolution list.
                    """
                class use_window_resolution(TUIMethod):
                    """
                    Use the currently active window's resolution for hardcopy (ignores the x-resolution and y-resolution in this case).
                    """
                class x_resolution(TUIMethod):
                    """
                    Set the width of raster-formatted images in pixels (0 implies current window size).
                    """
                class y_resolution(TUIMethod):
                    """
                    Set the height of raster-formatted images in pixels (0 implies current window size).
                    """

                class color_mode(TUIMenu):
                    """
                    Enter the hardcopy color mode menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.color = self.__class__.color(service, version, mode, path + ["color"])
                        self.gray_scale = self.__class__.gray_scale(service, version, mode, path + ["gray_scale"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.mono_chrome = self.__class__.mono_chrome(service, version, mode, path + ["mono_chrome"])
                        super().__init__(service, version, mode, path)
                    class color(TUIMethod):
                        """
                        Plot hardcopies in color.
                        """
                    class gray_scale(TUIMethod):
                        """
                        Convert color to grayscale for hardcopy.
                        """
                    class list(TUIMethod):
                        """
                        Display the current hardcopy color mode.
                        """
                    class mono_chrome(TUIMethod):
                        """
                        Convert color to monochrome (black and white) for hardcopy.
                        """

                class driver(TUIMenu):
                    """
                    Enter the set hardcopy driver menu.
                    """
                    def __init__(self, service, version, mode, path):
                        self.post_format = self.__class__.post_format(service, version, mode, path + ["post_format"])
                        self.avz = self.__class__.avz(service, version, mode, path + ["avz"])
                        self.dump_window = self.__class__.dump_window(service, version, mode, path + ["dump_window"])
                        self.eps = self.__class__.eps(service, version, mode, path + ["eps"])
                        self.glb = self.__class__.glb(service, version, mode, path + ["glb"])
                        self.hsf = self.__class__.hsf(service, version, mode, path + ["hsf"])
                        self.jpeg = self.__class__.jpeg(service, version, mode, path + ["jpeg"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.options = self.__class__.options(service, version, mode, path + ["options"])
                        self.png = self.__class__.png(service, version, mode, path + ["png"])
                        self.post_script = self.__class__.post_script(service, version, mode, path + ["post_script"])
                        self.ppm = self.__class__.ppm(service, version, mode, path + ["ppm"])
                        self.tiff = self.__class__.tiff(service, version, mode, path + ["tiff"])
                        self.usd = self.__class__.usd(service, version, mode, path + ["usd"])
                        self.vrml = self.__class__.vrml(service, version, mode, path + ["vrml"])
                        super().__init__(service, version, mode, path)
                    class avz(TUIMethod):
                        """
                        Use AVZ output for hardcopies.
                        """
                    class dump_window(TUIMethod):
                        """
                        Set the command used to dump the graphics window to a file.
                        """
                    class eps(TUIMethod):
                        """
                        Produce encapsulated PostScript (EPS) output for hardcopies.
                        """
                    class glb(TUIMethod):
                        """
                        Use GLB output for hardcopies.
                        """
                    class hsf(TUIMethod):
                        """
                        Use HSF output for hardcopies.
                        """
                    class jpeg(TUIMethod):
                        """
                        Produce JPEG output for hardcopies.
                        """
                    class list(TUIMethod):
                        """
                        List the current hardcopy driver.
                        """
                    class options(TUIMethod):
                        """
                        Set the hardcopy options. Available options are:
                        "no gamma correction", disables gamma correction of colors,
                        "physical size = (width,height)", where width and height
                        are the actual measurements of the printable area of the page
                        in centimeters.
                        "subscreen = (left,right,bottom,top)", where left,right,
                        bottom, and top are numbers in [-1,1] describing a subwindow on
                        the page in which to place the hardcopy.
                        The options may be combined by separating them with commas.
                        """
                    class png(TUIMethod):
                        """
                        Use PNG output for hardcopies.
                        """
                    class post_script(TUIMethod):
                        """
                        Produce PostScript output for hardcopies.
                        """
                    class ppm(TUIMethod):
                        """
                        Produce PPM output for hardcopies.
                        """
                    class tiff(TUIMethod):
                        """
                        Use TIFF output for hardcopies.
                        """
                    class usd(TUIMethod):
                        """
                        Use USD output for hardcopies.
                        """
                    class vrml(TUIMethod):
                        """
                        Use VRML output for hardcopies.
                        """

                    class post_format(TUIMenu):
                        """
                        Enter the PostScript driver format menu.
                        """
                        def __init__(self, service, version, mode, path):
                            self.fast_raster = self.__class__.fast_raster(service, version, mode, path + ["fast_raster"])
                            self.raster = self.__class__.raster(service, version, mode, path + ["raster"])
                            self.rle_raster = self.__class__.rle_raster(service, version, mode, path + ["rle_raster"])
                            self.vector = self.__class__.vector(service, version, mode, path + ["vector"])
                            super().__init__(service, version, mode, path)
                        class fast_raster(TUIMethod):
                            """
                            Use the new raster format.
                            """
                        class raster(TUIMethod):
                            """
                            Use the original raster format.
                            """
                        class rle_raster(TUIMethod):
                            """
                            Use the run-length encoded raster format.
                            """
                        class vector(TUIMethod):
                            """
                            Use vector format.
                            """

            class rendering_options(TUIMenu):
                """
                Rendering options menu.
                """
                def __init__(self, service, version, mode, path):
                    self.animation_option = self.__class__.animation_option(service, version, mode, path + ["animation_option"])
                    self.auto_spin = self.__class__.auto_spin(service, version, mode, path + ["auto_spin"])
                    self.color_map_alignment = self.__class__.color_map_alignment(service, version, mode, path + ["color_map_alignment"])
                    self.device_info = self.__class__.device_info(service, version, mode, path + ["device_info"])
                    self.double_buffering = self.__class__.double_buffering(service, version, mode, path + ["double_buffering"])
                    self.driver = self.__class__.driver(service, version, mode, path + ["driver"])
                    self.face_displacement = self.__class__.face_displacement(service, version, mode, path + ["face_displacement"])
                    self.front_faces_transparent = self.__class__.front_faces_transparent(service, version, mode, path + ["front_faces_transparent"])
                    self.help_text_color = self.__class__.help_text_color(service, version, mode, path + ["help_text_color"])
                    self.hidden_line_method = self.__class__.hidden_line_method(service, version, mode, path + ["hidden_line_method"])
                    self.hidden_lines = self.__class__.hidden_lines(service, version, mode, path + ["hidden_lines"])
                    self.hidden_surface_method = self.__class__.hidden_surface_method(service, version, mode, path + ["hidden_surface_method"])
                    self.hidden_surfaces = self.__class__.hidden_surfaces(service, version, mode, path + ["hidden_surfaces"])
                    self.set_rendering_options = self.__class__.set_rendering_options(service, version, mode, path + ["set_rendering_options"])
                    self.show_colormap = self.__class__.show_colormap(service, version, mode, path + ["show_colormap"])
                    self.surface_edge_visibility = self.__class__.surface_edge_visibility(service, version, mode, path + ["surface_edge_visibility"])
                    super().__init__(service, version, mode, path)
                class animation_option(TUIMethod):
                    """
                    Using Wireframe / All option during animation.
                    """
                class auto_spin(TUIMethod):
                    """
                    Enable/disable mouse view rotations to continue to spin the display after the button is released.
                    """
                class color_map_alignment(TUIMethod):
                    """
                    Set the color bar alignment.
                    """
                class device_info(TUIMethod):
                    """
                    List information for the graphics device.
                    """
                class double_buffering(TUIMethod):
                    """
                    Enable/disable double-buffering.
                    """
                class driver(TUIMethod):
                    """
                    Change the current graphics driver.
                    """
                class face_displacement(TUIMethod):
                    """
                    Set face displacement value in Z-buffer units along the Camera Z-axis.
                    """
                class front_faces_transparent(TUIMethod):
                    """
                    Make the front faces transparent.
                    """
                class help_text_color(TUIMethod):
                    """
                    Set the color of screen help text.
                    """
                class hidden_line_method(TUIMethod):
                    """
                    Specify the method to perform hidden line rendering.
                    """
                class hidden_lines(TUIMethod):
                    """
                    Enable/disable hidden line removal.
                    """
                class hidden_surface_method(TUIMethod):
                    """
                    Specify the method to perform hidden line and hidden surface rendering.
                    """
                class hidden_surfaces(TUIMethod):
                    """
                    Enable/disable hidden surface removal.
                    """
                class set_rendering_options(TUIMethod):
                    """
                    Set the rendering options.
                    """
                class show_colormap(TUIMethod):
                    """
                    Enable/Disable colormap.
                    """
                class surface_edge_visibility(TUIMethod):
                    """
                    Set edge visibility flags for surfaces.
                    """

            class styles(TUIMenu):
                """
                Display style menu.
                """
                def __init__(self, service, version, mode, path):
                    self.dummy = self.__class__.dummy(service, version, mode, path + ["dummy"])
                    super().__init__(service, version, mode, path)
                class dummy(TUIMethod):
                    """
                    No help available.
                    """

        class set_grid(TUIMenu):
            """
            Enter the set-grid menu.
            """
            def __init__(self, service, version, mode, path):
                self.all_cells = self.__class__.all_cells(service, version, mode, path + ["all_cells"])
                self.all_faces = self.__class__.all_faces(service, version, mode, path + ["all_faces"])
                self.all_nodes = self.__class__.all_nodes(service, version, mode, path + ["all_nodes"])
                self.cell_quality = self.__class__.cell_quality(service, version, mode, path + ["cell_quality"])
                self.default = self.__class__.default(service, version, mode, path + ["default"])
                self.face_quality = self.__class__.face_quality(service, version, mode, path + ["face_quality"])
                self.free = self.__class__.free(service, version, mode, path + ["free"])
                self.label_alignment = self.__class__.label_alignment(service, version, mode, path + ["label_alignment"])
                self.label_font = self.__class__.label_font(service, version, mode, path + ["label_font"])
                self.label_scale = self.__class__.label_scale(service, version, mode, path + ["label_scale"])
                self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
                self.left_handed = self.__class__.left_handed(service, version, mode, path + ["left_handed"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.marked = self.__class__.marked(service, version, mode, path + ["marked"])
                self.multi = self.__class__.multi(service, version, mode, path + ["multi"])
                self.neighborhood = self.__class__.neighborhood(service, version, mode, path + ["neighborhood"])
                self.node_size = self.__class__.node_size(service, version, mode, path + ["node_size"])
                self.node_symbol = self.__class__.node_symbol(service, version, mode, path + ["node_symbol"])
                self.normal_scale = self.__class__.normal_scale(service, version, mode, path + ["normal_scale"])
                self.normals = self.__class__.normals(service, version, mode, path + ["normals"])
                self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                self.tagged = self.__class__.tagged(service, version, mode, path + ["tagged"])
                self.unmeshed = self.__class__.unmeshed(service, version, mode, path + ["unmeshed"])
                self.unused = self.__class__.unused(service, version, mode, path + ["unused"])
                self.x_range = self.__class__.x_range(service, version, mode, path + ["x_range"])
                self.y_range = self.__class__.y_range(service, version, mode, path + ["y_range"])
                self.z_range = self.__class__.z_range(service, version, mode, path + ["z_range"])
                super().__init__(service, version, mode, path)
            class all_cells(TUIMethod):
                """
                Draw all elements in cell zones.
                """
            class all_faces(TUIMethod):
                """
                Draw all elements in face zones.
                """
            class all_nodes(TUIMethod):
                """
                Draw all elements in node zones.
                """
            class cell_quality(TUIMethod):
                """
                Draw cells only in specified quality range.
                """
            class default(TUIMethod):
                """
                Reset all display variables to their default value.
                """
            class face_quality(TUIMethod):
                """
                Draw faces only in specified quality range.
                """
            class free(TUIMethod):
                """
                Draw free elements.
                """
            class label_alignment(TUIMethod):
                """
                Set label alignment; chose from "^v<>\\*".
                """
            class label_font(TUIMethod):
                """
                Set label font.
                """
            class label_scale(TUIMethod):
                """
                Set label scale.
                """
            class labels(TUIMethod):
                """
                Turn on/off labeling.
                """
            class left_handed(TUIMethod):
                """
                Draw left-handed elements.
                """
            class list(TUIMethod):
                """
                List display variables.
                """
            class marked(TUIMethod):
                """
                Draw marked elements.
                """
            class multi(TUIMethod):
                """
                Draw multiply-connected elements.
                """
            class neighborhood(TUIMethod):
                """
                Set display bounds to draw entities in the neighborhood of a entity.
                """
            class node_size(TUIMethod):
                """
                Set node symbol scaling factor.
                """
            class node_symbol(TUIMethod):
                """
                Set node symbol.
                """
            class normal_scale(TUIMethod):
                """
                Face normal scale.
                """
            class normals(TUIMethod):
                """
                Turn on/off face normals.
                """
            class refine(TUIMethod):
                """
                Draw refine marked elements.
                """
            class tagged(TUIMethod):
                """
                Draw tagged elements.
                """
            class unmeshed(TUIMethod):
                """
                Draw unmeshed elements.
                """
            class unused(TUIMethod):
                """
                Draw unused nodes.
                """
            class x_range(TUIMethod):
                """
                Draw only entities with x coordinates in specified range.
                """
            class y_range(TUIMethod):
                """
                Draw only entities with y coordinates in specified range.
                """
            class z_range(TUIMethod):
                """
                Draw only entities with z coordinates in specified range.
                """

        class update_scene(TUIMenu):
            """
            Enter the scene options menu.
            """
            def __init__(self, service, version, mode, path):
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.display = self.__class__.display(service, version, mode, path + ["display"])
                self.draw_frame = self.__class__.draw_frame(service, version, mode, path + ["draw_frame"])
                self.iso_sweep = self.__class__.iso_sweep(service, version, mode, path + ["iso_sweep"])
                self.overlays = self.__class__.overlays(service, version, mode, path + ["overlays"])
                self.pathline = self.__class__.pathline(service, version, mode, path + ["pathline"])
                self.select_geometry = self.__class__.select_geometry(service, version, mode, path + ["select_geometry"])
                self.set_frame = self.__class__.set_frame(service, version, mode, path + ["set_frame"])
                self.time = self.__class__.time(service, version, mode, path + ["time"])
                self.transform = self.__class__.transform(service, version, mode, path + ["transform"])
                super().__init__(service, version, mode, path)
            class delete(TUIMethod):
                """
                Delete selected geometries.
                """
            class display(TUIMethod):
                """
                Display selected geometries.
                """
            class draw_frame(TUIMethod):
                """
                Enable/disable drawing of the bounding frame.
                """
            class iso_sweep(TUIMethod):
                """
                Change iso-sweep values.
                """
            class overlays(TUIMethod):
                """
                Enable/disable the overlays option.
                """
            class pathline(TUIMethod):
                """
                Change pathline attributes.
                """
            class select_geometry(TUIMethod):
                """
                Select geometry to be updated.
                """
            class set_frame(TUIMethod):
                """
                Change frame options.
                """
            class time(TUIMethod):
                """
                Change time-step value.
                """
            class transform(TUIMethod):
                """
                Apply transformation matrix on selected geometries.
                """

        class xy_plot(TUIMenu):
            """
            Enter X-Y plot menu.
            """
            def __init__(self, service, version, mode, path):
                self.cell_distribution = self.__class__.cell_distribution(service, version, mode, path + ["cell_distribution"])
                self.face_distribution = self.__class__.face_distribution(service, version, mode, path + ["face_distribution"])
                self.file = self.__class__.file(service, version, mode, path + ["file"])
                self.set = self.__class__.set(service, version, mode, path + ["set"])
                super().__init__(service, version, mode, path)
            class cell_distribution(TUIMethod):
                """
                Display chart of distribution of cell quality.
                """
            class face_distribution(TUIMethod):
                """
                Display chart of distribution of face quality.
                """
            class file(TUIMethod):
                """
                Over-plot data from file.
                """
            class set(TUIMethod):
                """
                Set histogram plot parameters.
                """

        class zones(TUIMenu):
            """
            Enter the zones menu.
            """
            def __init__(self, service, version, mode, path):
                self.display_neighborhood = self.__class__.display_neighborhood(service, version, mode, path + ["display_neighborhood"])
                self.display_similar_area = self.__class__.display_similar_area(service, version, mode, path + ["display_similar_area"])
                self.hide_zones = self.__class__.hide_zones(service, version, mode, path + ["hide_zones"])
                self.isolate_zones = self.__class__.isolate_zones(service, version, mode, path + ["isolate_zones"])
                self.make_transparent = self.__class__.make_transparent(service, version, mode, path + ["make_transparent"])
                self.select_all_visible = self.__class__.select_all_visible(service, version, mode, path + ["select_all_visible"])
                self.show_all = self.__class__.show_all(service, version, mode, path + ["show_all"])
                self.toggle_color_mode = self.__class__.toggle_color_mode(service, version, mode, path + ["toggle_color_mode"])
                self.toggle_color_palette = self.__class__.toggle_color_palette(service, version, mode, path + ["toggle_color_palette"])
                super().__init__(service, version, mode, path)
            class display_neighborhood(TUIMethod):
                """
                Displays neighboring objects also.
                """
            class display_similar_area(TUIMethod):
                """
                Shows all similar surface area objects.
                """
            class hide_zones(TUIMethod):
                """
                Hide selected objects from view.
                """
            class isolate_zones(TUIMethod):
                """
                Hide selected objects from view.
                """
            class make_transparent(TUIMethod):
                """
                Toggle Transparent view based on object selection.
                """
            class select_all_visible(TUIMethod):
                """
                Probe select all visible objects.
                """
            class show_all(TUIMethod):
                """
                Show all displayed objects.
                """
            class toggle_color_mode(TUIMethod):
                """
                Toggles color mode between color by objects/threads.
                """
            class toggle_color_palette(TUIMethod):
                """
                Toggle between default and classic color palettes.
                """

    class file(TUIMenu):
        """
        Enter the file menu.
        """
        def __init__(self, service, version, mode, path):
            self.checkpoint = self.__class__.checkpoint(service, version, mode, path + ["checkpoint"])
            self.export = self.__class__.export(service, version, mode, path + ["export"])
            self.import_ = self.__class__.import_(service, version, mode, path + ["import_"])
            self.project_beta = self.__class__.project_beta(service, version, mode, path + ["project_beta"])
            self.append_mesh = self.__class__.append_mesh(service, version, mode, path + ["append_mesh"])
            self.append_meshes_by_tmerge = self.__class__.append_meshes_by_tmerge(service, version, mode, path + ["append_meshes_by_tmerge"])
            self.cff_files = self.__class__.cff_files(service, version, mode, path + ["cff_files"])
            self.confirm_overwrite = self.__class__.confirm_overwrite(service, version, mode, path + ["confirm_overwrite"])
            self.file_format = self.__class__.file_format(service, version, mode, path + ["file_format"])
            self.filter_list = self.__class__.filter_list(service, version, mode, path + ["filter_list"])
            self.filter_options = self.__class__.filter_options(service, version, mode, path + ["filter_options"])
            self.hdf_files = self.__class__.hdf_files(service, version, mode, path + ["hdf_files"])
            self.load_act_tool = self.__class__.load_act_tool(service, version, mode, path + ["load_act_tool"])
            self.read_boundary_mesh = self.__class__.read_boundary_mesh(service, version, mode, path + ["read_boundary_mesh"])
            self.read_case = self.__class__.read_case(service, version, mode, path + ["read_case"])
            self.read_domains = self.__class__.read_domains(service, version, mode, path + ["read_domains"])
            self.read_journal = self.__class__.read_journal(service, version, mode, path + ["read_journal"])
            self.read_mesh = self.__class__.read_mesh(service, version, mode, path + ["read_mesh"])
            self.read_mesh_vars = self.__class__.read_mesh_vars(service, version, mode, path + ["read_mesh_vars"])
            self.read_meshes_by_tmerge = self.__class__.read_meshes_by_tmerge(service, version, mode, path + ["read_meshes_by_tmerge"])
            self.read_multi_bound_mesh = self.__class__.read_multi_bound_mesh(service, version, mode, path + ["read_multi_bound_mesh"])
            self.read_multiple_mesh = self.__class__.read_multiple_mesh(service, version, mode, path + ["read_multiple_mesh"])
            self.read_options = self.__class__.read_options(service, version, mode, path + ["read_options"])
            self.read_size_field = self.__class__.read_size_field(service, version, mode, path + ["read_size_field"])
            self.set_idle_timeout = self.__class__.set_idle_timeout(service, version, mode, path + ["set_idle_timeout"])
            self.set_tui_version = self.__class__.set_tui_version(service, version, mode, path + ["set_tui_version"])
            self.show_configuration = self.__class__.show_configuration(service, version, mode, path + ["show_configuration"])
            self.start_journal = self.__class__.start_journal(service, version, mode, path + ["start_journal"])
            self.start_transcript = self.__class__.start_transcript(service, version, mode, path + ["start_transcript"])
            self.stop_journal = self.__class__.stop_journal(service, version, mode, path + ["stop_journal"])
            self.stop_transcript = self.__class__.stop_transcript(service, version, mode, path + ["stop_transcript"])
            self.write_boundaries = self.__class__.write_boundaries(service, version, mode, path + ["write_boundaries"])
            self.write_case = self.__class__.write_case(service, version, mode, path + ["write_case"])
            self.write_domains = self.__class__.write_domains(service, version, mode, path + ["write_domains"])
            self.write_mesh = self.__class__.write_mesh(service, version, mode, path + ["write_mesh"])
            self.write_mesh_vars = self.__class__.write_mesh_vars(service, version, mode, path + ["write_mesh_vars"])
            self.write_options = self.__class__.write_options(service, version, mode, path + ["write_options"])
            self.write_size_field = self.__class__.write_size_field(service, version, mode, path + ["write_size_field"])
            super().__init__(service, version, mode, path)
        class append_mesh(TUIMethod):
            """
            Append a new mesh to the existing mesh.
            """
        class append_meshes_by_tmerge(TUIMethod):
            """
            Append mesh files, or the meshes from case files.
            """
        class cff_files(TUIMethod):
            """
            Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
            """
        class confirm_overwrite(TUIMethod):
            """
            Indicate whether or not to confirm attempts to overwrite existing files.
            """
        class file_format(TUIMethod):
            """
            Indicate whether to write formatted or unformatted files.
            """
        class filter_list(TUIMethod):
            """
            List all filter names.
            """
        class filter_options(TUIMethod):
            """
            Change filter extension and/or its arguments.
            """
        class hdf_files(TUIMethod):
            """
            Indicate whether to write Ansys common fluids format (CFF) files or legacy case files.
            """
        class load_act_tool(TUIMethod):
            """
            Load ACT Start Page.
            """
        class read_boundary_mesh(TUIMethod):
            """
            Read the boundary mesh from either a mesh or case file.
            """
        class read_case(TUIMethod):
            """
            Read a case file.
            """
        class read_domains(TUIMethod):
            """
            Read TGrid domains from a file.
            """
        class read_journal(TUIMethod):
            """
            Start a main-menu that takes its input from a file.
            """
        class read_mesh(TUIMethod):
            """
            Read a mesh file, or the mesh from a case file.
            """
        class read_mesh_vars(TUIMethod):
            """
            Reads mesh varaibles from a mesh file.
            """
        class read_meshes_by_tmerge(TUIMethod):
            """
            Read mesh files, or the meshes from case files.
            """
        class read_multi_bound_mesh(TUIMethod):
            """
            Read multiple boundary meshes.
            """
        class read_multiple_mesh(TUIMethod):
            """
            Read multiple mesh files, or the meshes from multiple case files.
            """
        class read_options(TUIMethod):
            """
            Set read options.
            """
        class read_size_field(TUIMethod):
            """
            Read TGrid Size-field from a file.
            """
        class set_idle_timeout(TUIMethod):
            """
            Set the idle timeout.
            """
        class set_tui_version(TUIMethod):
            """
            Set the version of the TUI commands.
            """
        class show_configuration(TUIMethod):
            """
            Display current release and version information.
            """
        class start_journal(TUIMethod):
            """
            Start recording all input in a file.
            """
        class start_transcript(TUIMethod):
            """
            Start recording input and output in a file.
            """
        class stop_journal(TUIMethod):
            """
            Stop recording input and close journal file.
            """
        class stop_transcript(TUIMethod):
            """
            Stop recording input and output and close transcript file.
            """
        class write_boundaries(TUIMethod):
            """
            Write the mesh file of selected boundary face zones.
            """
        class write_case(TUIMethod):
            """
            Write the mesh to a case file.
            """
        class write_domains(TUIMethod):
            """
            Write all (except global) domains of the mesh into a file.
            """
        class write_mesh(TUIMethod):
            """
            Write a mesh file.
            """
        class write_mesh_vars(TUIMethod):
            """
            Writes mesh varaibles to a file.
            """
        class write_options(TUIMethod):
            """
            Set write options.
            """
        class write_size_field(TUIMethod):
            """
            Write TGrid Size-field into a file.
            """

        class checkpoint(TUIMenu):
            """
            Checkpoint stores the mesh in the memory instead of writing it to a file.
            """
            def __init__(self, service, version, mode, path):
                self.delete_checkpoint = self.__class__.delete_checkpoint(service, version, mode, path + ["delete_checkpoint"])
                self.list_checkpoint_names = self.__class__.list_checkpoint_names(service, version, mode, path + ["list_checkpoint_names"])
                self.restore_checkpoint = self.__class__.restore_checkpoint(service, version, mode, path + ["restore_checkpoint"])
                self.write_checkpoint = self.__class__.write_checkpoint(service, version, mode, path + ["write_checkpoint"])
                super().__init__(service, version, mode, path)
            class delete_checkpoint(TUIMethod):
                """
                Delete checkpoint.
                """
            class list_checkpoint_names(TUIMethod):
                """
                Get all checkpoint names.
                """
            class restore_checkpoint(TUIMethod):
                """
                Restore to checkpoint.
                """
            class write_checkpoint(TUIMethod):
                """
                Write checkpoint.
                """

        class export(TUIMenu):
            """
            Export surface and volume meshes to non-native formats.
            """
            def __init__(self, service, version, mode, path):
                self.ansys = self.__class__.ansys(service, version, mode, path + ["ansys"])
                self.hypermesh = self.__class__.hypermesh(service, version, mode, path + ["hypermesh"])
                self.nastran = self.__class__.nastran(service, version, mode, path + ["nastran"])
                self.patran = self.__class__.patran(service, version, mode, path + ["patran"])
                self.stl = self.__class__.stl(service, version, mode, path + ["stl"])
                super().__init__(service, version, mode, path)
            class ansys(TUIMethod):
                """
                Write a Ansys mesh file.
                """
            class hypermesh(TUIMethod):
                """
                Write a HYPERMESH ascii file.
                """
            class nastran(TUIMethod):
                """
                Write a NASTRAN mesh file.
                """
            class patran(TUIMethod):
                """
                Write a PATRAN mesh file.
                """
            class stl(TUIMethod):
                """
                Write a STL boundary mesh file.
                """

        class import_(TUIMenu):
            """
            Import surface and volume meshes from non-native formats.
            """
            def __init__(self, service, version, mode, path):
                self.cad_options = self.__class__.cad_options(service, version, mode, path + ["cad_options"])
                self.ansys_surf_mesh = self.__class__.ansys_surf_mesh(service, version, mode, path + ["ansys_surf_mesh"])
                self.ansys_vol_mesh = self.__class__.ansys_vol_mesh(service, version, mode, path + ["ansys_vol_mesh"])
                self.cad = self.__class__.cad(service, version, mode, path + ["cad"])
                self.cad_geometry = self.__class__.cad_geometry(service, version, mode, path + ["cad_geometry"])
                self.cgns_surf_mesh = self.__class__.cgns_surf_mesh(service, version, mode, path + ["cgns_surf_mesh"])
                self.cgns_vol_mesh = self.__class__.cgns_vol_mesh(service, version, mode, path + ["cgns_vol_mesh"])
                self.distributed_parallel_stride_import = self.__class__.distributed_parallel_stride_import(service, version, mode, path + ["distributed_parallel_stride_import"])
                self.fidap_surf_mesh = self.__class__.fidap_surf_mesh(service, version, mode, path + ["fidap_surf_mesh"])
                self.fidap_vol_mesh = self.__class__.fidap_vol_mesh(service, version, mode, path + ["fidap_vol_mesh"])
                self.fl_uns2_mesh = self.__class__.fl_uns2_mesh(service, version, mode, path + ["fl_uns2_mesh"])
                self.fluent_2d_mesh = self.__class__.fluent_2d_mesh(service, version, mode, path + ["fluent_2d_mesh"])
                self.fluent_3d_mesh = self.__class__.fluent_3d_mesh(service, version, mode, path + ["fluent_3d_mesh"])
                self.gambit_surf_mesh = self.__class__.gambit_surf_mesh(service, version, mode, path + ["gambit_surf_mesh"])
                self.gambit_vol_mesh = self.__class__.gambit_vol_mesh(service, version, mode, path + ["gambit_vol_mesh"])
                self.hypermesh_surf_mesh = self.__class__.hypermesh_surf_mesh(service, version, mode, path + ["hypermesh_surf_mesh"])
                self.hypermesh_vol_mesh = self.__class__.hypermesh_vol_mesh(service, version, mode, path + ["hypermesh_vol_mesh"])
                self.ideas_surf_mesh = self.__class__.ideas_surf_mesh(service, version, mode, path + ["ideas_surf_mesh"])
                self.ideas_vol_mesh = self.__class__.ideas_vol_mesh(service, version, mode, path + ["ideas_vol_mesh"])
                self.nastran_surf_mesh = self.__class__.nastran_surf_mesh(service, version, mode, path + ["nastran_surf_mesh"])
                self.nastran_vol_mesh = self.__class__.nastran_vol_mesh(service, version, mode, path + ["nastran_vol_mesh"])
                self.patran_surf_mesh = self.__class__.patran_surf_mesh(service, version, mode, path + ["patran_surf_mesh"])
                self.patran_vol_mesh = self.__class__.patran_vol_mesh(service, version, mode, path + ["patran_vol_mesh"])
                self.reimport_last_with_cfd_surface_mesh = self.__class__.reimport_last_with_cfd_surface_mesh(service, version, mode, path + ["reimport_last_with_cfd_surface_mesh"])
                self.stl = self.__class__.stl(service, version, mode, path + ["stl"])
                super().__init__(service, version, mode, path)
            class ansys_surf_mesh(TUIMethod):
                """
                Read a surface mesh from an Ansys prep7 or cdb file.
                """
            class ansys_vol_mesh(TUIMethod):
                """
                Read a volume mesh from an Ansys prep7 or cdb file.
                """
            class cad(TUIMethod):
                """
                Reads the following CAD formats:
                ACIS  \\*.sat, \\*.sab
                Ansys DesignModeler  \\*.agdb
                Ansys ICEM CFD  \\*.tin
                Ansys Workbench  \\*.meshdat, \\*.mechdat
                Autodesk Inventor  \\*.ipt, \\*.iam
                CATIA V4  \\*.model, \\*.exp, \\*.session, \\*.dlv
                CATIA V5  \\*.CATPart, \\*.CATProduct
                Creo Parametric  \\*.prt, \\*.asm
                GAMBIT  \\*.dbs
                IGES  \\*.igs, \\*.iges
                JTOpen  \\*.jt
                NX  \\*.prt
                Parasolid  \\*.x_t, \\*.xmt_txt, \\*.x_b, \\*.xmt_bin
                SolidWorks  \\*.sldprt, \\*.sldasm
                STEP  \\*.stp, \\*.step
                STL  \\*.stl.
                """
            class cad_geometry(TUIMethod):
                """
                Reads the following CAD formats:
                ACIS  \\*.sat, \\*.sab
                Ansys DesignModeler  \\*.agdb
                Ansys ICEM CFD  \\*.tin
                Ansys Workbench  \\*.meshdat, \\*.mechdat
                Autodesk Inventor  \\*.ipt, \\*.iam
                CATIA V4  \\*.model, \\*.exp, \\*.session, \\*.dlv
                CATIA V5  \\*.CATPart, \\*.CATProduct
                Creo Parametric  \\*.prt, \\*.asm
                GAMBIT  \\*.dbs
                IGES  \\*.igs, \\*.iges
                JTOpen  \\*.jt
                NX  \\*.prt
                Parasolid  \\*.x_t, \\*.xmt_txt, \\*.x_b, \\*.xmt_bin
                SolidWorks  \\*.sldprt, \\*.sldasm
                STEP  \\*.stp, \\*.step
                STL  \\*.stl.
                """
            class cgns_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a CGNS format file.
                """
            class cgns_vol_mesh(TUIMethod):
                """
                Read a volume mesh from an CGNS format file.
                """
            class distributed_parallel_stride_import(TUIMethod):
                """
                Read a cad file using distributed parallel stride import.
                """
            class fidap_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a FIDAP neutral file.
                """
            class fidap_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a FIDAP neutral file.
                """
            class fl_uns2_mesh(TUIMethod):
                """
                Read a mesh from a Fluent UNS V2 case file.
                """
            class fluent_2d_mesh(TUIMethod):
                """
                Read a 2D mesh.
                """
            class fluent_3d_mesh(TUIMethod):
                """
                Read a 3D mesh.
                """
            class gambit_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a GAMBIT neutral file.
                """
            class gambit_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a GAMBIT neutral file.
                """
            class hypermesh_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a HYPERMESH ascii file.
                """
            class hypermesh_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a HYPERMESH ascii file.
                """
            class ideas_surf_mesh(TUIMethod):
                """
                Read a surface mesh from an IDEAS universal file.
                """
            class ideas_vol_mesh(TUIMethod):
                """
                Read a volume mesh from an IDEAS universal file.
                """
            class nastran_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a NASTRAN file.
                """
            class nastran_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a NASTRAN file.
                """
            class patran_surf_mesh(TUIMethod):
                """
                Read a surface mesh from a PATRAN neutral file.
                """
            class patran_vol_mesh(TUIMethod):
                """
                Read a volume mesh from a PATRAN neutral file.
                """
            class reimport_last_with_cfd_surface_mesh(TUIMethod):
                """
                Reimport CAD using the size field.
                """
            class stl(TUIMethod):
                """
                Read a surface mesh from a stereolithography (STL) file.
                """

            class cad_options(TUIMenu):
                """
                Make settings for cad import.
                """
                def __init__(self, service, version, mode, path):
                    self.continue_on_error = self.__class__.continue_on_error(service, version, mode, path + ["continue_on_error"])
                    self.create_cad_assemblies = self.__class__.create_cad_assemblies(service, version, mode, path + ["create_cad_assemblies"])
                    self.create_label_per_body_during_cad_faceting = self.__class__.create_label_per_body_during_cad_faceting(service, version, mode, path + ["create_label_per_body_during_cad_faceting"])
                    self.derive_zone_name_from_object_scope = self.__class__.derive_zone_name_from_object_scope(service, version, mode, path + ["derive_zone_name_from_object_scope"])
                    self.double_connected_face_label = self.__class__.double_connected_face_label(service, version, mode, path + ["double_connected_face_label"])
                    self.enclosure_symm_processing = self.__class__.enclosure_symm_processing(service, version, mode, path + ["enclosure_symm_processing"])
                    self.extract_features = self.__class__.extract_features(service, version, mode, path + ["extract_features"])
                    self.import_body_names = self.__class__.import_body_names(service, version, mode, path + ["import_body_names"])
                    self.import_curvature_data_from_CAD = self.__class__.import_curvature_data_from_CAD(service, version, mode, path + ["import_curvature_data_from_CAD"])
                    self.import_label_for_body_named_selection = self.__class__.import_label_for_body_named_selection(service, version, mode, path + ["import_label_for_body_named_selection"])
                    self.import_part_names = self.__class__.import_part_names(service, version, mode, path + ["import_part_names"])
                    self.merge_nodes = self.__class__.merge_nodes(service, version, mode, path + ["merge_nodes"])
                    self.merge_objects_per_body_named_selection = self.__class__.merge_objects_per_body_named_selection(service, version, mode, path + ["merge_objects_per_body_named_selection"])
                    self.modify_all_duplicate_names = self.__class__.modify_all_duplicate_names(service, version, mode, path + ["modify_all_duplicate_names"])
                    self.name_separator_character = self.__class__.name_separator_character(service, version, mode, path + ["name_separator_character"])
                    self.named_selection_tessellation_failure = self.__class__.named_selection_tessellation_failure(service, version, mode, path + ["named_selection_tessellation_failure"])
                    self.named_selections = self.__class__.named_selections(service, version, mode, path + ["named_selections"])
                    self.object_type = self.__class__.object_type(service, version, mode, path + ["object_type"])
                    self.one_face_zone_per = self.__class__.one_face_zone_per(service, version, mode, path + ["one_face_zone_per"])
                    self.one_object_per = self.__class__.one_object_per(service, version, mode, path + ["one_object_per"])
                    self.read_all_cad_in_subdirectories = self.__class__.read_all_cad_in_subdirectories(service, version, mode, path + ["read_all_cad_in_subdirectories"])
                    self.reconstruct_topology = self.__class__.reconstruct_topology(service, version, mode, path + ["reconstruct_topology"])
                    self.replacement_character = self.__class__.replacement_character(service, version, mode, path + ["replacement_character"])
                    self.save_PMDB = self.__class__.save_PMDB(service, version, mode, path + ["save_PMDB"])
                    self.separate_features_by_type = self.__class__.separate_features_by_type(service, version, mode, path + ["separate_features_by_type"])
                    self.single_connected_edge_label = self.__class__.single_connected_edge_label(service, version, mode, path + ["single_connected_edge_label"])
                    self.strip_file_name_extension_from_naming = self.__class__.strip_file_name_extension_from_naming(service, version, mode, path + ["strip_file_name_extension_from_naming"])
                    self.strip_path_prefix_from_names = self.__class__.strip_path_prefix_from_names(service, version, mode, path + ["strip_path_prefix_from_names"])
                    self.tessellation = self.__class__.tessellation(service, version, mode, path + ["tessellation"])
                    self.use_body_names = self.__class__.use_body_names(service, version, mode, path + ["use_body_names"])
                    self.use_collection_names = self.__class__.use_collection_names(service, version, mode, path + ["use_collection_names"])
                    self.use_component_names = self.__class__.use_component_names(service, version, mode, path + ["use_component_names"])
                    self.use_part_names = self.__class__.use_part_names(service, version, mode, path + ["use_part_names"])
                    self.use_part_or_body_names_as_suffix_to_named_selections = self.__class__.use_part_or_body_names_as_suffix_to_named_selections(service, version, mode, path + ["use_part_or_body_names_as_suffix_to_named_selections"])
                    super().__init__(service, version, mode, path)
                class continue_on_error(TUIMethod):
                    """
                    Continue on error during cad import.
                    """
                class create_cad_assemblies(TUIMethod):
                    """
                    Import CAD Assemblies.
                    """
                class create_label_per_body_during_cad_faceting(TUIMethod):
                    """
                    Create label Per Body during cad faceting.
                    """
                class derive_zone_name_from_object_scope(TUIMethod):
                    """
                    Derive zone names from object scope.
                    """
                class double_connected_face_label(TUIMethod):
                    """
                    Double connected face label for CAD files.
                    """
                class enclosure_symm_processing(TUIMethod):
                    """
                    Processing of enclosure and symmetry named selections during import.
                    """
                class extract_features(TUIMethod):
                    """
                    Set the feature angle.
                    """
                class import_body_names(TUIMethod):
                    """
                    Import Body names from the CAD files.
                    """
                class import_curvature_data_from_CAD(TUIMethod):
                    """
                    Import Curvature Data from CAD.
                    """
                class import_label_for_body_named_selection(TUIMethod):
                    """
                    Import face zone labels for body named selections.
                    """
                class import_part_names(TUIMethod):
                    """
                    Import Part names from the CAD files.
                    """
                class merge_nodes(TUIMethod):
                    """
                    Merge Nodes for CAD import.
                    """
                class merge_objects_per_body_named_selection(TUIMethod):
                    """
                    Merge Objects per body named selection.
                    """
                class modify_all_duplicate_names(TUIMethod):
                    """
                    Modify all duplicate names by suffixing it with incremental integers.
                    """
                class name_separator_character(TUIMethod):
                    """
                    Character to be used as a separator in all names.
                    """
                class named_selection_tessellation_failure(TUIMethod):
                    """
                    Set named selection for CFD surface mesh failures.
                    """
                class named_selections(TUIMethod):
                    """
                    Allows to import Named Selections from the CAD file.
                    """
                class object_type(TUIMethod):
                    """
                    Object type for CAD files.
                    """
                class one_face_zone_per(TUIMethod):
                    """
                    Set one object per body, face or object.
                    """
                class one_object_per(TUIMethod):
                    """
                    Set one object per body, part or file.
                    """
                class read_all_cad_in_subdirectories(TUIMethod):
                    """
                    Recursive search for CAD files in sub-directories.
                    """
                class reconstruct_topology(TUIMethod):
                    """
                    Reconstruct topology for STL files.
                    """
                class replacement_character(TUIMethod):
                    """
                    Name replacement character.
                    """
                class save_PMDB(TUIMethod):
                    """
                    Saves PMDB file in the directory containing the CAD files imported.
                    """
                class separate_features_by_type(TUIMethod):
                    """
                    Separate features by type.
                    """
                class single_connected_edge_label(TUIMethod):
                    """
                    Single connected edge label for CAD files.
                    """
                class strip_file_name_extension_from_naming(TUIMethod):
                    """
                    Strip file name extension from naming.
                    """
                class strip_path_prefix_from_names(TUIMethod):
                    """
                    Strip path prefixes from naming.
                    """
                class tessellation(TUIMethod):
                    """
                    Set tessellation controls for cad import.
                    """
                class use_body_names(TUIMethod):
                    """
                    Use body names for CAD files.
                    """
                class use_collection_names(TUIMethod):
                    """
                    Use collection names for CAD files.
                    """
                class use_component_names(TUIMethod):
                    """
                    Use component names for CAD files.
                    """
                class use_part_names(TUIMethod):
                    """
                    Use part names for CAD files.
                    """
                class use_part_or_body_names_as_suffix_to_named_selections(TUIMethod):
                    """
                    Part or Body names are used as suffix for named selections spanning over multiple parts or bodies.
                    """

        class project_beta(TUIMenu):
            """
            Enter to create new project, open project, save and archive project.
            """
            def __init__(self, service, version, mode, path):
                self.simulation = self.__class__.simulation(service, version, mode, path + ["simulation"])
                self.archive = self.__class__.archive(service, version, mode, path + ["archive"])
                self.new = self.__class__.new(service, version, mode, path + ["new"])
                self.open = self.__class__.open(service, version, mode, path + ["open"])
                self.save = self.__class__.save(service, version, mode, path + ["save"])
                self.save_as = self.__class__.save_as(service, version, mode, path + ["save_as"])
                self.save_as_copy = self.__class__.save_as_copy(service, version, mode, path + ["save_as_copy"])
                super().__init__(service, version, mode, path)
            class archive(TUIMethod):
                """
                Archive Project.
                """
            class new(TUIMethod):
                """
                Create New Project.
                """
            class open(TUIMethod):
                """
                Open project.
                """
            class save(TUIMethod):
                """
                Save Project.
                """
            class save_as(TUIMethod):
                """
                Save As Project.
                """
            class save_as_copy(TUIMethod):
                """
                Save As Copy.
                """

            class simulation(TUIMenu):
                """
                Enter to create, duplicate, or delete a simulation.
                """
                def __init__(self, service, version, mode, path):
                    self.run = self.__class__.run(service, version, mode, path + ["run"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.new_simulation = self.__class__.new_simulation(service, version, mode, path + ["new_simulation"])
                    self.set_as_current = self.__class__.set_as_current(service, version, mode, path + ["set_as_current"])
                    super().__init__(service, version, mode, path)
                class delete(TUIMethod):
                    """
                    Delete A Simulation.
                    """
                class new_simulation(TUIMethod):
                    """
                    Create New Simulation.
                    """
                class set_as_current(TUIMethod):
                    """
                    Set the Current Simulation.
                    """

                class run(TUIMenu):
                    """
                    Enter to create, duplicate, or delete a run.
                    """
                    def __init__(self, service, version, mode, path):
                        self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                        self.new_run = self.__class__.new_run(service, version, mode, path + ["new_run"])
                        self.set_as_current = self.__class__.set_as_current(service, version, mode, path + ["set_as_current"])
                        super().__init__(service, version, mode, path)
                    class delete(TUIMethod):
                        """
                        Delete A Run.
                        """
                    class new_run(TUIMethod):
                        """
                        Create a New Run.
                        """
                    class set_as_current(TUIMethod):
                        """
                        Set the Current Run.
                        """

    class material_point(TUIMenu):
        """
        Manage material points.
        """
        def __init__(self, service, version, mode, path):
            self.create_material_point = self.__class__.create_material_point(service, version, mode, path + ["create_material_point"])
            self.delete_all_material_points = self.__class__.delete_all_material_points(service, version, mode, path + ["delete_all_material_points"])
            self.delete_material_point = self.__class__.delete_material_point(service, version, mode, path + ["delete_material_point"])
            self.list_material_points = self.__class__.list_material_points(service, version, mode, path + ["list_material_points"])
            super().__init__(service, version, mode, path)
        class create_material_point(TUIMethod):
            """
            Add a material point.
            """
        class delete_all_material_points(TUIMethod):
            """
            Delete all material points.
            """
        class delete_material_point(TUIMethod):
            """
            Delete a material point.
            """
        class list_material_points(TUIMethod):
            """
            List material points.
            """

    class mesh(TUIMenu):
        """
        Enter the grid menu.
        """
        def __init__(self, service, version, mode, path):
            self.auto_mesh_controls = self.__class__.auto_mesh_controls(service, version, mode, path + ["auto_mesh_controls"])
            self.cartesian = self.__class__.cartesian(service, version, mode, path + ["cartesian"])
            self.cavity = self.__class__.cavity(service, version, mode, path + ["cavity"])
            self.cell_zone_conditions = self.__class__.cell_zone_conditions(service, version, mode, path + ["cell_zone_conditions"])
            self.domains = self.__class__.domains(service, version, mode, path + ["domains"])
            self.hexcore = self.__class__.hexcore(service, version, mode, path + ["hexcore"])
            self.manage = self.__class__.manage(service, version, mode, path + ["manage"])
            self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
            self.non_conformals = self.__class__.non_conformals(service, version, mode, path + ["non_conformals"])
            self.poly = self.__class__.poly(service, version, mode, path + ["poly"])
            self.poly_hexcore = self.__class__.poly_hexcore(service, version, mode, path + ["poly_hexcore"])
            self.prism = self.__class__.prism(service, version, mode, path + ["prism"])
            self.pyramid = self.__class__.pyramid(service, version, mode, path + ["pyramid"])
            self.rapid_octree = self.__class__.rapid_octree(service, version, mode, path + ["rapid_octree"])
            self.scoped_prisms = self.__class__.scoped_prisms(service, version, mode, path + ["scoped_prisms"])
            self.scoped_thin_volume = self.__class__.scoped_thin_volume(service, version, mode, path + ["scoped_thin_volume"])
            self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
            self.tet = self.__class__.tet(service, version, mode, path + ["tet"])
            self.thin_volume_mesh = self.__class__.thin_volume_mesh(service, version, mode, path + ["thin_volume_mesh"])
            self.activate_lean_datastructures = self.__class__.activate_lean_datastructures(service, version, mode, path + ["activate_lean_datastructures"])
            self.auto_mesh = self.__class__.auto_mesh(service, version, mode, path + ["auto_mesh"])
            self.auto_mesh_multiple_objects = self.__class__.auto_mesh_multiple_objects(service, version, mode, path + ["auto_mesh_multiple_objects"])
            self.auto_prefix_cell_zones = self.__class__.auto_prefix_cell_zones(service, version, mode, path + ["auto_prefix_cell_zones"])
            self.check_mesh = self.__class__.check_mesh(service, version, mode, path + ["check_mesh"])
            self.check_quality = self.__class__.check_quality(service, version, mode, path + ["check_quality"])
            self.check_quality_level = self.__class__.check_quality_level(service, version, mode, path + ["check_quality_level"])
            self.clear_mesh = self.__class__.clear_mesh(service, version, mode, path + ["clear_mesh"])
            self.clear_undo_stack = self.__class__.clear_undo_stack(service, version, mode, path + ["clear_undo_stack"])
            self.create_frustrum = self.__class__.create_frustrum(service, version, mode, path + ["create_frustrum"])
            self.create_heat_exchanger = self.__class__.create_heat_exchanger(service, version, mode, path + ["create_heat_exchanger"])
            self.deactivate_lean_datastructures = self.__class__.deactivate_lean_datastructures(service, version, mode, path + ["deactivate_lean_datastructures"])
            self.laplace_smooth_nodes = self.__class__.laplace_smooth_nodes(service, version, mode, path + ["laplace_smooth_nodes"])
            self.list_mesh_parameter = self.__class__.list_mesh_parameter(service, version, mode, path + ["list_mesh_parameter"])
            self.prepare_for_solve = self.__class__.prepare_for_solve(service, version, mode, path + ["prepare_for_solve"])
            self.prime_meshing = self.__class__.prime_meshing(service, version, mode, path + ["prime_meshing"])
            self.repair_face_handedness = self.__class__.repair_face_handedness(service, version, mode, path + ["repair_face_handedness"])
            self.reset_mesh = self.__class__.reset_mesh(service, version, mode, path + ["reset_mesh"])
            self.reset_mesh_parameter = self.__class__.reset_mesh_parameter(service, version, mode, path + ["reset_mesh_parameter"])
            self.selective_mesh_check = self.__class__.selective_mesh_check(service, version, mode, path + ["selective_mesh_check"])
            self.zone_names_clean_up = self.__class__.zone_names_clean_up(service, version, mode, path + ["zone_names_clean_up"])
            super().__init__(service, version, mode, path)
        class activate_lean_datastructures(TUIMethod):
            """
            Activates Lean data structures to reduce memory.
            """
        class auto_mesh(TUIMethod):
            """
            Automatically executes initialization and refinement of mesh.
            """
        class auto_mesh_multiple_objects(TUIMethod):
            """
            Automatically executes initialization and refinement of mesh for multiple objects.
            """
        class auto_prefix_cell_zones(TUIMethod):
            """
            Prefix cell zones with user defined name.
            """
        class check_mesh(TUIMethod):
            """
            Check mesh for topological errors.
            """
        class check_quality(TUIMethod):
            """
            Check mesh quality.
            """
        class check_quality_level(TUIMethod):
            """
            Check mesh quality level.
            """
        class clear_mesh(TUIMethod):
            """
            Clear internal mesh, leaving boundary faces.
            """
        class clear_undo_stack(TUIMethod):
            """
            Clears undo stack.
            """
        class create_frustrum(TUIMethod):
            """
            Create a cylindrical hex mesh.
            """
        class create_heat_exchanger(TUIMethod):
            """
            Create heat exchanger zones using four points and 3 intervals.
            """
        class deactivate_lean_datastructures(TUIMethod):
            """
            Deactivates Lean data structures.
            """
        class laplace_smooth_nodes(TUIMethod):
            """
            Laplace smooth nodes.
            """
        class list_mesh_parameter(TUIMethod):
            """
            Show all mesh parameters.
            """
        class prepare_for_solve(TUIMethod):
            """
            Performs the following cleanup operations.
            - Delete dead zones.
            - Delete geom and wrap objects.
            - Delete all edge zones.
            - Delete unused faces.
            - Delete unused nodes.
            .
            """
        class prime_meshing(TUIMethod):
            """
            Enable Prime Meshing.
            """
        class repair_face_handedness(TUIMethod):
            """
            Reverse face node orientation.
            """
        class reset_mesh(TUIMethod):
            """
            Clear entire mesh.
            """
        class reset_mesh_parameter(TUIMethod):
            """
            Reset all parameters to their default values.
            """
        class selective_mesh_check(TUIMethod):
            """
            Selective mesh check.
            """
        class zone_names_clean_up(TUIMethod):
            """
            Cleanup face and cell zone names.
            """

        class auto_mesh_controls(TUIMenu):
            """
            Automesh controls.
            """
            def __init__(self, service, version, mode, path):
                self.backup_object = self.__class__.backup_object(service, version, mode, path + ["backup_object"])
                super().__init__(service, version, mode, path)
            class backup_object(TUIMethod):
                """
                Option to create a back up for object.
                """

        class cartesian(TUIMenu):
            """
            Enter Cartesian mesh menu.
            """
            def __init__(self, service, version, mode, path):
                self.mesh = self.__class__.mesh(service, version, mode, path + ["mesh"])
                super().__init__(service, version, mode, path)
            class mesh(TUIMethod):
                """
                Generate Cartesian mesh.
                """

        class cavity(TUIMenu):
            """
            Enter cavity menu.
            """
            def __init__(self, service, version, mode, path):
                self.add_zones = self.__class__.add_zones(service, version, mode, path + ["add_zones"])
                self.create_hexcore_cavity_by_region = self.__class__.create_hexcore_cavity_by_region(service, version, mode, path + ["create_hexcore_cavity_by_region"])
                self.create_hexcore_cavity_by_scale = self.__class__.create_hexcore_cavity_by_scale(service, version, mode, path + ["create_hexcore_cavity_by_scale"])
                self.merge_cavity = self.__class__.merge_cavity(service, version, mode, path + ["merge_cavity"])
                self.region = self.__class__.region(service, version, mode, path + ["region"])
                self.remesh_hexcore_cavity = self.__class__.remesh_hexcore_cavity(service, version, mode, path + ["remesh_hexcore_cavity"])
                self.remove_zones = self.__class__.remove_zones(service, version, mode, path + ["remove_zones"])
                self.replace_zones = self.__class__.replace_zones(service, version, mode, path + ["replace_zones"])
                super().__init__(service, version, mode, path)
            class add_zones(TUIMethod):
                """
                Create a cavity for remeshing.
                """
            class create_hexcore_cavity_by_region(TUIMethod):
                """
                Create a cavity in hexcore mesh for remeshing.
                """
            class create_hexcore_cavity_by_scale(TUIMethod):
                """
                Create a cavity in hexcore mesh for remeshing by scale.
                """
            class merge_cavity(TUIMethod):
                """
                Merge a cavity domain with a domain.
                """
            class region(TUIMethod):
                """
                Create a cavity for remeshing.
                """
            class remesh_hexcore_cavity(TUIMethod):
                """
                Remesh a cavity in hexcore mesh.
                """
            class remove_zones(TUIMethod):
                """
                Create a cavity for remeshing.
                """
            class replace_zones(TUIMethod):
                """
                Create a cavity for remeshing.
                """

        class cell_zone_conditions(TUIMenu):
            """
            Enter manage cell zone conditions menu.
            """
            def __init__(self, service, version, mode, path):
                self.clear = self.__class__.clear(service, version, mode, path + ["clear"])
                self.clear_all = self.__class__.clear_all(service, version, mode, path + ["clear_all"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                super().__init__(service, version, mode, path)
            class clear(TUIMethod):
                """
                Clear cell zone conditions.
                """
            class clear_all(TUIMethod):
                """
                Clear all cell zone conditions.
                """
            class copy(TUIMethod):
                """
                Copy cell zone conditions.
                """

        class domains(TUIMenu):
            """
            Enter domains menu.
            """
            def __init__(self, service, version, mode, path):
                self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.create_by_cell_zone = self.__class__.create_by_cell_zone(service, version, mode, path + ["create_by_cell_zone"])
                self.create_by_point = self.__class__.create_by_point(service, version, mode, path + ["create_by_point"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                self.print = self.__class__.print(service, version, mode, path + ["print"])
                super().__init__(service, version, mode, path)
            class activate(TUIMethod):
                """
                Activate the domain for subsequent meshing operations.
                .
                """
            class create(TUIMethod):
                """
                Create a new domain by specifying the boundary face zones.
                .
                """
            class create_by_cell_zone(TUIMethod):
                """
                Create new domain using cell zones.
                .
                """
            class create_by_point(TUIMethod):
                """
                Create new domain using material point.
                .
                """
            class delete(TUIMethod):
                """
                Delete the specified domain.
                .
                """
            class draw(TUIMethod):
                """
                Draw the boundary face zones of the domain.
                .
                """
            class print(TUIMethod):
                """
                Print domain content.
                .
                """

        class hexcore(TUIMenu):
            """
            Enter the hexcore menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.merge_tets_to_pyramids = self.__class__.merge_tets_to_pyramids(service, version, mode, path + ["merge_tets_to_pyramids"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create hexcore mesh from boundary zone list.
                """
            class merge_tets_to_pyramids(TUIMethod):
                """
                Merge tets into pyramids.
                """

            class controls(TUIMenu):
                """
                Enter hexcore controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.outer_domain_params = self.__class__.outer_domain_params(service, version, mode, path + ["outer_domain_params"])
                    self.avoid_1_by_8_cell_jump_in_hexcore = self.__class__.avoid_1_by_8_cell_jump_in_hexcore(service, version, mode, path + ["avoid_1_by_8_cell_jump_in_hexcore"])
                    self.buffer_layers = self.__class__.buffer_layers(service, version, mode, path + ["buffer_layers"])
                    self.compute_max_cell_length = self.__class__.compute_max_cell_length(service, version, mode, path + ["compute_max_cell_length"])
                    self.define_hexcore_extents = self.__class__.define_hexcore_extents(service, version, mode, path + ["define_hexcore_extents"])
                    self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                    self.island_thresholds = self.__class__.island_thresholds(service, version, mode, path + ["island_thresholds"])
                    self.keep_hex_tet_separate = self.__class__.keep_hex_tet_separate(service, version, mode, path + ["keep_hex_tet_separate"])
                    self.maximum_cell_length = self.__class__.maximum_cell_length(service, version, mode, path + ["maximum_cell_length"])
                    self.maximum_initial_cells = self.__class__.maximum_initial_cells(service, version, mode, path + ["maximum_initial_cells"])
                    self.maximum_subdivisions = self.__class__.maximum_subdivisions(service, version, mode, path + ["maximum_subdivisions"])
                    self.merge_tets_to_pyramids = self.__class__.merge_tets_to_pyramids(service, version, mode, path + ["merge_tets_to_pyramids"])
                    self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                    self.octree_hexcore = self.__class__.octree_hexcore(service, version, mode, path + ["octree_hexcore"])
                    self.only_hexcore = self.__class__.only_hexcore(service, version, mode, path + ["only_hexcore"])
                    self.peel_layers = self.__class__.peel_layers(service, version, mode, path + ["peel_layers"])
                    self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                    self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                    self.skip_tet_refinement = self.__class__.skip_tet_refinement(service, version, mode, path + ["skip_tet_refinement"])
                    self.smooth_interface = self.__class__.smooth_interface(service, version, mode, path + ["smooth_interface"])
                    self.smooth_iterations = self.__class__.smooth_iterations(service, version, mode, path + ["smooth_iterations"])
                    self.smooth_relaxation = self.__class__.smooth_relaxation(service, version, mode, path + ["smooth_relaxation"])
                    super().__init__(service, version, mode, path)
                class avoid_1_by_8_cell_jump_in_hexcore(TUIMethod):
                    """
                    Avoid-1:8-cell-jump-in-hexcore.
                    """
                class buffer_layers(TUIMethod):
                    """
                    Number of addition cells to mark for subdivision.
                    """
                class compute_max_cell_length(TUIMethod):
                    """
                    Compute maximum cell length.
                    """
                class define_hexcore_extents(TUIMethod):
                    """
                    Enables sspecificaton of hexcore outer domain parameters.
                    """
                class delete_dead_zones(TUIMethod):
                    """
                    Delete dead zones after hexcore creation.
                    """
                class island_thresholds(TUIMethod):
                    """
                    Maximum number of cells and volume fraction in islands, deleted while separating the cells by region.
                    """
                class keep_hex_tet_separate(TUIMethod):
                    """
                    Separate Hex and Tet cells.
                    """
                class maximum_cell_length(TUIMethod):
                    """
                    Maximum cell length.
                    """
                class maximum_initial_cells(TUIMethod):
                    """
                    Maximum number of initial Cartesian cells.
                    """
                class maximum_subdivisions(TUIMethod):
                    """
                    Maximum number of subdivision sweeps.
                    """
                class merge_tets_to_pyramids(TUIMethod):
                    """
                    Merge tets into pyramids.
                    """
                class non_fluid_type(TUIMethod):
                    """
                    Set non fluid type for cell zones.
                    """
                class octree_hexcore(TUIMethod):
                    """
                    Create hexcore using size-function driven octree.
                    """
                class only_hexcore(TUIMethod):
                    """
                    Create hexcore and activate tet domain.
                    """
                class peel_layers(TUIMethod):
                    """
                    Number of hexcore cells to peel back from boundary.
                    """
                class print_region_based_sizing(TUIMethod):
                    """
                    Print region based sizings.
                    """
                class set_region_based_sizing(TUIMethod):
                    """
                    Set region based sizings.
                    """
                class skip_tet_refinement(TUIMethod):
                    """
                    Skip tethedral refinement in transition cell generation.
                    """
                class smooth_interface(TUIMethod):
                    """
                    Enable smoothing of hexcore interface.
                    """
                class smooth_iterations(TUIMethod):
                    """
                    Number of smoothing iterations on hexcore interface.
                    """
                class smooth_relaxation(TUIMethod):
                    """
                    Smoothing under relaxation on hexcore interface.
                    """

                class outer_domain_params(TUIMenu):
                    """
                    Define outer domain parameters.
                    """
                    def __init__(self, service, version, mode, path):
                        self.auto_align = self.__class__.auto_align(service, version, mode, path + ["auto_align"])
                        self.auto_align_boundaries = self.__class__.auto_align_boundaries(service, version, mode, path + ["auto_align_boundaries"])
                        self.auto_align_tolerance = self.__class__.auto_align_tolerance(service, version, mode, path + ["auto_align_tolerance"])
                        self.boundaries = self.__class__.boundaries(service, version, mode, path + ["boundaries"])
                        self.coordinates = self.__class__.coordinates(service, version, mode, path + ["coordinates"])
                        self.delete_old_face_zones = self.__class__.delete_old_face_zones(service, version, mode, path + ["delete_old_face_zones"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.specify_boundaries = self.__class__.specify_boundaries(service, version, mode, path + ["specify_boundaries"])
                        self.specify_coordinates = self.__class__.specify_coordinates(service, version, mode, path + ["specify_coordinates"])
                        super().__init__(service, version, mode, path)
                    class auto_align(TUIMethod):
                        """
                        Enable auto-align?.
                        """
                    class auto_align_boundaries(TUIMethod):
                        """
                        Auto-align selected boundaries.
                        """
                    class auto_align_tolerance(TUIMethod):
                        """
                        Set auto-align-tolerance.
                        """
                    class boundaries(TUIMethod):
                        """
                        Set box-aligned zones which  have to be removed from hexcore meshing.
                        """
                    class coordinates(TUIMethod):
                        """
                        Secifiy coordinates of outer box.
                        """
                    class delete_old_face_zones(TUIMethod):
                        """
                        Delete replaced old tri face zones.
                        """
                    class list(TUIMethod):
                        """
                        List the face zones selected for hexcore up to boundaries.
                        """
                    class specify_boundaries(TUIMethod):
                        """
                        Set parameters to get hex mesh to boundary(s).
                        """
                    class specify_coordinates(TUIMethod):
                        """
                        Enables specification of coordinates of hexcore outer box.
                        """

            class local_regions(TUIMenu):
                """
                Enter the hexcore refine-local menu.
                """
                def __init__(self, service, version, mode, path):
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.deactivate = self.__class__.deactivate(service, version, mode, path + ["deactivate"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.ideal_hex_vol = self.__class__.ideal_hex_vol(service, version, mode, path + ["ideal_hex_vol"])
                    self.ideal_quad_area = self.__class__.ideal_quad_area(service, version, mode, path + ["ideal_quad_area"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class activate(TUIMethod):
                    """
                    Activate regions for hexcore refinement.
                    """
                class deactivate(TUIMethod):
                    """
                    Activate regions for hexcore refinement.
                    """
                class define(TUIMethod):
                    """
                    Define a refinement region's parameters.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region.
                    """
                class ideal_hex_vol(TUIMethod):
                    """
                    Ideal hex volume for given edge length.
                    """
                class ideal_quad_area(TUIMethod):
                    """
                    Ideal quad area for given edge length.
                    """
                class init(TUIMethod):
                    """
                    Delete all current regions and add the default refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    List all refinement regions.
                    """

        class manage(TUIMenu):
            """
            Enter cell zone menu.
            """
            def __init__(self, service, version, mode, path):
                self.active_list = self.__class__.active_list(service, version, mode, path + ["active_list"])
                self.adjacent_face_zones = self.__class__.adjacent_face_zones(service, version, mode, path + ["adjacent_face_zones"])
                self.auto_set_active = self.__class__.auto_set_active(service, version, mode, path + ["auto_set_active"])
                self.change_prefix = self.__class__.change_prefix(service, version, mode, path + ["change_prefix"])
                self.change_suffix = self.__class__.change_suffix(service, version, mode, path + ["change_suffix"])
                self.copy = self.__class__.copy(service, version, mode, path + ["copy"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.get_material_point = self.__class__.get_material_point(service, version, mode, path + ["get_material_point"])
                self.id = self.__class__.id(service, version, mode, path + ["id"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.merge_dead_zones = self.__class__.merge_dead_zones(service, version, mode, path + ["merge_dead_zones"])
                self.name = self.__class__.name(service, version, mode, path + ["name"])
                self.origin = self.__class__.origin(service, version, mode, path + ["origin"])
                self.revolve_face_zone = self.__class__.revolve_face_zone(service, version, mode, path + ["revolve_face_zone"])
                self.rotate = self.__class__.rotate(service, version, mode, path + ["rotate"])
                self.rotate_model = self.__class__.rotate_model(service, version, mode, path + ["rotate_model"])
                self.scale = self.__class__.scale(service, version, mode, path + ["scale"])
                self.scale_model = self.__class__.scale_model(service, version, mode, path + ["scale_model"])
                self.set_active = self.__class__.set_active(service, version, mode, path + ["set_active"])
                self.translate = self.__class__.translate(service, version, mode, path + ["translate"])
                self.translate_model = self.__class__.translate_model(service, version, mode, path + ["translate_model"])
                self.type = self.__class__.type(service, version, mode, path + ["type"])
                super().__init__(service, version, mode, path)
            class active_list(TUIMethod):
                """
                List active cell zones.
                """
            class adjacent_face_zones(TUIMethod):
                """
                List all face zones referring the specified cell zone.
                """
            class auto_set_active(TUIMethod):
                """
                Set active zones based on prescribed points.
                """
            class change_prefix(TUIMethod):
                """
                Change the prefix for specified face zones.
                """
            class change_suffix(TUIMethod):
                """
                Change the suffix for specified face zones.
                """
            class copy(TUIMethod):
                """
                Copy the zone.
                """
            class delete(TUIMethod):
                """
                Delete cell zone.
                """
            class get_material_point(TUIMethod):
                """
                Returns material point coordinates for all regions of a cell zone.
                """
            class id(TUIMethod):
                """
                Give zone a new id number.
                """
            class list(TUIMethod):
                """
                List all cell zones.
                """
            class merge(TUIMethod):
                """
                Merge two or more cell zones.
                """
            class merge_dead_zones(TUIMethod):
                """
                Merge dead zones.
                """
            class name(TUIMethod):
                """
                Give zone a new name.
                """
            class origin(TUIMethod):
                """
                Set the origin of the mesh coordinates.
                """
            class revolve_face_zone(TUIMethod):
                """
                Generate cells by revolving a face thread.
                """
            class rotate(TUIMethod):
                """
                Rotate all nodes of specified cell zones.
                """
            class rotate_model(TUIMethod):
                """
                Rotate all nodes.
                """
            class scale(TUIMethod):
                """
                Scale all nodes of specified cell zones.
                """
            class scale_model(TUIMethod):
                """
                Scale all nodes.
                """
            class set_active(TUIMethod):
                """
                Refine/swap/display only cells in these cell zones.
                """
            class translate(TUIMethod):
                """
                Translate all nodes of specified cell zones.
                """
            class translate_model(TUIMethod):
                """
                Translate all nodes.
                """
            class type(TUIMethod):
                """
                Change cell zone type.
                """

        class modify(TUIMenu):
            """
            Enter the mesh modify menu.
            """
            def __init__(self, service, version, mode, path):
                self.auto_improve_warp = self.__class__.auto_improve_warp(service, version, mode, path + ["auto_improve_warp"])
                self.auto_node_move = self.__class__.auto_node_move(service, version, mode, path + ["auto_node_move"])
                self.clear_selections = self.__class__.clear_selections(service, version, mode, path + ["clear_selections"])
                self.delete_isolated_cells = self.__class__.delete_isolated_cells(service, version, mode, path + ["delete_isolated_cells"])
                self.deselect_last = self.__class__.deselect_last(service, version, mode, path + ["deselect_last"])
                self.extract_unused_nodes = self.__class__.extract_unused_nodes(service, version, mode, path + ["extract_unused_nodes"])
                self.list_selections = self.__class__.list_selections(service, version, mode, path + ["list_selections"])
                self.list_skewed_cells = self.__class__.list_skewed_cells(service, version, mode, path + ["list_skewed_cells"])
                self.mesh_node = self.__class__.mesh_node(service, version, mode, path + ["mesh_node"])
                self.mesh_nodes_on_zone = self.__class__.mesh_nodes_on_zone(service, version, mode, path + ["mesh_nodes_on_zone"])
                self.neighborhood_skew = self.__class__.neighborhood_skew(service, version, mode, path + ["neighborhood_skew"])
                self.refine_cell = self.__class__.refine_cell(service, version, mode, path + ["refine_cell"])
                self.repair_negative_volume_cells = self.__class__.repair_negative_volume_cells(service, version, mode, path + ["repair_negative_volume_cells"])
                self.select_entity = self.__class__.select_entity(service, version, mode, path + ["select_entity"])
                self.smooth_node = self.__class__.smooth_node(service, version, mode, path + ["smooth_node"])
                super().__init__(service, version, mode, path)
            class auto_improve_warp(TUIMethod):
                """
                Improve the warp of the faces by node movement.
                """
            class auto_node_move(TUIMethod):
                """
                Improve the quality of the mesh by node movement.
                """
            class clear_selections(TUIMethod):
                """
                Clear all selections.
                """
            class delete_isolated_cells(TUIMethod):
                """
                Delete isolated cells.
                """
            class deselect_last(TUIMethod):
                """
                Deselect last selection.
                """
            class extract_unused_nodes(TUIMethod):
                """
                Extract all unused nodes into a separate interior node zone.
                """
            class list_selections(TUIMethod):
                """
                List selections.
                """
            class list_skewed_cells(TUIMethod):
                """
                List cells between skewness limits.
                """
            class mesh_node(TUIMethod):
                """
                Introduce new node into existing mesh.
                """
            class mesh_nodes_on_zone(TUIMethod):
                """
                Insert nodes associated with node or face thread into volume mesh.  If a face thread is specified, the faces are deleted before the nodes are introduced into the mesh.
                """
            class neighborhood_skew(TUIMethod):
                """
                Report max skew of all cells using node.
                """
            class refine_cell(TUIMethod):
                """
                Refine cells in probe list with node near centroid.
                """
            class repair_negative_volume_cells(TUIMethod):
                """
                Improves negative volume cells by node movement.
                """
            class select_entity(TUIMethod):
                """
                Select a entity.
                """
            class smooth_node(TUIMethod):
                """
                Laplace smooth nodes in probe list.
                """

        class non_conformals(TUIMenu):
            """
            Enter the non conformals controls menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.separate = self.__class__.separate(service, version, mode, path + ["separate"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create layer of non conformals on one or more face zones.
                """
            class separate(TUIMethod):
                """
                Separate non-conformal interfaces between cell zones.
                """

            class controls(TUIMenu):
                """
                Enter the non conformals controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.enable = self.__class__.enable(service, version, mode, path + ["enable"])
                    self.retri_method = self.__class__.retri_method(service, version, mode, path + ["retri_method"])
                    super().__init__(service, version, mode, path)
                class enable(TUIMethod):
                    """
                    Enable creation of non conformal interface. The quads will be split into tris.
                    """
                class retri_method(TUIMethod):
                    """
                    Enable triangulation of non-conformal interfaces instead of quad splitting.
                    """

        class poly(TUIMenu):
            """
            Enter the poly menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.collapse = self.__class__.collapse(service, version, mode, path + ["collapse"])
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.quality_method = self.__class__.quality_method(service, version, mode, path + ["quality_method"])
                self.remesh = self.__class__.remesh(service, version, mode, path + ["remesh"])
                super().__init__(service, version, mode, path)
            class collapse(TUIMethod):
                """
                Collapse short edges and small faces.
                """
            class improve(TUIMethod):
                """
                Smooth poly mesh.
                """
            class quality_method(TUIMethod):
                """
                Set poly quality method.
                """
            class remesh(TUIMethod):
                """
                Remesh local region.
                """

            class controls(TUIMenu):
                """
                Poly controls.
                """
                def __init__(self, service, version, mode, path):
                    self.prism = self.__class__.prism(service, version, mode, path + ["prism"])
                    self.smooth_controls = self.__class__.smooth_controls(service, version, mode, path + ["smooth_controls"])
                    self.cell_sizing = self.__class__.cell_sizing(service, version, mode, path + ["cell_sizing"])
                    self.edge_size_ratio = self.__class__.edge_size_ratio(service, version, mode, path + ["edge_size_ratio"])
                    self.face_size_ratio = self.__class__.face_size_ratio(service, version, mode, path + ["face_size_ratio"])
                    self.feature_angle = self.__class__.feature_angle(service, version, mode, path + ["feature_angle"])
                    self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                    self.merge_skew = self.__class__.merge_skew(service, version, mode, path + ["merge_skew"])
                    self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                    self.remesh_skew = self.__class__.remesh_skew(service, version, mode, path + ["remesh_skew"])
                    self.sliver_cell_area_fraction = self.__class__.sliver_cell_area_fraction(service, version, mode, path + ["sliver_cell_area_fraction"])
                    super().__init__(service, version, mode, path)
                class cell_sizing(TUIMethod):
                    """
                    Allow cell volume distribution to be determined based on boundary.
                    """
                class edge_size_ratio(TUIMethod):
                    """
                    Size ratio tolerance of two connected edges.
                    """
                class face_size_ratio(TUIMethod):
                    """
                    Size ratio tolerance of two faces in one cell.
                    """
                class feature_angle(TUIMethod):
                    """
                    Feature angle.
                    """
                class improve(TUIMethod):
                    """
                    Improve the poly mesh by smoothing?.
                    """
                class merge_skew(TUIMethod):
                    """
                    Merge minimum skewness.
                    """
                class non_fluid_type(TUIMethod):
                    """
                    Select the default non-fluid cell zone type.
                    """
                class remesh_skew(TUIMethod):
                    """
                    Remesh target skewness.
                    """
                class sliver_cell_area_fraction(TUIMethod):
                    """
                    Fraction tolerance between face area and cell surface area.
                    """

                class prism(TUIMenu):
                    """
                    Poly prism transition controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.apply_growth = self.__class__.apply_growth(service, version, mode, path + ["apply_growth"])
                        self.clear_growth = self.__class__.clear_growth(service, version, mode, path + ["clear_growth"])
                        self.list_growth = self.__class__.list_growth(service, version, mode, path + ["list_growth"])
                        super().__init__(service, version, mode, path)
                    class apply_growth(TUIMethod):
                        """
                        Apply growth settings.
                        """
                    class clear_growth(TUIMethod):
                        """
                        Clear growth settings.
                        """
                    class list_growth(TUIMethod):
                        """
                        List growth settings.
                        """

                class smooth_controls(TUIMenu):
                    """
                    Poly smooth controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.centroid_smooth_iterations = self.__class__.centroid_smooth_iterations(service, version, mode, path + ["centroid_smooth_iterations"])
                        self.edge_smooth_iterations = self.__class__.edge_smooth_iterations(service, version, mode, path + ["edge_smooth_iterations"])
                        self.laplace_smooth_iterations = self.__class__.laplace_smooth_iterations(service, version, mode, path + ["laplace_smooth_iterations"])
                        self.smooth_attempts = self.__class__.smooth_attempts(service, version, mode, path + ["smooth_attempts"])
                        self.smooth_boundary = self.__class__.smooth_boundary(service, version, mode, path + ["smooth_boundary"])
                        self.smooth_iterations = self.__class__.smooth_iterations(service, version, mode, path + ["smooth_iterations"])
                        self.smooth_on_layer = self.__class__.smooth_on_layer(service, version, mode, path + ["smooth_on_layer"])
                        self.smooth_skew = self.__class__.smooth_skew(service, version, mode, path + ["smooth_skew"])
                        super().__init__(service, version, mode, path)
                    class centroid_smooth_iterations(TUIMethod):
                        """
                        Centroid smoothing iterations.
                        """
                    class edge_smooth_iterations(TUIMethod):
                        """
                        Edge smoothing iterations.
                        """
                    class laplace_smooth_iterations(TUIMethod):
                        """
                        Laplace smoothing iterations.
                        """
                    class smooth_attempts(TUIMethod):
                        """
                        Smooth attempts.
                        """
                    class smooth_boundary(TUIMethod):
                        """
                        Smooth boundary as part of cell smoothing.
                        """
                    class smooth_iterations(TUIMethod):
                        """
                        Smooth iterations.
                        """
                    class smooth_on_layer(TUIMethod):
                        """
                        Smooth poly-prism nodes on layer.
                        """
                    class smooth_skew(TUIMethod):
                        """
                        Smooth minimum skewness.
                        """

            class local_regions(TUIMenu):
                """
                Enter the refine-local menu.
                """
                def __init__(self, service, version, mode, path):
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.deactivate = self.__class__.deactivate(service, version, mode, path + ["deactivate"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.ideal_area = self.__class__.ideal_area(service, version, mode, path + ["ideal_area"])
                    self.ideal_vol = self.__class__.ideal_vol(service, version, mode, path + ["ideal_vol"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                    super().__init__(service, version, mode, path)
                class activate(TUIMethod):
                    """
                    Activate regions for tet refinement.
                    """
                class deactivate(TUIMethod):
                    """
                    Activate regions for tet refinement.
                    """
                class define(TUIMethod):
                    """
                    Define a refinement region's parameters.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region.
                    """
                class ideal_area(TUIMethod):
                    """
                    Ideal triangle area for given edge length.
                    """
                class ideal_vol(TUIMethod):
                    """
                    Ideal tet volume for given edge length.
                    """
                class init(TUIMethod):
                    """
                    Delete all current regions and add the default refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    List all refinement regions.
                    """
                class refine(TUIMethod):
                    """
                    Refine live cells inside region based on refinement parameters.
                    """

        class poly_hexcore(TUIMenu):
            """
            Enter the poly-hexcore menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                super().__init__(service, version, mode, path)

            class controls(TUIMenu):
                """
                Enter poly-hexcore controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.avoid_1_by_8_cell_jump_in_hexcore = self.__class__.avoid_1_by_8_cell_jump_in_hexcore(service, version, mode, path + ["avoid_1_by_8_cell_jump_in_hexcore"])
                    self.mark_core_region_cell_type_as_hex = self.__class__.mark_core_region_cell_type_as_hex(service, version, mode, path + ["mark_core_region_cell_type_as_hex"])
                    self.only_polyhedra_for_selected_regions = self.__class__.only_polyhedra_for_selected_regions(service, version, mode, path + ["only_polyhedra_for_selected_regions"])
                    self.poly_cell_sizing_method = self.__class__.poly_cell_sizing_method(service, version, mode, path + ["poly_cell_sizing_method"])
                    super().__init__(service, version, mode, path)
                class avoid_1_by_8_cell_jump_in_hexcore(TUIMethod):
                    """
                    Avoid-1:8-cell-jump-in-hexcore.
                    """
                class mark_core_region_cell_type_as_hex(TUIMethod):
                    """
                    Mark-core-region-cell-type-as-hex?.
                    """
                class only_polyhedra_for_selected_regions(TUIMethod):
                    """
                    Only-polyhedra-for-selected-regions.
                    """
                class poly_cell_sizing_method(TUIMethod):
                    """
                    Poly-cell-sizing.
                    """

        class prism(TUIMenu):
            """
            Enter the scoped prisms menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.post_ignore = self.__class__.post_ignore(service, version, mode, path + ["post_ignore"])
                self.split = self.__class__.split(service, version, mode, path + ["split"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.list_parameters = self.__class__.list_parameters(service, version, mode, path + ["list_parameters"])
                self.mark_ignore_faces = self.__class__.mark_ignore_faces(service, version, mode, path + ["mark_ignore_faces"])
                self.mark_nonmanifold_nodes = self.__class__.mark_nonmanifold_nodes(service, version, mode, path + ["mark_nonmanifold_nodes"])
                self.mark_proximity_faces = self.__class__.mark_proximity_faces(service, version, mode, path + ["mark_proximity_faces"])
                self.quality_method = self.__class__.quality_method(service, version, mode, path + ["quality_method"])
                self.reset_parameters = self.__class__.reset_parameters(service, version, mode, path + ["reset_parameters"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create prism layers on one or more face zones.
                """
            class list_parameters(TUIMethod):
                """
                Show all prism mesh parameters.
                """
            class mark_ignore_faces(TUIMethod):
                """
                Mark prism base faces which will be ignored.
                """
            class mark_nonmanifold_nodes(TUIMethod):
                """
                Mark prism base nodes which have invalid manifold around them.
                """
            class mark_proximity_faces(TUIMethod):
                """
                Mark prism base faces with certain gap.
                """
            class quality_method(TUIMethod):
                """
                Set prism quality method.
                """
            class reset_parameters(TUIMethod):
                """
                Reset Prism Parameters.
                """

            class controls(TUIMenu):
                """
                Prism Controls.
                """
                def __init__(self, service, version, mode, path):
                    self.adjacent_zone = self.__class__.adjacent_zone(service, version, mode, path + ["adjacent_zone"])
                    self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                    self.morph = self.__class__.morph(service, version, mode, path + ["morph"])
                    self.normal = self.__class__.normal(service, version, mode, path + ["normal"])
                    self.offset = self.__class__.offset(service, version, mode, path + ["offset"])
                    self.post_ignore = self.__class__.post_ignore(service, version, mode, path + ["post_ignore"])
                    self.proximity = self.__class__.proximity(service, version, mode, path + ["proximity"])
                    self.zone_specific_growth = self.__class__.zone_specific_growth(service, version, mode, path + ["zone_specific_growth"])
                    self.auto_separate_cells = self.__class__.auto_separate_cells(service, version, mode, path + ["auto_separate_cells"])
                    self.check_quality = self.__class__.check_quality(service, version, mode, path + ["check_quality"])
                    self.grow_individually = self.__class__.grow_individually(service, version, mode, path + ["grow_individually"])
                    self.merge_ignored_threads = self.__class__.merge_ignored_threads(service, version, mode, path + ["merge_ignored_threads"])
                    self.remove_invalid_layer = self.__class__.remove_invalid_layer(service, version, mode, path + ["remove_invalid_layer"])
                    self.set_overset_prism_controls = self.__class__.set_overset_prism_controls(service, version, mode, path + ["set_overset_prism_controls"])
                    self.set_post_mesh_controls = self.__class__.set_post_mesh_controls(service, version, mode, path + ["set_post_mesh_controls"])
                    self.split = self.__class__.split(service, version, mode, path + ["split"])
                    super().__init__(service, version, mode, path)
                class auto_separate_cells(TUIMethod):
                    """
                    Automatically separate prism cells extruded from multiple face threads?.
                    """
                class check_quality(TUIMethod):
                    """
                    Check the volume, skewness, and handedness
                    of each new cell and face?.
                    """
                class grow_individually(TUIMethod):
                    """
                    Grow from multiple zones one-at-a-time?.
                    """
                class merge_ignored_threads(TUIMethod):
                    """
                    Automatically merge all ignored zones related to a base thread into one thread?.
                    """
                class remove_invalid_layer(TUIMethod):
                    """
                    Remove the last layer if it fails in the quality check.
                    """
                class set_overset_prism_controls(TUIMethod):
                    """
                    Set boundary layer controls for overset mesh generation.
                    """
                class set_post_mesh_controls(TUIMethod):
                    """
                    Set controls specific to growing prisms post volume mesh.
                    """
                class split(TUIMethod):
                    """
                    Split prism cells after prism mesh is done.
                    """

                class adjacent_zone(TUIMenu):
                    """
                    Prism Adjacent Zone Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.project = self.__class__.project(service, version, mode, path + ["project"])
                        self.project_adjacent_angle = self.__class__.project_adjacent_angle(service, version, mode, path + ["project_adjacent_angle"])
                        self.project_converged = self.__class__.project_converged(service, version, mode, path + ["project_converged"])
                        self.project_iter = self.__class__.project_iter(service, version, mode, path + ["project_iter"])
                        self.retri_feature_angle = self.__class__.retri_feature_angle(service, version, mode, path + ["retri_feature_angle"])
                        self.retriangulate_adjacent = self.__class__.retriangulate_adjacent(service, version, mode, path + ["retriangulate_adjacent"])
                        self.side_feature_align_angle = self.__class__.side_feature_align_angle(service, version, mode, path + ["side_feature_align_angle"])
                        self.side_feature_angle = self.__class__.side_feature_angle(service, version, mode, path + ["side_feature_angle"])
                        self.side_topology_align_angle = self.__class__.side_topology_align_angle(service, version, mode, path + ["side_topology_align_angle"])
                        super().__init__(service, version, mode, path)
                    class project(TUIMethod):
                        """
                        Project outer nodes to adjacent planar zones?.
                        """
                    class project_adjacent_angle(TUIMethod):
                        """
                        Outer edges of advancing layers are projected to
                        adjacent planar zones whose angles relative to the growth direction are
                        less than or equal to this angle.
                        """
                    class project_converged(TUIMethod):
                        """
                        Convergence criterion for projection to adjacent zones.
                        """
                    class project_iter(TUIMethod):
                        """
                        Maximum number of iterations for projection to adjacent zones.
                        """
                    class retri_feature_angle(TUIMethod):
                        """
                        This angle (degrees) is used for determining the feature edges on the face zones which are retirangulated.
                        """
                    class retriangulate_adjacent(TUIMethod):
                        """
                        Retriangulate planar zones along which prism layers are grown?.
                        """
                    class side_feature_align_angle(TUIMethod):
                        """
                        This angle (degrees) is used for aligning projected normals along a feature edge.
                        """
                    class side_feature_angle(TUIMethod):
                        """
                        This angle (degrees) is used for computing feature normals (more flexible than retriangulation-feature-angle).
                        """
                    class side_topology_align_angle(TUIMethod):
                        """
                        This angle (degrees) is used for aligning projected normals along one from many feature edges based on topology (if feature-align doesn't occur).
                        """

                class improve(TUIMenu):
                    """
                    Prism Smoothing Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.check_allowable_skew = self.__class__.check_allowable_skew(service, version, mode, path + ["check_allowable_skew"])
                        self.check_size = self.__class__.check_size(service, version, mode, path + ["check_size"])
                        self.corner_height_weight = self.__class__.corner_height_weight(service, version, mode, path + ["corner_height_weight"])
                        self.edge_smooth = self.__class__.edge_smooth(service, version, mode, path + ["edge_smooth"])
                        self.edge_smooth_angle = self.__class__.edge_smooth_angle(service, version, mode, path + ["edge_smooth_angle"])
                        self.edge_swap = self.__class__.edge_swap(service, version, mode, path + ["edge_swap"])
                        self.edge_swap_base_angle = self.__class__.edge_swap_base_angle(service, version, mode, path + ["edge_swap_base_angle"])
                        self.edge_swap_cap_angle = self.__class__.edge_swap_cap_angle(service, version, mode, path + ["edge_swap_cap_angle"])
                        self.face_smooth = self.__class__.face_smooth(service, version, mode, path + ["face_smooth"])
                        self.face_smooth_converged = self.__class__.face_smooth_converged(service, version, mode, path + ["face_smooth_converged"])
                        self.face_smooth_rings = self.__class__.face_smooth_rings(service, version, mode, path + ["face_smooth_rings"])
                        self.face_smooth_skew = self.__class__.face_smooth_skew(service, version, mode, path + ["face_smooth_skew"])
                        self.identify_feature_line = self.__class__.identify_feature_line(service, version, mode, path + ["identify_feature_line"])
                        self.improve_warp = self.__class__.improve_warp(service, version, mode, path + ["improve_warp"])
                        self.layer_by_layer_smoothing = self.__class__.layer_by_layer_smoothing(service, version, mode, path + ["layer_by_layer_smoothing"])
                        self.left_hand_check = self.__class__.left_hand_check(service, version, mode, path + ["left_hand_check"])
                        self.max_allowable_cap_skew = self.__class__.max_allowable_cap_skew(service, version, mode, path + ["max_allowable_cap_skew"])
                        self.max_allowable_cell_skew = self.__class__.max_allowable_cell_skew(service, version, mode, path + ["max_allowable_cell_skew"])
                        self.node_smooth = self.__class__.node_smooth(service, version, mode, path + ["node_smooth"])
                        self.node_smooth_angle = self.__class__.node_smooth_angle(service, version, mode, path + ["node_smooth_angle"])
                        self.node_smooth_converged = self.__class__.node_smooth_converged(service, version, mode, path + ["node_smooth_converged"])
                        self.node_smooth_iter = self.__class__.node_smooth_iter(service, version, mode, path + ["node_smooth_iter"])
                        self.node_smooth_local = self.__class__.node_smooth_local(service, version, mode, path + ["node_smooth_local"])
                        self.node_smooth_rings = self.__class__.node_smooth_rings(service, version, mode, path + ["node_smooth_rings"])
                        self.post_adjust_height = self.__class__.post_adjust_height(service, version, mode, path + ["post_adjust_height"])
                        self.shrink_left_handed_cap = self.__class__.shrink_left_handed_cap(service, version, mode, path + ["shrink_left_handed_cap"])
                        self.smooth_improve_prism_cells = self.__class__.smooth_improve_prism_cells(service, version, mode, path + ["smooth_improve_prism_cells"])
                        self.swap_smooth_skew = self.__class__.swap_smooth_skew(service, version, mode, path + ["swap_smooth_skew"])
                        super().__init__(service, version, mode, path)
                    class check_allowable_skew(TUIMethod):
                        """
                        Check skewness for cap every layer?.
                        """
                    class check_size(TUIMethod):
                        """
                        Check for negative cell volume?.
                        """
                    class corner_height_weight(TUIMethod):
                        """
                        Improve cell quality/shape by adjusting heights at large corners?.
                        """
                    class edge_smooth(TUIMethod):
                        """
                        Perform local smoothing of nodes on longest edges of skewed faces?.
                        """
                    class edge_smooth_angle(TUIMethod):
                        """
                        Skewness-driven edge smoothing is only allowed between cap faces whose normals
                        are within this angle.
                        """
                    class edge_swap(TUIMethod):
                        """
                        Perform edge swapping to improve skewness?.
                        """
                    class edge_swap_base_angle(TUIMethod):
                        """
                        Skewness-driven edge swapping is only allowed between base faces whose normals
                        are within this angle.
                        """
                    class edge_swap_cap_angle(TUIMethod):
                        """
                        Skewness-driven edge swapping is only allowed between cap faces whose normals
                        are within this angle.
                        """
                    class face_smooth(TUIMethod):
                        """
                        Perform face-driven smoothing to improve skewness?.
                        """
                    class face_smooth_converged(TUIMethod):
                        """
                        Convergence criteria for cap face smoothing.
                        """
                    class face_smooth_rings(TUIMethod):
                        """
                        No. of rings to propagate skewness during smoothing of cap faces.
                        """
                    class face_smooth_skew(TUIMethod):
                        """
                        Min. skewness to smooth cap faces.
                        """
                    class identify_feature_line(TUIMethod):
                        """
                        Perform normal smoothing on feature lines?.
                        """
                    class improve_warp(TUIMethod):
                        """
                        Perform node movement to improve warp of quad face?.
                        """
                    class layer_by_layer_smoothing(TUIMethod):
                        """
                        Perform normals and heights smoothing to improve cell quality/shape?.
                        """
                    class left_hand_check(TUIMethod):
                        """
                        Check for left handedness of faces
                        (0 - no check, 1 - only cap faces, 2 - faces of all cells in current layer).
                        """
                    class max_allowable_cap_skew(TUIMethod):
                        """
                        Layer growth is stopped if any cap face has
                        skewness > this value (after all smoothing).
                        """
                    class max_allowable_cell_skew(TUIMethod):
                        """
                        Cell quality criteria for smoothing and quality checking.
                        """
                    class node_smooth(TUIMethod):
                        """
                        Perform node-driven smoothing to improve skewness?.
                        """
                    class node_smooth_angle(TUIMethod):
                        """
                        Only manifolds having characteristic angles
                        within this many degrees of 180 will be smoothed.
                        """
                    class node_smooth_converged(TUIMethod):
                        """
                        Convergence criterion for node smoothing.
                        """
                    class node_smooth_iter(TUIMethod):
                        """
                        Maximum number of smoothing iterations for nodes on advancing layers.
                        """
                    class node_smooth_local(TUIMethod):
                        """
                        Allow node-smoothing to converge locally (for large geometries).
                        """
                    class node_smooth_rings(TUIMethod):
                        """
                        Controls locality of skewness-driven node smoothing.
                        If greater than zero, nodes surrounding a node to be smoothed are smoothed
                        first.  Nodes directly connected to the target node are in ring 1.  Nodes not
                        in ring 1 which are directly connected to nodes in ring 1 are in ring 2,
                        and so on.  This value determines how many surrounding rings to smooth.
                        """
                    class post_adjust_height(TUIMethod):
                        """
                        Perform prism height adjustment based on growth rate?.
                        """
                    class shrink_left_handed_cap(TUIMethod):
                        """
                        Shrink if required to get rid of left handed faces.
                        """
                    class smooth_improve_prism_cells(TUIMethod):
                        """
                        Smooth and improve prism cells.
                        """
                    class swap_smooth_skew(TUIMethod):
                        """
                        Only faces with skewness >= this value are swapped and/or smoothed.
                        """

                class morph(TUIMenu):
                    """
                    Morpher Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.improve_threshold = self.__class__.improve_threshold(service, version, mode, path + ["improve_threshold"])
                        self.morphing_convergence_limit = self.__class__.morphing_convergence_limit(service, version, mode, path + ["morphing_convergence_limit"])
                        self.morphing_frequency = self.__class__.morphing_frequency(service, version, mode, path + ["morphing_frequency"])
                        super().__init__(service, version, mode, path)
                    class improve_threshold(TUIMethod):
                        """
                        Quality threshold used during the morpher improve operation.
                        """
                    class morphing_convergence_limit(TUIMethod):
                        """
                        Relative convergence criterion of the iterative linear solver .
                        """
                    class morphing_frequency(TUIMethod):
                        """
                        Number of layers created between each morphing call.
                        """

                class normal(TUIMenu):
                    """
                    Prism Normal Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.bisect_angle = self.__class__.bisect_angle(service, version, mode, path + ["bisect_angle"])
                        self.compute_normal = self.__class__.compute_normal(service, version, mode, path + ["compute_normal"])
                        self.converge_locally = self.__class__.converge_locally(service, version, mode, path + ["converge_locally"])
                        self.direction_method = self.__class__.direction_method(service, version, mode, path + ["direction_method"])
                        self.direction_vector = self.__class__.direction_vector(service, version, mode, path + ["direction_vector"])
                        self.ignore_invalid_normals = self.__class__.ignore_invalid_normals(service, version, mode, path + ["ignore_invalid_normals"])
                        self.max_angle_change = self.__class__.max_angle_change(service, version, mode, path + ["max_angle_change"])
                        self.normal_method = self.__class__.normal_method(service, version, mode, path + ["normal_method"])
                        self.orient_mesh_object_face_normals = self.__class__.orient_mesh_object_face_normals(service, version, mode, path + ["orient_mesh_object_face_normals"])
                        self.orthogonal_layers = self.__class__.orthogonal_layers(service, version, mode, path + ["orthogonal_layers"])
                        self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                        self.smooth_converged = self.__class__.smooth_converged(service, version, mode, path + ["smooth_converged"])
                        self.smooth_iter = self.__class__.smooth_iter(service, version, mode, path + ["smooth_iter"])
                        self.smooth_relaxation_factor = self.__class__.smooth_relaxation_factor(service, version, mode, path + ["smooth_relaxation_factor"])
                        super().__init__(service, version, mode, path)
                    class bisect_angle(TUIMethod):
                        """
                        Advancement vectors are forced onto bisecting planes
                        in sharp corners with angles less than this.
                        """
                    class compute_normal(TUIMethod):
                        """
                        Compute normal for the given face zone.
                        """
                    class converge_locally(TUIMethod):
                        """
                        Converge normal smoothing locally by freezing each
                        individually once it has converged?.  Otherwise, all normals are continuously
                        smoothed until all have converged.
                        """
                    class direction_method(TUIMethod):
                        """
                        Grow layers normal to surfaces or along a specified direction vector?.
                        """
                    class direction_vector(TUIMethod):
                        """
                        Direction vector for prism extrusion.
                        """
                    class ignore_invalid_normals(TUIMethod):
                        """
                        Ignore nodes which have very poor normals.
                        """
                    class max_angle_change(TUIMethod):
                        """
                        Smoothing changes in advancement vectors are constrained by this angle.
                        """
                    class normal_method(TUIMethod):
                        """
                        Method in which normal marching direction vectors are determined.
                        """
                    class orient_mesh_object_face_normals(TUIMethod):
                        """
                        Orient Face Normals Of Mesh Object.
                        """
                    class orthogonal_layers(TUIMethod):
                        """
                        Number of layers to preserve orthogonality.
                        All smoothing is deferred until after these layers.
                        """
                    class smooth(TUIMethod):
                        """
                        Perform smoothing of normal advancement direction vectors?.
                        """
                    class smooth_converged(TUIMethod):
                        """
                        Convergence criterion (in DEGREES) for angle changes
                        during normal smoothing.
                        """
                    class smooth_iter(TUIMethod):
                        """
                        Maximum number of smoothing iterations for normal vectors.
                        """
                    class smooth_relaxation_factor(TUIMethod):
                        """
                        Normal Smooth Relaxation factor.
                        """

                class offset(TUIMenu):
                    """
                    Prism Offset Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.first_aspect_ratio_min = self.__class__.first_aspect_ratio_min(service, version, mode, path + ["first_aspect_ratio_min"])
                        self.min_aspect_ratio = self.__class__.min_aspect_ratio(service, version, mode, path + ["min_aspect_ratio"])
                        self.smooth = self.__class__.smooth(service, version, mode, path + ["smooth"])
                        self.smooth_converged = self.__class__.smooth_converged(service, version, mode, path + ["smooth_converged"])
                        self.smooth_iter = self.__class__.smooth_iter(service, version, mode, path + ["smooth_iter"])
                        super().__init__(service, version, mode, path)
                    class first_aspect_ratio_min(TUIMethod):
                        """
                        Minimum base-length-over-height for prism cells.
                        """
                    class min_aspect_ratio(TUIMethod):
                        """
                        Minimum base-length-over-height for prism cells.
                        """
                    class smooth(TUIMethod):
                        """
                        Perform smoothing of offset distances?.
                        """
                    class smooth_converged(TUIMethod):
                        """
                        Convergence criterion for offset smoothing.
                        """
                    class smooth_iter(TUIMethod):
                        """
                        Maximum number of smoothing iterations for offset distances.
                        """

                class post_ignore(TUIMenu):
                    """
                    Prism Post Ignore Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.post_remove_cells = self.__class__.post_remove_cells(service, version, mode, path + ["post_remove_cells"])
                        super().__init__(service, version, mode, path)
                    class post_remove_cells(TUIMethod):
                        """
                        Post remove bad prism cells.
                        """

                class proximity(TUIMenu):
                    """
                    Prism Proximity Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.allow_ignore = self.__class__.allow_ignore(service, version, mode, path + ["allow_ignore"])
                        self.allow_shrinkage = self.__class__.allow_shrinkage(service, version, mode, path + ["allow_shrinkage"])
                        self.gap_factor = self.__class__.gap_factor(service, version, mode, path + ["gap_factor"])
                        self.keep_first_layer_offsets = self.__class__.keep_first_layer_offsets(service, version, mode, path + ["keep_first_layer_offsets"])
                        self.max_aspect_ratio = self.__class__.max_aspect_ratio(service, version, mode, path + ["max_aspect_ratio"])
                        self.max_shrink_factor = self.__class__.max_shrink_factor(service, version, mode, path + ["max_shrink_factor"])
                        self.smoothing_rate = self.__class__.smoothing_rate(service, version, mode, path + ["smoothing_rate"])
                        super().__init__(service, version, mode, path)
                    class allow_ignore(TUIMethod):
                        """
                        Ignore nodes where shrink factor can't be maintained.
                        """
                    class allow_shrinkage(TUIMethod):
                        """
                        Allow shrinkage while growing each layer.
                        """
                    class gap_factor(TUIMethod):
                        """
                        Gap rate to determine the space in proximity region.
                        """
                    class keep_first_layer_offsets(TUIMethod):
                        """
                        Fix first layer offsets while performing proximity detection?.
                        """
                    class max_aspect_ratio(TUIMethod):
                        """
                        Minimum offset to fall back to avoid degenerate cells.
                        """
                    class max_shrink_factor(TUIMethod):
                        """
                        Shrink factor to determine the maximum shrinkage of prism layer.
                        """
                    class smoothing_rate(TUIMethod):
                        """
                        Rate at which shrinkage is propagated in lateral direction.
                        """

                class zone_specific_growth(TUIMenu):
                    """
                    Prism Growth Controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.apply_growth = self.__class__.apply_growth(service, version, mode, path + ["apply_growth"])
                        self.clear_growth = self.__class__.clear_growth(service, version, mode, path + ["clear_growth"])
                        self.list_growth = self.__class__.list_growth(service, version, mode, path + ["list_growth"])
                        super().__init__(service, version, mode, path)
                    class apply_growth(TUIMethod):
                        """
                        Apply prism growth on individual zones.
                        """
                    class clear_growth(TUIMethod):
                        """
                        Clear zone specific growth on individual zones.
                        """
                    class list_growth(TUIMethod):
                        """
                        List zone specific growth on applied zones.
                        """

            class improve(TUIMenu):
                """
                Prism Improve Menu.
                """
                def __init__(self, service, version, mode, path):
                    self.improve_prism_cells = self.__class__.improve_prism_cells(service, version, mode, path + ["improve_prism_cells"])
                    self.smooth_brute_force = self.__class__.smooth_brute_force(service, version, mode, path + ["smooth_brute_force"])
                    self.smooth_cell_rings = self.__class__.smooth_cell_rings(service, version, mode, path + ["smooth_cell_rings"])
                    self.smooth_improve_prism_cells = self.__class__.smooth_improve_prism_cells(service, version, mode, path + ["smooth_improve_prism_cells"])
                    self.smooth_prism_cells = self.__class__.smooth_prism_cells(service, version, mode, path + ["smooth_prism_cells"])
                    self.smooth_sliver_skew = self.__class__.smooth_sliver_skew(service, version, mode, path + ["smooth_sliver_skew"])
                    super().__init__(service, version, mode, path)
                class improve_prism_cells(TUIMethod):
                    """
                    Smoothing cells by collecting rings of cells around them.
                    """
                class smooth_brute_force(TUIMethod):
                    """
                    Brute Force smooth cell if cell skewness is still higher after regular smoothing.
                    """
                class smooth_cell_rings(TUIMethod):
                    """
                    No. of Cell rings around the skewed cell used by improve-prism-cells.
                    """
                class smooth_improve_prism_cells(TUIMethod):
                    """
                    Combination of smooth and improve prism cells.
                    """
                class smooth_prism_cells(TUIMethod):
                    """
                    Optimization based smoothing.
                    """
                class smooth_sliver_skew(TUIMethod):
                    """
                    Prism Cells above this skewness will be smoothed.
                    """

            class post_ignore(TUIMenu):
                """
                Prism Post-Ignore Menu.
                """
                def __init__(self, service, version, mode, path):
                    self.create_cavity = self.__class__.create_cavity(service, version, mode, path + ["create_cavity"])
                    self.mark_cavity_prism_cap = self.__class__.mark_cavity_prism_cap(service, version, mode, path + ["mark_cavity_prism_cap"])
                    self.mark_prism_cap = self.__class__.mark_prism_cap(service, version, mode, path + ["mark_prism_cap"])
                    self.post_remove_cells = self.__class__.post_remove_cells(service, version, mode, path + ["post_remove_cells"])
                    super().__init__(service, version, mode, path)
                class create_cavity(TUIMethod):
                    """
                    Post tet cell quality ignore.
                    """
                class mark_cavity_prism_cap(TUIMethod):
                    """
                    Mark post-ignore tet cell cavity prism cap faces.
                    """
                class mark_prism_cap(TUIMethod):
                    """
                    Post mark cell quality ignore cap.
                    """
                class post_remove_cells(TUIMethod):
                    """
                    Post cell quality ignore.
                    """

            class split(TUIMenu):
                """
                Prism Post-Split Menu.
                """
                def __init__(self, service, version, mode, path):
                    self.split = self.__class__.split(service, version, mode, path + ["split"])
                    super().__init__(service, version, mode, path)
                class split(TUIMethod):
                    """
                    Split prism layer cells.
                    """

        class pyramid(TUIMenu):
            """
            Enter the pyramid controls menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create layer of pyramids on quad face zone.
                """

            class controls(TUIMenu):
                """
                Enter the pyramid controls menu.
                """
                def __init__(self, service, version, mode, path):
                    self.neighbor_angle = self.__class__.neighbor_angle(service, version, mode, path + ["neighbor_angle"])
                    self.offset_factor = self.__class__.offset_factor(service, version, mode, path + ["offset_factor"])
                    self.offset_scaling = self.__class__.offset_scaling(service, version, mode, path + ["offset_scaling"])
                    self.vertex_method = self.__class__.vertex_method(service, version, mode, path + ["vertex_method"])
                    super().__init__(service, version, mode, path)
                class neighbor_angle(TUIMethod):
                    """
                    Dihedral angle threshold used to limit which neighboring faces are considered in the creation of pyramids.
                    """
                class offset_factor(TUIMethod):
                    """
                    Factor of pyramid height used to randomly adjust the height of the pyramids during pyramid creation. Default is 0.
                    """
                class offset_scaling(TUIMethod):
                    """
                    The node created to produce a pyramid from a face is positioned along a vector emanating from the face centroid in the direction of the face's normal.  This factor scales the distance along this vector, unity represents an equilateral pyramid.
                    """
                class vertex_method(TUIMethod):
                    """
                    Method by which offset distances are determined.
                    """

        class rapid_octree(TUIMenu):
            """
            Enter the octree menu.
            """
            def __init__(self, service, version, mode, path):
                self.advanced_meshing_options = self.__class__.advanced_meshing_options(service, version, mode, path + ["advanced_meshing_options"])
                self.boundary_layer_mesh_configuration = self.__class__.boundary_layer_mesh_configuration(service, version, mode, path + ["boundary_layer_mesh_configuration"])
                self.geometry = self.__class__.geometry(service, version, mode, path + ["geometry"])
                self.mesh_sizing = self.__class__.mesh_sizing(service, version, mode, path + ["mesh_sizing"])
                self.refinement_regions = self.__class__.refinement_regions(service, version, mode, path + ["refinement_regions"])
                self.boundary_mesh_optimization = self.__class__.boundary_mesh_optimization(service, version, mode, path + ["boundary_mesh_optimization"])
                self.boundary_treatment = self.__class__.boundary_treatment(service, version, mode, path + ["boundary_treatment"])
                self.bounding_box = self.__class__.bounding_box(service, version, mode, path + ["bounding_box"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.create_stair_step_mesh = self.__class__.create_stair_step_mesh(service, version, mode, path + ["create_stair_step_mesh"])
                self.delete_poor_quality_cells = self.__class__.delete_poor_quality_cells(service, version, mode, path + ["delete_poor_quality_cells"])
                self.distribute_geometry = self.__class__.distribute_geometry(service, version, mode, path + ["distribute_geometry"])
                self.dry_run = self.__class__.dry_run(service, version, mode, path + ["dry_run"])
                self.estimate_cell_count = self.__class__.estimate_cell_count(service, version, mode, path + ["estimate_cell_count"])
                self.extract_refinement_levels = self.__class__.extract_refinement_levels(service, version, mode, path + ["extract_refinement_levels"])
                self.flow_volume = self.__class__.flow_volume(service, version, mode, path + ["flow_volume"])
                self.improve_geometry_resolution = self.__class__.improve_geometry_resolution(service, version, mode, path + ["improve_geometry_resolution"])
                self.input_object = self.__class__.input_object(service, version, mode, path + ["input_object"])
                self.is_manifold_geo = self.__class__.is_manifold_geo(service, version, mode, path + ["is_manifold_geo"])
                self.reset_bounding_box = self.__class__.reset_bounding_box(service, version, mode, path + ["reset_bounding_box"])
                self.resolve_geometry = self.__class__.resolve_geometry(service, version, mode, path + ["resolve_geometry"])
                self.undo_last_meshing_operation = self.__class__.undo_last_meshing_operation(service, version, mode, path + ["undo_last_meshing_operation"])
                self.verbosity = self.__class__.verbosity(service, version, mode, path + ["verbosity"])
                self.volume_specification = self.__class__.volume_specification(service, version, mode, path + ["volume_specification"])
                super().__init__(service, version, mode, path)
            class boundary_mesh_optimization(TUIMethod):
                """
                Set optimization scheme for boundary mesh optimization in projection meshing.
                """
            class boundary_treatment(TUIMethod):
                """
                Choose the boundary treatment option (0: Projection , 1: Snapping).
                """
            class bounding_box(TUIMethod):
                """
                Define/Modify the bounding box around the geometry.
                """
            class create(TUIMethod):
                """
                Create rapid octree mesh.
                """
            class create_stair_step_mesh(TUIMethod):
                """
                Create rapid octree mesh with a cartesian boundary approximation.
                """
            class delete_poor_quality_cells(TUIMethod):
                """
                Delete all cells with orthogonal-quality less than 0.01.
                """
            class distribute_geometry(TUIMethod):
                """
                Distributes input geometry across partitions to reduce memory requirements.
                """
            class dry_run(TUIMethod):
                """
                If yes: Just print diagnostic information, do not create a mesh.
                """
            class estimate_cell_count(TUIMethod):
                """
                Give a quick estimate about the expected number of cells.
                """
            class extract_refinement_levels(TUIMethod):
                """
                Enables extraction of refinement levels for mesh adaption in Fluent.
                """
            class flow_volume(TUIMethod):
                """
                Specify the volume to be filled by the mesh.
                """
            class improve_geometry_resolution(TUIMethod):
                """
                Enables improved geometry resolution.
                """
            class input_object(TUIMethod):
                """
                Specify the boundary geometry for the Rapid Octree mesher.
                """
            class is_manifold_geo(TUIMethod):
                """
                Set to yes if the geomety is manifold (speed up mesh generation).
                """
            class reset_bounding_box(TUIMethod):
                """
                Redefine the bounding box extends to encompass the currently selected geoemtry.
                """
            class resolve_geometry(TUIMethod):
                """
                Set geometry resolution mode.
                """
            class undo_last_meshing_operation(TUIMethod):
                """
                Attempt to undo the last meshing operation.
                """
            class verbosity(TUIMethod):
                """
                Set rapid octree verbosity.
                """
            class volume_specification(TUIMethod):
                """
                Specify the volume to be filled by the mesh.
                """

            class advanced_meshing_options(TUIMenu):
                """
                Advanced and experimental options for octree mesh generation.
                """
                def __init__(self, service, version, mode, path):
                    self.activate_projection_layer_improvement_algorithm = self.__class__.activate_projection_layer_improvement_algorithm(service, version, mode, path + ["activate_projection_layer_improvement_algorithm"])
                    self.align_surface_normals = self.__class__.align_surface_normals(service, version, mode, path + ["align_surface_normals"])
                    self.aspect_ratio_skewness_limit = self.__class__.aspect_ratio_skewness_limit(service, version, mode, path + ["aspect_ratio_skewness_limit"])
                    self.auto_align_surface_normals = self.__class__.auto_align_surface_normals(service, version, mode, path + ["auto_align_surface_normals"])
                    self.distance_erosion_factor = self.__class__.distance_erosion_factor(service, version, mode, path + ["distance_erosion_factor"])
                    self.improved_proximity_for_projection = self.__class__.improved_proximity_for_projection(service, version, mode, path + ["improved_proximity_for_projection"])
                    self.max_num_inflection_point_iter = self.__class__.max_num_inflection_point_iter(service, version, mode, path + ["max_num_inflection_point_iter"])
                    self.planar_feature_recovery_mode = self.__class__.planar_feature_recovery_mode(service, version, mode, path + ["planar_feature_recovery_mode"])
                    self.prism_stack_pullback = self.__class__.prism_stack_pullback(service, version, mode, path + ["prism_stack_pullback"])
                    self.projection_priority_zones = self.__class__.projection_priority_zones(service, version, mode, path + ["projection_priority_zones"])
                    self.pseudo_normal_mode = self.__class__.pseudo_normal_mode(service, version, mode, path + ["pseudo_normal_mode"])
                    self.rename_bounding_box_zones = self.__class__.rename_bounding_box_zones(service, version, mode, path + ["rename_bounding_box_zones"])
                    self.target_bnd_face_warp = self.__class__.target_bnd_face_warp(service, version, mode, path + ["target_bnd_face_warp"])
                    self.target_cell_orthoskew = self.__class__.target_cell_orthoskew(service, version, mode, path + ["target_cell_orthoskew"])
                    self.target_int_face_warp = self.__class__.target_int_face_warp(service, version, mode, path + ["target_int_face_warp"])
                    self.use_cg_based_smoothing = self.__class__.use_cg_based_smoothing(service, version, mode, path + ["use_cg_based_smoothing"])
                    super().__init__(service, version, mode, path)
                class activate_projection_layer_improvement_algorithm(TUIMethod):
                    """
                    Force the projection algorithm to do smoothing expansion without prisms defined.
                    """
                class align_surface_normals(TUIMethod):
                    """
                    Adjust the geometries normal orientation according to the current volume specification.
                    """
                class aspect_ratio_skewness_limit(TUIMethod):
                    """
                    Ignore cells with higher skew in aspect ratio improvement.
                    """
                class auto_align_surface_normals(TUIMethod):
                    """
                    Activates atuomatic orientation of facet normals for better proximity detection.
                    """
                class distance_erosion_factor(TUIMethod):
                    """
                    Set distance erosion factor as a factor of prism edge length.
                    """
                class improved_proximity_for_projection(TUIMethod):
                    """
                    Activate the imporved version of proximity refinement for projection boundary treatment.
                    """
                class max_num_inflection_point_iter(TUIMethod):
                    """
                    Sets the maximum number of iterations for inflection point removal during projection front fix.
                    """
                class planar_feature_recovery_mode(TUIMethod):
                    """
                    Set the mode for planar feature recovery from 0:off to 2: with hanging nodes.
                    """
                class prism_stack_pullback(TUIMethod):
                    """
                    Enable algorithm to use pullback scheme on subdivided prism stack to ensure positive volumes in case of bad cells.
                    """
                class projection_priority_zones(TUIMethod):
                    """
                    Prioritize zone association of faces crossing multiple boundary zones.
                    """
                class pseudo_normal_mode(TUIMethod):
                    """
                    Sets the mode for cumputing projection front sudo normals.
                    """
                class rename_bounding_box_zones(TUIMethod):
                    """
                    Set flag to change naming scheme of bounding box surface zones.
                    """
                class target_bnd_face_warp(TUIMethod):
                    """
                    Set target face warpage for boundary faces in mesh (-1.0 - 1.0). Higher values are likely to increase pullback.
                    """
                class target_cell_orthoskew(TUIMethod):
                    """
                    Set target orthoskew in mesh (0.0-1.0). Smaller values are likely to increase pullback.
                    """
                class target_int_face_warp(TUIMethod):
                    """
                    Set target face warpage for interior faces in mesh (-1.0 - 1.0). Higher values are likely to increase pullback.
                    """
                class use_cg_based_smoothing(TUIMethod):
                    """
                    Use a conjugate gradient method for volume mesh smoothing instead of Laplacian smoothing.
                    """

            class boundary_layer_mesh_configuration(TUIMenu):
                """
                Define anisotropic refinements of the projection layer (prismatic layers).
                """
                def __init__(self, service, version, mode, path):
                    self.add = self.__class__.add(service, version, mode, path + ["add"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
                    self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    super().__init__(service, version, mode, path)
                class add(TUIMethod):
                    """
                    Add a boudnary layer definition.
                    """
                class delete(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                class delete_all(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                class edit(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """
                class list(TUIMethod):
                    """
                    Specify the number of prismatic layers for surface zones.
                    """

            class geometry(TUIMenu):
                """
                Specify input for Rapid-Octree like material points, mesh objects, etc.
                """
                def __init__(self, service, version, mode, path):
                    self.bounding_box = self.__class__.bounding_box(service, version, mode, path + ["bounding_box"])
                    self.distribute_geometry = self.__class__.distribute_geometry(service, version, mode, path + ["distribute_geometry"])
                    self.input_object = self.__class__.input_object(service, version, mode, path + ["input_object"])
                    self.reference_size = self.__class__.reference_size(service, version, mode, path + ["reference_size"])
                    self.reset_bounding_box = self.__class__.reset_bounding_box(service, version, mode, path + ["reset_bounding_box"])
                    self.volume_specification = self.__class__.volume_specification(service, version, mode, path + ["volume_specification"])
                    super().__init__(service, version, mode, path)
                class bounding_box(TUIMethod):
                    """
                    Define/Modify the bounding box around the geometry.
                    """
                class distribute_geometry(TUIMethod):
                    """
                    Distributes input geometry across partitions to reduce memory requirements.
                    """
                class input_object(TUIMethod):
                    """
                    Specify the boundary geometry for the Rapid Octree mesher.
                    """
                class reference_size(TUIMethod):
                    """
                    Expands the currently defined bounding box to make the given cell size realizable.
                    """
                class reset_bounding_box(TUIMethod):
                    """
                    Redefine the bounding box extends to encompass the currently selected geoemtry.
                    """
                class volume_specification(TUIMethod):
                    """
                    Specify the volume to be filled by the mesh.
                    """

            class mesh_sizing(TUIMenu):
                """
                Define cell sizes.
                """
                def __init__(self, service, version, mode, path):
                    self.curvature_refinement_options = self.__class__.curvature_refinement_options(service, version, mode, path + ["curvature_refinement_options"])
                    self.add_surface_sizing = self.__class__.add_surface_sizing(service, version, mode, path + ["add_surface_sizing"])
                    self.boundary_layers = self.__class__.boundary_layers(service, version, mode, path + ["boundary_layers"])
                    self.buffer_layers = self.__class__.buffer_layers(service, version, mode, path + ["buffer_layers"])
                    self.change_surface_sizing = self.__class__.change_surface_sizing(service, version, mode, path + ["change_surface_sizing"])
                    self.clear_all_surface_sizings = self.__class__.clear_all_surface_sizings(service, version, mode, path + ["clear_all_surface_sizings"])
                    self.default_boundary_cell_size = self.__class__.default_boundary_cell_size(service, version, mode, path + ["default_boundary_cell_size"])
                    self.delete_surface_sizing = self.__class__.delete_surface_sizing(service, version, mode, path + ["delete_surface_sizing"])
                    self.list_surface_sizings = self.__class__.list_surface_sizings(service, version, mode, path + ["list_surface_sizings"])
                    self.max_cell_size = self.__class__.max_cell_size(service, version, mode, path + ["max_cell_size"])
                    self.mesh_coarsening_exponent = self.__class__.mesh_coarsening_exponent(service, version, mode, path + ["mesh_coarsening_exponent"])
                    self.smooth_mesh_coarsening = self.__class__.smooth_mesh_coarsening(service, version, mode, path + ["smooth_mesh_coarsening"])
                    self.surface_coarsening_layers = self.__class__.surface_coarsening_layers(service, version, mode, path + ["surface_coarsening_layers"])
                    self.surface_transition_layers = self.__class__.surface_transition_layers(service, version, mode, path + ["surface_transition_layers"])
                    self.volume_transition_exponent = self.__class__.volume_transition_exponent(service, version, mode, path + ["volume_transition_exponent"])
                    super().__init__(service, version, mode, path)
                class add_surface_sizing(TUIMethod):
                    """
                    Add a size function definition.
                    """
                class boundary_layers(TUIMethod):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry.
                    """
                class buffer_layers(TUIMethod):
                    """
                    Set the number of buffer layers.
                    """
                class change_surface_sizing(TUIMethod):
                    """
                    Change a size function definition.
                    """
                class clear_all_surface_sizings(TUIMethod):
                    """
                    Delete all size function definitions.
                    """
                class default_boundary_cell_size(TUIMethod):
                    """
                    Set the default cell size on the geometry.
                    """
                class delete_surface_sizing(TUIMethod):
                    """
                    Delete a size function definition.
                    """
                class list_surface_sizings(TUIMethod):
                    """
                    List all size function definitions.
                    """
                class max_cell_size(TUIMethod):
                    """
                    Set maximum cell size in octree mesh.
                    """
                class mesh_coarsening_exponent(TUIMethod):
                    """
                    Set the exponent (power of two) for mesh coarsening. Higher values will lead to a slower transiton from fine to coarse cells.
                    """
                class smooth_mesh_coarsening(TUIMethod):
                    """
                    Enable smoothing of the transitions between regions of different mesh sizes.
                    """
                class surface_coarsening_layers(TUIMethod):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry.
                    """
                class surface_transition_layers(TUIMethod):
                    """
                    Set the minimum number of constant-size cells adjacent to the geometry layer.
                    """
                class volume_transition_exponent(TUIMethod):
                    """
                    Set the exponent (power of two) for the mesh coarsening transition. A higher value results in a slower transition from fine to coarse cells.
                    """

                class curvature_refinement_options(TUIMenu):
                    """
                    Define options for curvature size functions.
                    """
                    def __init__(self, service, version, mode, path):
                        self.criterion = self.__class__.criterion(service, version, mode, path + ["criterion"])
                        self.maximum_angle_threshold = self.__class__.maximum_angle_threshold(service, version, mode, path + ["maximum_angle_threshold"])
                        self.minimum_angle_threshold = self.__class__.minimum_angle_threshold(service, version, mode, path + ["minimum_angle_threshold"])
                        self.switched_criterion_threshold = self.__class__.switched_criterion_threshold(service, version, mode, path + ["switched_criterion_threshold"])
                        super().__init__(service, version, mode, path)
                    class criterion(TUIMethod):
                        """
                        Sets the criterion for curvature size functions in Rapid-Octree.
                        """
                    class maximum_angle_threshold(TUIMethod):
                        """
                        Sets the maximum angle between two facets for angular refinements (e.g., to exclude sharp corners).
                        """
                    class minimum_angle_threshold(TUIMethod):
                        """
                        Sets the minimum angle between two facets for angular refinements (e.g., to prevent spurious refinements).
                        """
                    class switched_criterion_threshold(TUIMethod):
                        """
                        Specify the angular value to switch between "facets-normal-angle" and "arc-estimate" in the "switched" criterion.
                        """

            class refinement_regions(TUIMenu):
                """
                Enter the rapid octree refinement region menu.
                """
                def __init__(self, service, version, mode, path):
                    self.add = self.__class__.add(service, version, mode, path + ["add"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
                    self.list = self.__class__.list(service, version, mode, path + ["list"])
                    self.list_properties = self.__class__.list_properties(service, version, mode, path + ["list_properties"])
                    super().__init__(service, version, mode, path)
                class add(TUIMethod):
                    """
                    Add a new refinement region definition.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region definition.
                    """
                class edit(TUIMethod):
                    """
                    Edit a refinement region definition.
                    """
                class list(TUIMethod):
                    """
                    List all refinement region definitions.
                    """
                class list_properties(TUIMethod):
                    """
                    List the properties of a refinement region definition.
                    """

        class scoped_prisms(TUIMenu):
            """
            Manage scoped prisms.
            """
            def __init__(self, service, version, mode, path):
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.growth_options = self.__class__.growth_options(service, version, mode, path + ["growth_options"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
                self.poly_keep_nlayer_prism_characteristics = self.__class__.poly_keep_nlayer_prism_characteristics(service, version, mode, path + ["poly_keep_nlayer_prism_characteristics"])
                self.read = self.__class__.read(service, version, mode, path + ["read"])
                self.set_advanced_controls = self.__class__.set_advanced_controls(service, version, mode, path + ["set_advanced_controls"])
                self.set_no_imprint_zones = self.__class__.set_no_imprint_zones(service, version, mode, path + ["set_no_imprint_zones"])
                self.set_overset_prism_controls = self.__class__.set_overset_prism_controls(service, version, mode, path + ["set_overset_prism_controls"])
                self.tet_prism_stairstep_exposed_quads = self.__class__.tet_prism_stairstep_exposed_quads(service, version, mode, path + ["tet_prism_stairstep_exposed_quads"])
                self.write = self.__class__.write(service, version, mode, path + ["write"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create new scoped prism.
                """
            class delete(TUIMethod):
                """
                Delete scoped prisms.
                """
            class growth_options(TUIMethod):
                """
                Set scoped prisms growth options.
                """
            class list(TUIMethod):
                """
                List all scoped prisms parameters.
                """
            class modify(TUIMethod):
                """
                Modify scoped prisms.
                """
            class poly_keep_nlayer_prism_characteristics(TUIMethod):
                """
                Number of layers to maintain poly-prism characteristics.
                """
            class read(TUIMethod):
                """
                Read scoped prisms from a file.
                """
            class set_advanced_controls(TUIMethod):
                """
                Set scoped boundary layer controls.
                """
            class set_no_imprint_zones(TUIMethod):
                """
                Set zones which should not be imprinted during prism generation.
                """
            class set_overset_prism_controls(TUIMethod):
                """
                Set boundary layer controls for overset mesh generation.
                """
            class tet_prism_stairstep_exposed_quads(TUIMethod):
                """
                Tet-Prism Stairstep exposed quad.
                """
            class write(TUIMethod):
                """
                Write scoped prisms to a file.
                """

        class scoped_thin_volume(TUIMenu):
            """
            Enter the scoped thin volume mesh controls menu. .
            """
            def __init__(self, service, version, mode, path):
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.global_params = self.__class__.global_params(service, version, mode, path + ["global_params"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Auto Create thin volume control(s).
                """
            class delete(TUIMethod):
                """
                Create thin volume mesh on one or more face zones.
                """
            class global_params(TUIMethod):
                """
                Prime Auto Mesh thin volume global params.
                """
            class list(TUIMethod):
                """
                List thin volume control names.
                """

        class separate(TUIMenu):
            """
            Separate cells by various user defined methods.
            """
            def __init__(self, service, version, mode, path):
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.separate_cell_by_face = self.__class__.separate_cell_by_face(service, version, mode, path + ["separate_cell_by_face"])
                self.separate_cell_by_mark = self.__class__.separate_cell_by_mark(service, version, mode, path + ["separate_cell_by_mark"])
                self.separate_cell_by_region = self.__class__.separate_cell_by_region(service, version, mode, path + ["separate_cell_by_region"])
                self.separate_cell_by_shape = self.__class__.separate_cell_by_shape(service, version, mode, path + ["separate_cell_by_shape"])
                self.separate_cell_by_size = self.__class__.separate_cell_by_size(service, version, mode, path + ["separate_cell_by_size"])
                self.separate_cell_by_skew = self.__class__.separate_cell_by_skew(service, version, mode, path + ["separate_cell_by_skew"])
                self.separate_prisms_from_hex = self.__class__.separate_prisms_from_hex(service, version, mode, path + ["separate_prisms_from_hex"])
                self.separate_prisms_from_poly = self.__class__.separate_prisms_from_poly(service, version, mode, path + ["separate_prisms_from_poly"])
                self.separate_wedge_prisms = self.__class__.separate_wedge_prisms(service, version, mode, path + ["separate_wedge_prisms"])
                super().__init__(service, version, mode, path)
            class separate_cell_by_face(TUIMethod):
                """
                Separate prism cell with source faces.
                """
            class separate_cell_by_mark(TUIMethod):
                """
                Separate cell by marks.
                """
            class separate_cell_by_region(TUIMethod):
                """
                Separate cell by region.
                """
            class separate_cell_by_shape(TUIMethod):
                """
                Separate cell thread by cell shape.
                """
            class separate_cell_by_size(TUIMethod):
                """
                Separate cell thread by cell size.
                """
            class separate_cell_by_skew(TUIMethod):
                """
                Separate cell thread by cell skewness.
                """
            class separate_prisms_from_hex(TUIMethod):
                """
                Separate prism cells from hex.
                """
            class separate_prisms_from_poly(TUIMethod):
                """
                Separate poly-prism cells from poly.
                """
            class separate_wedge_prisms(TUIMethod):
                """
                Separate wedge-prism cells from bulk.
                """

            class local_regions(TUIMenu):
                """
                Enter the refine-local menu.
                """
                def __init__(self, service, version, mode, path):
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    super().__init__(service, version, mode, path)
                class define(TUIMethod):
                    """
                    Define a refinement region's parameters.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region.
                    """
                class init(TUIMethod):
                    """
                    Delete all current regions and add the default refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    List all refinement regions.
                    """

        class tet(TUIMenu):
            """
            Enter the triangulation menu.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                self.local_regions = self.__class__.local_regions(service, version, mode, path + ["local_regions"])
                self.delete_virtual_cells = self.__class__.delete_virtual_cells(service, version, mode, path + ["delete_virtual_cells"])
                self.init = self.__class__.init(service, version, mode, path + ["init"])
                self.init_refine = self.__class__.init_refine(service, version, mode, path + ["init_refine"])
                self.mesh_object = self.__class__.mesh_object(service, version, mode, path + ["mesh_object"])
                self.preserve_cell_zone = self.__class__.preserve_cell_zone(service, version, mode, path + ["preserve_cell_zone"])
                self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                self.trace_path_between_cells = self.__class__.trace_path_between_cells(service, version, mode, path + ["trace_path_between_cells"])
                self.un_preserve_cell_zone = self.__class__.un_preserve_cell_zone(service, version, mode, path + ["un_preserve_cell_zone"])
                super().__init__(service, version, mode, path)
            class delete_virtual_cells(TUIMethod):
                """
                Delete virtual face/dead cells left by activating keep-virtual-entities?.
                """
            class init(TUIMethod):
                """
                Tet mesh initialization.
                """
            class init_refine(TUIMethod):
                """
                Tet initialization and refinement of mesh.
                """
            class mesh_object(TUIMethod):
                """
                Tet mesh object of type mesh.
                """
            class preserve_cell_zone(TUIMethod):
                """
                Preserve cell zone.
                """
            class refine(TUIMethod):
                """
                Tet mesh refinement.
                """
            class trace_path_between_cells(TUIMethod):
                """
                Trace path between two cell.
                """
            class un_preserve_cell_zone(TUIMethod):
                """
                Un-preserve cell zone.
                """

            class controls(TUIMenu):
                """
                Tet controls.
                """
                def __init__(self, service, version, mode, path):
                    self.adv_front_method = self.__class__.adv_front_method(service, version, mode, path + ["adv_front_method"])
                    self.advanced = self.__class__.advanced(service, version, mode, path + ["advanced"])
                    self.improve_mesh = self.__class__.improve_mesh(service, version, mode, path + ["improve_mesh"])
                    self.remove_slivers = self.__class__.remove_slivers(service, version, mode, path + ["remove_slivers"])
                    self.tet_improve = self.__class__.tet_improve(service, version, mode, path + ["tet_improve"])
                    self.cell_sizing = self.__class__.cell_sizing(service, version, mode, path + ["cell_sizing"])
                    self.clear_zone_growth_rate = self.__class__.clear_zone_growth_rate(service, version, mode, path + ["clear_zone_growth_rate"])
                    self.compute_max_cell_volume = self.__class__.compute_max_cell_volume(service, version, mode, path + ["compute_max_cell_volume"])
                    self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                    self.delete_unused_nodes = self.__class__.delete_unused_nodes(service, version, mode, path + ["delete_unused_nodes"])
                    self.improve_surface_mesh = self.__class__.improve_surface_mesh(service, version, mode, path + ["improve_surface_mesh"])
                    self.max_cell_length = self.__class__.max_cell_length(service, version, mode, path + ["max_cell_length"])
                    self.max_cell_volume = self.__class__.max_cell_volume(service, version, mode, path + ["max_cell_volume"])
                    self.merge_free_nodes = self.__class__.merge_free_nodes(service, version, mode, path + ["merge_free_nodes"])
                    self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                    self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                    self.refine_method = self.__class__.refine_method(service, version, mode, path + ["refine_method"])
                    self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                    self.set_zone_growth_rate = self.__class__.set_zone_growth_rate(service, version, mode, path + ["set_zone_growth_rate"])
                    self.skewness_method = self.__class__.skewness_method(service, version, mode, path + ["skewness_method"])
                    self.use_max_cell_size = self.__class__.use_max_cell_size(service, version, mode, path + ["use_max_cell_size"])
                    super().__init__(service, version, mode, path)
                class cell_sizing(TUIMethod):
                    """
                    Allow cell volume distribution to be determined based on boundary.
                    """
                class clear_zone_growth_rate(TUIMethod):
                    """
                    Clear zone specific geometric growth rates.
                    """
                class compute_max_cell_volume(TUIMethod):
                    """
                    Computes max cell size.
                    """
                class delete_dead_zones(TUIMethod):
                    """
                    Automatically delete dead face and cell zones?.
                    """
                class delete_unused_nodes(TUIMethod):
                    """
                    Automatically delete unused nodes?.
                    """
                class improve_surface_mesh(TUIMethod):
                    """
                    Automatically improve surface mesh?.
                    """
                class max_cell_length(TUIMethod):
                    """
                    Set max-cell-length.
                    """
                class max_cell_volume(TUIMethod):
                    """
                    Set max-cell-volume.
                    """
                class merge_free_nodes(TUIMethod):
                    """
                    Automatically merge duplicate nodes?.
                    """
                class non_fluid_type(TUIMethod):
                    """
                    Select the default non-fluid cell zone type.
                    """
                class print_region_based_sizing(TUIMethod):
                    """
                    Print region based sizings.
                    """
                class refine_method(TUIMethod):
                    """
                    Define refinement method.
                    """
                class set_region_based_sizing(TUIMethod):
                    """
                    Set region based sizings.
                    """
                class set_zone_growth_rate(TUIMethod):
                    """
                    Set zone specific geometric growth rates.
                    """
                class skewness_method(TUIMethod):
                    """
                    Skewness refinement controls.
                    """
                class use_max_cell_size(TUIMethod):
                    """
                    Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed.
                    """

                class adv_front_method(TUIMenu):
                    """
                    Advancing front refinement controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.skew_improve = self.__class__.skew_improve(service, version, mode, path + ["skew_improve"])
                        self.first_improve_params = self.__class__.first_improve_params(service, version, mode, path + ["first_improve_params"])
                        self.refine_parameters = self.__class__.refine_parameters(service, version, mode, path + ["refine_parameters"])
                        self.second_improve_params = self.__class__.second_improve_params(service, version, mode, path + ["second_improve_params"])
                        super().__init__(service, version, mode, path)
                    class first_improve_params(TUIMethod):
                        """
                        Define refine front improve parameters.
                        """
                    class refine_parameters(TUIMethod):
                        """
                        Define refine parameters.
                        """
                    class second_improve_params(TUIMethod):
                        """
                        Define cell zone improve parameters.
                        """

                    class skew_improve(TUIMenu):
                        """
                        Refine improve controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                            self.boundary_sliver_skew = self.__class__.boundary_sliver_skew(service, version, mode, path + ["boundary_sliver_skew"])
                            self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                            self.sliver_skew = self.__class__.sliver_skew(service, version, mode, path + ["sliver_skew"])
                            self.target = self.__class__.target(service, version, mode, path + ["target"])
                            self.target_low_skew = self.__class__.target_low_skew(service, version, mode, path + ["target_low_skew"])
                            self.target_skew = self.__class__.target_skew(service, version, mode, path + ["target_skew"])
                            super().__init__(service, version, mode, path)
                        class attempts(TUIMethod):
                            """
                            Refine improve attempts.
                            """
                        class boundary_sliver_skew(TUIMethod):
                            """
                            Refine improve boundary sliver skew.
                            """
                        class iterations(TUIMethod):
                            """
                            Refine improve iterations.
                            """
                        class sliver_skew(TUIMethod):
                            """
                            Refine improve sliver skew.
                            """
                        class target(TUIMethod):
                            """
                            Activate target skew refinement.
                            """
                        class target_low_skew(TUIMethod):
                            """
                            Refine improve target low skew.
                            """
                        class target_skew(TUIMethod):
                            """
                            Refine improve target skew.
                            """

                class advanced(TUIMenu):
                    """
                    Tet advanced controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.defaults = self.__class__.defaults(service, version, mode, path + ["defaults"])
                        self.freeze_boundary_cells = self.__class__.freeze_boundary_cells(service, version, mode, path + ["freeze_boundary_cells"])
                        self.keep_virtual_entities = self.__class__.keep_virtual_entities(service, version, mode, path + ["keep_virtual_entities"])
                        self.max_cells = self.__class__.max_cells(service, version, mode, path + ["max_cells"])
                        self.max_nodes = self.__class__.max_nodes(service, version, mode, path + ["max_nodes"])
                        self.node_tolerance = self.__class__.node_tolerance(service, version, mode, path + ["node_tolerance"])
                        self.progress_reports = self.__class__.progress_reports(service, version, mode, path + ["progress_reports"])
                        self.report_max_unmeshed = self.__class__.report_max_unmeshed(service, version, mode, path + ["report_max_unmeshed"])
                        self.report_unmeshed_faces = self.__class__.report_unmeshed_faces(service, version, mode, path + ["report_unmeshed_faces"])
                        self.report_unmeshed_nodes = self.__class__.report_unmeshed_nodes(service, version, mode, path + ["report_unmeshed_nodes"])
                        self.sliver_size = self.__class__.sliver_size(service, version, mode, path + ["sliver_size"])
                        super().__init__(service, version, mode, path)
                    class defaults(TUIMethod):
                        """
                        Calculate defaults.
                        """
                    class freeze_boundary_cells(TUIMethod):
                        """
                        Freeze boundary cells .
                        """
                    class keep_virtual_entities(TUIMethod):
                        """
                        Toggle deletion of virtual entities after intialization.
                        """
                    class max_cells(TUIMethod):
                        """
                        Set maximum number of cells in mesh.
                        """
                    class max_nodes(TUIMethod):
                        """
                        Set maximum number of nodes in mesh.
                        """
                    class node_tolerance(TUIMethod):
                        """
                        Set node-tolerance.
                        """
                    class progress_reports(TUIMethod):
                        """
                        Set time between progress reports in seconds.
                        """
                    class report_max_unmeshed(TUIMethod):
                        """
                        Max number of unmeshed entities reported.
                        """
                    class report_unmeshed_faces(TUIMethod):
                        """
                        Report unmeshed faces.
                        """
                    class report_unmeshed_nodes(TUIMethod):
                        """
                        Report unmeshed nodes.
                        """
                    class sliver_size(TUIMethod):
                        """
                        Set sliver-size.
                        """

                class improve_mesh(TUIMenu):
                    """
                    Improve mesh controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                        self.laplace_smooth = self.__class__.laplace_smooth(service, version, mode, path + ["laplace_smooth"])
                        self.skewness_smooth = self.__class__.skewness_smooth(service, version, mode, path + ["skewness_smooth"])
                        self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                        super().__init__(service, version, mode, path)
                    class improve(TUIMethod):
                        """
                        Automatically improve mesh.
                        """
                    class laplace_smooth(TUIMethod):
                        """
                        Laplace smooth parameters.
                        """
                    class skewness_smooth(TUIMethod):
                        """
                        Skewness smooth parametersx.
                        """
                    class swap(TUIMethod):
                        """
                        Face swap parameters.
                        """

                class remove_slivers(TUIMenu):
                    """
                    Sliver remove controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                        self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                        self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                        self.low_skew = self.__class__.low_skew(service, version, mode, path + ["low_skew"])
                        self.method = self.__class__.method(service, version, mode, path + ["method"])
                        self.remove = self.__class__.remove(service, version, mode, path + ["remove"])
                        self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                        super().__init__(service, version, mode, path)
                    class angle(TUIMethod):
                        """
                        Max dihedral angle defining a valid boundary sliver.
                        """
                    class attempts(TUIMethod):
                        """
                        Sliver remove attempts.
                        """
                    class iterations(TUIMethod):
                        """
                        Sliver remove iterations.
                        """
                    class low_skew(TUIMethod):
                        """
                        Remove sliver low skew.
                        """
                    class method(TUIMethod):
                        """
                        Sliver remove method.
                        """
                    class remove(TUIMethod):
                        """
                        Automatically remove slivers.
                        """
                    class skew(TUIMethod):
                        """
                        Remove sliver skew.
                        """

                class tet_improve(TUIMenu):
                    """
                    Improve cells controls.
                    """
                    def __init__(self, service, version, mode, path):
                        self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                        self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                        self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                        self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                        super().__init__(service, version, mode, path)
                    class angle(TUIMethod):
                        """
                        Max dihedral angle defining a valid boundary cell.
                        """
                    class attempts(TUIMethod):
                        """
                        Improve attempts.
                        """
                    class iterations(TUIMethod):
                        """
                        Improve iterations.
                        """
                    class skew(TUIMethod):
                        """
                        Remove skew.
                        """

            class improve(TUIMenu):
                """
                Enter the Tet improve menu.
                """
                def __init__(self, service, version, mode, path):
                    self.collapse_slivers = self.__class__.collapse_slivers(service, version, mode, path + ["collapse_slivers"])
                    self.improve_cells = self.__class__.improve_cells(service, version, mode, path + ["improve_cells"])
                    self.refine_boundary_slivers = self.__class__.refine_boundary_slivers(service, version, mode, path + ["refine_boundary_slivers"])
                    self.refine_slivers = self.__class__.refine_slivers(service, version, mode, path + ["refine_slivers"])
                    self.skew_smooth_nodes = self.__class__.skew_smooth_nodes(service, version, mode, path + ["skew_smooth_nodes"])
                    self.sliver_boundary_swap = self.__class__.sliver_boundary_swap(service, version, mode, path + ["sliver_boundary_swap"])
                    self.smooth_boundary_sliver = self.__class__.smooth_boundary_sliver(service, version, mode, path + ["smooth_boundary_sliver"])
                    self.smooth_interior_sliver = self.__class__.smooth_interior_sliver(service, version, mode, path + ["smooth_interior_sliver"])
                    self.smooth_nodes = self.__class__.smooth_nodes(service, version, mode, path + ["smooth_nodes"])
                    self.swap_faces = self.__class__.swap_faces(service, version, mode, path + ["swap_faces"])
                    super().__init__(service, version, mode, path)
                class collapse_slivers(TUIMethod):
                    """
                    Remove skewed cells by edge collapse.
                    """
                class improve_cells(TUIMethod):
                    """
                    Improve skewed cells.
                    """
                class refine_boundary_slivers(TUIMethod):
                    """
                    Refine boundary slivers by edge-split.
                    """
                class refine_slivers(TUIMethod):
                    """
                    Refine sliver cells by introducing
                    node near centroid.
                    """
                class skew_smooth_nodes(TUIMethod):
                    """
                    Smooth node locations.
                    """
                class sliver_boundary_swap(TUIMethod):
                    """
                    Remove boundary slivers by moving the boundary
                    to exclude the cells from the zone.
                    """
                class smooth_boundary_sliver(TUIMethod):
                    """
                    Smooth skewed cells with all nodes on the boundary.
                    """
                class smooth_interior_sliver(TUIMethod):
                    """
                    Smooth skewed cells with some interior node.
                    """
                class smooth_nodes(TUIMethod):
                    """
                    Smooth node locations.
                    """
                class swap_faces(TUIMethod):
                    """
                    Perform interior face swapping to improve cell skewness.
                    """

            class local_regions(TUIMenu):
                """
                Enter the refine-local menu.
                """
                def __init__(self, service, version, mode, path):
                    self.activate = self.__class__.activate(service, version, mode, path + ["activate"])
                    self.deactivate = self.__class__.deactivate(service, version, mode, path + ["deactivate"])
                    self.define = self.__class__.define(service, version, mode, path + ["define"])
                    self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                    self.ideal_area = self.__class__.ideal_area(service, version, mode, path + ["ideal_area"])
                    self.ideal_vol = self.__class__.ideal_vol(service, version, mode, path + ["ideal_vol"])
                    self.init = self.__class__.init(service, version, mode, path + ["init"])
                    self.list_all_regions = self.__class__.list_all_regions(service, version, mode, path + ["list_all_regions"])
                    self.refine = self.__class__.refine(service, version, mode, path + ["refine"])
                    super().__init__(service, version, mode, path)
                class activate(TUIMethod):
                    """
                    Activate regions for tet refinement.
                    """
                class deactivate(TUIMethod):
                    """
                    Activate regions for tet refinement.
                    """
                class define(TUIMethod):
                    """
                    Define a refinement region's parameters.
                    """
                class delete(TUIMethod):
                    """
                    Delete a refinement region.
                    """
                class ideal_area(TUIMethod):
                    """
                    Ideal triangle area for given edge length.
                    """
                class ideal_vol(TUIMethod):
                    """
                    Ideal tet volume for given edge length.
                    """
                class init(TUIMethod):
                    """
                    Delete all current regions and add the default refinement region.
                    """
                class list_all_regions(TUIMethod):
                    """
                    List all refinement regions.
                    """
                class refine(TUIMethod):
                    """
                    Refine live cells inside region based on refinement parameters.
                    """

        class thin_volume_mesh(TUIMenu):
            """
            Enter the thin volume mesh controls menu.
            """
            def __init__(self, service, version, mode, path):
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                super().__init__(service, version, mode, path)
            class create(TUIMethod):
                """
                Create thin volume mesh on one or more face zones.
                """

    class objects(TUIMenu):
        """
        Manage objects.
        """
        def __init__(self, service, version, mode, path):
            self.cad_association = self.__class__.cad_association(service, version, mode, path + ["cad_association"])
            self.create_new_mesh_object = self.__class__.create_new_mesh_object(service, version, mode, path + ["create_new_mesh_object"])
            self.deprecated = self.__class__.deprecated(service, version, mode, path + ["deprecated"])
            self.fix_holes = self.__class__.fix_holes(service, version, mode, path + ["fix_holes"])
            self.join_intersect = self.__class__.join_intersect(service, version, mode, path + ["join_intersect"])
            self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
            self.remove_gaps = self.__class__.remove_gaps(service, version, mode, path + ["remove_gaps"])
            self.set = self.__class__.set(service, version, mode, path + ["set"])
            self.volumetric_regions = self.__class__.volumetric_regions(service, version, mode, path + ["volumetric_regions"])
            self.wrap = self.__class__.wrap(service, version, mode, path + ["wrap"])
            self.change_object_type = self.__class__.change_object_type(service, version, mode, path + ["change_object_type"])
            self.change_prefix = self.__class__.change_prefix(service, version, mode, path + ["change_prefix"])
            self.change_suffix = self.__class__.change_suffix(service, version, mode, path + ["change_suffix"])
            self.check_mesh = self.__class__.check_mesh(service, version, mode, path + ["check_mesh"])
            self.clear_backup = self.__class__.clear_backup(service, version, mode, path + ["clear_backup"])
            self.create = self.__class__.create(service, version, mode, path + ["create"])
            self.create_and_activate_domain = self.__class__.create_and_activate_domain(service, version, mode, path + ["create_and_activate_domain"])
            self.create_groups = self.__class__.create_groups(service, version, mode, path + ["create_groups"])
            self.create_intersection_loops = self.__class__.create_intersection_loops(service, version, mode, path + ["create_intersection_loops"])
            self.create_multiple = self.__class__.create_multiple(service, version, mode, path + ["create_multiple"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
            self.delete_all_geom = self.__class__.delete_all_geom(service, version, mode, path + ["delete_all_geom"])
            self.delete_unreferenced_faces_and_edges = self.__class__.delete_unreferenced_faces_and_edges(service, version, mode, path + ["delete_unreferenced_faces_and_edges"])
            self.extract_edges = self.__class__.extract_edges(service, version, mode, path + ["extract_edges"])
            self.improve_feature_capture = self.__class__.improve_feature_capture(service, version, mode, path + ["improve_feature_capture"])
            self.improve_object_quality = self.__class__.improve_object_quality(service, version, mode, path + ["improve_object_quality"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
            self.merge_edges = self.__class__.merge_edges(service, version, mode, path + ["merge_edges"])
            self.merge_nodes = self.__class__.merge_nodes(service, version, mode, path + ["merge_nodes"])
            self.merge_voids = self.__class__.merge_voids(service, version, mode, path + ["merge_voids"])
            self.merge_walls = self.__class__.merge_walls(service, version, mode, path + ["merge_walls"])
            self.rename_cell_zone_boundaries_using_labels = self.__class__.rename_cell_zone_boundaries_using_labels(service, version, mode, path + ["rename_cell_zone_boundaries_using_labels"])
            self.rename_object = self.__class__.rename_object(service, version, mode, path + ["rename_object"])
            self.rename_object_zones = self.__class__.rename_object_zones(service, version, mode, path + ["rename_object_zones"])
            self.restore_faces = self.__class__.restore_faces(service, version, mode, path + ["restore_faces"])
            self.rotate = self.__class__.rotate(service, version, mode, path + ["rotate"])
            self.scale = self.__class__.scale(service, version, mode, path + ["scale"])
            self.separate_faces_by_angle = self.__class__.separate_faces_by_angle(service, version, mode, path + ["separate_faces_by_angle"])
            self.separate_faces_by_seed = self.__class__.separate_faces_by_seed(service, version, mode, path + ["separate_faces_by_seed"])
            self.sew = self.__class__.sew(service, version, mode, path + ["sew"])
            self.summary = self.__class__.summary(service, version, mode, path + ["summary"])
            self.translate = self.__class__.translate(service, version, mode, path + ["translate"])
            self.update = self.__class__.update(service, version, mode, path + ["update"])
            super().__init__(service, version, mode, path)
        class change_object_type(TUIMethod):
            """
            Change object type.
            """
        class change_prefix(TUIMethod):
            """
            Change the prefix for specified objects.
            """
        class change_suffix(TUIMethod):
            """
            Change the suffix for specified objects.
            """
        class check_mesh(TUIMethod):
            """
            Check mesh.
            """
        class clear_backup(TUIMethod):
            """
            Clear backup data of objects.
            """
        class create(TUIMethod):
            """
            Create an object with closed face zones.
            """
        class create_and_activate_domain(TUIMethod):
            """
            Create and activate domain with all face zones of Objects.
            """
        class create_groups(TUIMethod):
            """
            Create a face and edge zone group from Objects.
            """
        class create_intersection_loops(TUIMethod):
            """
            Create intersection loops for face zones of objects.
            """
        class create_multiple(TUIMethod):
            """
            Create multiple objects one for each face zone passed.
            """
        class delete(TUIMethod):
            """
            Delete Objects.
            """
        class delete_all(TUIMethod):
            """
            Delete all objects.
            """
        class delete_all_geom(TUIMethod):
            """
            Delete all objects of type geom.
            """
        class delete_unreferenced_faces_and_edges(TUIMethod):
            """
            Delete unreferenced faces and edges.
            """
        class extract_edges(TUIMethod):
            """
            Extract edges for the Objects.
            """
        class improve_feature_capture(TUIMethod):
            """
            Imprint edges of object on to faces of object.
            """
        class improve_object_quality(TUIMethod):
            """
            Improve mesh objects quality.
            """
        class list(TUIMethod):
            """
            Print existing objects.
            """
        class merge(TUIMethod):
            """
            Merge volume objects.
            """
        class merge_edges(TUIMethod):
            """
            Merge edges of Objects.
            """
        class merge_nodes(TUIMethod):
            """
            Merge nodes of an object.
            """
        class merge_voids(TUIMethod):
            """
            Merge voids/packets.
            """
        class merge_walls(TUIMethod):
            """
            Merge walls of Objects.
            """
        class rename_cell_zone_boundaries_using_labels(TUIMethod):
            """
            Rename cell zone boundaries using the label names.
            """
        class rename_object(TUIMethod):
            """
            Rename object name.
            """
        class rename_object_zones(TUIMethod):
            """
            Rename zones of the objects based on the object name.
            """
        class restore_faces(TUIMethod):
            """
            Restore object boundaries.
            """
        class rotate(TUIMethod):
            """
            Rotate objects.
            """
        class scale(TUIMethod):
            """
            Scale objects.
            """
        class separate_faces_by_angle(TUIMethod):
            """
            Separate faces of object.
            """
        class separate_faces_by_seed(TUIMethod):
            """
            Separate faces of all object based on given face seed and angle.
            """
        class sew(TUIMethod):
            """
            Enter the sew operation menu.
            """
        class summary(TUIMethod):
            """
            List summary by object name or geom/mesh group.
            """
        class translate(TUIMethod):
            """
            Translate objects.
            """
        class update(TUIMethod):
            """
            Remove invalid/deleted zones from object's face/edge list.
            """

        class cad_association(TUIMenu):
            """
            Objects association with CAD entities.
            """
            def __init__(self, service, version, mode, path):
                self.attach_cad = self.__class__.attach_cad(service, version, mode, path + ["attach_cad"])
                self.detach_all_objects = self.__class__.detach_all_objects(service, version, mode, path + ["detach_all_objects"])
                self.detach_objects = self.__class__.detach_objects(service, version, mode, path + ["detach_objects"])
                self.query_object_association = self.__class__.query_object_association(service, version, mode, path + ["query_object_association"])
                self.restore_cad = self.__class__.restore_cad(service, version, mode, path + ["restore_cad"])
                self.unlock_cad = self.__class__.unlock_cad(service, version, mode, path + ["unlock_cad"])
                self.update_all_objects = self.__class__.update_all_objects(service, version, mode, path + ["update_all_objects"])
                self.update_objects = self.__class__.update_objects(service, version, mode, path + ["update_objects"])
                super().__init__(service, version, mode, path)
            class attach_cad(TUIMethod):
                """
                Attach Object association.
                """
            class detach_all_objects(TUIMethod):
                """
                Detach all Objects from CAD association.
                """
            class detach_objects(TUIMethod):
                """
                Detach Objects from CAD association.
                """
            class query_object_association(TUIMethod):
                """
                Query Object associations.
                """
            class restore_cad(TUIMethod):
                """
                Restore Object associations.
                """
            class unlock_cad(TUIMethod):
                """
                Unlock Object associations.
                """
            class update_all_objects(TUIMethod):
                """
                Update all Objects from CAD association.
                """
            class update_objects(TUIMethod):
                """
                Update Objects from CAD association.
                """

        class create_new_mesh_object(TUIMenu):
            """
            Create new mesh objects br wrap or remesh.
            """
            def __init__(self, service, version, mode, path):
                self.remesh = self.__class__.remesh(service, version, mode, path + ["remesh"])
                self.wrap = self.__class__.wrap(service, version, mode, path + ["wrap"])
                super().__init__(service, version, mode, path)
            class remesh(TUIMethod):
                """
                Remesh objects.
                """
            class wrap(TUIMethod):
                """
                Wrap objects.
                """

        class deprecated(TUIMenu):
            """
            Deprecated features.
            """
            def __init__(self, service, version, mode, path):
                self.create_mesh_object_from_wrap = self.__class__.create_mesh_object_from_wrap(service, version, mode, path + ["create_mesh_object_from_wrap"])
                super().__init__(service, version, mode, path)
            class create_mesh_object_from_wrap(TUIMethod):
                """
                Create mesh object from a wrap object.
                """

        class fix_holes(TUIMenu):
            """
            Fix holes in surface mesh using octree.
            """
            def __init__(self, service, version, mode, path):
                self.advanced = self.__class__.advanced(service, version, mode, path + ["advanced"])
                self.find_holes = self.__class__.find_holes(service, version, mode, path + ["find_holes"])
                self.open_all_holes = self.__class__.open_all_holes(service, version, mode, path + ["open_all_holes"])
                self.open_holes = self.__class__.open_holes(service, version, mode, path + ["open_holes"])
                self.patch_all_holes = self.__class__.patch_all_holes(service, version, mode, path + ["patch_all_holes"])
                self.patch_holes = self.__class__.patch_holes(service, version, mode, path + ["patch_holes"])
                self.reset_material_point = self.__class__.reset_material_point(service, version, mode, path + ["reset_material_point"])
                self.shrink_wrap = self.__class__.shrink_wrap(service, version, mode, path + ["shrink_wrap"])
                super().__init__(service, version, mode, path)
            class find_holes(TUIMethod):
                """
                Find holes in objects using octree.
                """
            class open_all_holes(TUIMethod):
                """
                Open all wetted holes of the material point.
                """
            class open_holes(TUIMethod):
                """
                Open holes even not connected by material point.
                """
            class patch_all_holes(TUIMethod):
                """
                Patch all wetted holes of the material point.
                """
            class patch_holes(TUIMethod):
                """
                Patch holes even not connected by material point.
                """
            class reset_material_point(TUIMethod):
                """
                Reset material point of of region of interest.
                """
            class shrink_wrap(TUIMethod):
                """
                Shrink wrap wetted region of material point.
                """

            class advanced(TUIMenu):
                """
                Advanced fix holes options.
                """
                def __init__(self, service, version, mode, path):
                    self.open_holes_between_material_points = self.__class__.open_holes_between_material_points(service, version, mode, path + ["open_holes_between_material_points"])
                    self.open_holes_connected_to_material_points = self.__class__.open_holes_connected_to_material_points(service, version, mode, path + ["open_holes_connected_to_material_points"])
                    self.open_holes_not_connected_to_material_points = self.__class__.open_holes_not_connected_to_material_points(service, version, mode, path + ["open_holes_not_connected_to_material_points"])
                    self.open_traced_holes_between_material_points = self.__class__.open_traced_holes_between_material_points(service, version, mode, path + ["open_traced_holes_between_material_points"])
                    self.patch_holes_between_material_points = self.__class__.patch_holes_between_material_points(service, version, mode, path + ["patch_holes_between_material_points"])
                    self.patch_holes_connected_to_material_points = self.__class__.patch_holes_connected_to_material_points(service, version, mode, path + ["patch_holes_connected_to_material_points"])
                    self.patch_holes_not_connected_to_material_points = self.__class__.patch_holes_not_connected_to_material_points(service, version, mode, path + ["patch_holes_not_connected_to_material_points"])
                    super().__init__(service, version, mode, path)
                class open_holes_between_material_points(TUIMethod):
                    """
                    Open holes separating the material points to merge them.
                    """
                class open_holes_connected_to_material_points(TUIMethod):
                    """
                    Open all holes wetted by material points.
                    """
                class open_holes_not_connected_to_material_points(TUIMethod):
                    """
                    Open all holes other than holes wetted by material points.
                    """
                class open_traced_holes_between_material_points(TUIMethod):
                    """
                    Trace a path between material points and open holes part of the traced path.
                    """
                class patch_holes_between_material_points(TUIMethod):
                    """
                    Patch holes separating the material points.
                    """
                class patch_holes_connected_to_material_points(TUIMethod):
                    """
                    Patch all holes wetted by material points.
                    """
                class patch_holes_not_connected_to_material_points(TUIMethod):
                    """
                    Patch all holes other than holes wetted by material points.
                    """

        class join_intersect(TUIMenu):
            """
            Join, intersect and build regions in a mesh object.
            """
            def __init__(self, service, version, mode, path):
                self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
                self.add_objects_to_mesh_object = self.__class__.add_objects_to_mesh_object(service, version, mode, path + ["add_objects_to_mesh_object"])
                self.change_region_type = self.__class__.change_region_type(service, version, mode, path + ["change_region_type"])
                self.compute_regions = self.__class__.compute_regions(service, version, mode, path + ["compute_regions"])
                self.create_mesh_object = self.__class__.create_mesh_object(service, version, mode, path + ["create_mesh_object"])
                self.delete_region = self.__class__.delete_region(service, version, mode, path + ["delete_region"])
                self.intersect = self.__class__.intersect(service, version, mode, path + ["intersect"])
                self.join = self.__class__.join(service, version, mode, path + ["join"])
                self.list_regions = self.__class__.list_regions(service, version, mode, path + ["list_regions"])
                self.merge_regions = self.__class__.merge_regions(service, version, mode, path + ["merge_regions"])
                self.rename_region = self.__class__.rename_region(service, version, mode, path + ["rename_region"])
                super().__init__(service, version, mode, path)
            class add_objects_to_mesh_object(TUIMethod):
                """
                Add mesh and wrap objects to a mesh object.
                """
            class change_region_type(TUIMethod):
                """
                Change type of region.
                """
            class compute_regions(TUIMethod):
                """
                Recompute mesh object topo regions.
                """
            class create_mesh_object(TUIMethod):
                """
                Create mesh object from wrap objects.
                """
            class delete_region(TUIMethod):
                """
                Delete regions in the object.
                """
            class intersect(TUIMethod):
                """
                Intersect all face zones in mesh object.
                """
            class join(TUIMethod):
                """
                Join all face zones in mesh object.
                """
            class list_regions(TUIMethod):
                """
                List regions of mesh object.
                """
            class merge_regions(TUIMethod):
                """
                Merge regions in the object.
                """
            class rename_region(TUIMethod):
                """
                Rename a region in mesh object.
                """

            class controls(TUIMenu):
                """
                Build topology controls.
                """
                def __init__(self, service, version, mode, path):
                    self.remesh_post_intersection = self.__class__.remesh_post_intersection(service, version, mode, path + ["remesh_post_intersection"])
                    super().__init__(service, version, mode, path)
                class remesh_post_intersection(TUIMethod):
                    """
                    Remesh after intersection.
                    """

        class labels(TUIMenu):
            """
            Manage Face Zones Labels of an object.
            """
            def __init__(self, service, version, mode, path):
                self.cavity = self.__class__.cavity(service, version, mode, path + ["cavity"])
                self.add_zones = self.__class__.add_zones(service, version, mode, path + ["add_zones"])
                self.create = self.__class__.create(service, version, mode, path + ["create"])
                self.create_label_per_object = self.__class__.create_label_per_object(service, version, mode, path + ["create_label_per_object"])
                self.create_label_per_zone = self.__class__.create_label_per_zone(service, version, mode, path + ["create_label_per_zone"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.label_unlabeled_zones = self.__class__.label_unlabeled_zones(service, version, mode, path + ["label_unlabeled_zones"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.remove_all_labels_on_zones = self.__class__.remove_all_labels_on_zones(service, version, mode, path + ["remove_all_labels_on_zones"])
                self.remove_zones = self.__class__.remove_zones(service, version, mode, path + ["remove_zones"])
                self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
                super().__init__(service, version, mode, path)
            class add_zones(TUIMethod):
                """
                Add face zones to existing label.
                """
            class create(TUIMethod):
                """
                Create a new label with face zones.
                """
            class create_label_per_object(TUIMethod):
                """
                Create label per object.
                """
            class create_label_per_zone(TUIMethod):
                """
                Create a label for zone with it's name.
                """
            class delete(TUIMethod):
                """
                Delete labels of an object.
                """
            class label_unlabeled_zones(TUIMethod):
                """
                Label unlabeled zones.
                """
            class merge(TUIMethod):
                """
                Merge multiple labels of an object.
                """
            class remove_all_labels_on_zones(TUIMethod):
                """
                Clear all labels on selected zones.
                """
            class remove_zones(TUIMethod):
                """
                Remove face zones from existing label.
                """
            class rename(TUIMethod):
                """
                Rename an existing label of an object.
                """

            class cavity(TUIMenu):
                """
                Enter menu to create cavity using labels.
                """
                def __init__(self, service, version, mode, path):
                    self.add = self.__class__.add(service, version, mode, path + ["add"])
                    self.remove = self.__class__.remove(service, version, mode, path + ["remove"])
                    self.replace = self.__class__.replace(service, version, mode, path + ["replace"])
                    super().__init__(service, version, mode, path)
                class add(TUIMethod):
                    """
                    Create cavity by adding labels from another mesh object.
                    """
                class remove(TUIMethod):
                    """
                    Create cavity by removing labels.
                    """
                class replace(TUIMethod):
                    """
                    Create cavity by replacing labels from another mesh object.
                    """

        class remove_gaps(TUIMenu):
            """
            Enter the gap removal operation menu.
            """
            def __init__(self, service, version, mode, path):
                self.ignore_orientation = self.__class__.ignore_orientation(service, version, mode, path + ["ignore_orientation"])
                self.remove_gaps = self.__class__.remove_gaps(service, version, mode, path + ["remove_gaps"])
                self.show_gaps = self.__class__.show_gaps(service, version, mode, path + ["show_gaps"])
                super().__init__(service, version, mode, path)
            class ignore_orientation(TUIMethod):
                """
                Set if gaps should be identified considering orientation.
                """
            class remove_gaps(TUIMethod):
                """
                Remove gaps between objects or remove thickness in objects.
                """
            class show_gaps(TUIMethod):
                """
                Mark faces at gaps.
                """

        class set(TUIMenu):
            """
            Set object parameters.
            """
            def __init__(self, service, version, mode, path):
                self.set_edge_feature_angle = self.__class__.set_edge_feature_angle(service, version, mode, path + ["set_edge_feature_angle"])
                self.show_edge_zones = self.__class__.show_edge_zones(service, version, mode, path + ["show_edge_zones"])
                self.show_face_zones = self.__class__.show_face_zones(service, version, mode, path + ["show_face_zones"])
                super().__init__(service, version, mode, path)
            class set_edge_feature_angle(TUIMethod):
                """
                Set edge feature angle for edge extraction.
                """
            class show_edge_zones(TUIMethod):
                """
                Show object edges on display.
                """
            class show_face_zones(TUIMethod):
                """
                Show object faces on display.
                """

        class volumetric_regions(TUIMenu):
            """
            Manage volumetric regions of an object.
            """
            def __init__(self, service, version, mode, path):
                self.hexcore = self.__class__.hexcore(service, version, mode, path + ["hexcore"])
                self.scoped_prism = self.__class__.scoped_prism(service, version, mode, path + ["scoped_prism"])
                self.tet = self.__class__.tet(service, version, mode, path + ["tet"])
                self.auto_fill_volume = self.__class__.auto_fill_volume(service, version, mode, path + ["auto_fill_volume"])
                self.change_type = self.__class__.change_type(service, version, mode, path + ["change_type"])
                self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
                self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                self.delete_cells = self.__class__.delete_cells(service, version, mode, path + ["delete_cells"])
                self.fill_empty_volume = self.__class__.fill_empty_volume(service, version, mode, path + ["fill_empty_volume"])
                self.list = self.__class__.list(service, version, mode, path + ["list"])
                self.merge = self.__class__.merge(service, version, mode, path + ["merge"])
                self.merge_cells = self.__class__.merge_cells(service, version, mode, path + ["merge_cells"])
                self.rename = self.__class__.rename(service, version, mode, path + ["rename"])
                self.update = self.__class__.update(service, version, mode, path + ["update"])
                super().__init__(service, version, mode, path)
            class auto_fill_volume(TUIMethod):
                """
                Auto mesh selected regions.
                """
            class change_type(TUIMethod):
                """
                Change type of region.
                """
            class compute(TUIMethod):
                """
                Recompute mesh object topo regions using face zone labels.
                """
            class delete(TUIMethod):
                """
                Delete regions in the object.
                """
            class delete_cells(TUIMethod):
                """
                Delete all cell zones assocaited to selected regions.
                """
            class fill_empty_volume(TUIMethod):
                """
                Fill empty volume of selected regions.
                """
            class list(TUIMethod):
                """
                List regions of mesh object.
                """
            class merge(TUIMethod):
                """
                Merge regions in the object.
                """
            class merge_cells(TUIMethod):
                """
                Merge all cell zones assocaited to a region.
                """
            class rename(TUIMethod):
                """
                Rename a region in mesh object.
                """
            class update(TUIMethod):
                """
                Update mesh object topo regions.
                """

            class hexcore(TUIMenu):
                """
                Enter the hexcore menu.
                """
                def __init__(self, service, version, mode, path):
                    self.set = self.__class__.set(service, version, mode, path + ["set"])
                    self.generate = self.__class__.generate(service, version, mode, path + ["generate"])
                    super().__init__(service, version, mode, path)
                class generate(TUIMethod):
                    """
                    Fill empty volume of selected regions with hexcore.
                    """

                class set(TUIMenu):
                    """
                    Enter hexcore settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.outer_domain_params = self.__class__.outer_domain_params(service, version, mode, path + ["outer_domain_params"])
                        self.avoid_1_by_8_cell_jump_in_hexcore = self.__class__.avoid_1_by_8_cell_jump_in_hexcore(service, version, mode, path + ["avoid_1_by_8_cell_jump_in_hexcore"])
                        self.buffer_layers = self.__class__.buffer_layers(service, version, mode, path + ["buffer_layers"])
                        self.compute_max_cell_length = self.__class__.compute_max_cell_length(service, version, mode, path + ["compute_max_cell_length"])
                        self.define_hexcore_extents = self.__class__.define_hexcore_extents(service, version, mode, path + ["define_hexcore_extents"])
                        self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                        self.island_thresholds = self.__class__.island_thresholds(service, version, mode, path + ["island_thresholds"])
                        self.keep_hex_tet_separate = self.__class__.keep_hex_tet_separate(service, version, mode, path + ["keep_hex_tet_separate"])
                        self.maximum_cell_length = self.__class__.maximum_cell_length(service, version, mode, path + ["maximum_cell_length"])
                        self.maximum_initial_cells = self.__class__.maximum_initial_cells(service, version, mode, path + ["maximum_initial_cells"])
                        self.maximum_subdivisions = self.__class__.maximum_subdivisions(service, version, mode, path + ["maximum_subdivisions"])
                        self.merge_tets_to_pyramids = self.__class__.merge_tets_to_pyramids(service, version, mode, path + ["merge_tets_to_pyramids"])
                        self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                        self.octree_hexcore = self.__class__.octree_hexcore(service, version, mode, path + ["octree_hexcore"])
                        self.only_hexcore = self.__class__.only_hexcore(service, version, mode, path + ["only_hexcore"])
                        self.peel_layers = self.__class__.peel_layers(service, version, mode, path + ["peel_layers"])
                        self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                        self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                        self.skip_tet_refinement = self.__class__.skip_tet_refinement(service, version, mode, path + ["skip_tet_refinement"])
                        self.smooth_interface = self.__class__.smooth_interface(service, version, mode, path + ["smooth_interface"])
                        self.smooth_iterations = self.__class__.smooth_iterations(service, version, mode, path + ["smooth_iterations"])
                        self.smooth_relaxation = self.__class__.smooth_relaxation(service, version, mode, path + ["smooth_relaxation"])
                        super().__init__(service, version, mode, path)
                    class avoid_1_by_8_cell_jump_in_hexcore(TUIMethod):
                        """
                        Avoid-1:8-cell-jump-in-hexcore.
                        """
                    class buffer_layers(TUIMethod):
                        """
                        Number of addition cells to mark for subdivision.
                        """
                    class compute_max_cell_length(TUIMethod):
                        """
                        Compute maximum cell length.
                        """
                    class define_hexcore_extents(TUIMethod):
                        """
                        Enables sspecificaton of hexcore outer domain parameters.
                        """
                    class delete_dead_zones(TUIMethod):
                        """
                        Delete dead zones after hexcore creation.
                        """
                    class island_thresholds(TUIMethod):
                        """
                        Maximum number of cells and volume fraction in islands, deleted while separating the cells by region.
                        """
                    class keep_hex_tet_separate(TUIMethod):
                        """
                        Separate Hex and Tet cells.
                        """
                    class maximum_cell_length(TUIMethod):
                        """
                        Maximum cell length.
                        """
                    class maximum_initial_cells(TUIMethod):
                        """
                        Maximum number of initial Cartesian cells.
                        """
                    class maximum_subdivisions(TUIMethod):
                        """
                        Maximum number of subdivision sweeps.
                        """
                    class merge_tets_to_pyramids(TUIMethod):
                        """
                        Merge tets into pyramids.
                        """
                    class non_fluid_type(TUIMethod):
                        """
                        Set non fluid type for cell zones.
                        """
                    class octree_hexcore(TUIMethod):
                        """
                        Create hexcore using size-function driven octree.
                        """
                    class only_hexcore(TUIMethod):
                        """
                        Create hexcore and activate tet domain.
                        """
                    class peel_layers(TUIMethod):
                        """
                        Number of hexcore cells to peel back from boundary.
                        """
                    class print_region_based_sizing(TUIMethod):
                        """
                        Print region based sizings.
                        """
                    class set_region_based_sizing(TUIMethod):
                        """
                        Set region based sizings.
                        """
                    class skip_tet_refinement(TUIMethod):
                        """
                        Skip tethedral refinement in transition cell generation.
                        """
                    class smooth_interface(TUIMethod):
                        """
                        Enable smoothing of hexcore interface.
                        """
                    class smooth_iterations(TUIMethod):
                        """
                        Number of smoothing iterations on hexcore interface.
                        """
                    class smooth_relaxation(TUIMethod):
                        """
                        Smoothing under relaxation on hexcore interface.
                        """

                    class outer_domain_params(TUIMenu):
                        """
                        Define outer domain parameters.
                        """
                        def __init__(self, service, version, mode, path):
                            self.auto_align = self.__class__.auto_align(service, version, mode, path + ["auto_align"])
                            self.auto_align_boundaries = self.__class__.auto_align_boundaries(service, version, mode, path + ["auto_align_boundaries"])
                            self.auto_align_tolerance = self.__class__.auto_align_tolerance(service, version, mode, path + ["auto_align_tolerance"])
                            self.boundaries = self.__class__.boundaries(service, version, mode, path + ["boundaries"])
                            self.coordinates = self.__class__.coordinates(service, version, mode, path + ["coordinates"])
                            self.delete_old_face_zones = self.__class__.delete_old_face_zones(service, version, mode, path + ["delete_old_face_zones"])
                            self.list = self.__class__.list(service, version, mode, path + ["list"])
                            self.specify_boundaries = self.__class__.specify_boundaries(service, version, mode, path + ["specify_boundaries"])
                            self.specify_coordinates = self.__class__.specify_coordinates(service, version, mode, path + ["specify_coordinates"])
                            super().__init__(service, version, mode, path)
                        class auto_align(TUIMethod):
                            """
                            Enable auto-align?.
                            """
                        class auto_align_boundaries(TUIMethod):
                            """
                            Auto-align selected boundaries.
                            """
                        class auto_align_tolerance(TUIMethod):
                            """
                            Set auto-align-tolerance.
                            """
                        class boundaries(TUIMethod):
                            """
                            Set box-aligned zones which  have to be removed from hexcore meshing.
                            """
                        class coordinates(TUIMethod):
                            """
                            Secifiy coordinates of outer box.
                            """
                        class delete_old_face_zones(TUIMethod):
                            """
                            Delete replaced old tri face zones.
                            """
                        class list(TUIMethod):
                            """
                            List the face zones selected for hexcore up to boundaries.
                            """
                        class specify_boundaries(TUIMethod):
                            """
                            Set parameters to get hex mesh to boundary(s).
                            """
                        class specify_coordinates(TUIMethod):
                            """
                            Enables specification of coordinates of hexcore outer box.
                            """

            class scoped_prism(TUIMenu):
                """
                Enter the scoped prisms menu.
                """
                def __init__(self, service, version, mode, path):
                    self.set = self.__class__.set(service, version, mode, path + ["set"])
                    self.generate = self.__class__.generate(service, version, mode, path + ["generate"])
                    super().__init__(service, version, mode, path)
                class generate(TUIMethod):
                    """
                    Grow prism into selected region using scoped prism controls.
                    """

                class set(TUIMenu):
                    """
                    Enter scoped prism settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.create = self.__class__.create(service, version, mode, path + ["create"])
                        self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
                        self.growth_options = self.__class__.growth_options(service, version, mode, path + ["growth_options"])
                        self.list = self.__class__.list(service, version, mode, path + ["list"])
                        self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
                        self.poly_keep_nlayer_prism_characteristics = self.__class__.poly_keep_nlayer_prism_characteristics(service, version, mode, path + ["poly_keep_nlayer_prism_characteristics"])
                        self.read = self.__class__.read(service, version, mode, path + ["read"])
                        self.set_advanced_controls = self.__class__.set_advanced_controls(service, version, mode, path + ["set_advanced_controls"])
                        self.set_no_imprint_zones = self.__class__.set_no_imprint_zones(service, version, mode, path + ["set_no_imprint_zones"])
                        self.set_overset_prism_controls = self.__class__.set_overset_prism_controls(service, version, mode, path + ["set_overset_prism_controls"])
                        self.tet_prism_stairstep_exposed_quads = self.__class__.tet_prism_stairstep_exposed_quads(service, version, mode, path + ["tet_prism_stairstep_exposed_quads"])
                        self.write = self.__class__.write(service, version, mode, path + ["write"])
                        super().__init__(service, version, mode, path)
                    class create(TUIMethod):
                        """
                        Create new scoped prism.
                        """
                    class delete(TUIMethod):
                        """
                        Delete scoped prisms.
                        """
                    class growth_options(TUIMethod):
                        """
                        Set scoped prisms growth options.
                        """
                    class list(TUIMethod):
                        """
                        List all scoped prisms parameters.
                        """
                    class modify(TUIMethod):
                        """
                        Modify scoped prisms.
                        """
                    class poly_keep_nlayer_prism_characteristics(TUIMethod):
                        """
                        Number of layers to maintain poly-prism characteristics.
                        """
                    class read(TUIMethod):
                        """
                        Read scoped prisms from a file.
                        """
                    class set_advanced_controls(TUIMethod):
                        """
                        Set scoped boundary layer controls.
                        """
                    class set_no_imprint_zones(TUIMethod):
                        """
                        Set zones which should not be imprinted during prism generation.
                        """
                    class set_overset_prism_controls(TUIMethod):
                        """
                        Set boundary layer controls for overset mesh generation.
                        """
                    class tet_prism_stairstep_exposed_quads(TUIMethod):
                        """
                        Tet-Prism Stairstep exposed quad.
                        """
                    class write(TUIMethod):
                        """
                        Write scoped prisms to a file.
                        """

            class tet(TUIMenu):
                """
                Enter the tetrahedral menu.
                """
                def __init__(self, service, version, mode, path):
                    self.set = self.__class__.set(service, version, mode, path + ["set"])
                    self.generate = self.__class__.generate(service, version, mode, path + ["generate"])
                    super().__init__(service, version, mode, path)
                class generate(TUIMethod):
                    """
                    Fill empty volume of selected regions with tets.
                    """

                class set(TUIMenu):
                    """
                    Enter tet settings.
                    """
                    def __init__(self, service, version, mode, path):
                        self.adv_front_method = self.__class__.adv_front_method(service, version, mode, path + ["adv_front_method"])
                        self.advanced = self.__class__.advanced(service, version, mode, path + ["advanced"])
                        self.improve_mesh = self.__class__.improve_mesh(service, version, mode, path + ["improve_mesh"])
                        self.remove_slivers = self.__class__.remove_slivers(service, version, mode, path + ["remove_slivers"])
                        self.tet_improve = self.__class__.tet_improve(service, version, mode, path + ["tet_improve"])
                        self.cell_sizing = self.__class__.cell_sizing(service, version, mode, path + ["cell_sizing"])
                        self.clear_zone_growth_rate = self.__class__.clear_zone_growth_rate(service, version, mode, path + ["clear_zone_growth_rate"])
                        self.compute_max_cell_volume = self.__class__.compute_max_cell_volume(service, version, mode, path + ["compute_max_cell_volume"])
                        self.delete_dead_zones = self.__class__.delete_dead_zones(service, version, mode, path + ["delete_dead_zones"])
                        self.delete_unused_nodes = self.__class__.delete_unused_nodes(service, version, mode, path + ["delete_unused_nodes"])
                        self.improve_surface_mesh = self.__class__.improve_surface_mesh(service, version, mode, path + ["improve_surface_mesh"])
                        self.max_cell_length = self.__class__.max_cell_length(service, version, mode, path + ["max_cell_length"])
                        self.max_cell_volume = self.__class__.max_cell_volume(service, version, mode, path + ["max_cell_volume"])
                        self.merge_free_nodes = self.__class__.merge_free_nodes(service, version, mode, path + ["merge_free_nodes"])
                        self.non_fluid_type = self.__class__.non_fluid_type(service, version, mode, path + ["non_fluid_type"])
                        self.print_region_based_sizing = self.__class__.print_region_based_sizing(service, version, mode, path + ["print_region_based_sizing"])
                        self.refine_method = self.__class__.refine_method(service, version, mode, path + ["refine_method"])
                        self.set_region_based_sizing = self.__class__.set_region_based_sizing(service, version, mode, path + ["set_region_based_sizing"])
                        self.set_zone_growth_rate = self.__class__.set_zone_growth_rate(service, version, mode, path + ["set_zone_growth_rate"])
                        self.skewness_method = self.__class__.skewness_method(service, version, mode, path + ["skewness_method"])
                        self.use_max_cell_size = self.__class__.use_max_cell_size(service, version, mode, path + ["use_max_cell_size"])
                        super().__init__(service, version, mode, path)
                    class cell_sizing(TUIMethod):
                        """
                        Allow cell volume distribution to be determined based on boundary.
                        """
                    class clear_zone_growth_rate(TUIMethod):
                        """
                        Clear zone specific geometric growth rates.
                        """
                    class compute_max_cell_volume(TUIMethod):
                        """
                        Computes max cell size.
                        """
                    class delete_dead_zones(TUIMethod):
                        """
                        Automatically delete dead face and cell zones?.
                        """
                    class delete_unused_nodes(TUIMethod):
                        """
                        Automatically delete unused nodes?.
                        """
                    class improve_surface_mesh(TUIMethod):
                        """
                        Automatically improve surface mesh?.
                        """
                    class max_cell_length(TUIMethod):
                        """
                        Set max-cell-length.
                        """
                    class max_cell_volume(TUIMethod):
                        """
                        Set max-cell-volume.
                        """
                    class merge_free_nodes(TUIMethod):
                        """
                        Automatically merge duplicate nodes?.
                        """
                    class non_fluid_type(TUIMethod):
                        """
                        Select the default non-fluid cell zone type.
                        """
                    class print_region_based_sizing(TUIMethod):
                        """
                        Print region based sizings.
                        """
                    class refine_method(TUIMethod):
                        """
                        Define refinement method.
                        """
                    class set_region_based_sizing(TUIMethod):
                        """
                        Set region based sizings.
                        """
                    class set_zone_growth_rate(TUIMethod):
                        """
                        Set zone specific geometric growth rates.
                        """
                    class skewness_method(TUIMethod):
                        """
                        Skewness refinement controls.
                        """
                    class use_max_cell_size(TUIMethod):
                        """
                        Use max cell size for objects in auto-mesh and do not recompute it based on the object being meshed.
                        """

                    class adv_front_method(TUIMenu):
                        """
                        Advancing front refinement controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.skew_improve = self.__class__.skew_improve(service, version, mode, path + ["skew_improve"])
                            self.first_improve_params = self.__class__.first_improve_params(service, version, mode, path + ["first_improve_params"])
                            self.refine_parameters = self.__class__.refine_parameters(service, version, mode, path + ["refine_parameters"])
                            self.second_improve_params = self.__class__.second_improve_params(service, version, mode, path + ["second_improve_params"])
                            super().__init__(service, version, mode, path)
                        class first_improve_params(TUIMethod):
                            """
                            Define refine front improve parameters.
                            """
                        class refine_parameters(TUIMethod):
                            """
                            Define refine parameters.
                            """
                        class second_improve_params(TUIMethod):
                            """
                            Define cell zone improve parameters.
                            """

                        class skew_improve(TUIMenu):
                            """
                            Refine improve controls.
                            """
                            def __init__(self, service, version, mode, path):
                                self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                                self.boundary_sliver_skew = self.__class__.boundary_sliver_skew(service, version, mode, path + ["boundary_sliver_skew"])
                                self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                                self.sliver_skew = self.__class__.sliver_skew(service, version, mode, path + ["sliver_skew"])
                                self.target = self.__class__.target(service, version, mode, path + ["target"])
                                self.target_low_skew = self.__class__.target_low_skew(service, version, mode, path + ["target_low_skew"])
                                self.target_skew = self.__class__.target_skew(service, version, mode, path + ["target_skew"])
                                super().__init__(service, version, mode, path)
                            class attempts(TUIMethod):
                                """
                                Refine improve attempts.
                                """
                            class boundary_sliver_skew(TUIMethod):
                                """
                                Refine improve boundary sliver skew.
                                """
                            class iterations(TUIMethod):
                                """
                                Refine improve iterations.
                                """
                            class sliver_skew(TUIMethod):
                                """
                                Refine improve sliver skew.
                                """
                            class target(TUIMethod):
                                """
                                Activate target skew refinement.
                                """
                            class target_low_skew(TUIMethod):
                                """
                                Refine improve target low skew.
                                """
                            class target_skew(TUIMethod):
                                """
                                Refine improve target skew.
                                """

                    class advanced(TUIMenu):
                        """
                        Tet advanced controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.defaults = self.__class__.defaults(service, version, mode, path + ["defaults"])
                            self.freeze_boundary_cells = self.__class__.freeze_boundary_cells(service, version, mode, path + ["freeze_boundary_cells"])
                            self.keep_virtual_entities = self.__class__.keep_virtual_entities(service, version, mode, path + ["keep_virtual_entities"])
                            self.max_cells = self.__class__.max_cells(service, version, mode, path + ["max_cells"])
                            self.max_nodes = self.__class__.max_nodes(service, version, mode, path + ["max_nodes"])
                            self.node_tolerance = self.__class__.node_tolerance(service, version, mode, path + ["node_tolerance"])
                            self.progress_reports = self.__class__.progress_reports(service, version, mode, path + ["progress_reports"])
                            self.report_max_unmeshed = self.__class__.report_max_unmeshed(service, version, mode, path + ["report_max_unmeshed"])
                            self.report_unmeshed_faces = self.__class__.report_unmeshed_faces(service, version, mode, path + ["report_unmeshed_faces"])
                            self.report_unmeshed_nodes = self.__class__.report_unmeshed_nodes(service, version, mode, path + ["report_unmeshed_nodes"])
                            self.sliver_size = self.__class__.sliver_size(service, version, mode, path + ["sliver_size"])
                            super().__init__(service, version, mode, path)
                        class defaults(TUIMethod):
                            """
                            Calculate defaults.
                            """
                        class freeze_boundary_cells(TUIMethod):
                            """
                            Freeze boundary cells .
                            """
                        class keep_virtual_entities(TUIMethod):
                            """
                            Toggle deletion of virtual entities after intialization.
                            """
                        class max_cells(TUIMethod):
                            """
                            Set maximum number of cells in mesh.
                            """
                        class max_nodes(TUIMethod):
                            """
                            Set maximum number of nodes in mesh.
                            """
                        class node_tolerance(TUIMethod):
                            """
                            Set node-tolerance.
                            """
                        class progress_reports(TUIMethod):
                            """
                            Set time between progress reports in seconds.
                            """
                        class report_max_unmeshed(TUIMethod):
                            """
                            Max number of unmeshed entities reported.
                            """
                        class report_unmeshed_faces(TUIMethod):
                            """
                            Report unmeshed faces.
                            """
                        class report_unmeshed_nodes(TUIMethod):
                            """
                            Report unmeshed nodes.
                            """
                        class sliver_size(TUIMethod):
                            """
                            Set sliver-size.
                            """

                    class improve_mesh(TUIMenu):
                        """
                        Improve mesh controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.improve = self.__class__.improve(service, version, mode, path + ["improve"])
                            self.laplace_smooth = self.__class__.laplace_smooth(service, version, mode, path + ["laplace_smooth"])
                            self.skewness_smooth = self.__class__.skewness_smooth(service, version, mode, path + ["skewness_smooth"])
                            self.swap = self.__class__.swap(service, version, mode, path + ["swap"])
                            super().__init__(service, version, mode, path)
                        class improve(TUIMethod):
                            """
                            Automatically improve mesh.
                            """
                        class laplace_smooth(TUIMethod):
                            """
                            Laplace smooth parameters.
                            """
                        class skewness_smooth(TUIMethod):
                            """
                            Skewness smooth parametersx.
                            """
                        class swap(TUIMethod):
                            """
                            Face swap parameters.
                            """

                    class remove_slivers(TUIMenu):
                        """
                        Sliver remove controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                            self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                            self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                            self.low_skew = self.__class__.low_skew(service, version, mode, path + ["low_skew"])
                            self.method = self.__class__.method(service, version, mode, path + ["method"])
                            self.remove = self.__class__.remove(service, version, mode, path + ["remove"])
                            self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                            super().__init__(service, version, mode, path)
                        class angle(TUIMethod):
                            """
                            Max dihedral angle defining a valid boundary sliver.
                            """
                        class attempts(TUIMethod):
                            """
                            Sliver remove attempts.
                            """
                        class iterations(TUIMethod):
                            """
                            Sliver remove iterations.
                            """
                        class low_skew(TUIMethod):
                            """
                            Remove sliver low skew.
                            """
                        class method(TUIMethod):
                            """
                            Sliver remove method.
                            """
                        class remove(TUIMethod):
                            """
                            Automatically remove slivers.
                            """
                        class skew(TUIMethod):
                            """
                            Remove sliver skew.
                            """

                    class tet_improve(TUIMenu):
                        """
                        Improve cells controls.
                        """
                        def __init__(self, service, version, mode, path):
                            self.angle = self.__class__.angle(service, version, mode, path + ["angle"])
                            self.attempts = self.__class__.attempts(service, version, mode, path + ["attempts"])
                            self.iterations = self.__class__.iterations(service, version, mode, path + ["iterations"])
                            self.skew = self.__class__.skew(service, version, mode, path + ["skew"])
                            super().__init__(service, version, mode, path)
                        class angle(TUIMethod):
                            """
                            Max dihedral angle defining a valid boundary cell.
                            """
                        class attempts(TUIMethod):
                            """
                            Improve attempts.
                            """
                        class iterations(TUIMethod):
                            """
                            Improve iterations.
                            """
                        class skew(TUIMethod):
                            """
                            Remove skew.
                            """

        class wrap(TUIMenu):
            """
            Enter the wrapping operation menu.
            """
            def __init__(self, service, version, mode, path):
                self.set = self.__class__.set(service, version, mode, path + ["set"])
                self.check_holes = self.__class__.check_holes(service, version, mode, path + ["check_holes"])
                self.debug = self.__class__.debug(service, version, mode, path + ["debug"])
                self.object_zone_separate = self.__class__.object_zone_separate(service, version, mode, path + ["object_zone_separate"])
                self.wrap = self.__class__.wrap(service, version, mode, path + ["wrap"])
                super().__init__(service, version, mode, path)
            class check_holes(TUIMethod):
                """
                Check for holes on wrapped objects.
                """
            class debug(TUIMethod):
                """
                Debug from intermediate objects.
                """
            class object_zone_separate(TUIMethod):
                """
                Separate Object Face Zones.
                """
            class wrap(TUIMethod):
                """
                Wrap the object.
                """

            class set(TUIMenu):
                """
                Set wrap options.
                """
                def __init__(self, service, version, mode, path):
                    self.add_geometry_recovery_level_to_zones = self.__class__.add_geometry_recovery_level_to_zones(service, version, mode, path + ["add_geometry_recovery_level_to_zones"])
                    self.delete_far_edges = self.__class__.delete_far_edges(service, version, mode, path + ["delete_far_edges"])
                    self.include_thin_cut_edges_and_faces = self.__class__.include_thin_cut_edges_and_faces(service, version, mode, path + ["include_thin_cut_edges_and_faces"])
                    self.list_zones_geometry_recovery_levels = self.__class__.list_zones_geometry_recovery_levels(service, version, mode, path + ["list_zones_geometry_recovery_levels"])
                    self.max_free_edges_for_hole_patching = self.__class__.max_free_edges_for_hole_patching(service, version, mode, path + ["max_free_edges_for_hole_patching"])
                    self.minimum_relative_topo_area = self.__class__.minimum_relative_topo_area(service, version, mode, path + ["minimum_relative_topo_area"])
                    self.minimum_relative_topo_count = self.__class__.minimum_relative_topo_count(service, version, mode, path + ["minimum_relative_topo_count"])
                    self.minimum_topo_area = self.__class__.minimum_topo_area(service, version, mode, path + ["minimum_topo_area"])
                    self.minimum_topo_count = self.__class__.minimum_topo_count(service, version, mode, path + ["minimum_topo_count"])
                    self.relative_feature_tolerance = self.__class__.relative_feature_tolerance(service, version, mode, path + ["relative_feature_tolerance"])
                    self.report_holes = self.__class__.report_holes(service, version, mode, path + ["report_holes"])
                    self.resolution_factor = self.__class__.resolution_factor(service, version, mode, path + ["resolution_factor"])
                    self.shrink_wrap_rezone_parameters = self.__class__.shrink_wrap_rezone_parameters(service, version, mode, path + ["shrink_wrap_rezone_parameters"])
                    self.use_ray_tracing = self.__class__.use_ray_tracing(service, version, mode, path + ["use_ray_tracing"])
                    self.use_smooth_folded_faces = self.__class__.use_smooth_folded_faces(service, version, mode, path + ["use_smooth_folded_faces"])
                    self.zone_name_prefix = self.__class__.zone_name_prefix(service, version, mode, path + ["zone_name_prefix"])
                    super().__init__(service, version, mode, path)
                class add_geometry_recovery_level_to_zones(TUIMethod):
                    """
                    Update zones with geometry recovery level attributes.
                    """
                class delete_far_edges(TUIMethod):
                    """
                    Delete-far-edges-after-wrap.
                    """
                class include_thin_cut_edges_and_faces(TUIMethod):
                    """
                    Include thin cut Face zones and Edge zones.
                    """
                class list_zones_geometry_recovery_levels(TUIMethod):
                    """
                    List zones with medium and high geometry recovery levels.
                    """
                class max_free_edges_for_hole_patching(TUIMethod):
                    """
                    Maximum length of free edge loop for filling holes.
                    """
                class minimum_relative_topo_area(TUIMethod):
                    """
                    Minimum Relative Topo Area.
                    """
                class minimum_relative_topo_count(TUIMethod):
                    """
                    Minimum Relative Topo Face Count.
                    """
                class minimum_topo_area(TUIMethod):
                    """
                    Minimum Topo Area.
                    """
                class minimum_topo_count(TUIMethod):
                    """
                    Minimum Topo Face Count.
                    """
                class relative_feature_tolerance(TUIMethod):
                    """
                    Relative Feature Tolerance.
                    """
                class report_holes(TUIMethod):
                    """
                    Detect holes in wrapped objects.
                    """
                class resolution_factor(TUIMethod):
                    """
                    Resolution Factor.
                    """
                class shrink_wrap_rezone_parameters(TUIMethod):
                    """
                    Set wrapper rezone parameters.
                    """
                class use_ray_tracing(TUIMethod):
                    """
                    Use ray tracing.
                    """
                class use_smooth_folded_faces(TUIMethod):
                    """
                    Use smooth folded faces.
                    """
                class zone_name_prefix(TUIMethod):
                    """
                    Prefix to be used for names of wrap face zones created.
                    """

    class openmp_controls(TUIMenu):
        """
        Enter the openmp menu.
        """
        def __init__(self, service, version, mode, path):
            self.get_active_cores = self.__class__.get_active_cores(service, version, mode, path + ["get_active_cores"])
            self.get_max_cores = self.__class__.get_max_cores(service, version, mode, path + ["get_max_cores"])
            self.set_num_cores = self.__class__.set_num_cores(service, version, mode, path + ["set_num_cores"])
            super().__init__(service, version, mode, path)
        class get_active_cores(TUIMethod):
            """
            Number of Active Cores.
            """
        class get_max_cores(TUIMethod):
            """
            Max Number of Cores.
            """
        class set_num_cores(TUIMethod):
            """
            Enter Number of Cores.
            """

    class parallel(TUIMenu):
        """
        Enter the parallel menu.
        """
        def __init__(self, service, version, mode, path):
            self.agglomerate = self.__class__.agglomerate(service, version, mode, path + ["agglomerate"])
            self.auto_partition = self.__class__.auto_partition(service, version, mode, path + ["auto_partition"])
            self.print_partition_info = self.__class__.print_partition_info(service, version, mode, path + ["print_partition_info"])
            self.spawn_solver_processes = self.__class__.spawn_solver_processes(service, version, mode, path + ["spawn_solver_processes"])
            self.thread_number_control = self.__class__.thread_number_control(service, version, mode, path + ["thread_number_control"])
            super().__init__(service, version, mode, path)
        class agglomerate(TUIMethod):
            """
            Agglomerate mesh into compute node 0.
            """
        class auto_partition(TUIMethod):
            """
            Auto Partition Prism Base Zones?.
            """
        class print_partition_info(TUIMethod):
            """
            Prints Partition Info to console.
            """
        class spawn_solver_processes(TUIMethod):
            """
            Spawn additional solver processes.
            """
        class thread_number_control(TUIMethod):
            """
            Thread number control.
            """

    class preferences(TUIMenu):
        """
        Set preferences.
        """
        def __init__(self, service, version, mode, path):
            self.ansys_cloud_burst = self.__class__.ansys_cloud_burst(service, version, mode, path + ["ansys_cloud_burst"])
            self.appearance = self.__class__.appearance(service, version, mode, path + ["appearance"])
            self.general = self.__class__.general(service, version, mode, path + ["general"])
            self.gpuapp = self.__class__.gpuapp(service, version, mode, path + ["gpuapp"])
            self.graphics = self.__class__.graphics(service, version, mode, path + ["graphics"])
            self.mat_pro_app = self.__class__.mat_pro_app(service, version, mode, path + ["mat_pro_app"])
            self.meshing_workflow = self.__class__.meshing_workflow(service, version, mode, path + ["meshing_workflow"])
            self.navigation = self.__class__.navigation(service, version, mode, path + ["navigation"])
            self.parametric_study = self.__class__.parametric_study(service, version, mode, path + ["parametric_study"])
            self.prj_app = self.__class__.prj_app(service, version, mode, path + ["prj_app"])
            self.python_console = self.__class__.python_console(service, version, mode, path + ["python_console"])
            self.simulation = self.__class__.simulation(service, version, mode, path + ["simulation"])
            self.turbo_setup = self.__class__.turbo_setup(service, version, mode, path + ["turbo_setup"])
            self.turbo_workflow = self.__class__.turbo_workflow(service, version, mode, path + ["turbo_workflow"])
            super().__init__(service, version, mode, path)

        class ansys_cloud_burst(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.authentication_method = self.__class__.authentication_method(service, version, mode, path + ["authentication_method"])
                super().__init__(service, version, mode, path)
            class authentication_method(TUIMethod):
                """
                No help available.
                """

        class appearance(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.ansys_logo = self.__class__.ansys_logo(service, version, mode, path + ["ansys_logo"])
                self.charts = self.__class__.charts(service, version, mode, path + ["charts"])
                self.selections = self.__class__.selections(service, version, mode, path + ["selections"])
                self.allow_interface_bounds_flags = self.__class__.allow_interface_bounds_flags(service, version, mode, path + ["allow_interface_bounds_flags"])
                self.application_font_size = self.__class__.application_font_size(service, version, mode, path + ["application_font_size"])
                self.axis_triad = self.__class__.axis_triad(service, version, mode, path + ["axis_triad"])
                self.color_theme = self.__class__.color_theme(service, version, mode, path + ["color_theme"])
                self.completer = self.__class__.completer(service, version, mode, path + ["completer"])
                self.custom_title_bar = self.__class__.custom_title_bar(service, version, mode, path + ["custom_title_bar"])
                self.default_view = self.__class__.default_view(service, version, mode, path + ["default_view"])
                self.graphics_background_color1 = self.__class__.graphics_background_color1(service, version, mode, path + ["graphics_background_color1"])
                self.graphics_background_color2 = self.__class__.graphics_background_color2(service, version, mode, path + ["graphics_background_color2"])
                self.graphics_background_style = self.__class__.graphics_background_style(service, version, mode, path + ["graphics_background_style"])
                self.graphics_color_theme = self.__class__.graphics_color_theme(service, version, mode, path + ["graphics_color_theme"])
                self.graphics_default_manual_face_color = self.__class__.graphics_default_manual_face_color(service, version, mode, path + ["graphics_default_manual_face_color"])
                self.graphics_default_manual_node_color = self.__class__.graphics_default_manual_node_color(service, version, mode, path + ["graphics_default_manual_node_color"])
                self.graphics_edge_color = self.__class__.graphics_edge_color(service, version, mode, path + ["graphics_edge_color"])
                self.graphics_foreground_color = self.__class__.graphics_foreground_color(service, version, mode, path + ["graphics_foreground_color"])
                self.graphics_partition_boundary_color = self.__class__.graphics_partition_boundary_color(service, version, mode, path + ["graphics_partition_boundary_color"])
                self.graphics_surface_color = self.__class__.graphics_surface_color(service, version, mode, path + ["graphics_surface_color"])
                self.graphics_title_window_framecolor = self.__class__.graphics_title_window_framecolor(service, version, mode, path + ["graphics_title_window_framecolor"])
                self.graphics_view = self.__class__.graphics_view(service, version, mode, path + ["graphics_view"])
                self.graphics_wall_face_color = self.__class__.graphics_wall_face_color(service, version, mode, path + ["graphics_wall_face_color"])
                self.group_by_tree_view = self.__class__.group_by_tree_view(service, version, mode, path + ["group_by_tree_view"])
                self.group_physics_by_tree_view = self.__class__.group_physics_by_tree_view(service, version, mode, path + ["group_physics_by_tree_view"])
                self.model_color_scheme = self.__class__.model_color_scheme(service, version, mode, path + ["model_color_scheme"])
                self.number_of_files_recently_used = self.__class__.number_of_files_recently_used(service, version, mode, path + ["number_of_files_recently_used"])
                self.number_of_pastel_colors = self.__class__.number_of_pastel_colors(service, version, mode, path + ["number_of_pastel_colors"])
                self.pastel_color_saturation = self.__class__.pastel_color_saturation(service, version, mode, path + ["pastel_color_saturation"])
                self.pastel_color_value = self.__class__.pastel_color_value(service, version, mode, path + ["pastel_color_value"])
                self.py_console_completer = self.__class__.py_console_completer(service, version, mode, path + ["py_console_completer"])
                self.quick_property_view = self.__class__.quick_property_view(service, version, mode, path + ["quick_property_view"])
                self.ruler = self.__class__.ruler(service, version, mode, path + ["ruler"])
                self.show_default_interior = self.__class__.show_default_interior(service, version, mode, path + ["show_default_interior"])
                self.show_enabled_models = self.__class__.show_enabled_models(service, version, mode, path + ["show_enabled_models"])
                self.show_interface_non_overlapping_boundaries = self.__class__.show_interface_non_overlapping_boundaries(service, version, mode, path + ["show_interface_non_overlapping_boundaries"])
                self.show_model_edges = self.__class__.show_model_edges(service, version, mode, path + ["show_model_edges"])
                self.solution_mode_edge_color_in_meshing_mode = self.__class__.solution_mode_edge_color_in_meshing_mode(service, version, mode, path + ["solution_mode_edge_color_in_meshing_mode"])
                self.surface_emissivity = self.__class__.surface_emissivity(service, version, mode, path + ["surface_emissivity"])
                self.surface_specularity = self.__class__.surface_specularity(service, version, mode, path + ["surface_specularity"])
                self.surface_specularity_for_contours = self.__class__.surface_specularity_for_contours(service, version, mode, path + ["surface_specularity_for_contours"])
                self.titles = self.__class__.titles(service, version, mode, path + ["titles"])
                self.titles_border_offset = self.__class__.titles_border_offset(service, version, mode, path + ["titles_border_offset"])
                super().__init__(service, version, mode, path)
            class allow_interface_bounds_flags(TUIMethod):
                """
                No help available.
                """
            class application_font_size(TUIMethod):
                """
                No help available.
                """
            class axis_triad(TUIMethod):
                """
                No help available.
                """
            class color_theme(TUIMethod):
                """
                No help available.
                """
            class completer(TUIMethod):
                """
                No help available.
                """
            class custom_title_bar(TUIMethod):
                """
                No help available.
                """
            class default_view(TUIMethod):
                """
                No help available.
                """
            class graphics_background_color1(TUIMethod):
                """
                No help available.
                """
            class graphics_background_color2(TUIMethod):
                """
                No help available.
                """
            class graphics_background_style(TUIMethod):
                """
                No help available.
                """
            class graphics_color_theme(TUIMethod):
                """
                No help available.
                """
            class graphics_default_manual_face_color(TUIMethod):
                """
                No help available.
                """
            class graphics_default_manual_node_color(TUIMethod):
                """
                No help available.
                """
            class graphics_edge_color(TUIMethod):
                """
                No help available.
                """
            class graphics_foreground_color(TUIMethod):
                """
                No help available.
                """
            class graphics_partition_boundary_color(TUIMethod):
                """
                No help available.
                """
            class graphics_surface_color(TUIMethod):
                """
                No help available.
                """
            class graphics_title_window_framecolor(TUIMethod):
                """
                No help available.
                """
            class graphics_view(TUIMethod):
                """
                No help available.
                """
            class graphics_wall_face_color(TUIMethod):
                """
                No help available.
                """
            class group_by_tree_view(TUIMethod):
                """
                No help available.
                """
            class group_physics_by_tree_view(TUIMethod):
                """
                No help available.
                """
            class model_color_scheme(TUIMethod):
                """
                No help available.
                """
            class number_of_files_recently_used(TUIMethod):
                """
                No help available.
                """
            class number_of_pastel_colors(TUIMethod):
                """
                No help available.
                """
            class pastel_color_saturation(TUIMethod):
                """
                No help available.
                """
            class pastel_color_value(TUIMethod):
                """
                No help available.
                """
            class py_console_completer(TUIMethod):
                """
                No help available.
                """
            class quick_property_view(TUIMethod):
                """
                No help available.
                """
            class ruler(TUIMethod):
                """
                No help available.
                """
            class show_default_interior(TUIMethod):
                """
                No help available.
                """
            class show_enabled_models(TUIMethod):
                """
                No help available.
                """
            class show_interface_non_overlapping_boundaries(TUIMethod):
                """
                No help available.
                """
            class show_model_edges(TUIMethod):
                """
                No help available.
                """
            class solution_mode_edge_color_in_meshing_mode(TUIMethod):
                """
                No help available.
                """
            class surface_emissivity(TUIMethod):
                """
                No help available.
                """
            class surface_specularity(TUIMethod):
                """
                No help available.
                """
            class surface_specularity_for_contours(TUIMethod):
                """
                No help available.
                """
            class titles(TUIMethod):
                """
                No help available.
                """
            class titles_border_offset(TUIMethod):
                """
                No help available.
                """

            class ansys_logo(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.color = self.__class__.color(service, version, mode, path + ["color"])
                    self.visible = self.__class__.visible(service, version, mode, path + ["visible"])
                    super().__init__(service, version, mode, path)
                class color(TUIMethod):
                    """
                    No help available.
                    """
                class visible(TUIMethod):
                    """
                    No help available.
                    """

            class charts(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.font = self.__class__.font(service, version, mode, path + ["font"])
                    self.text_color = self.__class__.text_color(service, version, mode, path + ["text_color"])
                    self.curve_colors = self.__class__.curve_colors(service, version, mode, path + ["curve_colors"])
                    self.enable_open_glfor_modern_plots = self.__class__.enable_open_glfor_modern_plots(service, version, mode, path + ["enable_open_glfor_modern_plots"])
                    self.legend_alignment = self.__class__.legend_alignment(service, version, mode, path + ["legend_alignment"])
                    self.legend_visibility = self.__class__.legend_visibility(service, version, mode, path + ["legend_visibility"])
                    self.modern_plots_enabled = self.__class__.modern_plots_enabled(service, version, mode, path + ["modern_plots_enabled"])
                    self.modern_plots_points_threshold = self.__class__.modern_plots_points_threshold(service, version, mode, path + ["modern_plots_points_threshold"])
                    self.plots_behavior = self.__class__.plots_behavior(service, version, mode, path + ["plots_behavior"])
                    self.print_plot_data = self.__class__.print_plot_data(service, version, mode, path + ["print_plot_data"])
                    self.print_residuals_data = self.__class__.print_residuals_data(service, version, mode, path + ["print_residuals_data"])
                    self.threshold = self.__class__.threshold(service, version, mode, path + ["threshold"])
                    self.tooltip_interpolation = self.__class__.tooltip_interpolation(service, version, mode, path + ["tooltip_interpolation"])
                    super().__init__(service, version, mode, path)
                class curve_colors(TUIMethod):
                    """
                    No help available.
                    """
                class enable_open_glfor_modern_plots(TUIMethod):
                    """
                    No help available.
                    """
                class legend_alignment(TUIMethod):
                    """
                    No help available.
                    """
                class legend_visibility(TUIMethod):
                    """
                    No help available.
                    """
                class modern_plots_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class modern_plots_points_threshold(TUIMethod):
                    """
                    No help available.
                    """
                class plots_behavior(TUIMethod):
                    """
                    No help available.
                    """
                class print_plot_data(TUIMethod):
                    """
                    No help available.
                    """
                class print_residuals_data(TUIMethod):
                    """
                    No help available.
                    """
                class threshold(TUIMethod):
                    """
                    No help available.
                    """
                class tooltip_interpolation(TUIMethod):
                    """
                    No help available.
                    """

                class font(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.axes = self.__class__.axes(service, version, mode, path + ["axes"])
                        self.axes_titles = self.__class__.axes_titles(service, version, mode, path + ["axes_titles"])
                        self.legend = self.__class__.legend(service, version, mode, path + ["legend"])
                        self.title = self.__class__.title(service, version, mode, path + ["title"])
                        super().__init__(service, version, mode, path)
                    class axes(TUIMethod):
                        """
                        No help available.
                        """
                    class axes_titles(TUIMethod):
                        """
                        No help available.
                        """
                    class legend(TUIMethod):
                        """
                        No help available.
                        """
                    class title(TUIMethod):
                        """
                        No help available.
                        """

                class text_color(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.axes = self.__class__.axes(service, version, mode, path + ["axes"])
                        self.axes_titles = self.__class__.axes_titles(service, version, mode, path + ["axes_titles"])
                        self.legend = self.__class__.legend(service, version, mode, path + ["legend"])
                        self.title = self.__class__.title(service, version, mode, path + ["title"])
                        super().__init__(service, version, mode, path)
                    class axes(TUIMethod):
                        """
                        No help available.
                        """
                    class axes_titles(TUIMethod):
                        """
                        No help available.
                        """
                    class legend(TUIMethod):
                        """
                        No help available.
                        """
                    class title(TUIMethod):
                        """
                        No help available.
                        """

            class selections(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.enable_highlight_edge_transparency = self.__class__.enable_highlight_edge_transparency(service, version, mode, path + ["enable_highlight_edge_transparency"])
                    self.general_displacement = self.__class__.general_displacement(service, version, mode, path + ["general_displacement"])
                    self.highlight_edge_color = self.__class__.highlight_edge_color(service, version, mode, path + ["highlight_edge_color"])
                    self.highlight_edge_weight = self.__class__.highlight_edge_weight(service, version, mode, path + ["highlight_edge_weight"])
                    self.highlight_face_color = self.__class__.highlight_face_color(service, version, mode, path + ["highlight_face_color"])
                    self.highlight_gloss = self.__class__.highlight_gloss(service, version, mode, path + ["highlight_gloss"])
                    self.highlight_specular_component = self.__class__.highlight_specular_component(service, version, mode, path + ["highlight_specular_component"])
                    self.highlight_transparency = self.__class__.highlight_transparency(service, version, mode, path + ["highlight_transparency"])
                    self.mouse_hover_probe_values_enabled = self.__class__.mouse_hover_probe_values_enabled(service, version, mode, path + ["mouse_hover_probe_values_enabled"])
                    self.mouse_over_highlight_enabled = self.__class__.mouse_over_highlight_enabled(service, version, mode, path + ["mouse_over_highlight_enabled"])
                    self.probe_tooltip_hide_delay_timer = self.__class__.probe_tooltip_hide_delay_timer(service, version, mode, path + ["probe_tooltip_hide_delay_timer"])
                    self.probe_tooltip_show_delay_timer = self.__class__.probe_tooltip_show_delay_timer(service, version, mode, path + ["probe_tooltip_show_delay_timer"])
                    super().__init__(service, version, mode, path)
                class enable_highlight_edge_transparency(TUIMethod):
                    """
                    No help available.
                    """
                class general_displacement(TUIMethod):
                    """
                    No help available.
                    """
                class highlight_edge_color(TUIMethod):
                    """
                    No help available.
                    """
                class highlight_edge_weight(TUIMethod):
                    """
                    No help available.
                    """
                class highlight_face_color(TUIMethod):
                    """
                    No help available.
                    """
                class highlight_gloss(TUIMethod):
                    """
                    No help available.
                    """
                class highlight_specular_component(TUIMethod):
                    """
                    No help available.
                    """
                class highlight_transparency(TUIMethod):
                    """
                    No help available.
                    """
                class mouse_hover_probe_values_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class mouse_over_highlight_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class probe_tooltip_hide_delay_timer(TUIMethod):
                    """
                    No help available.
                    """
                class probe_tooltip_show_delay_timer(TUIMethod):
                    """
                    No help available.
                    """

        class general(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.startup_messages = self.__class__.startup_messages(service, version, mode, path + ["startup_messages"])
                self.advanced_partition = self.__class__.advanced_partition(service, version, mode, path + ["advanced_partition"])
                self.automatic_transcript = self.__class__.automatic_transcript(service, version, mode, path + ["automatic_transcript"])
                self.default_ioformat = self.__class__.default_ioformat(service, version, mode, path + ["default_ioformat"])
                self.dock_editor = self.__class__.dock_editor(service, version, mode, path + ["dock_editor"])
                self.flow_model = self.__class__.flow_model(service, version, mode, path + ["flow_model"])
                self.idle_timeout = self.__class__.idle_timeout(service, version, mode, path + ["idle_timeout"])
                self.import_physics_volume_definitions = self.__class__.import_physics_volume_definitions(service, version, mode, path + ["import_physics_volume_definitions"])
                self.initial_physics_volume_definitions = self.__class__.initial_physics_volume_definitions(service, version, mode, path + ["initial_physics_volume_definitions"])
                self.skip_creation_of_groups_pointing_to_single_entity = self.__class__.skip_creation_of_groups_pointing_to_single_entity(service, version, mode, path + ["skip_creation_of_groups_pointing_to_single_entity"])
                self.utlcreate_default_object_if_possible = self.__class__.utlcreate_default_object_if_possible(service, version, mode, path + ["utlcreate_default_object_if_possible"])
                self.utlmode = self.__class__.utlmode(service, version, mode, path + ["utlmode"])
                super().__init__(service, version, mode, path)
            class advanced_partition(TUIMethod):
                """
                No help available.
                """
            class automatic_transcript(TUIMethod):
                """
                No help available.
                """
            class default_ioformat(TUIMethod):
                """
                No help available.
                """
            class dock_editor(TUIMethod):
                """
                No help available.
                """
            class flow_model(TUIMethod):
                """
                No help available.
                """
            class idle_timeout(TUIMethod):
                """
                No help available.
                """
            class import_physics_volume_definitions(TUIMethod):
                """
                No help available.
                """
            class initial_physics_volume_definitions(TUIMethod):
                """
                No help available.
                """
            class skip_creation_of_groups_pointing_to_single_entity(TUIMethod):
                """
                No help available.
                """
            class utlcreate_default_object_if_possible(TUIMethod):
                """
                No help available.
                """
            class utlmode(TUIMethod):
                """
                No help available.
                """

            class startup_messages(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.color_theme_change_message = self.__class__.color_theme_change_message(service, version, mode, path + ["color_theme_change_message"])
                    self.key_behavioral_changes_message = self.__class__.key_behavioral_changes_message(service, version, mode, path + ["key_behavioral_changes_message"])
                    self.qaservice_message = self.__class__.qaservice_message(service, version, mode, path + ["qaservice_message"])
                    super().__init__(service, version, mode, path)
                class color_theme_change_message(TUIMethod):
                    """
                    No help available.
                    """
                class key_behavioral_changes_message(TUIMethod):
                    """
                    No help available.
                    """
                class qaservice_message(TUIMethod):
                    """
                    No help available.
                    """

        class gpuapp(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.alpha_features = self.__class__.alpha_features(service, version, mode, path + ["alpha_features"])
                super().__init__(service, version, mode, path)
            class alpha_features(TUIMethod):
                """
                No help available.
                """

        class graphics(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.boundary_markers = self.__class__.boundary_markers(service, version, mode, path + ["boundary_markers"])
                self.colormap_settings = self.__class__.colormap_settings(service, version, mode, path + ["colormap_settings"])
                self.display_lists = self.__class__.display_lists(service, version, mode, path + ["display_lists"])
                self.embedded_windows = self.__class__.embedded_windows(service, version, mode, path + ["embedded_windows"])
                self.export_video_settings = self.__class__.export_video_settings(service, version, mode, path + ["export_video_settings"])
                self.graphics_effects = self.__class__.graphics_effects(service, version, mode, path + ["graphics_effects"])
                self.hardcopy_settings = self.__class__.hardcopy_settings(service, version, mode, path + ["hardcopy_settings"])
                self.lighting = self.__class__.lighting(service, version, mode, path + ["lighting"])
                self.manage_hoops_memory = self.__class__.manage_hoops_memory(service, version, mode, path + ["manage_hoops_memory"])
                self.material_effects = self.__class__.material_effects(service, version, mode, path + ["material_effects"])
                self.meshing_mode = self.__class__.meshing_mode(service, version, mode, path + ["meshing_mode"])
                self.performance = self.__class__.performance(service, version, mode, path + ["performance"])
                self.ray_tracing_options = self.__class__.ray_tracing_options(service, version, mode, path + ["ray_tracing_options"])
                self.transparency = self.__class__.transparency(service, version, mode, path + ["transparency"])
                self.vector_settings = self.__class__.vector_settings(service, version, mode, path + ["vector_settings"])
                self.animation_option = self.__class__.animation_option(service, version, mode, path + ["animation_option"])
                self.backface_cull = self.__class__.backface_cull(service, version, mode, path + ["backface_cull"])
                self.camera_near_limit = self.__class__.camera_near_limit(service, version, mode, path + ["camera_near_limit"])
                self.double_buffering = self.__class__.double_buffering(service, version, mode, path + ["double_buffering"])
                self.enable_camera_near_limit_to_avoid_zfighting = self.__class__.enable_camera_near_limit_to_avoid_zfighting(service, version, mode, path + ["enable_camera_near_limit_to_avoid_zfighting"])
                self.enable_non_object_based_workflow = self.__class__.enable_non_object_based_workflow(service, version, mode, path + ["enable_non_object_based_workflow"])
                self.event_poll_interval = self.__class__.event_poll_interval(service, version, mode, path + ["event_poll_interval"])
                self.event_poll_timeout = self.__class__.event_poll_timeout(service, version, mode, path + ["event_poll_timeout"])
                self.force_key_frame_animation_markers_to_off = self.__class__.force_key_frame_animation_markers_to_off(service, version, mode, path + ["force_key_frame_animation_markers_to_off"])
                self.graphics_window_line_width = self.__class__.graphics_window_line_width(service, version, mode, path + ["graphics_window_line_width"])
                self.graphics_window_point_symbol = self.__class__.graphics_window_point_symbol(service, version, mode, path + ["graphics_window_point_symbol"])
                self.hidden_surface_removal_method = self.__class__.hidden_surface_removal_method(service, version, mode, path + ["hidden_surface_removal_method"])
                self.higher_resolution_graphics_window_line_width = self.__class__.higher_resolution_graphics_window_line_width(service, version, mode, path + ["higher_resolution_graphics_window_line_width"])
                self.lower_resolution_graphics_window_line_width = self.__class__.lower_resolution_graphics_window_line_width(service, version, mode, path + ["lower_resolution_graphics_window_line_width"])
                self.marker_drawing_mode = self.__class__.marker_drawing_mode(service, version, mode, path + ["marker_drawing_mode"])
                self.max_graphics_text_size = self.__class__.max_graphics_text_size(service, version, mode, path + ["max_graphics_text_size"])
                self.min_graphics_text_size = self.__class__.min_graphics_text_size(service, version, mode, path + ["min_graphics_text_size"])
                self.plot_legend_margin = self.__class__.plot_legend_margin(service, version, mode, path + ["plot_legend_margin"])
                self.point_tool_size = self.__class__.point_tool_size(service, version, mode, path + ["point_tool_size"])
                self.remove_partition_lines = self.__class__.remove_partition_lines(service, version, mode, path + ["remove_partition_lines"])
                self.remove_partition_lines_tolerance = self.__class__.remove_partition_lines_tolerance(service, version, mode, path + ["remove_partition_lines_tolerance"])
                self.rotation_centerpoint_visible = self.__class__.rotation_centerpoint_visible(service, version, mode, path + ["rotation_centerpoint_visible"])
                self.scroll_wheel_event_end_timer = self.__class__.scroll_wheel_event_end_timer(service, version, mode, path + ["scroll_wheel_event_end_timer"])
                self.selection_highlight_window = self.__class__.selection_highlight_window(service, version, mode, path + ["selection_highlight_window"])
                self.set_camera_normal_to_surface_increments = self.__class__.set_camera_normal_to_surface_increments(service, version, mode, path + ["set_camera_normal_to_surface_increments"])
                self.show_hidden_lines = self.__class__.show_hidden_lines(service, version, mode, path + ["show_hidden_lines"])
                self.show_hidden_surfaces = self.__class__.show_hidden_surfaces(service, version, mode, path + ["show_hidden_surfaces"])
                self.surface_general_displacement = self.__class__.surface_general_displacement(service, version, mode, path + ["surface_general_displacement"])
                self.switch_to_open_glfor_remote_visualization = self.__class__.switch_to_open_glfor_remote_visualization(service, version, mode, path + ["switch_to_open_glfor_remote_visualization"])
                self.test_use_external_function = self.__class__.test_use_external_function(service, version, mode, path + ["test_use_external_function"])
                self.text_window_line_width = self.__class__.text_window_line_width(service, version, mode, path + ["text_window_line_width"])
                super().__init__(service, version, mode, path)
            class animation_option(TUIMethod):
                """
                No help available.
                """
            class backface_cull(TUIMethod):
                """
                No help available.
                """
            class camera_near_limit(TUIMethod):
                """
                No help available.
                """
            class double_buffering(TUIMethod):
                """
                No help available.
                """
            class enable_camera_near_limit_to_avoid_zfighting(TUIMethod):
                """
                No help available.
                """
            class enable_non_object_based_workflow(TUIMethod):
                """
                No help available.
                """
            class event_poll_interval(TUIMethod):
                """
                No help available.
                """
            class event_poll_timeout(TUIMethod):
                """
                No help available.
                """
            class force_key_frame_animation_markers_to_off(TUIMethod):
                """
                No help available.
                """
            class graphics_window_line_width(TUIMethod):
                """
                No help available.
                """
            class graphics_window_point_symbol(TUIMethod):
                """
                No help available.
                """
            class hidden_surface_removal_method(TUIMethod):
                """
                No help available.
                """
            class higher_resolution_graphics_window_line_width(TUIMethod):
                """
                No help available.
                """
            class lower_resolution_graphics_window_line_width(TUIMethod):
                """
                No help available.
                """
            class marker_drawing_mode(TUIMethod):
                """
                No help available.
                """
            class max_graphics_text_size(TUIMethod):
                """
                No help available.
                """
            class min_graphics_text_size(TUIMethod):
                """
                No help available.
                """
            class plot_legend_margin(TUIMethod):
                """
                No help available.
                """
            class point_tool_size(TUIMethod):
                """
                No help available.
                """
            class remove_partition_lines(TUIMethod):
                """
                No help available.
                """
            class remove_partition_lines_tolerance(TUIMethod):
                """
                No help available.
                """
            class rotation_centerpoint_visible(TUIMethod):
                """
                No help available.
                """
            class scroll_wheel_event_end_timer(TUIMethod):
                """
                No help available.
                """
            class selection_highlight_window(TUIMethod):
                """
                No help available.
                """
            class set_camera_normal_to_surface_increments(TUIMethod):
                """
                No help available.
                """
            class show_hidden_lines(TUIMethod):
                """
                No help available.
                """
            class show_hidden_surfaces(TUIMethod):
                """
                No help available.
                """
            class surface_general_displacement(TUIMethod):
                """
                No help available.
                """
            class switch_to_open_glfor_remote_visualization(TUIMethod):
                """
                No help available.
                """
            class test_use_external_function(TUIMethod):
                """
                No help available.
                """
            class text_window_line_width(TUIMethod):
                """
                No help available.
                """

            class boundary_markers(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.automatic_marker_scaling = self.__class__.automatic_marker_scaling(service, version, mode, path + ["automatic_marker_scaling"])
                    self.color_option = self.__class__.color_option(service, version, mode, path + ["color_option"])
                    self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                    self.exclude_from_bounding = self.__class__.exclude_from_bounding(service, version, mode, path + ["exclude_from_bounding"])
                    self.inlet_color = self.__class__.inlet_color(service, version, mode, path + ["inlet_color"])
                    self.marker_fraction = self.__class__.marker_fraction(service, version, mode, path + ["marker_fraction"])
                    self.marker_size_limiting_scale_multiplier = self.__class__.marker_size_limiting_scale_multiplier(service, version, mode, path + ["marker_size_limiting_scale_multiplier"])
                    self.markers_limit = self.__class__.markers_limit(service, version, mode, path + ["markers_limit"])
                    self.outlet_color = self.__class__.outlet_color(service, version, mode, path + ["outlet_color"])
                    self.scale_marker = self.__class__.scale_marker(service, version, mode, path + ["scale_marker"])
                    self.show_inlet_markers = self.__class__.show_inlet_markers(service, version, mode, path + ["show_inlet_markers"])
                    self.show_outlet_markers = self.__class__.show_outlet_markers(service, version, mode, path + ["show_outlet_markers"])
                    super().__init__(service, version, mode, path)
                class automatic_marker_scaling(TUIMethod):
                    """
                    No help available.
                    """
                class color_option(TUIMethod):
                    """
                    No help available.
                    """
                class enabled(TUIMethod):
                    """
                    No help available.
                    """
                class exclude_from_bounding(TUIMethod):
                    """
                    No help available.
                    """
                class inlet_color(TUIMethod):
                    """
                    No help available.
                    """
                class marker_fraction(TUIMethod):
                    """
                    No help available.
                    """
                class marker_size_limiting_scale_multiplier(TUIMethod):
                    """
                    No help available.
                    """
                class markers_limit(TUIMethod):
                    """
                    No help available.
                    """
                class outlet_color(TUIMethod):
                    """
                    No help available.
                    """
                class scale_marker(TUIMethod):
                    """
                    No help available.
                    """
                class show_inlet_markers(TUIMethod):
                    """
                    No help available.
                    """
                class show_outlet_markers(TUIMethod):
                    """
                    No help available.
                    """

            class colormap_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.alignment = self.__class__.alignment(service, version, mode, path + ["alignment"])
                    self.aspect_ratio_when_horizontal = self.__class__.aspect_ratio_when_horizontal(service, version, mode, path + ["aspect_ratio_when_horizontal"])
                    self.aspect_ratio_when_vertical = self.__class__.aspect_ratio_when_vertical(service, version, mode, path + ["aspect_ratio_when_vertical"])
                    self.auto_refit_on_resize = self.__class__.auto_refit_on_resize(service, version, mode, path + ["auto_refit_on_resize"])
                    self.automatic_resize = self.__class__.automatic_resize(service, version, mode, path + ["automatic_resize"])
                    self.border_style = self.__class__.border_style(service, version, mode, path + ["border_style"])
                    self.colormap = self.__class__.colormap(service, version, mode, path + ["colormap"])
                    self.isolines_position_offset = self.__class__.isolines_position_offset(service, version, mode, path + ["isolines_position_offset"])
                    self.labels = self.__class__.labels(service, version, mode, path + ["labels"])
                    self.levels = self.__class__.levels(service, version, mode, path + ["levels"])
                    self.log_scale = self.__class__.log_scale(service, version, mode, path + ["log_scale"])
                    self.major_length_to_screen_ratio_when_horizontal = self.__class__.major_length_to_screen_ratio_when_horizontal(service, version, mode, path + ["major_length_to_screen_ratio_when_horizontal"])
                    self.major_length_to_screen_ratio_when_vertical = self.__class__.major_length_to_screen_ratio_when_vertical(service, version, mode, path + ["major_length_to_screen_ratio_when_vertical"])
                    self.margin_from_edge_to_screen_ratio = self.__class__.margin_from_edge_to_screen_ratio(service, version, mode, path + ["margin_from_edge_to_screen_ratio"])
                    self.max_size_scale_factor = self.__class__.max_size_scale_factor(service, version, mode, path + ["max_size_scale_factor"])
                    self.min_size_scale_factor = self.__class__.min_size_scale_factor(service, version, mode, path + ["min_size_scale_factor"])
                    self.number_format_precision = self.__class__.number_format_precision(service, version, mode, path + ["number_format_precision"])
                    self.number_format_type = self.__class__.number_format_type(service, version, mode, path + ["number_format_type"])
                    self.preserve_aspect_ratio_for_hardcopy = self.__class__.preserve_aspect_ratio_for_hardcopy(service, version, mode, path + ["preserve_aspect_ratio_for_hardcopy"])
                    self.show_colormap = self.__class__.show_colormap(service, version, mode, path + ["show_colormap"])
                    self.skip_value = self.__class__.skip_value(service, version, mode, path + ["skip_value"])
                    self.text_behavior = self.__class__.text_behavior(service, version, mode, path + ["text_behavior"])
                    self.text_font_automatic_horizontal_size = self.__class__.text_font_automatic_horizontal_size(service, version, mode, path + ["text_font_automatic_horizontal_size"])
                    self.text_font_automatic_size = self.__class__.text_font_automatic_size(service, version, mode, path + ["text_font_automatic_size"])
                    self.text_font_automatic_units = self.__class__.text_font_automatic_units(service, version, mode, path + ["text_font_automatic_units"])
                    self.text_font_automatic_vertical_size = self.__class__.text_font_automatic_vertical_size(service, version, mode, path + ["text_font_automatic_vertical_size"])
                    self.text_font_fixed_horizontal_size = self.__class__.text_font_fixed_horizontal_size(service, version, mode, path + ["text_font_fixed_horizontal_size"])
                    self.text_font_fixed_size = self.__class__.text_font_fixed_size(service, version, mode, path + ["text_font_fixed_size"])
                    self.text_font_fixed_units = self.__class__.text_font_fixed_units(service, version, mode, path + ["text_font_fixed_units"])
                    self.text_font_fixed_vertical_size = self.__class__.text_font_fixed_vertical_size(service, version, mode, path + ["text_font_fixed_vertical_size"])
                    self.text_font_name = self.__class__.text_font_name(service, version, mode, path + ["text_font_name"])
                    self.text_truncation_limit_for_horizontal_colormaps = self.__class__.text_truncation_limit_for_horizontal_colormaps(service, version, mode, path + ["text_truncation_limit_for_horizontal_colormaps"])
                    self.text_truncation_limit_for_vertical_colormaps = self.__class__.text_truncation_limit_for_vertical_colormaps(service, version, mode, path + ["text_truncation_limit_for_vertical_colormaps"])
                    self.type = self.__class__.type(service, version, mode, path + ["type"])
                    self.use_no_sub_windows = self.__class__.use_no_sub_windows(service, version, mode, path + ["use_no_sub_windows"])
                    super().__init__(service, version, mode, path)
                class alignment(TUIMethod):
                    """
                    No help available.
                    """
                class aspect_ratio_when_horizontal(TUIMethod):
                    """
                    No help available.
                    """
                class aspect_ratio_when_vertical(TUIMethod):
                    """
                    No help available.
                    """
                class auto_refit_on_resize(TUIMethod):
                    """
                    No help available.
                    """
                class automatic_resize(TUIMethod):
                    """
                    No help available.
                    """
                class border_style(TUIMethod):
                    """
                    No help available.
                    """
                class colormap(TUIMethod):
                    """
                    No help available.
                    """
                class isolines_position_offset(TUIMethod):
                    """
                    No help available.
                    """
                class labels(TUIMethod):
                    """
                    No help available.
                    """
                class levels(TUIMethod):
                    """
                    No help available.
                    """
                class log_scale(TUIMethod):
                    """
                    No help available.
                    """
                class major_length_to_screen_ratio_when_horizontal(TUIMethod):
                    """
                    No help available.
                    """
                class major_length_to_screen_ratio_when_vertical(TUIMethod):
                    """
                    No help available.
                    """
                class margin_from_edge_to_screen_ratio(TUIMethod):
                    """
                    No help available.
                    """
                class max_size_scale_factor(TUIMethod):
                    """
                    No help available.
                    """
                class min_size_scale_factor(TUIMethod):
                    """
                    No help available.
                    """
                class number_format_precision(TUIMethod):
                    """
                    No help available.
                    """
                class number_format_type(TUIMethod):
                    """
                    No help available.
                    """
                class preserve_aspect_ratio_for_hardcopy(TUIMethod):
                    """
                    No help available.
                    """
                class show_colormap(TUIMethod):
                    """
                    No help available.
                    """
                class skip_value(TUIMethod):
                    """
                    No help available.
                    """
                class text_behavior(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_automatic_horizontal_size(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_automatic_size(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_automatic_units(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_automatic_vertical_size(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_fixed_horizontal_size(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_fixed_size(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_fixed_units(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_fixed_vertical_size(TUIMethod):
                    """
                    No help available.
                    """
                class text_font_name(TUIMethod):
                    """
                    No help available.
                    """
                class text_truncation_limit_for_horizontal_colormaps(TUIMethod):
                    """
                    No help available.
                    """
                class text_truncation_limit_for_vertical_colormaps(TUIMethod):
                    """
                    No help available.
                    """
                class type(TUIMethod):
                    """
                    No help available.
                    """
                class use_no_sub_windows(TUIMethod):
                    """
                    No help available.
                    """

            class display_lists(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.options = self.__class__.options(service, version, mode, path + ["options"])
                    super().__init__(service, version, mode, path)
                class options(TUIMethod):
                    """
                    No help available.
                    """

            class embedded_windows(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.default_embedded_mesh_windows_view = self.__class__.default_embedded_mesh_windows_view(service, version, mode, path + ["default_embedded_mesh_windows_view"])
                    self.default_embedded_windows_view = self.__class__.default_embedded_windows_view(service, version, mode, path + ["default_embedded_windows_view"])
                    self.save_embedded_window_layout = self.__class__.save_embedded_window_layout(service, version, mode, path + ["save_embedded_window_layout"])
                    self.show_border_for_embedded_window = self.__class__.show_border_for_embedded_window(service, version, mode, path + ["show_border_for_embedded_window"])
                    super().__init__(service, version, mode, path)
                class default_embedded_mesh_windows_view(TUIMethod):
                    """
                    No help available.
                    """
                class default_embedded_windows_view(TUIMethod):
                    """
                    No help available.
                    """
                class save_embedded_window_layout(TUIMethod):
                    """
                    No help available.
                    """
                class show_border_for_embedded_window(TUIMethod):
                    """
                    No help available.
                    """

            class export_video_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.advanced_video_quality_options = self.__class__.advanced_video_quality_options(service, version, mode, path + ["advanced_video_quality_options"])
                    self.video_format = self.__class__.video_format(service, version, mode, path + ["video_format"])
                    self.video_fps = self.__class__.video_fps(service, version, mode, path + ["video_fps"])
                    self.video_quality = self.__class__.video_quality(service, version, mode, path + ["video_quality"])
                    self.video_resoution_x = self.__class__.video_resoution_x(service, version, mode, path + ["video_resoution_x"])
                    self.video_resoution_y = self.__class__.video_resoution_y(service, version, mode, path + ["video_resoution_y"])
                    self.video_scale = self.__class__.video_scale(service, version, mode, path + ["video_scale"])
                    self.video_smooth_scaling = self.__class__.video_smooth_scaling(service, version, mode, path + ["video_smooth_scaling"])
                    self.video_use_frame_resolution = self.__class__.video_use_frame_resolution(service, version, mode, path + ["video_use_frame_resolution"])
                    super().__init__(service, version, mode, path)
                class video_format(TUIMethod):
                    """
                    No help available.
                    """
                class video_fps(TUIMethod):
                    """
                    No help available.
                    """
                class video_quality(TUIMethod):
                    """
                    No help available.
                    """
                class video_resoution_x(TUIMethod):
                    """
                    No help available.
                    """
                class video_resoution_y(TUIMethod):
                    """
                    No help available.
                    """
                class video_scale(TUIMethod):
                    """
                    No help available.
                    """
                class video_smooth_scaling(TUIMethod):
                    """
                    No help available.
                    """
                class video_use_frame_resolution(TUIMethod):
                    """
                    No help available.
                    """

                class advanced_video_quality_options(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.bit_rate_quality = self.__class__.bit_rate_quality(service, version, mode, path + ["bit_rate_quality"])
                        self.bitrate = self.__class__.bitrate(service, version, mode, path + ["bitrate"])
                        self.compression_method = self.__class__.compression_method(service, version, mode, path + ["compression_method"])
                        self.enable_h264 = self.__class__.enable_h264(service, version, mode, path + ["enable_h264"])
                        super().__init__(service, version, mode, path)
                    class bit_rate_quality(TUIMethod):
                        """
                        No help available.
                        """
                    class bitrate(TUIMethod):
                        """
                        No help available.
                        """
                    class compression_method(TUIMethod):
                        """
                        No help available.
                        """
                    class enable_h264(TUIMethod):
                        """
                        No help available.
                        """

            class graphics_effects(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.ambient_occlusion_enabled = self.__class__.ambient_occlusion_enabled(service, version, mode, path + ["ambient_occlusion_enabled"])
                    self.ambient_occlusion_quality = self.__class__.ambient_occlusion_quality(service, version, mode, path + ["ambient_occlusion_quality"])
                    self.ambient_occlusion_strength = self.__class__.ambient_occlusion_strength(service, version, mode, path + ["ambient_occlusion_strength"])
                    self.anti_aliasing = self.__class__.anti_aliasing(service, version, mode, path + ["anti_aliasing"])
                    self.bloom_blur = self.__class__.bloom_blur(service, version, mode, path + ["bloom_blur"])
                    self.bloom_enabled = self.__class__.bloom_enabled(service, version, mode, path + ["bloom_enabled"])
                    self.bloom_strength = self.__class__.bloom_strength(service, version, mode, path + ["bloom_strength"])
                    self.grid_color = self.__class__.grid_color(service, version, mode, path + ["grid_color"])
                    self.grid_plane_count = self.__class__.grid_plane_count(service, version, mode, path + ["grid_plane_count"])
                    self.grid_plane_enabled = self.__class__.grid_plane_enabled(service, version, mode, path + ["grid_plane_enabled"])
                    self.grid_plane_offset = self.__class__.grid_plane_offset(service, version, mode, path + ["grid_plane_offset"])
                    self.grid_plane_size_factor = self.__class__.grid_plane_size_factor(service, version, mode, path + ["grid_plane_size_factor"])
                    self.plane_direction = self.__class__.plane_direction(service, version, mode, path + ["plane_direction"])
                    self.reflections_enabled = self.__class__.reflections_enabled(service, version, mode, path + ["reflections_enabled"])
                    self.shadow_map_enabled = self.__class__.shadow_map_enabled(service, version, mode, path + ["shadow_map_enabled"])
                    self.show_edge_reflections = self.__class__.show_edge_reflections(service, version, mode, path + ["show_edge_reflections"])
                    self.show_marker_reflections = self.__class__.show_marker_reflections(service, version, mode, path + ["show_marker_reflections"])
                    self.simple_shadows_enabled = self.__class__.simple_shadows_enabled(service, version, mode, path + ["simple_shadows_enabled"])
                    self.update_after_mouse_release = self.__class__.update_after_mouse_release(service, version, mode, path + ["update_after_mouse_release"])
                    super().__init__(service, version, mode, path)
                class ambient_occlusion_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class ambient_occlusion_quality(TUIMethod):
                    """
                    No help available.
                    """
                class ambient_occlusion_strength(TUIMethod):
                    """
                    No help available.
                    """
                class anti_aliasing(TUIMethod):
                    """
                    No help available.
                    """
                class bloom_blur(TUIMethod):
                    """
                    No help available.
                    """
                class bloom_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class bloom_strength(TUIMethod):
                    """
                    No help available.
                    """
                class grid_color(TUIMethod):
                    """
                    No help available.
                    """
                class grid_plane_count(TUIMethod):
                    """
                    No help available.
                    """
                class grid_plane_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class grid_plane_offset(TUIMethod):
                    """
                    No help available.
                    """
                class grid_plane_size_factor(TUIMethod):
                    """
                    No help available.
                    """
                class plane_direction(TUIMethod):
                    """
                    No help available.
                    """
                class reflections_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class shadow_map_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class show_edge_reflections(TUIMethod):
                    """
                    No help available.
                    """
                class show_marker_reflections(TUIMethod):
                    """
                    No help available.
                    """
                class simple_shadows_enabled(TUIMethod):
                    """
                    No help available.
                    """
                class update_after_mouse_release(TUIMethod):
                    """
                    No help available.
                    """

            class hardcopy_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.export_edges_for_avz = self.__class__.export_edges_for_avz(service, version, mode, path + ["export_edges_for_avz"])
                    self.hardcopy_driver = self.__class__.hardcopy_driver(service, version, mode, path + ["hardcopy_driver"])
                    self.hardcopy_line_width = self.__class__.hardcopy_line_width(service, version, mode, path + ["hardcopy_line_width"])
                    self.hardware_image_accel = self.__class__.hardware_image_accel(service, version, mode, path + ["hardware_image_accel"])
                    self.post_script_permission_override = self.__class__.post_script_permission_override(service, version, mode, path + ["post_script_permission_override"])
                    self.retain_colormap_pos_for_avz = self.__class__.retain_colormap_pos_for_avz(service, version, mode, path + ["retain_colormap_pos_for_avz"])
                    self.save_embedded_hardcopies_separately = self.__class__.save_embedded_hardcopies_separately(service, version, mode, path + ["save_embedded_hardcopies_separately"])
                    self.save_embedded_windows_in_hardcopy = self.__class__.save_embedded_windows_in_hardcopy(service, version, mode, path + ["save_embedded_windows_in_hardcopy"])
                    self.transparent_embedded_windows = self.__class__.transparent_embedded_windows(service, version, mode, path + ["transparent_embedded_windows"])
                    super().__init__(service, version, mode, path)
                class export_edges_for_avz(TUIMethod):
                    """
                    No help available.
                    """
                class hardcopy_driver(TUIMethod):
                    """
                    No help available.
                    """
                class hardcopy_line_width(TUIMethod):
                    """
                    No help available.
                    """
                class hardware_image_accel(TUIMethod):
                    """
                    No help available.
                    """
                class post_script_permission_override(TUIMethod):
                    """
                    No help available.
                    """
                class retain_colormap_pos_for_avz(TUIMethod):
                    """
                    No help available.
                    """
                class save_embedded_hardcopies_separately(TUIMethod):
                    """
                    No help available.
                    """
                class save_embedded_windows_in_hardcopy(TUIMethod):
                    """
                    No help available.
                    """
                class transparent_embedded_windows(TUIMethod):
                    """
                    No help available.
                    """

            class lighting(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.ambient_light_intensity = self.__class__.ambient_light_intensity(service, version, mode, path + ["ambient_light_intensity"])
                    self.headlight = self.__class__.headlight(service, version, mode, path + ["headlight"])
                    self.headlight_intensity = self.__class__.headlight_intensity(service, version, mode, path + ["headlight_intensity"])
                    self.lighting_method = self.__class__.lighting_method(service, version, mode, path + ["lighting_method"])
                    super().__init__(service, version, mode, path)
                class ambient_light_intensity(TUIMethod):
                    """
                    No help available.
                    """
                class headlight(TUIMethod):
                    """
                    No help available.
                    """
                class headlight_intensity(TUIMethod):
                    """
                    No help available.
                    """
                class lighting_method(TUIMethod):
                    """
                    No help available.
                    """

            class manage_hoops_memory(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                    self.hsfimport_limit = self.__class__.hsfimport_limit(service, version, mode, path + ["hsfimport_limit"])
                    super().__init__(service, version, mode, path)
                class enabled(TUIMethod):
                    """
                    No help available.
                    """
                class hsfimport_limit(TUIMethod):
                    """
                    No help available.
                    """

            class material_effects(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.decimation_filter = self.__class__.decimation_filter(service, version, mode, path + ["decimation_filter"])
                    self.parameterization_source = self.__class__.parameterization_source(service, version, mode, path + ["parameterization_source"])
                    self.tiling_style = self.__class__.tiling_style(service, version, mode, path + ["tiling_style"])
                    super().__init__(service, version, mode, path)
                class decimation_filter(TUIMethod):
                    """
                    No help available.
                    """
                class parameterization_source(TUIMethod):
                    """
                    No help available.
                    """
                class tiling_style(TUIMethod):
                    """
                    No help available.
                    """

            class meshing_mode(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.graphics_window_display_timeout = self.__class__.graphics_window_display_timeout(service, version, mode, path + ["graphics_window_display_timeout"])
                    self.graphics_window_display_timeout_value = self.__class__.graphics_window_display_timeout_value(service, version, mode, path + ["graphics_window_display_timeout_value"])
                    super().__init__(service, version, mode, path)
                class graphics_window_display_timeout(TUIMethod):
                    """
                    No help available.
                    """
                class graphics_window_display_timeout_value(TUIMethod):
                    """
                    No help available.
                    """

            class performance(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.fast_display_mode = self.__class__.fast_display_mode(service, version, mode, path + ["fast_display_mode"])
                    self.minimum_frame_rate = self.__class__.minimum_frame_rate(service, version, mode, path + ["minimum_frame_rate"])
                    self.optimize_input_data = self.__class__.optimize_input_data(service, version, mode, path + ["optimize_input_data"])
                    self.optimize_for = self.__class__.optimize_for(service, version, mode, path + ["optimize_for"])
                    self.ratio_of_target_frame_rate_to_classify_heavy_geometry = self.__class__.ratio_of_target_frame_rate_to_classify_heavy_geometry(service, version, mode, path + ["ratio_of_target_frame_rate_to_classify_heavy_geometry"])
                    self.ratio_of_target_frame_rate_to_declassify_heavy_geometry = self.__class__.ratio_of_target_frame_rate_to_declassify_heavy_geometry(service, version, mode, path + ["ratio_of_target_frame_rate_to_declassify_heavy_geometry"])
                    self.surface_caching = self.__class__.surface_caching(service, version, mode, path + ["surface_caching"])
                    super().__init__(service, version, mode, path)
                class optimize_for(TUIMethod):
                    """
                    No help available.
                    """
                class ratio_of_target_frame_rate_to_classify_heavy_geometry(TUIMethod):
                    """
                    No help available.
                    """
                class ratio_of_target_frame_rate_to_declassify_heavy_geometry(TUIMethod):
                    """
                    No help available.
                    """
                class surface_caching(TUIMethod):
                    """
                    No help available.
                    """

                class fast_display_mode(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.culling = self.__class__.culling(service, version, mode, path + ["culling"])
                        self.faces_shown = self.__class__.faces_shown(service, version, mode, path + ["faces_shown"])
                        self.markers_decimation = self.__class__.markers_decimation(service, version, mode, path + ["markers_decimation"])
                        self.nodes_shown = self.__class__.nodes_shown(service, version, mode, path + ["nodes_shown"])
                        self.perimeter_edges_shown = self.__class__.perimeter_edges_shown(service, version, mode, path + ["perimeter_edges_shown"])
                        self.silhouette_shown = self.__class__.silhouette_shown(service, version, mode, path + ["silhouette_shown"])
                        self.status = self.__class__.status(service, version, mode, path + ["status"])
                        self.transparency = self.__class__.transparency(service, version, mode, path + ["transparency"])
                        super().__init__(service, version, mode, path)
                    class culling(TUIMethod):
                        """
                        No help available.
                        """
                    class faces_shown(TUIMethod):
                        """
                        No help available.
                        """
                    class markers_decimation(TUIMethod):
                        """
                        No help available.
                        """
                    class nodes_shown(TUIMethod):
                        """
                        No help available.
                        """
                    class perimeter_edges_shown(TUIMethod):
                        """
                        No help available.
                        """
                    class silhouette_shown(TUIMethod):
                        """
                        No help available.
                        """
                    class status(TUIMethod):
                        """
                        No help available.
                        """
                    class transparency(TUIMethod):
                        """
                        No help available.
                        """

                class minimum_frame_rate(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.dynamic_adjustment = self.__class__.dynamic_adjustment(service, version, mode, path + ["dynamic_adjustment"])
                        self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                        self.fixed_culling_value = self.__class__.fixed_culling_value(service, version, mode, path + ["fixed_culling_value"])
                        self.maximum_culling_threshold = self.__class__.maximum_culling_threshold(service, version, mode, path + ["maximum_culling_threshold"])
                        self.minimum_culling_threshold = self.__class__.minimum_culling_threshold(service, version, mode, path + ["minimum_culling_threshold"])
                        self.target_fps = self.__class__.target_fps(service, version, mode, path + ["target_fps"])
                        super().__init__(service, version, mode, path)
                    class dynamic_adjustment(TUIMethod):
                        """
                        No help available.
                        """
                    class enabled(TUIMethod):
                        """
                        No help available.
                        """
                    class fixed_culling_value(TUIMethod):
                        """
                        No help available.
                        """
                    class maximum_culling_threshold(TUIMethod):
                        """
                        No help available.
                        """
                    class minimum_culling_threshold(TUIMethod):
                        """
                        No help available.
                        """
                    class target_fps(TUIMethod):
                        """
                        No help available.
                        """

                class optimize_input_data(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.enabled = self.__class__.enabled(service, version, mode, path + ["enabled"])
                        self.maximum_facets_per_shell = self.__class__.maximum_facets_per_shell(service, version, mode, path + ["maximum_facets_per_shell"])
                        super().__init__(service, version, mode, path)
                    class enabled(TUIMethod):
                        """
                        No help available.
                        """
                    class maximum_facets_per_shell(TUIMethod):
                        """
                        No help available.
                        """

            class ray_tracing_options(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.volume_rendering_method = self.__class__.volume_rendering_method(service, version, mode, path + ["volume_rendering_method"])
                    super().__init__(service, version, mode, path)
                class volume_rendering_method(TUIMethod):
                    """
                    No help available.
                    """

            class transparency(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.algorithm_for_modern_drivers = self.__class__.algorithm_for_modern_drivers(service, version, mode, path + ["algorithm_for_modern_drivers"])
                    self.depth_peeling_layers = self.__class__.depth_peeling_layers(service, version, mode, path + ["depth_peeling_layers"])
                    self.depth_peeling_preference = self.__class__.depth_peeling_preference(service, version, mode, path + ["depth_peeling_preference"])
                    self.quick_moves = self.__class__.quick_moves(service, version, mode, path + ["quick_moves"])
                    self.zsort_options = self.__class__.zsort_options(service, version, mode, path + ["zsort_options"])
                    super().__init__(service, version, mode, path)
                class algorithm_for_modern_drivers(TUIMethod):
                    """
                    No help available.
                    """
                class depth_peeling_layers(TUIMethod):
                    """
                    No help available.
                    """
                class depth_peeling_preference(TUIMethod):
                    """
                    No help available.
                    """
                class quick_moves(TUIMethod):
                    """
                    No help available.
                    """
                class zsort_options(TUIMethod):
                    """
                    No help available.
                    """

            class vector_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.arrow3_dradius1_factor = self.__class__.arrow3_dradius1_factor(service, version, mode, path + ["arrow3_dradius1_factor"])
                    self.arrow3_dradius2_factor = self.__class__.arrow3_dradius2_factor(service, version, mode, path + ["arrow3_dradius2_factor"])
                    self.arrowhead3_dradius1_factor = self.__class__.arrowhead3_dradius1_factor(service, version, mode, path + ["arrowhead3_dradius1_factor"])
                    self.line_arrow3_dperpendicular_radius = self.__class__.line_arrow3_dperpendicular_radius(service, version, mode, path + ["line_arrow3_dperpendicular_radius"])
                    super().__init__(service, version, mode, path)
                class arrow3_dradius1_factor(TUIMethod):
                    """
                    No help available.
                    """
                class arrow3_dradius2_factor(TUIMethod):
                    """
                    No help available.
                    """
                class arrowhead3_dradius1_factor(TUIMethod):
                    """
                    No help available.
                    """
                class line_arrow3_dperpendicular_radius(TUIMethod):
                    """
                    No help available.
                    """

        class mat_pro_app(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.check_expression = self.__class__.check_expression(service, version, mode, path + ["check_expression"])
                self.statistics = self.__class__.statistics(service, version, mode, path + ["statistics"])
                self.beta_features = self.__class__.beta_features(service, version, mode, path + ["beta_features"])
                self.check_crash = self.__class__.check_crash(service, version, mode, path + ["check_crash"])
                self.debug = self.__class__.debug(service, version, mode, path + ["debug"])
                self.focus = self.__class__.focus(service, version, mode, path + ["focus"])
                self.mesh_naming = self.__class__.mesh_naming(service, version, mode, path + ["mesh_naming"])
                self.tracking = self.__class__.tracking(service, version, mode, path + ["tracking"])
                self.warning = self.__class__.warning(service, version, mode, path + ["warning"])
                super().__init__(service, version, mode, path)
            class beta_features(TUIMethod):
                """
                No help available.
                """
            class check_crash(TUIMethod):
                """
                No help available.
                """
            class debug(TUIMethod):
                """
                No help available.
                """
            class focus(TUIMethod):
                """
                No help available.
                """
            class mesh_naming(TUIMethod):
                """
                No help available.
                """
            class tracking(TUIMethod):
                """
                No help available.
                """
            class warning(TUIMethod):
                """
                No help available.
                """

            class check_expression(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.cdot = self.__class__.cdot(service, version, mode, path + ["cdot"])
                    self.coordinates = self.__class__.coordinates(service, version, mode, path + ["coordinates"])
                    self.dvv = self.__class__.dvv(service, version, mode, path + ["dvv"])
                    self.edot = self.__class__.edot(service, version, mode, path + ["edot"])
                    self.gdot = self.__class__.gdot(service, version, mode, path + ["gdot"])
                    self.giesekus = self.__class__.giesekus(service, version, mode, path + ["giesekus"])
                    self.pressure = self.__class__.pressure(service, version, mode, path + ["pressure"])
                    self.species = self.__class__.species(service, version, mode, path + ["species"])
                    self.temperature = self.__class__.temperature(service, version, mode, path + ["temperature"])
                    self.time = self.__class__.time(service, version, mode, path + ["time"])
                    self.velocities = self.__class__.velocities(service, version, mode, path + ["velocities"])
                    self.vorticity = self.__class__.vorticity(service, version, mode, path + ["vorticity"])
                    super().__init__(service, version, mode, path)
                class cdot(TUIMethod):
                    """
                    No help available.
                    """
                class coordinates(TUIMethod):
                    """
                    No help available.
                    """
                class dvv(TUIMethod):
                    """
                    No help available.
                    """
                class edot(TUIMethod):
                    """
                    No help available.
                    """
                class gdot(TUIMethod):
                    """
                    No help available.
                    """
                class giesekus(TUIMethod):
                    """
                    No help available.
                    """
                class pressure(TUIMethod):
                    """
                    No help available.
                    """
                class species(TUIMethod):
                    """
                    No help available.
                    """
                class temperature(TUIMethod):
                    """
                    No help available.
                    """
                class time(TUIMethod):
                    """
                    No help available.
                    """
                class velocities(TUIMethod):
                    """
                    No help available.
                    """
                class vorticity(TUIMethod):
                    """
                    No help available.
                    """

            class statistics(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.max_positions = self.__class__.max_positions(service, version, mode, path + ["max_positions"])
                    self.point_size = self.__class__.point_size(service, version, mode, path + ["point_size"])
                    self.point_symbol = self.__class__.point_symbol(service, version, mode, path + ["point_symbol"])
                    self.quick_slicing = self.__class__.quick_slicing(service, version, mode, path + ["quick_slicing"])
                    self.vector_size = self.__class__.vector_size(service, version, mode, path + ["vector_size"])
                    self.vector_symbol = self.__class__.vector_symbol(service, version, mode, path + ["vector_symbol"])
                    super().__init__(service, version, mode, path)
                class max_positions(TUIMethod):
                    """
                    No help available.
                    """
                class point_size(TUIMethod):
                    """
                    No help available.
                    """
                class point_symbol(TUIMethod):
                    """
                    No help available.
                    """
                class quick_slicing(TUIMethod):
                    """
                    No help available.
                    """
                class vector_size(TUIMethod):
                    """
                    No help available.
                    """
                class vector_symbol(TUIMethod):
                    """
                    No help available.
                    """

        class meshing_workflow(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.cad_log_option = self.__class__.cad_log_option(service, version, mode, path + ["cad_log_option"])
                self.draw_settings = self.__class__.draw_settings(service, version, mode, path + ["draw_settings"])
                self.checkpointing_option = self.__class__.checkpointing_option(service, version, mode, path + ["checkpointing_option"])
                self.save_checkpoint_files = self.__class__.save_checkpoint_files(service, version, mode, path + ["save_checkpoint_files"])
                self.save_wft_file_with_mesh = self.__class__.save_wft_file_with_mesh(service, version, mode, path + ["save_wft_file_with_mesh"])
                self.temp_folder = self.__class__.temp_folder(service, version, mode, path + ["temp_folder"])
                self.templates_folder = self.__class__.templates_folder(service, version, mode, path + ["templates_folder"])
                self.verbosity = self.__class__.verbosity(service, version, mode, path + ["verbosity"])
                super().__init__(service, version, mode, path)
            class checkpointing_option(TUIMethod):
                """
                No help available.
                """
            class save_checkpoint_files(TUIMethod):
                """
                No help available.
                """
            class save_wft_file_with_mesh(TUIMethod):
                """
                No help available.
                """
            class temp_folder(TUIMethod):
                """
                No help available.
                """
            class templates_folder(TUIMethod):
                """
                No help available.
                """
            class verbosity(TUIMethod):
                """
                No help available.
                """

            class cad_log_option(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.location = self.__class__.location(service, version, mode, path + ["location"])
                    self.prefix = self.__class__.prefix(service, version, mode, path + ["prefix"])
                    self.write = self.__class__.write(service, version, mode, path + ["write"])
                    super().__init__(service, version, mode, path)
                class location(TUIMethod):
                    """
                    No help available.
                    """
                class prefix(TUIMethod):
                    """
                    No help available.
                    """
                class write(TUIMethod):
                    """
                    No help available.
                    """

            class draw_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.auto_draw = self.__class__.auto_draw(service, version, mode, path + ["auto_draw"])
                    self.face_zone_limit = self.__class__.face_zone_limit(service, version, mode, path + ["face_zone_limit"])
                    self.facet_limit = self.__class__.facet_limit(service, version, mode, path + ["facet_limit"])
                    super().__init__(service, version, mode, path)
                class auto_draw(TUIMethod):
                    """
                    No help available.
                    """
                class face_zone_limit(TUIMethod):
                    """
                    No help available.
                    """
                class facet_limit(TUIMethod):
                    """
                    No help available.
                    """

        class navigation(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.mouse_mapping = self.__class__.mouse_mapping(service, version, mode, path + ["mouse_mapping"])
                super().__init__(service, version, mode, path)

            class mouse_mapping(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.additional = self.__class__.additional(service, version, mode, path + ["additional"])
                    self.basic = self.__class__.basic(service, version, mode, path + ["basic"])
                    self.mousemaptheme = self.__class__.mousemaptheme(service, version, mode, path + ["mousemaptheme"])
                    super().__init__(service, version, mode, path)
                class mousemaptheme(TUIMethod):
                    """
                    No help available.
                    """

                class additional(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.ctrllmbclick = self.__class__.ctrllmbclick(service, version, mode, path + ["ctrllmbclick"])
                        self.ctrllmbdrag = self.__class__.ctrllmbdrag(service, version, mode, path + ["ctrllmbdrag"])
                        self.ctrlmmbclick = self.__class__.ctrlmmbclick(service, version, mode, path + ["ctrlmmbclick"])
                        self.ctrlmmbdrag = self.__class__.ctrlmmbdrag(service, version, mode, path + ["ctrlmmbdrag"])
                        self.ctrlrmbclick = self.__class__.ctrlrmbclick(service, version, mode, path + ["ctrlrmbclick"])
                        self.ctrlrmbdrag = self.__class__.ctrlrmbdrag(service, version, mode, path + ["ctrlrmbdrag"])
                        self.mouseprobe = self.__class__.mouseprobe(service, version, mode, path + ["mouseprobe"])
                        self.mousewheel = self.__class__.mousewheel(service, version, mode, path + ["mousewheel"])
                        self.mousewheelsensitivity = self.__class__.mousewheelsensitivity(service, version, mode, path + ["mousewheelsensitivity"])
                        self.reversewheeldirection = self.__class__.reversewheeldirection(service, version, mode, path + ["reversewheeldirection"])
                        self.shiftlmbclick = self.__class__.shiftlmbclick(service, version, mode, path + ["shiftlmbclick"])
                        self.shiftlmbdrag = self.__class__.shiftlmbdrag(service, version, mode, path + ["shiftlmbdrag"])
                        self.shiftmmbclick = self.__class__.shiftmmbclick(service, version, mode, path + ["shiftmmbclick"])
                        self.shiftmmbdrag = self.__class__.shiftmmbdrag(service, version, mode, path + ["shiftmmbdrag"])
                        self.shiftrmbclick = self.__class__.shiftrmbclick(service, version, mode, path + ["shiftrmbclick"])
                        self.shiftrmbdrag = self.__class__.shiftrmbdrag(service, version, mode, path + ["shiftrmbdrag"])
                        super().__init__(service, version, mode, path)
                    class ctrllmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class ctrllmbdrag(TUIMethod):
                        """
                        No help available.
                        """
                    class ctrlmmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class ctrlmmbdrag(TUIMethod):
                        """
                        No help available.
                        """
                    class ctrlrmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class ctrlrmbdrag(TUIMethod):
                        """
                        No help available.
                        """
                    class mouseprobe(TUIMethod):
                        """
                        No help available.
                        """
                    class mousewheel(TUIMethod):
                        """
                        No help available.
                        """
                    class mousewheelsensitivity(TUIMethod):
                        """
                        No help available.
                        """
                    class reversewheeldirection(TUIMethod):
                        """
                        No help available.
                        """
                    class shiftlmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class shiftlmbdrag(TUIMethod):
                        """
                        No help available.
                        """
                    class shiftmmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class shiftmmbdrag(TUIMethod):
                        """
                        No help available.
                        """
                    class shiftrmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class shiftrmbdrag(TUIMethod):
                        """
                        No help available.
                        """

                class basic(TUIMenu):
                    """
                    No help available.
                    """
                    def __init__(self, service, version, mode, path):
                        self.lmb = self.__class__.lmb(service, version, mode, path + ["lmb"])
                        self.lmbclick = self.__class__.lmbclick(service, version, mode, path + ["lmbclick"])
                        self.mmb = self.__class__.mmb(service, version, mode, path + ["mmb"])
                        self.mmbclick = self.__class__.mmbclick(service, version, mode, path + ["mmbclick"])
                        self.rmb = self.__class__.rmb(service, version, mode, path + ["rmb"])
                        self.rmbclick = self.__class__.rmbclick(service, version, mode, path + ["rmbclick"])
                        super().__init__(service, version, mode, path)
                    class lmb(TUIMethod):
                        """
                        No help available.
                        """
                    class lmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class mmb(TUIMethod):
                        """
                        No help available.
                        """
                    class mmbclick(TUIMethod):
                        """
                        No help available.
                        """
                    class rmb(TUIMethod):
                        """
                        No help available.
                        """
                    class rmbclick(TUIMethod):
                        """
                        No help available.
                        """

        class parametric_study(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.layout_options = self.__class__.layout_options(service, version, mode, path + ["layout_options"])
                self.update_options = self.__class__.update_options(service, version, mode, path + ["update_options"])
                super().__init__(service, version, mode, path)

            class layout_options(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.current_case_parameters = self.__class__.current_case_parameters(service, version, mode, path + ["current_case_parameters"])
                    self.parametric_study_tree = self.__class__.parametric_study_tree(service, version, mode, path + ["parametric_study_tree"])
                    super().__init__(service, version, mode, path)
                class current_case_parameters(TUIMethod):
                    """
                    No help available.
                    """
                class parametric_study_tree(TUIMethod):
                    """
                    No help available.
                    """

            class update_options(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.auto_refresh_time = self.__class__.auto_refresh_time(service, version, mode, path + ["auto_refresh_time"])
                    self.capture_sim_report_data = self.__class__.capture_sim_report_data(service, version, mode, path + ["capture_sim_report_data"])
                    self.enable_auto_refresh = self.__class__.enable_auto_refresh(service, version, mode, path + ["enable_auto_refresh"])
                    self.parameter_value_precision = self.__class__.parameter_value_precision(service, version, mode, path + ["parameter_value_precision"])
                    self.save_project_after_dpupdate = self.__class__.save_project_after_dpupdate(service, version, mode, path + ["save_project_after_dpupdate"])
                    self.write_data = self.__class__.write_data(service, version, mode, path + ["write_data"])
                    super().__init__(service, version, mode, path)
                class auto_refresh_time(TUIMethod):
                    """
                    No help available.
                    """
                class capture_sim_report_data(TUIMethod):
                    """
                    No help available.
                    """
                class enable_auto_refresh(TUIMethod):
                    """
                    No help available.
                    """
                class parameter_value_precision(TUIMethod):
                    """
                    No help available.
                    """
                class save_project_after_dpupdate(TUIMethod):
                    """
                    No help available.
                    """
                class write_data(TUIMethod):
                    """
                    No help available.
                    """

        class prj_app(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.advanced_flag = self.__class__.advanced_flag(service, version, mode, path + ["advanced_flag"])
                self.beta_flag = self.__class__.beta_flag(service, version, mode, path + ["beta_flag"])
                self.unit_system = self.__class__.unit_system(service, version, mode, path + ["unit_system"])
                super().__init__(service, version, mode, path)
            class advanced_flag(TUIMethod):
                """
                No help available.
                """
            class beta_flag(TUIMethod):
                """
                No help available.
                """
            class unit_system(TUIMethod):
                """
                No help available.
                """

        class python_console(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.console_suggestion = self.__class__.console_suggestion(service, version, mode, path + ["console_suggestion"])
                self.console_suggestion_active_only = self.__class__.console_suggestion_active_only(service, version, mode, path + ["console_suggestion_active_only"])
                self.pretty_print_dict = self.__class__.pretty_print_dict(service, version, mode, path + ["pretty_print_dict"])
                self.quick_search_results_active_only = self.__class__.quick_search_results_active_only(service, version, mode, path + ["quick_search_results_active_only"])
                super().__init__(service, version, mode, path)
            class console_suggestion(TUIMethod):
                """
                No help available.
                """
            class console_suggestion_active_only(TUIMethod):
                """
                No help available.
                """
            class pretty_print_dict(TUIMethod):
                """
                No help available.
                """
            class quick_search_results_active_only(TUIMethod):
                """
                No help available.
                """

        class simulation(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.report_definitions = self.__class__.report_definitions(service, version, mode, path + ["report_definitions"])
                self.flow_model = self.__class__.flow_model(service, version, mode, path + ["flow_model"])
                self.local_residual_scaling = self.__class__.local_residual_scaling(service, version, mode, path + ["local_residual_scaling"])
                self.pdf_combustion_robust_numerics = self.__class__.pdf_combustion_robust_numerics(service, version, mode, path + ["pdf_combustion_robust_numerics"])
                super().__init__(service, version, mode, path)
            class flow_model(TUIMethod):
                """
                No help available.
                """
            class local_residual_scaling(TUIMethod):
                """
                No help available.
                """
            class pdf_combustion_robust_numerics(TUIMethod):
                """
                No help available.
                """

            class report_definitions(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.automatic_plot_file = self.__class__.automatic_plot_file(service, version, mode, path + ["automatic_plot_file"])
                    self.report_plot_history_data_size = self.__class__.report_plot_history_data_size(service, version, mode, path + ["report_plot_history_data_size"])
                    super().__init__(service, version, mode, path)
                class automatic_plot_file(TUIMethod):
                    """
                    No help available.
                    """
                class report_plot_history_data_size(TUIMethod):
                    """
                    No help available.
                    """

        class turbo_setup(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.face_zone_settings = self.__class__.face_zone_settings(service, version, mode, path + ["face_zone_settings"])
                self.graphics_settings = self.__class__.graphics_settings(service, version, mode, path + ["graphics_settings"])
                self.checkpointing_option = self.__class__.checkpointing_option(service, version, mode, path + ["checkpointing_option"])
                self.save_checkpoint_files = self.__class__.save_checkpoint_files(service, version, mode, path + ["save_checkpoint_files"])
                super().__init__(service, version, mode, path)
            class checkpointing_option(TUIMethod):
                """
                No help available.
                """
            class save_checkpoint_files(TUIMethod):
                """
                No help available.
                """

            class face_zone_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.blade_region = self.__class__.blade_region(service, version, mode, path + ["blade_region"])
                    self.fzsearch_order = self.__class__.fzsearch_order(service, version, mode, path + ["fzsearch_order"])
                    self.hub_region = self.__class__.hub_region(service, version, mode, path + ["hub_region"])
                    self.inlet_region = self.__class__.inlet_region(service, version, mode, path + ["inlet_region"])
                    self.interior_region = self.__class__.interior_region(service, version, mode, path + ["interior_region"])
                    self.outlet_region = self.__class__.outlet_region(service, version, mode, path + ["outlet_region"])
                    self.periodic1_region = self.__class__.periodic1_region(service, version, mode, path + ["periodic1_region"])
                    self.periodic2_region = self.__class__.periodic2_region(service, version, mode, path + ["periodic2_region"])
                    self.shroud_region = self.__class__.shroud_region(service, version, mode, path + ["shroud_region"])
                    self.symmetry_region = self.__class__.symmetry_region(service, version, mode, path + ["symmetry_region"])
                    self.tip1_region = self.__class__.tip1_region(service, version, mode, path + ["tip1_region"])
                    self.tip2_region = self.__class__.tip2_region(service, version, mode, path + ["tip2_region"])
                    super().__init__(service, version, mode, path)
                class blade_region(TUIMethod):
                    """
                    No help available.
                    """
                class fzsearch_order(TUIMethod):
                    """
                    No help available.
                    """
                class hub_region(TUIMethod):
                    """
                    No help available.
                    """
                class inlet_region(TUIMethod):
                    """
                    No help available.
                    """
                class interior_region(TUIMethod):
                    """
                    No help available.
                    """
                class outlet_region(TUIMethod):
                    """
                    No help available.
                    """
                class periodic1_region(TUIMethod):
                    """
                    No help available.
                    """
                class periodic2_region(TUIMethod):
                    """
                    No help available.
                    """
                class shroud_region(TUIMethod):
                    """
                    No help available.
                    """
                class symmetry_region(TUIMethod):
                    """
                    No help available.
                    """
                class tip1_region(TUIMethod):
                    """
                    No help available.
                    """
                class tip2_region(TUIMethod):
                    """
                    No help available.
                    """

            class graphics_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.auto_draw = self.__class__.auto_draw(service, version, mode, path + ["auto_draw"])
                    super().__init__(service, version, mode, path)
                class auto_draw(TUIMethod):
                    """
                    No help available.
                    """

        class turbo_workflow(TUIMenu):
            """
            No help available.
            """
            def __init__(self, service, version, mode, path):
                self.face_zone_settings = self.__class__.face_zone_settings(service, version, mode, path + ["face_zone_settings"])
                self.graphics_settings = self.__class__.graphics_settings(service, version, mode, path + ["graphics_settings"])
                self.checkpointing_option = self.__class__.checkpointing_option(service, version, mode, path + ["checkpointing_option"])
                self.save_checkpoint_files = self.__class__.save_checkpoint_files(service, version, mode, path + ["save_checkpoint_files"])
                super().__init__(service, version, mode, path)
            class checkpointing_option(TUIMethod):
                """
                No help available.
                """
            class save_checkpoint_files(TUIMethod):
                """
                No help available.
                """

            class face_zone_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.blade_region = self.__class__.blade_region(service, version, mode, path + ["blade_region"])
                    self.fzsearch_order = self.__class__.fzsearch_order(service, version, mode, path + ["fzsearch_order"])
                    self.hub_region = self.__class__.hub_region(service, version, mode, path + ["hub_region"])
                    self.inlet_region = self.__class__.inlet_region(service, version, mode, path + ["inlet_region"])
                    self.interior_region = self.__class__.interior_region(service, version, mode, path + ["interior_region"])
                    self.outlet_region = self.__class__.outlet_region(service, version, mode, path + ["outlet_region"])
                    self.periodic1_region = self.__class__.periodic1_region(service, version, mode, path + ["periodic1_region"])
                    self.periodic2_region = self.__class__.periodic2_region(service, version, mode, path + ["periodic2_region"])
                    self.shroud_region = self.__class__.shroud_region(service, version, mode, path + ["shroud_region"])
                    self.symmetry_region = self.__class__.symmetry_region(service, version, mode, path + ["symmetry_region"])
                    self.tip1_region = self.__class__.tip1_region(service, version, mode, path + ["tip1_region"])
                    self.tip2_region = self.__class__.tip2_region(service, version, mode, path + ["tip2_region"])
                    super().__init__(service, version, mode, path)
                class blade_region(TUIMethod):
                    """
                    No help available.
                    """
                class fzsearch_order(TUIMethod):
                    """
                    No help available.
                    """
                class hub_region(TUIMethod):
                    """
                    No help available.
                    """
                class inlet_region(TUIMethod):
                    """
                    No help available.
                    """
                class interior_region(TUIMethod):
                    """
                    No help available.
                    """
                class outlet_region(TUIMethod):
                    """
                    No help available.
                    """
                class periodic1_region(TUIMethod):
                    """
                    No help available.
                    """
                class periodic2_region(TUIMethod):
                    """
                    No help available.
                    """
                class shroud_region(TUIMethod):
                    """
                    No help available.
                    """
                class symmetry_region(TUIMethod):
                    """
                    No help available.
                    """
                class tip1_region(TUIMethod):
                    """
                    No help available.
                    """
                class tip2_region(TUIMethod):
                    """
                    No help available.
                    """

            class graphics_settings(TUIMenu):
                """
                No help available.
                """
                def __init__(self, service, version, mode, path):
                    self.auto_draw = self.__class__.auto_draw(service, version, mode, path + ["auto_draw"])
                    super().__init__(service, version, mode, path)
                class auto_draw(TUIMethod):
                    """
                    No help available.
                    """

    class reference_frames(TUIMenu):
        """
        Manage reference frames.
        """
        def __init__(self, service, version, mode, path):
            self.add = self.__class__.add(service, version, mode, path + ["add"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.display = self.__class__.display(service, version, mode, path + ["display"])
            self.display_edit = self.__class__.display_edit(service, version, mode, path + ["display_edit"])
            self.edit = self.__class__.edit(service, version, mode, path + ["edit"])
            self.hide = self.__class__.hide(service, version, mode, path + ["hide"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.list_properties = self.__class__.list_properties(service, version, mode, path + ["list_properties"])
            super().__init__(service, version, mode, path)
        class add(TUIMethod):
            """
            Add a new object.
            """
        class delete(TUIMethod):
            """
            Delete an object.
            """
        class display(TUIMethod):
            """
            Display Reference Frame.
            """
        class display_edit(TUIMethod):
            """
            Display and edit reference frame from graphics.
            """
        class edit(TUIMethod):
            """
            Edit an object.
            """
        class hide(TUIMethod):
            """
            Hide Reference Frame.
            """
        class list(TUIMethod):
            """
            List objects.
            """
        class list_properties(TUIMethod):
            """
            List properties of an object.
            """

    class report(TUIMenu):
        """
        Enter the report menu.
        """
        def __init__(self, service, version, mode, path):
            self.boundary_cell_quality = self.__class__.boundary_cell_quality(service, version, mode, path + ["boundary_cell_quality"])
            self.cell_distribution = self.__class__.cell_distribution(service, version, mode, path + ["cell_distribution"])
            self.cell_quality_limits = self.__class__.cell_quality_limits(service, version, mode, path + ["cell_quality_limits"])
            self.cell_size_limits = self.__class__.cell_size_limits(service, version, mode, path + ["cell_size_limits"])
            self.cell_zone_at_location = self.__class__.cell_zone_at_location(service, version, mode, path + ["cell_zone_at_location"])
            self.cell_zone_volume = self.__class__.cell_zone_volume(service, version, mode, path + ["cell_zone_volume"])
            self.edge_size_limits = self.__class__.edge_size_limits(service, version, mode, path + ["edge_size_limits"])
            self.enhanced_orthogonal_quality = self.__class__.enhanced_orthogonal_quality(service, version, mode, path + ["enhanced_orthogonal_quality"])
            self.face_distribution = self.__class__.face_distribution(service, version, mode, path + ["face_distribution"])
            self.face_node_degree_distribution = self.__class__.face_node_degree_distribution(service, version, mode, path + ["face_node_degree_distribution"])
            self.face_quality_limits = self.__class__.face_quality_limits(service, version, mode, path + ["face_quality_limits"])
            self.face_size_limits = self.__class__.face_size_limits(service, version, mode, path + ["face_size_limits"])
            self.face_zone_area = self.__class__.face_zone_area(service, version, mode, path + ["face_zone_area"])
            self.face_zone_at_location = self.__class__.face_zone_at_location(service, version, mode, path + ["face_zone_at_location"])
            self.list_cell_quality = self.__class__.list_cell_quality(service, version, mode, path + ["list_cell_quality"])
            self.memory_usage = self.__class__.memory_usage(service, version, mode, path + ["memory_usage"])
            self.mesh_size = self.__class__.mesh_size(service, version, mode, path + ["mesh_size"])
            self.mesh_statistics = self.__class__.mesh_statistics(service, version, mode, path + ["mesh_statistics"])
            self.meshing_time = self.__class__.meshing_time(service, version, mode, path + ["meshing_time"])
            self.neighborhood_quality = self.__class__.neighborhood_quality(service, version, mode, path + ["neighborhood_quality"])
            self.number_meshed = self.__class__.number_meshed(service, version, mode, path + ["number_meshed"])
            self.print_info = self.__class__.print_info(service, version, mode, path + ["print_info"])
            self.quality_method = self.__class__.quality_method(service, version, mode, path + ["quality_method"])
            self.spy_level = self.__class__.spy_level(service, version, mode, path + ["spy_level"])
            self.unrefined_cells = self.__class__.unrefined_cells(service, version, mode, path + ["unrefined_cells"])
            self.update_bounding_box = self.__class__.update_bounding_box(service, version, mode, path + ["update_bounding_box"])
            self.verbosity_level = self.__class__.verbosity_level(service, version, mode, path + ["verbosity_level"])
            super().__init__(service, version, mode, path)
        class boundary_cell_quality(TUIMethod):
            """
            Report quality of boundary cells.
            """
        class cell_distribution(TUIMethod):
            """
            Report distribution of cell quality.
            """
        class cell_quality_limits(TUIMethod):
            """
            Report cell quality limits.
            """
        class cell_size_limits(TUIMethod):
            """
            Report cell size limits.
            """
        class cell_zone_at_location(TUIMethod):
            """
            Report cell zone at given location.
            """
        class cell_zone_volume(TUIMethod):
            """
            Report volume of a cell zone.
            """
        class edge_size_limits(TUIMethod):
            """
            Report edge size limits.
            """
        class enhanced_orthogonal_quality(TUIMethod):
            """
            Enable enhanced orthogonal quality method.
            """
        class face_distribution(TUIMethod):
            """
            Reports the distribution of face quality.
            """
        class face_node_degree_distribution(TUIMethod):
            """
            Report face node degree of boundary faces.
            """
        class face_quality_limits(TUIMethod):
            """
            Report face quality limits.
            """
        class face_size_limits(TUIMethod):
            """
            Report face size limits.
            """
        class face_zone_area(TUIMethod):
            """
            Report area of a face zone.
            """
        class face_zone_at_location(TUIMethod):
            """
            Report face zone at given location.
            """
        class list_cell_quality(TUIMethod):
            """
            List cells between quality limits.
            """
        class memory_usage(TUIMethod):
            """
            Report memory usage.
            """
        class mesh_size(TUIMethod):
            """
            Report number of each type of grid object.
            """
        class mesh_statistics(TUIMethod):
            """
            Write vital mesh statistics to file.
            """
        class meshing_time(TUIMethod):
            """
            Report meshing time.
            """
        class neighborhood_quality(TUIMethod):
            """
            Report max quality measure of all cells using node.
            """
        class number_meshed(TUIMethod):
            """
            Report number of nodes and faces that have been meshed.
            """
        class print_info(TUIMethod):
            """
            Print node/face/cell info.
            """
        class quality_method(TUIMethod):
            """
            Method to use for measuring face and cell quality.
            """
        class spy_level(TUIMethod):
            """
            Spy on meshing process.
            """
        class unrefined_cells(TUIMethod):
            """
            Report number of cells not refined.
            """
        class update_bounding_box(TUIMethod):
            """
            Updates bounding box.
            """
        class verbosity_level(TUIMethod):
            """
            Verbosity level control.
            """

    class scoped_sizing(TUIMenu):
        """
        Manage scoped sizing.
        """
        def __init__(self, service, version, mode, path):
            self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
            self.create = self.__class__.create(service, version, mode, path + ["create"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
            self.delete_size_field = self.__class__.delete_size_field(service, version, mode, path + ["delete_size_field"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.list_zones_uncovered_by_controls = self.__class__.list_zones_uncovered_by_controls(service, version, mode, path + ["list_zones_uncovered_by_controls"])
            self.modify = self.__class__.modify(service, version, mode, path + ["modify"])
            self.read = self.__class__.read(service, version, mode, path + ["read"])
            self.validate = self.__class__.validate(service, version, mode, path + ["validate"])
            self.write = self.__class__.write(service, version, mode, path + ["write"])
            super().__init__(service, version, mode, path)
        class compute(TUIMethod):
            """
            Compute scoped sizing/functions.
            """
        class create(TUIMethod):
            """
            Create new scoped sizing.
            """
        class delete(TUIMethod):
            """
            Delete scoped sizing.
            """
        class delete_all(TUIMethod):
            """
            Delete all scoped sizing.
            """
        class delete_size_field(TUIMethod):
            """
            Reset all the processed sizing functions/scoped sizing.
            """
        class list(TUIMethod):
            """
            List all scoped sizing  parameters.
            """
        class list_zones_uncovered_by_controls(TUIMethod):
            """
            List all Zones not covered by scoepd sizing.
            """
        class modify(TUIMethod):
            """
            Modify scoped sizing.
            """
        class read(TUIMethod):
            """
            Read scoped sizing from a file.
            """
        class validate(TUIMethod):
            """
            Validate scoped sizing.
            """
        class write(TUIMethod):
            """
            Write scoped sizing to a file.
            """

    class server(TUIMenu):
        """
        Enter the server menu.
        """
        def __init__(self, service, version, mode, path):
            self.print_connected_grpc_clients = self.__class__.print_connected_grpc_clients(service, version, mode, path + ["print_connected_grpc_clients"])
            self.print_grpc_server_address = self.__class__.print_grpc_server_address(service, version, mode, path + ["print_grpc_server_address"])
            self.print_web_server_info = self.__class__.print_web_server_info(service, version, mode, path + ["print_web_server_info"])
            self.shutdown_grpc_server = self.__class__.shutdown_grpc_server(service, version, mode, path + ["shutdown_grpc_server"])
            self.start_grpc_server = self.__class__.start_grpc_server(service, version, mode, path + ["start_grpc_server"])
            self.start_web_server = self.__class__.start_web_server(service, version, mode, path + ["start_web_server"])
            self.stop_web_server = self.__class__.stop_web_server(service, version, mode, path + ["stop_web_server"])
            self.write_or_reset_grpc_server_info = self.__class__.write_or_reset_grpc_server_info(service, version, mode, path + ["write_or_reset_grpc_server_info"])
            super().__init__(service, version, mode, path)
        class print_connected_grpc_clients(TUIMethod):
            """
            Print connected clients.
            """
        class print_grpc_server_address(TUIMethod):
            """
            Print server address.
            """
        class print_web_server_info(TUIMethod):
            """
            No help available.
            """
        class shutdown_grpc_server(TUIMethod):
            """
            Shutdown server.
            """
        class start_grpc_server(TUIMethod):
            """
            Start gRPC server.
            """
        class start_web_server(TUIMethod):
            """
            No help available.
            """
        class stop_web_server(TUIMethod):
            """
            No help available.
            """
        class write_or_reset_grpc_server_info(TUIMethod):
            """
            Write/Reset server info.
            """

    class size_functions(TUIMenu):
        """
        Manage advanced size functions.
        """
        def __init__(self, service, version, mode, path):
            self.contours = self.__class__.contours(service, version, mode, path + ["contours"])
            self.controls = self.__class__.controls(service, version, mode, path + ["controls"])
            self.compute = self.__class__.compute(service, version, mode, path + ["compute"])
            self.create = self.__class__.create(service, version, mode, path + ["create"])
            self.create_defaults = self.__class__.create_defaults(service, version, mode, path + ["create_defaults"])
            self.delete = self.__class__.delete(service, version, mode, path + ["delete"])
            self.delete_all = self.__class__.delete_all(service, version, mode, path + ["delete_all"])
            self.disable_periodicity_filter = self.__class__.disable_periodicity_filter(service, version, mode, path + ["disable_periodicity_filter"])
            self.enable_periodicity_filter = self.__class__.enable_periodicity_filter(service, version, mode, path + ["enable_periodicity_filter"])
            self.list = self.__class__.list(service, version, mode, path + ["list"])
            self.list_periodicity_filter = self.__class__.list_periodicity_filter(service, version, mode, path + ["list_periodicity_filter"])
            self.reset_global_controls = self.__class__.reset_global_controls(service, version, mode, path + ["reset_global_controls"])
            self.set_global_controls = self.__class__.set_global_controls(service, version, mode, path + ["set_global_controls"])
            self.set_prox_gap_tolerance = self.__class__.set_prox_gap_tolerance(service, version, mode, path + ["set_prox_gap_tolerance"])
            self.set_scaling_filter = self.__class__.set_scaling_filter(service, version, mode, path + ["set_scaling_filter"])
            self.triangulate_quad_faces = self.__class__.triangulate_quad_faces(service, version, mode, path + ["triangulate_quad_faces"])
            self.use_cad_imported_curvature = self.__class__.use_cad_imported_curvature(service, version, mode, path + ["use_cad_imported_curvature"])
            super().__init__(service, version, mode, path)
        class compute(TUIMethod):
            """
            Compute Size-functions.
            """
        class create(TUIMethod):
            """
            Add size function.
            """
        class create_defaults(TUIMethod):
            """
            Creates default curvature & proximty size functions acting on all faces and edges.
            """
        class delete(TUIMethod):
            """
            Delete Size Functions.
            """
        class delete_all(TUIMethod):
            """
            Delete All Size Functions.
            """
        class disable_periodicity_filter(TUIMethod):
            """
            Disable size field periodicity.
            """
        class enable_periodicity_filter(TUIMethod):
            """
            Enable size field periodicity.
            """
        class list(TUIMethod):
            """
            List all Size function parameters.
            """
        class list_periodicity_filter(TUIMethod):
            """
            List periodic in size field.
            """
        class reset_global_controls(TUIMethod):
            """
            Reset controls for global controls.
            """
        class set_global_controls(TUIMethod):
            """
            Set controls for global controls.
            """
        class set_prox_gap_tolerance(TUIMethod):
            """
            Set proximity min gap tolerance relative to global min-size.
            """
        class set_scaling_filter(TUIMethod):
            """
            Set scaling filter on size field.
            """
        class triangulate_quad_faces(TUIMethod):
            """
            Replace non-triangular face zones with triangulated face zones during size field computation.
            """
        class use_cad_imported_curvature(TUIMethod):
            """
            Use curvature data imported from CAD.
            """

        class contours(TUIMenu):
            """
            Menu to contour of size field.
            """
            def __init__(self, service, version, mode, path):
                self.set = self.__class__.set(service, version, mode, path + ["set"])
                self.draw = self.__class__.draw(service, version, mode, path + ["draw"])
                super().__init__(service, version, mode, path)
            class draw(TUIMethod):
                """
                Draw size field contour on face zones.
                """

            class set(TUIMenu):
                """
                Set contour options.
                """
                def __init__(self, service, version, mode, path):
                    self.refine_facets = self.__class__.refine_facets(service, version, mode, path + ["refine_facets"])
                    super().__init__(service, version, mode, path)
                class refine_facets(TUIMethod):
                    """
                    Option to refine facets virtually? for better contour resolution.
                    """

        class controls(TUIMenu):
            """
            Menu to control different behavior of sf.
            """
            def __init__(self, service, version, mode, path):
                self.curvature_method = self.__class__.curvature_method(service, version, mode, path + ["curvature_method"])
                self.meshed_sf_behavior = self.__class__.meshed_sf_behavior(service, version, mode, path + ["meshed_sf_behavior"])
                super().__init__(service, version, mode, path)
            class curvature_method(TUIMethod):
                """
                Option to get facet curvature.
                """
            class meshed_sf_behavior(TUIMethod):
                """
                Set meshed size function processing to hard.
                """
