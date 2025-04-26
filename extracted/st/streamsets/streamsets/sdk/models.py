# Copyright 2019 StreamSets Inc.

"""Models to be used by multiple StreamSets components."""

# fmt: off
import json
import warnings
from uuid import uuid4

import inflection

# fmt: on

json_to_python_style = lambda x: inflection.underscore(x)
python_to_json_style = lambda x: inflection.camelize(x, uppercase_first_letter=False)


class Configuration:
    """Abstraction for configurations.

    This class enables easy access to and modification of data stored as a list of dictionaries. A Configuration is
    stored in the form:

    .. code-block:: none

        [{"name" : "<name_1>","value" : "<value_1>"}, {"name" : "<name_2>", value" : "<value_2>"},...]

    However, the passed in configuration parameter can be a list of Configurations such as:

    .. code-block:: none

        [[{"name" : "<name_1>","value" : "<value_1>"}, {"name" : "<name_2>", value" : "<value_2>"},...],
        [{"name" : "<name_3>","value" : "<value_3>"}, {"name" : "<name_4>", value" : "<value_4>"},...],...]

    Args:
        compatibility_map (:obj:`dict`, optional): A dictionary mapping values used for backwards compatibility.
        configuration (:obj:`list`): List of configurations (see above for format).
        property_key (:obj:`str`, optional): The dictionary entry denoting the property key.
            Default: ``name``
        property_value (:obj:`str`, optional): The dictionary entry denoting the property value.
            Default: ``value``
        update_callable (optional): A callable to which ``self._data`` will be passed as part of ``__setitem__``.
        update_callable_kwargs (:obj:`dict`, optional): A dictionary of kwargs to pass (along with a body)
            to the callable.
        id_to_remap (:obj:`dict`, optional): A dictionary mapping configuration IDs to human-readable container keys.
                                             Example: {'custom_region':'googleCloudConfig.customRegion', ... }
    """

    # Use an uber secret class attribute to specify whether other attributes can be assigned by __setattr__.
    __frozen = False

    def __init__(
        self,
        configuration=None,
        compatibility_map=None,
        property_key='name',
        property_value='value',
        update_callable=None,
        update_callable_kwargs=None,
        id_to_remap=None,
    ):
        # Apply overrides to initial data
        if compatibility_map:
            for configuration_entry in configuration:
                configuration_name = configuration_entry.get(property_key)
                configuration_value = configuration_entry.get(property_value)

                if configuration_name in compatibility_map:
                    overrides = compatibility_map[configuration_name]
                    override_values = overrides.get('values', {})

                    configuration_entry[property_key] = overrides['name']

                    if configuration_value in override_values:
                        configuration_entry[property_value] = override_values[configuration_value]
                        warnings.warn(
                            'Configuration {}={} has been deprecated. Please use {}={} instead.'.format(
                                configuration_name,
                                configuration_value,
                                overrides['name'],
                                override_values[configuration_value],
                            ),
                            DeprecationWarning,
                        )
                    else:
                        warnings.warn(
                            'Configuration {} has been deprecated. Please use {} instead.'.format(
                                configuration_name, overrides['name']
                            ),
                            DeprecationWarning,
                        )

        self._compatibility_map = compatibility_map or {}
        self.property_key = property_key
        self.property_value = property_value

        self._id_to_remap = id_to_remap or {}
        self._update_callable = update_callable
        self._update_callable_kwargs = update_callable_kwargs or {}

        # Ensure the input 'configuration' is properly formatted, handling both single configurations and lists.
        self._data = [configuration] if isinstance(configuration[0], dict) else configuration
        self._configuration_index_map = self._create_configuration_index_map()

        self.__frozen = True

    def _create_configuration_index_map(self):
        """
        Creates a mapping {config_item_name: (config_item_index, config_list_index)} for efficient lookups.
        This method facilitates quick identification of the index of a configuration item within the
        Configurations/self._data list.

        Here,
        1. config_list_index is the index within the Configurations list, i.e. the outer index.
        2. config_item_index is the index within an individual Configuration, i.e. the inner index.

        If our ._data is as follows:
            [[{"name" : "<name_1>","value" : "<value_1>"}, {"name" : "<name_2>", value" : "<value_2>"}],
            [{"name" : "<name_3>","value" : "<value_3>"}, {"name" : "<name_4>", value" : "<value_4>"}]]

        Then configuration_index_map would be returned as:
            {<name_1>:(0,0), <name_2>:(1,0),, <name_3>:(0,1),, <name_4>:(1,1),}

        Returns:
            A configuration index map (:obj:`dict`).

        Raises:
            TypeError: If the input data structure is not a list of configurations,
                       if a Configuration is not a list of dictionaries, or
                       if a Configuration does not contain the specified property_key and property_value.
        """
        configuration_index_map = {}
        for config_list_index, config_list in enumerate(self._data):
            if not isinstance(config_list, list):
                raise TypeError('Please pass in a list of configurations')

            for config_item_index, config_item in enumerate(config_list):
                if not isinstance(config_item, dict):
                    raise TypeError('A Configuration must be a list of dictionaries')
                if self.property_key not in config_item or self.property_value not in config_item:
                    raise TypeError(
                        'Configuration {} does not contain property_key:{} or property_value:{}'.format(
                            config_item, self.property_key, self.property_value
                        )
                    )
                configuration_index_map[config_item[self.property_key]] = (config_item_index, config_list_index)

        return configuration_index_map

    def __getattr__(self, key):
        if not self.__frozen:
            super().__getattr__(key)
            return

        return self.__getitem__(key)

    def __getitem__(self, key):
        if key in self._id_to_remap:
            key = self._id_to_remap[key]

        if key not in self._configuration_index_map:
            raise AttributeError(key)

        index, configuration_index = self._configuration_index_map[key]
        config = self._data[configuration_index][index]
        return self._convert_value(config)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if not self.__frozen:
            super().__setattr__(key, value)
            return

        if key in self._id_to_remap:
            key = self._id_to_remap[key]

        if key in self._compatibility_map:
            overrides = self._compatibility_map[key]
            if 'values' in overrides and value in self._compatibility_map[key]['values']:
                warnings.warn(
                    'Deprecation warning: Configuration {}={} is deprecated on this engine version. '
                    'Updating value to {}={}.'.format(key, value, overrides['name'], overrides['values'][value]),
                    DeprecationWarning,
                )
                value = overrides['values'][value]
            else:
                warnings.warn(
                    'Configuration {} has been deprecated. Please use {} instead.'.format(key, overrides['name']),
                    DeprecationWarning,
                )

            key = overrides['name']

        if key not in self._configuration_index_map:
            raise AttributeError(key)

        index, configuration_index = self._configuration_index_map[key]
        config = self._data[configuration_index][index]

        config[self.property_value] = value
        if self._update_callable:
            kwargs = dict(body=[config])
            kwargs.update(self._update_callable_kwargs)
            self._update_callable(**kwargs)

    def __contains__(self, item):
        return item in self._id_to_remap or item in self._configuration_index_map

    def __repr__(self):
        configs = {}
        for configuration in self._data:
            for config in configuration:
                key = config[self.property_key]
                configs[key] = self._convert_value(config)

        # If a key has a remapped key, delete the original key and add the remapped key into configs
        for remapped_key, original_key in self._id_to_remap.items():
            if original_key != remapped_key and original_key in configs:
                configs[remapped_key] = configs[original_key]
                del configs[original_key]

        return '{{{}}}'.format(', '.join("'{}': {}".format(k, v) for k, v in configs.items()))

    def __dir__(self):
        # Stripping out any values that have multiple words in it. Example: 'Organization account type'
        # in sch_models.Organization.configuration
        id_to_remap_cleaned = [key for key in self._id_to_remap.keys() if ' ' not in key]
        return sorted(list(dir(object)) + list(self.__dict__.keys()) + id_to_remap_cleaned)

    def items(self):
        """Gets the configuration's items.

        Returns:
            A new view of the configuration’s items ((key, value) pairs).
        """
        # To keep the behavior in line with a Python dict's, we'll generate one and then use its items method.
        configuration_dict = {}
        for configuration in self._data:
            for config in configuration:
                configuration_dict[config[self.property_key]] = self._convert_value(config)

        for config_property in self._id_to_remap:
            key = self._id_to_remap[config_property]
            if key in configuration_dict:
                configuration_dict[config_property] = configuration_dict[key]
                del configuration_dict[key]
        return configuration_dict.items()

    def get(self, key, default=None):
        """Return the value of key or, if not in the configuration, the default value."""
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, configs):
        """Update instance with a collection of configurations.

        Args:
            configs (:obj:`dict`): Dictionary of configurations to use.
        """
        for key, value in configs.items():
            self[key] = value

    def _convert_value(self, config):
        if config.get('type') == 'boolean':
            return json.loads(config[self.property_value])
        elif config.get('type') == 'integer':
            return int(config[self.property_value])
        else:
            return config[self.property_value]


