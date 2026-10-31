"""
example_get_setpoints.py shows how to get the set points in MultiVu.
"""

from MultiPyVu import Client, Server

with Server() as server:
    with Client() as client:
        # Get the temperature set points
        temp, rate, approach = client.get_temperature_setpoints()
        print(f'Temperature Set Point: {temp:.4f} K')
        print(f'Rate: {rate} K/min')
        print(f'Approach Mode: {approach}')

        print('---')

        # Get the field set points
        field, rate, approach, driven = client.get_field_setpoints()
        print(f'Field Set Point: {field} T')
        print(f'Rate: {rate} T/min')
        print(f'Approach Mode: {approach}')
        print(f'Driven Mode: {driven}')
