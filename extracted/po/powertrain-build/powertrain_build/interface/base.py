# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Python module used for abstracting an application that should be interfacing others."""
from abc import abstractmethod
from ruamel.yaml import YAML
from powertrain_build.lib import logger

LOGGER = logger.create_logger('base')


def filter_signals(signals, domain):
    """ Take a list of signals and remove all domains belonging to a domain

    If the signal is part of the domain, it is not part of the resulting list

    Arguments:
        signals (list(Signal)): signals to filter
        domain (Domain): domain that the signals should not be part of
    """
    filtered_signals = []
    for signal in signals:
        if signal.name not in domain.signals:
            filtered_signals.append(signal)
    return filtered_signals


class MultipleProducersError(Exception):
    """Error when setting a producer and there already exists one"""
    def __init__(self, signal, old_producer, new_producer):
        """Set error message

        Args:
            signal (Signal): Signal object
            old_producer (BaseApplication): Producer already registered
            new_producer (BaseApplication): Producer attempted to be registered
        """
        super().__init__()
        self.message = (f"{signal.name}:"
                        f" Attempting to set producer {new_producer}"
                        f" when {old_producer} is already set")


class BaseApplication:
    """Base application to build other adapters on"""
    name = str()
    _signals = None
    node = str()  # Used to calculate interface

    read_strategies = {
        "Always",
        "OnChanged",
        "OnUpdated"
    }

    def __repr__(self):
        """String representation for logging and debugging

        Returns:
            repr (string): Name of the application, the number of insignals and outsignals
        """
        return f"<{self.name}" \
               f" insignals:{len(self.insignals)}" \
               f" outsignals:{len(self.outsignals)}>"

    def parse_signals(self):
        """API interface to read all signals in any child object"""
        self._get_signals()

    @property
    def insignals(self):
        """ Insignals to the raster.
        Calculated as all read ports - all written ports

        Returns:
            signals (list): List of Signal objects.
        """
        if self._insignals is None:
            self._get_signals()
        return [self._signals[port] for port in self._insignals - self._outsignals]

    @property
    def outsignals(self):
        """ All outports.
        Since we might consume some of the signals that should also be sent elsewhere,
        we do not remove internally consumed signals.

        Returns:
            signals (list): List of Signal objects.
        """
        if self._outsignals is None:
            self._get_signals()
        return [self._signals[port] for port in self._outsignals]

    @property
    def signals(self):
        """API interface property in any child object

        All cached signals.
        If no cache exists, reads all signals and save to cache.

        Returns:
            signals (list): Signal objects
        """
        if self._signals is None:
            self.parse_signals()
        return self._signals.values()

    @abstractmethod
    def _get_signals(self):
        """Stub to implement in child object"""

    @abstractmethod
    def get_signal_properties(self, signal):
        """Stub to implement in child object

        Ideally, this should be moved to the signal.
        Currently, getting the properties depends on how we read and define the signals.
        """

    @abstractmethod
    def parse_definition(self, definition):
        """Stub for parsing a defintion after the object has been initialized.

        Raises NotImplementedError if called without being implemented.

        Args:
            definition: Definition of the Application. Type depends on the application.
        """
        raise NotImplementedError('This is a stub')


