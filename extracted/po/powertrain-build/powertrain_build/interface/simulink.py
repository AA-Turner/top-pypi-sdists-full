# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module to handle the Simulink interface."""


from powertrain_build.lib import logger

LOGGER = logger.create_logger("simulink")


def get_interface(interface_data_types, dp_interface, hal_interface, sfw_interface, method_interface):
    """ Get interface combined for dp, hal and sfw

    Args:
        interface_data_types (dict): User defined interface data types
        dp_interface (dict): DP interface
        hal_interface (dict): HAL interface
        sfw_interface (dict): SFW interface
        method_interface (dict): Method interface
    Returns:
        output ([dict]): Combined interface
    """
    output = []
    output = add_dp(output, interface_data_types, split_interface(dp_interface))
    output = add_api(output, interface_data_types, split_interface(hal_interface))
    output = add_api(output, interface_data_types, split_interface(sfw_interface))
    output = add_methods(output, interface_data_types, method_interface)

    # Cannot have a completely empty adapters file, CSP will break
    if not output:
        if dp_interface:
            output = ensure_raster(output, list(dp_interface.keys())[0] + '_Nothing__Always')
        elif hal_interface:
            output = ensure_raster(output, list(hal_interface.keys())[0] + '_Nothing_Always')
        elif sfw_interface:
            output = ensure_raster(output, list(sfw_interface.keys())[0] + '_Nothing_Always')
    return output


def split_interface(interface):
    """Takes a raster interface and splits it based on read strategies.

    Args:
        interface (dict): DP/HAL/SFW raster interface.
    Returns:
        strategy_split_interface (dict): DP/HAL/SFW interface divided by read strategy.
    """
    strategy_split_interface = {}
    for raster, raster_data in interface.items():
        for port_type, signals in raster_data.items():
            for signal_spec in signals:
                interface_name = signal_spec.get('api') or signal_spec.get('domain').replace('_', '')
                new_raster = '_'.join([raster, interface_name, signal_spec['strategy']])
                if new_raster not in strategy_split_interface:
                    strategy_split_interface[new_raster] = {p: [] for p in raster_data}
                strategy_split_interface[new_raster][port_type].append(signal_spec)
    return strategy_split_interface


def ensure_raster(output, raster):
    """ Ensure raster exists in the output

    Args:
        output ([dict]): Combined interface
        raster (str): Name of raster
    Returns:
        output ([dict]): Combined interface
    """
    for adapter in output:
        if adapter['name'] == raster:
            return output
    output.append(
        {
            "name": raster,
            "ports": {
                "in": {},
                "out": {}
            }
        }
    )
    return output


def get_adapter(interface, raster):
    """ Get adapter

    Args:
        interface (dict): Combined interface
        raster (str): Name of raster
    Returns:
        adapter (dict): Adapter for the raster already in the interface
    """
    for adapter in interface:
        if adapter['name'] == raster:
            return adapter
    raise KeyError(raster)


def add_dp(output, interface_data_types, interface):
    """ Adds the DP interface to the combined interface

    Args:
        output ([dict]): Combined interface
        interface_data_types (dict): User defined interface data types
        interface (dict): DP interface
    Returns
        output (dict): Combined interface
    """
    ports = {
        "consumer": "in",
        "producer": "out"
    }
    for raster, raster_data in interface.items():
        if not isinstance(raster_data, dict):
            LOGGER.debug('Ignoring metadata: %s', raster_data)
            continue
        output = ensure_raster(output, raster)
        adapter = get_adapter(output, raster)
        for port_type, signals in raster_data.items():
            for signal in signals:
                data_type = signal['variable_type']
                primitive = ['signals']
                primitive.append(signal['domain'])
                if signal['group'] is not None:
                    primitive.append(signal['group'])
                primitive.append(signal['property'])
                adapter['ports'][ports[port_type]][signal['variable']] = {
                    'primitive': '.'.join(primitive),
                    'type': data_type
                }
                if 'enums' in interface_data_types and data_type in interface_data_types['enums']:
                    csp_enum_definition = add_csp_enum_def(data_type, interface_data_types['enums'][data_type])
                    if 'types' not in adapter:
                        adapter['types'] = []
                    if csp_enum_definition not in adapter['types']:
                        adapter['types'].append(csp_enum_definition)
    return output


