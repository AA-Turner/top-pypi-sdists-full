#!/usr/bin/env python3
'''
example_Local.py - This example tests local operation on the MultiVu PC.
'''

import time

import MultiPyVu as mpv

# Start the server.
with mpv.Server():
    # Start the client
    with mpv.Client() as client:
        # A basic loop that demonstrates communication between
        # client/server
        for mult in range(4):
            print('===============================================')
            set_point = (100*2**(-0.5)*mult, 100*2**(-0.5)*mult, 100*3**(0.5)*mult)
            print(f'Setting the vector field to {set_point}')
            client.set_vector_cartesian(set_point, 50, client.field.approach_mode.linear)
            client.wait_for(3, 0, client.field.waitfor)
            
            # Polls MultiVu for the vector magnetic field coordinates and its status
            (fx, fy, fz), f_status = client.get_vector_cartesian()
            (H, theta, phi), h_status = client.get_vector_spherical()
    

            # Relay the information from MultiVu
            print(f'The cartesian vector field is {fx:.2f}, {fy:.2f}, {fz:.2f}, status is {f_status}. ')
            print(f'The spherical vector field is {H:.2f}, {theta:.4f}, {phi:.4f}, status is {h_status}. ')

            # collect data at roughly 1s intervals
            time.sleep(.1)

        for phi in (0.0, 45.0, 90.0, 135.0, 180.0):
            print('===============================================')
            set_point = (1e4, 60, phi)
            print(f'Setting the vector field to {set_point}')
            client.set_vector_spherical(set_point, 50, client.field.approach_mode.linear)
            client.wait_for(3, 0, client.field.waitfor)
            
            # Polls MultiVu for the vector magnetic field coordinates and its status
            (fx, fy, fz), f_status = client.get_vector_cartesian()
            (H, theta, phi), h_status = client.get_vector_spherical()
    

            # Relay the information from MultiVu
            print(f'The cartesian vector field is {fx:.2f}, {fy:.2f}, {fz:.2f}, status is {f_status}. ')
            print(f'The spherical vector field is {H:.2f}, {theta:.4f}, {phi:.4f}, status is {h_status}. ')

            # collect data at roughly 1s intervals
            time.sleep(.1)
            
        # go to zero field at end
        print('Setting the vector field to zero')
        client.set_vector_spherical((0,0,0), 50, client.field.approach_mode.linear)