class BaseModel:
    """Base class for StreamSets Accounts models that essentially just wrap a dictionary.

    Args:
        data (:obj:`dict`): The underlying JSON representation of the model.
        attributes_to_ignore (:obj:`list`, optional): A list of string attributes to mask from being handled
            by this class' __setattr__ method. Default: ``None``.
        attributes_to_remap (:obj:`dict`, optional): A dictionary of attributes to remap with the desired attributes
            as keys and the corresponding property name in the JSON representation as values. Default: ``None``.
        repr_metadata (:obj:`list`, optional): A list of attributes to use in the model's __repr__ string.
            Default: ``None``.
    """

    def __new__(cls, *args, **kwargs):
        instance = super(BaseModel, cls).__new__(cls)
        super(BaseModel, instance).__setattr__('_data_internal', {})
        super(BaseModel, instance).__setattr__('_attributes_to_ignore', [])
        super(BaseModel, instance).__setattr__('_attributes_to_remap', {})
        super(BaseModel, instance).__setattr__('_repr_metadata', [])

        return instance

    def __init__(self, data, attributes_to_ignore=None, attributes_to_remap=None, repr_metadata=None):
        # _data_internal is introduced to  help inherited classes that need to load _data when _data is accessed
        # eg. Pipeline
        super().__setattr__('_data_internal', data)
        super().__setattr__('_attributes_to_ignore', attributes_to_ignore or [])
        super().__setattr__('_attributes_to_remap', attributes_to_remap or {})
        super().__setattr__('_repr_metadata', repr_metadata or [])

    # By default these properties don't do anything by can be overrided by inherited classes to load something
    @property
    def _data_internal(self):
        return self.__dict__['_data'] if '_data' in self.__dict__ else None

    @_data_internal.setter
    def _data_internal(self, data):
        self.__dict__['_data'] = data

    @property
    def _data(self):
        return self._data_internal

    @_data.setter
    def _data(self, data):
        self._data_internal = data

    def __getattr__(self, name):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            return self._data_internal[remapped_name]
        elif (
            name_ in self._data_internal
            and name not in self._attributes_to_ignore
            and name not in self._attributes_to_remap.values()
        ):
            return self._data_internal[name_]
        raise AttributeError('Could not find attribute {}.'.format(name_))

    def __setattr__(self, name, value):
        name_ = python_to_json_style(name)
        if name in self._attributes_to_remap:
            remapped_name = self._attributes_to_remap[name]
            self._data_internal[remapped_name] = value
        elif (
            name_ in self._data_internal
            and name not in self._attributes_to_ignore
            and name not in self._attributes_to_remap.values()
        ):
            self._data_internal[name_] = value
        else:
            super().__setattr__(name, value)

    def __dir__(self):
        return sorted(
            list(dir(object))
            + list(self.__dict__.keys())
            + list(
                json_to_python_style(key)
                for key in self._data_internal.keys()
                if key not in (list(self._attributes_to_remap.values()) + self._attributes_to_ignore)
            )
            + list(self._attributes_to_remap.keys())
        )

    def __eq__(self, other):
        return self._data_internal == other._data_internal

    def __repr__(self):
        return '<{} ({})>'.format(
            self.__class__.__name__, ', '.join('{}={}'.format(key, getattr(self, key)) for key in self._repr_metadata)
        )