def add_api(output, interface_data_types, interface):
    """ Adds the HAL/GenericApi/SFW interface to the combined interface

    Args:
        output ([dict]): Combined interface
        interface_data_types (dict): User defined interface data types
        interface (dict): HAL interface
    Returns
        output (dict): Combined interface
    """
    ports = {
        "consumer": "in",
        "producer": "out"
    }
    for raster, raster_data in interface.items():
        if not isinstance(raster_data, dict):
            LOGGER.debug('Ignoring metadata: %s', raster_data)
            continue
        output = ensure_raster(output, raster)
        adapter = get_adapter(output, raster)
        for port_type, signals in raster_data.items():
            for signal in signals:
                data_type = signal['variable_type']
                primitive = [signal['api'].lower()]
                primitive.append(signal['endpoint'].lower())
                if signal['property'] is not None:
                    primitive.append(signal['property'].lower())
                adapter['ports'][ports[port_type]][signal['variable']] = {
                    'primitive': '.'.join(primitive),
                    'type': data_type
                }
                if 'enums' in interface_data_types and data_type in interface_data_types['enums']:
                    csp_enum_definition = add_csp_enum_def(data_type, interface_data_types['enums'][data_type])
                    if 'types' not in adapter:
                        adapter['types'] = []
                    if csp_enum_definition not in adapter['types']:
                        adapter['types'].append(csp_enum_definition)
    return output


def add_methods(output, interface_data_types, methods):
    """ Adds the CSP method call interfaces to the combined interface.

    Args:
        output ([dict]): Combined interface
        interface_data_types (dict): Dict with enum definitions
        methods (dict): Methods used by the application
    Returns:
        output (dict): Combined interface
    """

    if methods == {}:
        return output
    output = ensure_raster(output, 'csp_methods')
    adapter = get_adapter(output, 'csp_methods')
    if 'methods' not in adapter:
        adapter['methods'] = []
    for method_data in methods.values():
        method_spec = {}
        method_spec['name'] = method_data['name']
        method_spec['primitive_method'] = method_data['primitive']
        method_spec['namespace'] = method_data['namespace']
        if 'description' in method_data:
            method_spec['description'] = method_data['description']
        for direction in ['in', 'out']:
            parameters = method_data['ports'][direction]
            if len(parameters) > 0:
                method_spec[direction] = []
            for param_name, param_data in parameters.items():
                param_spec = {}
                param_spec['name'] = param_name
                param_spec['primitive_name'] = param_data['primitive']
                data_type = param_data['type']
                param_spec['type'] = data_type
                method_spec[direction].append(param_spec)
                if data_type in interface_data_types.get('enums', {}):
                    csp_enum_definition = add_csp_enum_def(data_type, interface_data_types['enums'][data_type])
                    if 'types' not in adapter:
                        adapter['types'] = []
                    if csp_enum_definition not in adapter['types']:
                        adapter['types'].append(csp_enum_definition)
        adapter['methods'].append(method_spec)
    return output


def add_csp_enum_def(enum_name, interface_enum_definition):
    """ Returns a CSP style enumeration definition, given an interface style enum definition.

    Args:
        enum_name (str): Name of the enumeration
        interface_enum_definition (dict): Enumeration from interface data types
    Returns:
        csp_enum_definition (dict): Combined interface
    """
    default = {}
    enumerators = []
    for enum_member_definition in interface_enum_definition:
        if 'default' in enum_member_definition:
            default = {enum_member_definition['in']: enum_member_definition['out']}
        else:
            enumerators.append({enum_member_definition['in']: enum_member_definition['out']})

    csp_enum_definition = {
        'name': enum_name,
        'kind': 'enum',
        'enumerators': enumerators,
        'default': default
    }
    return csp_enum_definition
