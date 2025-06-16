"""
Module with classes for rendering specifications and object hierarchies
"""
from hdmf.spec.spec import AttributeSpec, LinkSpec
from hdmf.spec import GroupSpec
from hdmf.spec import DatasetSpec
from hdmf.utils import docval, getargs
import warnings


class HierarchyDescription(dict):
    """
    Dictionary data structure used to describe the contents of the specification or HDMF object hierarchy.
    This simple helper data structure was designed to ease rendering of object hierarchies but may
    be useful for other purposes as well.

    Ultimately, this is a flattened version of a spec or namespace where all datasets, groups, attributes,
    and links are sorted into flat lists of dicts. The nesting of the objects is then described via
    a list of relationships between the objects. Each object has a unique name that is determined
    by the full path to the object plus the actual name or type of the object.

    TODO Instead of using our own dict datastructures to describe datasets, groups etc. we should use
         the standard spec datastructures provided by HDMF
    """
    RELATIONSHIP_TYPES = {'managed_by': 'Object managed by',
                          'link': 'Object links to',
                          'attribute_of': 'Object is attribute of'}

    def __init__(self):
        super(HierarchyDescription, self).__init__()
        super(HierarchyDescription, self).__setitem__('datasets', [])
        super(HierarchyDescription, self).__setitem__('groups', [])
        super(HierarchyDescription, self).__setitem__('attributes', [])
        super(HierarchyDescription, self).__setitem__('relationships', [])
        super(HierarchyDescription, self).__setitem__('links', [])

    def __setitem__(self, key, value):
        raise ValueError("Explicit setting of objects not allowed. Use the add_* functions to add objects")

    def add_dataset(self, name, shape=None, dtype=None, data_type=None, size=None):
        """
        Add a dataset to the description

        :param name: Name of the dataset (full path)
        :param shape: Shape of the dataset
        :param dtype: Data type of the data
        :param data_type: object data_type (e.g., NWB neurodata_type)
        """
        self['datasets'].append({
            'name': name,
            'shape': shape,
            'dtype': dtype,
            'data_type': data_type,
            'size': size
        })

    def add_group(self, name, data_type=None):
        """
        Add a group to the description

        :param name: Name of the group (full path)
        :param data_type: object data type (e.g., NWB neurodata type)
        """
        self['groups'].append({
            'name': name,
            'data_type': data_type
        })

    def add_attribute(self, name, value, size=None):
        """
        Add an attribute

        :param name: Name of the attribute (Full name, including the path of the parent object)
        :param value: Value of the attribute
        :return:
        """
        self['attributes'].append({
            'name': name,
            'value': value,
            'size': size
        })

    def add_link(self, name, target_type):
        """
        Add a link

        :param name: Name of the link (full path)
        :param target_type: Type of object the link points to.
        """
        self['links'].append({'name': name,
                              'target_type': target_type})

    def add_relationship(self, source, target, name, rtype):
        """
        Add a relationship between two objects

        :param source: Name of the source object (full path)
        :param target: Name of the target object (full path)
        :param name: Name of the relationship
        :param rtype: Type of the relationship
        """
        self['relationships'].append({
            'source': source,
            'target': target,
            'name': name,
            'type': rtype
        })

    @classmethod
    def from_spec(cls, spec):
        """
        Traverse the spec to compute spec related hierarchy data.
        :param spec: The specification object
        :type spec: GroupSpec, AttributeSpec, DatasetSpec
        :return: Instance of HierarchyDescription with the hierarchy of the objects
        """
        import os

        specstats = cls()

        def update_stats(obj, parent_name):
            """
            Function used to recursively visit all items in a stat and update the specstats object
            :param obj: The spec for the object
            :param parent_name: String with the full path of the parent in the hierarchy
            """
            type_def_key = obj.def_key() if hasattr(obj, 'def_key') else 'data_type'
            type_inc_key = obj.inc_key() if hasattr(obj, 'inc_key') else 'data_type'
            obj_main_name = obj.name \
                if obj.get('name', None) is not None \
                else obj.get(type_def_key, None) \
                if obj.get(type_def_key, None) is not None \
                else obj.get(type_inc_key, None) \
                if obj.get(type_inc_key, None) is not None \
                else obj['target_type']
            if obj.get('name', None) is None:
                obj_main_name = '<' + obj_main_name + '>'
            obj_name = os.path.join(parent_name, obj_main_name)

            if isinstance(obj, GroupSpec):
                type_def_key = obj.def_key()
                type_inc_key = obj.inc_key()
                if obj.get(type_def_key, None) is not None:
                    ndt = obj[type_def_key]
                else:
                    ndt = obj.get(type_inc_key, None)
                specstats.add_group(name=obj_name,
                                    data_type=ndt)
            elif isinstance(obj, DatasetSpec):
                type_def_key = obj.def_key()
                type_inc_key = obj.inc_key()
                if obj.get(type_def_key, None) is not None:
                    ndt = obj[type_def_key]
                else:
                    ndt = obj.get(type_inc_key, None)
                specstats.add_dataset(name=obj_name,
                                      shape=obj.shape,
                                      dtype=obj['type'] if hasattr(obj, 'type') else None,
                                      data_type=ndt)
            elif isinstance(obj, AttributeSpec):
                specstats.add_attribute(name=obj_name,
                                        value=obj.value)
            elif isinstance(obj, LinkSpec):
                specstats.add_link(name=obj_name,
                                   target_type=obj['target_type'])

            # Recursively add all groups and datasets
            if isinstance(obj, GroupSpec):
                for d in obj.datasets:
                    dn = update_stats(d, obj_name)
                    specstats.add_relationship(source=obj_name,
                                               target=dn,
                                               name=dn+"_managed_by_"+obj_name,
                                               rtype='managed_by')
                for g in obj.groups:
                    gn = update_stats(g, obj_name)
                    specstats.add_relationship(source=obj_name,
                                               target=gn,
                                               name=gn+"_managed_by_"+obj_name,
                                               rtype='managed_by')
                for link in obj.links:
                    ln = update_stats(link, obj_name)
                    specstats.add_relationship(source=obj_name,
                                               target=ln,
                                               name=ln+"_managed_by_"+obj_name,
                                               rtype='managed_by')
            if isinstance(obj, GroupSpec) or isinstance(obj, DatasetSpec):
                for a in obj.attributes:
                    an = update_stats(a, obj_name)
                    specstats.add_relationship(source=obj_name,
                                               target=an,
                                               name=an+"_attribute_of_"+obj_name,
                                               rtype='attribute_of')
            return obj_name

        update_stats(spec, parent_name='/')
        return specstats

    @classmethod
    def from_hdf5(cls, hdf_object, root='/', data_type_attr_name='neurodata_type'):
        """
        Traverse the file to compute file object hierarchy data.

        :param hdf_object: The h5py.Group or h5py.File object. If a string is given then the function assumes
                           that this is a path to and HDF5 file and will open the file.
        :param root: String indicating the root object starting from which we should compute the file statistics.
                     Default value is "/", i.e., starting from the root itself
        :type root: String
        :param data_type_attr_name: Name of the attribute in the HDF5 file reserved for storing the name of
                                    object types, e.g., the neurodata_type in the case of NWB:N. Default is
                                    'neurodata_type' with NWB in mind.

        :return: Instance of HierarchyDescription with the hierarchy of the objects

        """
        import h5py
        import os

        filestats = cls()

        def update_stats(name, obj):
            """
            Callback function used in conjunction with the visititems function to compile
            statistics for the file

            :param name: the name of the object in the file
            :param obj: the hdf5 object itself
            """
            obj_name = os.path.join(root, name)
            # Group and dataset metadata
            if isinstance(obj, h5py.Dataset):
                ntype = None
                if data_type_attr_name in obj.attrs.keys():
                    ntype = obj.attrs[data_type_attr_name][:]

                filestats.add_dataset(name=obj_name,
                                      shape=obj.shape,
                                      dtype=obj.dtype,
                                      data_type=ntype,
                                      size=obj.size * obj.dtype.itemsize)
            elif isinstance(obj, h5py.Group):
                ntype = None
                if data_type_attr_name in obj.attrs.keys():
                    ntype = obj.attrs[data_type_attr_name][:]
                filestats.add_group(name=obj_name, data_type=ntype)
                # visititems does not visit any links. We need to add them here
                for objkey in obj.keys():
                    objval = obj.get(objkey, getlink=True)
                    if isinstance(objval, h5py.SoftLink) or isinstance(objval, h5py.ExternalLink):
                        try:
                            linktarget = obj[objkey]
                            if data_type_attr_name in linktarget.attrs.keys():
                                targettype = linktarget.attrs[data_type_attr_name][:]
                            else:
                                targettype = str(type(linktarget))
                        except KeyError:
                            warnings.warn('Unable to determine target type of link %s, %s' % ((obj_name, objkey)))
                            targettype = 'undefined'
                        linkname = os.path.join(obj_name, objkey)
                        filestats.add_link(linkname, target_type=targettype)
                        if isinstance(objval, h5py.SoftLink):
                            filestats.add_relationship(source=linkname,
                                                       target=objval.path,
                                                       name=linkname,
                                                       rtype='link')
            # Visit all attributes of the object
            for attr_name, attr_value in obj.attrs.items():
                attr_path = os.path.join(obj_name, attr_name)
                try:
                    size = attr_value.size * attr_value.dtype.itemsize
                except:
                    size = None
                filestats.add_attribute(name=attr_path, value=attr_value, size=size)
                filestats.add_relationship(source=attr_path,
                                           target=obj_name,
                                           name=attr_name + '_attribute_of_' + obj_name,
                                           rtype='attribute_of')

            # Create the relationship for the object
            if obj_name != '/':
                filestats.add_relationship(source=os.path.dirname(obj_name),
                                           target=obj_name,
                                           name=obj_name + '_managed_by_' + root,
                                           rtype='managed_by')
        # Determine the main HDF5 object
        if isinstance(hdf_object, str):
            main_hdf_object = h5py.File(hdf_object, 'r')
            close_main_hdf_object = True
        else:
            main_hdf_object = hdf_object
            close_main_hdf_object = False

        # Visit all items in the hdf5 object to compile the object statistics
        main_hdf_object[root].visititems(update_stats)
        if root == '/':
            update_stats(name='/', obj=main_hdf_object['/'])

        # Close the hdf5 object if we opened it
        if close_main_hdf_object:
            main_hdf_object.close()
            del main_hdf_object

        # Return the results
        return filestats


