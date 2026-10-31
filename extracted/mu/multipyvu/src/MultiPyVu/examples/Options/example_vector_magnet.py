#!/usr/bin/env python3
"""
Simple script for interacting with the OptiCool's vector magnet

"""

import time
from typing import cast, Tuple

import MultiPyVu as mpv


def floats_equal(current_val: float,
                 set_point: float,
                 rel_tol: float,
                 abs_tol: float,
                 ) -> bool:
    """
    Use a combination of relative tolerance and absolute tolerance
    to determine if the values are equal
    """
    diff = abs(current_val - set_point)
    pass_absolute = diff <= abs_tol
    if pass_absolute:
        return pass_absolute

    ave = 0.5 * (current_val + set_point)
    rel_diff = diff / max(abs(ave), 1)
    return rel_diff <= rel_tol


def tuples_equal(tuple1: Tuple, tuple2: Tuple) -> bool:
    """
    Checks if tuples with float members are equal.

    Arguments:
        tuple1 -- Tuple made up of floats
        tuple2 -- Tuple made up of floats

    Returns:
        True if the tuples are equal
    """
    accept_pct = 0.005
    abs_tol = 0.4
    for item1, item2 in zip(tuple1, tuple2):
        if not isinstance(item1, float):
            return False
        if not isinstance(item2, float):
            return False
        if not floats_equal(item1, item2, accept_pct, abs_tol):
            return False
    # If we get here, then the items in the tuple must be equal
    return True


def main():
    # configure the MultiVu columns
    data = mpv.DataFile()
    data.add_multiple_columns(['h_x', 'h_y', 'h_z', 'h_cart_status',
                               'h_m', 'theta', 'phi', 'h_spher_status'])
    data.create_file_and_write_header('VectorMagnet.dat',
                                      'Using the OptiCool vector magnet')

    with mpv.Server():
        with mpv.Client() as client:
            # Print the original setpoints:
            # Get the X field set points
            field_x, rate, approach, driven = client.get_field_setpointsX()
            print(f'X Field Set Point: {field_x} T')
            print(f'Rate: {rate} T/min')
            print(f'Approach Mode: {approach}')
            print(f'Driven Mode: {driven}')

            print('---')

            # Get the Y field set points
            field_y, rate, approach, driven = client.get_field_setpointsY()
            print(f'Y Field Set Point: {field_y} T')
            print(f'Rate: {rate} T/min')
            print(f'Approach Mode: {approach}')
            print(f'Driven Mode: {driven}')

            print('---')

            # Get the Z field set points
            field_z, rate, approach, driven = client.get_field_setpointsZ()
            print(f'Z Field Set Point: {field_z} T')
            print(f'Rate: {rate} T/min')
            print(f'Approach Mode: {approach}')
            print(f'Driven Mode: {driven}')

            print('---')

            # print a header
            print('')
            hdr = f"{'__ Cartesian __':^10}{'__ status __':^7}"
            hdr += f"{'__ Spherical __':^10}{'__ status __':^7}"
            print(hdr)

            pause_time = 0.5

            field_cart_oe_original, status_cart = client.get_vector_cartesian()
            delta_field = (1000.0, 800.0, 1500.0)
            set_point_oe = tuple(orig + delta for orig, delta in
                                 zip(field_cart_oe_original, delta_field))
            # Let linters know the size of the tuple:
            set_point_oe = cast(Tuple[float, float, float], set_point_oe)
            rate = 150.0
            approach = client.field.approach_mode.linear
            client.set_vector_cartesian(set_point_oe, rate, approach)
            field_cart_oe, status_cart = client.get_vector_cartesian()

            while not client.is_steady(client.temperature.waitfor):
                field_cart_oe, status_cart = client.get_vector_cartesian()
                field_spher_oe, status_spher = client.get_vector_spherical()

                # Set the values
                h_x, h_y, h_z = field_cart_oe
                data.set_value('h_x', h_x)
                data.set_value('h_y', h_y)
                data.set_value('h_z', h_z)
                data.set_value('h_cart_status', status_cart)
                h_m, theta, phi = field_spher_oe
                data.set_value('h_m', h_m)
                data.set_value('theta', theta)
                data.set_value('phi', phi)
                data.set_value('h_spher_status', status_spher)
                # Write the resistance and status
                data.write_data()
                print(f'{field_cart_oe:^15.4f}{status_cart:^10}', end='')
                print(f'{field_spher_oe:^15.4f}{status_spher:^10}')
                time.sleep(pause_time)

            # End by printing the final set points
            field_x, _, _, _ = client.get_field_setpointsX()
            field_y, _, _, _ = client.get_field_setpointsY()
            field_z, _, _, _ = client.get_field_setpointsZ()
    print('---')
    print(f'Final setpoints: ({field_x}, {field_y}, {field_z}) T')


if __name__ == '__main__':
    main()
