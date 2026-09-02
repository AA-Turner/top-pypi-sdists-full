"""This module is in charge of building a Aug object from it's over the wire form.

Since most serialization format do not support polymorphism, we add this capability in this module.

This module finds and loads all dynamic classes and dynamically builds the relevant component based on it's id.
"""

import six

from rook.factory import Factory
from .aug_rate_limiter import AugRateLimiter
from .limit_manager import LimitManager

from ..augs import actions, conditions, locations
from ..augs.aug import Aug


from rook.rookout_json import json
from rook import config

from rook.processor.processor_factory import ProcessorFactory

from rook.exceptions import ToolException, RookAugInvalidKey, RookObjectNameMissing, RookUnknownObject, \
    RookInvalidObjectConfiguration, RookUnsupportedLocation, RookInvalidRateLimitConfiguration
import rook.utils as utils
from rook.user_warnings import UserWarnings
from rook.processor.error import Error


class AugFactory(Factory):
    """This is the factory for building Augs by their configuration."""

    def __init__(self, output):
        """Initialize the class."""
        super(AugFactory, self).__init__()

        self._output = output
        self._processor_factory = ProcessorFactory([], [])

        self._load_dynamic_classes()

        self._global_rate_limiter = None

    @staticmethod
    def get_dict_value(configuration, value, default_value):
        val = configuration.get(value)
        return val if val is not None else default_value

    def get_aug(self, configuration):
        """Returns an Aug object based on the given configuration."""
        aug_id = None
        try:
            aug_id = configuration['id']
        except KeyError as exc:
            six.raise_from(RookAugInvalidKey('id', json.dumps(configuration)), exc)

        condition = None
        conditional = configuration.get('conditional')
        if conditional:
            condition = conditions.IfCondition(conditional)

        try:
            action_dict = configuration['action']
        except KeyError as exc:
            six.raise_from(RookAugInvalidKey('action', json.dumps(configuration)), exc)
        action = self._get_dynamic_class(action_dict)

        if self._global_rate_limiter is None:
            self._global_rate_limiter = self.create_global_rate_limiter(aug_id)

        limiters = []
        if self._global_rate_limiter is not None:
            limiters.append(self._global_rate_limiter)
        else:
            limits_spec = configuration.get('rateLimit', "")
            quota = utils.milliseconds_to_int_nano_seconds(200)
            window_size = utils.milliseconds_to_int_nano_seconds(5000)
            limiter = self.create_rate_limiter(limits_spec, quota, window_size)
            if limiter:
                limiters.append(limiter)

        max_aug_execution_time = AugFactory.get_dict_value(configuration, 'maxAugTime', config.InstrumentationConfig.MAX_AUG_TIME_MS)
        max_aug_execution_time = utils.milliseconds_to_int_nano_seconds(max_aug_execution_time)

        aug = Aug(aug_id=aug_id,
                  condition=condition,
                  action=action,
                  max_aug_execution_time_ns=max_aug_execution_time,
                  limit_manager=LimitManager(limiters))

        try:
            location_dict = configuration['location']
        except KeyError as exc:
            six.raise_from(RookAugInvalidKey('location', json.dumps(configuration)), exc)
        location = self._get_location(aug, location_dict)

        return location

    def create_global_rate_limiter(self, aug_id):
        if config.RateLimiter.GLOBAL_RATE_LIMIT == "":
            return None

        global_rate_limiter = None
        try:
            global_rate_limiter = self.create_rate_limiter(config.RateLimiter.GLOBAL_RATE_LIMIT, 0, 0)
            if global_rate_limiter is None:
                raise RookInvalidRateLimitConfiguration(config.RateLimiter.GLOBAL_RATE_LIMIT)

            config.RateLimiter.USING_GLOBAL_RATE_LIMITER = True
        except RookInvalidRateLimitConfiguration as e:
            # TODO: LOG WARNING
            if self._output:
                self._output.send_rule_status(aug_id, "Warning", Error(e))

        return global_rate_limiter

    def create_rate_limiter(self, limits_spec, default_quota, default_window_size):
        quota = default_quota
        window_size = default_window_size

        if limits_spec != "":
            limits = limits_spec.split('/')

            if len(limits) == 2:
                try:
                    quota = utils.milliseconds_to_int_nano_seconds(int(limits[0]))
                    window_size = utils.milliseconds_to_int_nano_seconds(int(limits[1]))
                except ValueError:
                    quota = default_quota
                    window_size = default_window_size

        if quota == 0:
            return None

        if quota >= window_size:
            raise RookInvalidRateLimitConfiguration(limits_spec)

        return AugRateLimiter(quota, window_size)

    def _load_dynamic_classes(self):
        """Load all dynamic classes into the factory."""
        self.register_methods(locations.__all__)
        self.register_methods(conditions.__all__)
        self.register_methods(actions.__all__)

    def _get_dynamic_class(self, configuration):
        """Return a class instance based on configuration."""

        if not configuration:
            return None
        else:
            factory = self._get_factory(configuration)

            try:
                return factory(configuration, self._processor_factory)
            except ToolException:
                raise
            except Exception as exc:
                six.raise_from(RookInvalidObjectConfiguration(configuration['name'], json.dumps(configuration)), exc)

    def _get_location(self, aug, configuration):
        """Return a location instance based on configuration."""

        if not configuration:
            return None
        else:
            factory = self._get_factory(configuration)

            try:
                return factory(self._output, aug, configuration, self._processor_factory)
            except ToolException:
                raise
            except Exception as exc:
                six.raise_from(RookInvalidObjectConfiguration(configuration['name'], json.dumps(configuration)), exc)

    def _get_factory(self, configuration):
        """Return a class factory on configuration."""
        try:
            name = configuration['name']
        except KeyError as exc:
            six.raise_from(RookObjectNameMissing(json.dumps(configuration)), exc)

        try:
            return self.get_object_factory(name)
        except (RookUnknownObject, AttributeError, KeyError) as exc:
            six.raise_from(RookUnsupportedLocation(name), exc)