class NXGraphHierarchyDescription(object):
    """
    Description of the object hierarchy as an nx graph
    """

    @docval({'name': 'data', 'type': HierarchyDescription, 'doc': 'Data of the hierarchy'},
            {'name': 'include_groups', 'type': bool,
             'doc': 'Bool indicating whether we should include groups in the hierarchy', 'default': True},
            {'name': 'include_datasets', 'type': bool,
             'doc': 'Bool indicating whether we should include datasets in the hierarchy', 'default': True},
            {'name': 'include_attributes', 'type': bool,
             'doc': 'Bool indicating whether we should include attributes in the hierarchy', 'default': True},
            {'name': 'include_links', 'type': bool,
             'doc': 'Bool indicating whether we should include links in the hierarchy', 'default': True},
            {'name': 'include_relationships', 'type': bool,
             'doc': 'Bool or list of strings indicating thh types of relationships to be included', 'default': True})
    def __init__(self, **kwargs):
        self.data, self.include_groups, self.include_datasets, self.include_attributes, \
            self.include_links, self.include_relationships = getargs('data', 'include_groups',
                                                                     'include_datasets', 'include_attributes',
                                                                     'include_links', 'include_relationships',
                                                                     kwargs)
        self.graph = self.nxgraph_from_data(self.data,
                                            self.include_groups,
                                            self.include_datasets,
                                            self.include_attributes,
                                            self.include_links,
                                            self.include_relationships)
        self.pos = self.create_hierarchical_graph_layout(self.graph)

    def draw(self, **kwargs):
        """
        Draw the graph using the draw_graph method
        :param kwargs: Additional keyword arguments to be passed to the static draw_graph method
        :return:
        """
        return self.draw_graph(graph=self.graph, pos=self.pos, data=self.data, **kwargs)

    @staticmethod
    def nxgraph_from_data(data,
                          include_groups=True,
                          include_datasets=True,
                          include_attributes=True,
                          include_links=True,
                          include_relationships=True):
        """
        Create a networkX representation of the objects in the HiearchyDescription stored in self.data

        :param data: Description of the object hierarchy
        :type data: HierarchyDescription
        :param include_groups: Bool indicating whether we should include groups in the hierarchy
        :param include_datasets: Bool indicating whether we should include datasets in the hierarchy
        :param include_attributes: Bool indicating whether we should include groups in the hierarchy
        :param include_links: Bool indicating whether we should include links in the hierarchy
        :param include_relationships: Bool or list of strings indicating which types of relationships should be included

        :return:  NXGraph from self.data
        """
        import networkx as nx

        graph = nx.Graph()  # nx.MultiDiGraph()
        # Add all nodes
        if include_datasets:
            for d in data['datasets']:
                graph.add_node(d['name'])
        if include_groups:
            for g in data['groups']:
                graph.add_node(g['name'])
        if include_attributes:
            for g in data['attributes']:
                graph.add_node(g['name'])
        if include_links:
            for link in data['links']:
                graph.add_node(link['name'])

        # Create edges from relationships
        rel_list = include_relationships \
            if isinstance(include_relationships, list) \
            else data.RELATIONSHIP_TYPES \
            if include_relationships is True \
            else []
        all_nodes = graph.nodes(data=False)
        if len(rel_list) > 0:
            for r in data['relationships']:
                # Add only those relationships we were asked to include
                if r['type'] in rel_list:
                    # Add only relationships for which we have both the source and target in the graph
                    if r['source'] in all_nodes and r['target'] in all_nodes:
                        graph.add_edge(r['source'], r['target'])
        return graph

    @staticmethod
    def create_hierarchical_graph_layout(graph):
        """
        Given a networkX graph of file hierarchy, comput the positions of all nodes of the
        graph (i.e., groups and datasets) in a hierarchical layout

        :param graph: Network X graph of file objects

        :return: Dictionary where the keys are the names of the nodes in the graph and the values are
                 tuples with the floating point x and y coordinates for that node.
        """

        import numpy as np

        pos_hierarchy = {}
        allnodes = graph.nodes(data=False)
        nodes_at_level = {}
        for v in allnodes:
            xpos = len(v.split('/')) if v != '/' else 1
            try:
                nodes_at_level[xpos] += 1
            except KeyError:
                nodes_at_level[xpos] = 1

        curr_nodes_at_level = {i: 0 for i in nodes_at_level.keys()}
        for v in np.sort(list(allnodes)):
            xpos = len(v.split('/')) if v != '/' else 1
            ypos = 1 - float(curr_nodes_at_level[xpos]) / nodes_at_level[xpos] * 1
            curr_nodes_at_level[xpos] += 1
            pos_hierarchy[v] = np.asarray([np.power(xpos, 2), ypos])

        return pos_hierarchy

    @staticmethod
    def create_warped_hierarchial_graph_layout(graph):
        """
        Given a networkX graph of file hierarchy, compute the positions of all nodes of the
        graph (i.e., groups and datasets) in a hierarchical layout where the levels of the
        hierarchy are warped to follow a semi-circle shape.

        :param graph: Network X graph of file objects

        :return: Dictionary where the keys are the names of the nodes in the graph and the values are
                 tuples with the floating point x and y coordinates for that node.
        """
        import numpy as np

        pos_hierarchy = {}
        allnodes = graph.nodes(data=False)
        nodes_at_level = {}
        for v in allnodes:
            xpos = len(v.split('/')) if v != '/' else 1
            try:
                nodes_at_level[xpos] += 1
            except KeyError:
                nodes_at_level[xpos] = 1

        curr_nodes_at_level = {i: 0 for i in range(7)}
        for i, v in enumerate(np.sort(allnodes)):
            xpos = len(v.split('/')) if v != '/' else 1
            ypos = float(curr_nodes_at_level[xpos]) / nodes_at_level[xpos]
            curr_nodes_at_level[xpos] += 1
            if xpos > 3:
                xpos += np.sin(ypos*np.pi)
            xpos = np.power(xpos, 2)
            pos_hierarchy[v] = np.asarray([xpos, -ypos])

        return pos_hierarchy

    @staticmethod
    def normalize_graph_layout(graph_layout):
        """
        Normalize the positions in the given graph layout so that the x and y
        values have a range of [0,1]
        :param graph_layout: Dict where the keys are the names of the nodes in the graph
               and the values are tuples with the (x,y) locations for the nodes
        :return: New graph layout with normalized coordinates
        """
        import numpy as np

        # Compute positions stats
        xpos = np.asarray([i[0] for i in graph_layout.values()])
        ypos = np.asarray([i[1] for i in graph_layout.values()])
        xmin = xpos.min()
        xmax = xpos.max()
        xr = xmax - xmin
        ymin = ypos.min()
        ymax = ypos.max()
        yr = ymax - ymin

        # Create the output layout
        normlized_layout = {k: np.asarray([(n[0] - xmin) / xr, (n[1] - xmin) / yr]) for k, n in graph_layout.items()}
        return normlized_layout

    def suggest_xlim(self):
        """
        Suggest xlimits for plotting
        :return: Tuple with min/max x values
        """
        import numpy as np

        xpos = np.asarray([i[0] for i in self.pos.values()])
        xmin = xpos.min()
        xmax = xpos.max()
        xrange = np.abs(xmax-xmin)
        xmin -= xrange*0.2
        xmax += xrange*0.2
        return (xmin, xmax)

    def suggest_ylim(self):
        """
        Suggest ylimits for plotting
        :return: Tuple with min/max x values
        """
        import numpy as np

        ypos = np.asarray([i[1] for i in self.pos.values()])
        ymin = ypos.min()
        ymax = ypos.max()
        yrange = np.abs(ymax-ymin)
        ymin -= yrange*0.1
        ymax += yrange*0.1
        return (ymin, ymax)

    def suggest_figure_size(self):
        """
        Suggest a figure size for a graph based on the number of rows and columns in the hierarchy
        :param graph: Network X graph of file objects
        :return: Tuple with the width and height for the figure
        """
        allnodes = self.graph.nodes(data=False)
        nodes_at_level = {}
        for v in allnodes:
            xpos = len(v.split('/')) if v != '/' else 1
            try:
                nodes_at_level[xpos] += 1
            except KeyError:
                nodes_at_level[xpos] = 1
        num_rows = max([v for v in nodes_at_level.values()])
        # num_cols = len(nodes_at_level)
        # w = num_cols + 1.5
        # h = num_rows * 0.5 + 1.5
        w = 8
        h = min(num_rows*0.75, 8)
        return (w, h)

    @staticmethod
    def draw_graph(graph,
                   pos,
                   data,
                   show_labels=True,
                   relationship_types=None,
                   figsize=None,
                   label_offset=(0.0, 0.012),
                   label_font_size=8,
                   xlim=None,
                   ylim=None,
                   legend_location='lower left',
                   axis_on=False,
                   relationship_counts=True,
                   show_plot=True,
                   relationship_colors=None,
                   relationship_alpha=0.7,
                   node_colors=None,
                   node_alpha=1.0,
                   node_shape='o',
                   node_size=20):
        """
        Helper function used to render the file hierarchy and the inter-object relationships

        :param graph: The networkx graph
        :param pos: Dict with the position for each node generated, e.g., via nx.shell_layout(graph)
        :param data: Data about the hierarchy
        :type data: HierarchyDescription
        :param show_labels: Boolean indicating whether we should show the names of the nodes
        :param relationship_types: List of edge types that should be rendered. If None, then all edges will be rendered.
        :param figsize: The size of the matplotlib figure
        :param label_offset: Offsets for the node labels. This may be either: i) None (default),
                   ii) Tuple with constant (x,y) offset for the text labels, or
                   iii) Dict of tuples where the keys are the names of the nodes for which labels should be moved
                        and the values are the (x,y) offsets for the given nodes.
        :param label_font_size: Font size for the labels
        :param xlim: The x limits to be used for the plot
        :param ylim: The y limits to be used for the plot
        :param legend_location: The legend location (e.g., 'upper left' , 'lower right')
        :param axis_on: Boolean indicating whether the axes should be turned on or not.
        :param relationship_counts: Boolean indicating if edge/relationship counts should be shown.
        :param relationship_colors: Optional dict for changing the default colors used for drawing relationship edges.
            The keys of the dict are the type of relationship and the values are the names of the colors. This may
            also be a single color string in case that all relationships should be shown in the same color. Default
            behavior is:

               ```{'shared_encoding': 'magenta',
                  'indexes_values': 'cyan',
                  'equivalent': 'gray',
                  'indexes': 'orange',
                  'user': 'green',
                  'shared_ascending_encoding': 'blue',
                  'order': 'red',
                  'managed_by': 'steelblue',
                  'attribute_of': 'black'}```

        :param relationship_alpha: Float alpha value in the range of [0,1] with the alpha value to be used
            for relationship edges. This may also be a dict of per-relationship-typ alpha values, similar
            to relationship_colors.
        :param node_colors: Dict with the color strings of the different node types. This may also be a single
                string in case that the same color should be used for all node types. Default behavior is:

                ```{'typed_dataset': 'blue',
                    'untyped_dataset': 'lightblue',
                    'typed_group': 'red',
                    'untyped_group': 'orange',
                    'attribute': 'gray',
                    'link': 'white'}```

        :param node_shape: Dict indicating the shape string for each node type. This may also be a single string
               if the same shape should be used for all node types. Default='o'
        :param node_size:  Dict indicating the integer size for each node type. This may also be a single int
               if the same size should be used for all node types. Default='o'
        :param show_plot: If true call show to display the figure. If False return the matplotlib figure
                          without showing it.

        :return: Matplotlib figure of the data

        """
        from matplotlib import pyplot as plt
        import networkx as nx
        import os
        from copy import deepcopy
        from matplotlib.ticker import NullLocator

        fig = plt.figure(figsize=figsize)
        # List of object names
        all_nodes = graph.nodes(data=False)
        n_names = {'typed_dataset': [i['name'] for i in data['datasets']
                                     if i['data_type'] is not None and i['name'] in all_nodes],
                   'untyped_dataset': [i['name'] for i in data['datasets']
                                       if i['data_type'] is None and i['name'] in all_nodes],
                   'typed_group': [i['name'] for i in data['groups']
                                   if i['data_type'] is not None and i['name'] in all_nodes],
                   'untyped_group': [i['name'] for i in data['groups']
                                     if i['data_type'] is None and i['name'] in all_nodes],
                   'attribute': [i['name'] for i in data['attributes']
                                 if i['name'] in all_nodes],
                   'link': [i['name'] for i in data['links']
                            if i['name'] in all_nodes]
                   }
        # Define the legend labels
        n_legend = {'typed_dataset': 'Typed Dataset (%i)' % len(n_names['typed_dataset']),
                    'untyped_dataset': 'Untyped Dataset (%i)' % len(n_names['untyped_dataset']),
                    'typed_group': 'Typed Group (%i)' % len(n_names['typed_group']),
                    'untyped_group': 'Untyped Group (%i)' % len(n_names['untyped_group']),
                    'attribute': 'Attributes (%i)' % len(n_names['attribute']),
                    'link': 'Links (%i)' % len(n_names['link'])}

        # Define the node colors
        n_colors = {'typed_dataset': 'blue',
                    'untyped_dataset': 'lightblue',
                    'typed_group': 'red',
                    'untyped_group': 'orange',
                    'attribute': 'gray',
                    'link': 'white'}

        if node_colors is not None:
            node_colors.update(node_colors)
        # Define the node alpha
        n_alpha_base = node_alpha if isinstance(node_alpha, float) else 1.0
        n_alpha = {k: n_alpha_base for k in n_colors}
        if isinstance(node_alpha, dict):
            n_alpha.update(node_alpha)
        # Define the shape of each node type
        n_shape_base = node_shape if isinstance(node_alpha, float) else 'o'
        n_shape = {k: n_shape_base for k in n_colors}
        if isinstance(node_shape, dict):
            n_shape.update(node_shape)
        # Define the size of each node type
        n_size_base = node_size if isinstance(node_size, float) or isinstance(node_size, int) else 20
        n_size = {k: n_size_base for k in n_colors}
        if isinstance(node_size, dict):
            n_size.update(node_size)

        # Draw all the nodes by type with the type-specific properties
        for ntype in n_names.keys():
            # Draw the typed dataset nodes of the network
            nx.draw_networkx_nodes(graph, pos,
                                   nodelist=n_names[ntype],
                                   node_color=n_colors[ntype],
                                   node_shape=n_shape[ntype],
                                   node_size=n_size[ntype],
                                   alpha=n_alpha[ntype],
                                   label=n_legend[ntype])

        # Define edge colors and alpha values
        rel_colors = {'shared_encoding': 'magenta',
                      'indexes_values': 'cyan',
                      'equivalent': 'gray',
                      'indexes': 'orange',
                      'user': 'green',
                      'shared_ascending_encoding': 'blue',
                      'order': 'lightblue',
                      'managed_by': 'steelblue',
                      'link': 'magenta',
                      'attribute_of': 'black'}
        if isinstance(relationship_colors, str):
            for k in rel_colors:
                rel_colors[k] = relationship_colors
        if relationship_colors is not None:
            rel_colors.update(relationship_colors)
        rel_base_alpha = 0.6 if not isinstance(relationship_alpha, float) else relationship_alpha
        rel_alpha = {k: rel_base_alpha for k in rel_colors}
        if isinstance(relationship_alpha, dict):
            rel_alpha.update(relationship_alpha)
        # Resort edges by type
        edge_by_type = {}
        for r in data['relationships']:
            if r['type'] in edge_by_type:
                edge_by_type[r['type']].append((r['source'], r['target']))
            else:
                edge_by_type[r['type']] = [(r['source'], r['target'])]
        # Determine the counts of relationships, i.e., how many relationships of each type do we have
        if relationship_counts:
            relationship_counts = {rt: len(rl) for rt, rl in edge_by_type.items()}
        else:
            relationship_counts = None
        # Draw the network edges
        for rt, rl in edge_by_type.items():
            if relationship_types is None or rt in relationship_types:
                try:
                    edge_label = rt if relationship_counts is None else (rt+' (%i)' % relationship_counts[rt])
                    nx.draw_networkx_edges(graph,
                                           pos,
                                           edgelist=rl,
                                           width=1.0,
                                           alpha=rel_alpha[rt],
                                           edge_color=rel_colors[rt],
                                           arrows=False,
                                           style='solid' if rt != 'link' else 'dashed',
                                           label=edge_label
                                           )
                except KeyError:
                    pass

        if show_labels:
            # Create node labels
            labels = {i: os.path.basename(i) if len(os.path.basename(i)) > 0 else i for i in graph.nodes(data=False)}
            # Determine label positions
            if label_offset is not None:
                # Move individual labels by the user-defined offsets
                if isinstance(label_offset, dict):
                    label_pos = deepcopy(pos)
                    for k, v in label_offset.items():
                        label_pos[k] += v
                # Move all labels by a single, user-defined offset
                else:
                    label_pos = {k: (v+label_offset) for k, v in pos.items()}
            else:
                # Use the node positions as label positions
                label_pos = pos
            # Draw the labels
            nx.draw_networkx_labels(graph, label_pos, labels, font_size=label_font_size)

        if axis_on:
            plt.axis('on')
        else:
            plt.axis('off')
            # Get rid of large whitespace around the figure
            plt.gca().xaxis.set_major_locator(NullLocator())
            plt.gca().yaxis.set_major_locator(NullLocator())
        plt.legend(prop={'size': label_font_size}, loc=legend_location)
        plt.autoscale(True)
        plt.tight_layout()
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        if show_plot:
            plt.show()
        return fig