class ModelCollection:
    """Base class wrapper with Abstractions.

    Args:
        streamsets_entity: An instance of underlysing StreamSets entity
            e.g. :py:class:`streamsets.sdk.next.Next` or :py:class:`streamsets.sdk.accounts.Accounts`.
    """

    def __init__(self, streamsets_entity):
        self._streamsets_entity = streamsets_entity
        self._id_attr = 'id'

    def _get_all_results_from_api(self, **kwargs):
        """Used to get multiple (all) results from api.

        Args:
            Optional arguments to be passed to filter the results.

        Returns:
            A :obj:`collections.namedtuple`: of
                results (:py:class:`streamsets.sdk.utils.SeekableList`): a SeekableList of inherited instances of
                :py:class:`streamsets.sdk.models.BaseModel` and
                kwargs (:obj:`dict`): a dict of local variables not used in this function.
        """
        pass

    def __iter__(self):
        """Enables the list enumeration or iteration."""
        for item in self._get_all_results_from_api().results:
            yield item

    def __getitem__(self, i):
        """Enables the user to fetch items by index.

        Args:
            i (:obj:`int`): Index of the item.

        Returns:
            An inherited instance of :py:class:`streamsets.sdk.models.BaseModel`.
        """
        return self._get_all_results_from_api().results[i]

    def __len__(self):
        """Provides length (count) of items.

        Returns:
            A :py:obj:`int` object.
        """
        return len(self._get_all_results_from_api().results)

    def __contains__(self, item_given):
        """Checks if given item is in the list of items by comparing the ids.

        Returns:
            A :py:obj:`boolean` object.
        """
        return self.contains(**{self._id_attr: getattr(item_given, self._id_attr)})

    def get(self, **kwargs):
        """
        Args:
            **kwargs: Optional arguments to be passed to filter the results offline.

        Returns:
            An inherited instance of :py:class:`streamsets.sdk.models.BaseModel`.
        """
        result, new_kwargs = self._get_all_results_from_api(**kwargs)
        return result.get(**new_kwargs)

    def get_all(self, **kwargs):
        """
        Args:
            **kwargs: Optional other arguments to be passed to filter the results offline.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of inherited instances of
            :py:class:`streamsets.sdk.models.BaseModel`.
        """
        result, new_kwargs = self._get_all_results_from_api(**kwargs)
        return result.get_all(**new_kwargs)

    def __repr__(self):
        return str(self._get_all_results_from_api().results)

    def contains(self, **kwargs):
        """
        Args:
            **kwargs: Optional arguments to be passed to filter the results offline.

        Returns:
            A :py:obj:`boolean` object.
        """
        try:
            self.get(**kwargs)
        except ValueError:
            return False
        return True