class Signal:
    """Signal object

    The signal should behave the same way independently of where we define it.
    """
    def __repr__(self):
        """String representation for logging and debugging

        Returns:
            repr (string): Name of the application, the number of insignals and outsignals
        """
        return (f"<{self.name} in {self.applications}"
                f" producer:{self.producer}"
                f" consumers:{self.consumers}>")

    def __init__(self, name, application):
        """Define base properties of the signal object

        The application object is used to read properties of a signal.
        TODO: Do this when we define the signal and add properties known in other
              systems when we encounter them.

        Args:
            name (string): Signal name
            application (BaseApplication): Application defining the signal
        """
        self.name = name
        self.applications = {}  # Add applications to a dict to prevent duplicates
        if application is not None:
            self.applications[application.name] = application
        self._consumers = set()
        self._producer = None

    def add_application(self, application):
        """Add an application to find properties from

        Args:
            application (BaseApplication): Application to read properties from
        """
        if application.name in self.applications:
            return
        self.applications[application.name] = application

    @property
    def consumers(self):
        """Get all consumers of a signal

        Returns:
            consumers (set): All consumers of a signal
        """
        if isinstance(self._consumers, set):
            return self._consumers
        return set()

    @consumers.setter
    def consumers(self, consumers):
        """Set consumers of a signal

        If the consumers is a list or set, iterate over each consumer
        Otherwise, add the consumer to the set of consumers

        Args:
            consumers (list/set/string): consumer(s) of a signal
        """
        if isinstance(consumers, (list, set)):
            for consumer in consumers:
                self._consumers.add(consumer)
        else:
            self._consumers.add(consumers)

    @property
    def producer(self):
        """Get the producer of a signal

        Since we have some strange signals with multiple producers,
        such as counters for dep, this returns a set.
        Returns:
            producer (set): Producer(s) of a signal
        """
        if isinstance(self._producer, set):
            return self._producer
        return set()

    @producer.setter
    def producer(self, producer):
        """Set producer of a signal

        Args:
            producer (string/set): Name of the producer
        """
        if isinstance(producer, set):
            self._producer = producer
        else:
            self._producer = {producer}

    def set_producer(self, producer):
        """Set producer of a signal

        If there already is a registered producer of the signal,
        raise MultipleProducersError

        This can be expected and force_producer can be called to override this.
        That must be explicit in each instance.

        Args:
            producer (string): Name of the producer
            application (BaseApplication): Application defining the signal. Optional
        """
        if isinstance(producer, set):
            if self._producer is not None and producer - self._producer:
                raise MultipleProducersError(self, self._producer, producer)
            self.producer = producer
        else:
            if self._producer is not None \
                    and isinstance(producer, str) \
                    and producer not in self._producer:
                raise MultipleProducersError(self, self._producer, producer)
            self.producer = {producer}

    def force_producer(self, producer):
        """Forcefully update add producers of a signal

        This is needed since we have some signals that are written by multiple model
        Args:
            producers (string): Producer of a signal
            application (BaseApplication): Application defining the signal. Optional
        """

        self._producer.add(producer)

    @property
    def properties(self):
        """Properties of a signal

        Currently not homogenized.
        Therefore we read the properties from the application that defined the signal.

        Returns:
            properties (dict): properties of a signal
        """
        properties = {}
        for application in self.applications.values():
            LOGGER.debug('Getting properties for %s from %s', self.name, application.name)
            application_properties = application.get_signal_properties(self)
            LOGGER.debug(application_properties)
            for key, value in application_properties.items():
                LOGGER.debug('Looking at %s: %s', key, value)
                if key in properties and value != properties[key]:
                    LOGGER.debug('Signal %s already has %s with value %s, ignoring %s from %s',
                                 self.name, key, properties[key], value, application.name)
                    continue
                properties[key] = value
        return properties


class Interface:
    """Interface between two objects"""
    def __repr__(self):
        """String representation for logging and debugging

        Returns:
            repr (string): Name of the interface, and the length of received and transmitted signals
        """
        return (f"<{self.name}"
                f" a->b:{len(self.get_directional_signals(self.current, self.corresponding))}"
                f" b->a:{len(self.get_directional_signals(self.corresponding, self.current))}>")

    def debug(self):
        """Debug an interface object to stdout"""
        LOGGER.info('name: %s', self.name)
        for signal in self.get_directional_signals(self.current, self.corresponding):
            LOGGER.info('insignal: %s', signal)
        for signal in self.get_directional_signals(self.corresponding, self.current):
            LOGGER.info('outsignal: %s', signal)

    def __init__(self, current, corresponding):
        """Create the interface object

        Args:
            current (BaseApplication): Primary object of an interface
            corresponding (BaseApplication): Secondary object of an interface
        """
        self.name = current.name + '_' + corresponding.name
        self.current = current
        self.corresponding = corresponding

    @staticmethod
    def get_directional_signals(producer, consumer):
        """Get signals going from producer to consumer

        Args:
            producer (BaseApplication): producer of the signals
            consumer (BaseApplication): consumer of the signals
        Returns:
            signals (list): Signals sent from producer and received in consumer
        """
        outsignals = {signal.name: signal for signal in producer.outsignals}
        signals = []
        for signal in consumer.insignals:
            if signal.name in outsignals:
                signal.set_producer(outsignals[signal.name].producer)
                signal.add_application(producer)
                signal.add_application(consumer)
                signals.append(signal)
        return signals

    def get_produced_signals(self, producer_name):
        """Get signals going from producer to consumer

        This function can be used if you are lacking some objects

        Args:
            consumer_name (string): name of the consumer of the signals
        Returns:
            signals (list): Signals sent from producer and received in consumer
        """
        if producer_name == self.current.name:
            consumer = self.corresponding
            producer = self.current
        elif producer_name == self.corresponding.name:
            consumer = self.current
            producer = self.corresponding
        else:
            LOGGER.error('%s not in [%s, %s]',
                         producer_name,
                         self.current.name,
                         self.corresponding.name)
        return self.get_directional_signals(producer, consumer)

    def get_consumed_signals(self, consumer_name):
        """Get signals going from producer to consumer

        This function can be used if you are lacking some objects

        Args:
            consumer_name (string): name of the consumer of the signals
        Returns:
            signals (list): Signals sent from producer and received in consumer
        """
        if consumer_name == self.current.name:
            consumer = self.current
            producer = self.corresponding
        elif consumer_name == self.corresponding.name:
            consumer = self.corresponding
            producer = self.current
        else:
            LOGGER.error('%s not in [%s, %s]',
                         consumer_name,
                         self.current.name,
                         self.corresponding.name)
        return self.get_directional_signals(producer, consumer)


