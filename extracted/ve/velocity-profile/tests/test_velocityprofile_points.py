import unittest
from typing import Dict, List

import numpy as np
from scanspec.core import Frames

from velocity_profile.velocityprofile import VelocityProfile

# Minimum move time for a whole profile
MIN_TIME = 0.002
# minimum time between points in a profile
MIN_INTERVAL = 0.002
# Duration between points
POINT_INTERVAL = 0.1


class MotorInfo:
    def __init__(
        self,
        acceleration: float,
        max_velocity: float,
        velocity_settle: float,
    ) -> None:
        self.acceleration = acceleration
        self.max_velocity = max_velocity
        self.velocity_settle = velocity_settle

    def make_velocity_profile(self, v1, v2, distance, min_time, min_interval):
        """Calculate PVT points that will perform the move within motor params

        Args:
            v1 (float): Starting velocity in EGUs/s
            v2 (float): Ending velocity in EGUs/s
            distance (float): Relative distance to travel in EGUs
            min_time (float): The minimum time the move should take
            min_interval (float): Minimum time between profile points

        Returns:
            VelocityProfile: defining a list of times and velocities
        """

        # Create the time and velocity arrays
        p = VelocityProfile(
            v1,
            v2,
            distance,
            min_time,
            self.acceleration,
            self.max_velocity,
            self.velocity_settle,
            min_interval,
        )
        p.get_profile()
        return p


def point_velocities(
    axis_mapping: Dict[str, MotorInfo], frame: Frames, entry: bool = True
) -> Dict[str, List[float]]:
    """Find the velocities of each axis over the entry/exit of current point"""
    velocities: Dict[str, List[float]] = {}
    for axis_name, motor_info in axis_mapping.items():
        uppers = frame.upper[axis_name]
        points = frame.midpoints[axis_name]
        lowers = frame.lower[axis_name]
        velocities[axis_name] = []
        for i in range(len(points)):
            #            x
            #        x       x
            #    x               x
            #    vl  vlp vp  vpu vu
            # Given distances from point,lower, position, upper, calculate
            # velocity at entry (vl) or exit (vu) of point by extrapolation
            dp = uppers[i] - lowers[i]
            vp = dp / POINT_INTERVAL
            if i:
                # Halfway point is vpu, so calculate dpu
                d_half = uppers[i] - points[i]
            else:
                # Halfway point is vlp, so calculate dlp
                d_half = points[i] - lowers[i]

            # Extrapolate to get our entry or exit velocity
            # (vl + vp) / 2 = vlp
            # so vl = 2 * vlp - vp
            # where vlp = dlp / (t/2)
            velocity = 4 * d_half / POINT_INTERVAL - vp
            max_velocity = motor_info.max_velocity
            assert (abs(velocity) - max_velocity) / max_velocity < 1e-6, (
                f"Velocity {velocity} invalid for {axis_name} with "
                f"max_velocity {max_velocity}"
            )
            velocities[axis_name].append(velocity)
    return velocities


def profile_between_start_end_points(
    axis_mapping: (Dict[str, MotorInfo]),
    frame: Frames,
    min_time: float = MIN_TIME,
    min_interval: float = MIN_INTERVAL,
):
    velocities = point_velocities(axis_mapping, frame)
    start_velocities = {axis: vel[0] for axis, vel in velocities.items()}
    end_velocities = {axis: vel[-1] for axis, vel in velocities.items()}

    p = None
    new_min_time = 0
    time_arrays = {}
    velocity_arrays = {}
    profiles = {}
    # The first iteration reveals the slowest profile. The second generates
    # all profiles with the slowest min_time
    iterations = 2
    while iterations > 0:
        for axis_name, motor_info in axis_mapping.items():
            distance = frame.lower[axis_name][-1] - frame.upper[axis_name][0]
            # If the distance is tiny, round to zero
            if np.isclose(distance, 0.0, atol=1e-12):
                distance = 0.0
            p = motor_info.make_velocity_profile(
                start_velocities[axis_name],
                end_velocities[axis_name],
                distance,
                min_time,
                min_interval,
            )
            # Absolute time values that we are at that velocity
            profiles[axis_name] = p
            new_min_time = max(new_min_time, p.t_total)
        if np.isclose(new_min_time, min_time):
            # We've got our consistent set - see if they require quantization
            quantize = False
            for axis_name, _ in axis_mapping.items():
                quantize = quantize or profiles[axis_name].check_quantize()
            for axis_name, _ in axis_mapping.items():
                if quantize:
                    profiles[axis_name].quantize()
                time_arrays[axis_name], velocity_arrays[axis_name] = profiles[
                    axis_name
                ].make_arrays()
            return time_arrays, velocity_arrays
        else:
            min_time = new_min_time
            iterations -= 1
    raise ValueError("Can't get a consistent time in 2 iterations")


class ProfileBetweenPoints(unittest.TestCase):
    def setUp(self):
        # Motor info and axis mappings from P99 sample stages
        self.sample_x_motor_info = MotorInfo(18.0, 1.8, 0.0)
        self.sample_y_motor_info = MotorInfo(18.0, 1.8, 0.0)
        self.axis_mapping = {
            "sample_x": self.sample_x_motor_info,
            "sample_y": self.sample_y_motor_info,
        }

    def test_approximately_stationary_axis_results_in_2_profile_points(self):
        # The stationary point which causes a problem on P99 testing
        position = {
            "sample_y": [1.0000000000000888, 1.0000000000000666],
            "sample_x": [1.5, 1.0],
        }
        frame = Frames(position)

        time_arrays, velocity_arrays = profile_between_start_end_points(
            self.axis_mapping, frame
        )

        expected_time_arrays = {
            "sample_x": [0.0, 0.1, 0.284, 0.384],
            "sample_y": [0.0, 0.384],
        }
        expected_velocity_arrays = {
            "sample_x": [0.0, -1.760563380282, -1.760563380282, 0.0],
            "sample_y": [0, 0],
        }
        self.assertEqual(time_arrays, expected_time_arrays)
        self.assertEqual(velocity_arrays, expected_velocity_arrays)

    def test_stationary_profile_is_two_points(self):
        # Create the two points the same as each other
        position = {"sample_y": [1.0], "sample_x": [1.5]}
        frame = Frames(position)

        time_arrays, velocity_arrays = profile_between_start_end_points(
            self.axis_mapping, frame
        )

        expected_time_arrays = {
            "sample_x": [0.0, 0.002],
            "sample_y": [0.0, 0.002],
        }
        expected_velocity_arrays = {
            "sample_x": [0.0, 0.0],
            "sample_y": [0.0, 0.0],
        }
        self.assertEqual(time_arrays, expected_time_arrays)
        self.assertEqual(velocity_arrays, expected_velocity_arrays)