class _StageWithPredicates:
    """Pipeline Stage extension to include a predicate configuration and handle the output lanes.
    This class is expected to inherit from either SDC or ST Stage class.

    Args:
            variable_output_drive (:obj:`str`, optional): Configuration name that drives the output lanes available.
            Default: ``None``.
    """

    def __init__(self, variable_output_drive=None, *args, **kwargs):
        self.variable_output_drive = variable_output_drive
        super().__init__(*args, **kwargs)
        if not self.predicates:
            self.predicates = ['default']

    def _prepare_predicates(self, predicates):
        """Validate a configuration dictionary and add an output lane if necessary.

        Args:
            predicates (:obj:`list`): A list of predicates in predicate/outputLane form or as predicates.

        Returns:
            A corresponding :obj:`list` of dictionaries containing the predicate and outputLane for each entry.
        """

        formatted_predicates = []
        for predicate in predicates:
            if not isinstance(predicate, dict):
                predicate = {'predicate': str(predicate)}

            output_lane = predicate.get(
                'outputLane', '{}OutputLane{}'.format(self._data['instanceName'], str(uuid4())).replace('-', '_')
            )

            if not predicate.get('predicate', None):
                raise ValueError('Output Lane drives should have a predicate key.')
            if not predicate.get('outputLane', None):
                output_lane_config = {'outputLane': output_lane}

                # We make sure that the predicate is in the form {'outputLane': 'value', 'predicate': 'value'} to be
                # consistent with the UI
                predicate = {**output_lane_config, **predicate}
            formatted_predicates.append(predicate)
        return formatted_predicates

    def _set_config(self, config_property, value):
        # Check whether the configuration asked for is driving the output lanes.
        if self.variable_output_drive == config_property.config_name:
            if isinstance(value, list):
                self.predicates = value
            else:
                raise ValueError('Configuration must be a list of predicates or a list of dictionaries.')
        else:
            super()._set_config(config_property, value)

    def _disconnect_and_remove_predicate(self, i):
        deleted_predicate = self.predicates.pop(i)
        output_lane = deleted_predicate['outputLane']

        output_lane_index = self.output_lanes.index(output_lane)
        self.disconnect_output_lanes(output_lane_index=output_lane_index)

        self._data['outputLanes'].remove(output_lane)
        self.output_streams -= 1

    @property
    def predicates(self):
        """
        Get the predicate list for this stage.
        Predicates define the output lanes number and behaviour.
        Set it using either a list of predicates or a list of the full dictionary specifying the output lane.

        Example:
            stage.predicates = ['>0']
            stage.predicates = ['>0', 'default']
            stage.predicates = [{'predicate':'>0', 'outputLane': 'lane1'}]

        Returns:
            A :obj:`list` of the predicates.
        """
        return self.configuration[self.variable_output_drive]

    @predicates.setter
    def predicates(self, predicates):
        predicates = self._prepare_predicates(predicates)

        # Create default condition if not present
        if not [predicate for predicate in predicates if predicate['predicate'] == 'default']:
            default_predicate = self._prepare_predicates(['default'])
            predicates.extend(default_predicate)

        if not predicates[-1]['predicate'] == 'default':
            raise ValueError('The default predicate must be placed at the end of the list.')

        self.disconnect_output_lanes(all_stages=True)

        self.output_streams = 0
        self._data['outputLanes'] = []
        self._output_lane_idx = 0

        # Create output lanes in parent stage for each predicate
        for predicate in predicates:
            self._data['outputLanes'].append(predicate['outputLane'])
            self.output_streams += 1

        self.configuration[self.variable_output_drive] = predicates

    def add_predicates(self, predicates):
        """Add a predicate.

        Example:
            stage.add_predicates(['>0'])
            stage.add_predicates([{'predicate':'>0', 'outputLane':'lane1'}])
            stage.add_predicates(['>0' ,'=0'])

        Args:
            predicates (:obj:`list`): The list of predicates to add.

        """
        if not isinstance(predicates, list):
            raise ValueError('Predicates should be a list.')

        formatted_predicates = self._prepare_predicates(predicates)

        for new_predicate in formatted_predicates:
            self._data['outputLanes'].insert(0, new_predicate['outputLane'])
            self.predicates.insert(0, new_predicate)
            self.output_streams += 1

    def remove_predicate(self, predicate):
        """Remove a predicate.

        Example:
            stage.remove_predicate(stage.predicates[0])
            stage.remove_predicate({'predicate':'>0', 'outputLane':'lane1'})

        Args:
            predicate (:obj:`dict`): The predicate to delete as a dictionary including the outputLane.

        """

        clean_predicate = next(iter(self._prepare_predicates([predicate])), {})

        if not clean_predicate:
            raise ValueError("Need to specify a predicate")

        if clean_predicate.get('predicate') == 'default':
            raise ValueError("Can't delete the default predicate.")

        for i, found_predicate in enumerate(self.predicates):
            if found_predicate == clean_predicate:
                self._disconnect_and_remove_predicate(i)
                return
        raise ValueError("Can't find target predicate in the predicates list.")
