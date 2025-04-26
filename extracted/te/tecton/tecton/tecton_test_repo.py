from typing import Dict
from typing import List

from tecton import DataSource
from tecton import Entity
from tecton import FeatureService
from tecton import FeatureTable
from tecton import FeatureView
from tecton import Transformation
from tecton.framework.base_tecton_object import BaseTectonObject


class TestRepo:
    """
    A repository class for accessing and managing various Tecton objects.

    This class stores and provides access to FeatureViews, Entities, Data Sources,
    FeatureServices, and Transformations defined in the Feature Repository.
    """

    _feature_views: Dict[str, FeatureView] = {}
    _entities: Dict[str, Entity] = {}
    _data_sources: Dict[str, DataSource] = {}
    _feature_services: Dict[str, FeatureService] = {}
    _transformations: Dict[str, Transformation] = {}

    _type_to_collection: Dict[type, Dict[str, BaseTectonObject]] = {
        FeatureView: _feature_views,
        Entity: _entities,
        DataSource: _data_sources,
        FeatureService: _feature_services,
        Transformation: _transformations,
    }

    def __init__(self, objects: List[BaseTectonObject]):
        """
        Initialize the TestRepo with a list of Tecton objects.

        Args:
            objects (List[BaseTectonObject]): A list of Tecton objects to be stored in the repository.
        """
        for obj in objects:
            for fcoType, collection in self._type_to_collection.items():
                if isinstance(obj, fcoType):
                    collection[obj.name] = obj
                    break

    def _get_fco(self, name: str, fcoType: type) -> BaseTectonObject:
        if name in self._type_to_collection[fcoType]:
            return self._type_to_collection[fcoType][name]
        else:
            err = f"{fcoType.__name__} '{name}' not found."
            raise KeyError(err)

    def get_all_objects(self) -> List[BaseTectonObject]:
        """
        Retrieve all Tecton objects stored in the repository.

        Returns:
            List[BaseTectonObject]: A list of all stored Tecton objects.
        """
        objects = [
            tecton_obj
            for collection_values in self._type_to_collection.values()
            for name, tecton_obj in collection_values.items()
        ]
        return objects

    def get_feature_view(self, name) -> FeatureView:
        """
        Retrieve a FeatureView by name.

        Args:
            name (str): The name of the FeatureView to retrieve.

        Returns:
            FeatureView: The requested FeatureView.

        Raises:
            KeyError: If the FeatureView is not found in the repository.
        """
        return self._get_fco(name, FeatureView)

    def get_feature_table(self, name) -> FeatureTable:
        """
        Retrieve a FeatureTable by name.

        Args:
            name (str): The name of the FeatureTable to retrieve.

        Returns:
            FeatureTable: The requested FeatureTable.

        Raises:
            KeyError: If the FeatureTable is not found in the repository.
        """
        return self._get_fco(name, FeatureView)

    def get_feature_service(self, name) -> FeatureService:
        """
        Retrieve a FeatureService by name.

        Args:
            name (str): The name of the FeatureService to retrieve.

        Returns:
            FeatureService: The requested FeatureService.

        Raises:
            KeyError: If the FeatureService is not found in the repository.
        """
        return self._get_fco(name, FeatureService)

    def get_data_source(self, name) -> DataSource:
        """
        Retrieve a DataSource by name.

        Args:
            name (str): The name of the DataSource to retrieve.

        Returns:
            DataSource: The requested DataSource.

        Raises:
            KeyError: If the DataSource is not found in the repository.
        """
        return self._get_fco(name, DataSource)

    def get_transformation(self, name) -> Transformation:
        """
        Retrieve a Transformation by name.

        Args:
            name (str): The name of the Transformation to retrieve.

        Returns:
            Transformation: The requested Transformation.

        Raises:
            KeyError: If the Transformation is not found in the repository.
        """
        return self._get_fco(name, Transformation)

    def get_entity(self, name: str) -> Entity:
        """
        Retrieve an entity by name.

        :param name: The name of the Transformation to retrieve.

        :return: The requested Entity

        :raises KeyError: If the Entity is not found in the repository.
        """
        return self._get_fco(name, Entity)

    @property
    def feature_views(self):
        """Get all FeatureViews in the repository."""
        return [fv for fv in self._feature_views.values() if not isinstance(fv, FeatureTable)]

    @property
    def feature_tables(self):
        """Get all FeatureTables in the repository."""
        fts = [fv for fv in self._feature_views.values() if isinstance(fv, FeatureTable)]
        return fts

    @property
    def entities(self):
        """Get all Entities in the repository."""
        return list(self._entities.values())

    @property
    def transformations(self):
        """Get all Transformations in the repository."""
        return list(self._transformations.values())

    @property
    def feature_services(self):
        """Get all Feature Services in the repository."""
        return list(self._feature_services.values())

    @property
    def data_sources(self):
        """Get all Data Sources in the repository."""
        return list(self._data_sources.values())