class Domain:
    """Domain with interacting interfaces"""
    def __repr__(self):
        """String representation for logging and debugging

        Returns:
            repr (string): Name of the domain, and all clients for that domain
        """
        return f"<{self.name}: {self.clients}>"

    def __init__(self):
        """Initialize the object"""
        self.name = ''
        self.signals = {}
        self.clients = set()
        self._clients = {}

    def set_name(self, name):
        """Set the name of the domain

        Args:
            name (string): Name of the domain
        """
        self.name = name

    def add_interface(self, interface):
        """Add an interface to a domain

        Args:
            interface (Interface): Interface object
        """
        self._process_interface(interface)

    def _process_interface(self, interface):
        """Process interface to add signals to the domain

        Args:
            interface (Interface): Interface object
        """
        for signal in interface.get_directional_signals(interface.current, interface.corresponding):
            self._process_signal(signal.name, interface.current, interface.corresponding)
        for signal in interface.get_directional_signals(interface.corresponding, interface.current):
            self._process_signal(signal.name, interface.corresponding, interface.current)

    def _process_signal(self, signal_name, producer, consumer):
        """Process signal to add to the domain

        Args:
            signal_name (string): Name of the signal
            consumer (BaseApplication): Consumer application of the signal
            producer (BaseApplication): Producer application of the signal
        """
        if signal_name not in self.signals:
            self.signals[signal_name] = Signal(signal_name, producer)
            self.signals[signal_name].consumers = consumer.name
            self.signals[signal_name].add_application(producer)
            self.signals[signal_name].add_application(consumer)
        signal = self.signals[signal_name]
        if producer.name not in self.clients:
            self.clients.add(producer.name)
            self._clients[producer.name] = {'producer': [], 'consumer': []}
        self._clients[producer.name]['producer'].append(signal)
        if consumer.name not in self.clients:
            self.clients.add(producer.name)
            self._clients[producer.name] = {'producer': [], 'consumer': []}
        self._clients[producer.name]['consumer'].append(signal)
        signal.consumers = consumer.name
        try:
            signal.producer = producer.name
        except MultipleProducersError as mpe:
            LOGGER.debug(mpe.message)

    def create_groups(self):
        """Create groups of signals going from each producer

        Returns:
            signal_groups (dict): Signal groups
        """
        signal_groups = {}
        for signal in self.signals.values():
            # Producer is always a set, to handle pass-through signals
            for producer in signal.producer - set(signal_groups.keys()):
                signal_groups[producer] = []
            for producer in signal.producer:
                signal_groups[producer].append(signal)
        return signal_groups

    def create_selective_groups(self, a_names, b_names):
        """Create groups for the a_list communicating with the b_names

        Returns:
            signal_groups (dict): Signal groups
        """
        signal_groups = {name: {'consumer': [], 'producer': []} for name in a_names}
        for signal in self.signals.values():
            for producer in set(signal.producer):
                if producer in a_names and signal.consumers & b_names:
                    signal_groups[producer]['producer'].append(signal)
            for consumer in signal.consumers:
                if consumer in a_names and set(signal.producer) & a_names:
                    signal_groups[consumer]['consumer'].append(signal)
        return signal_groups

    @staticmethod
    def to_yaml(spec, output):
        """Writes spec to yaml file

        Args:
            spec (dict): data for the yaml
            output (Path): file to write to
        """
        with open(output, 'w', encoding="utf-8") as yaml_file:
            yaml = YAML()
            yaml.dump(spec, yaml_file)
