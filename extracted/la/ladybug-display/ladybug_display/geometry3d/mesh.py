# coding=utf-8
"""A mesh in 3D space with display properties."""
from __future__ import division

from ladybug_geometry.geometry3d.mesh import Mesh3D
from ladybug.color import Color

from .._base import _MeshBase
from ._base import _SingleColorModeBase3D


class DisplayMesh3D(_SingleColorModeBase3D, _MeshBase):
    """A mesh in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Mesh3D.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        display_mode: Text to indicate the display mode (surface, wireframe, etc.).
            Choose from the following. (Default: Surface).

            * Surface
            * SurfaceWithEdges
            * Wireframe
            * Points

    Properties:
        * geometry
        * color
        * display_mode
        * vertices
        * faces
        * min
        * max
        * center
        * area
        * face_areas
        * face_centroids
        * face_normals
        * vertex_normals
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, display_mode='Surface'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Mesh3D), '\
            Expected ladybug_geometry Mesh3D. Got {}'.format(type(geometry))
        _SingleColorModeBase3D.__init__(self, geometry, color, display_mode)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayMesh3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayMesh3D object.
        """
        assert data['type'] == 'DisplayMesh3D', \
            'Expected DisplayMesh3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        d_mode = data['display_mode'] if 'display_mode' in data and \
            data['display_mode'] is not None else 'Surface'
        geo = cls(Mesh3D.from_dict(data['geometry']), color, d_mode)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertices(self):
        """Get a tuple of vertices in the mesh."""
        return self._geometry.vertices

    @property
    def faces(self):
        """Get a tuple of all faces in the mesh."""
        return self._geometry.faces

    @property
    def min(self):
        """Get a Point3D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point3D for the maximum of the bounding box around the object."""
        return self._geometry.max

    @property
    def center(self):
        """Get a Point3D for the center of the bounding box around the object."""
        return self._geometry.center

    @property
    def area(self):
        """Get the area of the mesh."""
        return self._geometry.area

    @property
    def face_areas(self):
        """Get a tuple with the area of each face in the mesh."""
        return self._geometry.face_areas

    @property
    def face_centroids(self):
        """Get a tuple with the centroid of each face in the mesh."""
        return self._geometry.face_centroids

    @property
    def face_normals(self):
        """Get a tuple of Vector3D objects for all face normals."""
        return self._geometry.face_normals

    @property
    def vertex_normals(self):
        """Get a tuple of Vector3D objects for all vertex normals."""
        return self._geometry.vertex_normals

    def to_dict(self):
        """Return DisplayMesh3D as a dictionary."""
        base = {'type': 'DisplayMesh3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['display_mode'] = self.display_mode
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self):
        """Return DisplayMesh3D as an SVG Element."""
        return _MeshBase._display_mesh_to_svg(self)

    @staticmethod
    def mesh3d_to_svg(mesh, display_mode='Surface'):
        """SVG Group of Polygon elements from ladybug-geometry Mesh3D."""
        return _MeshBase._mesh_to_svg(mesh, display_mode)

    def __copy__(self):
        new_g = DisplayMesh3D(self.geometry, self.color, self.display_mode)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayMesh3D: {}'.format(self.geometry)
