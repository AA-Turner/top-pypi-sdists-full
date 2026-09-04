from collections.abc import Callable
from typing import List, Dict, Optional, Any, Union, Tuple
import asyncio
import itertools
import logging
import math
import sys
from decimal import Decimal
from pathlib import Path
import osmnx as ox
from osmnx import graph as ox_graph
from osmnx import distance as ox_distance
import networkx as nx
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from navconfig import BASE_DIR
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from shapely.geometry import Polygon
from scipy.spatial.distance import pdist, squareform
from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import BallTree
from ..interfaces.flow import FlowComponent
from ..interfaces.OverpassGeocoding import (
    OverpassReverseGeocoder,
    ReverseGeocodeResult,
    DEFAULT_OVERPASS_URL,
)
from ..exceptions import (
    DataNotFound,
    ConfigError,
    ComponentError,
)
from ..conf import ROUTING_DETOUR_FACTOR
from ..interfaces.routing import RoutingService, DistanceMatrix
from .SchedulingVisits import SchedulingVisits


# -----------------------------
# Utility Functions
# -----------------------------

# Named to make the coupling visible (FEAT-241 code review fix): must
# match RoutingService's own `average_speed` default (currently 40.0,
# see flowtask/interfaces/routing.py — no shared named constant exists
# there to import instead). Used only for the cheap, network-free
# intra-cluster travel-hours estimate in `_pocket_hours`; the real
# road-mile lookup (Module 3, `_select_subcluster_market`) always goes
# through the actual RoutingService instance and its own average_speed.
_INTRA_CLUSTER_AVERAGE_SPEED_MPH = 40.0


def meters_to_miles(m):
    return m * 0.000621371


def miles_to_radians(miles):
    earth_radius_km = 6371.0087714150598
    km_per_mi = 1.609344
    earth_radius_mi = earth_radius_km / km_per_mi
    return miles / earth_radius_mi

def degrees_to_radians(row):
    lat = np.deg2rad(row[0])
    lon = np.deg2rad(row[1])

    return lat, lon


def radians_to_miles(rad):
    # Options here: https://geopy.readthedocs.io/en/stable/#module-geopy.distance
    earth_radius = 6371.0087714150598
    mi_per_km = 0.62137119

    return rad * earth_radius * mi_per_km


def create_data_model(distance_matrix, num_vehicles, depot=0, max_distance=150, max_stores_per_vehicle=3):
    """Stores the data for the VRP problem.

    ``max_distance`` is the maximum travel distance (miles) allowed per
    vehicle/day. Pass ``None`` to leave the daily distance unbounded — the
    routes are then limited only by ``max_stores_per_vehicle``.
    """
    return {
        'distance_matrix': distance_matrix,
        'num_vehicles': num_vehicles,
        'depot': depot,
        'max_distance': max_distance,
        'max_stores_per_vehicle': max_stores_per_vehicle,
    }


def vrp_distance_capacity(data) -> int:
    """Upper bound (in matrix units * 1000) for the VRP 'Distance' dimension.

    When ``max_distance`` is ``None`` the daily distance is unbounded: we keep
    the dimension (its global span cost still balances routes between ghosts)
    but give it a capacity no feasible route can ever reach — the sum of the
    largest arc of every row, which dominates any simple path in the matrix.
    """
    max_distance = data.get('max_distance')
    if max_distance is not None:
        return int(max_distance * 1000)

    matrix = data['distance_matrix']
    largest_arc = max((max(row) for row in matrix if len(row)), default=0)
    return int(largest_arc * 1000) * len(matrix) + 1


def solve_vrp(data):
    """Solves the VRP problem using OR-Tools and returns the routes."""
    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        data['num_vehicles'], data['depot']
    )

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node] * 1000)  # Convert to integer

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        vrp_distance_capacity(data),  # maximum distance per vehicle
        True,  # start cumul to zero
        'Distance')
    distance_dimension = routing.GetDimensionOrDie('Distance')
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Add Constraint: Maximum number of stores per vehicle
    def demand_callback(from_index):
        """Returns the demand of the node."""
        return 1  # Each store is a demand of 1

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        [data['max_stores_per_vehicle']] * data['num_vehicles'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # If no solution found, return empty routes
    if not solution:
        print("No solution found!")
        return []

    # Extract routes
    routes = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes


def print_routes(routes, store_ids):
    """Prints the routes in a readable format."""
    for i, route in enumerate(routes):
        print(f"Route for ghost employee {i+1}:")
        # Exclude depot if it's part of the route
        route_store_ids = [store_ids[node] for node in route if store_ids[node] != store_ids[route[0]]]
        print(" -> ".join(map(str, route_store_ids)))
        print()


class FTECalculator:
    """
    Helper class to calculate FTE requirements for clusters.

    FTE (Full-Time Employee) calculations:
    - Daily FTE: hours_needed_per_day / day_hours
    - Monthly FTE: (total_hours_per_month / full_time_hours_per_month)
    - Considers working days per month (typically ~21.7 days)
    """

    def __init__(
        self,
        day_hours: float = 8.0,
        hours_per_week: float = 40.0,
        working_days_per_week: float = 5.0,
        in_store_hours: float = 2.0,  # hours
        in_store_hours_range: Optional[Tuple[float, float]] = None,
        setup_time_per_store: float = 0.5,  # hours per visit
        visit_frequency: Optional[float] = None,
        fte_monthly_target: Optional[float] = None,
        fte_daily_target: Optional[float] = None,
        num_ghosts_range: Optional[Tuple[int, int]] = None
    ):
        self.day_hours = day_hours
        self.hours_per_week = hours_per_week
        self.working_days_per_week = working_days_per_week
        self.in_store_hours = in_store_hours
        # Flexible in-store time: (min, max) hours per store visit
        self.in_store_hours_range = in_store_hours_range
        # Fixed setup/teardown overhead per store visit (hours)
        self.setup_time_per_store = setup_time_per_store
        self.default_visit_frequency = (
            float(visit_frequency) if visit_frequency is not None else 2.0
        )
        self.fte_monthly_target = fte_monthly_target
        self.fte_daily_target = fte_daily_target
        self.num_ghosts_range = num_ghosts_range or (1, 10)

    def _weeks_per_month(self) -> float:
        """Return the average number of working weeks in a month."""
        return 4.0

    def _working_days_per_month(self) -> float:
        """Estimate working days per month from weekly configuration."""
        if self.working_days_per_week <= 0:
            return 0.0

        return self.working_days_per_week * self._weeks_per_month()

    def _full_time_hours_per_month(self) -> float:
        """Return the expected monthly hours for a full-time employee."""
        if self.fte_monthly_target is not None:
            return self.fte_monthly_target

        if self.hours_per_week is None or self.hours_per_week <= 0:
            return 0.0

        return self.hours_per_week * self._weeks_per_month()

    def fte_monthly_per_employee(self, monthly_hours: float) -> float:
        """Return the monthly FTE equivalent for a given number of hours."""
        full_time_monthly_hours = self._full_time_hours_per_month()
        if full_time_monthly_hours <= 0:
            return np.nan

        return monthly_hours / full_time_monthly_hours

    def fte_daily_per_employee(self, daily_hours: float) -> float:
        """Return the daily FTE equivalent for a given number of hours."""
        if self.day_hours <= 0:
            return np.nan

        return daily_hours / self.day_hours

    def calculate_cluster_hours(
        self,
        num_stores: int,
        avg_distance_between_stores: float,
        avg_speed_mph: float = 35.0,
        setup_time_per_store: Optional[float] = None,  # hours; None = configured default
        visit_frequencies: Optional[pd.Series] = None,
        in_store_hours: Optional[pd.Series] = None,
        num_employees: int = 1,
    ) -> Dict[str, float]:
        """
        Calculate hours needed for a cluster based on stores and distances.

        When ``in_store_hours_range`` is set, the default in-store time per
        visit is flexible: it starts at the range maximum and is compressed
        (never below the minimum) just enough for the daily schedule to fit
        in ``day_hours`` given ``num_employees``. Per-store values provided
        via the ``in_store_hours`` series always take precedence.

        Returns:
            Dictionary with daily_hours, monthly_hours, travel_hours,
            work_hours and effective_in_store_hours.
        """
        # Travel time between stores
        travel_time_per_store = (avg_distance_between_stores / avg_speed_mph) if avg_speed_mph > 0 else 0

        if setup_time_per_store is None:
            setup_time_per_store = self.setup_time_per_store

        weeks_per_month = self._weeks_per_month()

        frequency_series: Optional[pd.Series] = None
        if visit_frequencies is not None:
            frequency_series = pd.to_numeric(visit_frequencies, errors='coerce')
            frequency_series = frequency_series.fillna(self.default_visit_frequency)

        # Default in-store time per visit; flexible when a range is set
        default_service_hours = self.in_store_hours
        if self.in_store_hours_range:
            range_min, range_max = self.in_store_hours_range
            if frequency_series is not None and len(frequency_series) > 0:
                monthly_visits_estimate = float(frequency_series.sum())
            else:
                monthly_visits_estimate = num_stores * self.default_visit_frequency
            working_days_month = self._working_days_per_month()
            employees = max(1, int(num_employees))
            visits_per_day = (
                monthly_visits_estimate / working_days_month / employees
                if working_days_month > 0 else 0.0
            )
            if visits_per_day > 0 and self.day_hours > 0:
                ideal = (
                    self.day_hours / visits_per_day
                    - setup_time_per_store - travel_time_per_store
                )
                default_service_hours = min(range_max, max(range_min, ideal))
            else:
                default_service_hours = range_max

        service_time_series: Optional[pd.Series] = None
        if in_store_hours is not None:
            service_time_series = pd.to_numeric(in_store_hours, errors='coerce')
            service_time_series = service_time_series.fillna(default_service_hours)

        if frequency_series is None and service_time_series is None:
            work_hours_per_store = default_service_hours
            total_time_per_store = work_hours_per_store + travel_time_per_store + setup_time_per_store
            monthly_visits = num_stores * self.default_visit_frequency
            monthly_hours = monthly_visits * total_time_per_store
        else:
            if frequency_series is None:
                index = service_time_series.index if service_time_series is not None else None
                frequency_series = pd.Series(
                    self.default_visit_frequency,
                    index=index if index is not None else range(num_stores),
                    dtype=float
                )
            if service_time_series is None:
                service_time_series = pd.Series(
                    default_service_hours,
                    index=frequency_series.index,
                    dtype=float
                )
            else:
                service_time_series = service_time_series.reindex(frequency_series.index)
                service_time_series = service_time_series.fillna(default_service_hours)

            per_store_total = service_time_series + travel_time_per_store + setup_time_per_store
            monthly_hours = float((per_store_total * frequency_series).sum())
            monthly_visits = float(frequency_series.sum())
            work_hours_per_store = float(service_time_series.mean()) if len(service_time_series) > 0 else default_service_hours
            total_time_per_store = float(per_store_total.mean()) if len(per_store_total) > 0 else (
                work_hours_per_store + travel_time_per_store + setup_time_per_store
            )

        if frequency_series is None or len(frequency_series) == 0:
            work_hours_per_store = default_service_hours
            total_time_per_store = work_hours_per_store + travel_time_per_store + setup_time_per_store

        # Weekly totals derived from monthly visits
        weekly_hours = monthly_hours / weeks_per_month if weeks_per_month > 0 else 0.0

        # Daily hours needed (distributed across working days)
        if self.working_days_per_week > 0:
            daily_hours = weekly_hours / self.working_days_per_week
        else:
            daily_hours = weekly_hours

        return {
            'daily_hours': daily_hours,
            'weekly_hours': weekly_hours,
            'monthly_hours': monthly_hours,
            'monthly_visits': float(monthly_visits),
            'effective_in_store_hours': float(default_service_hours),
            'travel_hours_per_store': travel_time_per_store,
            'work_hours_per_store': work_hours_per_store,
            'setup_hours_per_store': setup_time_per_store,
            'total_hours_per_store': total_time_per_store
        }

    def stores_capacity(
        self,
        avg_distance_between_stores: float,
        visits_per_month: float,
        num_employees: int = 1,
        avg_speed_mph: float = 35.0,
    ) -> int:
        """How many stores a market's staff can actually service.

        The time budget is what limits a market: with 8-hour days, a store
        taking 4 hours means two visits a day and one taking 2 hours means
        four. This turns that budget into a store count::

            capacity = monthly_hours / (visits × (in_store + setup + travel))

        ``in_store`` is the compressed end of ``in_store_hours_range`` (the
        cap answers "how many stores COULD be served", and
        ``calculate_cluster_hours`` compresses towards that end when the
        schedule is tight).

        Args:
            avg_distance_between_stores: Typical hop inside the market.
            visits_per_month: Visits each store needs per month.
            num_employees: Staff assigned to the market.
            avg_speed_mph: Driving speed used to price the hop.

        Returns:
            Maximum number of stores that fits the monthly budget (0 when
            the configuration leaves no working time at all).
        """
        monthly_hours = self._full_time_hours_per_month() * max(1, int(num_employees))
        if monthly_hours <= 0:
            return 0

        travel = (
            avg_distance_between_stores / avg_speed_mph if avg_speed_mph > 0 else 0.0
        )
        in_store = (
            self.in_store_hours_range[0]
            if self.in_store_hours_range
            else self.in_store_hours
        )
        visits = (
            float(visits_per_month)
            if visits_per_month and visits_per_month > 0
            else self.default_visit_frequency
        )
        hours_per_store = (in_store + self.setup_time_per_store + travel) * visits
        if hours_per_store <= 0:
            return 0

        return int(monthly_hours // hours_per_store)

    def calculate_fte_requirements(
        self,
        cluster_hours: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate FTE requirements based on cluster hours.

        Returns:
            Dictionary with fte_daily, fte_monthly, num_employees_needed
        """
        daily_hours = cluster_hours['daily_hours']
        weekly_hours = cluster_hours.get('weekly_hours', daily_hours * self.working_days_per_week)
        monthly_hours = cluster_hours['monthly_hours']

        # Daily FTE: how many full-time employees needed per day (CLUSTER TOTAL)
        fte_daily_cluster = self.fte_daily_per_employee(daily_hours)
        if np.isnan(fte_daily_cluster):
            fte_daily_cluster = 0.0

        # Monthly FTE: considering hours per employee per month (CLUSTER TOTAL)
        fte_monthly_cluster = self.fte_monthly_per_employee(monthly_hours)
        if np.isnan(fte_monthly_cluster):
            fte_monthly_cluster = 0.0

        return {
            'fte_daily_cluster': fte_daily_cluster,
            'fte_monthly_cluster': fte_monthly_cluster,
            'daily_hours': daily_hours,
            'weekly_hours': weekly_hours,
            'monthly_hours': monthly_hours
        }

    def optimize_num_employees(
        self,
        num_stores: int,
        avg_distance: float,
        max_stores_per_employee: int = 3,
        visit_frequencies: Optional[pd.Series] = None,
        in_store_hours: Optional[pd.Series] = None,
    ) -> Dict[str, Any]:
        """
        Determine optimal number of employees to meet FTE targets.

        If fte_monthly_target is set (e.g., 173), this will try to allocate
        employees to reach that target while respecting constraints.

        Returns:
            Dictionary with num_employees, fte_daily, fte_monthly, and other metrics
        """
        min_ghosts, max_ghosts = self.num_ghosts_range
        full_time_monthly_hours = self._full_time_hours_per_month()

        # Calculate base hours needed
        cluster_hours = self.calculate_cluster_hours(
            num_stores,
            avg_distance,
            visit_frequencies=visit_frequencies,
            in_store_hours=in_store_hours,
        )
        base_fte = self.calculate_fte_requirements(cluster_hours)

        # If no FTE targets, use range-based logic
        if self.fte_monthly_target is None and self.fte_daily_target is None:
            # max_stores_per_employee is a DAILY route limit: size the team on
            # visits per working day (monthly cadence spread over the month),
            # never on the raw monthly portfolio size.
            working_days_month = self._working_days_per_month()
            visits_per_day = (
                cluster_hours['monthly_visits'] / working_days_month
                if working_days_month > 0 else 0.0
            )
            required_for_visits = (
                math.ceil(visits_per_day / max_stores_per_employee)
                if max_stores_per_employee > 0 else min_ghosts
            )
            required_for_hours = (
                math.ceil(cluster_hours['daily_hours'] / self.day_hours)
                if self.day_hours > 0 else min_ghosts
            )
            num_employees = min(
                max_ghosts,
                max(min_ghosts, required_for_visits, required_for_hours, 1),
            )

            return {
                'num_employees': num_employees,
                'fte_daily_cluster': base_fte['fte_daily_cluster'],
                'fte_monthly_cluster': base_fte['fte_monthly_cluster'],
                'daily_hours': cluster_hours['daily_hours'],
                'weekly_hours': cluster_hours['weekly_hours'],
                'monthly_hours': cluster_hours['monthly_hours'],
                'fte_monthly_target': None,
                'fte_daily_target': None,
            }

        # FTE-constrained optimization
        best_score = float('inf')
        best_candidate: Optional[Dict[str, Any]] = None

        # Derive the acceptable monthly hours band (±10%) if we have a
        # monthly target. These constraints are treated as HARD bounds.
        monthly_min_hours: Optional[float] = None
        monthly_max_hours: Optional[float] = None
        if full_time_monthly_hours > 0:
            monthly_max_hours = full_time_monthly_hours * 1.1
            monthly_min_hours = full_time_monthly_hours * 0.9

        # Ensure we search enough employees to satisfy the hard daily limit
        # and the monthly upper bound (<= +10%). We may have to go beyond the
        # provided max range if the cluster requires it.
        required_for_daily = (
            int(np.ceil(cluster_hours['daily_hours'] / self.day_hours))
            if self.day_hours > 0 else min_ghosts
        )
        required_for_monthly_cap = (
            int(np.ceil(cluster_hours['monthly_hours'] / monthly_max_hours))
            if monthly_max_hours and monthly_max_hours > 0 else min_ghosts
        )

        search_upper = max(
            max_ghosts,
            required_for_daily,
            required_for_monthly_cap,
        )

        for num_emp in range(min_ghosts, search_upper + 1):
            # Distribute stores among employees
            stores_per_emp = num_stores / num_emp if num_emp > 0 else num_stores

            # Calculate hours per employee
            hours_per_emp = cluster_hours['daily_hours'] / num_emp if num_emp > 0 else cluster_hours['daily_hours']
            weekly_hours_per_emp = hours_per_emp * self.working_days_per_week
            monthly_hours_per_emp = hours_per_emp * self._working_days_per_month()

            # Hard daily hours constraint
            if hours_per_emp > self.day_hours + 1e-6:
                continue

            # Hard monthly constraint: employees must stay within ±10% of the
            # target when one is defined. Reject candidates outside the band.
            if monthly_min_hours is not None and monthly_max_hours is not None:
                if (
                    monthly_hours_per_emp < monthly_min_hours - 1e-6 or
                    monthly_hours_per_emp > monthly_max_hours + 1e-6
                ):
                    continue

            # Calculate FTE metrics (CLUSTER level)
            fte_daily_cluster = num_emp * (hours_per_emp / self.day_hours)
            fte_monthly_cluster = self.fte_monthly_per_employee(cluster_hours['monthly_hours'])
            if np.isnan(fte_monthly_cluster):
                fte_monthly_cluster = 0.0

            # Calculate score based on targets
            score = 0

            # Daily FTE constraint
            if self.fte_daily_target is not None:
                daily_diff = abs(fte_daily_cluster - self.fte_daily_target)
                score += daily_diff * 10  # Weight daily constraint heavily

            # Monthly hours per employee constraint (primary target)
            if full_time_monthly_hours > 0:
                monthly_diff = abs(monthly_hours_per_emp - full_time_monthly_hours)
                score += monthly_diff

            # Prefer not exceeding max stores per employee
            if stores_per_emp > max_stores_per_employee:
                score += (stores_per_emp - max_stores_per_employee) * 5

            # Prefer balanced distribution
            score += abs(stores_per_emp - (num_stores / max(min_ghosts, 2))) * 0.1

            if score < best_score:
                best_score = score
                best_candidate = {
                    'num_employees': num_emp,
                    'fte_daily_cluster': fte_daily_cluster,
                    'fte_monthly_cluster': fte_monthly_cluster,
                    'daily_hours': cluster_hours['daily_hours'],
                    'weekly_hours': cluster_hours['weekly_hours'],
                    'monthly_hours': cluster_hours['monthly_hours'],
                    'hours_per_employee_daily': hours_per_emp,
                    'hours_per_employee_monthly': monthly_hours_per_emp,
                    'hours_per_employee_weekly': weekly_hours_per_emp,
                    'stores_per_employee': stores_per_emp,
                    'fte_monthly_target': self.fte_monthly_target,
                    'fte_daily_target': self.fte_daily_target,
                    'fte_ratio_per_employee': self.fte_monthly_per_employee(
                        monthly_hours_per_emp
                    ),
                    'range_expanded': num_emp > max_ghosts,
                    'constraint_warning': None,
                }

        # If no candidate respected the hard constraints, fall back to the
        # minimum number of employees required to meet the daily limit.
        if best_candidate is None:
            min_emp_for_daily = max(
                min_ghosts,
                required_for_daily,
                required_for_monthly_cap,
            )

            constraint_warning = None
            if monthly_min_hours and monthly_min_hours > 0:
                max_emp_for_min_hours = int(
                    np.floor(cluster_hours['monthly_hours'] / monthly_min_hours)
                ) if cluster_hours['monthly_hours'] > 0 else 0
                if max_emp_for_min_hours > 0 and min_emp_for_daily <= max_emp_for_min_hours:
                    constraint_warning = None
                else:
                    constraint_warning = 'monthly_hours_below_tolerance'
            elif full_time_monthly_hours > 0:
                constraint_warning = 'monthly_hours_outside_tolerance'

            hours_per_emp = (
                cluster_hours['daily_hours'] / min_emp_for_daily
                if min_emp_for_daily > 0 else 0
            )
            monthly_hours_per_emp = hours_per_emp * self._working_days_per_month()
            fallback_fte_daily_cluster = self.fte_daily_per_employee(cluster_hours['daily_hours'])
            if np.isnan(fallback_fte_daily_cluster):
                fallback_fte_daily_cluster = 0.0

            fallback_fte_monthly_cluster = self.fte_monthly_per_employee(
                cluster_hours['monthly_hours']
            )
            if np.isnan(fallback_fte_monthly_cluster):
                fallback_fte_monthly_cluster = 0.0

            best_candidate = {
                'num_employees': min_emp_for_daily,
                'fte_daily_cluster': fallback_fte_daily_cluster,
                'fte_monthly_cluster': fallback_fte_monthly_cluster,
                'daily_hours': cluster_hours['daily_hours'],
                'weekly_hours': cluster_hours['weekly_hours'],
                'monthly_hours': cluster_hours['monthly_hours'],
                'hours_per_employee_daily': hours_per_emp,
                'hours_per_employee_monthly': monthly_hours_per_emp,
                'hours_per_employee_weekly': hours_per_emp * self.working_days_per_week,
                'stores_per_employee': num_stores / min_emp_for_daily if min_emp_for_daily > 0 else 0,
                'fte_monthly_target': self.fte_monthly_target,
                'fte_daily_target': self.fte_daily_target,
                'constraint_warning': constraint_warning,
                'fte_ratio_per_employee': self.fte_monthly_per_employee(
                    monthly_hours_per_emp
                ),
                'range_expanded': min_emp_for_daily > max_ghosts,
            }

        # Enrich with per-employee FTE in hours and ratio form for convenience.
        hours_per_emp_monthly = best_candidate.get('hours_per_employee_monthly', np.nan)
        hours_per_emp_daily = best_candidate.get('hours_per_employee_daily', np.nan)
        if 'fte_ratio_per_employee' not in best_candidate:
            best_candidate['fte_ratio_per_employee'] = self.fte_monthly_per_employee(
                hours_per_emp_monthly
            )

        best_candidate['fte_monthly_per_employee'] = self.fte_monthly_per_employee(
            hours_per_emp_monthly
        )
        best_candidate['fte_daily_per_employee'] = self.fte_daily_per_employee(
            hours_per_emp_daily
        )
        best_candidate['monthly_hours_per_employee'] = hours_per_emp_monthly
        best_candidate['daily_hours_per_employee'] = hours_per_emp_daily

        return best_candidate


class MarketClustering(FlowComponent):
    """
    Offline clustering of stores using BallTree+DBSCAN (in miles or km),
    then generating a fixed number of ghost employees for each cluster,
    refining if store-to-ghost distance > threshold,
    and optionally checking daily route constraints.

    NEW FEATURES:
    - Dynamic ghost employee allocation based on FTE constraints
    - Compute daily and monthly FTE by cluster
    - Support for FTE targets (e.g., 173 FTE/month total)
    - Variable number of employees per cluster (not fixed)

    Steps:
        1) Clustering with DBSCAN (haversine + approximate).
        2) Create ghost employees at cluster centroid (random offset).
        3) Remove 'unreachable' stores if no ghost employee can reach them within a threshold (e.g. 25 miles).
        4) Check if a single ghost can cover up to `max_stores_per_day` in a route < `day_hours` or `max_distance_by_day`.
            If not, we mark that store as 'rejected' too.
        5) Return two DataFrames: final assignment + rejected stores.


    Parameters:
        cluster_radius (default: 150.0)

        Purpose: Controls the search radius for the BallTree clustering algorithm
        Usage: Converted to radians and used in tree.query_radius() to find nearby stores during cluster formation
        Effect: Determines how far apart stores can be and still be considered for the same cluster during the initial clustering phase
        Location: Used in _create_cluster() method

        density_seeding (bool, default True)

        Purpose: Density-first pass before any BFS clustering. Dense cores
        (e.g. cities) are detected first, each core founds its own market and
        the market centroid is ANCHORED inside the core — never at the plain
        mean of all members, which lands "between cities" (the Waco effect)
        when a market spans sparse territory. Remaining stores join their
        nearest core (nearest-first, within cluster_radius); stores in
        low-density areas fall through to the legacy BFS clustering.
        Set to False to restore the legacy behavior entirely.

        density_radius (float, default 20.0)

        Purpose: Radius in miles defining a store's local density (how many
        neighbours it has within it) and the extent of a core: the anchored
        centroid is the mean of the members within this radius of the core.
        Two cores of the same partition are at least twice this radius apart.

        min_core_density (int, optional)

        Purpose: Minimum neighbours within density_radius for a store to
        qualify as a dense core. Defaults to min_cluster_size (floor 2).

        random_seed (int or None, default 42)

        Purpose: Seeds the RNG that scatters ghost employees around each
        market centroid. Those positions decide which stores
        _filter_unreachable_stores drops, so the seed governs whether the
        delivered layout is reproducible at all. Pass None for per-run
        randomness.

        max_cluster_distance (default: 50.0)

        Purpose: Controls outlier detection within already-formed clusters
        Usage: Used in _detect_outliers() to check if stores are too far from their cluster's centroid
        Effect: Stores farther than this distance from their cluster center get marked as outliers
        Location: Used in validation after clusters are formed

        max_stores_per_day: Max stores per ghost employee per day
        day_hours: Working hours per day
        max_distance_by_day: Max travel distance per day (miles). Only applied
            when ``enforce_max_distance_by_day`` is true.

        enforce_max_distance_by_day (bool, default True): Whether the daily
            travel distance is a hard VRP constraint. Set to ``False`` when
            employees are not expected to be capped by mileage (e.g. they fly
            to their stores); the daily route is then limited only by
            ``max_stores_per_day``, which avoids stores being rejected as
            out-of-reach. Passing ``max_distance_by_day: null`` (or a
            non-positive value) disables it as well.


        # NEW FTE-related parameters:
        fte_monthly (float, optional): Target monthly hours per employee (e.g., 173).
            When provided, each employee is kept within ±10% of this value.

        fte_daily (float, optional): Target daily FTE (e.g., 1.0). If set,
            constrains daily FTE per cluster.

        hours_per_week (float, optional): Hours per employee per week (default 40).
            Used to derive the monthly FTE target when ``fte_monthly`` is not provided.

        working_days_per_week (float, optional): Average working days per week.
            Default: 5.0

        num_ghosts_range (tuple, optional): Min and max ghost employees per cluster
            (e.g., (2, 6)). Replaces fixed num_ghosts_per_cluster when using FTE mode.
            Default: (1, 10)

        in_store_hours (float, optional): Hours spent at each store. Default: 2.0
            When an ``in_store_hours`` column is present in the input data,
            those values override the default on a per-store basis.
        travel_route_factor (float, optional): Multiplier over the mean
            nearest-neighbour hop when estimating travel time per visit,
            covering imperfect route ordering and return legs. Default: 1.3
        setup_time_per_store (float, optional): Fixed setup/teardown overhead
            per store visit, in hours. Default: 0.5
        in_store_hours_range (list, optional): ``[min, max]`` hours per store
            visit. Makes the in-store time flexible per market: the effective
            value starts at ``max`` and is compressed (never below ``min``)
            just enough for the employee's daily schedule to fit in
            ``day_hours`` — allowing more stores per day, up to
            ``max_stores_per_day``. Reported per market as
            ``in_store_hours_effective``. Per-store column values still take
            precedence. Example: ``[2.0, 3.5]``.
        visit_frequency (float, optional): Default number of visits per store each
            month when a ``visit_frequency`` column is not provided in the input
            data. Defaults to ``2`` visits per month.
        visit_frequency_column (str, optional): Name of the column in the INPUT
            data containing per-store monthly visit frequencies. Defaults to
            ``visit_frequency``.
        visit_rule_column (str, optional): Name of the OUTPUT column holding
            the visit COUNT (1, 2, 3...). The count computed under
            ``visit_frequency_column`` is renamed to it as the last step, and
            falls back to the ``visit_frequency`` default when no per-store
            count exists. Defaults to ``visit_rule``.
        visit_frequency_rule (str, optional): Value of the OUTPUT cadence-rule
            column (``Monthly``, ``Weekly``, ``Bi-Weekly``). Defaults to
            ``Monthly``, the only cadence the clustering currently models.
        visit_frequency_rule_column (str, optional): Name of the OUTPUT column
            carrying ``visit_frequency_rule``. Defaults to ``visit_frequency``.

            Together, ``visit_rule_column``/``visit_frequency_rule_column``
            deliver the two-column contract read by the ``SchedulingVisits``
            component: ``visit_rule=2`` + ``visit_frequency='Monthly'`` means
            two visits a month.
        in_store_hours_column (str, optional): Name of the column containing
            per-store service times. Defaults to ``in_store_hours``.
        visit_cadence_rules (list, optional): Distance-based visit cadence
            rules. Each rule is a dict with ``min_distance`` (default 0),
            ``max_distance`` (``None``/absent = unbounded) and ``visits``
            (monthly visits, > 0). Distances are miles to the market center
            (semi-open ranges: ``min <= d < max``); ranges must not overlap.
            Precedence per store: non-null value in the
            ``visit_frequency_column`` > matching rule > ``visit_frequency``
            default. Adds a boolean ``cadence_rule_applied`` output column.

            Example::

                visit_cadence_rules:
                  - {min_distance: 0, max_distance: 100, visits: 2}
                  - {min_distance: 100, max_distance: null, visits: 1}
        enforce_max_cluster_size (bool, default True)

        Purpose: Whether max_cluster_size is enforced when ASSIGNING stores
        to markets. Set to False to make the cap a soft preference: every
        store then joins its NEAREST market (within the distance rules) no
        matter how many stores that market already has — e.g. a store
        between two cities is covered by the closest one instead of being
        pushed to a farther market that still has room. This includes the
        borderline second pass: existing markets may grow past
        max_cluster_size by absorbing closer stores during reassignment,
        and the overflow is never shed afterwards. The cap still guides
        the initial cluster formation and max_markets splitting.

        max_assign_distance (float, default 50.0): Maximum distance in miles
            from a market centroid for absorbing leftover (orphan/rejected)
            stores. This cap is HARD; ``max_cluster_size`` is SOFT for these
            stores: when every market within reach is full, the store is
            still absorbed by the nearest one — exceeding the size cap and
            keeping the ``outlier`` flag — rather than staying rejected. The
            final rebalancing pass never sheds the overflow to markets
            farther than ``max_cluster_distance``.
        max_markets (int, optional): Hard cap on the number of markets
            (clusters) created. Once reached, remaining stores are assigned
            to their nearest existing market; those beyond the relaxed
            distance threshold keep the ``outlier`` flag set to True.
            Default: unlimited.
        exclude_states (list | str, optional): State codes (e.g. ``['MI']``)
            whose stores are dropped before clustering. Comparison is
            case-insensitive and whitespace-tolerant. Excluded stores are
            available via ``get_excluded_stores()`` with an
            ``exclusion_reason`` column and are never reassigned.
        state_column (str, optional): Column holding the state code used by
            ``exclude_states``. Default: ``state_code``.
        excluded_regions (list | str, optional): Region values (e.g.
            ``['Great Lakes']``) whose stores are dropped before clustering
            and from the output — the ``exclude_states`` philosophy keyed on
            ``region_column``. Comparison is case-insensitive and
            whitespace-tolerant. Excluded stores are available via
            ``get_excluded_stores()`` with ``exclusion_reason``
            ``'excluded_region'`` and are never reassigned. Requires
            ``region_column`` (e.g. ``'Verizon Market'``).
        market_column (str, default ``'sub_market'``): Column holding the
            pre-defined market per store, read only in ``no_clustering``
            mode.
        no_clustering (bool, default False): Skip clustering entirely and
            adopt the markets pre-defined in ``market_column``: each distinct
            non-null value becomes one market holding exactly its rows —
            nothing is formed, moved, merged or shed, and formation options
            (``max_markets``, ``standalone_markets``, budget mode,
            ``subcluster_outliers``, ``optimize``) are ignored with a
            warning. Rows with a null/empty value are delivered unassigned
            (``market_id = -1``). The reporting chain still runs in full:
            centroids (core-anchored like standalone markets), distances,
            cadence, FTE metrics (reporting only, never enforced),
            Market-1..N renumbering and centroid reverse-geocoding.
        isolation_column (str, optional): Column used to ring-fence a group
            of stores (e.g. NYC sub-markets) into its own partition.
        standalone_markets (list, optional): Values of ``isolation_column``
            that become ONE market each, containing every matching store.
            Computed FIRST (before any clustering), ignoring distance and
            size caps, and frozen afterwards: no pipeline step may add or
            remove their stores. They count against ``max_markets`` (e.g.
            7 NYC sub-markets leave 115 slots for the rest of the network).

            A **nested list** is a group: its values are fused into a SINGLE
            market instead of one market per value. Useful to collapse every
            sub-market of a region into one market::

                standalone_markets:
                  - Newark                              # its own market
                  - [HI-Oahu, HI-Maui, HI-Kauai]        # ONE Hawaii market

            Nesting is flattened to any depth, and a value repeated across
            groups is kept only in the first one.
        resolve_centroid_location (bool, default False): Reverse-geocode each
            market's centroid and emit where it lands: ``centroid_address``
            (one-line label, e.g. ``"1234 Mundy Mill Road, Oakwood, GA"``)
            plus ``centroid_city``, ``centroid_state``, ``centroid_county``
            and ``centroid_postcode``. The point resolved is
            ``centroid_lat``/``centroid_lon`` itself — the market's centre,
            not a member store — at **one Overpass query per market**,
            issued once the layout is final.

            A centroid is a geometric mean and can land on a parking lot or
            an empty field: a point with nothing addressable nearby degrades
            to the nearest named road and then to ``"<County>, <ST>"``. An
            unreachable backend leaves every column empty and logs a
            warning — it never fails the run. While ``false`` the run makes
            zero HTTP calls and adds no columns.
        overpass_url / overpass_url_fallback (str | list, optional): Overpass
            endpoint used by ``resolve_centroid_location``, e.g.
            ``http://192.168.1.16:12345/api/interpreter``. The instance must
            be built with ``OVERPASS_USE_AREAS=true`` (both
            ``docker/overpass`` and ``docker/overpass-geocode`` are), since
            the query relies on ``is_in`` for city/state. Fallbacks are
            rotated through on retry.
        geocode_concurrency (int, default 8): Maximum in-flight
            reverse-geocode queries.
        isolation_values (list, optional): Values of ``isolation_column``
            forming the isolated partition. Stores inside and outside the
            partition are clustered separately and NEVER share a market —
            isolation also outranks outlier force-assignment.

            When combined with ``max_markets``, the cap is split between the
            partitions: the isolated one reserves the larger of its
            proportional share (``round(n_isolated / n_total * max_markets)``)
            and the minimum needed to fit its stores under
            ``max_cluster_size``, so the rest of the network can never
            consume the whole cap first.

            Example::

                isolation_column: sub_market
                isolation_values:
                  - 'Manhattan - South'
                  - 'Manhattan / Queens'
                  - 'Newark'

        max_employees (int, optional): Hard global hiring cap for the whole
            run (FEAT-240). Its presence — together with
            ``use_fte_constraints=True`` and no ``max_markets`` — activates
            the global employee-budget mode: rather than let headcount be a
            pure consequence of the layout's geometry, a greedy pass merges
            adjacent markets whenever doing so strictly reduces total
            headcount, subject to full store coverage. It is a feasibility
            constraint, never "spent": the objective stays minimization.
            Requires ``use_fte_constraints=True`` and ``num_ghosts_range``
            (the per-market employee floor/ceiling); incompatible with
            ``max_markets``, ``num_ghosts_per_cluster`` and an explicit
            ``capacity_from_hours=False``. When the minimum staffing needed
            for full coverage exceeds the cap, raises ``ComponentError``
            stating the exact deficit. Default: ``None`` (mode inactive,
            behaviour unchanged).
        consolidation_reach (float, optional): Maximum centroid-to-centroid
            distance in miles for a market pair to be a consolidation merge
            candidate in budget mode. Defaults to ``_move_distance_guard``
            when not set.
        consolidation_relax_factor (float, default 1.5): Multiplier applied
            to ``consolidation_reach`` on the second consolidation round,
            used only when the first round leaves total headcount above
            ``max_employees``.
        max_consolidation_rounds (int, default 50): Cap on the number of
            greedy consolidation rounds in budget mode, to bound runtime
            the way ``_balance_market_sizes`` already does.
        subcluster_outliers (bool, default False): Opt-in master switch for
            outlier sub-cluster assignment (FEAT-241). When True, stores
            that cannot be legitimately placed in any market are pocketed
            into sub-clusters (DBSCAN, real-store medoid) and assigned to
            the market with the fewest road miles, instead of being left as
            ``market == "Outlier"`` rows.
        subcluster_radius (float, default 30.0): DBSCAN eps in miles used to
            group leftover outliers into geographic pockets.
        max_subcluster_days (int, default 2): Day budget (1 or 2) a
            sub-cluster's in-store hours plus intra-cluster travel estimate
            must fit under; oversized pockets split recursively.
        subcluster_market_candidates (int, default 2): Number of nearest
            markets (by haversine distance, centroid to medoid) that get a
            Valhalla road-mile lookup before picking the sub-cluster's
            receiving market.
        subcluster_flyout (bool, default False): Opt-in switch for the
            fly-out peel pass (FEAT-243). Requires ``subcluster_outliers``
            to also be True. When enabled, assigned stores that are too far
            from (or have no road path to) their own market's centroid are
            peeled into sub-clusters — internally, if the market is
            standalone, or back into the outlier pool otherwise.
        flyout_distance_factor (float, default 2.0): Rule A threshold — a
            store peels when its haversine distance to its market centroid
            exceeds ``flyout_distance_factor * max_distance_by_day``.
        flyout_probe_factor (float, default 0.5): Rule B pre-filter —
            stores farther than ``flyout_probe_factor * max_distance_by_day``
            from their centroid get a routing probe to detect unroutable
            (island) pairs. Must be <= ``flyout_distance_factor``.
        capacity_shedding (bool, default False): Opt-in switch for the
            capacity-aware shedding pass (FEAT-243). Independent of
            ``subcluster_flyout``/``subcluster_outliers``. When enabled,
            markets whose total row count exceeds their layout ceiling
            shed near-boundary normal stores to neighbors with room.
        shed_distance_tolerance (float, default 1.5): Multiplier applied to
            a shed candidate's current distance-to-center to bound how far
            a receiving market's centroid may be ("similar distance").
        optimize (bool, default False): Opt-in switch for the scheduling
            feedback loop (FEAT-244). When True, an internal
            ``SchedulingVisits`` run against this component's own output
            is used as ground truth to reclassify exception stores
            (distance-impossible, capacity-saturated, block-overflow)
            before the final output is delivered. Requires
            ``scheduling_kwargs``.
        scheduling_kwargs (dict, default None): Kwargs passed as-is to the
            internal ``SchedulingVisits`` instance when ``optimize=True``.
            Must contain ``'year'`` and ``'month'``.
        reject_unanchorable_subclusters (bool, default False): FEAT-249.
            Governs what happens when a satellite pocket (see
            ``subcluster_outliers``) has no candidate market within
            ``_subcluster_anchor_cap()`` road miles AND with whole-pocket
            headroom under ``_effective_ceiling`` (FEAT-248 G4). ``False``
            (default, restores the pre-FEAT-248 100%-assignment guarantee):
            the pocket anchors to the best market from the FULL
            (unfiltered) candidate pool instead, and every row is stamped
            ``constraint_reason='subcluster_anchored_beyond_cap'``. ``True``:
            the pocket is delivered UNASSIGNED
            (``market_id=-1``, ``constraint_reason=
            'subcluster_no_candidate_within_cap'``) — the FEAT-248 G4
            behavior, now opt-in.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          MarketClustering:
          # attributes here
        ```
    """
    _version = "1.1.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Which knobs the caller set explicitly: budget mode (FEAT-240)
        # derives defaults for some of them, and a derived default must
        # never overwrite a real choice. Snapshotted before any pop.
        explicit_kwargs = set(kwargs)
        # DBSCAN config
        self.max_cluster_distance = kwargs.pop('max_cluster_distance', 50.0)
        self.cluster_radius = kwargs.pop('cluster_radius', 150.0)
        self.max_cluster_size: int = kwargs.pop('max_cluster_size', 25)  # number of items in cluster
        # When False, max_cluster_size stops being enforced on ASSIGNMENT:
        # every store joins its nearest market regardless of size (the cap
        # still guides initial cluster formation and splitting).
        self.enforce_max_cluster_size: bool = bool(
            kwargs.pop('enforce_max_cluster_size', True)
        )
        self.min_cluster_size: int = kwargs.pop('min_cluster_size', 5)  # minimum number of items in cluster
        self.rejected_stores_file: Path = kwargs.pop('rejected_stores', None)
        self.distance_unit = kwargs.pop('distance_unit', 'miles')  # or 'km'
        self.min_samples = kwargs.pop('min_samples', 1)
        # Density-first seeding: a first pass detects dense cores (cities),
        # founds one market per core and anchors its centroid inside the
        # core. False restores the legacy BFS-only clustering.
        self.density_seeding: bool = bool(kwargs.pop('density_seeding', True))
        self.density_radius: float = float(kwargs.pop('density_radius', 20.0))
        min_core_density = kwargs.pop('min_core_density', None)
        self.min_core_density: Optional[int] = (
            int(min_core_density) if min_core_density is not None else None
        )
        # Minimum distance (miles) between two density cores of the same
        # partition; None = legacy rule (2 x density_radius). Lower it so
        # close metro pairs (e.g. Fort Myers / Naples, ~35 mi) each found
        # their own market.
        core_separation = kwargs.pop('core_separation', None)
        self.core_separation: Optional[float] = None
        if core_separation is not None:
            try:
                self.core_separation = float(core_separation)
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f"core_separation must be a number, got {core_separation!r}"
                ) from exc
            if self.core_separation <= 0:
                raise ConfigError(
                    f"core_separation must be > 0, got {core_separation!r}"
                )
        # Minimum stores of the market that must sit within
        # base_density_radius of its base. Restricting the base to a store
        # LOCATION is not enough: a store in a two-store town is still a
        # two-store town, and the
        # 1-median of a multi-polar market minimises total travel by landing
        # in the empty middle between the poles — which is how a market
        # spanning Raleigh, Goldsboro and Fayetteville ended up based in
        # Clinton, a town holding 2 of its 50 stores. Candidates below this
        # threshold are excluded; when none qualifies the market falls back to
        # its plain 1-median. 0 disables the filter.
        # Split markets that are two cities rather than one. Splits are
        # otherwise triggered by SIZE alone, so a market holding two dense
        # nuclei 125 miles apart — Richmond plus Durham, across a state line —
        # never splits as long as it fits the capacity gate. 49 of 122 markets
        # hold nuclei more than 50 miles apart; one spans six states.
        self.split_incoherent_markets: bool = bool(
            kwargs.pop('split_incoherent_markets', True)
        )
        # Miles between two nuclei that make a market two markets.
        market_nucleus_separation = kwargs.pop('market_nucleus_separation', 100.0)
        try:
            self.market_nucleus_separation: float = float(market_nucleus_separation)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "market_nucleus_separation must be a number, got "
                f"{market_nucleus_separation!r}"
            ) from exc
        if self.market_nucleus_separation <= 0:
            raise ConfigError(
                "market_nucleus_separation must be > 0, got "
                f"{market_nucleus_separation!r}"
            )
        # Stores within nucleus_radius that make a cluster a nucleus worth its
        # own market, rather than a handful of stragglers to absorb.
        market_nucleus_min_stores = kwargs.pop('market_nucleus_min_stores', 6)
        try:
            self.market_nucleus_min_stores: int = int(market_nucleus_min_stores)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "market_nucleus_min_stores must be an integer, got "
                f"{market_nucleus_min_stores!r}"
            ) from exc
        if self.market_nucleus_min_stores < 2:
            raise ConfigError(
                "market_nucleus_min_stores must be >= 2, got "
                f"{market_nucleus_min_stores!r}"
            )
        self.market_nucleus_radius: float = float(
            kwargs.pop('market_nucleus_radius', 25.0)
        )

        # Outlier sub-cluster assignment (FEAT-241). Opt-in: while False,
        # stores that cannot be legitimately placed in any market keep
        # leaving the run as market == "Outlier" rows, byte-identical to
        # current behaviour.
        self.subcluster_outliers: bool = bool(
            kwargs.pop('subcluster_outliers', False)
        )
        # DBSCAN eps (miles) used to pocket the leftover outliers.
        subcluster_radius = kwargs.pop('subcluster_radius', 30.0)
        try:
            self.subcluster_radius: float = float(subcluster_radius)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                f"subcluster_radius must be a number, got {subcluster_radius!r}"
            ) from exc
        if self.subcluster_radius <= 0:
            raise ConfigError(
                f"subcluster_radius must be > 0, got {subcluster_radius!r}"
            )
        # Day budget (1 or 2) a sub-cluster's in-store hours + intra-cluster
        # travel estimate must fit under; oversized pockets split further.
        max_subcluster_days = kwargs.pop('max_subcluster_days', 2)
        try:
            self.max_subcluster_days: int = int(max_subcluster_days)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                f"max_subcluster_days must be an integer, got {max_subcluster_days!r}"
            ) from exc
        if self.max_subcluster_days not in (1, 2):
            raise ConfigError(
                f"max_subcluster_days must be 1 or 2, got {max_subcluster_days!r}"
            )
        # Haversine prefilter size: how many nearest markets (by centroid)
        # get a Valhalla road-mile lookup before picking the sub-cluster's
        # receiving market.
        subcluster_market_candidates = kwargs.pop('subcluster_market_candidates', 2)
        try:
            self.subcluster_market_candidates: int = int(subcluster_market_candidates)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "subcluster_market_candidates must be an integer, got "
                f"{subcluster_market_candidates!r}"
            ) from exc
        if self.subcluster_market_candidates < 1:
            raise ConfigError(
                "subcluster_market_candidates must be >= 1, got "
                f"{subcluster_market_candidates!r}"
            )

        # Fly-out peel pass (FEAT-243). Opt-in and requires
        # subcluster_outliers=True: peeled rows are pocketed with the same
        # _form_outlier_subclusters() machinery, so the master switch must
        # already be on.
        self.subcluster_flyout: bool = bool(
            kwargs.pop('subcluster_flyout', False)
        )
        if self.subcluster_flyout and not self.subcluster_outliers:
            raise ConfigError(
                "subcluster_flyout requires subcluster_outliers=True"
            )
        # Rule A: a store peels when its haversine distance to its own
        # market centroid exceeds flyout_distance_factor * max_distance_by_day.
        flyout_distance_factor = kwargs.pop('flyout_distance_factor', 2.0)
        try:
            self.flyout_distance_factor: float = float(flyout_distance_factor)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "flyout_distance_factor must be a number, got "
                f"{flyout_distance_factor!r}"
            ) from exc
        if self.flyout_distance_factor <= 0:
            raise ConfigError(
                "flyout_distance_factor must be > 0, got "
                f"{flyout_distance_factor!r}"
            )
        # Rule B pre-filter: only stores beyond this fraction of
        # max_distance_by_day get a routing probe for unroutable (island)
        # legs. Must not exceed flyout_distance_factor.
        flyout_probe_factor = kwargs.pop('flyout_probe_factor', 0.5)
        try:
            self.flyout_probe_factor: float = float(flyout_probe_factor)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "flyout_probe_factor must be a number, got "
                f"{flyout_probe_factor!r}"
            ) from exc
        if self.flyout_probe_factor <= 0:
            raise ConfigError(
                "flyout_probe_factor must be > 0, got "
                f"{flyout_probe_factor!r}"
            )
        if self.flyout_probe_factor > self.flyout_distance_factor:
            raise ConfigError(
                "flyout_probe_factor must be <= flyout_distance_factor, got "
                f"{self.flyout_probe_factor!r} > {self.flyout_distance_factor!r}"
            )
        # Satellite anchor opt-out (FEAT-249). Default False restores the
        # pre-FEAT-248 100%-assignment guarantee: a pocket with no candidate
        # market within _subcluster_anchor_cap()/headroom anchors to the
        # best market from the FULL (unfiltered) candidate pool instead of
        # being delivered unassigned. True reproduces FEAT-248 G4's
        # honest-rejection behavior (pocket delivered market_id=-1,
        # constraint_reason='subcluster_no_candidate_within_cap').
        self.reject_unanchorable_subclusters: bool = bool(
            kwargs.pop('reject_unanchorable_subclusters', False)
        )

        # Capacity-aware shedding pass (FEAT-243). Opt-in, independent of
        # subcluster_flyout/subcluster_outliers.
        self.capacity_shedding: bool = bool(
            kwargs.pop('capacity_shedding', False)
        )
        # How far (as a multiple of the shed candidate's current distance
        # to its own center) a receiving market's centroid may be to still
        # count as "similar distance".
        shed_distance_tolerance = kwargs.pop('shed_distance_tolerance', 1.5)
        try:
            self.shed_distance_tolerance: float = float(shed_distance_tolerance)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "shed_distance_tolerance must be a number, got "
                f"{shed_distance_tolerance!r}"
            ) from exc
        if self.shed_distance_tolerance < 1.0:
            raise ConfigError(
                "shed_distance_tolerance must be >= 1.0, got "
                f"{shed_distance_tolerance!r}"
            )

        # Scheduling feedback loop (FEAT-244). Opt-in and independent of
        # subcluster_flyout/capacity_shedding: when enabled, an internal
        # SchedulingVisits run against this component's own clustering
        # output is used as ground truth to correct exceptions the
        # geometry-only heuristics above missed.
        self._optimize: bool = bool(kwargs.pop('optimize', False))
        self._scheduling_kwargs: Optional[dict] = kwargs.pop(
            'scheduling_kwargs', None
        )
        if self._optimize:
            if not isinstance(self._scheduling_kwargs, dict):
                raise ConfigError(
                    "optimize=True requires scheduling_kwargs dict with "
                    "'year' and 'month'"
                )
            if (
                'year' not in self._scheduling_kwargs
                or 'month' not in self._scheduling_kwargs
            ):
                raise ConfigError(
                    "scheduling_kwargs must contain 'year' and 'month'"
                )

        # Follow the neighbourhood, not only the centre. Every other rule in
        # this component assigns by distance to a POINT, and a point cannot
        # represent a multi-polar territory: a store can be nearest to its own
        # centroid — correctly assigned under every distance rule here — while
        # every store around it belongs to someone else, so you cross another
        # market to reach it. A store whose k nearest neighbours are mostly
        # one other market's follows them.
        # ON since the markets it runs on are coherent (see
        # _split_incoherent_markets) and it respects min_cluster_size. It
        # shipped OFF first because on incoherent markets a store followed its
        # neighbourhood into a market whose centre was 130 miles away — that
        # market was Richmond AND Durham stitched together — and because it
        # drained markets under their floor. Both causes are fixed, and on the
        # coherent layout it beats the baseline: undersized 6 -> 4, median
        # worst leg 95.41 -> 93.46, median leg 23.65 -> 22.85, territory
        # crossings 1011 -> 879, at the cost of 12 more stores beyond 100 mi.
        self.neighbourhood_repair: bool = bool(
            kwargs.pop('neighbourhood_repair', True)
        )
        # 15 measured best over the Verizon layout: it removes the most
        # crossings (1039 -> 879) while also saving travel (-2.5k miles).
        neighbourhood_k = kwargs.pop('neighbourhood_k', 15)
        try:
            self.neighbourhood_k: int = int(neighbourhood_k)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                f"neighbourhood_k must be an integer, got {neighbourhood_k!r}"
            ) from exc
        if self.neighbourhood_k < 3:
            raise ConfigError(
                f"neighbourhood_k must be >= 3, got {neighbourhood_k!r}"
            )

        # Re-check every assignment once the layout has settled. The
        # assignment passes run BEFORE dissolution, reconciliation, orphan
        # handling and rescue move stores and shift centroids, so their
        # decisions rest on geometry that no longer holds by the time the
        # layout is delivered — a store can end up 74 miles from its market
        # with three markets holding room closer to it.
        self.repair_assignments: bool = bool(
            kwargs.pop('repair_assignments', True)
        )

        # Let a FULL market accept a store sitting right next to it by handing
        # one of its own members to a neighbour that suits that member better.
        # Sizes are redistributed, never grown: the receiving gate stays hard
        # at every link. Without it a store stays stranded whenever the only
        # market near it happens to be at capacity, however small the gain of
        # the swap would be.
        self.ejection_chain: bool = bool(kwargs.pop('ejection_chain', True))

        # Miles of improvement that let a borderline move ignore the 20%
        # reassignment buffer (the receiving gate itself stays hard).
        #
        # That buffer subtracts a share of max_cluster_size from
        # _capacity_for, so with a receiving gate above max_cluster_size the
        # threshold lands exactly on the size the layout pushes every market
        # to — 59% of markets then refuse every optimisation move despite
        # having free slots, and stores stay stranded 120+ miles from their
        # market with a market holding room 36 miles closer. Uneven markets
        # with every store close beat uniform markets with stranded stores.
        # 0 restores the old, unconditional buffer.
        reassign_overflow_gain = kwargs.pop('reassign_overflow_gain', 25.0)
        try:
            self.reassign_overflow_gain: float = float(reassign_overflow_gain)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "reassign_overflow_gain must be a number, got "
                f"{reassign_overflow_gain!r}"
            ) from exc
        if self.reassign_overflow_gain < 0:
            raise ConfigError(
                "reassign_overflow_gain must be >= 0, got "
                f"{reassign_overflow_gain!r}"
            )

        # Radius used for that count. Deliberately TIGHTER than
        # density_radius: at 30 miles a store simply near a metro inherits its
        # density and passes the filter, which is how a market kept its base
        # in Springfield GA (25 miles from Savannah) instead of moving to the
        # Savannah node itself. 15 miles measures presence, not proximity.
        base_density_radius = kwargs.pop('base_density_radius', 15.0)
        try:
            self.base_density_radius: float = float(base_density_radius)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                "base_density_radius must be a number, got "
                f"{base_density_radius!r}"
            ) from exc
        if self.base_density_radius <= 0:
            raise ConfigError(
                f"base_density_radius must be > 0, got {base_density_radius!r}"
            )

        base_min_density = kwargs.pop('base_min_density', 6)
        try:
            self.base_min_density: int = int(base_min_density)
        except (TypeError, ValueError) as exc:
            raise ConfigError(
                f"base_min_density must be an integer, got {base_min_density!r}"
            ) from exc
        if self.base_min_density < 0:
            raise ConfigError(
                f"base_min_density must be >= 0, got {base_min_density!r}"
            )

        # How far a market with room may be and still outrank a CLOSER market
        # that is full, in every orphan-absorption pass. This is the dial that
        # decides whether a store is shipped across the map to find capacity
        # or stays near home and risks being left unassigned.
        #
        # It used to be hardwired to max_cluster_distance, which made that one
        # parameter do three jobs at once (outlier threshold, cluster-forming
        # radius, and capacity-chasing reach). Unset it still falls back to
        # max_cluster_distance, so leaving it out changes nothing.
        room_reach = kwargs.pop('room_reach', None)
        self.room_reach: Optional[float] = None
        if room_reach is not None:
            try:
                self.room_reach = float(room_reach)
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f"room_reach must be a number, got {room_reach!r}"
                ) from exc
            if self.room_reach <= 0:
                raise ConfigError(
                    f"room_reach must be > 0, got {room_reach!r}"
                )

        # What a market's centre IS. This is not only what gets reported: it is
        # what _reassign_borderline_pass, _plan_market_dissolution,
        # _nearest_absorbing_market and _unassign_orphan_pass all measure
        # distances from.
        #   'base'     - the market's base (see ghost_placement): one real
        #                store location, shared by reporting and every
        #                distance decision. Default.
        #   'anchored' - legacy: mean of the members inside density_radius of
        #                a dense core, falling back to the plain mean. Lands
        #                in empty country when a market has two poles, and is
        #                never a place anybody can drive from.
        market_center = kwargs.pop('market_center', 'base')
        if market_center not in ('base', 'anchored'):
            raise ComponentError(
                "market_center must be 'base' or 'anchored', got "
                f"{market_center!r}"
            )
        self.market_center: str = market_center

        # Where a market's field rep is based. The base must be a place a rep
        # can actually operate from, so every strategy picks one of the
        # market's OWN store locations:
        #   'median'  - the store minimising TOTAL travel to all members
        #               (1-median). Default: measured over the Verizon layout
        #               it lands ~5 mi from the dense core and cuts total
        #               travel ~4% against the plain mean.
        #   'minimax' - the store minimising the WORST leg (1-center). Shortens
        #               the worst trip but sits ~19 mi from the dense core and
        #               raises total travel ~25%: it favours empty middle
        #               ground over cities. Use it as a feasibility probe.
        #   'centroid'- legacy behaviour: the plain mean of the members, which
        #               falls in empty country whenever a market has two poles.
        ghost_placement = kwargs.pop('ghost_placement', 'median')
        if ghost_placement not in ('median', 'minimax', 'centroid'):
            raise ComponentError(
                "ghost_placement must be one of 'median', 'minimax' or "
                f"'centroid', got {ghost_placement!r}"
            )
        self.ghost_placement: str = ghost_placement

        # Ghost-employee placement draws random offsets around each market
        # centroid, and those positions decide which stores
        # ``_filter_unreachable_stores`` DROPS — so an unseeded RNG makes the
        # whole layout irreproducible: the same design delivers a different
        # market map on every run. Seeded by default; pass ``None`` to opt
        # back into per-run randomness.
        random_seed = kwargs.pop('random_seed', 42)
        self.random_seed: Optional[int] = None
        if random_seed is not None:
            try:
                self.random_seed = int(random_seed)
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f"random_seed must be an integer or None, got {random_seed!r}"
                ) from exc
        self._rng = np.random.default_rng(self.random_seed)

        # Hard cap on the number of markets (clusters) created; None = unlimited
        max_markets = kwargs.pop('max_markets', None)
        self.max_markets: Optional[int] = None
        if max_markets is not None:
            try:
                self.max_markets = max(1, int(max_markets))
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f"max_markets must be an integer, got {max_markets!r}"
                ) from exc
        # Stores whose state code is listed here are dropped before clustering
        exclude_states = kwargs.pop('exclude_states', None)
        if isinstance(exclude_states, str):
            exclude_states = [exclude_states]
        self.exclude_states: Optional[List[str]] = (
            [str(state).strip().upper() for state in exclude_states]
            if exclude_states else None
        )
        self.state_column: str = kwargs.pop('state_column', 'state_code')
        # Region hard-constraint (FEAT-247): the input is split by this
        # column BEFORE any clustering happens, and the existing pipeline
        # core runs once per region — a market can never span two region
        # values. When set, per-region formation is ALWAYS on; there is no
        # enable/disable flag (hard cut, spec §2). None reproduces today's
        # single-partition behaviour.
        self.region_column: Optional[str] = kwargs.pop('region_column', None)
        # Soft-score weights for state affinity at assignment surfaces
        # (FEAT-247): state / distance / capacity, default
        # {"state": 0.5, "distance": 0.3, "capacity": 0.2} (state
        # dominant). Missing keys fill from the defaults; must be a dict
        # of known keys with non-negative numeric values and at least one
        # weight > 0, else ConfigError (FEAT-241 fail-fast pattern).
        self.state_score_weights: Dict[str, float] = (
            self._validate_state_score_weights(
                kwargs.pop('state_score_weights', None)
            )
        )
        # Stores whose region value (region_column) is listed here are
        # dropped before clustering and from the output — the exclude_states
        # philosophy keyed on the region column instead of a state column
        # (e.g. region_column='Verizon Market', excluded_regions=['Great Lakes']).
        excluded_regions = kwargs.pop('excluded_regions', None)
        if isinstance(excluded_regions, str):
            excluded_regions = [excluded_regions]
        self.excluded_regions: Optional[List[str]] = (
            [str(region).strip().casefold() for region in excluded_regions]
            if excluded_regions else None
        )
        if self.excluded_regions and not self.region_column:
            raise ComponentError(
                "excluded_regions is configured but region_column was not "
                "provided; set region_column to the column holding those "
                "values (e.g. region_column='Verizon Market')."
            )
        # Pre-defined markets (no clustering): each distinct non-null value
        # of market_column IS a market, delivered exactly as given — no
        # formation, no movement passes, no constraint enforcement. Only the
        # reporting chain runs (centroids, distances, cadence, FTE metrics,
        # Market-1..N renumbering, centroid geocoding).
        self.no_clustering: bool = bool(kwargs.pop('no_clustering', False))
        self.market_column: str = kwargs.pop('market_column', 'sub_market')
        # Market isolation (e.g. New York City): stores whose isolation_column
        # value is in isolation_values are clustered separately and can never
        # share a market with the rest of the network.
        self.isolation_column: Optional[str] = kwargs.pop('isolation_column', None)
        self.isolation_values: Optional[List[Any]] = kwargs.pop('isolation_values', None)
        # Standalone markets: each listed isolation_column value becomes ONE
        # market containing all its stores — computed FIRST, distance and
        # size caps ignored, frozen for the rest of the pipeline. They count
        # against max_markets.
        # A nested list inside standalone_markets is a GROUP: its values are
        # fused into ONE market (e.g. every HI sub-market -> a single Hawaii
        # market). Normalised here into one tuple of values per market.
        self.standalone_markets: Optional[List[Any]] = kwargs.pop('standalone_markets', None)
        self._standalone_groups: List[Tuple[Any, ...]] = (
            self._normalize_standalone_markets(self.standalone_markets)
        )
        self._cluster_id: str = kwargs.pop('cluster_id', 'market_id')
        self._cluster_name: str = kwargs.pop('cluster_name', 'market')
        # degrees around min/max lat/lon
        self.buffer_deg = kwargs.pop('buffer_deg', 0.01)
        # OSMnx config
        self.custom_filter = kwargs.get(
            "custom_filter",
            '["highway"~"motorway|trunk|primary|secondary|tertiary"]'
        )
        self.network_type = kwargs.get("network_type", "drive")
        # Ghost employees config. An explicit num_ghosts_per_cluster is a
        # HARD value: neither the fte column nor computed optima override it.
        self.num_ghosts_per_cluster: Union[int, List[int]] = kwargs.pop('num_ghosts_per_cluster', None)
        self._forced_num_ghosts: bool = self.num_ghosts_per_cluster is not None
        # How far a store may sit from a ghost employee before it counts as
        # unreachable. It must follow the market radius: a hardcoded 50 miles
        # against a 150-mile max_cluster_distance rejects every legitimately
        # distant store, and the rejects then re-enter through the
        # force-assignment door, overfilling markets.
        self.ghost_distance_threshold = kwargs.pop(
            'ghost_distance_threshold', None
        ) or self.max_cluster_distance
        # Daily route constraints
        self.max_stores_per_day = kwargs.pop('max_stores_per_day', 3)
        self.day_hours = kwargs.pop('day_hours', 8.0)
        self.max_distance_by_day = kwargs.pop('max_distance_by_day', 150.0)
        # e.g. 150 miles, or if using km, adapt accordingly
        # Opt-out for the daily distance cap: some employees fly to their
        # stores, so a per-day mileage limit only creates false "unreachable"
        # stores. Disabling it leaves max_stores_per_day as the only daily
        # route constraint. A null/non-positive max_distance_by_day means the
        # same thing.
        self.enforce_max_distance_by_day: bool = bool(
            kwargs.pop('enforce_max_distance_by_day', True)
        )
        try:
            self.max_distance_by_day = (
                None if self.max_distance_by_day is None
                else float(self.max_distance_by_day)
            )
        except (TypeError, ValueError):
            self.max_distance_by_day = None
        if self.max_distance_by_day is None or self.max_distance_by_day <= 0:
            self.enforce_max_distance_by_day = False

        # FTE-related parameters
        self.fte_monthly = kwargs.pop('fte_monthly', None)  # Expected monthly hours per employee (e.g., 173)
        self.fte_daily = kwargs.pop('fte_daily', None)  # e.g., 1.0 total daily FTE
        # Explicit flag that determines whether FTE metrics act as constraints
        self.use_fte_constraints = kwargs.pop('use_fte_constraints', False)
        self.fte_mode = self.use_fte_constraints

        self.hours_per_week = kwargs.pop('hours_per_week', 40.0)  # e.g., 40
        self.working_days_per_week = kwargs.pop('working_days_per_week', 5.0)
        self.num_ghosts_range = kwargs.pop('num_ghosts_range', None)  # e.g., (2, 6)
        self.in_store_hours = kwargs.pop('in_store_hours', 2.0)  # hours per store
        # Flexible in-store time per visit: [min, max] hours. The effective
        # value per market compresses from max toward min so the daily
        # schedule fits in day_hours (see FTECalculator).
        in_store_hours_range = kwargs.pop('in_store_hours_range', None)
        self.in_store_hours_range: Optional[Tuple[float, float]] = None
        if in_store_hours_range is not None:
            try:
                range_min, range_max = (
                    float(in_store_hours_range[0]),
                    float(in_store_hours_range[1]),
                )
            except (TypeError, ValueError, IndexError) as exc:
                raise ConfigError(
                    "in_store_hours_range must be a [min, max] pair of numbers, "
                    f"got {in_store_hours_range!r}"
                ) from exc
            if range_min <= 0 or range_max < range_min:
                raise ConfigError(
                    "in_store_hours_range requires 0 < min <= max, "
                    f"got {in_store_hours_range!r}"
                )
            self.in_store_hours_range = (range_min, range_max)
        self.in_store_hours_column = kwargs.pop('in_store_hours_column', 'in_store_hours')
        # Fixed setup/teardown overhead per store visit (hours)
        self.setup_time_per_store: float = float(kwargs.pop('setup_time_per_store', 0.5))
        # Multiplier over the mean nearest-neighbour hop when estimating
        # travel per visit (route-ordering imperfection and return legs)
        self.travel_route_factor: float = float(kwargs.pop('travel_route_factor', 1.3))
        self.visit_frequency_column = kwargs.pop('visit_frequency_column', 'visit_frequency')
        # Delivered layout expected by SchedulingVisits: the visit COUNT goes
        # out as `visit_rule` and the cadence RULE it follows as
        # `visit_frequency` (a fixed 'Monthly' — the only cadence modelled).
        self.visit_rule_column: str = kwargs.pop('visit_rule_column', 'visit_rule')
        self.visit_frequency_rule_column: str = kwargs.pop(
            'visit_frequency_rule_column', 'visit_frequency'
        )
        self.visit_frequency_rule: str = kwargs.pop('visit_frequency_rule', 'Monthly')

        visit_frequency = kwargs.pop('visit_frequency', None)
        visits_per_month_per_store = kwargs.pop('visits_per_month_per_store', None)
        legacy_visits_per_week = kwargs.pop('visits_per_week_per_store', None)

        if visits_per_month_per_store is not None:
            try:
                visits_per_month_per_store = float(visits_per_month_per_store)
            except (TypeError, ValueError):
                visits_per_month_per_store = None

        if legacy_visits_per_week is not None:
            try:
                legacy_visits_per_week = float(legacy_visits_per_week)
            except (TypeError, ValueError):
                legacy_visits_per_week = None

        if visit_frequency is None:
            if visits_per_month_per_store is not None:
                visit_frequency = visits_per_month_per_store
            elif legacy_visits_per_week is not None:
                visit_frequency = legacy_visits_per_week * 4.0

        self.default_visit_frequency = None
        if visit_frequency is not None:
            try:
                self.default_visit_frequency = float(visit_frequency)
            except (TypeError, ValueError):
                self.default_visit_frequency = None

        # Distance-based visit cadence rules (list of dicts with
        # min_distance/max_distance/visits), validated and sorted by range.
        self.visit_cadence_rules: Optional[List[Dict[str, float]]] = (
            self._parse_cadence_rules(kwargs.pop('visit_cadence_rules', None))
        )

        if self.use_fte_constraints and self.num_ghosts_range is None:
            self.use_fte_constraints = False
            self.fte_mode = False
            # super().__init__() has not run yet, so self._logger does not exist
            logging.getLogger(__name__).warning(
                "FTE constraints disabled: num_ghosts_range not specified. "
                f"Using fixed num_ghosts_per_cluster={self.num_ghosts_per_cluster if self.num_ghosts_per_cluster else 'default'}"  # noqa
            )

        if self.num_ghosts_per_cluster is None:
            if self.use_fte_constraints and self.num_ghosts_range is not None:
                self.num_ghosts_per_cluster = self.num_ghosts_range[0]
            else:
                # Legacy mode: use fixed num_ghosts_per_cluster when constraints are disabled
                self.num_ghosts_per_cluster = 2

        # Always create an FTE calculator so FTE metrics are computed even when
        # they are not being used as constraints.
        fte_monthly_target = self.fte_monthly if self.use_fte_constraints else None
        fte_daily_target = self.fte_daily if self.use_fte_constraints else None
        num_ghosts_range = self.num_ghosts_range if self.use_fte_constraints else None

        self.fte_calculator = FTECalculator(
            day_hours=self.day_hours,
            hours_per_week=self.hours_per_week,
            working_days_per_week=self.working_days_per_week,
            in_store_hours=self.in_store_hours,
            in_store_hours_range=self.in_store_hours_range,
            setup_time_per_store=self.setup_time_per_store,
            visit_frequency=self.default_visit_frequency,
            fte_monthly_target=fte_monthly_target,
            fte_daily_target=fte_daily_target,
            num_ghosts_range=num_ghosts_range
        )
        self.default_visit_frequency = self.fte_calculator.default_visit_frequency

        # Extra distance (same unit as cluster_radius) added to cluster_radius
        # when absorbing unassigned stores into existing clusters
        self.relaxed_threshold: float = kwargs.pop('relaxed_threshold', 10.0)
        # Relaxed threshold for outlier reassignment
        # e.g. 25 miles or km to consider a store "reachable" from that ghost
        self.reassignment_threshold_factor = kwargs.pop(
            'reassignment_threshold_factor', 0.5
        )  # 50% of max_cluster_distance
        # Default 20% of max_cluster_size
        self.max_reassignment_percentage = kwargs.pop('max_reassignment_percentage', 0.2)
        # Hard ceiling on how many stores a market may hold while RECEIVING
        # stores. Unlike max_cluster_size (a property of the final layout)
        # this one gates every assignment/absorption pass, so a market never
        # swells past it just because it happens to be the nearest one.
        self.max_reassigned_stores: Optional[int] = kwargs.pop(
            'max_reassigned_stores', None
        )
        # Derive each market's ceiling from its own time budget: a market
        # whose stores need 4 hours each holds half of what a 2-hour market
        # holds, and a spread-out market pays travel on every visit.
        self.capacity_from_hours: bool = bool(
            kwargs.pop('capacity_from_hours', False)
        )
        # ``day_hours`` as a physical ceiling: no market may demand a longer
        # working day from its staff. Stores that do not fit are handed to a
        # market that can service them, or left unassigned.
        self.enforce_daily_hours: bool = bool(
            kwargs.pop('enforce_daily_hours', False)
        )
        # Trade a market that nobody needs for one a stranded cluster does:
        # inert unless stores actually end up unassigned.
        self.rescue_unassigned: bool = bool(
            kwargs.pop('rescue_unassigned', True)
        )
        # Size and radius of the unassigned cluster worth a market slot.
        # Kept separate from min_cluster_size: raising the layout floor must
        # not silently switch the rescue off (a 23-store city stranded
        # because the floor moved to 25).
        self.rescue_min_stores: Optional[int] = kwargs.pop(
            'rescue_min_stores', None
        )
        self.rescue_radius: Optional[float] = kwargs.pop('rescue_radius', None)
        # Let a full market absorb the last stranded stores around it: when
        # the unassigned stores within ``rescue_radius`` of a market are at
        # most ``remnant_overflow``, they join it even past the hard capacity
        # gate — too few to rescue into a market of their own, too close to
        # deliver unassigned.
        self.absorb_remnants: bool = bool(kwargs.pop('absorb_remnants', False))
        self.remnant_overflow: int = int(kwargs.pop('remnant_overflow', 2))
        # Distance beyond which a store is left UNASSIGNED (cluster -1)
        # instead of being parked in a faraway market. ``None`` disables it:
        # every store keeps a market, however far.
        self.unassign_distance: Optional[float] = kwargs.pop(
            'unassign_distance', None
        )
        # Floor for the demand-driven relaxation of ``core_separation``: a
        # dense region may found extra cores (one per max_cluster_size worth
        # of stores) but never two closer than this. Defaults to a third of
        # ``core_separation``.
        self.min_core_separation: Optional[float] = kwargs.pop(
            'min_core_separation', None
        )
        # How many times the second pass re-evaluates distant stores: every
        # move shifts the centroids of both markets, so a single sweep can
        # leave stores stranded next to a market that only became the
        # closest one after the previous move.
        self.reassignment_passes: int = int(kwargs.pop('reassignment_passes', 3))
        # Reclaim market slots from tiny markets to split oversized ones, so
        # max_cluster_size is honoured by reshaping the layout instead of by
        # stranding stores far from their market.
        self.balance_market_sizes: bool = bool(
            kwargs.pop('balance_market_sizes', True)
        )
        # Refinement with OSMnx route-based distances?
        self.borderline_threshold = kwargs.pop('borderline_threshold', 2.5)
        # max force distance to assign a rejected store to the nearest market:
        self._max_force_assign_distance = kwargs.pop('max_assign_distance', 50)
        # bounding box or place
        self.bounding_box = kwargs.pop('bounding_box', None)
        self.place_name = kwargs.pop('place_name', None)

        # Opt-in reverse geocoding of each market's centroid into a street
        # address. Off by default — it needs a reachable Overpass instance,
        # and while off the run makes zero HTTP calls and adds no columns.
        self.resolve_centroid_location: bool = bool(
            kwargs.pop('resolve_centroid_location', False)
        )
        self.overpass_url: str = kwargs.pop('overpass_url', DEFAULT_OVERPASS_URL)
        _overpass_fallback = kwargs.pop('overpass_url_fallback', None)
        if not _overpass_fallback:
            self.overpass_url_fallback: List[str] = []
        elif isinstance(_overpass_fallback, str):
            self.overpass_url_fallback = [_overpass_fallback]
        else:
            self.overpass_url_fallback = list(_overpass_fallback)
        self.geocode_concurrency: int = kwargs.pop('geocode_concurrency', 8)

        # -- Global employee-budget mode (FEAT-240) --------------------------
        # A hard cap on total hires for the entire run. Its presence (with
        # use_fte_constraints and no max_markets) activates _budget_mode,
        # which minimizes headcount by consolidating markets rather than
        # leaving headcount as a pure consequence of the geometry.
        max_employees = kwargs.pop('max_employees', None)
        self.max_employees: Optional[int] = None
        if max_employees is not None:
            try:
                self.max_employees = int(max_employees)
            except (TypeError, ValueError) as exc:
                raise ComponentError(
                    f"max_employees must be an integer, got {max_employees!r}"
                ) from exc
            if self.max_employees < 1:
                raise ComponentError(
                    f"max_employees must be >= 1, got {max_employees!r}"
                )
        # Max centroid-to-centroid miles for a consolidation merge candidate.
        # None resolves to _move_distance_guard at merge time.
        #
        # NOTE on exception choice: these four budget-mode-only parameters
        # (this one, consolidation_relax_factor, max_consolidation_rounds,
        # plus max_employees above) all raise ComponentError, even for
        # plain type/range checks that would otherwise be ConfigError
        # elsewhere in this file (see core_separation, room_reach, etc.) —
        # deliberately, so a caller catching ComponentError for "anything
        # wrong with my budget-mode config" gets every one of them, since
        # none of these four parameters means anything outside budget mode.
        consolidation_reach = kwargs.pop('consolidation_reach', None)
        self.consolidation_reach: Optional[float] = None
        if consolidation_reach is not None:
            try:
                self.consolidation_reach = float(consolidation_reach)
            except (TypeError, ValueError) as exc:
                raise ComponentError(
                    f"consolidation_reach must be a number, got {consolidation_reach!r}"
                ) from exc
            if self.consolidation_reach <= 0:
                raise ComponentError(
                    f"consolidation_reach must be > 0, got {consolidation_reach!r}"
                )
        # Multiplier applied to consolidation_reach on the relaxed second
        # round, when the first round leaves the layout over max_employees.
        # Must be > 1, or the "relaxed" round would not actually widen the
        # reach and would just silently repeat the base round for nothing.
        consolidation_relax_factor = kwargs.pop('consolidation_relax_factor', 1.5)
        try:
            self.consolidation_relax_factor: float = float(consolidation_relax_factor)
        except (TypeError, ValueError) as exc:
            raise ComponentError(
                "consolidation_relax_factor must be a number, got "
                f"{consolidation_relax_factor!r}"
            ) from exc
        if self.consolidation_relax_factor <= 1:
            raise ComponentError(
                "consolidation_relax_factor must be > 1, got "
                f"{consolidation_relax_factor!r}: a factor of 1 or less "
                "would make the relaxed round a no-op."
            )
        # Greedy round cap for the consolidation pass. Exists because of the
        # _balance_market_sizes precedent (122 rounds before its RC-2 fix).
        max_consolidation_rounds = kwargs.pop('max_consolidation_rounds', 50)
        try:
            self.max_consolidation_rounds: int = int(max_consolidation_rounds)
        except (TypeError, ValueError) as exc:
            raise ComponentError(
                "max_consolidation_rounds must be an integer, got "
                f"{max_consolidation_rounds!r}"
            ) from exc
        if self.max_consolidation_rounds < 1:
            raise ComponentError(
                "max_consolidation_rounds must be >= 1, got "
                f"{max_consolidation_rounds!r}"
            )

        # Budget-mode configuration validation: every contradictory
        # combination fails loudly in __init__ rather than silently
        # degrading, because a forced/capped value contradicts minimization.
        if self.max_employees is not None:
            if self.max_markets is not None:
                raise ComponentError(
                    "max_employees and max_markets are mutually exclusive: "
                    "market count is an output of budget mode, not an input."
                )
            if self._forced_num_ghosts:
                raise ComponentError(
                    "max_employees and num_ghosts_per_cluster are mutually "
                    "exclusive: a forced per-market headcount contradicts "
                    "minimization."
                )
            # Checked before use_fte_constraints: a missing num_ghosts_range
            # already forced use_fte_constraints back to False a few lines
            # above (the existing degrade-with-a-warning behaviour), so this
            # order surfaces the actual root cause instead of a downstream
            # symptom.
            if self.num_ghosts_range is None:
                raise ComponentError(
                    "max_employees requires num_ghosts_range: it is also the "
                    "per-market employee floor/ceiling in budget mode."
                )
            if not self.use_fte_constraints:
                raise ComponentError(
                    "max_employees requires use_fte_constraints=True: budget "
                    "mode needs the FTE optimizer to price a merge."
                )
            if (
                'capacity_from_hours' in explicit_kwargs
                and not self.capacity_from_hours
            ):
                raise ComponentError(
                    "max_employees with explicit capacity_from_hours=False "
                    "would leave markets with no ceiling at all."
                )

        # Derived defaults: applied ONLY when the caller did not pass the
        # key explicitly, so an explicit user choice is never overwritten.
        # The two are inseparable: enforce_max_cluster_size=False makes
        # _capacity_gate return inf, and only capacity_from_hours=True
        # restores a real ceiling via _capacity_for.
        if self._budget_mode:
            if 'capacity_from_hours' not in explicit_kwargs:
                self.capacity_from_hours = True
                logging.getLogger(__name__).info(
                    "budget mode: capacity_from_hours=True (derived default)"
                )
            if 'enforce_max_cluster_size' not in explicit_kwargs:
                self.enforce_max_cluster_size = False
                logging.getLogger(__name__).info(
                    "budget mode: enforce_max_cluster_size=False (derived default)"
                )

        # Internals
        self._data: pd.DataFrame = pd.DataFrame()
        self._result: Optional[pd.DataFrame] = None
        self._rejected: pd.DataFrame = pd.DataFrame()  # for stores that get dropped
        # _data index -> _rejected index for rows readmitted as unassigned,
        # so _reconcile_rejected_ledger() can prune the ledger of stores a
        # later pass (sub-cluster attach, rescue, absorb) ends up assigning
        self._readmitted_index_map: Dict[Any, Any] = {}
        self._ghosts: List[Dict[str, Any]] = []
        self._graphs: dict = {}
        self._cluster_centroids: Dict[int, Dict[str, float]] = {}  # Store cluster centroids
        # Stores each market's time budget allows (capacity_from_hours)
        self._market_capacity: Dict[int, int] = {}
        # Anchor point (lat, lon) of each density-seeded cluster: centroid
        # recomputations stay pinned to the dense core instead of drifting
        # to the plain member mean
        self._anchored_centroids: Dict[int, Tuple[float, float]] = {}
        # Street/administrative context of each market's centroid, by
        # cluster id. Filled once by _resolve_centroid_locations(), which
        # runs after the markets are renumbered, so these keys are already
        # the delivered 1-based ids and need no remapping.
        self._centroid_locations: Dict[Any, ReverseGeocodeResult] = {}
        # Stores dropped by exclude_states (out of scope, never reassigned)
        self._excluded: pd.DataFrame = pd.DataFrame()
        # Partition (isolated or not) each cluster belongs to, by cluster id
        self._cluster_partition: Dict[int, bool] = {}
        # Frozen standalone markets: cluster id -> tuple of isolation_column
        # values (more than one when the market is a merged group)
        self._standalone_clusters: Dict[int, Tuple[Any, ...]] = {}
        # User-provided visit frequencies snapshot (set on first cadence pass)
        self._cadence_user_freq: Optional[pd.Series] = None
        # Store FTE info per cluster
        self._cluster_fte_info: Dict[int, Dict[str, Any]] = {}
        self._constraint_removed_total: int = 0
        self._constraint_rebalance_required: bool = False
        # Employee-budget consolidation counters (FEAT-240), read by
        # _log_employee_budget_summary. Set inside
        # _consolidate_markets_for_headcount; reset at the top of run() the
        # same way _constraint_removed_total is, so two consecutive run()
        # calls on the same component never accumulate.
        self._budget_markets_before: Optional[int] = None
        self._budget_markets_after: Optional[int] = None
        self._budget_merges_applied: int = 0
        self._budget_headcount_saved: int = 0
        self._budget_relaxed_round_used: bool = False
        # Scratch cache (FEAT-240): union avg_distance per candidate pair,
        # keyed by frozenset({a, b}) — filled by _merge_saving while
        # pricing a merge, read by _best_merge_candidate for sort key 3 so
        # it does not re-run the O(k²) pairwise haversine a second time
        # over the same union. Keyed (not "last call") so it degrades
        # safely to a cache miss — never a crash — if _merge_saving is
        # ever bypassed (e.g. monkeypatched directly in a test).
        self._merge_avg_distance_cache: Dict[frozenset, float] = {}
        # Scratch cache (FEAT-247): dominant state / headroom per market,
        # cleared once at the top of each of the five state-affinity
        # scoring surfaces (_reset_state_score_cache) so repeated
        # candidates within ONE pass are not recomputed per pair, while a
        # fresh pass always sees the current membership.
        self._state_score_cache: Dict[str, Dict[Any, Any]] = {
            'dominant_state': {}, 'headroom': {},
        }
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._outlier_stores: set = set()  # Track stores that were marked as outliers

    @property
    def _budget_mode(self) -> bool:
        """True when the global employee budget drives market sizing.

        Active only when ``max_employees`` is set, the FTE optimizer prices
        every market (``use_fte_constraints``), and market count is not
        separately capped (``max_markets is None`) — market count is an
        OUTPUT of this mode, never an input.
        """
        return (
            self.max_employees is not None
            and self.use_fte_constraints
            and self.max_markets is None
        )

    @staticmethod
    def _format_standalone_group(group: Tuple[Any, ...]) -> str:
        """Render a standalone group for logs: a bare value, or a merge list."""
        if len(group) == 1:
            return repr(group[0])
        return f"{list(group)!r} (merged)"

    @staticmethod
    def _normalize_standalone_markets(values: Any) -> List[Tuple[Any, ...]]:
        """Normalise ``standalone_markets`` into one tuple of values per market.

        A plain element is a market of its own. A nested list/tuple/set is a
        GROUP: every value in it lands in the SAME market — the way to fuse,
        say, all the ``HI-*`` sub-markets into a single Hawaii market::

            standalone_markets:
              - Newark                       # one market
              - [HI-Oahu, HI-Maui, HI-Kauai] # one merged market

        Nesting is flattened to any depth, ``None`` entries are dropped, and a
        value already claimed by an earlier group is skipped so no store can be
        pulled into two standalone markets.

        Args:
            values: The raw ``standalone_markets`` argument (list, scalar or
                ``None``).

        Returns:
            One tuple of isolation-column values per standalone market, in the
            order given. Empty when nothing is configured.
        """
        if not values:
            return []
        if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple, set)):
            values = [values]

        log = logging.getLogger(__name__)

        def _flatten(item: Any) -> List[Any]:
            if isinstance(item, (list, tuple, set)):
                return [leaf for sub in item for leaf in _flatten(sub)]
            return [item]

        groups: List[Tuple[Any, ...]] = []
        claimed: set = set()
        for entry in values:
            group: List[Any] = []
            for value in _flatten(entry):
                if value is None:
                    continue
                if value in claimed:
                    log.warning(
                        "standalone_markets: %r is listed more than once; "
                        "kept in the first market only.", value
                    )
                    continue
                claimed.add(value)
                group.append(value)
            if not group:
                log.warning("standalone_markets: ignoring empty entry %r", entry)
                continue
            groups.append(tuple(group))

        return groups

    @staticmethod
    def _validate_state_score_weights(
        raw: Optional[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Validate and normalise the ``state_score_weights`` kwarg.

        Merges the caller's overrides onto the FEAT-247 defaults
        (``{"state": 0.5, "distance": 0.3, "capacity": 0.2}``): missing
        keys keep their default weight, every value must be a
        non-negative number, and at least one weight must be > 0.

        Args:
            raw: The raw ``state_score_weights`` kwarg (dict or ``None``).

        Returns:
            The merged weights dict (always all three keys present).

        Raises:
            ConfigError: If ``raw`` is not a dict, has unknown keys, has a
                non-numeric or negative value, or every weight is 0.
        """
        defaults = {"state": 0.5, "distance": 0.3, "capacity": 0.2}
        if raw is None:
            return dict(defaults)

        if not isinstance(raw, dict):
            raise ConfigError(
                "state_score_weights must be a dict with keys "
                f"{sorted(defaults)}, got {raw!r}"
            )

        unknown_keys = set(raw) - set(defaults)
        if unknown_keys:
            raise ConfigError(
                f"state_score_weights has unknown keys {sorted(unknown_keys)}; "
                f"valid keys are {sorted(defaults)}"
            )

        merged = dict(defaults)
        for key, value in raw.items():
            try:
                numeric_value = float(value)
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f"state_score_weights[{key!r}] must be numeric, got {value!r}"
                ) from exc
            if numeric_value < 0:
                raise ConfigError(
                    f"state_score_weights[{key!r}] must be >= 0, got {value!r}"
                )
            merged[key] = numeric_value

        if not any(value > 0 for value in merged.values()):
            raise ConfigError(
                "state_score_weights must have at least one weight > 0, "
                f"got {merged!r}"
            )

        return merged

    @property
    def _capacity_gate(self) -> float:
        """Size limit used by every assignment/absorption pass.

        ``max_reassigned_stores`` wins when set: it caps how many stores a
        market may hold while receiving, independently of whether the
        ``max_cluster_size`` ceiling is enforced on the final layout.
        Otherwise the gate is ``max_cluster_size`` when
        ``enforce_max_cluster_size`` is on, and infinite when it is off
        (stores then always join their nearest market, however big it is).
        """
        if self.max_reassigned_stores:
            return float(self.max_reassigned_stores)
        if not self.enforce_max_cluster_size:
            return float('inf')
        return float(self.max_cluster_size)

    def _market_can_receive(
        self,
        cid: Any,
        sizes: Dict[Any, int],
        exclude: Any = None,
        partition: Optional[bool] = None,
    ) -> bool:
        """Can this market take one more store?

        One predicate for a question that was answered in six places with
        slightly different combinations of gate, standalone check and
        partition. That dispersion is where the defects lived: a gate meant
        for reassignment leaked into seeding, and a buffer computed from one
        ceiling but compared against another refused 72 of 122 markets.

        Passes that deliberately overfill (the orphan-absorption policy, where
        ``max_cluster_size`` is SOFT) do not use this — they own that choice
        explicitly.

        Args:
            cid: Candidate market.
            sizes: Current store count per market.
            exclude: Market the store is coming from, if any.
            partition: Isolation partition the store belongs to; when given,
                the market must share it.

        Returns:
            True when the market may take the store.
        """
        if cid == exclude or cid in self._standalone_clusters:
            return False
        if partition is not None and self._cluster_partition.get(cid, False) != partition:
            return False
        return sizes.get(cid, 0) < self._capacity_for(cid)

    def _market_can_release(self, cid: Any, sizes: Dict[Any, int]) -> bool:
        """Can this market give a store away without falling under its floor?

        A market below ``min_cluster_size`` stops justifying a rep, so a move
        that helps one store can hurt the layout. Standalone markets never
        give stores away at all.

        Args:
            cid: Market being asked to release a store.
            sizes: Current store count per market.

        Returns:
            True when the market may lose one store.
        """
        if cid in self._standalone_clusters:
            return False
        return sizes.get(cid, 0) > max(1, int(self.min_cluster_size))

    @property
    def _resolved_room_reach(self) -> float:
        """How far a market with room may be and still beat a closer full one.

        ``room_reach`` when configured; otherwise ``max_cluster_distance``,
        which is what this reach was hardwired to before it became its own
        parameter.
        """
        if self.room_reach is not None:
            return float(self.room_reach)
        return float(self.max_cluster_distance or float('inf'))

    @property
    def _seed_ceiling(self) -> float:
        """Size limit for INITIAL cluster formation (density seeding).

        ``_capacity_gate`` governs the absorption passes, where
        ``max_reassigned_stores`` deliberately lets a market grow past
        ``max_cluster_size`` rather than strand a store hundreds of miles
        from any market. Seeding is not absorption: a market must not be
        *born* above the ceiling it will later be split back to, or every
        size-enforcement pass starts from a layout it cannot fix.

        So the gate is tightened by ``max_cluster_size`` whenever that
        ceiling is enforced, mirroring the legacy BFS in ``_create_cluster``,
        which caps its own growth at ``max_cluster_size``. With
        ``enforce_max_cluster_size`` off the looser gate stands.
        """
        gate = self._capacity_gate
        if self.enforce_max_cluster_size and self.max_cluster_size:
            return min(gate, float(self.max_cluster_size))
        return gate

    def _capacity_for(self, cid: Any) -> float:
        """Ceiling for one market: the global gate, tightened by its hours.

        With ``capacity_from_hours`` the time budget rules — a market whose
        visits do not fit in its staff's month stops taking stores even if
        the global ``max_reassigned_stores`` still has room.
        """
        gate = self._capacity_gate
        if not self.capacity_from_hours:
            return gate

        hours_capacity = self._market_capacity.get(cid)
        if hours_capacity is None:
            return gate

        return float(min(gate, hours_capacity))

    def _reset_state_score_cache(self) -> None:
        """Clear the per-pass state-affinity scratch cache (FEAT-247).

        Dominant state and headroom are expensive to recompute per
        candidate pair (these surfaces loop over many stores/candidates).
        Called once at the top of each of the five scoring surfaces so
        repeated candidates within ONE pass hit the cache, while the next
        pass always recomputes against the current (possibly just-changed)
        membership -- spec §7 "Market dominant state... compute once per
        pass, not per candidate pair."
        """
        self._state_score_cache = {'dominant_state': {}, 'headroom': {}}

    def _market_dominant_state(self, market_id: Any) -> Optional[Any]:
        """Mode of ``state_column`` among a market's current members (FEAT-247).

        Cached per pass — see ``_reset_state_score_cache``.

        Args:
            market_id: Candidate market id.

        Returns:
            The most common ``state_column`` value among the market's
            current members, or ``None`` when unknown (missing column, no
            members, or every member's state is null).
        """
        cache = self._state_score_cache['dominant_state']
        if market_id in cache:
            return cache[market_id]

        value = None
        if self.state_column in self._data.columns:
            members = self._data.loc[
                self._data[self._cluster_id] == market_id, self.state_column
            ].dropna()
            if not members.empty:
                value = members.mode().iloc[0]

        cache[market_id] = value
        return value

    def _market_headroom(self, market_id: Any) -> float:
        """Free slots / ``max_cluster_size``, clamped to [0, 1] (FEAT-247).

        Cached per pass — see ``_reset_state_score_cache``.
        """
        cache = self._state_score_cache['headroom']
        if market_id in cache:
            return cache[market_id]

        if not self.max_cluster_size or self._cluster_id not in self._data.columns:
            value = 0.0
        else:
            size = int((self._data[self._cluster_id] == market_id).sum())
            value = max(
                0.0,
                min(1.0, (self.max_cluster_size - size) / self.max_cluster_size),
            )

        cache[market_id] = value
        return value

    def _dominant_state_of_indices(self, indices: Any) -> Optional[Any]:
        """Mode of ``state_column`` over an arbitrary set of row indices.

        Used to derive a sub-cluster's own "entity state" (its member
        stores), the same way ``_market_dominant_state`` derives a
        market's — but over an explicit index set rather than a
        ``cluster_id`` match.

        Args:
            indices: Row indices into ``self._data``.

        Returns:
            The most common ``state_column`` value, or ``None``.
        """
        indices = list(indices)
        if not indices or self.state_column not in self._data.columns:
            return None
        members = self._data.loc[
            self._data.index.intersection(indices), self.state_column
        ].dropna()
        if members.empty:
            return None
        return members.mode().iloc[0]

    def _state_affinity_score(
        self, entity_state: Any, market_id: Any, distance: float, max_distance: float
    ) -> float:
        """Weighted state/distance/capacity score ranking a candidate market.

        ::

            score = w_state    * same_state(entity, market)     # 1.0 or 0.0
                  + w_distance * (1 - distance / max_candidate)  # normalized
                  + w_capacity * headroom(market)                # [0, 1]

        Weights come from ``self.state_score_weights`` (TASK-194). A ranking
        function ONLY — it never overrides a hard guard (size gate,
        distance cap): callers only ever score candidates that already
        passed those. Null/missing state on either side scores the state
        term 0 (neutral) — distance and capacity decide (spec §2).

        Args:
            entity_state: The entity's (store's/sub-cluster's) dominant
                ``state_column`` value, or ``None``/NaN when unknown.
            market_id: Candidate market id.
            distance: Distance (miles) from the entity to this candidate.
            max_distance: Farthest candidate under consideration in this
                same ranking — normalizes the distance term into [0, 1].
                ``<= 0`` (or falsy) scores the distance term 0.

        Returns:
            The weighted score (state/capacity terms are in [0, 1]; the
            distance term is exact when ``max_distance > 0``).
        """
        weights = self.state_score_weights
        market_state = self._market_dominant_state(market_id)

        same_state = 0.0
        if (
            entity_state is not None and not pd.isna(entity_state)
            and market_state is not None and not pd.isna(market_state)
            and str(entity_state).strip().casefold() == str(market_state).strip().casefold()
        ):
            same_state = 1.0

        if max_distance and max_distance > 0:
            distance_term = max(0.0, 1.0 - (float(distance) / float(max_distance)))
        else:
            distance_term = 0.0

        headroom = self._market_headroom(market_id)

        return (
            weights.get('state', 0.0) * same_state
            + weights.get('distance', 0.0) * distance_term
            + weights.get('capacity', 0.0) * headroom
        )

    def _layout_ceiling(self, cid: Any) -> float:
        """Size a market may reach in the final layout.

        ``max_cluster_size``, tightened by the market's own time budget when
        ``capacity_from_hours`` is on — that is what makes an oversized
        market get split.
        """
        limit = float(self.max_cluster_size) if self.max_cluster_size else float('inf')
        if not self.capacity_from_hours:
            return limit

        hours_capacity = self._market_capacity.get(cid)
        if hours_capacity is None:
            return limit

        return float(min(limit, hours_capacity))

    def _effective_ceiling(self, cid: Any) -> int:
        """The ONE size ceiling every pass must agree a market has.

        FEAT-248 G2: before this method, three different numbers answered
        "how big may this market be" and passes disagreed about which one
        to read (raw ``max_cluster_size`` in ``_enforce_max_cluster_size``;
        ``_layout_ceiling`` -- with the hours component -- in
        ``_capacity_shed_pass``; ``_capacity_gate`` -- WITHOUT the hours
        component -- in ``_rescue_unassigned_clusters``). A market could be
        "full" for one pass and "has room" for another in the same run.

        Delegates to ``_layout_ceiling`` (``max_cluster_size``, tightened
        by the market's own time budget when ``capacity_from_hours`` is
        on) and floors the result to ``int`` -- every caller compares it
        against an integer row count, so a float ceiling only invites
        off-by-fraction bugs. A market with no configured
        ``max_cluster_size`` (and no hours cap) has no ceiling at all;
        ``sys.maxsize`` is returned instead of a float ``inf`` so `>` /
        `>=` comparisons against row counts stay well-typed.

        Every pass that DECIDES a move based on market size (enforce, shed,
        rescue, balance, split feasibility) must read this instead of
        ``max_cluster_size``, ``_layout_ceiling`` or ``_capacity_gate``
        directly. Passes that merely LOG or ANNOTATE a raw
        ``max_cluster_size`` value are unaffected -- and
        ``_absorb_remnant_stores`` stays a documented, deliberate
        exception: it overfills by design and does not gate on any
        ceiling.

        Args:
            cid: The market being sized.

        Returns:
            The ceiling as a non-negative int (``sys.maxsize`` when
            unbounded).
        """
        limit = self._layout_ceiling(cid)
        if not math.isfinite(limit):
            return sys.maxsize
        return int(limit)

    def _recompute_market_capacity(self) -> None:
        """Recalculate how many stores each market's time budget allows."""
        self._market_capacity = {}
        if (
            not self.capacity_from_hours
            or self._data.empty
            or self.fte_calculator is None
        ):
            return

        for cid, cluster_df in self._data.groupby(self._cluster_id):
            if cid == -1 or cluster_df.empty:
                continue

            frequencies = self._get_cluster_visit_frequencies(cluster_df)
            visits = (
                float(frequencies.mean())
                if frequencies is not None and len(frequencies) > 0
                else self.fte_calculator.default_visit_frequency
            )
            if self._forced_num_ghosts:
                employees = int(
                    self.num_ghosts_per_cluster[0]
                    if isinstance(self.num_ghosts_per_cluster, list)
                    else self.num_ghosts_per_cluster
                )
            else:
                employees = int(
                    self._cluster_fte_info.get(cid, {}).get('num_employees', 1)
                )

            self._market_capacity[cid] = self.fte_calculator.stores_capacity(
                avg_distance_between_stores=self._calculate_cluster_avg_distance(
                    cluster_df
                ),
                visits_per_month=visits,
                num_employees=max(1, employees),
            )

    @property
    def _move_distance_guard(self) -> float:
        """How far a store may be dragged by a size-rebalancing pass.

        The stricter of ``max_cluster_distance`` and ``max_assign_distance``:
        a generous cluster radius (say 300 miles, used to keep stores from
        being rejected) must not license an undersized market to pull a
        store from 100 miles away when a market sits 10 miles from it.
        A market that cannot be filled within the guard keeps its size and
        logs a warning.
        """
        return min(
            self.max_cluster_distance or float('inf'),
            self._max_force_assign_distance or float('inf'),
        )

    @property
    def daily_distance_cap(self) -> Optional[float]:
        """Daily travel cap (miles) handed to the VRP solver.

        ``None`` when ``enforce_max_distance_by_day`` is disabled, meaning the
        daily route is bounded only by ``max_stores_per_day``.
        """
        if not self.enforce_max_distance_by_day:
            return None
        return self.max_distance_by_day

    def _convert_decimal_columns_to_float(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert decimal.Decimal columns to float for numpy compatibility."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if first non-null value is Decimal
                sample = None if df[col].dropna().empty else df[col].dropna().iloc[0]
                if isinstance(sample, Decimal):
                    df[col] = df[col].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

        return df

    async def start(self, **kwargs):
        """Validate input DataFrame and columns."""
        if not self.previous:
            raise DataNotFound("No input DataFrame found.")
        self._data = self.input
        if not isinstance(self._data, pd.DataFrame):
            raise ConfigError("Incompatible input: Must be a Pandas DataFrame.")

        required_cols = {'store_id', 'latitude', 'longitude'}
        if missing := required_cols - set(self._data.columns):
            raise ComponentError(
                f"DataFrame missing required columns: {missing}"
            )

        # Convert decimal.Decimal columns to float
        self._data = self._convert_decimal_columns_to_float(self._data)

        # Drop out-of-scope states before any clustering happens
        self._data = self._apply_state_exclusions(self._data)
        if self._data.empty:
            raise DataNotFound(
                "No stores left to cluster after applying exclude_states."
            )

        # Drop out-of-scope regions before any clustering happens
        self._data = self._apply_region_exclusions(self._data)
        if self._data.empty:
            raise DataNotFound(
                "No stores left to cluster after applying excluded_regions."
            )

        # Region hard-constraint (FEAT-247): fail fast before any
        # clustering work. Runs after exclusions so out-of-scope rows
        # never trip the null-region check.
        self._validate_region_config(self._data)

        return True

    async def close(self):
        pass

    def get_rejected_stores(self) -> pd.DataFrame:
        """Return the DataFrame of rejected stores (those removed from any final market)."""
        return self._rejected

    def get_excluded_stores(self) -> pd.DataFrame:
        """Return the DataFrame of stores dropped by ``exclude_states``."""
        return self._excluded

    def _apply_state_exclusions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop stores whose state code is listed in ``exclude_states``.

        Excluded stores are out of scope (not rejected): they are kept in
        ``self._excluded`` and no later step reassigns them to a market.

        Args:
            df: Input stores DataFrame.

        Returns:
            The DataFrame without the excluded stores.

        Raises:
            ComponentError: If ``exclude_states`` is configured but the
                ``state_column`` is missing from the input DataFrame.
        """
        if not self.exclude_states:
            return df

        if self.state_column not in df.columns:
            raise ComponentError(
                f"exclude_states is configured but column '{self.state_column}' "
                "is missing from the input DataFrame."
            )

        states = df[self.state_column].astype(str).str.strip().str.upper()
        excluded_mask = states.isin(self.exclude_states)
        if excluded_mask.any():
            self._excluded = df[excluded_mask].copy()
            self._excluded['exclusion_reason'] = 'excluded_state'
            self._logger.info(
                "exclude_states: dropped %s stores in %s (%s -> %s)",
                int(excluded_mask.sum()),
                ", ".join(self.exclude_states),
                len(df),
                int((~excluded_mask).sum()),
            )
            df = df[~excluded_mask].reset_index(drop=True)

        return df

    def _apply_region_exclusions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop stores whose ``region_column`` value is in ``excluded_regions``.

        Excluded stores are out of scope (not rejected): they are appended to
        ``self._excluded`` (with ``exclusion_reason='excluded_region'``) and
        no later step reassigns them to a market. Matching is
        whitespace-insensitive and case-insensitive.

        Args:
            df: Input stores DataFrame.

        Returns:
            The DataFrame without the excluded stores.

        Raises:
            ComponentError: If ``excluded_regions`` is configured but the
                ``region_column`` is missing from the input DataFrame.
        """
        if not self.excluded_regions:
            return df

        if self.region_column not in df.columns:
            raise ComponentError(
                f"excluded_regions is configured but column "
                f"'{self.region_column}' is missing from the input DataFrame."
            )

        regions = df[self.region_column].astype(str).str.strip().str.casefold()
        excluded_mask = regions.isin(self.excluded_regions)
        if excluded_mask.any():
            dropped = df[excluded_mask].copy()
            dropped['exclusion_reason'] = 'excluded_region'
            self._excluded = (
                dropped if self._excluded.empty
                else pd.concat([self._excluded, dropped])
            )
            self._logger.info(
                "excluded_regions: dropped %s stores in %s (%s -> %s)",
                int(excluded_mask.sum()),
                ", ".join(self.excluded_regions),
                len(df),
                int((~excluded_mask).sum()),
            )
            df = df[~excluded_mask].reset_index(drop=True)

        return df

    def _validate_region_config(self, df: pd.DataFrame) -> None:
        """Fail-fast validation of the FEAT-247 region hard-constraint.

        A no-op when ``region_column`` is not configured. Must run AFTER
        exclusions (``exclude_states`` / ``excluded_regions``) so
        out-of-scope rows never trip these checks (spec §2).

        Args:
            df: The input stores DataFrame, post-exclusions.

        Raises:
            ConfigError: If ``region_column`` is missing from ``df``, any
                row has a null/empty/whitespace region value, a
                ``standalone_markets`` group spans more than one region,
                or the number of distinct regions exceeds ``max_markets``
                (each region needs at least one market of its own).
        """
        if not self.region_column:
            return

        if self.region_column not in df.columns:
            raise ConfigError(
                f"region_column is configured but column "
                f"'{self.region_column}' is missing from the input DataFrame."
            )

        region_values = df[self.region_column]
        is_null_or_blank = (
            region_values.isna()
            | (region_values.astype(str).str.strip() == '')
        )
        if is_null_or_blank.any():
            raise ConfigError(
                f"{int(is_null_or_blank.sum())} row(s) have a null/empty/"
                f"whitespace '{self.region_column}' value; region_column "
                "requires a value on every row (fail fast, spec §2)."
            )

        if self._standalone_groups:
            if not self.isolation_column or self.isolation_column not in df.columns:
                raise ConfigError(
                    "standalone_markets is configured but isolation_column "
                    f"'{self.isolation_column}' is missing from the input "
                    "DataFrame."
                )
            isolation_values = df[self.isolation_column]
            for group in self._standalone_groups:
                group_mask = isolation_values.isin(group)
                group_regions = set(df.loc[group_mask, self.region_column].unique())
                if len(group_regions) > 1:
                    raise ConfigError(
                        "standalone_markets group "
                        f"{self._format_standalone_group(group)} spans "
                        f"more than one region ({sorted(group_regions)}); "
                        "every standalone market must be region-pure."
                    )

        number_of_regions = int(region_values.nunique())
        if self.max_markets is not None and number_of_regions > self.max_markets:
            raise ConfigError(
                f"max_markets={self.max_markets} cannot fit "
                f"{number_of_regions} regions (each region needs at least "
                "one market); raise max_markets or drop region_column."
            )

        self._logger.info(
            "region_column '%s': %s distinct regions, state_score_weights=%s",
            self.region_column, number_of_regions, self.state_score_weights,
        )

    def _partition_mask(self, stores: pd.DataFrame) -> Optional[pd.Series]:
        """Return the isolation partition of each store (True = isolated).

        Returns ``None`` when isolation is not configured or the isolation
        column is not present in the DataFrame.
        """
        if (
            self.isolation_column
            and self.isolation_values
            and self.isolation_column in stores.columns
        ):
            return stores[self.isolation_column].isin(self.isolation_values)

        return None

    def _partition_market_quotas(
        self, partition: Optional[pd.Series]
    ) -> Optional[Dict[bool, int]]:
        """Split ``max_markets`` proportionally between isolation partitions.

        The isolated partition reserves the larger of its proportional share
        of ``max_markets`` and the minimum number of markets needed to fit
        its stores under ``max_cluster_size``, so the rest of the network can
        never consume the whole cap before the isolated group gets a market.

        Args:
            partition: Boolean mask marking isolated stores, or ``None``.

        Returns:
            ``{True: k_isolated, False: k_rest}``, or ``None`` when quotas do
            not apply (no cap, no isolation, or a single-partition input).
        """
        if self.max_markets is None or partition is None:
            return None

        n_total = int(len(partition))
        n_isolated = int(partition.sum())
        if n_isolated == 0 or n_isolated == n_total:
            return None

        k_isolated = max(
            math.ceil(n_isolated / self.max_cluster_size),
            round(n_isolated / n_total * self.max_markets),
            1,
        )
        k_isolated = min(k_isolated, self.max_markets - 1)

        return {True: k_isolated, False: self.max_markets - k_isolated}

    # ------------------------------------------------------------------
    # FTE Calculations
    # ------------------------------------------------------------------

    def _calculate_cluster_avg_distance(self, cluster_df: pd.DataFrame) -> float:
        """Estimate the average travel leg between stores in a cluster.

        Uses the mean nearest-neighbour hop — how a person actually routes
        between adjacent stores — scaled by ``travel_route_factor`` (default
        1.3) to account for imperfect route ordering and return legs. The
        mean pairwise distance is deliberately NOT used: it assumes every
        visit crosses the whole market and overstates travel severely
        (~9x on real data).
        """
        if len(cluster_df) < 2:
            return 0.0

        coords = cluster_df[['latitude', 'longitude']].values
        n = len(coords)
        dist_matrix = np.full((n, n), np.inf)

        for i in range(n):
            for j in range(i + 1, n):
                dist = self._haversine_miles(
                    coords[i][0], coords[i][1],
                    coords[j][0], coords[j][1]
                )
                dist_matrix[i, j] = dist_matrix[j, i] = dist

        nearest_hops = dist_matrix.min(axis=1)
        return float(nearest_hops.mean() * self.travel_route_factor)

    @staticmethod
    def _parse_cadence_rules(
        rules: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[Dict[str, float]]]:
        """Validate and normalize distance-based visit cadence rules.

        Args:
            rules: Raw rule definitions, each with ``min_distance`` (default 0),
                ``max_distance`` (``None`` means unbounded) and ``visits``.

        Returns:
            Rules sorted by ``min_distance`` with float values, or ``None``
            when no rules were provided.

        Raises:
            ConfigError: If a rule is malformed, has non-positive visits,
                an inverted range, or ranges overlap.
        """
        if not rules:
            return None

        parsed: List[Dict[str, float]] = []
        for rule in rules:
            if not isinstance(rule, dict):
                raise ConfigError(
                    f"visit_cadence_rules entries must be dicts, got {rule!r}"
                )
            try:
                min_distance = float(rule.get('min_distance', 0.0))
                max_distance = rule.get('max_distance', None)
                if max_distance is not None:
                    max_distance = float(max_distance)
                visits = float(rule['visits'])
            except KeyError as exc:
                raise ConfigError(
                    f"visit_cadence_rules entry missing 'visits': {rule!r}"
                ) from exc
            except (TypeError, ValueError) as exc:
                raise ConfigError(
                    f"visit_cadence_rules entry has non-numeric values: {rule!r}"
                ) from exc

            if visits <= 0:
                raise ConfigError(
                    f"visit_cadence_rules 'visits' must be > 0, got {visits}"
                )
            if min_distance < 0:
                raise ConfigError(
                    f"visit_cadence_rules 'min_distance' must be >= 0, got {min_distance}"
                )
            if max_distance is not None and max_distance <= min_distance:
                raise ConfigError(
                    "visit_cadence_rules 'max_distance' must be greater than "
                    f"'min_distance': {rule!r}"
                )
            parsed.append(
                {
                    'min_distance': min_distance,
                    'max_distance': max_distance,
                    'visits': visits,
                }
            )

        parsed.sort(key=lambda r: r['min_distance'])
        for previous, current in zip(parsed, parsed[1:]):
            if previous['max_distance'] is None or current['min_distance'] < previous['max_distance']:
                raise ConfigError(
                    "visit_cadence_rules ranges overlap: "
                    f"{previous!r} and {current!r}"
                )
        return parsed

    def _resolve_cadence_visits(self, distance: float) -> Optional[float]:
        """Return the visits defined by the rule containing ``distance``.

        Ranges are semi-open: ``min_distance <= distance < max_distance``.
        A ``max_distance`` of ``None`` means unbounded.

        Args:
            distance: Distance to the cluster center (same unit as
                ``distance_to_center``, i.e. miles).

        Returns:
            The configured visits, or ``None`` when the distance is NaN or
            matches no rule.
        """
        if not self.visit_cadence_rules or distance is None or np.isnan(distance):
            return None
        for rule in self.visit_cadence_rules:
            upper = rule['max_distance']
            if distance >= rule['min_distance'] and (upper is None or distance < upper):
                return rule['visits']
        return None

    def _apply_cadence_rules(self, df: pd.DataFrame) -> None:
        """Fill the visit-frequency column from distance-based cadence rules.

        Precedence per store: an existing non-null value in
        ``visit_frequency_column`` wins, then the matching cadence rule,
        then ``default_visit_frequency``. Adds a boolean
        ``cadence_rule_applied`` column flagging stores whose frequency
        came from a rule. No-op when no rules are configured or the
        ``distance_to_center`` column is missing.

        Args:
            df: Result DataFrame with a ``distance_to_center`` column.
        """
        if not self.visit_cadence_rules or 'distance_to_center' not in df.columns:
            return

        column = self.visit_frequency_column or 'visit_frequency'
        # Snapshot the user-provided frequencies on the first application so
        # later passes (after rebalancing) re-evaluate rule-derived values
        # instead of treating them as user data.
        if self._cadence_user_freq is None:
            if column in df.columns:
                self._cadence_user_freq = pd.to_numeric(df[column], errors='coerce')
            else:
                self._cadence_user_freq = pd.Series(np.nan, index=df.index, dtype=float)
        existing = self._cadence_user_freq.reindex(df.index)

        distances = pd.to_numeric(df['distance_to_center'], errors='coerce')

        resolved: List[float] = []
        applied: List[bool] = []
        unmatched = 0
        for idx in df.index:
            current = existing.loc[idx]
            if not np.isnan(current):
                resolved.append(float(current))
                applied.append(False)
                continue
            visits = self._resolve_cadence_visits(distances.loc[idx])
            if visits is not None:
                resolved.append(visits)
                applied.append(True)
            else:
                if not np.isnan(distances.loc[idx]):
                    unmatched += 1
                default = self.default_visit_frequency
                resolved.append(default if default is not None else np.nan)
                applied.append(False)

        df[column] = resolved
        df['cadence_rule_applied'] = applied

        if unmatched:
            self._logger.warning(
                f"{unmatched} stores matched no visit_cadence_rules range; "
                "falling back to the default visit frequency"
            )

    def _apply_visit_rule_columns(self, df: pd.DataFrame) -> None:
        """Emit the visit columns in the shape SchedulingVisits expects.

        SchedulingVisits reads two separate columns: ``visit_rule`` — HOW MANY
        visits (1, 2, 3...) — and ``visit_frequency`` — the cadence rule those
        visits follow (``Monthly``, ``Weekly``, ``Bi-Weekly``). Internally the
        clustering computes the count under ``visit_frequency_column``, so
        this last step renames the count to ``visit_rule_column`` and stamps
        the rule column with ``visit_frequency_rule``.

        When no per-store count exists at all (no cadence rules and no input
        column) the count falls back to ``visit_frequency`` (the configured
        default), so the downstream contract always holds.

        Args:
            df: The final result DataFrame, modified in place.
        """
        source = self.visit_frequency_column or 'visit_frequency'
        target = self.visit_rule_column

        if target != source and source in df.columns:
            # Drop any stale target first: rename must not create duplicates
            if target in df.columns:
                df.drop(columns=[target], inplace=True)
            df.rename(columns={source: target}, inplace=True)

        if target not in df.columns:
            if self.default_visit_frequency is None:
                self._logger.warning(
                    "No visit counts available: '%s' is missing from the "
                    "result and no default visit_frequency is configured.",
                    target,
                )
                return
            df[target] = self.default_visit_frequency

        if self.visit_frequency_rule_column == target:
            self._logger.warning(
                "visit_frequency_rule_column and visit_rule_column are both "
                "%r; the cadence rule name was not added.", target,
            )
            return

        df[self.visit_frequency_rule_column] = self.visit_frequency_rule

    def _get_cluster_visit_frequencies(self, cluster_df: pd.DataFrame) -> Optional[pd.Series]:
        """Return per-store visit frequencies when available."""
        if self.visit_frequency_column and self.visit_frequency_column in cluster_df.columns:
            return pd.to_numeric(cluster_df[self.visit_frequency_column], errors='coerce')

        return None

    def _get_cluster_in_store_hours(self, cluster_df: pd.DataFrame) -> Optional[pd.Series]:
        """Return per-store in-store hours when available."""
        if self.in_store_hours_column and self.in_store_hours_column in cluster_df.columns:
            return pd.to_numeric(cluster_df[self.in_store_hours_column], errors='coerce')

        return None

    def _get_num_ghosts_for_cluster(self, cid: int, cluster_df: pd.DataFrame) -> int:
        """
        Determine the number of ghost employees for a cluster.

        When FTE constraints are enabled, an optimization routine decides the
        number of employees. Otherwise the configured `num_ghosts_per_cluster`
        is used, but FTE metrics are still computed for reporting.
        """
        # Check if 'fte' column already exists (from previous calculation).
        # A forced num_ghosts_per_cluster is a hard value: skip the shortcut.
        if not self._forced_num_ghosts and 'fte' in cluster_df.columns:
            fte_values = cluster_df['fte'].dropna().unique()
            if len(fte_values) > 0:
                fte_value = fte_values[0]
                if pd.notna(fte_value) and fte_value > 0:
                    return max(1, int(fte_value))

        if self.fte_calculator is None:
            return self.num_ghosts_per_cluster

        num_stores = len(cluster_df)
        avg_distance = self._calculate_cluster_avg_distance(cluster_df)
        visit_frequencies = self._get_cluster_visit_frequencies(cluster_df)
        in_store_hours = self._get_cluster_in_store_hours(cluster_df)

        if self.use_fte_constraints and not self._forced_num_ghosts:
            optimization_result = self.fte_calculator.optimize_num_employees(
                num_stores=num_stores,
                avg_distance=avg_distance,
                max_stores_per_employee=self.max_stores_per_day,
                visit_frequencies=visit_frequencies,
                in_store_hours=in_store_hours,
            )
            cluster_info = optimization_result
        else:
            num_ghosts = self.num_ghosts_per_cluster
            if isinstance(num_ghosts, list):
                num_ghosts = num_ghosts[0] if num_ghosts else 1

            if not num_ghosts or num_ghosts < 1:
                num_ghosts = 1

            cluster_hours = self.fte_calculator.calculate_cluster_hours(
                num_stores=num_stores,
                avg_distance_between_stores=avg_distance,
                visit_frequencies=visit_frequencies,
                in_store_hours=in_store_hours,
                num_employees=num_ghosts,
            )
            fte_totals = self.fte_calculator.calculate_fte_requirements(cluster_hours)

            # FIXED: Calculate per-employee hours correctly by dividing cluster totals
            hours_per_emp_daily = cluster_hours['daily_hours'] / num_ghosts
            hours_per_emp_weekly = cluster_hours['weekly_hours'] / num_ghosts
            hours_per_emp_monthly = cluster_hours['monthly_hours'] / num_ghosts

            # DETECT constraint violations (but don't auto-fix)
            constraint_violated = False
            constraint_warning = None
            suggested_employees = num_ghosts

            # Check if daily hours constraint is violated
            if (
                self.day_hours is not None
                and self.day_hours > 0
                and hours_per_emp_daily > self.day_hours + 1e-6
            ):
                constraint_violated = True
                suggested_employees_daily = math.ceil(cluster_hours['daily_hours'] / self.day_hours)
                suggested_employees = max(suggested_employees, suggested_employees_daily)

            # Check if weekly hours constraint is violated
            if (
                self.hours_per_week is not None
                and self.hours_per_week > 0
                and hours_per_emp_weekly > self.hours_per_week + 1e-6
            ):
                constraint_violated = True
                suggested_employees_weekly = math.ceil(cluster_hours['weekly_hours'] / self.hours_per_week)
                suggested_employees = max(suggested_employees, suggested_employees_weekly)

            stores_per_employee = (
                num_stores / num_ghosts if num_ghosts else np.nan
            )
            # max_stores_per_day is a DAILY route limit. The comparable
            # figure is visits per working day (the monthly cadence spread
            # over the month), NOT the monthly portfolio size.
            working_days_month = (
                self.working_days_per_week * 4.0
                if self.working_days_per_week else 0.0
            )
            monthly_visits = cluster_hours.get('monthly_visits', 0.0)
            visits_per_day_per_employee = (
                monthly_visits / working_days_month / num_ghosts
                if num_ghosts and working_days_month > 0 else np.nan
            )
            stores_limit_exceeded = (
                pd.notna(visits_per_day_per_employee)
                and self.max_stores_per_day is not None
                and self.max_stores_per_day > 0
                and visits_per_day_per_employee > self.max_stores_per_day
            )
            if stores_limit_exceeded:
                constraint_violated = True
                suggested_employees_store = math.ceil(
                    monthly_visits / working_days_month / self.max_stores_per_day
                )
                suggested_employees = max(suggested_employees, suggested_employees_store)

            # Set warning message if violated
            if constraint_violated:
                warning_parts = [
                    f"CONSTRAINT VIOLATED: Cluster needs {suggested_employees} employees (configured: {num_ghosts})."
                ]

                if self.day_hours is not None and self.day_hours > 0:
                    warning_parts.append(
                        f"Hours: {hours_per_emp_daily:.1f}h/day (limit: {self.day_hours}h)"
                    )
                if self.hours_per_week is not None and self.hours_per_week > 0:
                    warning_parts.append(
                        f"{hours_per_emp_weekly:.1f}h/week (limit: {self.hours_per_week}h)"
                    )
                if stores_limit_exceeded:
                    warning_parts.append(
                        f"Visits: {visits_per_day_per_employee:.1f}/day per employee "
                        f"(limit: {self.max_stores_per_day}/day)"
                    )

                constraint_warning = " ".join(warning_parts)
                if self._constraints_enforcement_enabled():
                    self._logger.error(f"Cluster {cid}: {constraint_warning}")
                    self._constraint_rebalance_required = True
                else:
                    # Headcount is forced / enforcement is off: informational only
                    self._logger.warning(f"Cluster {cid}: {constraint_warning}")

            cluster_info = {
                'num_employees': num_ghosts,
                **fte_totals,
                'daily_hours': cluster_hours['daily_hours'],
                'weekly_hours': cluster_hours['weekly_hours'],
                'monthly_hours': cluster_hours['monthly_hours'],
                'hours_per_employee_daily': hours_per_emp_daily,
                'hours_per_employee_weekly': hours_per_emp_weekly,
                'hours_per_employee_monthly': hours_per_emp_monthly,
                'stores_per_employee': stores_per_employee,
                'visits_per_day_per_employee': visits_per_day_per_employee,
                'in_store_hours_effective': cluster_hours.get('effective_in_store_hours', np.nan),
                'constraint_warning': constraint_warning,
                'constraint_violated': constraint_violated,
                'suggested_employees': suggested_employees,
                'range_expanded': False,
                'fte_ratio_per_employee': self.fte_calculator.fte_monthly_per_employee(
                    hours_per_emp_monthly
                ),
                'fte_monthly_per_employee': self.fte_calculator.fte_monthly_per_employee(
                    hours_per_emp_monthly
                ),
                'fte_daily_per_employee': self.fte_calculator.fte_daily_per_employee(
                    hours_per_emp_daily
                ),
                'monthly_hours_per_employee': hours_per_emp_monthly,
                'daily_hours_per_employee': hours_per_emp_daily,
            }

        self._cluster_fte_info[cid] = cluster_info
        num_ghosts = cluster_info.get('num_employees', self.num_ghosts_per_cluster)

        self._logger.debug(
            f"Cluster {cid}: {num_stores} stores, "
            f"avg_dist={avg_distance:.1f}mi, "
            f"num_employees={num_ghosts}, "
            f"fte_daily_cluster={cluster_info.get('fte_daily_cluster', np.nan):.2f}, "
            f"fte_monthly_cluster={cluster_info.get('fte_monthly_cluster', np.nan):.2f}"
        )

        return num_ghosts

    def _constraints_enforcement_enabled(self) -> bool:
        """Return True when configuration allows automatic constraint enforcement."""
        if self.fte_calculator is None or self._data.empty:
            return False

        if self.use_fte_constraints:
            return True

        # Without FTE constraints enabled we avoid any automatic rebalancing.
        return False

    def _add_fte_columns_to_result(self, df: pd.DataFrame):
        """Add FTE-related columns to the result DataFrame with proper dtypes."""

        # Define columns with their expected dtypes
        numeric_columns = [
            'fte_daily_cluster', 'fte_monthly_cluster', 'num_employees',
            'suggested_employees',
            'daily_hours', 'weekly_hours', 'monthly_hours',
            'hours_per_employee_daily', 'hours_per_employee_weekly',
            'hours_per_employee_monthly', 'daily_hours_per_employee',
            'monthly_hours_per_employee', 'stores_per_employee',
            'fte_monthly_per_employee', 'fte_daily_per_employee',
            'fte_ratio_per_employee'
        ]

        boolean_columns = ['range_expanded', 'constraint_violated']
        string_columns = ['constraint_warning']

        # Initialize numeric columns with NaN
        for col in numeric_columns:
            df[col] = np.nan

        # Initialize boolean columns with False
        for col in boolean_columns:
            df[col] = False

        # Initialize string columns with empty string
        for col in string_columns:
            df[col] = ''

        for cid in df[self._cluster_id].unique():
            if cid == -1:  # Skip outliers
                continue

            if cid in self._cluster_fte_info:
                info = self._cluster_fte_info[cid]
                mask = df[self._cluster_id] == cid

                # FIXED: Use .get() with defaults and use fte_daily_cluster/fte_monthly_cluster
                df.loc[mask, 'fte_daily_cluster'] = info.get('fte_daily_cluster', np.nan)
                df.loc[mask, 'fte_monthly_cluster'] = info.get('fte_monthly_cluster', np.nan)
                df.loc[mask, 'num_employees'] = info.get('num_employees', np.nan)
                df.loc[mask, 'suggested_employees'] = info.get('suggested_employees', np.nan)
                df.loc[mask, 'daily_hours'] = info.get('daily_hours', np.nan)
                df.loc[mask, 'weekly_hours'] = info.get('weekly_hours', np.nan)
                df.loc[mask, 'monthly_hours'] = info.get('monthly_hours', np.nan)
                df.loc[mask, 'hours_per_employee_daily'] = info.get('hours_per_employee_daily', np.nan)
                df.loc[mask, 'hours_per_employee_weekly'] = info.get('hours_per_employee_weekly', np.nan)
                df.loc[mask, 'hours_per_employee_monthly'] = info.get('hours_per_employee_monthly', np.nan)
                df.loc[mask, 'stores_per_employee'] = info.get('stores_per_employee', np.nan)
                df.loc[mask, 'fte_monthly_per_employee'] = info.get('fte_monthly_per_employee', np.nan)
                df.loc[mask, 'fte_daily_per_employee'] = info.get('fte_daily_per_employee', np.nan)
                df.loc[mask, 'fte_ratio_per_employee'] = info.get('fte_ratio_per_employee', np.nan)
                df.loc[mask, 'daily_hours_per_employee'] = info.get('daily_hours_per_employee', np.nan)
                df.loc[mask, 'monthly_hours_per_employee'] = info.get('monthly_hours_per_employee', np.nan)

                # Boolean columns (no more FutureWarning)
                df.loc[mask, 'range_expanded'] = bool(info.get('range_expanded', False))
                df.loc[mask, 'constraint_violated'] = bool(info.get('constraint_violated', False))

                # String columns (no more FutureWarning)
                df.loc[mask, 'constraint_warning'] = str(info.get('constraint_warning', ''))

    def _log_fte_summary(self):
        """Log summary of FTE calculations across all clusters."""
        if not self._cluster_fte_info:
            return

        # FIXED: Use .get() to prevent KeyError and use fte_daily_cluster/fte_monthly_cluster
        total_fte_daily = sum(info.get('fte_daily_cluster', 0) for info in self._cluster_fte_info.values())
        total_fte_monthly = sum(info.get('fte_monthly_cluster', 0) for info in self._cluster_fte_info.values())
        total_employees = sum(info.get('num_employees', 0) for info in self._cluster_fte_info.values())

        self._logger.info("=== FTE Summary ===")
        self._logger.info(f"Total FTE Daily: {total_fte_daily:.2f}")
        self._logger.info(f"Total FTE Monthly: {total_fte_monthly:.2f}")
        self._logger.info(f"Total Ghost Employees: {total_employees}")
        self._logger.info(f"Number of Clusters: {len(self._cluster_fte_info)}")

        if self.fte_monthly:
            target = self.fte_monthly
            per_employee_hours = [
                info.get('hours_per_employee_monthly')
                for info in self._cluster_fte_info.values()
                if info.get('hours_per_employee_monthly') is not None
            ]

            if per_employee_hours:
                avg_hours = float(np.mean(per_employee_hours))
                max_diff = max(abs(hours - target) for hours in per_employee_hours)
                max_pct_diff = (max_diff / target) * 100 if target else 0

                self._logger.info(f"Monthly Hours Target per Employee: {target:.2f}")
                self._logger.info(f"Average Monthly Hours per Employee: {avg_hours:.2f}")
                self._logger.info(f"Max deviation from target: {max_diff:.2f} ({max_pct_diff:.1f}%)")

                if max_pct_diff <= 10:
                    self._logger.info("✓ All employees within 10% target margin")
                else:
                    self._logger.warning("⚠ Monthly hours exceed 10% margin for at least one employee")

        # Per-cluster breakdown
        self._logger.info("\nPer-Cluster FTE Breakdown:")
        for cid, info in sorted(self._cluster_fte_info.items()):
            warning = info.get('constraint_warning')
            range_note = info.get('range_expanded')
            extras = []
            if warning:
                extras.append(f"warning={warning}")
            if range_note:
                extras.append("range_expanded")
            extra_msg = f" ({', '.join(extras)})" if extras else ""
            self._logger.info(
                (
                    f"  Cluster {cid}: {info['num_employees']} employees, "
                    f"FTE_daily={info['fte_daily']:.2f}, "
                    f"FTE_monthly={info['fte_monthly']:.2f}, "
                    f"stores/emp={info.get('stores_per_employee', 0):.1f}, "
                    f"hours/emp(month)={info.get('hours_per_employee_monthly', 0):.1f}"
                    f"{extra_msg}"
                )
            )

    def _log_employee_budget_summary(self) -> None:
        """Log what the global employee-budget consolidation did (FEAT-240).

        The one block that makes a budget-mode run auditable: headcount
        required against ``max_employees`` (and the slack left), how many
        merges were applied and the resulting market count, headcount saved
        by consolidating, and whether the relaxed-geometry round ran.
        """
        # Uses the SAME expression _consolidate_markets_for_headcount
        # actually checked against max_employees (via _total_headcount /
        # _market_employees, floor 1 per live market), rather than
        # independently re-summing _cluster_fte_info with a different
        # default — so the two can never quietly drift apart.
        total_employees = self._total_headcount()
        slack = (
            self.max_employees - total_employees
            if self.max_employees is not None else None
        )
        # The ComponentError raised inside _consolidate_markets_for_
        # headcount means run() never reaches this call with a negative
        # slack — logged as an ERROR rather than crashing, in case that
        # invariant is ever broken.
        headcount_log = (
            self._logger.error if slack is not None and slack < 0
            else self._logger.info
        )

        self._logger.info("=== Employee Budget ===")
        self._logger.info("max_employees: %s", self.max_employees)
        headcount_log("Headcount required: %s (slack: %s)", total_employees, slack)
        self._logger.info(
            "Merges applied: %s (markets %s -> %s)",
            self._budget_merges_applied,
            self._budget_markets_before,
            self._budget_markets_after,
        )
        self._logger.info(
            "Headcount saved by consolidation: %s", self._budget_headcount_saved
        )
        self._logger.info(
            "Relaxed-geometry round: %s",
            "yes" if self._budget_relaxed_round_used else "no",
        )

    def _log_per_region_summary(
        self, region_values: List[Any], undersized_regions: List[Any]
    ) -> None:
        """Log the FEAT-247 per-region formation summary + global totals.

        One block, style of ``_log_employee_budget_summary``: markets
        formed per region, undersized regions (spec §2: "one undersized
        market... never merged across regions"), and capacity cessions
        (from the additive ``ceded_from`` column TASK-198 stamps).
        Numbers come straight from the columns/state earlier tasks
        already produced — never re-derived independently, so this can
        never drift from what was actually decided (spec §7 "Summary
        numbers must come from the ledgers stamped by earlier tasks").

        Args:
            region_values: Sorted distinct region values processed by
                ``run()``'s per-region loop (in that same order).
            undersized_regions: Subset of ``region_values`` that formed
                exactly one undersized market.
        """
        if self._data.empty:
            return

        self._logger.info("=== Per-Region Formation (FEAT-247) ===")
        delivered = self._data[self._data[self._cluster_id] != -1]
        total_ceded = 0
        has_ceded_from = 'ceded_from' in self._data.columns

        for region_value in region_values:
            region_rows = delivered[delivered['region'] == region_value]
            market_count = int(region_rows[self._cluster_id].nunique())
            cession_count = (
                int(region_rows['ceded_from'].notna().sum())
                if has_ceded_from else 0
            )
            total_ceded += cession_count
            self._logger.info(
                "Region %r: %s market(s), %s store(s)%s%s",
                region_value, market_count, len(region_rows),
                " (undersized)" if region_value in undersized_regions else "",
                f", {cession_count} ceded store(s)" if cession_count else "",
            )

        if total_ceded:
            self._logger.info(
                "Total capacity cessions: %s store(s) moved by in-region "
                "cession passes.", total_ceded,
            )

    # -------------------------------- BallTree + Haversine ----------------------------------
    # ------------------------------------------------------------------

    def _detect_outliers(
        self,
        stores: pd.DataFrame,
        cluster_label: int,
        cluster_indices: List[int]
    ) -> List[int]:
        """
        1) Compute centroid of all stores in 'cluster_indices'.
        2) Check each store in that cluster: if dist(store -> centroid) >
            self.max_cluster_distance, mark as outlier.
        3) Return a list of outlier indices.
        """
        if not cluster_indices:
            return []

        # coordinates of cluster
        arr = stores.loc[cluster_indices, ['latitude', 'longitude']].values

        # Simple approach: K-Means with n_clusters=1
        # This basically finds the centroid that minimizes sum of squares.
        km = KMeans(n_clusters=1, random_state=42).fit(arr)
        centroid = km.cluster_centers_[0]  # [lat, lon]

        # Store the centroid for this cluster
        self._cluster_centroids[cluster_label] = {
            'centroid_lat': centroid[0],
            'centroid_lon': centroid[1]
        }

        outliers = []
        for idx in cluster_indices:
            store_lat = stores.at[idx, 'latitude']
            store_lon = stores.at[idx, 'longitude']
            d = self._haversine_miles(centroid[0], centroid[1], store_lat, store_lon)
            if d > (self.max_cluster_distance + self.borderline_threshold):
                outliers.append(idx)
        self._outlier_stores.update(outliers)  # Track outliers globally
        return outliers

    def _validate_distance(self, stores, cluster_stores: pd.DataFrame):
        """
        Validates distances between neighbors using precomputed distances.
        Args:
            coords_rad (ndarray): Array of [latitude, longitude] in radians.
            neighbors (ndarray): Array of indices of neighbors.
            distances (ndarray): Distances from the query point to each neighbor.
        """
        # Convert max_cluster_distance (in miles) to radians
        max_distance_radians = miles_to_radians(
            self.max_cluster_distance + self.borderline_threshold
        )

        # Extract coordinates of the stores in the cluster
        cluster_coords = cluster_stores[['latitude', 'longitude']].values
        cluster_indices = cluster_stores.index.tolist()

        # Iterate through each store in the cluster
        outliers = []
        for idx, (store_lat, store_lon) in zip(cluster_indices, cluster_coords):
            # Compute the traveled distance using OSMnx to all other stores in the cluster
            traveled_distances = []
            for neighbor_idx, (neighbor_lat, neighbor_lon) in zip(cluster_indices, cluster_coords):
                if idx == neighbor_idx:
                    continue  # Skip self-distance
                try:
                    # Calculate the traveled distance using OSMnx (network distance)
                    traveled_distance = self._osmnx_travel_distance(
                        store_lat, store_lon, neighbor_lat, neighbor_lon
                    )
                    traveled_distances.append(traveled_distance)
                except Exception as e:
                    print(f"Error calculating distance for {idx} -> {neighbor_idx}: {e}")

            # Check if the maximum traveled distance exceeds the threshold
            if traveled_distances and max(traveled_distances) > max_distance_radians:
                outliers.append(idx)
                # Mark store as unassigned
                stores.at[idx, self._cluster_id] = -1

        return outliers

    def _post_process_outliers(self, stores: pd.DataFrame, unassigned: set):
        """
        Assign unassigned stores to the nearest cluster using relaxed distance criteria.
        """
        if not unassigned:
            return

        # FEAT-248 TASK-205: this surface scores via _nearest_absorbing_market
        # below; reset the cache at its top like every other scoring surface.
        self._reset_state_score_cache()

        # Get cluster centroids and current sizes (to honour max_cluster_size)
        clusters = stores[stores[self._cluster_id] != -1].groupby(self._cluster_id)
        centroids = {
            cluster_id: cluster_df[['latitude', 'longitude']].mean().values
            for cluster_id, cluster_df in clusters
        }
        cluster_sizes = {
            cluster_id: len(cluster_df) for cluster_id, cluster_df in clusters
        }

        # Relaxed distance threshold
        relaxed_threshold = self.cluster_radius + self.relaxed_threshold

        partition = self._partition_mask(stores)

        for outlier_idx in list(unassigned):
            outlier_lat = stores.at[outlier_idx, 'latitude']
            outlier_lon = stores.at[outlier_idx, 'longitude']

            eligible = {
                cluster_id: (centroid[0], centroid[1])
                for cluster_id, centroid in centroids.items()
                if cluster_id not in self._standalone_clusters  # frozen markets
                and (
                    partition is None
                    or self._cluster_partition.get(cluster_id, False)
                    == bool(partition.loc[outlier_idx])
                )
            }

            # Nearby absorption first: within max_assign_distance the size
            # cap is soft, so a store next to a full market joins it instead
            # of being shipped to a distant market with room.
            entity_state = (
                stores.at[outlier_idx, self.state_column]
                if self.state_column in stores.columns else None
            )
            choice = self._nearest_absorbing_market(
                outlier_lat, outlier_lon, eligible, cluster_sizes,
                self._max_force_assign_distance,
                entity_state=entity_state,
            )
            if choice is None:
                # Fallback: nearest cluster WITH capacity within the relaxed
                # clustering radius
                nearest_cluster = None
                min_distance = float('inf')
                for cluster_id, (center_lat, center_lon) in eligible.items():
                    if cluster_sizes.get(cluster_id, 0) >= self._capacity_for(cluster_id):
                        continue  # Cluster is already full
                    distance = self._haversine_miles(
                        center_lat, center_lon, outlier_lat, outlier_lon
                    )
                    if distance < relaxed_threshold and distance < min_distance:
                        nearest_cluster = cluster_id
                        min_distance = distance
                if nearest_cluster is not None:
                    choice = (nearest_cluster, min_distance, False)

            # Assign to the chosen cluster if valid
            if choice is not None:
                nearest_cluster, _, overfilled = choice
                stores.at[outlier_idx, self._cluster_id] = nearest_cluster
                cluster_sizes[nearest_cluster] = cluster_sizes.get(nearest_cluster, 0) + 1
                if overfilled:
                    self._outlier_stores.add(outlier_idx)
                else:
                    self._outlier_stores.discard(outlier_idx)
                unassigned.remove(outlier_idx)

        print(f"Post-processing completed. Remaining unassigned: {len(unassigned)}")

    def _force_assign_to_nearest_market(self, stores: pd.DataFrame, indices: List[int]):
        """
        Assign the given stores to their nearest market regardless of distance,
        keeping them flagged as outliers.

        FEAT-247: the receiving market is chosen by state-affinity score
        (``_nearest_absorbing_market``), not pure distance.
        """
        self._reset_state_score_cache()
        clusters = stores[stores[self._cluster_id] != -1].groupby(self._cluster_id)
        centroids = {
            cluster_id: cluster_df[['latitude', 'longitude']].mean().values
            for cluster_id, cluster_df in clusters
        }
        cluster_sizes = {
            cluster_id: len(cluster_df) for cluster_id, cluster_df in clusters
        }
        if not centroids:
            return

        partition = self._partition_mask(stores)

        for idx in indices:
            store_lat = stores.at[idx, 'latitude']
            store_lon = stores.at[idx, 'longitude']
            # Isolation outranks force-assignment: only clusters of the
            # store's own partition are eligible; standalone markets never
            # receive outside stores.
            eligible = [
                cid for cid in centroids if cid not in self._standalone_clusters
            ]
            if not eligible:
                self._logger.warning(
                    "Store at index %s cannot be force-assigned: every market "
                    "is a frozen standalone market.",
                    idx,
                )
                continue
            if partition is not None:
                store_partition = bool(partition.loc[idx])
                eligible = [
                    cid for cid in eligible
                    if self._cluster_partition.get(cid, False) == store_partition
                ]
                if not eligible:
                    self._logger.warning(
                        "Store at index %s has no market in its isolation "
                        "partition; it stays unassigned to preserve isolation.",
                        idx,
                    )
                    continue
            # Nearby absorption first: within max_assign_distance the size
            # cap is soft, so the orphan overfills the market next door
            # rather than travelling to a distant market with room.
            entity_state = (
                stores.at[idx, self.state_column]
                if self.state_column in stores.columns else None
            )
            choice = self._nearest_absorbing_market(
                store_lat, store_lon,
                {cid: (centroids[cid][0], centroids[cid][1]) for cid in eligible},
                cluster_sizes,
                self._max_force_assign_distance,
                entity_state=entity_state,
            )
            if choice is not None:
                nearest_cluster, choice_distance, overfilled = choice
                if overfilled:
                    self._logger.warning(
                        "Every market within %s miles is at max_cluster_size=%s; "
                        "assigning store index %s to market %s (%.1f miles) "
                        "beyond the limit.",
                        self._max_force_assign_distance,
                        self.max_cluster_size,
                        idx,
                        nearest_cluster,
                        choice_distance,
                    )
            else:
                # Nothing within reach: prefer the nearest cluster that still
                # has capacity; if every cluster is full, fall back to the
                # nearest one (nobody may be left unassigned by this method)
                # and log the violation.
                with_capacity = [
                    cid for cid in eligible
                    if cluster_sizes.get(cid, 0) < self._capacity_for(cid)
                ]
                if not with_capacity and self.max_reassigned_stores:
                    # Hard ceiling: leave the store unassigned instead of
                    # pushing a market past max_reassigned_stores
                    stores.at[idx, self._cluster_id] = -1
                    self._outlier_stores.add(idx)
                    self._logger.warning(
                        "Store index %s left unassigned: every market in reach "
                        "is at max_reassigned_stores=%s.",
                        idx, self.max_reassigned_stores,
                    )
                    continue
                candidates = with_capacity or eligible
                candidate_distances = {
                    cid: self._haversine_miles(
                        centroids[cid][0], centroids[cid][1], store_lat, store_lon
                    )
                    for cid in candidates
                }
                max_candidate_distance = max(candidate_distances.values())
                nearest_cluster = max(
                    candidate_distances,
                    key=lambda cid: (
                        self._state_affinity_score(
                            entity_state, cid, candidate_distances[cid],
                            max_candidate_distance,
                        ),
                        -candidate_distances[cid],
                    ),
                )
                if not with_capacity:
                    self._logger.warning(
                        "All clusters are at max_cluster_size=%s; force-assigning "
                        "store index %s to cluster %s beyond the limit.",
                        self.max_cluster_size,
                        idx,
                        nearest_cluster,
                    )
            stores.at[idx, self._cluster_id] = nearest_cluster
            cluster_sizes[nearest_cluster] = cluster_sizes.get(nearest_cluster, 0) + 1
            self._outlier_stores.add(idx)
            winning_distance = self._haversine_miles(
                centroids[nearest_cluster][0], centroids[nearest_cluster][1],
                store_lat, store_lon,
            )
            stores.at[idx, 'state_affinity_score'] = self._state_affinity_score(
                entity_state, nearest_cluster, winning_distance,
                self._max_force_assign_distance,
            )

    def _add_outlier_column_to_result(self, df: pd.DataFrame):
        """Add outlier boolean column to indicate stores that were marked as outliers."""
        df['outlier'] = df.index.isin(self._outlier_stores)

    def _cluster_center(self, cid: Any, members: pd.DataFrame) -> Dict[str, float]:
        """The market's centre, per ``market_center``.

        ``base`` returns the market's base (a real store location), so the
        centre that gets reported is the same point every distance pass
        measures from. ``anchored`` keeps the legacy dense-core mean.

        Args:
            cid: Market id.
            members: Stores currently assigned to the market.

        Returns:
            ``{'centroid_lat': ..., 'centroid_lon': ...}``.
        """
        if self.market_center == 'base':
            base = self._market_base(cid, members)
            if base is not None:
                return {'centroid_lat': base[0], 'centroid_lon': base[1]}

        anchor = self._anchored_centroids.get(cid)
        if anchor is None and self.density_seeding:
            # Markets born without an anchor (legacy BFS fallback,
            # max_markets splits) still get their centroid pinned to a
            # dense core among their own members when one exists.
            anchor = self._derive_core_anchor(members)
        if anchor is not None:
            return self._anchored_centroid(members, anchor)
        return {
            'centroid_lat': float(members['latitude'].mean()),
            'centroid_lon': float(members['longitude'].mean()),
        }

    def _recompute_cluster_centroids(self):
        """Recalculate centroids for all current clusters."""
        new_centroids: Dict[int, Dict[str, float]] = {}

        if self._data.empty:
            self._cluster_centroids = {}
            return

        for cid, grp in self._data.groupby(self._cluster_id):
            if cid == -1 or grp.empty:
                continue
            # Standalone markets are frozen: their centroid was set at
            # birth from the dense core and must never be recomputed —
            # rebalancing passes do not touch their membership, so
            # recalculating just lets rounding or path differences
            # drift the centre away from the anchor.
            if cid in self._standalone_clusters and cid in self._cluster_centroids:
                new_centroids[cid] = self._cluster_centroids[cid]
                continue
            # Sub-cluster rows (FEAT-241) are an annex with their own
            # medoid-based centre; they never skew the market's own
            # centroid. Falls back to every member if a market somehow
            # ends up made entirely of sub-cluster rows.
            centroid_members = grp
            if 'is_subcluster' in grp.columns:
                core_members = grp[~grp['is_subcluster']]
                if not core_members.empty:
                    centroid_members = core_members
            new_centroids[cid] = self._cluster_center(cid, centroid_members)

        self._cluster_centroids = new_centroids
        self._recompute_market_capacity()

    def _recompute_cluster_fte_info(self):
        """Recalculate FTE metrics for each cluster based on current assignments."""
        self._cluster_fte_info.clear()

        if self._data.empty:
            return

        for cid, cluster_df in self._data.groupby(self._cluster_id):
            if cid == -1 or cluster_df.empty:
                continue

            self._get_num_ghosts_for_cluster(cid, cluster_df)

    def _check_market_invariants(self) -> Dict[str, int]:
        """Report layout invariants that silently corrupted output before.

        Diagnostic only — logs warnings, never raises, so a run still
        delivers. Each check corresponds to a defect observed on the
        Verizon layout:

        - ``shared_bases``: two markets shipping one ``ghost_id``. Means
          fewer real employees than markets, whatever ``num_employees``
          says, and SchedulingVisits treats them as a single rep.
        - ``shared_centroids``: two markets reporting the same centre.
        - ``coreless``: a market made entirely of sub-cluster rows — it
          has no seeded core, so its centre is derived from satellites.
        - ``undersized`` / ``oversized``: markets outside the configured
          size band, counting attached sub-cluster stores.

        Returns:
            Counts per invariant, for callers that want to assert on them.
        """
        report = {
            'shared_bases': 0,
            'shared_centroids': 0,
            'coreless': 0,
            'undersized': 0,
            'oversized': 0,
        }
        if self._data.empty:
            return report

        assigned = self._data[self._data[self._cluster_id] != -1]
        if assigned.empty:
            return report

        n_markets = assigned[self._cluster_id].nunique()

        if 'ghost_id' in assigned.columns:
            per_ghost = assigned.groupby('ghost_id')[self._cluster_id].nunique()
            shared = per_ghost[per_ghost > 1]
            report['shared_bases'] = int(len(shared))
            if not shared.empty:
                self._logger.warning(
                    "%s market(s) share a base with another market: "
                    "%s distinct ghost_id(s) for %s markets. Sample: %s",
                    int(shared.sum()), int(per_ghost.size), n_markets,
                    shared.head(5).to_dict(),
                )

        has_centres = {'centroid_lat', 'centroid_lon'}.issubset(assigned.columns)
        centres = (
            assigned.groupby(self._cluster_id)[
                ['centroid_lat', 'centroid_lon']
            ].first().dropna()
            if has_centres
            else pd.DataFrame()
        )
        if not centres.empty:
            dupes = centres.groupby(['centroid_lat', 'centroid_lon']).size()
            dupes = dupes[dupes > 1]
            report['shared_centroids'] = int(len(dupes))
            if not dupes.empty:
                self._logger.warning(
                    "%s centroid coordinate(s) are reported by more than one "
                    "market (max %s markets on one point).",
                    int(len(dupes)), int(dupes.max()),
                )

        if 'is_subcluster' in assigned.columns:
            is_sc = assigned['is_subcluster'].fillna(False).astype(bool)
            core_counts = assigned[~is_sc].groupby(self._cluster_id).size()
            coreless = [
                cid for cid in assigned[self._cluster_id].unique()
                if int(core_counts.get(cid, 0)) == 0
            ]
            report['coreless'] = len(coreless)
            if coreless:
                self._logger.warning(
                    "%s market(s) have no core stores at all — every member "
                    "is a sub-cluster row: %s",
                    len(coreless), coreless[:10],
                )

        sizes = assigned.groupby(self._cluster_id).size()
        if self.min_cluster_size:
            under = sizes[sizes < self.min_cluster_size]
            report['undersized'] = int(len(under))
            if not under.empty:
                self._logger.warning(
                    "%s market(s) below min_cluster_size=%s (smallest %s).",
                    int(len(under)), self.min_cluster_size, int(under.min()),
                )
        if self.max_cluster_size:
            over = sizes[sizes > self.max_cluster_size]
            report['oversized'] = int(len(over))
            if not over.empty:
                self._logger.warning(
                    "%s market(s) above max_cluster_size=%s (largest %s).",
                    int(len(over)), self.max_cluster_size, int(over.max()),
                )

        return report

    def _allocate_region_market_quotas(
        self, full_data: pd.DataFrame, region_values: List[Any]
    ) -> Dict[Any, int]:
        """Split the global ``max_markets`` budget into per-region quotas.

        ``max_markets`` is a hard target, not an advisory ceiling: the
        layout must deliver exactly that many markets, each staffed by
        one employee. Letting each region's count emerge from
        ``min/max_cluster_size`` alone cannot honour that — on the Verizon
        dataset emergent formation births 77 markets against a target of
        122, and no amount of after-the-fact splitting closes a 45-market
        gap. So the budget is distributed up front and each region's
        formation pass drives to its own quota.

        Every quota is clamped to the band the region can actually
        support:

        - floor: ``ceil(stores / max_cluster_size)`` — fewer markets than
          this and the region cannot respect the size cap.
        - ceiling: ``stores // min_cluster_size`` — more markets than this
          and some are guaranteed to come out undersized.

        Each region starts at its floor; the surplus is handed out by
        largest remainder over each region's share of the stores, never
        pushing a region past its ceiling. When the budget cannot cover
        even the sum of floors, quotas are scaled down proportionally and
        the shortfall is logged — the cap will be violated either way, and
        an honest warning beats a silent one.

        Args:
            full_data: The post-exclusion frame, before region splitting.
            region_values: Regions to form, in deterministic order.

        Returns:
            ``{region_value: quota}``; empty when ``max_markets`` is unset.
        """
        total = self.max_markets
        if total is None or not self.region_column:
            return {}

        counts: Dict[Any, int] = {}
        for value in region_values:
            size = int((full_data[self.region_column] == value).sum())
            if size:
                counts[value] = size
        if not counts:
            return {}

        max_size = int(self.max_cluster_size or 0)
        min_size = int(self.min_cluster_size or 1) or 1

        floors: Dict[Any, int] = {}
        ceils: Dict[Any, int] = {}
        for value, size in counts.items():
            ceils[value] = max(1, size // min_size)
            floor = math.ceil(size / max_size) if max_size else 1
            floors[value] = max(1, min(floor, ceils[value]))

        quota = dict(floors)
        surplus = total - sum(quota.values())

        if surplus < 0:
            # The budget cannot even cover the size cap. Scale the floors
            # down proportionally (never below 1) and say so plainly.
            self._logger.warning(
                "max_markets=%s is below the %s market(s) needed just to "
                "respect max_cluster_size=%s; scaling region quotas down "
                "proportionally -- some markets WILL exceed the cap.",
                total, sum(floors.values()), max_size,
            )
            floor_total = sum(floors.values())
            scaled = {
                value: max(1, int(floors[value] * total / floor_total))
                for value in floors
            }
            # Largest-remainder correction so the quotas sum to `total`.
            quota = scaled
            drift = total - sum(quota.values())
            order = sorted(counts, key=lambda v: (-counts[v], str(v)))
            index = 0
            while drift != 0 and order:
                value = order[index % len(order)]
                if drift > 0:
                    quota[value] += 1
                    drift -= 1
                elif quota[value] > 1:
                    quota[value] -= 1
                    drift += 1
                index += 1
                if index > 4 * len(order) and drift < 0:
                    break
            return quota

        # Hand out the surplus by largest remainder over each region's
        # share of the stores, respecting every region's ceiling.
        grand_total = sum(counts.values())
        shares = {
            value: surplus * counts[value] / grand_total for value in counts
        }
        for value in sorted(counts, key=lambda v: str(v)):
            headroom = ceils[value] - quota[value]
            quota[value] += max(0, min(int(shares[value]), headroom))

        remaining = total - sum(quota.values())
        if remaining > 0:
            # Fractional leftovers, then any slots freed by a region that
            # hit its ceiling: give them to the regions with the largest
            # fractional part first, then simply to whoever has headroom.
            ranked = sorted(
                counts,
                key=lambda v: (-(shares[v] - int(shares[v])), -counts[v], str(v)),
            )
            progressed = True
            while remaining > 0 and progressed:
                progressed = False
                for value in ranked:
                    if remaining <= 0:
                        break
                    if quota[value] < ceils[value]:
                        quota[value] += 1
                        remaining -= 1
                        progressed = True
            if remaining > 0:
                self._logger.warning(
                    "%s market slot(s) of max_markets=%s cannot be placed: "
                    "every region is at its ceiling of "
                    "stores // min_cluster_size=%s.",
                    remaining, total, min_size,
                )

        self._logger.info(
            "Region market quotas for max_markets=%s: %s",
            total,
            {str(v): quota[v] for v in sorted(quota, key=str)},
        )
        return quota

    def _cluster_satisfies_constraints(self, info: Dict[str, Any]) -> bool:
        """Return True when the provided cluster metrics respect configured constraints."""
        if not info:
            return True

        if info.get('constraint_warning'):
            return False

        daily_hours = info.get('daily_hours_per_employee')
        if pd.notna(daily_hours) and self.day_hours > 0 and daily_hours > self.day_hours + 1e-6:
            return False

        # max_stores_per_day is a daily route limit: check visits per day,
        # never the monthly portfolio size
        visits_per_day = info.get('visits_per_day_per_employee')
        if (
            pd.notna(visits_per_day)
            and self.max_stores_per_day > 0
            and visits_per_day > self.max_stores_per_day + 1e-6
        ):
            return False

        return True

    def _remove_store_for_constraint(self, cid: int) -> bool:
        """Remove the farthest store from the cluster to help satisfy FTE constraints."""
        cluster_df = self._data[self._data[self._cluster_id] == cid]

        if cluster_df.empty or len(cluster_df) <= 1:
            return False

        centroid = self._cluster_centroids.get(cid)
        centroid_lat = centroid.get('centroid_lat') if centroid else float(cluster_df['latitude'].mean())
        centroid_lon = centroid.get('centroid_lon') if centroid else float(cluster_df['longitude'].mean())

        distances = cluster_df.apply(
            lambda row: self._haversine_miles(
                centroid_lat,
                centroid_lon,
                row['latitude'],
                row['longitude']
            ),
            axis=1
        )

        farthest_idx = distances.idxmax()
        removed_row = self._data.loc[[farthest_idx]].copy()
        removed_row['constraint_reason'] = 'fte_constraint_violation'

        if self._rejected.empty:
            self._rejected = removed_row
        else:
            self._rejected = pd.concat([self._rejected, removed_row])

        self._data.drop(index=farthest_idx, inplace=True)
        self._constraint_removed_total += 1

        store_label = removed_row.iloc[0].get('store_id', farthest_idx)
        self._logger.warning(
            f"Cluster {cid} violates FTE constraints; removed store {store_label} to rebalance"
        )

        updated_cluster = self._data[self._data[self._cluster_id] == cid]
        if updated_cluster.empty:
            self._cluster_centroids.pop(cid, None)
            self._anchored_centroids.pop(cid, None)
        else:
            self._cluster_centroids[cid] = self._cluster_center(
                cid, updated_cluster
            )

        return True

    def _rebalance_clusters_for_fte_constraints(self):
        """Iteratively trim clusters until they meet configured FTE constraints."""
        if not self._constraints_enforcement_enabled():
            return

        if not self.use_fte_constraints:
            self._constraint_rebalance_required = False
            return

        removed_this_pass = 0

        while True:
            self._recompute_cluster_fte_info()
            violation_found = False
            removed_in_iteration = False

            for cid, info in sorted(self._cluster_fte_info.items()):
                if cid == -1:
                    continue
                if cid in self._standalone_clusters:
                    continue  # Standalone markets are frozen

                if self._cluster_satisfies_constraints(info):
                    continue

                violation_found = True
                if self._remove_store_for_constraint(cid):
                    removed_this_pass += 1
                    removed_in_iteration = True
                    break
                else:
                    self._logger.warning(
                        f"Cluster {cid} violates FTE constraints but cannot be reduced further"
                    )
            if not violation_found or not removed_in_iteration:
                break

        if removed_this_pass:
            self._logger.info(
                f"Removed {removed_this_pass} stores while enforcing FTE constraints"
            )

        self._constraint_rebalance_required = False

    def _dissolve_undersized_clusters(self):
        """Dissolve clusters below ``min_cluster_size`` and re-evaluate their stores.

        Clusters are processed smallest-first. Each store of a dissolved
        cluster moves to the nearest surviving cluster that still has
        capacity (``max_cluster_size``) and lies within
        ``max_assign_distance``; stores with no viable market are rejected
        with ``constraint_reason='below_min_cluster_size'``.
        """
        if self.min_cluster_size is None or self.min_cluster_size <= 1:
            return
        if self._data.empty:
            return

        if self.max_markets is not None:
            # Exact-markets mode: dissolving would drop the market count below
            # the max_markets target, so undersized clusters are kept.
            sizes = self._data[self._data[self._cluster_id] != -1].groupby(
                self._cluster_id
            ).size()
            undersized = sizes[sizes < self.min_cluster_size]
            if not undersized.empty:
                self._logger.warning(
                    "Keeping %s cluster(s) below min_cluster_size=%s because "
                    "max_markets=%s is an exact target: %s",
                    len(undersized),
                    self.min_cluster_size,
                    self.max_markets,
                    dict(undersized),
                )
            return

        self._recompute_cluster_centroids()
        # FEAT-248 TASK-205: this surface scores via _nearest_absorbing_market
        # below; reset once at the top (not per store in the loop, which
        # would defeat the cache).
        self._reset_state_score_cache()

        while True:
            assigned = self._data[self._data[self._cluster_id] != -1]
            sizes = assigned.groupby(self._cluster_id).size()
            undersized = sizes[sizes < self.min_cluster_size]
            undersized = undersized[~undersized.index.isin(self._standalone_clusters)]

            if undersized.empty:
                break
            if len(sizes) <= 1:
                self._logger.warning(
                    "Cluster %s has %s stores (min_cluster_size=%s) but it is "
                    "the only market left; keeping it.",
                    undersized.index[0],
                    int(undersized.iloc[0]),
                    self.min_cluster_size,
                )
                break

            # Dissolve the smallest cluster first: its stores may grow a
            # neighbouring undersized cluster past the minimum.
            cid = undersized.sort_values().index[0]
            cluster_sizes = sizes.to_dict()
            cluster_sizes.pop(cid, None)
            member_indices = self._data.index[
                self._data[self._cluster_id] == cid
            ].tolist()

            rejected_indices = []
            for idx in member_indices:
                store_lat = self._data.at[idx, 'latitude']
                store_lon = self._data.at[idx, 'longitude']

                # Nearest market within max_assign_distance; the size cap is
                # soft (a full neighbour absorbs the store rather than
                # rejecting it)
                candidates = {
                    other_cid: (
                        centroid['centroid_lat'], centroid['centroid_lon']
                    )
                    for other_cid, centroid in self._cluster_centroids.items()
                    if other_cid != cid
                    and other_cid not in self._standalone_clusters
                }
                entity_state = (
                    self._data.at[idx, self.state_column]
                    if self.state_column in self._data.columns else None
                )
                choice = self._nearest_absorbing_market(
                    store_lat, store_lon, candidates, cluster_sizes,
                    self._max_force_assign_distance,
                    entity_state=entity_state,
                )
                nearest_cluster = None
                if choice is not None:
                    nearest_cluster, choice_distance, overfilled = choice
                    if overfilled:
                        self._logger.warning(
                            "Dissolved store index %s overfills market %s "
                            "(%.1f miles): every market within %s miles is at "
                            "max_cluster_size=%s.",
                            idx, nearest_cluster, choice_distance,
                            self._max_force_assign_distance,
                            self.max_cluster_size,
                        )

                if nearest_cluster is not None:
                    self._data.at[idx, self._cluster_id] = nearest_cluster
                    if self._cluster_name in self._data.columns:
                        self._data.at[idx, self._cluster_name] = f"Market-{nearest_cluster}"
                    if 'ghost_id' in self._data.columns:
                        self._data.at[idx, 'ghost_id'] = f"Ghost-{nearest_cluster}-1"
                    cluster_sizes[nearest_cluster] = cluster_sizes.get(nearest_cluster, 0) + 1
                else:
                    rejected_indices.append(idx)

            if rejected_indices:
                rejected_rows = self._data.loc[rejected_indices].copy()
                rejected_rows['constraint_reason'] = 'below_min_cluster_size'
                if self._rejected.empty:
                    self._rejected = rejected_rows
                else:
                    self._rejected = pd.concat([self._rejected, rejected_rows])
                self._data.drop(index=rejected_indices, inplace=True)

            self._logger.info(
                "Dissolved cluster %s (%s stores < min_cluster_size=%s): "
                "%s stores reassigned, %s rejected.",
                cid,
                len(member_indices),
                self.min_cluster_size,
                len(member_indices) - len(rejected_indices),
                len(rejected_indices),
            )

            self._cluster_fte_info.pop(cid, None)
            self._recompute_cluster_centroids()

    def _split_clusters_to_reach_max_markets(self, stores: pd.DataFrame) -> None:
        """Split clusters until the market count reaches ``max_markets``.

        ``max_markets`` is an exact target, not just a cap: ``cluster_radius``
        is a soft preference, so when the BFS produced fewer clusters than
        requested the largest ones are split in two (KMeans) until the target
        is met. Splits never mix isolation partitions (a cluster is
        partition-pure, so are its halves) and, when partition quotas are
        active, happen inside the partition that is still below its quota.
        Clusters that can keep both halves at ``min_cluster_size`` are
        preferred, but the exact market count wins over the minimum size.
        """
        if self.max_markets is None:
            return

        partition = self._partition_mask(stores)
        quotas = self._partition_market_quotas(partition)

        while True:
            sizes = stores[stores[self._cluster_id] != -1].groupby(
                stores[self._cluster_id]
            ).size()
            if len(sizes) >= self.max_markets:
                break

            splittable = sizes[sizes >= 2]
            if self._standalone_clusters:
                splittable = splittable[~splittable.index.isin(self._standalone_clusters)]
            if quotas is not None and not splittable.empty:
                counts: Dict[bool, int] = {True: 0, False: 0}
                for cid in sizes.index:
                    counts[self._cluster_partition.get(cid, False)] += 1
                lagging = [p for p in (True, False) if counts[p] < quotas[p]]
                in_lagging = splittable[
                    [
                        self._cluster_partition.get(cid, False) in lagging
                        for cid in splittable.index
                    ]
                ]
                if not in_lagging.empty:
                    splittable = in_lagging

            if splittable.empty:
                self._logger.warning(
                    "Cannot reach max_markets=%s: only %s markets are possible "
                    "with the current store distribution.",
                    self.max_markets,
                    len(sizes),
                )
                break

            preferred = splittable[splittable >= 2 * self.min_cluster_size]
            if preferred.empty and self.min_cluster_size > 1:
                self._logger.warning(
                    "Splitting to reach max_markets=%s leaves clusters below "
                    "min_cluster_size=%s; the exact market count takes priority.",
                    self.max_markets,
                    self.min_cluster_size,
                )
            pool = preferred if not preferred.empty else splittable
            cid = pool.idxmax()
            self._split_market(stores, cid, reason=f"reach max_markets={self.max_markets}")

    @staticmethod
    def _rebalance_stall_state(
        current_max: int, best_max: Optional[int], stalled: int
    ) -> Tuple[int, int]:
        """Advance the stall detector of ``_balance_market_sizes`` one round.

        The threshold is the BEST (smallest) largest-market size seen so far,
        not the previous round's. Comparing against the previous round only
        makes the detector blind to cycles: the pass can dissolve a donor
        whose stores flow straight back into the market it is about to split,
        so the largest market alternates (say 76, 68, 76, 68) instead of
        settling. Every other round then looks like an improvement, ``stalled``
        resets, and the loop burns all ``max_markets`` rounds achieving
        nothing. Ratcheting on the best value makes any cycle — of any period —
        stop counting as progress, while a genuine descent (even a noisy one)
        keeps ``stalled`` at zero.

        Args:
            current_max: Size of the largest market this round.
            best_max: Smallest ``current_max`` seen so far, or None on the
                first round.
            stalled: Consecutive rounds without improving on ``best_max``.

        Returns:
            The updated ``(best_max, stalled)``.
        """
        if best_max is not None and current_max >= best_max:
            return best_max, stalled + 1
        return (current_max if best_max is None else min(best_max, current_max)), 0

    def _balance_market_sizes(self) -> None:
        """Move market *budget* from tiny markets to oversized ones.

        ``max_markets`` fixes how many markets exist, not how big they are:
        a dense metro can hold several 15-store markets while a sparse region
        keeps a single 160-store one. Splitting alone cannot fix that (the
        count target is already met) and refusing stores — using
        ``max_cluster_size`` as an assignment gate — only strands them
        hundreds of miles from their market.

        So the layout, not the store, gives way: while a market is over
        ``max_cluster_size``, the smallest market whose stores can all be
        absorbed by a neighbour within ``_move_distance_guard`` is dissolved
        and the largest market is split in two. The market count never
        changes; stores only ever move to a market near them.
        """
        if (
            self.max_markets is None
            or not self.max_cluster_size
            or not self.balance_market_sizes
            or self._data.empty
        ):
            return

        partition = self._partition_mask(self._data)
        guard = self._move_distance_guard
        rebalanced = 0
        best_max: Optional[int] = None
        stalled = 0

        for _ in range(int(self.max_markets)):
            assigned = self._data[self._data[self._cluster_id] != -1]
            sizes = assigned.groupby(self._cluster_id).size()
            sizes = sizes[~sizes.index.isin(self._standalone_clusters)]
            if sizes.empty:
                return

            # The market to cut is the one furthest past its own ceiling —
            # with capacity_from_hours that is the market whose visits do not
            # fit its staff's month, not merely the one with most stores
            overflow = {
                cid: int(sizes[cid]) - self._effective_ceiling(cid)
                for cid in sizes.index
            }
            biggest = max(overflow, key=overflow.get)
            if overflow[biggest] <= 0:
                break

            # Each round should shrink the biggest market. When it stops
            # doing so the layout is as balanced as the geography allows and
            # further rounds would just shuffle rural markets around.
            current_max = int(sizes[biggest])
            best_max, stalled = self._rebalance_stall_state(
                current_max, best_max, stalled
            )
            if stalled >= 3:
                self._logger.warning(
                    "Market size rebalance stopped after %s round(s): the "
                    "largest market keeps %s stores (best seen %s, "
                    "max_cluster_size=%s) and no further slot reclaim "
                    "improves it.",
                    rebalanced, current_max, best_max, self.max_cluster_size,
                )
                break

            # Dissolving a market only pays off when it is clearly smaller
            # than the halves the split would produce
            donors = sizes[(sizes.index != biggest) & (sizes * 2 <= sizes[biggest])]
            if donors.empty:
                self._logger.warning(
                    "Market %s keeps %s stores (max_cluster_size=%s): no market "
                    "small enough to free a slot for a split.",
                    biggest, int(sizes[biggest]), self.max_cluster_size,
                )
                break

            # Prefer donors whose stores stay very close to their new market;
            # only when none qualifies is the full cluster radius allowed —
            # a market that cannot be split otherwise keeps 87 stores.
            moves = None
            donor = None
            for reach in (guard, self.max_cluster_distance or float('inf')):
                for candidate in donors.sort_values().index:
                    moves = self._plan_market_dissolution(
                        candidate, assigned, sizes, partition, reach,
                        split_target=biggest,
                    )
                    if moves is not None:
                        donor = candidate
                        break
                if moves is not None:
                    break

            if moves is None:
                self._logger.warning(
                    "Market %s keeps %s stores (max_cluster_size=%s): no small "
                    "market can hand its stores to a neighbour within %s miles.",
                    biggest, int(sizes[biggest]), self.max_cluster_size, guard,
                )
                break

            dropped = 0
            for idx, target in moves.items():
                self._data.at[idx, self._cluster_id] = target
                if target == -1:
                    self._data.at[idx, self._cluster_name] = 'Outlier'
                    self._data.at[idx, 'ghost_id'] = None
                    self._data.at[idx, 'constraint_reason'] = (
                        'market_dissolved_no_market_in_range'
                    )
                    self._outlier_stores.add(idx)
                    dropped += 1
            if dropped:
                self._logger.warning(
                    "%s store(s) of market %s were left unassigned: no market "
                    "within %s miles could take them.",
                    dropped, donor, self.unassign_distance,
                )
            self._anchored_centroids.pop(donor, None)
            self._cluster_fte_info.pop(donor, None)
            self._logger.info(
                "Dissolved market %s (%s stores) to free a slot for splitting "
                "market %s (%s stores, max_cluster_size=%s)",
                donor, len(moves), biggest, int(sizes[biggest]), self.max_cluster_size,
            )

            self._split_market(
                self._data, biggest,
                reason=f"honour max_cluster_size={self.max_cluster_size}",
            )
            rebalanced += 1
            self._recompute_cluster_centroids()

        if rebalanced:
            self._logger.info(
                "Rebalanced %s oversized market(s) by reclaiming slots from "
                "small ones", rebalanced,
            )

    def _rescue_unassigned_clusters(self) -> int:
        """Give a market to unassigned stores that form a real cluster.

        Seeding spends the budget on density before anyone is full, so a city
        whose neighbouring markets fill up later ends up with no market at
        all — Naples (38 stores within 30 miles) unassigned while a 11-store
        market spans 120 miles of empty Texas. With hindsight the trade is
        obvious: dissolve the market that can hand its stores to neighbours
        and give the slot to the cluster that has none.

        The market count never changes: one dissolved, one founded.

        Returns:
            How many markets were rescued this way.
        """
        if (
            not self.rescue_unassigned
            or self.max_markets is None
            or self._data.empty
        ):
            return 0

        min_group = max(
            2,
            int(
                self.rescue_min_stores
                if self.rescue_min_stores is not None
                else (self.min_cluster_size or 2)
            ),
        )
        rescue_radius = (
            self.rescue_radius
            if self.rescue_radius is not None
            else self.density_radius
        )
        partition = self._partition_mask(self._data)
        guard = self._move_distance_guard
        rescued = 0

        for _ in range(int(self.max_markets)):
            pool = self._data[self._data[self._cluster_id] == -1]
            if len(pool) < min_group:
                break

            coords = np.radians(pool[['latitude', 'longitude']].to_numpy())
            tree = BallTree(coords, leaf_size=40, metric='haversine')
            radius = miles_to_radians(rescue_radius)
            counts = tree.query_radius(coords, r=radius, count_only=True)
            seed = int(counts.argmax())
            if int(counts[seed]) < min_group:
                break  # no cluster worth a market, only scattered orphans

            members = pool.index[tree.query_radius([coords[seed]], r=radius)[0]]
            assigned = self._data[self._data[self._cluster_id] != -1]
            sizes = assigned.groupby(self._cluster_id).size()
            sizes = sizes[~sizes.index.isin(self._standalone_clusters)]

            donor = None
            moves = None
            for candidate in sizes[sizes < len(members)].sort_values().index:
                moves = self._plan_market_dissolution(
                    candidate, assigned, sizes, partition, guard
                )
                if moves is not None:
                    donor = candidate
                    break

            if donor is None:
                self._logger.warning(
                    "%s unassigned stores cluster together but no market is "
                    "small enough to free a slot for them.", len(members),
                )
                break

            for idx, target in moves.items():
                self._data.at[idx, self._cluster_id] = target
                if target == -1:
                    self._data.at[idx, self._cluster_name] = 'Outlier'
                    self._outlier_stores.add(idx)
            self._anchored_centroids.pop(donor, None)
            self._cluster_fte_info.pop(donor, None)

            new_cid = int(self._data[self._cluster_id].max()) + 1
            centre = pool.loc[pool.index[seed]]
            self._cluster_partition[new_cid] = (
                bool(partition.loc[pool.index[seed]]) if partition is not None else False
            )
            distances = self._data.loc[members].apply(
                lambda row: self._haversine_miles(
                    centre['latitude'], centre['longitude'],
                    row['latitude'], row['longitude'],
                ),
                axis=1,
            ).sort_values()
            # FEAT-248 TASK-201: was `_capacity_gate` (no hours component),
            # which could stuff a market that `_capacity_shed_pass` (reads
            # `_effective_ceiling`) would immediately try to drain again
            # when `capacity_from_hours` is on. Routed through the single
            # effective ceiling to close that oscillation.
            ceiling = self._effective_ceiling(new_cid)
            taken = 0
            for idx in distances.index:
                if taken >= ceiling:
                    break
                self._data.at[idx, self._cluster_id] = new_cid
                self._data.at[idx, self._cluster_name] = f"Market-{new_cid}"
                self._data.at[idx, 'ghost_id'] = f"Ghost-{new_cid}-1"
                self._data.at[idx, 'constraint_reason'] = None
                self._outlier_stores.discard(idx)
                taken += 1

            rescued += 1
            self._logger.info(
                "Rescued %s unassigned stores into new market %s (slot taken "
                "from market %s, which had %s stores)",
                taken, new_cid, donor, len(moves),
            )
            self._recompute_cluster_centroids()

        return rescued

    def _absorb_remnant_stores(self) -> int:
        """Let a full market absorb the last stranded stores around it.

        The rescue pass only helps groups of at least ``rescue_min_stores``;
        a remnant of one or two stores next to a market already at its hard
        capacity gate (``max_reassigned_stores``) has no door left and is
        delivered unassigned. With ``absorb_remnants`` on, a market whose
        surrounding unassigned stores (within ``rescue_radius``) number at
        most ``remnant_overflow`` takes them all, growing past the gate by
        that many at most. Larger groups are left alone: they are a cluster
        worth a market slot, not a silent overfill.

        Isolation partitions are respected and standalone markets never
        absorb. Absorbed stores stay flagged as outliers, like every other
        store that overfills a market.

        Returns:
            How many stores were absorbed.
        """
        if not self.absorb_remnants or self._data.empty:
            return 0
        overflow = max(0, int(self.remnant_overflow))
        if overflow == 0:
            return 0

        pool = self._data[self._data[self._cluster_id] == -1]
        if pool.empty:
            return 0

        radius = (
            self.rescue_radius
            if self.rescue_radius is not None
            else self.density_radius
        )
        partition = self._partition_mask(self._data)

        # Nearest eligible market within the radius, per stranded store
        chosen: Dict[Any, List[Any]] = {}
        for idx, store in pool.iterrows():
            store_partition = (
                bool(partition.loc[idx]) if partition is not None else None
            )
            best: Optional[Tuple[float, Any]] = None
            for cid, centroid in self._cluster_centroids.items():
                if cid in self._standalone_clusters:
                    continue
                if store_partition is not None and self._cluster_partition.get(
                    cid, False
                ) != store_partition:
                    continue
                distance = self._haversine_miles(
                    centroid['centroid_lat'], centroid['centroid_lon'],
                    store['latitude'], store['longitude'],
                )
                if distance <= radius and (best is None or distance < best[0]):
                    best = (distance, cid)
            if best is not None:
                chosen.setdefault(best[1], []).append(idx)

        absorbed = 0
        for cid, members in chosen.items():
            centroid = self._cluster_centroids[cid]
            # Gate on EVERY unassigned store around the market, not just the
            # ones that chose it: a bigger crowd nearby means this is a
            # cluster the rescue pass should handle, not a remnant
            nearby = pool.apply(
                lambda row: self._haversine_miles(
                    centroid['centroid_lat'], centroid['centroid_lon'],
                    row['latitude'], row['longitude'],
                ) <= radius,
                axis=1,
            ).sum()
            if int(nearby) > overflow:
                self._logger.info(
                    "Market %s keeps its size: %s unassigned stores within "
                    "%s miles exceed remnant_overflow=%s",
                    cid, int(nearby), radius, overflow,
                )
                continue

            for idx in members:
                self._data.at[idx, self._cluster_id] = cid
                self._data.at[idx, self._cluster_name] = f"Market-{cid}"
                self._data.at[idx, 'ghost_id'] = f"Ghost-{cid}-1"
                if 'constraint_reason' in self._data.columns:
                    self._data.at[idx, 'constraint_reason'] = None
                self._outlier_stores.add(idx)
                absorbed += 1
            self._logger.info(
                "Market %s absorbed %s remnant store(s) past its capacity "
                "gate (absorb_remnants)", cid, len(members),
            )

        return absorbed

    # -- Outlier sub-cluster formation (FEAT-241, Module 2) ------------------
    # Turns rows still cluster_id == -1 into pockets that fit a day budget,
    # each anchored on a real-store medoid. Pure/deterministic (given
    # self.random_seed); no network calls, no mutation of self._data.

    def _form_outlier_subclusters(self, pool: pd.DataFrame) -> List[dict]:
        """Group leftover outliers into day-budget-feasible sub-clusters.

        DBSCAN (haversine, ``min_samples=1``) pockets ``pool`` by proximity
        so every row — singletons included — lands in a pocket. Pockets
        whose in-store hours plus a cheap intra-cluster travel estimate
        exceed ``max_subcluster_days * self.day_hours`` are split
        recursively with balanced 2-means until every part fits or is a
        singleton.

        Args:
            pool: rows with ``self._data[self._cluster_id] == -1``.

        Returns:
            One dict per final pocket: ``{"indices": [...],
            "medoid": (lat, lon), "days": int, "hours": float}``.
        """
        if pool.empty:
            return []

        coords_rad = np.radians(pool[['latitude', 'longitude']].to_numpy())
        eps = miles_to_radians(self.subcluster_radius)
        labels = DBSCAN(
            eps=eps, min_samples=1, metric='haversine'
        ).fit_predict(coords_rad)

        day_budget = self.max_subcluster_days * self.day_hours
        pockets: List[dict] = []
        splits = 0
        for label in np.unique(labels):
            member_idx = pool.index[labels == label]
            pocket_df = pool.loc[member_idx]
            formed = self._split_pocket_to_budget(pocket_df, day_budget)
            splits += max(0, len(formed) - 1)
            pockets.extend(formed)

        self._logger.info(
            "Outlier sub-clusters: %s pocket(s) from %s store(s), %s "
            "split(s) (eps=%.1f mi, budget=%.1fh)",
            len(pockets), len(pool), splits, self.subcluster_radius, day_budget,
        )

        # FEAT-247 Module 4: DBSCAN pockets maximize stores per pocket, not
        # visit efficiency (El Paso: 2 pockets/6 stores -> 4 block-days when
        # 3 pockets/4 stores would cover the same stores in 3). Re-partition
        # each neighborhood of nearby pockets to minimize total days.
        pockets = self._repartition_pocket_neighborhoods(pockets, pool)
        return pockets

    def _repartition_pocket_neighborhoods(
        self, pockets: List[dict], pool: pd.DataFrame
    ) -> List[dict]:
        """Re-partition neighborhoods of pockets to minimize total days.

        A DBSCAN pocket maximizes stores per pocket, not visit days: 2
        pockets of 6 stores (each ~1.5 days -> ceil 2 each = 4 days total)
        can cover the same ground as 3 pockets of 4 (each ≤ 1 day = 3 days
        total) — one day saved with the same store set. This pass finds
        that better split.

        Pockets whose medoids lie within ``2 * self.subcluster_radius``
        miles form one NEIGHBORHOOD (transitive: A-B and B-C in reach group
        A, B and C even if A-C is not). For each neighborhood with k
        pockets, evaluates balanced k-means for k in
        ``[max(1, k-1), k+2]`` (seeded, degenerate/empty-cluster candidates
        skipped), each candidate part re-split under the day budget by the
        existing recursive mechanism (``_split_pocket_to_budget``). Scores
        each candidate partition by total days (Σ⌈hours/day_hours⌉),
        tie-break lower total travel miles (Σ ``_pocket_travel_miles``).
        The current (DBSCAN-formed) partition is always one of the
        candidates, so this pass never makes a neighborhood worse.

        A pocket with no neighbor within reach passes through unchanged
        (already carries honest ``days`` from ``_split_pocket_to_budget``).

        Args:
            pockets: Pocket dicts from the DBSCAN pass (post-budget-split).
            pool: The frame ``pockets``' indices were drawn from
                (``_form_outlier_subclusters``'s own ``pool`` argument) —
                looked up directly rather than via ``self._data`` so this
                method works whether or not the caller has already
                committed ``pool`` there.

        Returns:
            The same or fewer/more pocket dicts, days-optimized per
            neighborhood.
        """
        if len(pockets) <= 1:
            return pockets

        day_budget = self.max_subcluster_days * self.day_hours
        neighbor_reach = 2 * self.subcluster_radius

        # Union-find over pocket medoids, transitive within neighbor_reach.
        parent = list(range(len(pockets)))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for i in range(len(pockets)):
            lat1, lon1 = pockets[i]['medoid']
            for j in range(i + 1, len(pockets)):
                lat2, lon2 = pockets[j]['medoid']
                if self._haversine_miles(lat1, lon1, lat2, lon2) <= neighbor_reach:
                    union(i, j)

        groups: Dict[int, List[int]] = {}
        for i in range(len(pockets)):
            groups.setdefault(find(i), []).append(i)

        # Deterministic neighborhood processing order: sort groups by their
        # (sorted) member medoids.
        ordered_roots = sorted(
            groups, key=lambda root: sorted(pockets[i]['medoid'] for i in groups[root])
        )

        result: List[dict] = []
        total_days_before = 0
        total_days_after = 0
        neighborhoods_improved = 0

        for root in ordered_roots:
            member_positions = groups[root]
            member_pockets = [pockets[p] for p in member_positions]
            days_before = sum(p['days'] for p in member_pockets)
            total_days_before += days_before

            if len(member_pockets) <= 1:
                # Isolated pocket: no neighbor within reach, passes through
                # unchanged except the honest `days` it already carries.
                result.extend(member_pockets)
                total_days_after += days_before
                continue

            all_indices = [idx for p in member_pockets for idx in p['indices']]
            neighborhood_df = pool.loc[all_indices]
            current_k = len(member_pockets)

            def _travel_total(
                candidate_pockets: List[dict], _frame: pd.DataFrame = neighborhood_df
            ) -> float:
                return sum(
                    self._pocket_travel_miles(_frame.loc[p['indices']])
                    for p in candidate_pockets
                )

            best_partition = member_pockets
            best_score = (days_before, _travel_total(member_pockets))

            k_min = max(1, current_k - 1)
            k_max = current_k + 2
            for k in range(k_min, k_max + 1):
                if k <= 0 or k > len(neighborhood_df):
                    continue
                if k == current_k:
                    # Already scored above as the DBSCAN-formed baseline.
                    continue
                if k == 1:
                    candidate = self._split_pocket_to_budget(
                        neighborhood_df, day_budget
                    )
                else:
                    coords = neighborhood_df[['latitude', 'longitude']].to_numpy()
                    labels = KMeans(
                        n_clusters=k, random_state=self.random_seed, n_init=10
                    ).fit_predict(coords)
                    if len(set(labels)) < k:
                        continue  # degenerate (empty cluster) — not a real k-partition
                    candidate = []
                    for label in range(k):
                        part = neighborhood_df.iloc[labels == label]
                        if part.empty:
                            continue
                        candidate.extend(self._split_pocket_to_budget(part, day_budget))

                candidate_score = (
                    sum(p['days'] for p in candidate), _travel_total(candidate)
                )
                if candidate_score < best_score:
                    best_score = candidate_score
                    best_partition = candidate

            result.extend(best_partition)
            total_days_after += best_score[0]
            if best_score[0] < days_before:
                neighborhoods_improved += 1
                self._logger.debug(
                    "Sub-cluster neighborhood (%s stores): %s pocket(s)/"
                    "%s day(s) -> %s pocket(s)/%s day(s) (%s day(s) saved)",
                    len(neighborhood_df), len(member_pockets), days_before,
                    len(best_partition), best_score[0],
                    days_before - best_score[0],
                )

        if neighborhoods_improved:
            self._logger.info(
                "Sub-cluster neighborhood repartition: %s neighborhood(s) "
                "improved, %s -> %s pocket(s), %s -> %s day(s) total "
                "(%s day(s) saved)",
                neighborhoods_improved, len(pockets), len(result),
                total_days_before, total_days_after,
                total_days_before - total_days_after,
            )
        return result

    def _split_pocket_to_budget(
        self, pocket_df: pd.DataFrame, day_budget: float
    ) -> List[dict]:
        """Recursively split a pocket until every part fits or is a singleton."""
        hours = self._pocket_hours(pocket_df)
        if len(pocket_df) <= 1 or hours <= day_budget:
            # FEAT-247: true-ceil days, not the old `1 | max_subcluster_days`
            # binary. The pre-split under day_budget = max_subcluster_days *
            # day_hours guarantees this never exceeds max_subcluster_days.
            days = max(1, math.ceil(hours / self.day_hours))
            if days > self.max_subcluster_days:
                # Never silently ship an over-budget pocket -- a stripped
                # `assert` (python -O) would otherwise let this through.
                # This is a genuine invariant violation (the pre-split
                # under day_budget is supposed to make it unreachable),
                # not a normal validation failure, so it raises the same
                # way every other broken-invariant path in this file does.
                raise ComponentError(
                    f"pocket days={days} exceeds max_subcluster_days="
                    f"{self.max_subcluster_days} (hours={hours}, "
                    f"day_budget={day_budget}) — budget pre-split invariant broken"
                )
            return [{
                "indices": pocket_df.index.tolist(),
                "medoid": self._pocket_medoid(pocket_df),
                "days": days,
                "hours": float(hours),
            }]

        coords = pocket_df[['latitude', 'longitude']].to_numpy()
        split_labels = KMeans(
            n_clusters=2, random_state=self.random_seed, n_init=10
        ).fit_predict(coords)
        part_a = pocket_df.iloc[split_labels == 0]
        part_b = pocket_df.iloc[split_labels == 1]
        if part_a.empty or part_b.empty:
            # Degenerate split (e.g. coincident coordinates): fall back to a
            # deterministic positional split so recursion still terminates.
            sorted_df = pocket_df.sort_values(by=['latitude', 'longitude'])
            mid = len(sorted_df) // 2
            part_a, part_b = sorted_df.iloc[:mid], sorted_df.iloc[mid:]

        parts: List[dict] = []
        for part in (part_a, part_b):
            if part.empty:
                continue
            parts.extend(self._split_pocket_to_budget(part, day_budget))
        return parts

    def _pocket_hours(self, pocket_df: pd.DataFrame) -> float:
        """Cheap hours estimate: in-store hours + intra-cluster travel.

        No Valhalla calls here — the travel estimate is a nearest-neighbor
        haversine chain scaled by ``ROUTING_DETOUR_FACTOR`` at 40 mph,
        deliberately cheap (Module 3 does the real road-mile lookups).
        """
        hours_series = self._get_cluster_in_store_hours(pocket_df)
        if hours_series is not None:
            in_store_total = float(hours_series.fillna(self.in_store_hours).sum())
        else:
            in_store_total = self.in_store_hours * len(pocket_df)

        travel_miles = self._pocket_travel_miles(pocket_df)
        travel_hours = (
            travel_miles * ROUTING_DETOUR_FACTOR
        ) / _INTRA_CLUSTER_AVERAGE_SPEED_MPH
        return in_store_total + travel_hours

    def _pocket_travel_miles(self, pocket_df: pd.DataFrame) -> float:
        """Nearest-neighbor chain distance over the pocket's stores."""
        n = len(pocket_df)
        if n <= 1:
            return 0.0
        coords = pocket_df[['latitude', 'longitude']].to_numpy()
        remaining = list(range(1, n))
        current = 0
        total = 0.0
        while remaining:
            distances = [
                self._haversine_miles(
                    coords[current][0], coords[current][1],
                    coords[j][0], coords[j][1],
                )
                for j in remaining
            ]
            nearest_pos = int(np.argmin(distances))
            total += distances[nearest_pos]
            current = remaining.pop(nearest_pos)
        return total

    def _pocket_medoid(self, pocket_df: pd.DataFrame) -> Tuple[float, float]:
        """Real-store medoid: member minimizing summed haversine distance."""
        coords = pocket_df[['latitude', 'longitude']].to_numpy()
        n = len(coords)
        if n == 1:
            return float(coords[0][0]), float(coords[0][1])

        best_idx = 0
        best_total = None
        for i in range(n):
            total = float(np.sum([
                self._haversine_miles(
                    coords[i][0], coords[i][1], coords[j][0], coords[j][1]
                )
                for j in range(n) if j != i
            ]))
            if best_total is None or total < best_total:
                best_total = total
                best_idx = i
        return float(coords[best_idx][0]), float(coords[best_idx][1])

    # -- Sub-cluster market selection via road miles (FEAT-241, Module 3) ---
    # Haversine top-K prefilter, then Valhalla (via RoutingService) decides:
    # road proximity, not straight-line proximity, picks the receiving
    # market. One RoutingService session for the whole batch.

    def _subcluster_anchor_cap(self) -> Optional[float]:
        """Hard distance cap for satellite anchoring (FEAT-248 G4).

        ``unassign_distance`` when configured (matching the promise it
        already makes for normal stores); otherwise
        ``flyout_distance_factor * max_distance_by_day``. ``None`` when
        BOTH are unset/non-positive — a config that opted out of both
        never had a cap, and this task must not invent one (regression
        guard): satellites keep anchoring anywhere, as before.
        """
        if self.unassign_distance:
            return float(self.unassign_distance)
        if self.max_distance_by_day and self.max_distance_by_day > 0:
            return float(self.flyout_distance_factor) * float(self.max_distance_by_day)
        return None

    def _reject_subcluster_pocket(self, subcluster: dict) -> None:
        """Deliver an unplaceable satellite pocket as UNASSIGNED (FEAT-248 G4).

        Mirrors ``_unassign_orphan_pass``'s normal-store semantics: the
        pocket's rows are already at ``cluster_id == -1`` in
        ``self._data`` (they came from the ``_attach_outlier_subclusters``
        pool and ``market_cid`` stays ``None``, so the caller never
        assigns them) — this additionally stamps ``constraint_reason`` and
        records them in ``self._rejected`` (deduplicated by index, so a
        row already tracked there via ``_readmit_rejected_as_unassigned``
        is re-stamped, never duplicated), the same ledger normal-store
        rejections land in, so the delivered export/log account for them
        under a reason distinguishable from normal-store rejections.
        """
        indices = [
            idx for idx in subcluster.get('indices', [])
            if idx in self._data.index
        ]
        if not indices:
            return

        reason = 'subcluster_no_candidate_within_cap'
        if 'constraint_reason' not in self._data.columns:
            self._data['constraint_reason'] = None
        self._data.loc[indices, 'constraint_reason'] = reason
        self._outlier_stores.update(indices)

        rows = self._data.loc[indices].copy()
        rows['constraint_reason'] = reason
        if self._rejected.empty:
            self._rejected = rows
        else:
            self._rejected = pd.concat(
                [self._rejected.drop(index=indices, errors='ignore'), rows]
            )

    async def _select_subcluster_market(self, subclusters: List[dict]) -> List[dict]:
        """Pick each sub-cluster's receiving market by state-affinity score.

        Haversine-prefilters each sub-cluster's medoid to the nearest
        ``subcluster_market_candidates`` market centroids
        (``_centroid_points()``), then asks one shared ``RoutingService``
        session for road miles medoid<->centroid per sub-cluster (one
        small matrix per sub-cluster, never a global N×N). Candidates are
        then, when a cap is configured (FEAT-248 G4, see
        ``_subcluster_anchor_cap``), filtered BEFORE scoring to those
        within the hard distance cap AND with positive headroom under
        ``_effective_ceiling`` for the WHOLE pocket (a pocket anchors as
        one atomic unit, never split across receivers) — mirroring the
        promise ``unassign_distance`` already makes for normal stores. A
        pocket with no feasible candidate is delivered UNASSIGNED (see
        ``_reject_subcluster_pocket``) instead of anchored beyond the cap.
        The winner among feasible candidates is the one with the highest
        ``_state_affinity_score`` (FEAT-247) — state affinity, road-mile
        distance (normalized against the absolute cap when one applies,
        never the candidate pool's own max — a 400-mile candidate must
        not look "close" just because every candidate was far) and
        capacity headroom, not road miles alone — using ROAD miles as the
        distance term. On a degraded (geodesic-fallback) matrix, or on any
        unexpected exception from the service, the same scoring runs
        against HAVERSINE distances instead — this pass never aborts the
        run on a routing failure, and the FEAT-241 degraded-routing
        fallback survives unchanged in kind.

        Configs with neither ``unassign_distance`` nor a
        ``max_distance_by_day`` fallback configured see NO behavior
        change: ``_subcluster_anchor_cap()`` returns ``None`` and every
        candidate is scored exactly as before (pool-max normalization).

        Args:
            subclusters: dicts from ``_form_outlier_subclusters()``
                (must have ``medoid`` and ``indices`` — the latter now
                also used to derive the sub-cluster's own dominant state).

        Returns:
            The same dicts, extended in place with ``market_cid``
            (``None`` when the pocket is delivered unassigned),
            ``road_miles``, ``road_minutes``, ``routing_degraded`` and
            ``state_affinity_score``.
        """
        if not subclusters:
            return []

        centroids = self._centroid_points()
        if not centroids:
            self._logger.warning(
                "No market centroids available for sub-cluster market "
                "selection; %s sub-cluster(s) left without a winner.",
                len(subclusters),
            )
            for subcluster in subclusters:
                subcluster['market_cid'] = None
                subcluster['road_miles'] = None
                subcluster['road_minutes'] = None
                subcluster['routing_degraded'] = True
                subcluster['state_affinity_score'] = None
            return subclusters

        self._reset_state_score_cache()
        cap = self._subcluster_anchor_cap()
        sizes: Dict[Any, int] = (
            self._data[self._data[self._cluster_id] != -1]
            .groupby(self._cluster_id).size().to_dict()
            if cap is not None and self._cluster_id in self._data.columns
            else {}
        )
        n_degraded = 0
        n_unplaced = 0
        n_beyond_cap = 0
        stores_beyond_cap = 0
        async with RoutingService() as routing:
            for subcluster in subclusters:
                medoid = subcluster['medoid']
                candidates = sorted(
                    centroids.items(),
                    key=lambda item: self._haversine_miles(
                        medoid[0], medoid[1], item[1][0], item[1][1]
                    ),
                )[: self.subcluster_market_candidates]

                degraded = False
                distances: Dict[Any, float] = {
                    cid: self._haversine_miles(
                        medoid[0], medoid[1], centroid[0], centroid[1]
                    )
                    for cid, centroid in candidates
                }
                road_minutes_map: Dict[Any, Optional[float]] = {}
                try:
                    matrix = await routing.distance_matrix(
                        [medoid] + [centroid for _, centroid in candidates]
                    )
                    degraded = bool(matrix.degraded)
                    if not degraded:
                        for cid, centroid in candidates:
                            leg = matrix.lookup(medoid, centroid)
                            distances[cid] = leg.distance_miles
                            road_minutes_map[cid] = leg.duration_minutes
                except Exception as exc:  # noqa: BLE001 — routing must never abort the run
                    degraded = True
                    self._logger.warning(
                        "Sub-cluster market selection fell back to haversine "
                        "order after routing error: %s", exc,
                    )

                if degraded:
                    n_degraded += 1

                pocket_len = len(subcluster.get('indices', []))
                if cap is not None:
                    feasible = {
                        cid: dist for cid, dist in distances.items()
                        if dist <= cap
                        and sizes.get(cid, 0) + pocket_len
                        <= self._effective_ceiling(cid)
                    }
                else:
                    feasible = distances

                if not feasible:
                    if self.reject_unanchorable_subclusters:
                        # Opt-in (FEAT-248 G4 behavior): deliver UNASSIGNED.
                        n_unplaced += 1
                        subcluster['market_cid'] = None
                        subcluster['road_miles'] = None
                        subcluster['road_minutes'] = None
                        subcluster['routing_degraded'] = degraded
                        subcluster['state_affinity_score'] = None
                        self._reject_subcluster_pocket(subcluster)
                        self._logger.info(
                            "Sub-cluster (%s store(s)) has no candidate market "
                            "within the %.1f-mile cap / with headroom; "
                            "delivered unassigned.",
                            pocket_len, cap,
                        )
                        continue

                    # Default (FEAT-249): restore the pre-FEAT-248
                    # 100%-assignment guarantee. Score the FULL unfiltered
                    # `distances` pool with pool-max normalization -- the
                    # same semantics the `cap is None` path already uses --
                    # and anchor the pocket to the winner instead of
                    # rejecting it. Tie-break identical to
                    # `_best_cession_receiver` (score desc, distance asc,
                    # cid asc) for determinism.
                    n_beyond_cap += 1
                    stores_beyond_cap += pocket_len
                    entity_state = self._dominant_state_of_indices(
                        subcluster.get('indices', [])
                    )
                    fallback_max_distance = max(distances.values())
                    fb_cid, fb_score, fb_distance = None, None, None
                    for cid, dist in distances.items():
                        score = self._state_affinity_score(
                            entity_state, cid, dist, fallback_max_distance
                        )
                        if (
                            fb_score is None
                            or score > fb_score
                            or (score == fb_score and dist < fb_distance)
                            or (
                                score == fb_score and dist == fb_distance
                                and cid < fb_cid
                            )
                        ):
                            fb_cid, fb_score, fb_distance = cid, score, dist

                    winner_cid = fb_cid
                    winner_score = fb_score
                    road_miles = fb_distance
                    road_minutes = road_minutes_map.get(winner_cid)

                    subcluster['market_cid'] = winner_cid
                    subcluster['road_miles'] = float(road_miles)
                    subcluster['road_minutes'] = (
                        float(road_minutes) if road_minutes is not None else None
                    )
                    subcluster['routing_degraded'] = degraded
                    subcluster['state_affinity_score'] = winner_score
                    subcluster['anchored_beyond_cap'] = True
                    self._logger.info(
                        "Sub-cluster (%s store(s)) has no candidate market "
                        "within the %.1f-mile cap / with headroom; anchored "
                        "beyond cap to market %s (%.1f road mi, score=%.3f).",
                        pocket_len, cap, winner_cid, road_miles, winner_score,
                    )
                    continue

                entity_state = self._dominant_state_of_indices(
                    subcluster.get('indices', [])
                )
                max_distance = (
                    cap if cap is not None
                    else (max(feasible.values()) if feasible else 0.0)
                )
                winner_cid = max(
                    feasible,
                    key=lambda cid: (
                        self._state_affinity_score(
                            entity_state, cid, feasible[cid], max_distance
                        ),
                        -feasible[cid],
                    ),
                )
                winner_score = self._state_affinity_score(
                    entity_state, winner_cid, feasible[winner_cid], max_distance
                )
                road_miles = feasible[winner_cid]
                road_minutes = road_minutes_map.get(winner_cid)

                subcluster['market_cid'] = winner_cid
                subcluster['road_miles'] = float(road_miles)
                subcluster['road_minutes'] = (
                    float(road_minutes) if road_minutes is not None else None
                )
                subcluster['routing_degraded'] = degraded
                subcluster['state_affinity_score'] = winner_score
                self._logger.debug(
                    "Sub-cluster (%s store(s)) -> market %s: %.1f road mi, "
                    "score=%.3f (degraded=%s)",
                    len(subcluster.get('indices', [])), winner_cid, road_miles,
                    winner_score, degraded,
                )

        self._logger.info(
            "Sub-cluster market selection: %s sub-cluster(s), %s degraded, "
            "%s delivered unassigned (no candidate within cap/headroom), "
            "%s pocket(s) / %s store(s) anchored beyond cap",
            len(subclusters), n_degraded, n_unplaced,
            n_beyond_cap, stores_beyond_cap,
        )
        return subclusters

    # -- Fly-out peel pass (FEAT-243, Module 2) ------------------------------
    # Assigned stores too far from — or with no road path to — their own
    # market's centroid never enter the FEAT-241 pool (it only sees
    # cluster_id == -1 leftovers). This pass finds them (Rule A: haversine
    # distance; Rule B: routing-probe island detection) and routes them into
    # the FEAT-241 sub-cluster machinery: internally, for standalone
    # markets, or back into the pool, for normal markets. Runs once in
    # run(), right after `_absorb_remnant_stores()` and before
    # `_attach_outlier_subclusters()`.

    async def _peel_flyout_stores(self) -> int:
        """Peel unreachable assigned stores into fly-out sub-clusters.

        Opt-in (``subcluster_flyout``, requires ``subcluster_outliers``).
        Two eligibility rules, both keyed off ``max_distance_by_day``
        (inactive — no peels, no routing calls — when it is ``None`` or
        ``<= 0``):

        - Rule A (distance): haversine store -> own market centroid >
          ``flyout_distance_factor * max_distance_by_day``.
        - Rule B (no road path): for stores beyond
          ``flyout_probe_factor * max_distance_by_day`` and not already
          Rule-A eligible, one shared-session routing matrix per affected
          market (``[centroid] + far stores``) detects unroutable
          (island) legs — eligible iff the leg is ``degraded`` while the
          matrix's ``backend`` is not ``"geodesic"`` (a whole-matrix
          geodesic fallback means a backend outage, not an island, and
          peels nothing for that market).

        A standalone market's peeled rows are pocketed internally
        (``_form_outlier_subclusters``) and stamped with the FEAT-241
        seven-column contract while keeping their own market identity —
        ``_select_subcluster_market`` is skipped, cid/market/ghost_id are
        never touched. A non-standalone market's peeled rows are returned
        to the ``cluster_id == -1`` pool (market label cleared) so the
        very next call, ``_attach_outlier_subclusters()``, absorbs them by
        road miles exactly like any other outlier.

        Called once in ``run()``, right after ``_absorb_remnant_stores()``.

        Returns:
            Number of stores peeled (Rule A + Rule B combined).
        """
        if not self.subcluster_flyout or self._data.empty:
            return 0
        if self.max_distance_by_day is None or self.max_distance_by_day <= 0:
            return 0

        self._recompute_cluster_centroids()
        centroids = self._centroid_points()
        if not centroids:
            return 0

        assigned_mask = self._data[self._cluster_id] != -1
        if 'is_subcluster' in self._data.columns:
            assigned_mask &= self._data['is_subcluster'] != True
        candidates = self._data[assigned_mask]
        if candidates.empty:
            return 0

        distance_threshold = self.flyout_distance_factor * self.max_distance_by_day
        probe_threshold = self.flyout_probe_factor * self.max_distance_by_day

        rule_a_idx: List[Any] = []
        probe_idx: List[Any] = []
        for idx in sorted(candidates.index):
            row = candidates.loc[idx]
            cid = row[self._cluster_id]
            centroid = centroids.get(cid)
            if centroid is None:
                continue
            dist = self._haversine_miles(
                centroid[0], centroid[1], row['latitude'], row['longitude']
            )
            if dist > distance_threshold:
                rule_a_idx.append(idx)
            elif dist > probe_threshold:
                probe_idx.append(idx)

        rule_b_idx: List[Any] = []
        market_matrices: Dict[Any, DistanceMatrix] = {}
        probed_markets = 0
        degraded_markets = 0
        if probe_idx:
            by_market: Dict[Any, List[Any]] = {}
            for idx in probe_idx:
                cid = self._data.at[idx, self._cluster_id]
                by_market.setdefault(cid, []).append(idx)

            async with RoutingService() as routing:
                for cid in sorted(by_market.keys(), key=str):
                    idxs = sorted(by_market[cid])
                    centroid = centroids.get(cid)
                    if centroid is None:
                        continue
                    locations = [centroid] + [
                        (
                            float(self._data.at[i, 'latitude']),
                            float(self._data.at[i, 'longitude']),
                        )
                        for i in idxs
                    ]
                    probed_markets += 1
                    try:
                        matrix = await routing.distance_matrix(locations)
                    except Exception as exc:  # noqa: BLE001 — never abort the run
                        self._logger.warning(
                            "Fly-out Rule B probe failed for market %s: %s "
                            "— peeling nothing there this run.", cid, exc,
                        )
                        continue
                    if matrix.backend == "geodesic":
                        degraded_markets += 1
                        self._logger.warning(
                            "Fly-out Rule B probe for market %s degraded to "
                            "the geodesic fallback (backend outage) — "
                            "peeling nothing there this run.", cid,
                        )
                        continue
                    market_matrices[cid] = matrix
                    for i in idxs:
                        store_loc = (
                            float(self._data.at[i, 'latitude']),
                            float(self._data.at[i, 'longitude']),
                        )
                        try:
                            leg = matrix.lookup(centroid, store_loc)
                        except KeyError:
                            continue
                        if leg.degraded:
                            rule_b_idx.append(i)

        peel_idx = sorted(set(rule_a_idx) | set(rule_b_idx))
        if not peel_idx:
            self._logger.info(
                "Fly-out peel: 0 store(s) peeled (%s candidate(s) checked, "
                "%s market(s) probed, %s degraded).",
                len(candidates), probed_markets, degraded_markets,
            )
            return 0

        self._init_subcluster_columns()

        by_cid: Dict[Any, List[Any]] = {}
        for idx in peel_idx:
            cid = self._data.at[idx, self._cluster_id]
            by_cid.setdefault(cid, []).append(idx)

        standalone_count = 0
        pool_count = 0
        for cid in sorted(by_cid.keys(), key=str):
            idxs = sorted(by_cid[cid])
            if cid in self._standalone_clusters:
                self._pocket_flyout_standalone_market(
                    cid, idxs, centroids.get(cid), market_matrices.get(cid)
                )
                standalone_count += len(idxs)
            else:
                for i in idxs:
                    self._data.at[i, self._cluster_id] = -1
                    self._data.at[i, self._cluster_name] = 'Outlier'
                    self._data.at[i, 'ghost_id'] = None
                    if 'constraint_reason' in self._data.columns:
                        self._data.at[i, 'constraint_reason'] = (
                            'flyout_peel_pending_reassignment'
                        )
                    self._outlier_stores.add(i)
                pool_count += len(idxs)

        self._logger.info(
            "Fly-out peel: %s store(s) peeled (%s Rule A, %s Rule B) — "
            "%s standalone-internal, %s returned to the pool; %s market(s) "
            "probed, %s degraded.",
            len(peel_idx), len(rule_a_idx), len(rule_b_idx),
            standalone_count, pool_count, probed_markets, degraded_markets,
        )
        return len(peel_idx)

    def _pocket_flyout_standalone_market(
        self,
        cid: Any,
        indices: List[Any],
        centroid: Optional[Tuple[float, float]],
        matrix: Optional[DistanceMatrix],
    ) -> None:
        """Pocket a standalone market's peeled rows without changing identity.

        Reuses ``_form_outlier_subclusters`` on the subset of rows that
        qualified for fly-out, then stamps the FEAT-241 seven-column
        contract keeping ``cid``/market label/``ghost_id`` untouched —
        the whole point of a standalone market never losing a row.

        Args:
            cid: The standalone market's cluster id (unchanged on exit).
            indices: Row indices that qualified for fly-out in this market.
            centroid: The market's own centroid, or ``None`` if it never
                settled to a real coordinate (rows are still pocketed;
                road miles fall back to ``None``/degraded).
            matrix: The Rule B probe matrix for this market, if one was
                successfully computed, else ``None``.
        """
        rows = self._data.loc[indices]
        pockets = self._form_outlier_subclusters(rows)
        for pocket in pockets:
            p_indices = pocket['indices']
            medoid_lat, medoid_lon = pocket['medoid']
            days = pocket['days']

            road_miles: Optional[float] = None
            road_minutes: Optional[float] = None
            degraded = True
            if matrix is not None and centroid is not None:
                try:
                    leg = matrix.lookup(centroid, (medoid_lat, medoid_lon))
                    road_miles = leg.distance_miles
                    road_minutes = leg.duration_minutes
                    degraded = leg.degraded
                except KeyError:
                    pass
            if road_miles is None and centroid is not None:
                road_miles = self._haversine_miles(
                    medoid_lat, medoid_lon, centroid[0], centroid[1]
                )

            overnight = self._overnight_required(days, road_minutes)
            uid = min(p_indices)

            for idx in p_indices:
                self._data.at[idx, 'is_subcluster'] = True
                self._data.at[idx, 'subcluster_lat'] = medoid_lat
                self._data.at[idx, 'subcluster_lon'] = medoid_lon
                self._data.at[idx, 'subcluster_road_miles'] = road_miles
                self._data.at[idx, 'subcluster_days'] = days
                self._data.at[idx, 'overnight_required'] = overnight
                self._data.at[idx, 'subcluster_routing_degraded'] = degraded
                self._data.at[idx, 'subcluster_uid'] = uid

        self._logger.debug(
            "Fly-out standalone pocketing: market %s, %s row(s) -> %s "
            "pocket(s).", cid, len(indices), len(pockets),
        )

    def _overnight_required(
        self, days: int, road_minutes: Optional[float]
    ) -> bool:
        """Whether a sub-cluster's assigned employee must stay overnight.

        Shared by ``_attach_outlier_subclusters`` (FEAT-241) and
        ``_pocket_flyout_standalone_market`` (FEAT-243): a multi-day
        pocket always requires it, and so does a one-way trip longer
        than half a workday even when the pocket itself fits in one day.

        Args:
            days: The sub-cluster's day budget (``1`` or ``2``).
            road_minutes: One-way road minutes to the sub-cluster, or
                ``None`` when no routed leg was available.

        Returns:
            ``True`` when the employee needs to stay overnight.
        """
        return days >= 2 or (
            road_minutes is not None
            and road_minutes > (self.day_hours / 2) * 60
        )

    # -- Capacity shed pass (FEAT-243, Module 3) -----------------------------
    # `_reassign_borderline_pass` only re-evaluates FAR stores and demands a
    # reassign_overflow_gain-sized distance saving to spend a market's
    # buffered slots — capacity pressure is not one of its move criteria.
    # This pass complements it: an oversubscribed market (row count,
    # satellites included, above its layout ceiling) hands near-boundary
    # NORMAL stores to a neighbor with room at similar distance, with no
    # gain requirement. Runs once in run(), after
    # `_attach_outlier_subclusters()` (so satellite load is counted) and
    # before the final `_recompute_cluster_centroids()` +
    # `_repair_assignments()` pair.

    def _capacity_shed_pass(self) -> int:
        """Shed near-boundary normal stores from oversubscribed markets.

        Opt-in (``capacity_shedding``). For each non-standalone market
        whose total row count (satellites, i.e. ``is_subcluster`` rows,
        included) exceeds ``_effective_ceiling(cid)``, hands up to
        ``size - ceiling`` of its non-subcluster members to a neighbor
        market with room (``_capacity_for``, the hard receiving gate) at
        a similar distance (``shed_distance_tolerance * own_distance``).
        Unlike ``_reassign_borderline_pass``, this pass applies neither
        ``reassign_overflow_gain`` nor the 20% buffer
        (``_borderline_target_allowed``) — capacity, not distance gain,
        is the criterion, so it is never called here.

        FEAT-248 TASK-203 shed floor: the amount shed is capped to
        ``max(0, core_size - min_cluster_size)`` — this pass never drains
        a donor's CORE (non-satellite) count below ``min_cluster_size``,
        even when its total overload (core + satellites) is larger; a
        market whose overage is mostly satellite load is cession's
        (``_cede_oversize_subclusters``) territory, not this pass's.

        Moves are committed greedily by smallest added distance
        (deterministic: added miles, then store index), updating a live
        size ledger as each move commits so a target market can never be
        pushed past its own receiving gate within the same sweep.

        Distances are computed fresh via ``_haversine_miles`` against
        ``_centroid_points()`` rather than trusting the ``distance_to_
        center`` column, which is stale by this point in ``run()``.

        Sync method — no routing, no await.

        Called once in ``run()``, after ``_attach_outlier_subclusters()``.

        Returns:
            Number of stores shed.
        """
        if not self.capacity_shedding or self._data.empty:
            return 0

        self._recompute_cluster_centroids()
        centroids = self._centroid_points()
        if not centroids:
            return 0

        partition = self._partition_mask(self._data)
        assign_distance = self._max_force_assign_distance or float('inf')

        ledger: Dict[Any, int] = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size().to_dict()

        sorted_targets = sorted(centroids.items(), key=lambda kv: str(kv[0]))

        total_shed = 0
        for cid in sorted(
            (c for c in ledger if c not in self._standalone_clusters),
            key=str,
        ):
            size = ledger.get(cid, 0)
            ceiling = self._effective_ceiling(cid)
            overload = size - ceiling
            if overload <= 0:
                continue
            overload = int(overload)

            own_centroid = centroids.get(cid)
            if own_centroid is None:
                continue

            source_rows = self._data[self._data[self._cluster_id] == cid]
            if 'is_subcluster' in source_rows.columns:
                source_rows = source_rows[source_rows['is_subcluster'] != True]
            if source_rows.empty:
                continue

            # FEAT-248 TASK-203: shed floor -- this pass may never drain a
            # donor's CORE below min_cluster_size. `overload` above is
            # measured against total size (satellites included); the
            # floor is measured against core_size (source_rows already
            # excludes satellites) so a market carrying most of its
            # ceiling-overage as sub-cluster load never gets its core
            # stripped to compensate.
            core_size = len(source_rows)
            floor_shed = max(0, core_size - int(self.min_cluster_size or 0))
            if floor_shed < overload:
                self._logger.info(
                    "Capacity shed: market %s overload=%s truncated to %s "
                    "to keep its core (%s stores) at/above "
                    "min_cluster_size=%s.",
                    cid, overload, floor_shed, core_size, self.min_cluster_size,
                )
                overload = floor_shed
            if overload <= 0:
                continue

            candidate_moves: List[Tuple[float, Any, Any, float]] = []
            for idx in sorted(source_rows.index):
                store = source_rows.loc[idx]
                lat, lon = store['latitude'], store['longitude']
                own_distance = self._haversine_miles(
                    own_centroid[0], own_centroid[1], lat, lon
                )
                store_partition = (
                    bool(partition.loc[idx]) if partition is not None else None
                )

                best_target: Optional[Any] = None
                best_distance: Optional[float] = None
                for other_cid, other_centroid in sorted_targets:
                    if other_cid == cid or other_cid in self._standalone_clusters:
                        continue
                    if ledger.get(other_cid, 0) >= self._capacity_for(other_cid):
                        continue
                    if (
                        partition is not None
                        and self._cluster_partition.get(other_cid, False)
                        != store_partition
                    ):
                        continue
                    target_distance = self._haversine_miles(
                        other_centroid[0], other_centroid[1], lat, lon
                    )
                    if target_distance > self.shed_distance_tolerance * own_distance:
                        continue
                    if target_distance > assign_distance:
                        continue
                    if best_distance is None or target_distance < best_distance:
                        best_distance = target_distance
                        best_target = other_cid

                if best_target is not None:
                    candidate_moves.append(
                        (best_distance - own_distance, idx, best_target, best_distance)
                    )

            candidate_moves.sort(key=lambda item: (item[0], str(item[1])))

            shed_from_market = 0
            for added_miles, idx, target, target_distance in candidate_moves:
                if shed_from_market >= overload:
                    break
                # Re-check live: an earlier move in this same sweep may
                # have just filled the target's last slot.
                if ledger.get(target, 0) >= self._capacity_for(target):
                    continue

                self._data.at[idx, self._cluster_id] = target
                self._data.at[idx, self._cluster_name] = f"Market-{target}"
                self._data.at[idx, 'ghost_id'] = f"Ghost-{target}-1"

                ledger[cid] = ledger.get(cid, 1) - 1
                ledger[target] = ledger.get(target, 0) + 1
                shed_from_market += 1
                total_shed += 1
                self._logger.debug(
                    "Capacity shed: store index %s Market-%s -> Market-%s "
                    "(+%.1f mi, target now %.1f mi).",
                    idx, cid, target, added_miles, target_distance,
                )

            if shed_from_market:
                self._logger.info(
                    "Capacity shed: market %s shed %s/%s overload store(s).",
                    cid, shed_from_market, overload,
                )

        if total_shed:
            self._recompute_cluster_centroids()

        return total_shed

    # -- Scheduling feedback pass (FEAT-244) ---------------------------------
    # Opt-in (`optimize`). Runs an internal SchedulingVisits pass against
    # this component's own clustering output and reads back
    # `exception_stores_df` as ground truth to correct exceptions the
    # geometry-only heuristics above (`_peel_flyout_stores`,
    # `_capacity_shed_pass`) missed. Called once in `run()`, after
    # `_capacity_shed_pass()` and before the final
    # `_recompute_cluster_centroids()` + `_repair_assignments()` pair.

    def _estimate_schedulable(self, scheduling_kwargs: dict) -> int:
        """Lightweight estimate of total schedulable stores.

        For each market, counts regular stores capped at the employee's
        available-day capacity (workdays minus block days reserved for
        sub-clusters), plus all sub-cluster stores (which have their own
        reserved days).  Outlier stores (``cluster_id == -1``) are
        excluded entirely.

        Used by the scheduling feedback pass's net-improvement gate
        (AC-2, TASK-187) to decide whether the reassignments it made
        improved or worsened the layout.

        Args:
            scheduling_kwargs: The scheduling parameters — ``year``,
                ``month``, and ``max_visits_per_day`` are read from here.

        Returns:
            Estimated count of stores that can be scheduled.
        """
        import calendar

        year = scheduling_kwargs.get('year', 2026)
        month = scheduling_kwargs.get('month', 1)
        max_visits = scheduling_kwargs.get('max_visits_per_day', 5)

        _, days_in_month = calendar.monthrange(year, month)
        workdays = sum(
            1 for d in range(1, days_in_month + 1)
            if calendar.weekday(year, month, d) < 5
        )

        assigned = self._data[self._data[self._cluster_id] != -1]
        if assigned.empty:
            return 0

        has_sub = 'is_subcluster' in assigned.columns
        has_days = 'subcluster_days' in assigned.columns
        has_label = 'sub_cluster' in assigned.columns

        total = 0
        for _cid, group in assigned.groupby(self._cluster_id):
            if has_sub:
                sub_mask = group['is_subcluster'].fillna(False).astype(bool)
            else:
                sub_mask = pd.Series(False, index=group.index)

            n_regular = int((~sub_mask).sum())
            n_subcluster = int(sub_mask.sum())

            # Block days consumed by this market's sub-clusters —
            # one value per unique sub-cluster label.
            block_days = 0
            if has_days and has_label and sub_mask.any():
                block_days = int(
                    group.loc[sub_mask]
                    .groupby('sub_cluster')['subcluster_days']
                    .first()
                    .fillna(0)
                    .sum()
                )

            available_days = max(workdays - block_days, 0)
            schedulable_regular = min(n_regular, available_days * max_visits)
            total += schedulable_regular + n_subcluster

        return total

    async def _scheduling_feedback_pass(self) -> None:
        """Correct clustering exceptions using an internal scheduling run.

        Instantiates ``SchedulingVisits(input=self._data,
        **self._scheduling_kwargs)`` as a black-box oracle, awaits
        ``start()`` + ``run()``, and reads back ``exception_stores_df``.
        Exceptions are classified into three categories from the
        roundtrip feasibility threshold computed from the internal SV's
        own config:

        - **Distance-impossible** (``distance_from_start_miles`` beyond
          the threshold): standalone markets pocket the store internally
          (``_pocket_flyout_standalone_market``, reusing
          ``_form_outlier_subclusters``); normal markets return it to the
          outlier pool (``cluster_id = -1``).
        - **Capacity-saturated** (within threshold, no feasible day):
          shed to a neighbor market with room (adapted
          ``_capacity_shed_pass`` mechanics, keyed by the exception count
          per market rather than ``_layout_ceiling``); failing that,
          converted to a sub-cluster via the pool; failing that, logged
          as a ghost-increase recommendation.
        - **Block overflow** (``no_free_block_days``): the affected
          sub-cluster's ``subcluster_days`` is recalculated from
          ``ceil(stores * in_store_visit_hours / day_duration)``.

        Fail-safe: any exception raised by the internal SchedulingVisits
        run is caught, logged as a warning, and no exception-driven
        correction is made. The one part of ``self._data`` touched even
        on this path is ``_label_subclusters()`` (see below), which is
        idempotent and harmless — the canonical call later in ``run()``
        (once markets are renumbered) fully re-stamps the same column,
        so the delivered clustering output is unaffected by a crash here.

        No intermediate files are written (spec §1 Non-Goals) — the
        internal run is never given ``exceptions_filename`` or any other
        output-file kwarg, so ``SchedulingVisits`` itself writes nothing
        to disk; only summary counts are logged.

        A single pass, not a convergence loop (spec §1 Non-Goals).

        Only executes when ``self._optimize`` is True.
        """
        if not self._optimize or self._data.empty:
            return

        # SchedulingVisits' block scheduler groups sub-cluster rows by the
        # `sub_cluster` column (`groupby('sub_cluster')`, which drops NaN
        # groups by default). That label is normally stamped only once,
        # late in run() by `_label_subclusters()` — at this point in the
        # pipeline it is still None for every is_subcluster row, which
        # would make every existing pocket silently vanish from the
        # internal run's schedule/exceptions instead of surfacing as a
        # block-overflow exception. `_label_subclusters()` is idempotent
        # (it recomputes fresh from `self._cluster_name` every call) and
        # runs again, safely, once markets are renumbered later in run().
        self._label_subclusters()

        scheduling_kwargs = dict(self._scheduling_kwargs)
        # Observation-only SV features that cost real time and do not
        # affect packing decisions (spec §7 Known Risks) — force off
        # regardless of what the caller passed.
        scheduling_kwargs['resolve_start_location'] = False
        scheduling_kwargs['return_geometry'] = 'none'
        # The feedback pass only needs to classify exceptions (distance-
        # impossible vs capacity-saturated), not produce road-accurate
        # routes.  Geodesic distances (haversine × detour_factor) are
        # good enough for this triage and avoid the ~50 s / market
        # Valhalla matrix request that makes this pass 100+ min on a
        # 122-market dataset.
        scheduling_kwargs['routing_backend'] = 'geodesic'

        # _apply_visit_rule_columns() runs later in run(), so at this point
        # the DataFrame still has the numeric visit count under
        # 'visit_frequency' instead of the cadence string SV expects.
        # Apply the column rename to a shallow copy so the internal SV
        # gets the right schema without mutating self._data prematurely.
        feedback_data = self._data.copy()
        self._apply_visit_rule_columns(feedback_data)

        try:
            sv = SchedulingVisits(input=feedback_data, **scheduling_kwargs)
            await sv.start()
            await sv.run()
        except Exception as exc:  # noqa: BLE001 — never abort the run
            self._logger.warning(
                "Scheduling feedback pass: internal SchedulingVisits run "
                "failed (%s) — keeping pre-feedback clustering.", exc,
            )
            return

        exc_df = sv.exception_stores_df
        if exc_df is None or exc_df.empty:
            self._logger.info(
                "Scheduling feedback pass: 0 exceptions from the internal "
                "SchedulingVisits run — clustering already optimal."
            )
            return

        if sv.roundtrip:
            threshold_miles = (
                (sv.day_duration - sv.in_store_visit_hours) / 2
            ) * sv.average_speed
        else:
            threshold_miles = (
                sv.day_duration - sv.in_store_visit_hours
            ) * sv.average_speed

        reason_no_day = "No feasible day in cadence window or month"
        # `distance_from_start_miles` is absent entirely (not just NaN) when
        # every exception this run is a block-overflow row (SV's
        # `_subcluster_block_exception_rows` never sets it) — guard the
        # column's existence before comparing.
        if 'distance_from_start_miles' in exc_df.columns:
            distance_col = exc_df['distance_from_start_miles']
        else:
            distance_col = pd.Series(np.nan, index=exc_df.index)
        distance_mask = (
            (exc_df['reason'] == reason_no_day)
            & (distance_col > threshold_miles)
        )
        capacity_mask = (
            (exc_df['reason'] == reason_no_day)
            & (distance_col <= threshold_miles)
        )
        block_mask = exc_df['reason'] == 'no_free_block_days'

        # `exception_stores_df` is one row per unscheduled STORE VISIT, so
        # a store with visit_rule > 1 (multiple required visits/month) can
        # appear more than once. Dedupe by store_id before iterating so a
        # store is never pocketed/pooled twice in the same pass (the
        # capacity-saturated loop below is self-guarding against this via
        # its live cluster_id re-check; this loop has no such re-check, so
        # the dedup must happen up front).
        distance_impossible = exc_df[distance_mask].drop_duplicates('store_id')
        capacity_saturated = exc_df[capacity_mask]
        block_overflow = exc_df[block_mask]

        store_id_to_idx: Dict[Any, Any] = {
            store_id: idx for idx, store_id in self._data['store_id'].items()
        }

        # AC-2 (TASK-187): snapshot before any reassignment so we can
        # revert if the modifications end up net-negative.
        # FEAT-249 (TASK-208): the rejection ledger is also snapshotted --
        # a revert that restores only `_data` leaves `_rejected`/
        # `_outlier_stores`/`_readmitted_index_map` mutated, so the final
        # ledger disagrees with the delivery it is supposed to describe.
        data_snapshot = self._data.copy()
        rejected_snapshot = self._rejected.copy()
        outliers_snapshot = set(self._outlier_stores)
        readmitted_snapshot = dict(self._readmitted_index_map)
        pre_schedulable = self._estimate_schedulable(scheduling_kwargs)

        recovered = 0
        standalone_pocketed = 0
        pool_returned = 0
        ghost_recommendations: Dict[Any, int] = {}
        # idx -> the market it was pulled from, for every store sent to the
        # cluster_id=-1 pool this pass (distance-impossible normal-market
        # returns and capacity-saturated no-neighbor returns). Used after
        # `_attach_outlier_subclusters()` to confirm placement actually
        # happened — `recovered` must count confirmed outcomes, not
        # attempts, and a store `_attach_outlier_subclusters()` could not
        # place (no market centroid available) must still surface as an
        # operator-visible ghost-increase recommendation rather than
        # silently vanishing from the summary.
        pool_returned_origin: Dict[Any, Any] = {}

        # --- Distance-impossible ---------------------------------------
        by_market_distance: Dict[Any, List[Any]] = {}
        for _, exc_row in distance_impossible.iterrows():
            idx = store_id_to_idx.get(exc_row['store_id'])
            if idx is None or idx not in self._data.index:
                continue
            cid = self._data.at[idx, self._cluster_id]
            by_market_distance.setdefault(cid, []).append(idx)

        if by_market_distance:
            self._recompute_cluster_centroids()
            centroids = self._centroid_points()
            for cid, idxs in by_market_distance.items():
                if cid in self._standalone_clusters:
                    self._pocket_flyout_standalone_market(
                        cid, idxs, centroids.get(cid), None
                    )
                    standalone_pocketed += len(idxs)
                else:
                    for idx in idxs:
                        self._data.at[idx, self._cluster_id] = -1
                        self._data.at[idx, self._cluster_name] = 'Outlier'
                        self._data.at[idx, 'ghost_id'] = None
                        if 'constraint_reason' in self._data.columns:
                            self._data.at[idx, 'constraint_reason'] = (
                                'scheduling_feedback_distance_impossible'
                            )
                        pool_returned_origin[idx] = cid
                    pool_returned += len(idxs)
                recovered += len(idxs)

        # --- Capacity-saturated ------------------------------------------
        self._recompute_cluster_centroids()
        centroids = self._centroid_points()
        partition = self._partition_mask(self._data)
        assign_distance = self._max_force_assign_distance or float('inf')

        ledger: Dict[Any, int] = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size().to_dict()

        by_market_capacity: Dict[Any, pd.DataFrame] = {
            cid: rows for cid, rows in capacity_saturated.groupby('market_id')
        }
        for cid in sorted(by_market_capacity.keys(), key=str):
            rows = by_market_capacity[cid].sort_values(
                by='distance_from_start_miles', ascending=False
            )
            own_centroid = centroids.get(cid)
            for _, exc_row in rows.iterrows():
                idx = store_id_to_idx.get(exc_row['store_id'])
                if idx is None or idx not in self._data.index:
                    continue
                if self._data.at[idx, self._cluster_id] != cid:
                    continue  # already moved earlier this pass
                store = self._data.loc[idx]
                lat, lon = store['latitude'], store['longitude']
                store_partition = (
                    bool(partition.loc[idx]) if partition is not None else None
                )
                own_distance = (
                    self._haversine_miles(own_centroid[0], own_centroid[1], lat, lon)
                    if own_centroid is not None else float('inf')
                )

                best_target: Optional[Any] = None
                best_distance: Optional[float] = None
                for other_cid, other_centroid in sorted(
                    centroids.items(), key=lambda kv: str(kv[0])
                ):
                    if other_cid == cid or other_cid in self._standalone_clusters:
                        continue
                    if ledger.get(other_cid, 0) >= self._capacity_for(other_cid):
                        continue
                    if (
                        partition is not None
                        and self._cluster_partition.get(other_cid, False)
                        != store_partition
                    ):
                        continue
                    target_distance = self._haversine_miles(
                        other_centroid[0], other_centroid[1], lat, lon
                    )
                    # With market_center='base' (the default) a market's
                    # centroid can BE one of its own stores — including,
                    # for a small/single-core market, the very exception
                    # store being evaluated here (own_distance == 0). The
                    # "similar distance" tolerance is meaningless against a
                    # zero baseline (tolerance * 0 == 0, so it would reject
                    # every real neighbor and this scheduling-proven
                    # necessary move could never happen); fall back to the
                    # assign_distance-only gate for that case instead.
                    if (
                        own_centroid is not None
                        and own_distance > 1e-6
                        and target_distance > self.shed_distance_tolerance * own_distance
                    ):
                        continue
                    if target_distance > assign_distance:
                        continue
                    if best_distance is None or target_distance < best_distance:
                        best_distance = target_distance
                        best_target = other_cid

                if best_target is not None:
                    self._data.at[idx, self._cluster_id] = best_target
                    self._data.at[idx, self._cluster_name] = f"Market-{best_target}"
                    self._data.at[idx, 'ghost_id'] = f"Ghost-{best_target}-1"
                    ledger[cid] = ledger.get(cid, 1) - 1
                    ledger[best_target] = ledger.get(best_target, 0) + 1
                    recovered += 1
                    self._logger.debug(
                        "Scheduling feedback shed: store %s Market-%s -> "
                        "Market-%s.", exc_row['store_id'], cid, best_target,
                    )
                elif self.subcluster_outliers:
                    self._data.at[idx, self._cluster_id] = -1
                    self._data.at[idx, self._cluster_name] = 'Outlier'
                    self._data.at[idx, 'ghost_id'] = None
                    if 'constraint_reason' in self._data.columns:
                        self._data.at[idx, 'constraint_reason'] = (
                            'scheduling_feedback_capacity_saturated'
                        )
                    ledger[cid] = ledger.get(cid, 1) - 1
                    pool_returned_origin[idx] = cid
                    pool_returned += 1
                    recovered += 1
                else:
                    ghost_recommendations[cid] = (
                        ghost_recommendations.get(cid, 0) + 1
                    )

        # --- Block overflow ------------------------------------------------
        block_recalculated = 0
        if not block_overflow.empty and 'sub_cluster' in self._data.columns:
            for sub_cluster_label, _rows in block_overflow.groupby('sub_cluster'):
                if not sub_cluster_label:
                    continue
                mask = self._data['sub_cluster'] == sub_cluster_label
                n_stores = int(self._data.loc[mask, 'store_id'].nunique())
                if n_stores == 0:
                    continue
                new_days = math.ceil(
                    n_stores * sv.in_store_visit_hours / sv.day_duration
                )
                self._data.loc[mask, 'subcluster_days'] = new_days
                block_recalculated += n_stores
                self._logger.info(
                    "Scheduling feedback: sub-cluster %s recalculated to "
                    "%s day(s) for %s store(s) (block overflow).",
                    sub_cluster_label, new_days, n_stores,
                )

        # --- Re-absorb pool + refresh geometry ------------------------------
        if pool_returned:
            await self._attach_outlier_subclusters()

        self._recompute_cluster_centroids()

        # `_attach_outlier_subclusters()` can leave a pocket unplaced (no
        # market centroid available to select from) — confirm every store
        # sent to the pool this pass actually landed somewhere before
        # counting it as `recovered`. A store still at cluster_id == -1 is
        # a genuine residual exception with no automated fix left; it must
        # surface as a ghost-increase recommendation rather than silently
        # inflating the "recovered" figure.
        pool_unresolved = 0
        for idx, orig_cid in pool_returned_origin.items():
            if idx not in self._data.index:
                continue
            if self._data.at[idx, self._cluster_id] == -1:
                pool_unresolved += 1
                recovered -= 1
                ghost_recommendations[orig_cid] = (
                    ghost_recommendations.get(orig_cid, 0) + 1
                )

        for cid, count in ghost_recommendations.items():
            self._logger.warning(
                "Scheduling feedback: Market-%s needs additional ghost "
                "capacity -- %s store(s) remain unresolved (could not be "
                "shed or sub-clustered).", cid, count,
            )

        self._logger.info(
            "Scheduling feedback pass summary: %s exception(s) before "
            "(%s distance-impossible, %s capacity-saturated, %s "
            "block-overflow) -> %s recovered (%s standalone-pocketed, %s "
            "pool-returned, %s of which stayed unresolved), %s block "
            "store(s) recalculated, %s market(s) flagged for a "
            "ghost-increase recommendation.",
            len(exc_df), len(distance_impossible), len(capacity_saturated),
            len(block_overflow), recovered, standalone_pocketed,
            pool_returned, pool_unresolved, block_recalculated,
            len(ghost_recommendations),
        )

        # AC-2 (TASK-187): net-improvement gate. If the reassignments
        # reduced the total schedulable stores (e.g. block-day cascade:
        # sub-cluster exclusive days consume regular employee capacity),
        # revert ALL changes and keep the pre-feedback clustering.
        post_schedulable = self._estimate_schedulable(scheduling_kwargs)
        if post_schedulable < pre_schedulable:
            self._logger.warning(
                "Scheduling feedback pass: net-negative result "
                "(%d → %d estimated schedulable stores, delta %+d). "
                "Reverting all reassignments — keeping pre-feedback "
                "clustering.",
                pre_schedulable, post_schedulable,
                post_schedulable - pre_schedulable,
            )
            # FEAT-249 (TASK-208): a reverted pass must be a true no-op --
            # restore every structure the pass mutated, not just `_data`,
            # so the final ledger (`Total rejected stores`,
            # `_save_rejected_stores()`) never disagrees with the delivery.
            self._data = data_snapshot
            self._rejected = rejected_snapshot
            self._outlier_stores = outliers_snapshot
            self._readmitted_index_map = readmitted_snapshot
            return

        self._logger.info(
            "Scheduling feedback pass: net-improvement gate passed "
            "(%d → %d estimated schedulable stores, delta %+d).",
            pre_schedulable, post_schedulable,
            post_schedulable - pre_schedulable,
        )

    # -- Assignment, column contract & pipeline wiring (FEAT-241, Module 4) -
    # Orchestrates Module 2 (formation) + Module 3 (selection), stamps the
    # seven-column contract, and provides the post-renumbering label. The
    # exemption guards themselves (centroid exclusion, own-medoid distance,
    # repair-pass skips) live inline in each pass touched — see the
    # `is_subcluster` checks in `_recompute_cluster_centroids`,
    # `_add_distance_to_center_column`, `_neighbourhood_repair_pass`,
    # `_ejection_chain_pass` and `_reassign_borderline_pass`.

    def _init_subcluster_columns(self) -> None:
        """Add the FEAT-241 column contract to the full DataFrame.

        False/NaN/None defaults so normal rows carry the columns too.
        Only called when ``subcluster_outliers`` is on — while it is off,
        these columns are never added, so the output stays byte-identical
        to current behaviour.

        Idempotent (FEAT-243): a no-op once the columns exist. Both
        ``_peel_flyout_stores`` and ``_attach_outlier_subclusters`` call
        this in the same run — without the guard, the second call would
        wipe the first pass's ``is_subcluster``/medoid stamps back to
        their defaults.
        """
        if self._data.empty:
            return
        if 'is_subcluster' in self._data.columns:
            return
        self._data['is_subcluster'] = False
        self._data['sub_cluster'] = None
        self._data['subcluster_lat'] = np.nan
        self._data['subcluster_lon'] = np.nan
        self._data['subcluster_road_miles'] = np.nan
        self._data['subcluster_days'] = np.nan
        self._data['overnight_required'] = False
        self._data['subcluster_routing_degraded'] = False
        # FEAT-247 (code review, post-TASK-198): a stable per-pocket
        # identity, independent of the (subcluster_lat, subcluster_lon)
        # medoid. Two genuinely distinct sub-clusters can share an exact
        # medoid by coincidence (e.g. two singleton pockets at the same
        # store's coordinates); grouping cession's atomic units by medoid
        # alone would silently merge them. `min(indices)` is unique by
        # construction: every pocket's member rows are disjoint from
        # every other pocket's, so two different pockets can never share
        # the same minimum row index.
        self._data['subcluster_uid'] = np.nan

    async def _attach_outlier_subclusters(self) -> int:
        """Fold leftover outliers into sub-clusters of an existing market.

        Opt-in (``subcluster_outliers``); a no-op that adds no columns when
        off. Otherwise forms day-budget-feasible pockets
        (``_form_outlier_subclusters``), picks each pocket's receiving
        market by road miles (``_select_subcluster_market``), assigns their
        rows following the file's normal assignment convention (``cid``,
        ``market`` label, ``ghost_id``, cleared ``constraint_reason`` —
        except pockets ``_select_subcluster_market`` flagged
        ``anchored_beyond_cap`` (FEAT-249), which are instead stamped
        ``constraint_reason='subcluster_anchored_beyond_cap'``), and
        stamps the sub-cluster column contract. ``max_cluster_size``
        overflow is annotated later, once the layout has fully settled, by
        ``_annotate_subcluster_overflow`` (called from ``run()`` after FTE
        columns are added — earlier would just be overwritten by the
        per-cluster ``constraint_warning`` write there).

        Called once in ``run()``, right after ``_absorb_remnant_stores()``.

        Returns:
            Number of stores incorporated into a sub-cluster.
        """
        if not self.subcluster_outliers:
            return 0

        self._init_subcluster_columns()

        if self._data.empty:
            return 0
        pool = self._data[self._data[self._cluster_id] == -1]
        if pool.empty:
            return 0

        # FEAT-241 code review fix: refresh centroids right before market
        # selection reads them via _centroid_points(). Several passes
        # since the last _recompute_cluster_centroids() call
        # (_unassign_orphan_stores, _readmit_rejected_as_unassigned,
        # _rescue_unassigned_clusters, _absorb_remnant_stores) can shift
        # membership without recomputing geometry, so without this the
        # haversine prefilter and road-mile decision could run against
        # slightly stale market centroids.
        self._recompute_cluster_centroids()

        subclusters = self._form_outlier_subclusters(pool)
        subclusters = await self._select_subcluster_market(subclusters)

        incorporated = 0
        for subcluster in subclusters:
            cid = subcluster.get('market_cid')
            if cid is None:
                continue  # no market centroid was available to select from
            indices = subcluster['indices']
            medoid_lat, medoid_lon = subcluster['medoid']
            days = subcluster['days']
            road_miles = subcluster.get('road_miles')
            road_minutes = subcluster.get('road_minutes')
            degraded = bool(subcluster.get('routing_degraded', False))
            overnight = self._overnight_required(days, road_minutes)
            affinity_score = subcluster.get('state_affinity_score')
            uid = min(indices)
            # FEAT-249: a pocket _select_subcluster_market anchored past the
            # cap (no candidate within _subcluster_anchor_cap()/headroom,
            # reject_unanchorable_subclusters=False) keeps its annotation
            # here instead of being cleared like a normally-anchored pocket.
            anchored_beyond_cap = bool(subcluster.get('anchored_beyond_cap'))
            if anchored_beyond_cap and 'constraint_reason' not in self._data.columns:
                self._data['constraint_reason'] = None

            for idx in indices:
                self._data.at[idx, self._cluster_id] = cid
                self._data.at[idx, self._cluster_name] = f"Market-{cid}"
                self._data.at[idx, 'ghost_id'] = f"Ghost-{cid}-1"
                if 'constraint_reason' in self._data.columns:
                    self._data.at[idx, 'constraint_reason'] = (
                        'subcluster_anchored_beyond_cap'
                        if anchored_beyond_cap else None
                    )
                self._data.at[idx, 'is_subcluster'] = True
                self._data.at[idx, 'subcluster_lat'] = medoid_lat
                self._data.at[idx, 'subcluster_lon'] = medoid_lon
                self._data.at[idx, 'subcluster_road_miles'] = road_miles
                self._data.at[idx, 'subcluster_days'] = days
                self._data.at[idx, 'overnight_required'] = overnight
                self._data.at[idx, 'subcluster_routing_degraded'] = degraded
                self._data.at[idx, 'state_affinity_score'] = affinity_score
                self._data.at[idx, 'subcluster_uid'] = uid
            incorporated += len(indices)

        self._logger.info(
            "Outlier sub-cluster assignment: %s store(s) incorporated "
            "across %s sub-cluster(s)", incorporated, len(subclusters),
        )
        return incorporated

    def _donor_subcluster_groups(self, donor: Any) -> Dict[Any, List[Any]]:
        """This market's sub-clusters, grouped by stable uid (FEAT-247, Module 5).

        Grouped by ``subcluster_uid`` (``min()`` of a pocket's own member
        row indices, stamped at attachment time — see
        ``_init_subcluster_columns``), NOT by the ``(subcluster_lat,
        subcluster_lon)`` medoid: two genuinely distinct sub-clusters can
        share an exact medoid by coincidence (e.g. two singleton pockets
        at the same store's coordinates), which grouping by medoid alone
        would silently merge into one atomic cession unit.

        Args:
            donor: Market id whose attached sub-clusters to enumerate.

        Returns:
            ``{subcluster_uid: [row indices]}`` — one entry per atomic
            sub-cluster currently attached to ``donor``.
        """
        mask = (
            (self._data[self._cluster_id] == donor)
            & (self._data['is_subcluster'] == True)
        )
        groups: Dict[Any, List[Any]] = {}
        for idx in self._data.index[mask]:
            uid = self._data.at[idx, 'subcluster_uid']
            groups.setdefault(uid, []).append(idx)
        return groups

    def _best_cession_receiver(
        self, donor: Any, indices: List[Any], sizes: Dict[Any, int]
    ) -> Optional[Tuple[Any, float]]:
        """Best-scoring market that can absorb this WHOLE sub-cluster.

        A receiver is feasible only if it can take every one of
        ``indices`` without itself exceeding its ``_effective_ceiling``
        (FEAT-248 G2) — the cap closed by this task never re-opens on the
        receiving end. Same isolation partition as the donor
        (cross-partition receivers make no sense — standalone/isolated
        markets are exempt from this pass entirely). Same-region is
        guaranteed by construction
        (TASK-195: this pass runs inside one region's frame) — ``sizes``
        never contains a cross-region market id, so no redundant check.

        Args:
            donor: Market the sub-cluster is being ceded FROM (excluded).
            indices: Row indices of the sub-cluster's stores.
            sizes: Current total (core + sub-cluster) store count per
                market — the same ledger the caller's donor loop updates
                after every cession ("recompute, don't batch stale").

        Returns:
            ``(receiver_cid, score)``, or ``None`` when no market can
            take the whole sub-cluster.
        """
        subcluster_size = len(indices)
        entity_state = self._dominant_state_of_indices(indices)
        medoid_lat = float(self._data.at[indices[0], 'subcluster_lat'])
        medoid_lon = float(self._data.at[indices[0], 'subcluster_lon'])
        donor_partition = self._cluster_partition.get(donor, False)

        candidates: List[Tuple[Any, float]] = []
        for cid, size in sizes.items():
            if cid == donor or cid in self._standalone_clusters:
                continue
            if self._cluster_partition.get(cid, False) != donor_partition:
                continue
            if size + subcluster_size > self._effective_ceiling(cid):
                continue  # receiver must never exceed its own ceiling
            centroid = self._cluster_centroids.get(cid)
            if centroid is None:
                continue
            distance = self._haversine_miles(
                medoid_lat, medoid_lon,
                centroid['centroid_lat'], centroid['centroid_lon'],
            )
            candidates.append((cid, distance))

        if not candidates:
            return None

        max_distance = max(distance for _, distance in candidates)
        best_cid, best_score, best_distance = None, None, None
        for cid, distance in candidates:
            score = self._state_affinity_score(
                entity_state, cid, distance, max_distance
            )
            if (
                best_score is None
                or score > best_score
                or (score == best_score and distance < best_distance)
                or (
                    score == best_score and distance == best_distance
                    and cid < best_cid
                )
            ):
                best_cid, best_score, best_distance = cid, score, distance

        return best_cid, best_score

    def _apply_cession(self, donor: Any, receiver: Any, indices: List[Any]) -> None:
        """Move a whole sub-cluster's rows from ``donor`` to ``receiver``.

        Follows the file's normal assignment convention (``cid``, market
        label, ``ghost_id`` — same fields ``_attach_outlier_subclusters``
        and ``_merge_markets`` update) and stamps the additive
        ``ceded_from`` column. ``sub_cluster`` labels are NOT touched here
        — ``_label_subclusters()`` (run()'s global tail) recomputes them
        fresh from the post-cession ``cluster_id``, so they refresh to the
        receiver's namespace automatically.

        Args:
            donor: Market the sub-cluster is leaving.
            receiver: Market the sub-cluster is joining.
            indices: Row indices of the sub-cluster's stores.
        """
        for idx in indices:
            self._data.at[idx, self._cluster_id] = receiver
            self._data.at[idx, self._cluster_name] = f"Market-{receiver}"
            self._data.at[idx, 'ghost_id'] = f"Ghost-{receiver}-1"
            self._data.at[idx, 'ceded_from'] = donor
        self._logger.debug(
            "Capacity cession: market %s ceded a %s-store sub-cluster to "
            "market %s.", donor, len(indices), receiver,
        )

    def _cede_oversize_subclusters(self) -> None:
        """Cede whole sub-clusters from over-cap markets (FEAT-247, Module 5).

        Closes the "sub-clusters attach for free" bypass: today
        ``max_cluster_size`` is enforced on core assignment only, and
        ``_annotate_subcluster_overflow`` merely REPORTS a market that
        exceeds it via attached sub-clusters. This pass turns that
        annotator from reporter into actor — a market whose TOTAL (core +
        sub-cluster) store count exceeds its ``_effective_ceiling`` (FEAT-248
        G2) cedes whole sub-clusters until at/under ceiling or every one of
        its sub-clusters has been considered. Cession is atomic: a
        sub-cluster never splits across receivers.

        FEAT-248 TASK-203 (§8 fan-out resolution): each donor's sub-cluster
        groups are processed INDEPENDENTLY, in deterministic
        ``subcluster_uid`` order — a group with no feasible receiver is
        SKIPPED (not a loop-terminating break), so the donor keeps fanning
        out across its remaining pockets instead of dead-ending the moment
        one pocket has no single roomy receiver (the old behavior, and how
        Denver shipped 110 rows: one 40-store pocket with no receiver
        blocked three smaller ones that each had room elsewhere). The
        ``sizes`` ledger updates after every cession so each subsequent
        group's feasibility check sees the current picture, never a stale
        one. Ceding stops as soon as the donor is back at/under its
        ceiling — a donor is never stripped of every pocket just because
        receivers exist for all of them.

        Donor order: most-over-ceiling first, tie-break lower market id.
        A donor left over ceiling after every group has been considered —
        overflow made of core stores alone, or no group found a receiver —
        is flagged by ``_annotate_subcluster_overflow`` right after this
        pass runs.

        A no-op when ``subcluster_outliers`` is off, ``max_cluster_size``
        is unset, or no market carries a sub-cluster at all.
        """
        if (
            not self.subcluster_outliers
            or not self.max_cluster_size
            or self._data.empty
            or 'is_subcluster' not in self._data.columns
        ):
            return
        if not (self._data['is_subcluster'] == True).any():
            return

        self._reset_state_score_cache()

        assigned = self._data[self._data[self._cluster_id] != -1]
        sizes = assigned.groupby(self._cluster_id).size().to_dict()
        donors = sorted(
            (
                cid for cid, size in sizes.items()
                if size > self._effective_ceiling(cid)
                and cid not in self._standalone_clusters
            ),
            key=lambda cid: (-(sizes[cid] - self._effective_ceiling(cid)), cid),
        )
        if not donors:
            return

        cessions = 0
        unresolved_donors = 0

        for donor in donors:
            groups = self._donor_subcluster_groups(donor)
            for uid in sorted(groups, key=str):
                if sizes.get(donor, 0) <= self._effective_ceiling(donor):
                    break  # back at/under ceiling -- stop ceding this donor

                indices = groups[uid]
                receiver_choice = self._best_cession_receiver(
                    donor, indices, sizes
                )
                if receiver_choice is None:
                    continue  # SKIP this pocket, fan out to the next one

                receiver, _score = receiver_choice
                self._apply_cession(donor, receiver, indices)
                sizes[donor] = sizes.get(donor, 0) - len(indices)
                sizes[receiver] = sizes.get(receiver, 0) + len(indices)
                cessions += 1

            if sizes.get(donor, 0) > self._effective_ceiling(donor):
                unresolved_donors += 1

        if cessions:
            self._logger.info(
                "Capacity cession: %s sub-cluster(s) ceded across %s "
                "oversize market(s) (%s market(s) still over ceiling "
                "after cession).",
                cessions, len(donors), unresolved_donors,
            )

    def _annotate_subcluster_overflow(self) -> None:
        """Flag markets that exceed ``max_cluster_size`` via sub-clusters.

        Never rejects — only annotates ``constraint_warning`` with
        ``"subcluster_overflow: <n>/<max>"``. Runs late in
        ``_run_region_pipeline()``, after ``_add_fte_columns_to_result()``
        writes the per-cluster ``constraint_warning`` column, so this
        row-level annotation on sub-cluster rows is not immediately
        clobbered by that per-cluster write.

        FEAT-248 G6: also called a second time from ``_finalize_delivery``,
        again right after its own ``_add_fte_columns_to_result()`` call —
        global ``_reconcile_global_max_markets`` (merges/splits) runs
        between the per-region call and delivery, so the per-region
        annotation can be stale for markets it touched (audit item 1d:
        ``subcluster_overflow: 141/52`` inherited from a pre-split parent).
        The second call re-derives the annotation from final membership;
        it is idempotent (re-groups and re-checks sizes from scratch).
        """
        if not self.subcluster_outliers or self._data.empty:
            return
        if 'is_subcluster' not in self._data.columns:
            return

        # `== True` (not `.astype(bool)`): a comparison treats any NaN
        # gap as False, whereas `.astype(bool)` converts NaN to True —
        # currently a non-issue given run()'s ordering always inits this
        # column with no gaps before either of these methods runs, but
        # matching the defensive pattern used in SchedulingVisits.py
        # (where an equivalent gap once caused exactly that bug) keeps
        # this safe even if that ordering invariant ever changes.
        subcluster_mask = self._data['is_subcluster'] == True
        if not subcluster_mask.any():
            return
        if 'constraint_warning' not in self._data.columns:
            self._data['constraint_warning'] = ''

        sizes = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size()

        for cid in self._data.loc[subcluster_mask, self._cluster_id].unique():
            size = int(sizes.get(cid, 0))
            if size > self.max_cluster_size:
                warning = f"subcluster_overflow: {size}/{self.max_cluster_size}"
                rows = subcluster_mask & (self._data[self._cluster_id] == cid)
                self._data.loc[rows, 'constraint_warning'] = warning

    def _label_subclusters(self) -> None:
        """Stamp ``sub_cluster = "<market>-SC<n>"`` labels.

        Runs after ``_renumber_markets_from_one()`` so labels use the
        delivered, 1-based market ids/names. ``n`` is 1-based, sequential
        per market, one value per distinct medoid (i.e. per sub-cluster).
        """
        if not self.subcluster_outliers or self._data.empty:
            return
        if 'is_subcluster' not in self._data.columns:
            return

        # `== True`, not `.astype(bool)` — see the note in
        # _annotate_subcluster_overflow above.
        subcluster_rows = self._data[self._data['is_subcluster'] == True]
        if subcluster_rows.empty:
            return

        for cid, rows in subcluster_rows.groupby(self._cluster_id):
            market_name = self._data.at[rows.index[0], self._cluster_name]
            seen_medoids: Dict[Tuple[float, float], int] = {}
            n = 0
            for idx in rows.index:
                medoid = (
                    self._data.at[idx, 'subcluster_lat'],
                    self._data.at[idx, 'subcluster_lon'],
                )
                if medoid not in seen_medoids:
                    n += 1
                    seen_medoids[medoid] = n
                self._data.at[idx, 'sub_cluster'] = (
                    f"{market_name}-SC{seen_medoids[medoid]}"
                )

    def _market_employees(self, cid: Any) -> int:
        """Staff assigned to a market (forced value wins over the FTE optimum)."""
        if self._forced_num_ghosts and self.num_ghosts_per_cluster is not None:
            value = self.num_ghosts_per_cluster
            if isinstance(value, (list, tuple)):
                value = value[0]
            return max(1, int(value))

        return max(
            1, int(self._cluster_fte_info.get(cid, {}).get('num_employees', 1))
        )

    def _market_daily_hours(self, cid: Any, cluster_df: pd.DataFrame) -> float:
        """Hours per working day the market demands from each employee."""
        if self.fte_calculator is None or cluster_df.empty:
            return 0.0

        hours = self.fte_calculator.calculate_cluster_hours(
            num_stores=len(cluster_df),
            avg_distance_between_stores=self._calculate_cluster_avg_distance(
                cluster_df
            ),
            setup_time_per_store=self.setup_time_per_store,
            visit_frequencies=self._get_cluster_visit_frequencies(cluster_df),
            in_store_hours=self._get_cluster_in_store_hours(cluster_df),
            num_employees=self._market_employees(cid),
        )
        return float(hours['daily_hours'])

    def _market_justifies_staff(self, cid: Any) -> bool:
        """True when the market's demand reaches its staffing floor (FEAT-240).

        A market whose work does not add up to ``num_ghosts_range[0]`` people
        is paying a whole salary for a fraction of a job, which makes it the
        first thing budget-mode consolidation should absorb.

        This is an ORDERING signal only (sort key 1 in
        ``_consolidate_markets_for_headcount``, TASK-164) — it never
        dissolves, rejects or reshapes anything, and it never touches
        ``min_cluster_size``, which keeps its store-count meaning everywhere
        else in this component (spec §7).

        Args:
            cid: Market to evaluate.

        Returns:
            True when the market's current headcount already meets or
            exceeds its staffing floor.
        """
        if self.num_ghosts_range is None:
            return True
        min_ghosts = self.num_ghosts_range[0]
        return self._market_employees(cid) >= min_ghosts

    def _union_frame_geometry(
        self, a: Any, union: pd.DataFrame
    ) -> Tuple[float, float, float]:
        """Real post-merge geometry of a candidate merge (FEAT-240).

        Computes the centre the merged market would ACTUALLY be delivered
        with, via ``_cluster_center`` — exactly what ``_merge_markets``
        computes once the merge is real, not a plain mean. Under the
        default ``market_center='base'``, ``_cluster_center`` calls
        ``_market_base``, which recomputes a 1-median/minimax REAL STORE
        over every member; it does **not** consult ``_anchored_centroids``
        for an ordinary (non-standalone) market, so validating this
        condition against a plain mean would silently pass merges whose
        real, delivered centre sits somewhere else entirely. Only under
        ``market_center='anchored'`` does this resolve to A's own
        dense-core anchor, unaffected by B's stores.

        Args:
            a: Higher-demand market of the pair — the survivor/receiver
                this centre is computed for.
            union: Rows of both markets being evaluated for a merge, with
                their ORIGINAL (pre-merge) cluster ids.

        Returns:
            ``(centroid_lat, centroid_lon, max_store_distance)`` — the real
            centre ``a`` would be delivered with after absorbing ``b``, and
            the farthest union store's haversine distance to it.

        Note (FEAT-241 code review fix): ``is_subcluster`` rows are
        excluded before either computation. A sub-cluster is exempt from
        distance-based market rules — it carries its own centerpoint and
        is never visited via the normal per-store route this geometry
        models — so including it would skew the simulated real centre
        and inflate ``max_store_distance`` for a market that just
        received one.
        """
        geometry_union = union
        if 'is_subcluster' in union.columns:
            core_only = union[~union['is_subcluster']]
            if not core_only.empty:
                geometry_union = core_only

        # _cluster_center / _market_base filter their `members` frame by
        # `df[self._cluster_id] == cid`, so a relabeled copy — not
        # `geometry_union` itself, whose rows still carry `a`'s and `b`'s
        # ORIGINAL ids — is what makes this the same computation
        # _merge_markets performs post-merge, without mutating self._data
        # before the merge is real.
        relabeled = geometry_union.copy()
        relabeled[self._cluster_id] = a
        centre = self._cluster_center(a, relabeled)
        centroid_lat = centre['centroid_lat']
        centroid_lon = centre['centroid_lon']
        distances = self._haversine_miles(
            geometry_union['latitude'].to_numpy(),
            geometry_union['longitude'].to_numpy(),
            centroid_lat,
            centroid_lon,
        )
        max_distance = float(np.max(distances)) if len(geometry_union) else 0.0
        return centroid_lat, centroid_lon, max_distance

    def _merge_saving(self, a: Any, b: Any, reach: float) -> Optional[int]:
        """Headcount saved by merging ``b`` into ``a``, or ``None`` when infeasible.

        Evaluates the seven-condition feasibility predicate (spec §2),
        cheapest checks first — ``optimize_num_employees`` on the union
        frame, the expensive one, only runs once every geometry/policy
        condition already passed.

        Args:
            a: Higher-demand market of the candidate pair (absorbs ``b``).
            b: Market that would dissolve into ``a``.
            reach: Effective ``consolidation_reach`` for this round.

        Returns:
            Positive headcount saved (``emp(a) + emp(b) - emp(a ∪ b)``)
            when every condition holds, else ``None``.
        """
        # 1. Neither side may be a frozen standalone market.
        if a in self._standalone_clusters or b in self._standalone_clusters:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — standalone market", a, b
            )
            return None
        # 2. Same isolation partition.
        if self._cluster_partition.get(a, False) != self._cluster_partition.get(
            b, False
        ):
            self._logger.debug(
                "_merge_saving(%s, %s): refused — different isolation partitions",
                a, b,
            )
            return None
        # 3. Centroid-to-centroid distance within reach.
        centroid_a = self._cluster_centroids.get(a)
        centroid_b = self._cluster_centroids.get(b)
        if centroid_a is None or centroid_b is None:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — missing centroid", a, b
            )
            return None
        centroid_distance = self._haversine_miles(
            centroid_a['centroid_lat'], centroid_a['centroid_lon'],
            centroid_b['centroid_lat'], centroid_b['centroid_lon'],
        )
        if centroid_distance > reach:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — %.1f mi centroid distance > "
                "reach %.1f mi", a, b, centroid_distance, reach,
            )
            return None

        union = self._data[self._data[self._cluster_id].isin([a, b])]
        if union.empty:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — empty union frame", a, b
            )
            return None

        # FEAT-241 code review fix: sub-cluster rows are exempt from
        # distance-based market rules (they carry their own centerpoint
        # and are never visited via the normal per-store route this
        # geometry models — a separate block schedules them). Including
        # them in the GEOMETRY probe below would inflate
        # union_avg_distance/max_store_distance and spuriously fail
        # condition 7 for any market that just received one, defeating
        # the reason _attach_outlier_subclusters() runs before this
        # consolidation pass. Headcount (emp_a/emp_b, num_stores below,
        # and in-store hours/visit frequencies) still counts them —
        # only the geometry excludes them.
        geometry_union = union
        if 'is_subcluster' in union.columns:
            core_only = union[~union['is_subcluster']]
            if not core_only.empty:
                geometry_union = core_only

        emp_a = self._market_employees(a)
        emp_b = self._market_employees(b)
        union_avg_distance = self._calculate_cluster_avg_distance(geometry_union)
        union_visit_frequencies = self._get_cluster_visit_frequencies(union)
        union_in_store_hours = self._get_cluster_in_store_hours(union)
        # _best_merge_candidate needs this same value for sort key 3 (the
        # resulting market's avg_distance); cache it so it does not pay
        # the O(k²) pairwise haversine over the same union a second time.
        self._merge_avg_distance_cache[frozenset({a, b})] = union_avg_distance

        result = self.fte_calculator.optimize_num_employees(
            num_stores=len(union),
            avg_distance=union_avg_distance,
            max_stores_per_employee=self.max_stores_per_day,
            visit_frequencies=union_visit_frequencies,
            in_store_hours=union_in_store_hours,
        )
        emp_union = int(result['num_employees'])

        # 4. Strict saving: no reason to pay the geometry without one.
        if not emp_union < emp_a + emp_b:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — no saving (%s -> %s)",
                a, b, emp_a + emp_b, emp_union,
            )
            return None
        # 5. Per-market employee ceiling.
        if emp_union > self.num_ghosts_range[1]:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — %s employees exceeds "
                "ceiling %s", a, b, emp_union, self.num_ghosts_range[1],
            )
            return None

        # 6. Hours/day per employee of the union, using the MERGED headcount
        # (not _market_daily_hours(a, union), which would resolve staff via
        # _market_employees(a) — a's CURRENT staff, not the merged figure).
        hours = self.fte_calculator.calculate_cluster_hours(
            num_stores=len(union),
            avg_distance_between_stores=union_avg_distance,
            setup_time_per_store=self.setup_time_per_store,
            visit_frequencies=union_visit_frequencies,
            in_store_hours=union_in_store_hours,
            num_employees=emp_union,
        )
        if float(hours['daily_hours']) > self.day_hours:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — %.2fh/day > day_hours %.2f",
                a, b, hours['daily_hours'], self.day_hours,
            )
            return None

        # 7. Max store→centre distance of the union, measured against the
        # REAL centre `a` would be delivered with after absorbing `b` (see
        # _union_frame_geometry) — not a plain mean a merge could pass
        # while the actually-delivered layout still violates the radius.
        # _union_frame_geometry excludes is_subcluster rows internally
        # (FEAT-241 code review fix), so the raw `union` is passed here.
        _, _, max_store_distance = self._union_frame_geometry(a, union)
        if max_store_distance > self.max_cluster_distance:
            self._logger.debug(
                "_merge_saving(%s, %s): refused — %.1f mi max store distance "
                "> max_cluster_distance %.1f mi",
                a, b, max_store_distance, self.max_cluster_distance,
            )
            return None

        return emp_a + emp_b - emp_union

    def _merge_markets(self, a: Any, b: Any) -> int:
        """Move every store of ``b`` into ``a`` and retire ``b`` (FEAT-240).

        ``a`` keeps its dense-core anchor: the merged market has two nuclei
        by design, and the plain member mean of two nuclei can fall between
        the metros the market actually serves. ``b``'s entry is deleted from
        every per-market dict, or stale state would be read later as a live
        market.

        Args:
            a: Higher-demand market of the pair; survives the merge.
            b: Market being absorbed; ceases to exist.

        Returns:
            How many stores changed market (``0`` when ``b`` is already
            empty).
        """
        assert b not in self._standalone_clusters, (
            f"_merge_markets: {b!r} is a frozen standalone market"
        )
        assert a != b, "_merge_markets: a and b must be different markets"

        members_b = self._data.index[self._data[self._cluster_id] == b]
        moved = len(members_b)

        if moved:
            self._data.loc[members_b, self._cluster_id] = a
            # Mirror the assignment convention every other reassignment pass
            # in this component follows (e.g. _absorb_remnant_stores): the
            # market label and ghost_id must track cluster_id, or
            # _renumber_markets_from_one's ghost_id remap silently leaves an
            # orphaned "Ghost-<b>-*" reference once b no longer exists.
            self._data.loc[members_b, self._cluster_name] = f"Market-{a}"
            self._data.loc[members_b, 'ghost_id'] = f"Ghost-{a}-1"
            if 'constraint_reason' in self._data.columns:
                self._data.loc[members_b, 'constraint_reason'] = None

        # b's entry must not survive in any per-market dict.
        self._cluster_centroids.pop(b, None)
        self._market_capacity.pop(b, None)
        self._anchored_centroids.pop(b, None)
        self._cluster_partition.pop(b, None)
        self._cluster_fte_info.pop(b, None)

        # a keeps its own anchor untouched; its centroid is recomputed over
        # the merged membership (_cluster_center already consults
        # _anchored_centroids). Not a full _recompute_cluster_centroids()
        # sweep: the caller (_consolidate_markets_for_headcount) owns that.
        # FEAT-241 code review fix: exclude sub-cluster rows here too —
        # otherwise this transient refresh (before that full sweep runs)
        # would pollute a's centroid with its annex's position for the
        # rest of the same consolidation round.
        members_a = self._data[self._data[self._cluster_id] == a]
        centroid_members_a = members_a
        if 'is_subcluster' in members_a.columns:
            core_only_a = members_a[~members_a['is_subcluster']]
            if not core_only_a.empty:
                centroid_members_a = core_only_a
        if not members_a.empty:
            self._cluster_centroids[a] = self._cluster_center(a, centroid_members_a)

        self._logger.info(
            "Merged market %s into %s: %s store(s) moved", b, a, moved
        )
        return moved

    def _live_market_ids(self) -> List[Any]:
        """Sorted, deterministic list of markets currently holding stores.

        Derived from ``self._data`` rather than ``_cluster_centroids``: the
        latter may still hold a just-merged, now-retired id until
        ``_merge_markets`` finishes cleaning it up. ``-1`` (Outlier) is
        excluded — it is not a market.
        """
        if self._data.empty:
            return []
        return sorted(
            cid for cid in self._data[self._cluster_id].unique() if cid != -1
        )

    def _region_merge_feasible(
        self,
        a: Any,
        b: Any,
        reach: float,
        member_index: Dict[Any, pd.Index],
    ) -> Optional[float]:
        """Feasibility of merging ``b`` into ``a`` for max_markets reconciliation.

        Mirrors ``_merge_saving``'s geometry/policy guards (spec §2 "reusing
        the ``_merge_saving``/``_merge_markets`` guards"): neither market is
        a frozen standalone market, both share the same isolation partition,
        and centroid-to-centroid distance is within ``reach``. Unlike
        ``_merge_saving`` (FEAT-240, headcount-driven — its condition 5
        hard-requires ``self.num_ghosts_range``, unset for the Verizon
        config this feature targets), feasibility here is purely geometric:
        the goal is fitting under ``max_markets``, not minimizing headcount.
        Deliberately does NOT gate on ``max_cluster_size`` — ``max_markets``
        is a HARD ceiling that FORCES the layout (spec §2), the same way
        the pre-FEAT-247 pipeline already lets ``max_markets`` push stores
        past ``max_cluster_size`` via overflow force-assignment.

        Args:
            a: Market that would survive (receives ``b``'s stores).
            b: Market that would be absorbed.
            reach: Maximum centroid-to-centroid distance for this pair.
            member_index: Market id -> row-index cache (maintained by the
                caller across the whole reconciliation loop) — avoids
                rescanning all of ``self._data`` for membership on every
                candidate pair evaluated.

        Returns:
            The post-merge max store distance (lower is a better/tighter
            merge) when every condition holds, else ``None``.
        """
        if a in self._standalone_clusters or b in self._standalone_clusters:
            return None
        if self._cluster_partition.get(a, False) != self._cluster_partition.get(
            b, False
        ):
            return None

        centroid_a = self._cluster_centroids.get(a)
        centroid_b = self._cluster_centroids.get(b)
        if centroid_a is None or centroid_b is None:
            return None
        centroid_distance = self._haversine_miles(
            centroid_a['centroid_lat'], centroid_a['centroid_lon'],
            centroid_b['centroid_lat'], centroid_b['centroid_lon'],
        )
        if centroid_distance > reach:
            return None

        union_index = member_index.get(a, pd.Index([])).union(
            member_index.get(b, pd.Index([]))
        )
        if union_index.empty:
            return None
        union = self._data.loc[union_index]

        _, _, max_store_distance = self._union_frame_geometry(a, union)
        if max_store_distance > self.max_cluster_distance:
            return None

        return max_store_distance

    def _best_region_merge_candidate(
        self,
        live: List[Any],
        region_of: Dict[Any, Any],
        reach: float,
        sizes: Dict[Any, int],
        member_index: Dict[Any, pd.Index],
    ) -> Optional[Tuple[Any, Any]]:
        """Tightest feasible same-region market pair to merge, or ``None``.

        Merges never cross regions: candidates are grouped by
        ``region_column`` value FIRST, so pairs from different regions are
        never even constructed — O(sum of each region's k²) instead of
        O(M²) over every live market regardless of region. The larger
        market (by store count) survives and absorbs the smaller —
        ``_merge_markets``'s own convention. Deterministic: ties break on
        the lower post-merge max-store-distance, then on the sorted
        iteration order within each region group.

        Args:
            live: Sorted, deterministic list of currently-live market ids.
            region_of: Market id -> region value (empty when unset).
            reach: Maximum centroid-to-centroid distance to consider.
            sizes: Current store count per market — maintained by the
                caller across the loop, not recomputed here.
            member_index: Market id -> row-index cache, see
                ``_region_merge_feasible``.

        Returns:
            ``(a, b)`` — ``a`` survives, ``b`` is absorbed — or ``None``
            when no feasible same-region pair remains.
        """
        groups: Dict[Any, List[Any]] = {}
        for cid in live:
            groups.setdefault(region_of.get(cid), []).append(cid)

        best: Optional[Tuple[Any, Any]] = None
        best_score: Optional[float] = None
        for group_ids in groups.values():
            if len(group_ids) < 2:
                continue
            for x, y in itertools.combinations(group_ids, 2):
                size_x = sizes.get(x, 0)
                size_y = sizes.get(y, 0)
                a, b = (x, y) if size_x >= size_y else (y, x)
                score = self._region_merge_feasible(a, b, reach, member_index)
                if score is None:
                    continue
                if best_score is None or score < best_score:
                    best, best_score = (a, b), score

        return best

    def _reconcile_global_max_markets(self) -> None:
        """Enforce ``max_markets`` as an exact target after all regions run.

        ``max_markets`` is both a hard ceiling AND a capacity to be consumed
        at 100%: if the emergent count is over it, merge same-region pairs
        down; if under, split the largest markets in the most starved
        regions up — until the target is met or no feasible action remains.

        **Merge-down** (emergent > target): identical to the pre-existing
        logic — merge the tightest feasible same-region pairs, never across
        regions, until count ≤ target.

        **Split-up** (emergent < target): new capacity-distribution pass.
        Each round identifies the region with the highest stores-per-market
        ratio, picks the largest splittable (≥ 2 stores) non-standalone
        market in that region, and splits it via KMeans
        (``_split_market``). Standalone markets are never split. The loop
        stops when the count reaches the target or no market can be split.

        Performance: ``live``, ``sizes`` and each market's member-row-index
        are computed ONCE up front and maintained incrementally — not
        rescanned from ``self._data`` on every loop iteration.
        """
        if self.max_markets is None or self._data.empty:
            return

        live_set = set(self._live_market_ids())

        region_of: Dict[Any, Any] = {}
        if self.region_column and self.region_column in self._data.columns:
            for cid in live_set:
                values = self._data.loc[
                    self._data[self._cluster_id] == cid, self.region_column
                ]
                if not values.empty:
                    region_of[cid] = values.iloc[0]

        assigned = self._data[self._data[self._cluster_id] != -1]
        sizes: Dict[Any, int] = assigned.groupby(self._cluster_id).size().to_dict()
        member_index: Dict[Any, pd.Index] = dict(
            assigned.groupby(self._cluster_id).groups
        )

        # --- Phase 1: merge-down (emergent > target) ----------------------
        reach = self.max_cluster_distance
        merges_applied = 0
        while len(live_set) > self.max_markets:
            candidate = self._best_region_merge_candidate(
                sorted(live_set), region_of, reach, sizes, member_index,
            )
            if candidate is None:
                self._logger.warning(
                    "max_markets=%s reconciliation stopped at %s markets: "
                    "no feasible same-region merge remains.",
                    self.max_markets, len(live_set),
                )
                break
            a, b = candidate
            self._merge_markets(a, b)
            merges_applied += 1

            # Maintain live_set/sizes/member_index incrementally: a merge
            # only ever changes a (grows) and retires b -- no other market
            # is affected, so there is no need to rescan self._data.
            sizes[a] = sizes.get(a, 0) + sizes.pop(b, 0)
            member_index[a] = member_index.get(a, pd.Index([])).union(
                member_index.pop(b, pd.Index([]))
            )
            live_set.discard(b)
            region_of.pop(b, None)

        if merges_applied:
            self._recompute_cluster_centroids()
            self._logger.info(
                "max_markets reconciliation: %s in-region merge(s) applied, "
                "%s market(s) remain.",
                merges_applied, len(live_set),
            )

        # --- Phase 2: split-up (emergent < target) ------------------------
        splits_applied = 0
        standalone_set = set(self._standalone_clusters or {})
        # FEAT-248 TASK-204: both halves of a split must EACH be >=
        # min_cluster_size (not min//2, which used to let a 25-store
        # minimum "pass" a 13+12 split -- both halves below the configured
        # minimum). With quotas (Module 1) driving formation to the
        # target up front, this phase is a backstop only, so making many
        # splits infeasible here is intended, not a regression: an
        # infeasible split is logged as a count shortfall, never forced.
        # Never below 15 either — a market that small will never justify
        # a dedicated employee regardless of min_cluster_size.
        split_half_floor = max(self.min_cluster_size or 25, 15)

        # Markets that produced a runt half (below the floor) on a
        # previous attempt are blacklisted for the rest of the pass so
        # we don't retry the same hopeless split in a loop.
        unsplittable: set = set()

        while len(live_set) < self.max_markets:
            # Per-region demand: stores-per-market ratio — highest wins the
            # next slot. Regions are identified from region_of; when
            # region_column is unset all markets share a single None region.
            region_load: Dict[Any, float] = {}
            region_markets: Dict[Any, List[Any]] = {}
            for cid in live_set:
                rgn = region_of.get(cid)
                region_load[rgn] = region_load.get(rgn, 0) + sizes.get(cid, 0)
                region_markets.setdefault(rgn, []).append(cid)

            # Stores-per-market ratio — split in the most overloaded region
            region_ratio = {
                rgn: region_load[rgn] / len(region_markets[rgn])
                for rgn in region_load
            }
            # Sort by ratio desc, then by region name for determinism
            ranked_regions = sorted(
                region_ratio, key=lambda r: (-region_ratio[r], str(r))
            )

            split_done = False
            for rgn in ranked_regions:
                # Find the largest splittable market in this region.
                # Both halves must be able to meet split_half_floor, so the
                # market needs at least 2 × that many stores.
                min_splittable = 2 * split_half_floor
                candidates = [
                    cid for cid in region_markets[rgn]
                    if (
                        sizes.get(cid, 0) >= min_splittable
                        and cid not in standalone_set
                        and cid not in unsplittable
                    )
                ]
                if not candidates:
                    continue

                # Pick the largest; tie-break on cid for determinism
                target_cid = max(candidates, key=lambda c: (sizes.get(c, 0), -c))

                new_cid = self._split_market(
                    self._data, target_cid,
                    reason=(
                        f"reach max_markets={self.max_markets} "
                        f"(region {rgn!r} has {region_ratio[rgn]:.0f} "
                        f"stores/market)"
                    ),
                )
                if new_cid is None:
                    unsplittable.add(target_cid)
                    continue

                # Check that BOTH halves meet the floor.  KMeans can
                # produce lopsided splits (e.g. 48+7) when a market has
                # remote sub-cluster stores.  If either half is a runt,
                # undo the split, blacklist the market, and try the next.
                new_count = int(
                    (self._data[self._cluster_id] == new_cid).sum()
                )
                old_remaining = sizes.get(target_cid, 0) - new_count

                if new_count < split_half_floor or old_remaining < split_half_floor:
                    # Undo: move the split stores back
                    self._data.loc[
                        self._data[self._cluster_id] == new_cid,
                        self._cluster_id,
                    ] = target_cid
                    self._cluster_partition.pop(new_cid, None)
                    unsplittable.add(target_cid)
                    self._logger.debug(
                        "Split-up reverted for cluster %s: halves %s+%s "
                        "below floor %s — trying next candidate.",
                        target_cid, old_remaining, new_count,
                        split_half_floor,
                    )
                    continue

                # Maintain bookkeeping incrementally
                sizes[target_cid] = old_remaining
                sizes[new_cid] = new_count
                live_set.add(new_cid)
                region_of[new_cid] = rgn
                splits_applied += 1
                split_done = True
                break  # re-evaluate ratios after each split

            if not split_done:
                self._logger.warning(
                    "max_markets=%s split-up stopped at %s markets: "
                    "no splittable market remains in any region.",
                    self.max_markets, len(live_set),
                )
                break

        if splits_applied:
            self._recompute_cluster_centroids()
            self._logger.info(
                "max_markets split-up: %s split(s) applied, "
                "%s market(s) now formed.",
                splits_applied, len(live_set),
            )

    def _total_headcount(self) -> int:
        """Sum of ``_market_employees()`` over every live market (FEAT-240)."""
        return sum(self._market_employees(cid) for cid in self._live_market_ids())

    def _demand_ordered_pair(self, x: Any, y: Any) -> Tuple[Any, Any]:
        """``(a, b)`` with ``a`` the higher-demand market of the pair.

        Spec §2: "A is the higher-demand market of the pair" — A survives
        and absorbs B. Ties break on the smaller id for a stable, repeatable
        choice (this component's precedent: an unseeded RNG once shipped a
        non-reproducible layout).
        """
        emp_x = self._market_employees(x)
        emp_y = self._market_employees(y)
        if emp_x > emp_y:
            return x, y
        if emp_y > emp_x:
            return y, x
        return min(x, y), max(x, y)

    def _best_merge_candidate(
        self, reach: float
    ) -> Optional[Tuple[Any, Any, int]]:
        """Highest-priority feasible merge pair at ``reach`` (FEAT-240).

        Candidates are every pair of live markets passing ``_merge_saving``,
        ranked by the four-key ordering (spec §2), in this order:

        1. the pair contains a market failing ``_market_justifies_staff`` (desc)
        2. headcount saving (desc)
        3. ``avg_distance`` of the resulting market (asc)
        4. ``min(cid_a, cid_b)`` (asc, deterministic tie-break)

        Args:
            reach: Effective ``consolidation_reach`` for this round.

        Returns:
            ``(a, b, saving)`` for the best candidate, or ``None`` when no
            pair is feasible.
        """
        best: Optional[Tuple[Any, Any, int]] = None
        best_key: Optional[Tuple[bool, int, float, float]] = None
        # Fresh per scan: pairs come and go as markets merge across rounds.
        self._merge_avg_distance_cache = {}

        for x, y in itertools.combinations(self._live_market_ids(), 2):
            a, b = self._demand_ordered_pair(x, y)
            saving = self._merge_saving(a, b, reach)
            if saving is None:
                continue

            # _merge_saving caches this union's avg_distance while pricing
            # the merge; reuse it instead of re-running the O(k²) pairwise
            # haversine over the same union a second time. Falls back to a
            # direct (re-)computation on a cache miss — e.g. _merge_saving
            # was bypassed by a test — rather than crashing on it.
            avg_distance = self._merge_avg_distance_cache.get(frozenset({a, b}))
            if avg_distance is None:
                union = self._data[self._data[self._cluster_id].isin([a, b])]
                # FEAT-241 code review fix: exclude is_subcluster rows,
                # matching what _merge_saving's cached value already does
                # — a cache miss must not fall back to a differently
                # (unfiltered) computed avg_distance.
                geometry_union = union
                if 'is_subcluster' in union.columns:
                    core_only = union[~union['is_subcluster']]
                    if not core_only.empty:
                        geometry_union = core_only
                avg_distance = self._calculate_cluster_avg_distance(geometry_union)
            thin_pair = (
                not self._market_justifies_staff(a)
                or not self._market_justifies_staff(b)
            )
            # All four keys maximized: asc criteria (3, 4) are negated so a
            # single tuple comparison picks the right winner.
            key = (thin_pair, saving, -avg_distance, -float(min(a, b)))

            if best_key is None or key > best_key:
                best_key = key
                best = (a, b, saving)

        return best

    def _count_feasible_pairs(self, reach: float) -> int:
        """How many live market pairs still pass ``_merge_saving`` at ``reach``.

        Used only to size the warning logged when
        ``max_consolidation_rounds`` is hit — never to decide anything.
        """
        count = 0
        for x, y in itertools.combinations(self._live_market_ids(), 2):
            a, b = self._demand_ordered_pair(x, y)
            if self._merge_saving(a, b, reach) is not None:
                count += 1
        return count

    def _consolidation_rounds(self, reach: float) -> int:
        """Greedy consolidation rounds at a fixed reach (FEAT-240).

        Repeatedly applies the best feasible merge (see
        ``_best_merge_candidate``) until none remains or
        ``max_consolidation_rounds`` is reached, whichever comes first.
        Each merge is irreversible (a market only ever disappears, never
        reappears), so — unlike ``_balance_market_sizes`` — this loop cannot
        cycle; the round cap exists purely to bound the worst case of a
        large market count.

        Args:
            reach: Effective ``consolidation_reach`` for this call.

        Returns:
            Number of merges applied.
        """
        merges = 0
        for round_num in range(1, self.max_consolidation_rounds + 1):
            best = self._best_merge_candidate(reach)
            if best is None:
                break
            a, b, saving = best
            moved = self._merge_markets(a, b)
            merges += 1
            self._logger.info(
                "Consolidation round %s (reach=%.1f mi): merged market %s "
                "into %s — saved %s employee(s), %s store(s) moved.",
                round_num, reach, b, a, saving, moved,
            )
            # Refresh what the merge changed: a's FTE info first (capacity
            # reads it), then the market_capacity sweep — the reverse order
            # would size a's capacity off its stale, pre-merge headcount.
            members_a = self._data[self._data[self._cluster_id] == a]
            if not members_a.empty:
                # Return value intentionally discarded: called only for its
                # side effect of refreshing self._cluster_fte_info[a].
                self._get_num_ghosts_for_cluster(a, members_a)
            self._recompute_market_capacity()
        else:
            # The loop ran every round up to the cap without a natural
            # break: the cap itself stopped the pass, not exhaustion of
            # candidates (RC-2 precedent: _balance_market_sizes once ran
            # 122 rounds before its fix). A hit cap is a cycle suspicion,
            # not a run failure — keep the layout reached.
            remaining = self._count_feasible_pairs(reach)
            if remaining:
                self._logger.warning(
                    "Consolidation stopped at max_consolidation_rounds=%s "
                    "with %s viable pair(s) still available; keeping the "
                    "layout reached.", self.max_consolidation_rounds, remaining,
                )
        return merges

    def _consolidate_markets_for_headcount(self) -> int:
        """Greedily merge markets to minimize total headcount (FEAT-240).

        A merge is applied only while it strictly recovers ``ceil()`` waste
        in the staffing figure and breaks no physical constraint. See the
        spec for the seven-condition predicate, which lives in
        ``_merge_saving``. When the first convergence still leaves total
        headcount above ``max_employees``, a second round runs with
        ``consolidation_reach`` widened by ``consolidation_relax_factor``
        (accepting worse geometry, never a relaxed physical constraint). If
        that still is not enough, raises with the exact deficit.

        Returns:
            How many merges were applied across both rounds.

        Raises:
            ComponentError: Full coverage needs more employees than
                ``max_employees`` allows, even after relaxation. The
                component is left EXACTLY as it was before this call —
                every merge applied by either round is rolled back first,
                so a caller never has to discard the instance.
        """
        if not self._budget_mode:
            return 0

        # Snapshot everything a merge can touch. Unlike every other
        # `raise` in this file, this one can fire AFTER real mutations
        # already happened: the relaxed-round flow needs to actually try
        # merges before it can know they were not enough. Restored
        # verbatim below if the budget still is not met.
        data_snapshot = self._data.copy()
        centroids_snapshot = {
            cid: dict(info) for cid, info in self._cluster_centroids.items()
        }
        capacity_snapshot = dict(self._market_capacity)
        anchored_snapshot = dict(self._anchored_centroids)
        partition_snapshot = dict(self._cluster_partition)
        fte_info_snapshot = {
            cid: dict(info) for cid, info in self._cluster_fte_info.items()
        }
        budget_counters_snapshot = (
            self._budget_markets_before,
            self._budget_markets_after,
            self._budget_merges_applied,
            self._budget_headcount_saved,
            self._budget_relaxed_round_used,
        )

        self._budget_markets_before = len(self._live_market_ids())
        headcount_before = self._total_headcount()
        self._budget_relaxed_round_used = False

        reach = self.consolidation_reach or self._move_distance_guard
        merges = self._consolidation_rounds(reach)

        total = self._total_headcount()
        if total > self.max_employees:
            relaxed_reach = reach * self.consolidation_relax_factor
            self._logger.warning(
                "Employee budget not met at reach=%.1f mi (%s employees > "
                "cap %s); retrying at %.1f mi (worse geometry accepted).",
                reach, total, self.max_employees, relaxed_reach,
            )
            merges += self._consolidation_rounds(relaxed_reach)
            self._budget_relaxed_round_used = True
            total = self._total_headcount()

        if total > self.max_employees:
            deficit = total - self.max_employees
            # Roll back every merge either round applied: raising here
            # must never leave the component half-merged for a caller
            # that might reuse this instance (e.g. a retry with a
            # different max_employees).
            self._data = data_snapshot
            self._cluster_centroids = centroids_snapshot
            self._market_capacity = capacity_snapshot
            self._anchored_centroids = anchored_snapshot
            self._cluster_partition = partition_snapshot
            self._cluster_fte_info = fte_info_snapshot
            (
                self._budget_markets_before,
                self._budget_markets_after,
                self._budget_merges_applied,
                self._budget_headcount_saved,
                self._budget_relaxed_round_used,
            ) = budget_counters_snapshot
            raise ComponentError(
                f"Full coverage needs {total} employees but max_employees "
                f"is {self.max_employees}: short by {deficit}."
            )

        # Counters for _log_employee_budget_summary (TASK-166). Set only on
        # a successful return: the ComponentError path above aborts run()
        # before the summary is ever logged.
        self._budget_merges_applied = merges
        self._budget_markets_after = len(self._live_market_ids())
        self._budget_headcount_saved = headcount_before - total

        return merges

    def _enforce_daily_hours_budget(self) -> int:
        """Keep every market inside ``day_hours`` per working day.

        Eight hours is a physical ceiling, not a preference: nobody can be
        made to work a longer day. A market whose schedule does not fit sheds
        its costliest store — the one farthest from the centroid, which is
        the one paying the most travel — to the nearest market that can
        service it without breaking its own day. When no market can, the
        store is left unassigned, which is the honest answer: it needs
        coverage nobody currently has.

        Returns:
            How many stores were moved out of over-budget markets.
        """
        if (
            not self.enforce_daily_hours
            or self._data.empty
            or self.fte_calculator is None
            or not self.day_hours
            or self.day_hours <= 0
        ):
            return 0

        guard = self._move_distance_guard
        partition = self._partition_mask(self._data)
        moved = 0
        dropped = 0

        for cid in [c for c in self._data[self._cluster_id].unique() if c != -1]:
            if cid in self._standalone_clusters:
                continue  # standalone markets are frozen by definition

            while True:
                cluster_df = self._data[self._data[self._cluster_id] == cid]
                if len(cluster_df) <= 1:
                    break
                if self._market_daily_hours(cid, cluster_df) <= self.day_hours:
                    break

                centroid = self._cluster_centroids.get(cid)
                if centroid is None:
                    break
                distances = cluster_df.apply(
                    lambda row: self._haversine_miles(
                        centroid['centroid_lat'], centroid['centroid_lon'],
                        row['latitude'], row['longitude'],
                    ),
                    axis=1,
                )
                idx = distances.idxmax()

                target = self._market_with_daily_room(idx, cid, guard, partition)
                if target is not None:
                    self._data.at[idx, self._cluster_id] = target
                    self._data.at[idx, self._cluster_name] = f"Market-{target}"
                    self._data.at[idx, 'ghost_id'] = f"Ghost-{target}-1"
                    moved += 1
                else:
                    self._data.at[idx, self._cluster_id] = -1
                    self._data.at[idx, self._cluster_name] = 'Outlier'
                    self._data.at[idx, 'ghost_id'] = None
                    self._data.at[idx, 'constraint_reason'] = (
                        f'over_daily_hours_budget_{self.day_hours:g}h'
                    )
                    self._outlier_stores.add(idx)
                    dropped += 1

        if moved or dropped:
            self._logger.warning(
                "Daily budget of %.1fh enforced: %s store(s) moved to a market "
                "with room in its day, %s left unassigned.",
                self.day_hours, moved, dropped,
            )
            self._recompute_cluster_centroids()

        return moved + dropped

    def _market_with_daily_room(
        self,
        idx: Any,
        current_cid: Any,
        guard: float,
        partition: Optional[pd.Series],
    ) -> Optional[int]:
        """Nearest market that can take the store without breaking its day.

        Only the five closest candidates are simulated: beyond those the move
        would trade a broken schedule for an unreasonable drive.
        """
        lat = self._data.at[idx, 'latitude']
        lon = self._data.at[idx, 'longitude']
        store_partition = (
            bool(partition.loc[idx]) if partition is not None else None
        )
        sizes = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size().to_dict()

        candidates = []
        for other, centroid in self._cluster_centroids.items():
            if not self._market_can_receive(
                other, sizes, exclude=current_cid, partition=store_partition
            ):
                continue
            distance = self._haversine_miles(
                centroid['centroid_lat'], centroid['centroid_lon'], lat, lon
            )
            if distance <= guard:
                candidates.append((distance, other))

        candidates.sort()
        store_row = self._data.loc[[idx]]
        for _, other in candidates[:5]:
            other_df = pd.concat(
                [self._data[self._data[self._cluster_id] == other], store_row]
            )
            if self._market_daily_hours(other, other_df) <= self.day_hours:
                return other

        return None

    def _readmit_rejected_as_unassigned(self) -> int:
        """Bring unplaceable stores back into the result as unassigned rows.

        With a hard ceiling (``max_reassigned_stores``) or an explicit
        ``unassign_distance``, a store that no market can take is a delivery,
        not a silence: it comes back as cluster ``-1`` carrying its
        ``constraint_reason`` instead of vanishing from the output.

        Returns:
            How many rows were readmitted.
        """
        if self._rejected.empty:
            return 0
        if not self.max_reassigned_stores and not self.unassign_distance:
            return 0

        rows = self._rejected.copy()
        rows[self._cluster_id] = -1
        rows[self._cluster_name] = 'Outlier'
        rows['ghost_id'] = None
        if 'constraint_reason' in rows.columns:
            rows['constraint_reason'] = rows['constraint_reason'].fillna(
                'no_market_available'
            )
        else:
            rows['constraint_reason'] = 'no_market_available'

        # Fresh indexes: earlier passes rebase _data's index, so the original
        # ones may now belong to different stores
        start = int(self._data.index.max()) + 1 if not self._data.empty else 0
        rows.index = pd.RangeIndex(start, start + len(rows))
        # No pass after this point rebases _data's index, so these new
        # indexes remain valid keys for _reconcile_rejected_ledger()
        self._readmitted_index_map = dict(zip(rows.index, self._rejected.index))

        self._data = pd.concat([self._data, rows])
        self._outlier_stores.update(rows.index)
        self._logger.warning(
            "%s store(s) delivered as UNASSIGNED: no market could take them.",
            len(rows),
        )
        return len(rows)

    def _count_delivered_markets(self) -> int:
        """How many real markets the layout delivers, excluding Outliers.

        The Outliers bucket (cluster id ``-1``) is only a distinct value in
        ``_cluster_id`` when at least one store ships unassigned, so it is
        subtracted conditionally. Subtracting it unconditionally
        under-reported by one on every clean run — the Verizon layout
        resolved 122 market centroids and logged "121 clusters formed"
        with zero unassigned stores.

        Returns:
            The number of distinct market ids other than ``-1``.
        """
        if self._data is None or self._data.empty:
            return 0
        ids = self._data[self._cluster_id]
        return int(ids.nunique() - int((ids == -1).any()))

    def _reconcile_rejected_ledger(self) -> int:
        """Prune ``self._rejected`` of stores that were delivered assigned.

        ``_readmit_rejected_as_unassigned()`` copies the ledger's rows back
        into ``_data`` as cluster ``-1`` without emptying it, and later
        passes (``_rescue_unassigned_clusters``, ``_absorb_remnant_stores``,
        ``_attach_outlier_subclusters``) can then assign those rows to a
        real market. Without this reconciliation the final
        ``Total rejected stores`` log and ``_save_rejected_stores()`` would
        report stores that actually ship assigned.

        Called once in ``run()``, after every assignment pass has settled
        and right before the ledger is logged and saved. Rows never
        readmitted (no ``max_reassigned_stores``/``unassign_distance``)
        stay in the ledger: they are absent from the delivery, which is
        exactly what the ledger records.

        Returns:
            How many rows were pruned from the ledger.
        """
        if not self._readmitted_index_map or self._rejected.empty:
            return 0

        delivered_assigned = [
            original_idx
            for new_idx, original_idx in self._readmitted_index_map.items()
            if new_idx in self._data.index
            and self._data.at[new_idx, self._cluster_id] != -1
        ]
        if not delivered_assigned:
            return 0

        self._rejected = self._rejected.drop(
            index=delivered_assigned, errors='ignore'
        )
        self._logger.info(
            "%s readmitted store(s) ended up assigned and left the "
            "rejected ledger", len(delivered_assigned),
        )
        return len(delivered_assigned)

    def _unassign_orphan_stores(self) -> int:
        """Drop orphan stores until the layout is stable.

        Every removal shifts the centroid of the market that lost the store,
        which can push another store past ``unassign_distance``, so the sweep
        repeats (up to ``reassignment_passes``) until nothing changes.

        Returns:
            How many stores ended up unassigned.
        """
        if not self.unassign_distance or self._data.empty:
            return 0

        total = 0
        for _ in range(max(1, self.reassignment_passes)):
            unassigned, rehomed = self._unassign_orphan_pass()
            total += unassigned
            if not unassigned and not rehomed:
                break
            self._recompute_cluster_centroids()

        return total

    def _unassign_orphan_pass(self) -> Tuple[int, int]:
        """Leave a store unassigned when no market can legitimately hold it.

        A store farther than ``unassign_distance`` from its market centroid
        is first offered to every market within that radius that still has
        room (``max_reassigned_stores``, else ``max_cluster_size``). When
        none qualifies — nothing that close, or everything at capacity — the
        store drops to cluster ``-1`` (``Outlier``) and records why in
        ``constraint_reason``, instead of being parked hundreds of miles from
        a market nobody can service it from.

        Returns:
            ``(unassigned, rehomed)`` counts for this sweep.
        """
        limit = self.unassign_distance
        if not limit or self._data.empty:
            return 0, 0

        partition = self._partition_mask(self._data)
        gate = self._capacity_gate
        assigned = self._data[self._data[self._cluster_id] != -1]
        sizes = assigned.groupby(self._cluster_id).size().to_dict()
        unassigned = 0
        rehomed = 0

        for idx, store in assigned.iterrows():
            cid = store[self._cluster_id]
            if cid in self._standalone_clusters:
                continue  # standalone markets are distance-blind by definition
            centroid = self._cluster_centroids.get(cid)
            if centroid is None:
                continue

            lat = store['latitude']
            lon = store['longitude']
            distance = self._haversine_miles(
                centroid['centroid_lat'], centroid['centroid_lon'], lat, lon
            )
            if distance <= limit:
                continue

            store_partition = (
                bool(partition.loc[idx]) if partition is not None else None
            )
            best: Optional[Tuple[float, int]] = None
            for other, other_centroid in self._cluster_centroids.items():
                if not self._market_can_receive(
                    other, sizes, exclude=cid, partition=store_partition
                ):
                    continue
                other_distance = self._haversine_miles(
                    other_centroid['centroid_lat'],
                    other_centroid['centroid_lon'],
                    lat, lon,
                )
                if other_distance <= limit and (best is None or other_distance < best[0]):
                    best = (other_distance, other)

            if best is not None:
                self._data.at[idx, self._cluster_id] = best[1]
                self._data.at[idx, self._cluster_name] = f"Market-{best[1]}"
                self._data.at[idx, 'ghost_id'] = f"Ghost-{best[1]}-1"
                sizes[cid] = sizes.get(cid, 1) - 1
                sizes[best[1]] = sizes.get(best[1], 0) + 1
                rehomed += 1
                continue

            self._data.at[idx, self._cluster_id] = -1
            self._data.at[idx, self._cluster_name] = 'Outlier'
            self._data.at[idx, 'ghost_id'] = None
            self._data.at[idx, 'constraint_reason'] = (
                f'no_market_with_room_within_{limit:g}_miles'
            )
            self._outlier_stores.add(idx)
            sizes[cid] = sizes.get(cid, 1) - 1
            unassigned += 1

        if rehomed:
            self._logger.info(
                "Moved %s store(s) to a market within %s miles before "
                "considering them unassigned", rehomed, limit,
            )
        if unassigned:
            self._logger.warning(
                "%s store(s) left UNASSIGNED: no market with room within %s "
                "miles (capacity gate %s)", unassigned, limit, gate,
            )
        return unassigned, rehomed

    def _plan_market_dissolution(
        self,
        cid: int,
        assigned: pd.DataFrame,
        sizes: pd.Series,
        partition: Optional[pd.Series],
        guard: float,
        split_target: Optional[int] = None,
    ) -> Optional[Dict[Any, int]]:
        """Plan where each store of ``cid`` would go if the market dissolved.

        Every store must land in another market of its own partition whose
        centroid is within ``guard`` miles and that stays at or below
        ``max_cluster_size`` once it takes the store — dissolving a market
        must never mint the next oversized one. ``split_target`` (the market
        about to be split in two) is exempt from that ceiling: it is halved
        immediately afterwards.

        Returns:
            ``{store_index: target_market}``, or ``None`` when at least one
            store has no market close enough with room (the market must then
            survive).
        """
        members = assigned.index[assigned[self._cluster_id] == cid]
        if len(members) == 0:
            return None

        centroids = {
            other: (centroid['centroid_lat'], centroid['centroid_lon'])
            for other, centroid in self._cluster_centroids.items()
            if other != cid
            and other in sizes.index
            and other not in self._standalone_clusters
        }
        if not centroids:
            return None

        projected = {other: int(sizes[other]) for other in centroids}
        moves: Dict[Any, int] = {}
        for idx in members:
            lat = self._data.at[idx, 'latitude']
            lon = self._data.at[idx, 'longitude']
            store_partition = (
                bool(partition.loc[idx]) if partition is not None else None
            )
            # Reach order: the tight guard first, then the distance at which
            # a store would still be considered assignable at all
            reaches = [guard]
            if self.unassign_distance and self.unassign_distance > guard:
                reaches.append(float(self.unassign_distance))

            choice: Optional[Tuple[float, int]] = None
            for reach in reaches:
                nearest_with_room: Optional[Tuple[float, int]] = None
                nearest_any: Optional[Tuple[float, int]] = None
                for other, (clat, clon) in centroids.items():
                    if store_partition is not None and self._cluster_partition.get(
                        other, False
                    ) != store_partition:
                        continue
                    distance = self._haversine_miles(clat, clon, lat, lon)
                    if distance > reach:
                        continue
                    if nearest_any is None or distance < nearest_any[0]:
                        nearest_any = (distance, other)
                    has_room = (
                        other == split_target
                        or projected[other] < self._effective_ceiling(other)
                    )
                    if has_room and (
                        nearest_with_room is None or distance < nearest_with_room[0]
                    ):
                        nearest_with_room = (distance, other)

                # A neighbour that grows past the ceiling is acceptable here:
                # it becomes the next market this pass splits.
                choice = nearest_with_room or nearest_any
                if choice is not None:
                    break

            if choice is None:
                if not self.unassign_distance:
                    return None  # this market cannot be dissolved
                # No market can hold this store: it becomes unassigned, which
                # is what the next pass would decide for it anyway
                moves[idx] = -1
                continue

            moves[idx] = choice[1]
            projected[choice[1]] += 1

        return moves

    def _split_market(self, stores: pd.DataFrame, cid: int, reason: str) -> Optional[int]:
        """Cut one market in two with KMeans over its CORE members' coordinates.

        FEAT-248 TASK-204: sub-cluster (satellite) rows are excluded from
        the KMeans input — including them was the coreless-market factory
        (a half could end up 100% satellites). ``cid`` is never retired by
        this method (only the new half, ``new_cid``, is born), so every
        excluded satellite row simply stays on the surviving parent id —
        never hand-assigned here, never left pointing at a retired market;
        the guarded ``_select_subcluster_market`` path (TASK-202) is the
        only place a satellite pocket gets re-anchored or delivered
        unassigned, and this method never duplicates that decision.

        Args:
            stores: DataFrame holding the cluster assignments.
            cid: Market to split.
            reason: Logged explanation of why the split happens.

        Returns:
            The id of the market born from the split, or ``None`` when the
            market has fewer than two CORE (non-satellite) stores.
        """
        member_idx = stores.index[stores[self._cluster_id] == cid]
        if 'is_subcluster' in stores.columns:
            # `!= True`, not `~.astype(bool)` -- see the note in
            # _annotate_subcluster_overflow: a comparison treats any NaN
            # gap as False (kept in), matching the defensive pattern used
            # throughout this file for this exact column.
            core_idx = member_idx[stores.loc[member_idx, 'is_subcluster'] != True]
        else:
            core_idx = member_idx
        if len(core_idx) < 2:
            return None

        coords = stores.loc[core_idx, ['latitude', 'longitude']].to_numpy()
        labels = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(coords)
        moved = core_idx[labels == 1]
        if len(moved) == 0 or len(moved) == len(core_idx):
            # Degenerate geometry (e.g. identical coordinates): split evenly
            moved = core_idx[: len(core_idx) // 2]

        new_cid = int(stores[self._cluster_id].max()) + 1
        stores.loc[moved, self._cluster_id] = new_cid
        self._cluster_partition[new_cid] = self._cluster_partition.get(cid, False)
        # A market born here is a market like any other: it needs its OWN
        # base. Without this the moved rows keep the parent's ghost_id, so
        # two markets ship the same employee identity — SchedulingVisits
        # then treats them as one rep, and `num_employees` reports 1 per
        # market while fewer distinct bases actually exist. Mirrors what
        # _merge_markets does for the receiving side.
        if 'ghost_id' in stores.columns:
            stores.loc[moved, 'ghost_id'] = f"Ghost-{new_cid}-1"
        # The dense core may now live in either half: drop the stale anchor so
        # both halves re-derive their centroid from their own members at the
        # next recompute
        self._anchored_centroids.pop(cid, None)
        self._logger.info(
            "Split cluster %s (%s stores) into %s + %s stores to %s",
            cid,
            len(member_idx),
            len(member_idx) - len(moved),
            len(moved),
            reason,
        )
        return new_cid

    def _enforce_max_cluster_size(self):
        """Shed stores from over-capacity markets into nearby markets.

        Repeatedly takes the most over-capacity market and moves its store
        closest to another market with room (same isolation partition) until
        every market is at or below its ``_effective_ceiling`` (FEAT-248
        G2: the single ceiling — ``max_cluster_size`` tightened by the
        market's own time budget when ``capacity_from_hours`` is on — not
        the raw, hours-blind ``max_cluster_size`` this pass compared
        against before). If no market has room the overage stays and a
        warning is logged — the exact market count outranks the size
        ceiling.

        FEAT-248 TASK-203: this pass now also runs a second time, AFTER
        ``_attach_outlier_subclusters``, so satellite attachment can no
        longer push a market over ceiling for free. Sizes (and therefore
        which markets are "over") count sub-cluster rows same as before,
        but the candidate pool of stores this pass may MOVE excludes them
        — a sub-cluster pocket is an atomic unit that only
        ``_cede_oversize_subclusters`` may relocate (whole pocket, never
        one row); this pass only ever sheds CORE stores. A market whose
        entire overage is satellite rows has nothing this pass can shed —
        it is marked unfixable here and left to cession/annotation.
        """
        if (
            not self.enforce_max_cluster_size
            or not self.max_cluster_size
            or self._data.empty
        ):
            return

        partition = self._partition_mask(self._data)
        # Same distance guard as _fill_undersized_clusters: overflow is never
        # shed to a market unreasonably far away — absorbed orphan stores may
        # keep a market above max_cluster_size.
        guard = self._move_distance_guard
        has_subclusters = 'is_subcluster' in self._data.columns
        moved = 0
        unfixable: set = set()
        while True:
            assigned = self._data[self._data[self._cluster_id] != -1]
            sizes = assigned.groupby(self._cluster_id).size()
            ceilings = sizes.index.to_series().map(self._effective_ceiling)
            over = sizes[sizes > ceilings]
            over = over[~over.index.isin(self._standalone_clusters)]
            over = over[~over.index.isin(unfixable)]
            if over.empty:
                break

            cid = over.idxmax()
            cid_partition = self._cluster_partition.get(cid, False)
            receivers = [
                other for other in sizes.index
                if other != cid and sizes[other] < self._effective_ceiling(other)
                and other not in self._standalone_clusters
                and (
                    partition is None
                    or self._cluster_partition.get(other, False) == cid_partition
                )
            ]
            if not receivers:
                unfixable.add(cid)
                self._logger.warning(
                    "Market %s keeps %s stores (max_cluster_size=%s): no market "
                    "with capacity available in its partition.",
                    cid, int(sizes[cid]), self.max_cluster_size,
                )
                continue

            receiver_centroids = {
                other: (
                    float(assigned.loc[assigned[self._cluster_id] == other, 'latitude'].mean()),
                    float(assigned.loc[assigned[self._cluster_id] == other, 'longitude'].mean()),
                )
                for other in receivers
            }
            core_mask = assigned[self._cluster_id] == cid
            if has_subclusters:
                core_mask &= assigned['is_subcluster'] != True
            members = assigned.index[core_mask]
            if members.empty:
                # Every row of this over-cap market is a sub-cluster row --
                # nothing here to shed; only cession may move a pocket.
                unfixable.add(cid)
                self._logger.warning(
                    "Market %s keeps %s stores (max_cluster_size=%s): every "
                    "member is a sub-cluster row -- only cession can relieve it.",
                    cid, int(sizes[cid]), self.max_cluster_size,
                )
                continue
            best: Optional[Tuple[float, Any, Any]] = None
            for member in members:
                lat = self._data.at[member, 'latitude']
                lon = self._data.at[member, 'longitude']
                for other, (rlat, rlon) in receiver_centroids.items():
                    dist = self._haversine_miles(rlat, rlon, lat, lon)
                    if best is None or dist < best[0]:
                        best = (dist, member, other)

            best_dist, move_idx, target = best
            if best_dist > guard:
                unfixable.add(cid)
                self._logger.warning(
                    "Market %s keeps %s stores (max_cluster_size=%s): nearest "
                    "market with room is %.1f miles away (guard %s miles).",
                    cid, int(sizes[cid]), self.max_cluster_size, best_dist, guard,
                )
                continue
            self._data.at[move_idx, self._cluster_id] = target
            moved += 1

        if moved:
            self._logger.info(
                "Rebalanced %s stores to honour max_cluster_size=%s",
                moved, self.max_cluster_size,
            )

    def _fill_undersized_clusters(self):
        """Pull stores into markets below ``min_cluster_size``.

        The most undersized market repeatedly pulls its geographically
        nearest store from a donor market of the same isolation partition
        that can spare one (donor stays at or above the minimum). Pulls
        respect ``_move_distance_guard``: an isolated market (e.g. Hawaii,
        Alaska) keeps its small size — with a warning — rather than absorb
        stores from unreasonably far away.
        """
        if not self.min_cluster_size or self.min_cluster_size <= 1 or self._data.empty:
            return

        partition = self._partition_mask(self._data)
        guard = self._move_distance_guard
        moved = 0
        unfixable: set = set()
        while True:
            assigned = self._data[self._data[self._cluster_id] != -1]
            sizes = assigned.groupby(self._cluster_id).size()
            under = sizes[sizes < self.min_cluster_size]
            under = under[~under.index.isin(unfixable)]
            under = under[~under.index.isin(self._standalone_clusters)]
            if under.empty:
                break

            cid = under.idxmin()
            cid_partition = self._cluster_partition.get(cid, False)
            members = assigned[assigned[self._cluster_id] == cid]
            centroid_lat = float(members['latitude'].mean())
            centroid_lon = float(members['longitude'].mean())

            donors = [
                other for other in sizes.index
                if other != cid and sizes[other] > self.min_cluster_size
                and other not in self._standalone_clusters
                and (
                    partition is None
                    or self._cluster_partition.get(other, False) == cid_partition
                )
            ]
            donor_stores = (
                assigned[assigned[self._cluster_id].isin(donors)]
                if donors else assigned.iloc[0:0]
            )
            if not donor_stores.empty:
                dist = donor_stores.apply(
                    lambda row: self._haversine_miles(
                        centroid_lat, centroid_lon, row['latitude'], row['longitude']
                    ),
                    axis=1,
                )
                if float(dist.min()) <= guard:
                    move_idx = dist.idxmin()
                    self._data.at[move_idx, self._cluster_id] = cid
                    moved += 1
                    continue

            # No donor at all, or the closest one is unreasonably far away:
            # keep the market small instead of building a cross-country one.
            unfixable.add(cid)
            self._logger.warning(
                "Market %s keeps %s stores (min_cluster_size=%s): no donor "
                "store within %s miles in its partition.",
                cid, int(sizes[cid]), self.min_cluster_size, guard,
            )

        if moved:
            self._logger.info(
                "Pulled %s stores to honour min_cluster_size=%s",
                moved, self.min_cluster_size,
            )

    def _reconcile_final_markets(self):
        """Restore the exact ``max_markets`` count and the size band.

        Run()-level passes (unreachable rejection, force-assignment of
        rejected stores, dissolution) can empty markets and overfill others.
        This final pass re-splits the largest markets until the exact count
        is met again, sheds over-capacity stores to markets with room, pulls
        stores into undersized markets, and refreshes the market labels.
        """
        if self._data.empty:
            return

        self._split_clusters_to_reach_max_markets(self._data)
        # Splitting mints markets whose centroids did not exist when the
        # second pass ran, so a store can end up 90 miles from its market
        # while the freshly-created one sits 30 miles away. Re-run the
        # proximity pass on the post-split geometry before the size passes
        # lock the layout in.
        self._recompute_cluster_centroids()
        self._add_distance_to_center_column(self._data)
        self._find_borderline_stores()
        self._recompute_cluster_centroids()
        # Oversized markets are cut down by reshaping the layout (a tiny
        # market hands back its slot), never by pushing stores away
        self._balance_market_sizes()
        self._recompute_cluster_centroids()
        self._add_distance_to_center_column(self._data)
        self._find_borderline_stores()
        self._recompute_cluster_centroids()
        self._enforce_max_cluster_size()
        self._fill_undersized_clusters()
        self._apply_market_labels(self._data, self._data[self._cluster_id].values)

    def _resolved_min_core_density(self) -> int:
        """Minimum neighbours (within ``density_radius``) for a dense core.

        Defaults to ``min_cluster_size``; a core of a single store is never
        meaningful, so the floor is 2.
        """
        if self.min_core_density is not None:
            return max(2, self.min_core_density)
        return max(2, int(self.min_cluster_size))

    def _anchored_centroid(
        self, members: pd.DataFrame, anchor: Tuple[float, float]
    ) -> Dict[str, float]:
        """Centroid of the dense core around ``anchor``.

        Mean of the members within ``density_radius`` of the anchor, so the
        market center stays inside the dense area (city) no matter how far
        the sparse members reach. Falls back to the plain member mean when
        no member remains inside the core.

        Args:
            members: Stores currently assigned to the cluster.
            anchor: (lat, lon) of the cluster's dense core.

        Returns:
            ``{'centroid_lat': ..., 'centroid_lon': ...}``.
        """
        anchor_lat, anchor_lon = anchor
        distances = members.apply(
            lambda row: self._haversine_miles(
                anchor_lat, anchor_lon, row['latitude'], row['longitude']
            ),
            axis=1,
        )
        core = members[distances <= self.density_radius]
        if core.empty:
            core = members
        return {
            'centroid_lat': float(core['latitude'].mean()),
            'centroid_lon': float(core['longitude'].mean()),
        }

    def _derive_core_anchor(
        self, members: pd.DataFrame, min_core: Optional[int] = None
    ) -> Optional[Tuple[float, float]]:
        """Find a dense core among a market's own members.

        Used for markets without a stored anchor (legacy BFS clusters and
        ``max_markets`` split halves): the member with the most neighbours
        within ``density_radius`` becomes the anchor when that count reaches
        the core threshold, so the centroid lands where the stores
        concentrate instead of at a plain mean dragged away by absorbed far
        stores.

        Args:
            members: Stores currently assigned to the market.
            min_core: Neighbours the densest member must have for the core to
                count. Defaults to ``_resolved_min_core_density()``. Callers
                whose market is exempt from the size caps (standalone
                markets) pass a lower floor: the default is derived from
                ``min_cluster_size``, a market-SIZE floor that has no
                business rejecting the core of a market that never had to
                respect it.

        Returns:
            (lat, lon) of the densest member, or ``None`` when the market
            has no dense core (its centroid stays at the plain mean).
        """
        n = len(members)
        if min_core is None:
            min_core = self._resolved_min_core_density()
        if n < max(2, min_core):
            return None

        coords = members[['latitude', 'longitude']].to_numpy()
        best_idx = -1
        best_count = 0
        for i in range(n):
            count = 1  # include self, matching the seeding-pass counts
            for j in range(n):
                if i == j:
                    continue
                distance = self._haversine_miles(
                    coords[i][0], coords[i][1], coords[j][0], coords[j][1]
                )
                if distance <= self.density_radius:
                    count += 1
            if count > best_count:
                best_count = count
                best_idx = i

        if best_count < min_core:
            return None
        return float(coords[best_idx][0]), float(coords[best_idx][1])

    def _nearest_absorbing_market(
        self,
        lat: float,
        lon: float,
        centroids: Dict[int, Tuple[float, float]],
        sizes: Dict[int, int],
        max_distance: float,
        room_reach: Optional[float] = None,
        entity_state: Any = None,
    ) -> Optional[Tuple[int, float, bool]]:
        """Best-scoring market within ``max_distance``, preferring those with room.

        Shared policy for every orphan-absorption pass: ``max_cluster_size``
        is SOFT (a full market is overfilled when no market with room lies
        within reach) while the distance cap is HARD.

        Room only outranks proximity inside ``room_reach`` (defaults to
        ``max_cluster_distance``). Otherwise a store next to full markets
        would be shipped across the country to the one market still below
        the cap. Within each tier (with-room / any-reachable), the WINNER
        is the highest ``_state_affinity_score`` (FEAT-247) — state affinity
        dominant by default, distance and headroom as tie-breakers —
        instead of pure nearest distance; ties on score break on lower
        distance, then lower market id (deterministic).

        Args:
            lat: Store latitude.
            lon: Store longitude.
            centroids: Candidate markets as ``{cluster_id: (lat, lon)}``,
                already filtered for standalone markets and isolation.
            sizes: Current store count per market.
            max_distance: Hard cap in miles from the market centroid.
            room_reach: How far a market with room may be and still beat a
                closer full one. Defaults to ``max_cluster_distance``.
            entity_state: The store's dominant ``state_column`` value (or
                ``None``), fed into the state-affinity score.

        Returns:
            ``(cluster_id, distance, overfilled)``, or ``None`` when no
            market centroid is within ``max_distance``.
        """
        if room_reach is None:
            room_reach = self._resolved_room_reach

        with_room: List[Tuple[Any, float]] = []
        any_reachable: List[Tuple[Any, float]] = []
        for cid, (center_lat, center_lon) in centroids.items():
            distance = self._haversine_miles(center_lat, center_lon, lat, lon)
            if distance > max_distance:
                continue
            any_reachable.append((cid, distance))
            if distance <= room_reach and sizes.get(cid, 0) < self._capacity_for(cid):
                with_room.append((cid, distance))

        def _best_scored(
            pool: List[Tuple[Any, float]]
        ) -> Optional[Tuple[Any, float]]:
            if not pool:
                return None
            pool_max_distance = max(distance for _, distance in pool)
            best: Optional[Tuple[Any, float, float]] = None  # (cid, distance, score)
            for cid, distance in pool:
                score = self._state_affinity_score(
                    entity_state, cid, distance, pool_max_distance
                )
                if best is None:
                    best = (cid, distance, score)
                    continue
                best_cid, best_distance, best_score = best
                if (
                    score > best_score
                    or (score == best_score and distance < best_distance)
                    or (
                        score == best_score and distance == best_distance
                        and cid < best_cid
                    )
                ):
                    best = (cid, distance, score)
            return best[0], best[1]

        picked = _best_scored(with_room)
        if picked is not None:
            return picked[0], picked[1], False
        if self.max_reassigned_stores:
            # Hard ceiling: a market never grows past max_reassigned_stores
            # while receiving. The store stays homeless and a later pass
            # decides whether it is unassigned.
            return None
        picked = _best_scored(any_reachable)
        if picked is not None:
            return picked[0], picked[1], True
        return None

    def _seed_uncovered_regions(
        self,
        stores: pd.DataFrame,
        unassigned: set,
        counts_by_index: Dict[int, int],
        partition: Optional[pd.Series],
        quotas: Optional[Dict[bool, int]],
        created_markets: Dict[bool, int],
        cluster_label: int,
        core_positions: Dict[int, Tuple[float, float]],
        core_partition_of: Dict[int, bool],
        core_region: Dict[int, int],
        region_cores: Dict[int, int],
        coverage_radius: float,
    ) -> int:
        """Found markets where no core reaches yet.

        The density walk stops as soon as candidates fall below
        ``min_core_density``, so a mid-sized city can end up hundreds of
        miles from the nearest core — its stores then have nowhere to go and
        surface as unassigned. Before any dense region gets a second market,
        the leftover budget covers those regions, densest first.

        Args:
            counts_by_index: Neighbours within ``density_radius`` per store.
            coverage_radius: A store farther than this from every core counts
                as uncovered.

        Returns:
            The next free cluster label.
        """
        if self.max_markets is None or not core_positions:
            return cluster_label

        while cluster_label < self.max_markets:
            candidates = sorted(unassigned)
            if not candidates:
                break

            lats = stores.loc[candidates, 'latitude'].to_numpy(dtype=float)
            lons = stores.loc[candidates, 'longitude'].to_numpy(dtype=float)
            core_ids = list(core_positions)
            core_lats = np.array([core_positions[cid][0] for cid in core_ids])
            core_lons = np.array([core_positions[cid][1] for cid in core_ids])
            nearest = self._haversine_miles(
                lats[:, None], lons[:, None], core_lats[None, :], core_lons[None, :]
            ).min(axis=1)

            uncovered = [
                (counts_by_index.get(idx, 0), -idx, idx, position)
                for position, idx in enumerate(candidates)
                if nearest[position] > coverage_radius
            ]
            if not uncovered:
                break

            # Densest uncovered store first: markets are founded where the
            # stores actually cluster, not at the first orphan we meet
            uncovered.sort(reverse=True)
            founded = False
            for _, _, idx, position in uncovered:
                idx_partition = (
                    bool(partition.loc[idx]) if partition is not None else False
                )
                if quotas is not None and created_markets[idx_partition] >= quotas[idx_partition]:
                    continue

                cid = cluster_label
                stores.at[idx, self._cluster_id] = cid
                unassigned.discard(idx)
                self._cluster_partition[cid] = idx_partition
                core_partition_of[cid] = idx_partition
                created_markets[idx_partition] += 1
                core_positions[cid] = (
                    float(stores.at[idx, 'latitude']),
                    float(stores.at[idx, 'longitude']),
                )
                core_region[cid] = cid
                region_cores[cid] = 1
                cluster_label += 1
                founded = True
                self._logger.info(
                    "Coverage market %s founded for an uncovered region "
                    "(%.1f miles from the nearest core)",
                    cid, float(nearest[position]),
                )
                break

            if not founded:
                break

        return cluster_label

    def _region_demand(
        self,
        core_positions: Dict[int, Tuple[float, float]],
        core_region: Dict[int, int],
        lats: np.ndarray,
        lons: np.ndarray,
        target_size: float,
    ) -> Dict[int, int]:
        """How many markets each region deserves, by gravitation.

        Every store is counted towards the region of its nearest core, so a
        city that sprawls beyond ``density_radius`` is sized by the stores
        that actually gravitate to it. A region then deserves one market per
        ``target_size`` stores.

        Returns:
            ``{region: markets_deserved}`` (at least one per region).
        """
        core_ids = list(core_positions)
        core_lats = np.array([core_positions[cid][0] for cid in core_ids])
        core_lons = np.array([core_positions[cid][1] for cid in core_ids])

        distances = self._haversine_miles(
            lats[:, None], lons[:, None], core_lats[None, :], core_lons[None, :]
        )
        nearest = distances.argmin(axis=1)

        tally: Dict[int, int] = {}
        for local_core in nearest:
            region = core_region[core_ids[int(local_core)]]
            tally[region] = tally.get(region, 0) + 1

        return {
            region: max(1, math.ceil(count / target_size))
            for region, count in tally.items()
        }

    def _reinforce_dense_regions(
        self,
        stores: pd.DataFrame,
        unassigned: set,
        unassigned_list: List[int],
        counts: np.ndarray,
        order: List[int],
        partition: Optional[pd.Series],
        quotas: Optional[Dict[bool, int]],
        created_markets: Dict[bool, int],
        cluster_label: int,
        core_positions: Dict[int, Tuple[float, float]],
        core_partition_of: Dict[int, bool],
        core_region: Dict[int, int],
        region_cores: Dict[int, int],
        core_separation: float,
        min_core_separation: float,
        target_size: float,
    ) -> int:
        """Spend the leftover market budget where the stores actually are.

        ``core_separation`` gives every region ONE market regardless of how
        many stores it holds, so a metro with 78 stores and a remote town
        with 14 cost the same slot. Once coverage is secured, this pass hands
        the remaining slots to the regions whose demand
        (``stores / max_cluster_size``) is still unmet, one core per region
        per round and densest first, so no single metro drains the budget.

        Args:
            unassigned: Stores still without a market; cores are removed
                from it as they are founded.
            unassigned_list: Global indexes behind the local ``counts`` order.
            counts: Neighbours within ``density_radius`` per local index.
            order: Local indexes sorted by decreasing density.
            core_separation: Radius that defines a region.
            min_core_separation: Closest two cores of a region may sit.
            target_size: Stores one market is meant to hold.

        Returns:
            The next free cluster label.
        """
        if self.max_markets is None or not core_positions:
            return cluster_label
        if not target_size or target_size == float('inf'):
            return cluster_label

        lats = stores['latitude'].to_numpy(dtype=float)
        lons = stores['longitude'].to_numpy(dtype=float)

        while cluster_label < self.max_markets:
            # Demand is measured by gravitation, not by the neighbours inside
            # density_radius: a city spread over 60 miles would otherwise look
            # half its size and run out of markets, leaving its overflow
            # unassigned.
            deserved = self._region_demand(
                core_positions, core_region, lats, lons, target_size
            )
            progressed = False
            for local_i in order:
                if cluster_label >= self.max_markets:
                    break
                global_idx = unassigned_list[local_i]
                if global_idx not in stores.index:
                    continue
                if stores.at[global_idx, self._cluster_id] != -1:
                    continue  # already a core

                idx_partition = (
                    bool(partition.loc[global_idx]) if partition is not None else False
                )
                if quotas is not None and created_markets[idx_partition] >= quotas[idx_partition]:
                    continue

                lat = float(stores.at[global_idx, 'latitude'])
                lon = float(stores.at[global_idx, 'longitude'])

                nearest: Optional[Tuple[float, int]] = None
                blocked = False
                for cid, (core_lat, core_lon) in core_positions.items():
                    if core_partition_of[cid] != idx_partition:
                        continue
                    distance = self._haversine_miles(lat, lon, core_lat, core_lon)
                    if distance < min_core_separation:
                        blocked = True  # too close to an existing core
                        break
                    # A store belongs to the region of its NEAREST core at any
                    # distance: demand that gravitates from 100 miles away
                    # (Naples towards a full Florida market) is demand of that
                    # region and must be able to found its own core. Bounding
                    # this by core_separation left those stores with no market
                    # while a 2-store town founded one.
                    if nearest is None or distance < nearest[0]:
                        nearest = (distance, cid)
                if blocked or nearest is None:
                    continue

                region = core_region[nearest[1]]
                if region_cores[region] >= deserved.get(region, 1):
                    continue

                cid = cluster_label
                stores.at[global_idx, self._cluster_id] = cid
                unassigned.discard(global_idx)
                self._cluster_partition[cid] = idx_partition
                core_partition_of[cid] = idx_partition
                created_markets[idx_partition] += 1
                core_positions[cid] = (lat, lon)
                core_region[cid] = region
                region_cores[region] += 1
                cluster_label += 1
                progressed = True

            if not progressed:
                break

        return cluster_label

    def _seed_density_cores(
        self,
        stores: pd.DataFrame,
        coords_rad: np.ndarray,
        unassigned: set,
        partition: Optional[pd.Series],
        quotas: Optional[Dict[bool, int]],
        created_markets: Dict[bool, int],
        cluster_label: int,
    ) -> int:
        """Density-first pass: one market per dense core, centroid anchored.

        1) Count each unassigned store's neighbours within ``density_radius``.
        2) Walk candidates by decreasing density: a store with at least
           ``min_core_density`` neighbours founds a market, unless another
           core of the same partition already sits within twice the density
           radius (isolated partitions may legitimately overlap, e.g. NYC
           next to NJ). ``max_markets`` and partition quotas are honoured.
        3) Assign the remaining stores to their nearest core, globally
           nearest-first, within ``cluster_radius`` and honouring
           ``max_cluster_size`` and isolation partitions.
        4) Anchor each market's centroid at the mean of its core members
           (those within ``density_radius`` of the core store); members past
           ``max_cluster_distance`` keep their market but are flagged as
           outliers.

        Stores that no core can absorb stay unassigned for the legacy BFS.

        Returns:
            The next free cluster label.
        """
        if not unassigned:
            return cluster_label

        unassigned_list = sorted(unassigned)
        sub_coords = coords_rad[unassigned_list]
        sub_tree = BallTree(sub_coords, leaf_size=50, metric='haversine')
        counts = sub_tree.query_radius(
            sub_coords,
            r=miles_to_radians(self.density_radius),
            count_only=True,
        )

        min_core = self._resolved_min_core_density()
        # Candidates by decreasing local density; index order breaks ties
        # so the pass is deterministic
        order = sorted(
            range(len(unassigned_list)),
            key=lambda i: (-int(counts[i]), unassigned_list[i]),
        )
        core_separation = (
            self.core_separation
            if self.core_separation is not None
            else 2.0 * self.density_radius
        )

        min_core_separation = (
            self.min_core_separation
            if self.min_core_separation is not None
            else core_separation / 3.0
        )
        target_size = float(self.max_cluster_size or 0) or float('inf')

        core_positions: Dict[int, Tuple[float, float]] = {}
        core_partition_of: Dict[int, bool] = {}
        # Region bookkeeping: cores closer than ``core_separation`` belong to
        # the same region and share its market budget
        core_region: Dict[int, int] = {}
        region_cores: Dict[int, int] = {}
        for local_i in order:
            if int(counts[local_i]) < min_core:
                break  # candidates are density-sorted: no core past this point
            if self.max_markets is not None and cluster_label >= self.max_markets:
                break
            global_idx = unassigned_list[local_i]
            idx_partition = (
                bool(partition.loc[global_idx]) if partition is not None else False
            )
            if quotas is not None and created_markets[idx_partition] >= quotas[idx_partition]:
                continue
            lat = float(stores.at[global_idx, 'latitude'])
            lon = float(stores.at[global_idx, 'longitude'])

            too_close = False
            for cid, (core_lat, core_lon) in core_positions.items():
                if core_partition_of[cid] != idx_partition:
                    continue
                if self._haversine_miles(lat, lon, core_lat, core_lon) < core_separation:
                    too_close = True
                    break
            if too_close:
                continue

            cid = cluster_label
            stores.at[global_idx, self._cluster_id] = cid
            unassigned.discard(global_idx)
            self._cluster_partition[cid] = idx_partition
            core_partition_of[cid] = idx_partition
            created_markets[idx_partition] += 1
            core_positions[cid] = (lat, lon)
            core_region[cid] = cid
            region_cores[cid] = 1
            cluster_label += 1

        # The density walk only founds cores while candidates stay above
        # min_core_density, so whole mid-sized cities can be left without a
        # market. Cover them BEFORE any dense region gets a second one.
        counts_by_index = {
            unassigned_list[local_i]: int(counts[local_i])
            for local_i in range(len(unassigned_list))
        }
        cluster_label = self._seed_uncovered_regions(
            stores, unassigned, counts_by_index, partition, quotas,
            created_markets, cluster_label, core_positions, core_partition_of,
            core_region, region_cores,
            self.max_cluster_distance or self.cluster_radius,
        )

        # Coverage is served: every region that can hold a market has one.
        # What is left of the budget now follows DEMAND — a metro holding
        # more stores than one market can take gets extra cores, an isolated
        # 14-store town keeps its single slot. Rounds hand out one core per
        # region at a time so the densest region cannot swallow the rest.
        cluster_label = self._reinforce_dense_regions(
            stores, unassigned, unassigned_list, counts, order, partition, quotas,
            created_markets, cluster_label, core_positions, core_partition_of,
            core_region, region_cores,
            core_separation, min_core_separation, target_size,
        )

        if not core_positions:
            return cluster_label

        # Globally nearest-first assignment: every store lands in the closest
        # core with remaining capacity, so a city fills with its own stores
        # before absorbing a neighbouring city's
        candidates: List[Tuple[float, int, int]] = []
        for idx in sorted(unassigned):
            lat = float(stores.at[idx, 'latitude'])
            lon = float(stores.at[idx, 'longitude'])
            idx_partition = (
                bool(partition.loc[idx]) if partition is not None else False
            )
            for cid, (core_lat, core_lon) in core_positions.items():
                if core_partition_of[cid] != idx_partition:
                    continue
                distance = self._haversine_miles(core_lat, core_lon, lat, lon)
                # The expanded (1.1x) radius only feeds clusters still below
                # min_cluster_size, mirroring the legacy BFS expansion
                if distance <= self.cluster_radius * 1.1:
                    candidates.append((distance, idx, cid))
        candidates.sort()

        sizes = {cid: 1 for cid in core_positions}
        for distance, idx, cid in candidates:
            if idx not in unassigned:
                continue
            if sizes[cid] >= self._seed_ceiling:
                continue
            if distance > self.cluster_radius and sizes[cid] >= self.min_cluster_size:
                continue
            stores.at[idx, self._cluster_id] = cid
            unassigned.discard(idx)
            sizes[cid] += 1

        for cid, (core_lat, core_lon) in core_positions.items():
            members = stores[stores[self._cluster_id] == cid]
            distances = members.apply(
                lambda row: self._haversine_miles(
                    core_lat, core_lon, row['latitude'], row['longitude']
                ),
                axis=1,
            )
            anchor_members = members[distances <= self.density_radius]
            if anchor_members.empty:
                anchor_members = members
            anchor = (
                float(anchor_members['latitude'].mean()),
                float(anchor_members['longitude'].mean()),
            )
            self._anchored_centroids[cid] = anchor
            # The anchor is kept either way (market_center='anchored' needs
            # it), but the centre handed to the passes that run inside
            # _create_cluster follows the configured definition.
            self._cluster_centroids[cid] = self._cluster_center(cid, members)
            # Distant members keep their market but carry the outlier flag,
            # mirroring what force-assignment would deliver anyway
            far = members.index[
                distances > (self.max_cluster_distance + self.borderline_threshold)
            ]
            self._outlier_stores.update(far)
            self._logger.info(
                "Density core market %s: %s stores, %s in core, anchor (%.4f, %.4f)",
                cid, len(members), len(anchor_members), anchor[0], anchor[1],
            )

        return cluster_label

    def _create_cluster(self, stores: pd.DataFrame):
        """
        1) BFS with BallTree to create a provisional cluster.
        2) Post-check each cluster with a distance validation (centroid-based or K-Means).
        3) Mark outliers as -1 or store them as rejected.
        """
        # 1) Sort by latitude and longitude to ensure spatial proximity in clustering
        stores = stores.sort_values(by=['latitude', 'longitude']).reset_index(drop=True)
        # FEAT-247: point self._data at the WIP frame for the rest of this
        # method's execution so state-affinity scoring helpers
        # (_market_dominant_state/_market_headroom, which read
        # self._data) see this method's own in-progress cluster
        # membership rather than stale pre-clustering state. The caller
        # reassigns self._data to this same (further-mutated) object when
        # _create_cluster returns, so this is a safe pre-commit.
        self._data = stores
        # Isolation partitions (e.g. NYC vs rest): computed after the reset so
        # the mask is aligned with the positional indices used by the BFS.
        partition = self._partition_mask(stores)
        self._cluster_partition = {}
        self._anchored_centroids = {}
        stores['rad'] = stores.apply(
            lambda row: np.radians([row.latitude, row.longitude]), axis=1
        )
        # rad_df = stores[['latitude', 'longitude']].apply(degrees_to_radians, axis=1).apply(pd.Series)
        # stores = pd.concat([stores, rad_df], axis=1)
        # stores.rename(columns={0: "rad_latitude", 1: "rad_longitude"}, inplace=True)

        # Convert 'rad' column to a numpy array for BallTree
        coords_rad = np.stack(stores['rad'].to_numpy())

        # Create BallTree with all coordinates:
        tree = BallTree(
            coords_rad,
            leaf_size=15,
            metric='haversine'
        )

        # All unassigned
        N = len(stores)
        # Initialize cluster labels to -1 (unassigned)
        stores[self._cluster_id] = -1
        unassigned = set(range(N))
        outliers = set()
        outlier_attempts = {idx: 0 for idx in range(N)}  # Track attempts to recluster

        cluster_label = 0

        # Standalone markets are computed FIRST: one market per listed value
        # with every matching store, regardless of distance or size caps.
        # They stay frozen for the rest of the pipeline and count against
        # max_markets.
        self._standalone_clusters = {}
        if self._standalone_groups:
            if not self.isolation_column or self.isolation_column not in stores.columns:
                raise ComponentError(
                    "standalone_markets is configured but isolation_column "
                    f"'{self.isolation_column}' is missing from the input DataFrame."
                )
            column = stores[self.isolation_column]
            for group in self._standalone_groups:
                # A group holds every isolation value that must share ONE
                # market, so all of its stores are selected at once.
                member_idx = stores.index[column.isin(group)].tolist()
                missing = [value for value in group if not (column == value).any()]
                if missing:
                    self._logger.warning(
                        "standalone market %s: no stores found in column %r for %s",
                        self._format_standalone_group(group),
                        self.isolation_column,
                        ", ".join(repr(value) for value in missing),
                    )
                if not member_idx:
                    continue
                stores.loc[member_idx, self._cluster_id] = cluster_label
                unassigned.difference_update(member_idx)
                self._standalone_clusters[cluster_label] = group
                self._cluster_partition[cluster_label] = True
                members = stores.loc[member_idx]
                # A standalone market takes every store of its isolation
                # value regardless of distance, so it is the layout's most
                # likely market to span two poles: the real Verizon
                # 'Seattle' sub-market holds a dense Puget Sound core plus
                # nine Alaska stores, and the mean of the two falls in the
                # open Pacific off British Columbia. Density-seeded markets
                # are born around a core and record it; standalone markets
                # have no seed, so the core is derived here from their own
                # members and stored the same way, which keeps their centre
                # inside the metro they actually serve. The floor is 2, not
                # min_cluster_size: a frozen market exempt from the size
                # caps must never be denied a core by a size threshold.
                anchor = self._derive_core_anchor(members, min_core=2)
                if anchor is not None:
                    self._anchored_centroids[cluster_label] = anchor
                self._cluster_centroids[cluster_label] = self._cluster_center(
                    cluster_label, members
                )
                self._logger.info(
                    "Standalone market %s: %s stores (market id %s, anchor %s)",
                    self._format_standalone_group(group),
                    len(member_idx),
                    cluster_label,
                    "(%.4f, %.4f)" % anchor if anchor else "none",
                )
                cluster_label += 1

        # Convert self.cluster_radius (in miles) to radians for BallTree search
        radius_radians = miles_to_radians(self.cluster_radius)

        # Proportional market quotas per isolation partition (only active when
        # both max_markets and isolation are configured)
        quotas = self._partition_market_quotas(partition)
        created_markets: Dict[bool, int] = {True: 0, False: 0}
        if quotas is not None:
            self._logger.info(
                "max_markets=%s split by isolation partition: %s isolated, %s rest",
                self.max_markets, quotas[True], quotas[False],
            )

        # First pass: dense cores found their own markets with centroids
        # anchored inside the core; the sparse remainder falls through to
        # the legacy BFS below.
        if self.density_seeding:
            cluster_label = self._seed_density_cores(
                stores, coords_rad, unassigned, partition,
                quotas, created_markets, cluster_label,
            )

        while unassigned:
            if self.max_markets is not None and cluster_label >= self.max_markets:
                self._logger.warning(
                    "max_markets=%s reached with %s stores still unassigned; "
                    "they will be assigned to their nearest market and flagged as outliers.",
                    self.max_markets,
                    len(unassigned),
                )
                break

            # Convert unassigned set to list and rebuild BallTree
            unassigned_list = sorted(list(unassigned))
            unassigned_coords = coords_rad[unassigned_list]

            # Build a new BallTree with only unassigned elements
            tree = BallTree(
                unassigned_coords,
                leaf_size=50,
                metric='haversine'
            )

            # Start a new cluster
            cluster_indices = []
            # Get the first unassigned store whose partition still has quota
            current_idx = None
            for idx in unassigned_list:
                idx_partition = (
                    bool(partition.loc[idx]) if partition is not None else False
                )
                if quotas is None or created_markets[idx_partition] < quotas[idx_partition]:
                    current_idx = idx
                    break
            if current_idx is None:
                self._logger.warning(
                    "Partition market quotas exhausted with %s stores still "
                    "unassigned; they will be assigned within their own partition.",
                    len(unassigned),
                )
                break
            cluster_indices.append(current_idx)
            stores.at[current_idx, self._cluster_id] = cluster_label
            unassigned.remove(current_idx)
            # The seed's partition defines the whole cluster's partition
            seed_partition = (
                bool(partition.loc[current_idx]) if partition is not None else False
            )
            self._cluster_partition[cluster_label] = seed_partition
            created_markets[seed_partition] += 1

            # Frontier for BFS
            frontier = [current_idx]

            while frontier and len(cluster_indices) < self.max_cluster_size:
                # Map global index to local index for the BallTree query
                global_idx = frontier.pop()
                local_idx = unassigned_list.index(global_idx)

                neighbors, distances = tree.query_radius(
                    [unassigned_coords[local_idx]], r=radius_radians, return_distance=True
                )

                neighbors = neighbors[0]  # Extract the single query point's neighbors
                distances = distances[0]  # Extract the single query point's distances

                # Map local indices back to global indices
                global_neighbors = [unassigned_list[i] for i in neighbors]
                new_candidates = [idx for idx in global_neighbors if idx in unassigned]

                # print('New candidates ', len(new_candidates))
                if not new_candidates and len(cluster_indices) < self.min_cluster_size:
                    # Expand search radius for small clusters
                    expanded_radius = radius_radians * 1.1  # Slightly larger radius
                    neighbors, distances = tree.query_radius(
                        [unassigned_coords[local_idx]], r=expanded_radius, return_distance=True
                    )
                    neighbors = neighbors[0]
                    distances = distances[0]
                    global_neighbors = [unassigned_list[i] for i in neighbors]
                    new_candidates = [idx for idx in global_neighbors if idx in unassigned]
                    if not new_candidates:
                        continue
                elif not new_candidates:
                    continue

                # Isolation: only stores of the seed's partition may join
                if partition is not None:
                    new_candidates = [
                        idx for idx in new_candidates
                        if bool(partition.loc[idx]) == seed_partition
                    ]
                    if not new_candidates:
                        continue

                # Limit number of stores to add to not exceed max_cluster_size
                num_needed = self.max_cluster_size - len(cluster_indices)
                new_candidates = new_candidates[:num_needed]

                # Assign them to the cluster
                for cand_idx in new_candidates:
                    if cand_idx not in cluster_indices:
                        frontier.append(cand_idx)
                    stores.at[cand_idx, self._cluster_id] = cluster_label
                    # Remove new_indices from unassigned_indices
                    unassigned.remove(cand_idx)

                # Add them to BFS frontier
                frontier.extend(new_candidates)
                cluster_indices.extend(new_candidates)

            # Validate cluster
            outliers = self._detect_outliers(stores, cluster_label, cluster_indices)
            for out_idx in outliers:
                stores.at[out_idx, self._cluster_id] = -1
                unassigned.add(out_idx)

            cluster_label += 1

        # Post-process unassigned stores
        print(f"Starting post-processing for {len(unassigned)} unassigned stores.")
        self._post_process_outliers(stores, unassigned)

        # Any store still unassigned (e.g. beyond max_markets and too far for the
        # relaxed threshold) is moved to its nearest market, keeping its outlier flag.
        remaining = stores.index[stores[self._cluster_id] == -1].tolist()
        if remaining:
            self._force_assign_to_nearest_market(stores, remaining)

        # max_markets is an exact target: split clusters until it is reached
        # (cluster_radius is only a soft preference in that mode)
        self._split_clusters_to_reach_max_markets(stores)

        # Map cluster -> Market1, Market2, ...
        print(f"Final clusters formed: {cluster_label}")
        print(f"Total outliers: {len(outliers)}")

        print(stores)
        self._apply_market_labels(stores, stores[self._cluster_id].values)
        return stores

    def _build_haversine_matrix(self, coords_rad, tree: BallTree) -> np.ndarray:
        """
        Build a full NxN matrix of haversine distances in radians.
        """
        n = len(coords_rad)
        dist_matrix = np.zeros((n, n), dtype=float)

        for i in range(n):
            dist, idx = tree.query([coords_rad[i]], k=n)
            dist = dist[0]  # shape (n,)
            idx = idx[0]    # shape (n,)
            dist_matrix[i, idx] = dist

        return dist_matrix

    def _convert_to_radians(self, value: float, unit: str) -> float:
        """
        Convert value in miles or km to radians (on Earth).
        Earth radius ~ 6371 km or 3959 miles.
        """
        if unit.lower().startswith('mile'):
            # miles
            earth_radius = 3959.0
        else:
            # kilometers
            earth_radius = 6371.0

        return value / earth_radius

    def _apply_market_labels(self, df: pd.DataFrame, labels: np.ndarray):
        """Map cluster_id => Market-1, Market-2, etc. (1-based)."""
        cluster_map = {}
        cluster_ids = sorted(set(labels))
        market_idx = 1
        for cid in cluster_ids:
            if cid == -1:
                cluster_map[cid] = "Outlier"
            else:
                cluster_map[cid] = f"Market-{market_idx}"
                market_idx += 1
        df[self._cluster_name] = df[self._cluster_id].map(cluster_map)

    def _remap_cluster_ids(self, mapping: Dict[Any, Any]) -> None:
        """Apply a total cluster-id remap to every id-keyed structure.

        Shared by ``_renumber_markets_from_one`` (compacts ids to 1..N) and
        the FEAT-247 per-region orchestration's ``_shift_region_cluster_ids``
        (offsets one region's ids into a globally-unique range before
        concatenation). ``mapping`` must cover every id currently present in
        ``self._data`` (including ``-1`` when outliers are present).

        Args:
            mapping: Old cluster id -> new cluster id.
        """
        self._data[self._cluster_id] = self._data[self._cluster_id].map(mapping)
        self._cluster_centroids = {
            mapping.get(cid, cid): info for cid, info in self._cluster_centroids.items()
        }
        self._cluster_fte_info = {
            mapping.get(cid, cid): info for cid, info in self._cluster_fte_info.items()
        }
        self._cluster_partition = {
            mapping[cid]: part for cid, part in self._cluster_partition.items()
            if cid in mapping
        }
        self._standalone_clusters = {
            mapping[cid]: value for cid, value in self._standalone_clusters.items()
            if cid in mapping
        }
        self._anchored_centroids = {
            mapping[cid]: anchor for cid, anchor in self._anchored_centroids.items()
            if cid in mapping
        }

        if 'ghost_id' in self._data.columns:
            def _remap_ghost(value: Any) -> Any:
                if not isinstance(value, str) or not value.startswith('Ghost-'):
                    return value
                parts = value.split('-')
                if len(parts) != 3:
                    return value
                try:
                    old_cid = int(parts[1])
                except ValueError:
                    return value
                new_cid = mapping.get(old_cid)
                return f"Ghost-{new_cid}-{parts[2]}" if new_cid is not None else value

            self._data['ghost_id'] = self._data['ghost_id'].map(_remap_ghost)

    def _renumber_markets_from_one(self):
        """Renumber final market ids sequentially starting at 1.

        Internal cluster ids can end up sparse (splits, dissolutions) and are
        0-based. The delivered layout uses market_id 1..N aligned with the
        Market-1..Market-N labels; -1 (Outlier) is preserved. Internal dicts
        keyed by cluster id and the ghost_id column are remapped to match.
        """
        if self._data.empty:
            return

        old_ids = sorted(
            cid for cid in self._data[self._cluster_id].unique() if cid != -1
        )
        mapping = {old: new for new, old in enumerate(old_ids, start=1)}
        mapping[-1] = -1

        self._remap_cluster_ids(mapping)
        self._apply_market_labels(self._data, self._data[self._cluster_id].values)

    def _shift_region_cluster_ids(self, id_offset: int) -> int:
        """Shift this region's cluster/market ids by ``id_offset`` (FEAT-247).

        Every region's ``_create_cluster`` call independently mints ids
        starting at 0, so concatenating two regions' frames without
        shifting would collide: ``_renumber_markets_from_one`` groups by
        numeric id VALUE, not by ``(region, id)``, and would silently merge
        two different regions' "market 0" into one delivered market.
        ``-1`` (Outlier) always stays ``-1``.

        Args:
            id_offset: Amount to add to every non-outlier id in this region.

        Returns:
            The offset the NEXT region must use (this region's highest
            shifted id + 1), or ``id_offset`` unchanged when this region
            formed no markets.
        """
        if self._data.empty:
            return id_offset

        ids_present = sorted(
            cid for cid in self._data[self._cluster_id].unique() if cid != -1
        )
        if not ids_present:
            return id_offset

        mapping = {old: old + id_offset for old in ids_present}
        mapping[-1] = -1
        self._remap_cluster_ids(mapping)
        return max(mapping[old] for old in ids_present) + 1

    def _shift_region_indices(self, row_offset: int) -> int:
        """Shift this region's row-index-keyed state by ``row_offset`` (FEAT-247).

        ``_create_cluster``'s ``reset_index(drop=True)`` is NOT the only
        index reset in the pipeline, and index growth is not bounded by
        the region's original row count either: ``_force_assign_all_
        rejected_stores`` re-concatenates with ``ignore_index=True``
        (a second full reset), and ``_readmit_rejected_as_unassigned``
        deliberately mints NEW indices starting at ``self._data.index.
        max() + 1`` ("earlier passes rebase _data's index, so the
        original ones may now belong to different stores" — its own
        docstring) — which can and does exceed the region's row count on
        real data. So the next region's offset is derived from the
        ACTUALLY OBSERVED highest index after shifting, not assumed from
        ``len(region_df)``.

        ``self._readmitted_index_map`` (``_readmit_rejected_as_
        unassigned``'s new-index -> original-``_rejected``-index map,
        consulted once by ``_reconcile_rejected_ledger()`` in run()'s
        global tail) is index-keyed on BOTH sides and must shift the same
        way, or a readmitted-then-reassigned store from any region but
        the last processed silently ships both assigned in ``self._data``
        AND still counted in the rejected ledger.

        Args:
            row_offset: Amount to add to every row index in this region.

        Returns:
            The offset the NEXT region must use — this region's highest
            index (across ``self._data`` and ``self._rejected``) + 1, or
            ``row_offset`` unchanged when this region is entirely empty.
        """
        if row_offset:
            if len(self._data):
                self._data.index = self._data.index + row_offset
            if not self._rejected.empty:
                self._rejected.index = self._rejected.index + row_offset
            if self._outlier_stores:
                self._outlier_stores = {
                    idx + row_offset for idx in self._outlier_stores
                }
            if self._readmitted_index_map:
                self._readmitted_index_map = {
                    new_idx + row_offset: original_idx + row_offset
                    for new_idx, original_idx in self._readmitted_index_map.items()
                }

        max_index = -1
        if len(self._data):
            max_index = max(max_index, int(self._data.index.max()))
        if not self._rejected.empty:
            max_index = max(max_index, int(self._rejected.index.max()))
        return max_index + 1 if max_index >= 0 else row_offset

    def _add_cluster_centroids_to_result(self, df: pd.DataFrame):
        """Add cluster centroid coordinates to the result DataFrame."""
        df['centroid_lat'] = df[self._cluster_id].map(
            lambda cid: self._cluster_centroids.get(cid, {}).get('centroid_lat', np.nan)
        )
        df['centroid_lon'] = df[self._cluster_id].map(
            lambda cid: self._cluster_centroids.get(cid, {}).get('centroid_lon', np.nan)
        )

    def _centroid_points(self) -> Dict[Any, Tuple[float, float]]:
        """Collect the one point per market that describes its centre.

        Outliers (cluster id ``-1``) are excluded: an unassigned store
        belongs to no market, so there is no centre to name. Markets whose
        centroid never settled to a real coordinate are dropped rather than
        sent to the backend as a NaN pair.

        Returns:
            A mapping from cluster id to ``(latitude, longitude)``.
        """
        points: Dict[Any, Tuple[float, float]] = {}
        for cid, info in self._cluster_centroids.items():
            if cid == -1:
                continue
            lat = info.get('centroid_lat')
            lon = info.get('centroid_lon')
            if lat is None or lon is None or pd.isna(lat) or pd.isna(lon):
                continue
            points[cid] = (float(lat), float(lon))
        return points

    async def _resolve_centroid_locations(self) -> None:
        """Reverse-geocode each market's centroid into a street address.

        One Overpass query per market — the centroid itself, not a member
        store — de-duplicated and run with bounded concurrency, so a market
        of 400 stores still costs exactly one lookup.

        The centroid is a geometric mean and can land anywhere: a parking
        lot, a field, the middle of a lake. The geocoder widens its search
        radius and, failing that, degrades to the nearest named road and
        then to ``"<County>, <ST>"``, which is why a market can report an
        approximate label instead of a street. Failure is never fatal
        either: an unreachable backend leaves every location empty and logs
        a warning, because an address label is not worth losing a month's
        layout over.

        Populates `self._centroid_locations`, keyed by cluster id.
        """
        if not self.resolve_centroid_location:
            return
        points = self._centroid_points()
        if not points:
            self._logger.warning(
                "resolve_centroid_location is on but no market has a usable "
                "centroid; centroid_address will be empty."
            )
            return

        self._logger.info(
            f"Resolving centroid location for {len(points)} markets via "
            f"Overpass ({self.overpass_url})"
        )
        try:
            async with OverpassReverseGeocoder(
                url=self.overpass_url,
                fallback_urls=self.overpass_url_fallback,
                concurrency=self.geocode_concurrency,
            ) as geocoder:
                resolved = await geocoder.reverse_many(points.values())
        except Exception as exc:  # noqa: BLE001 - never lose a layout over a label
            self._logger.warning(
                f"Centroid location resolution failed against "
                f"{self.overpass_url} ({exc}); every centroid_address will "
                f"be empty."
            )
            return

        approximate = 0
        unresolved = 0
        for cid, point in points.items():
            result = resolved.get(point)
            if result is None or result.formatted is None:
                unresolved += 1
                continue
            self._centroid_locations[cid] = result
            if result.degraded:
                approximate += 1

        if unresolved or approximate:
            self._logger.warning(
                f"centroid_address: {unresolved}/{len(points)} markets "
                f"unresolved, {approximate} approximate (no addressed "
                f"feature near the centroid)"
            )
        else:
            self._logger.info(
                f"centroid_address: all {len(points)} market centroids "
                f"resolved to a street address"
            )

    def _add_centroid_location_columns(self, df: pd.DataFrame):
        """Add the centroid's street and administrative context to `df`.

        Emits `centroid_address` (the one-line label, e.g.
        ``"1234 Mundy Mill Road, Oakwood, GA"``) alongside the parts that
        compose it — `centroid_city`, `centroid_state`, `centroid_county`
        and `centroid_postcode` — so a caller can group by city or state
        without parsing the string. The prefix keeps them clear of any
        `city`/`state_code` the source stores already carry.

        No-op while `resolve_centroid_location` is off: the columns are
        absent rather than empty. Markets that stayed unresolved, and
        outlier rows, map to None instead of raising.

        Args:
            df: The frame to annotate, carrying the cluster id column.
        """
        if not self.resolve_centroid_location:
            return
        for column, attribute in (
            ('centroid_address', 'formatted'),
            ('centroid_city', 'city'),
            ('centroid_state', 'state'),
            ('centroid_county', 'county'),
            ('centroid_postcode', 'postcode'),
        ):
            df[column] = df[self._cluster_id].map(
                lambda cid, attribute=attribute: getattr(
                    self._centroid_locations.get(cid), attribute, None
                )
            )

    # ------------------------------------------------------------------
    #  OSMnx-based refinement
    # ------------------------------------------------------------------


    def _build_osmnx_graph_for_point(self, lat: float, lon: float) -> nx.MultiDiGraph:
        """
        Build a local OSMnx graph for the point (lat, lon) + self.network_type.
        """
        # For example:
        G = ox.graph_from_point(
            (lat, lon),
            dist=50000,
            network_type=self.network_type,
            simplify=True,
            custom_filter=self.custom_filter
        )
        return G

    def _build_osmnx_graph_for_bbox(self, north, south, east, west) -> nx.MultiDiGraph:
        """
        Build a local OSMnx graph for the bounding box + self.network_type.
        """
        # For example:
        buffer = 0.005  # Degrees (~0.5 km buffer)
        bbox = (north + buffer, south - buffer, east + buffer, west - buffer)
        print('BOX > ', bbox)
        G = ox.graph_from_bbox(
            bbox=bbox,
            network_type=self.network_type,
            # simplify=True,
            # retain_all=True,
            # truncate_by_edge=True,
            # custom_filter=self.custom_filter
        )
        ox.plot_graph(G)
        return G

    def _find_borderline_stores(self):
        """Second assignment pass: move distant stores to a closer market.

        Re-evaluates every store farther than ``max_cluster_distance *
        reassignment_threshold_factor`` from its market centroid, in two
        tiers that mirror the shared orphan-absorption policy:

        * Misassigned stores (beyond ``max_cluster_distance`` — they do not
          legally belong to their market, e.g. a store 100+ miles from its
          centroid while another market sits 20 miles away):
          ``max_cluster_size`` is SOFT and ``max_assign_distance`` is HARD.
          The nearest market absorbs the store even when full, flagging it
          as outlier.
        * Borderline stores (between the threshold and
          ``max_cluster_distance``): the move is only an optimization, so
          the target must have spare capacity (below the 20% reassignment
          buffer), lie within ``max_cluster_distance``, and be at least 5
          miles closer.

        Partition isolation and standalone markets are respected in both
        tiers; cluster sizes are tracked incrementally so one move never
        hides capacity from the next.

        The sweep is repeated up to ``reassignment_passes`` times (stopping
        as soon as a pass moves nothing): every move shifts the centroid of
        both the donor and the receiver, so a store can only become
        re-assignable once a previous move reshaped the market next to it.
        """
        total_reassigned = 0

        for _ in range(max(1, self.reassignment_passes)):
            moved = self._reassign_borderline_pass()
            total_reassigned += moved
            if moved == 0:
                break
            # Both markets changed shape: refresh the geometry so the next
            # sweep decides on the new centroids, not the stale ones.
            self._recompute_cluster_centroids()
            self._add_cluster_centroids_to_result(self._data)
            self._add_distance_to_center_column(self._data)

        if total_reassigned > 0:
            self._logger.info(
                f"Re-evaluated and reassigned {total_reassigned} distant stores to closer markets"
            )
            # Cluster composition changed: FTE metrics must follow
            self._recalculate_cluster_ftes_after_reassignment()
            self._add_distance_to_center_column(self._data)

    def _split_incoherent_markets(self) -> int:
        """Split markets that cover two cities instead of one.

        Splits are otherwise triggered by SIZE alone, so a market holding two
        dense nuclei 125 miles apart never splits while it fits the capacity
        gate — and no assignment rule can repair a store inside it, because
        the store is either far from its centre or surrounded by another
        market's stores whichever way it is assigned.

        ``max_markets`` is a fixed count, so a split needs a slot: the
        smallest market whose stores can all be handed to a neighbour is
        dissolved first, exactly as ``_balance_market_sizes`` does when a
        market outgrows its ceiling. The market count never changes.

        Returns:
            The number of markets split.
        """
        if (
            not self.split_incoherent_markets
            or self.max_markets is None
            or self._data.empty
        ):
            return 0

        partition = self._partition_mask(self._data)
        guard = self._move_distance_guard
        split = 0
        # A market this pass just created must never become the next donor:
        # dissolving it feeds its stores straight back into the market being
        # split (the split target is exempt from the ceiling), the two-nucleus
        # shape returns, and the pass mints new ids until the loop bound stops
        # it — the cycle _balance_market_sizes used to have.
        created: set = set()
        best_separation: Optional[int] = None
        stalled = 0

        for _ in range(int(self.max_markets)):
            assigned = self._data[self._data[self._cluster_id] != -1]
            sizes = assigned.groupby(self._cluster_id).size()
            sizes = sizes[~sizes.index.isin(self._standalone_clusters)]
            if len(sizes) < 2:
                break

            worst, worst_separation = None, 0.0
            for cid in sizes.index:
                separation = self._market_incoherence(
                    assigned[assigned[self._cluster_id] == cid]
                )
                if separation > worst_separation:
                    worst, worst_separation = cid, separation
            if worst is None or worst_separation <= self.market_nucleus_separation:
                break

            # Each round must leave the worst market less split than the last.
            # Ratcheting on the BEST separation seen makes any cycle — of any
            # period — stop counting as progress.
            best_separation, stalled = self._rebalance_stall_state(
                int(worst_separation), best_separation, stalled
            )
            if stalled >= 3:
                self._logger.warning(
                    "Incoherence split stopped after %s split(s): the worst "
                    "market still covers nuclei %.0f miles apart and further "
                    "splits do not improve it.",
                    split, worst_separation,
                )
                break

            # Free a slot: the smallest market that can hand every store to a
            # neighbour near it. The market about to be split is exempt from
            # the ceiling, since it is halved immediately afterwards.
            donors = sizes[(sizes.index != worst) & (~sizes.index.isin(created))]
            donors = donors.sort_values()
            moves, donor = None, None
            for reach in (guard, self.max_cluster_distance or float('inf')):
                for candidate in donors.index:
                    moves = self._plan_market_dissolution(
                        candidate, assigned, sizes, partition, reach,
                        split_target=worst,
                    )
                    if moves is not None:
                        donor = candidate
                        break
                if moves is not None:
                    break
            if moves is None:
                self._logger.warning(
                    "Market %s covers two cities %.0f miles apart but no small "
                    "market can free a slot to split it.",
                    worst, worst_separation,
                )
                break

            for idx, target in moves.items():
                self._data.at[idx, self._cluster_id] = target
                if target == -1:
                    self._data.at[idx, self._cluster_name] = 'Outlier'
                    self._outlier_stores.add(idx)
            self._anchored_centroids.pop(donor, None)
            self._cluster_fte_info.pop(donor, None)
            self._logger.info(
                "Dissolved market %s (%s stores) to split market %s, which "
                "covers two nuclei %.0f miles apart",
                donor, len(moves), worst, worst_separation,
            )
            new_cid = self._split_market(
                self._data, worst,
                reason=f"two nuclei {worst_separation:.0f} miles apart",
            )
            created.add(worst)
            if new_cid is not None:
                created.add(new_cid)
            split += 1
            self._recompute_cluster_centroids()

        if split:
            self._logger.info(
                "Split %s market(s) that covered two cities rather than one",
                split,
            )
        return split

    def _market_nuclei(self, members: pd.DataFrame) -> List[Tuple[float, float]]:
        """Dense nuclei of a market: the cities it actually covers.

        A nucleus is a store with at least ``market_nucleus_min_stores``
        members within ``market_nucleus_radius``. Nuclei are taken by
        decreasing density and kept apart by twice that radius, so one metro
        with several lobes counts once and a handful of stragglers counts not
        at all.

        Args:
            members: Stores of one market.

        Returns:
            ``(lat, lon)`` of each nucleus, densest first.
        """
        n = len(members)
        if n < self.market_nucleus_min_stores:
            return []

        lat = members['latitude'].to_numpy(dtype=float)
        lon = members['longitude'].to_numpy(dtype=float)
        rad = np.radians(np.column_stack([lat, lon]))
        dlat = rad[:, 0][:, None] - rad[:, 0][None, :]
        dlon = rad[:, 1][:, None] - rad[:, 1][None, :]
        cos_lat = np.cos(rad[:, 0])
        arc = np.sin(dlat / 2.0) ** 2 + (
            cos_lat[:, None] * cos_lat[None, :] * np.sin(dlon / 2.0) ** 2
        )
        distances = radians_to_miles(2.0 * np.arcsin(np.sqrt(np.clip(arc, 0.0, 1.0))))

        density = (distances <= self.market_nucleus_radius).sum(axis=1)
        nuclei: List[int] = []
        for i in np.argsort(-density):
            if density[i] < self.market_nucleus_min_stores:
                break
            if any(distances[i][j] <= 2.0 * self.market_nucleus_radius for j in nuclei):
                continue
            nuclei.append(int(i))
        return [(float(lat[i]), float(lon[i])) for i in nuclei]

    def _market_incoherence(self, members: pd.DataFrame) -> float:
        """Miles between the two farthest nuclei of a market.

        Zero when the market covers a single city — which is what a market is
        supposed to be. A large value means the market is really two cities
        stitched together, and no assignment rule can fix a store inside it:
        the store is either far from its centre or surrounded by another
        market's stores, whichever way it is assigned.

        Args:
            members: Stores of one market.

        Returns:
            The largest separation between two nuclei, or 0.0 with fewer
            than two.
        """
        nuclei = self._market_nuclei(members)
        if len(nuclei) < 2:
            return 0.0
        return max(
            self._haversine_miles(a[0], a[1], b[0], b[1])
            for a in nuclei
            for b in nuclei
        )

    def _neighbourhood_repair_pass(self, max_rounds: int = 4) -> int:
        """Move stores whose neighbourhood belongs to another market.

        Every other rule here assigns by distance to a centre, and a centre
        cannot represent a multi-polar territory: a store can be nearest to
        its OWN centroid — correctly assigned under every distance rule in
        this component — while the stores all around it belong to someone
        else. That is what "you cross another market to reach it" means, and
        no amount of centroid arithmetic detects it.

        So each store looks at its ``neighbourhood_k`` nearest neighbours: if
        a strict majority of them belong to one other market, and that market
        has a free slot, it follows them. Worst-placed stores go first, and
        the sweep repeats until nothing moves.

        Args:
            max_rounds: Safety bound; convergence normally happens sooner.

        Returns:
            The number of stores relocated.
        """
        if not self.neighbourhood_repair or self._data.empty:
            return 0

        assigned = self._data[self._data[self._cluster_id] != -1]
        # Sub-cluster rows (FEAT-241) are exempt from this pass: they carry
        # their own centerpoint and never follow a neighbourhood majority.
        # Excluded from the candidate pool (and its neighbour graph), but
        # NOT from the headcount used for capacity checks below.
        candidates = assigned
        if 'is_subcluster' in assigned.columns:
            candidates = assigned[~assigned['is_subcluster']]
        if len(candidates) <= self.neighbourhood_k:
            return 0

        idx = candidates.index.to_numpy()
        lat = candidates['latitude'].to_numpy(dtype=float)
        lon = candidates['longitude'].to_numpy(dtype=float)
        coords = np.radians(np.column_stack([lat, lon]))
        tree = BallTree(coords, leaf_size=40, metric='haversine')
        k = min(self.neighbourhood_k + 1, len(idx))
        neighbours = tree.query(coords, k=k, return_distance=False)[:, 1:]

        partition = self._partition_mask(self._data)
        total = 0
        for _ in range(max(1, max_rounds)):
            markets = self._data.loc[idx, self._cluster_id].to_numpy()
            # Full headcount (including sub-cluster rows) for capacity
            # checks — they count toward the market even though they
            # cannot be moved by this pass.
            sizes = self._data[
                self._data[self._cluster_id] != -1
            ].groupby(self._cluster_id).size().to_dict()
            # How badly placed each store is decides who moves first
            centroid_distance = np.array([
                self._haversine_miles(
                    lat[i], lon[i],
                    *self._cluster_centroids.get(
                        markets[i], {'centroid_lat': lat[i], 'centroid_lon': lon[i]}
                    ).values()
                )
                for i in range(len(idx))
            ])
            moved = 0
            for i in np.argsort(-centroid_distance):
                own = markets[i]
                if own in self._standalone_clusters:
                    continue
                labels, counts = np.unique(markets[neighbours[i]], return_counts=True)
                dominant = labels[counts.argmax()]
                if dominant == own or dominant == -1:
                    continue
                if counts.max() * 2 <= len(neighbours[i]):
                    continue  # no strict majority: the border is genuine
                if dominant in self._standalone_clusters:
                    continue
                if partition is not None and (
                    bool(partition.loc[idx[i]])
                    != self._cluster_partition.get(dominant, False)
                ):
                    continue
                if sizes.get(dominant, 0) >= self._capacity_for(dominant):
                    continue
                # A market that drops below min_cluster_size stops justifying
                # a rep, so a move that is good for one store can be bad for
                # the layout. Markets already under the floor keep what they
                # have rather than bleeding further.
                if sizes.get(own, 0) <= max(1, int(self.min_cluster_size)):
                    continue
                sizes[dominant] = sizes.get(dominant, 0) + 1
                sizes[own] = sizes.get(own, 0) - 1
                markets[i] = dominant
                self._data.at[idx[i], self._cluster_id] = dominant
                moved += 1
            total += moved
            if moved == 0:
                break
            self._recompute_cluster_centroids()

        if total:
            self._logger.info(
                "Neighbourhood repair moved %s store(s) into the market that "
                "owns the ground around them", total,
            )
        return total

    def _repair_assignments(self, max_rounds: int = 3) -> int:
        """Re-check every assignment against the SETTLED layout.

        The assignment passes run early: after them, dissolution,
        reconciliation, orphan handling and rescue all move stores, and every
        move shifts a centroid. So the decisions that placed each store were
        taken against geometry that no longer holds — which is how a store
        ends up 74 miles from its market while three markets with room sit
        closer to it.

        Runs the borderline pass and the ejection chain until nothing moves,
        so on an already settled layout this is a no-op rather than a source
        of churn.

        Args:
            max_rounds: Safety bound; convergence normally happens sooner.

        Returns:
            The number of stores relocated.
        """
        if not self.repair_assignments or self._data.empty:
            return 0

        total = 0
        for _ in range(max(1, max_rounds)):
            before = self._data[self._cluster_id].copy()
            self._find_borderline_stores()
            self._ejection_chain_pass()
            self._recompute_cluster_centroids()
            changed = int((before != self._data[self._cluster_id]).sum())
            total += changed
            if changed == 0:
                break

        if total:
            self._add_cluster_centroids_to_result(self._data)
            self._add_distance_to_center_column(self._data)
            self._logger.info(
                "Repair pass relocated %s store(s) once the layout had "
                "settled", total,
            )
        return total

    def _ejection_chain_pass(self, min_gain: float = 5.0) -> int:
        """Place stranded stores by making a full market hand one of its own away.

        A store whose nearest market is at capacity stays stranded no matter
        how close that market is — the assignment passes can only move it into
        a market with a free slot. So instead of growing the full market, ask
        it to give up the member that gains most by leaving: the store joins,
        one of its members moves to a neighbour that suits it better, and the
        full market keeps exactly the size it had.

        Every link must strictly improve the moved store's distance to its
        market centre, so total travel falls monotonically and the chain
        cannot cycle. The receiving gate is hard at every link, partitions and
        standalone markets are respected, and a market is never emptied.

        FEAT-247: among a store's own gainful (``gain >= min_gain``)
        candidate targets, the receiver is ranked by state-affinity score
        first, distance-gain second — the strict-improvement eligibility
        bar (``gain >= min_gain``) is unchanged, only the priority among
        already-eligible candidates changes.

        Args:
            min_gain: Miles a link must save to be worth making.

        Returns:
            The number of stores relocated (each chain moves two).
        """
        if not self.ejection_chain or self._data.empty:
            return 0
        self._reset_state_score_cache()

        assigned = self._data[self._data[self._cluster_id] != -1]
        if assigned.empty:
            return 0

        centroids = {
            cid: (info['centroid_lat'], info['centroid_lon'])
            for cid, info in self._cluster_centroids.items()
            if cid not in self._standalone_clusters
        }
        if len(centroids) < 2:
            return 0
        # Headcount for capacity checks includes sub-cluster rows (FEAT-241:
        # they count toward the market even though they cannot be ejected).
        sizes = assigned.groupby(self._cluster_id).size().to_dict()
        # Only non-sub-cluster stores can initiate or be picked for an
        # ejection: they carry their own centerpoint and are exempt from
        # this chain.
        movable = assigned
        if 'is_subcluster' in assigned.columns:
            movable = assigned[~assigned['is_subcluster']]
        partition = self._partition_mask(self._data)

        def part_of(idx: Any) -> bool:
            return bool(partition.loc[idx]) if partition is not None else False

        def distance_to(idx: Any, cid: Any) -> float:
            lat = float(self._data.at[idx, 'latitude'])
            lon = float(self._data.at[idx, 'longitude'])
            return self._haversine_miles(lat, lon, *centroids[cid])

        def entity_state_of(idx: Any) -> Any:
            if self.state_column not in self._data.columns:
                return None
            return self._data.at[idx, self.state_column]

        # Stranded stores first: the ones with most to gain from a market that
        # is currently out of reach because it is full.
        wishes = []
        for idx in movable.index:
            cid = self._data.at[idx, self._cluster_id]
            if cid in self._standalone_clusters or cid not in centroids:
                continue
            own = distance_to(idx, cid)
            own_state = entity_state_of(idx)
            own_targets = [
                (other, own - distance_to(idx, other))
                for other in centroids
                if other != cid
                and self._cluster_partition.get(other, False) == part_of(idx)
            ]
            own_targets = [(other, gain) for other, gain in own_targets if gain >= min_gain]
            if not own_targets:
                continue
            max_gain_distance = max(distance_to(idx, other) for other, _ in own_targets)
            for other, gain in own_targets:
                score = self._state_affinity_score(
                    own_state, other, distance_to(idx, other), max_gain_distance
                )
                wishes.append((score, gain, idx, cid, other))
        wishes.sort(key=lambda w: (-w[0], -w[1], str(w[2])))

        moved = 0
        for score, gain, idx, cid, target in wishes:
            if self._data.at[idx, self._cluster_id] != cid:
                continue  # already relocated by an earlier chain
            if sizes.get(target, 0) < self._capacity_for(target):
                continue  # it has room: the borderline pass owns this case
            if sizes.get(cid, 0) <= 1:
                continue  # never empty a market

            # Who inside the full market is best off leaving? (sub-cluster
            # rows excluded: they are exempt from ejection.) Among a
            # member's own gainful destinations, ranked by state-affinity
            # score first, distance-gain second (FEAT-247) — same priority
            # rule as the outer wish list.
            member_mask = self._data[self._cluster_id] == target
            if 'is_subcluster' in self._data.columns:
                member_mask &= ~self._data['is_subcluster']
            members = self._data.index[member_mask]
            best = None
            for member in members:
                here = distance_to(member, target)
                member_state = entity_state_of(member)
                member_targets = [
                    (nxt, here - distance_to(member, nxt))
                    for nxt in centroids
                    if not (nxt in (target, cid) and nxt != cid)
                    and self._cluster_partition.get(nxt, False) == part_of(member)
                    and sizes.get(nxt, 0) < self._capacity_for(nxt)
                ]
                member_targets = [
                    (nxt, member_gain) for nxt, member_gain in member_targets
                    if member_gain >= min_gain
                ]
                if not member_targets:
                    continue
                max_member_distance = max(
                    distance_to(member, nxt) for nxt, _ in member_targets
                )
                for nxt, member_gain in member_targets:
                    member_score = self._state_affinity_score(
                        member_state, nxt, distance_to(member, nxt),
                        max_member_distance,
                    )
                    if (
                        best is None
                        or member_score > best[0]
                        or (member_score == best[0] and member_gain > best[1])
                    ):
                        best = (member_score, member_gain, member, nxt)
            if best is None:
                continue

            member_score, member_gain, member, nxt = best
            self._data.at[member, self._cluster_id] = nxt
            self._data.at[idx, self._cluster_id] = target
            self._data.at[idx, 'state_affinity_score'] = score
            self._data.at[member, 'state_affinity_score'] = member_score
            sizes[nxt] = sizes.get(nxt, 0) + 1
            sizes[cid] = sizes.get(cid, 0) - 1
            moved += 2
            self._logger.debug(
                "Ejection chain: store %s joins market %s (saves %.1f mi); "
                "market %s hands %s to market %s (saves %.1f mi)",
                idx, target, gain, target, member, nxt, member_gain,
            )

        if moved:
            self._logger.info(
                "Ejection chain relocated %s store(s) into markets that were "
                "full, without growing any of them", moved,
            )
        return moved

    def _borderline_target_allowed(
        self, current_size: int, gain: float, cid: Any
    ) -> bool:
        """Can a market receive a borderline (optimisation) move?

        The 20% reassignment buffer keeps a reserve so an optimisation does
        not push a market to its limit. But the buffer is computed from
        ``max_cluster_size`` and subtracted from ``_capacity_for``, so when a
        receiving gate sits above ``max_cluster_size`` the threshold lands on
        the very size the layout drives every market to, and markets with
        free slots refuse every move.

        So a large enough ``gain`` overrides the buffer. The receiving gate
        itself stays hard: no optimisation ever grows a market past
        ``_capacity_for``.

        Args:
            current_size: Stores the target holds right now.
            gain: Miles the store would save by moving there.
            cid: Target market id (its hours may tighten the gate).

        Returns:
            True when the target may take the store.
        """
        capacity = self._capacity_for(cid)
        if current_size >= capacity:
            return False  # the receiving gate is hard, always

        buffer = int(self.max_cluster_size * self.max_reassignment_percentage)
        if current_size < capacity - buffer:
            return True
        return bool(
            self.reassign_overflow_gain
            and gain >= self.reassign_overflow_gain
        )

    def _reassign_borderline_pass(self) -> int:
        """Run a single sweep of the second assignment pass.

        FEAT-247: the receiving market in both tiers below is chosen by
        state-affinity score, not pure distance — see
        ``_state_affinity_score``.

        Returns:
            The number of stores moved to a closer market.
        """
        self._reset_state_score_cache()
        # The trigger must not scale away with a generous max_cluster_distance:
        # with a 300-mile radius the derived threshold (150 miles) silently
        # disables the pass, leaving a store 95 miles from its market while
        # another market sits 30 miles away. A store farther from its centroid
        # than the distance at which it would have been assigned in the first
        # place always deserves a second look.
        assign_distance = self._max_force_assign_distance or float('inf')
        reassignment_threshold = min(
            self.max_cluster_distance * self.reassignment_threshold_factor,
            assign_distance,
        )
        reassigned_count = 0
        # The 20% buffer now lives in _borderline_target_allowed, which also
        # decides when a large saving may spend a market's remaining slots.
        min_improvement = 5.0  # miles a move must gain to be worth it

        partition = self._partition_mask(self._data)
        # Track current cluster sizes
        cluster_sizes = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size().to_dict()
        active_markets = set(cluster_sizes)

        # Group stores by current market
        for current_cid in self._data[self._cluster_id].unique():
            if current_cid == -1:
                continue
            if current_cid in self._standalone_clusters:
                continue  # Standalone markets are frozen

            current_market_stores = self._data[self._data[self._cluster_id] == current_cid].copy()

            for idx, store in current_market_stores.iterrows():
                # Sub-cluster rows (FEAT-241) carry their own centerpoint
                # and are exempt from the market's borderline reassignment.
                if bool(store.get('is_subcluster', False)):
                    continue

                store_distance = store.get('distance_to_center', 0)

                # Only re-evaluate stores beyond the threshold
                if not store_distance > reassignment_threshold:
                    continue

                store_lat = store['latitude']
                store_lon = store['longitude']

                candidates = {
                    other_cid: (
                        centroid['centroid_lat'], centroid['centroid_lon']
                    )
                    for other_cid, centroid in self._cluster_centroids.items()
                    if other_cid != current_cid
                    and other_cid in active_markets
                    and other_cid not in self._standalone_clusters
                    and (
                        partition is None
                        or self._cluster_partition.get(other_cid, False)
                        == bool(partition.loc[idx])
                    )
                }

                best_market = None
                min_distance = float('inf')
                overfilled = False
                entity_state = (
                    store[self.state_column]
                    if self.state_column in self._data.columns else None
                )

                if store_distance > self.max_cluster_distance:
                    # Misassigned: the store does not belong to its market.
                    # First choice is the best-scoring market within
                    # max_assign_distance — the size cap is soft here.
                    # If nothing is that close, the store is NOT left where
                    # it is: any strictly closer market beats a market it
                    # never belonged to (a store 100 miles out does not get
                    # to stay there just because the best alternative is 40
                    # miles away instead of 30).
                    for reach in (self._max_force_assign_distance, float('inf')):
                        choice = self._nearest_absorbing_market(
                            store_lat, store_lon, candidates, cluster_sizes,
                            reach, entity_state=entity_state,
                        )
                        if choice is None:
                            continue
                        target, distance, overfilled = choice
                        if distance < (store_distance - min_improvement):
                            best_market = target
                            min_distance = distance
                            break
                else:
                    # Borderline optimization: only markets with spare room.
                    # Collect every feasible candidate first (hard guards
                    # below unchanged), then the WINNER is the
                    # highest-scoring one (FEAT-247) rather than pure
                    # nearest distance.
                    feasible: List[Tuple[Any, float]] = []
                    for other_cid, (center_lat, center_lon) in candidates.items():
                        # Check if target market would exceed size limit
                        # (never blocks when the cap is not enforced)
                        current_size = cluster_sizes.get(other_cid, 0)

                        distance = self._haversine_miles(store_lat, store_lon, center_lat, center_lon)
                        # A market at its layout size still has slots up to the
                        # receiving gate; a large enough saving may use them
                        # rather than strand the store.
                        if not self._borderline_target_allowed(
                            current_size, store_distance - distance, other_cid
                        ):
                            continue

                        # Only reassign if significantly closer (at least 5 miles difference)
                        # and within max_cluster_distance
                        if (
                            distance <= self.max_cluster_distance and distance < (store_distance - min_improvement)  # noqa
                        ):
                            feasible.append((other_cid, distance))

                    if feasible:
                        max_feasible_distance = max(d for _, d in feasible)
                        best_cid, best_distance, best_score = None, None, None
                        for other_cid, distance in feasible:
                            score = self._state_affinity_score(
                                entity_state, other_cid, distance,
                                max_feasible_distance,
                            )
                            if (
                                best_score is None
                                or score > best_score
                                or (score == best_score and distance < best_distance)
                                or (
                                    score == best_score and distance == best_distance
                                    and other_cid < best_cid
                                )
                            ):
                                best_cid, best_distance, best_score = (
                                    other_cid, distance, score,
                                )
                        best_market = best_cid
                        min_distance = best_distance

                # Reassign if we found a better market
                if best_market is not None:
                    if cluster_sizes.get(current_cid, 0) <= 1:
                        # Never empty a market: the exact ``max_markets``
                        # count outranks a single store's proximity.
                        continue

                    self._data.at[idx, self._cluster_id] = best_market
                    self._data.at[idx, self._cluster_name] = f"Market-{best_market}"
                    self._data.at[idx, 'ghost_id'] = f"Ghost-{best_market}-1"

                    # Update centroid coordinates
                    self._data.at[idx, 'centroid_lat'] = self._cluster_centroids[best_market]['centroid_lat']
                    self._data.at[idx, 'centroid_lon'] = self._cluster_centroids[best_market]['centroid_lon']
                    self._data.at[idx, 'state_affinity_score'] = self._state_affinity_score(
                        entity_state, best_market, min_distance,
                        max(min_distance, self.max_cluster_distance),
                    )

                    cluster_sizes[current_cid] = cluster_sizes.get(current_cid, 1) - 1
                    cluster_sizes[best_market] = cluster_sizes.get(best_market, 0) + 1

                    if overfilled or min_distance > self.max_cluster_distance:
                        self._outlier_stores.add(idx)
                        if overfilled:
                            self._logger.warning(
                                "Store %s overfills market %s (%.1f miles): "
                                "every market within %s miles is at "
                                "max_cluster_size=%s.",
                                store.get('store_id', idx), best_market,
                                min_distance, self._max_force_assign_distance,
                                self.max_cluster_size,
                            )
                    else:
                        self._outlier_stores.discard(idx)

                    reassigned_count += 1

                    self._logger.info(
                        f"Reassigned store {store.get('store_id', idx)} from Market-{current_cid} "
                        f"(dist: {store_distance:.1f}mi) to Market-{best_market} (dist: {min_distance:.1f}mi)"
                    )

        return reassigned_count

    def _recalculate_cluster_ftes_after_reassignment(self):
        """
        Recalculate FTE info for all clusters after store reassignment.

        This ensures that after stores are reassigned to different markets,
        the FTE calculations are updated to reflect the new cluster compositions.
        """
        if not self.use_fte_constraints and self.fte_calculator is None:
            return

        for cid in self._data[self._cluster_id].unique():
            if cid == -1:  # Skip outliers
                continue

            cluster_df = self._data[self._data[self._cluster_id] == cid]
            if cluster_df.empty:
                continue

            # Recalculate FTE for this cluster
            _ = self._get_num_ghosts_for_cluster(cid, cluster_df)

    # ------------------------------------------------------------------
    #  Ghost Employees
    # ------------------------------------------------------------------
    def _haversine_distance_km(self, lat1, lon1, lat2, lon2):
        """
        Calculate the geodesic distance between two points in kilometers using Geopy.
        """
        return geodesic((lat1, lon1), (lat2, lon2)).kilometers

    def _market_base(
        self, cid: Any, df: pd.DataFrame
    ) -> Optional[Tuple[float, float]]:
        """Where the market's field rep is based, as a real store location.

        The plain mean of a market's members is a statistical artefact: when a
        market has two poles (say a metro plus a mid-sized city) it lands in
        the empty country between them, and every reachability decision taken
        from there is meaningless. So the base is chosen among the market's
        OWN stores, per ``ghost_placement``:

        - ``median``: minimises the sum of distances to all members
          (1-median) — the cheapest base to run a month of visits from.
        - ``minimax``: minimises the largest distance (1-center) — shortest
          worst leg, but it drifts towards geometric middle ground.
        - ``centroid``: legacy plain mean (not a store location).

        Args:
            cid: Market id, used only for logging.
            df: Stores of the whole layout, or of this market alone.

        Returns:
            ``(lat, lon)`` of the base, or ``None`` when the market is empty.
        """
        members = df[df[self._cluster_id] == cid] if self._cluster_id in df else df
        if members.empty:
            return None

        # Standalone markets can span two distant poles (e.g. Seattle's
        # Puget Sound core + Alaska stores).  The 1-median over ALL members
        # gets dragged by the far pole.  When an anchor (the dense core)
        # was stored for this market, restrict the base computation to
        # members within density_radius of the anchor — the base should
        # serve the metro the market actually concentrates in, not minimise
        # travel to a satellite 1 400 miles away.
        if cid in self._standalone_clusters:
            anchor = self._anchored_centroids.get(cid)
            if anchor is not None:
                a_lat_r = np.radians(anchor[0])
                a_lon_r = np.radians(anchor[1])
                m_lat_r = np.radians(
                    members['latitude'].to_numpy(dtype=float)
                )
                m_lon_r = np.radians(
                    members['longitude'].to_numpy(dtype=float)
                )
                dlat = m_lat_r - a_lat_r
                dlon = m_lon_r - a_lon_r
                arc = np.sin(dlat / 2.0) ** 2 + (
                    np.cos(a_lat_r) * np.cos(m_lat_r)
                    * np.sin(dlon / 2.0) ** 2
                )
                dist_to_anchor = radians_to_miles(
                    2.0 * np.arcsin(np.sqrt(np.clip(arc, 0.0, 1.0)))
                )
                core_mask = dist_to_anchor <= self.density_radius
                if core_mask.sum() >= 2:
                    members = members[core_mask]

        lat = members['latitude'].to_numpy(dtype=float)
        lon = members['longitude'].to_numpy(dtype=float)
        if self.ghost_placement == 'centroid' or len(members) == 1:
            return float(lat.mean()), float(lon.mean())

        # Pairwise haversine over the market's own members (markets are
        # capped at max_cluster_size, so this stays small)
        rad = np.radians(np.column_stack([lat, lon]))
        dlat = rad[:, 0][:, None] - rad[:, 0][None, :]
        dlon = rad[:, 1][:, None] - rad[:, 1][None, :]
        cos_lat = np.cos(rad[:, 0])
        arc = np.sin(dlat / 2.0) ** 2 + (
            cos_lat[:, None] * cos_lat[None, :] * np.sin(dlon / 2.0) ** 2
        )
        distances = radians_to_miles(2.0 * np.arcsin(np.sqrt(np.clip(arc, 0.0, 1.0))))

        # A base must be somewhere the market actually has presence. Without
        # this filter the 1-median of a multi-polar market minimises total
        # travel by sitting in the empty middle between the poles, which can
        # be a town holding two of its stores.
        candidates = np.arange(len(members))
        if self.base_min_density > 0:
            local = (distances <= self.base_density_radius).sum(axis=1)
            dense = np.flatnonzero(local >= self.base_min_density)
            if dense.size:
                candidates = dense

        if self.ghost_placement == 'minimax':
            best = int(candidates[distances[np.ix_(candidates)].max(axis=1).argmin()])
        else:
            best = int(candidates[distances[np.ix_(candidates)].sum(axis=1).argmin()])
        return float(lat[best]), float(lon[best])

    def _create_ghost_employees(self, cid, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Create ghost employees around each cluster's centroid.
        Uses 'fte' column if available, otherwise uses num_ghosts_per_cluster.
        Ensure no ghost is more than 5 km from the centroid.
        Spread ghosts within the cluster to maximize coverage.
        """
        ghosts = []
        cluster_rows = df[df[self._cluster_id] == cid]
        if cluster_rows.empty:
            return ghosts

        if len(cluster_rows) == 1:
            # Only one store in this cluster, no need for ghosts
            return ghosts

        # Base of this market: a real store location, not the plain mean —
        # the mean falls in empty country whenever a market has two poles,
        # and every reachability decision below is measured from here.
        lat_mean, lon_mean = self._market_base(cid, cluster_rows)

        max_offset_lat = 0.002  # ~5 km
        max_offset_lon = 0.002  # ~5 km at 40° latitude
        max_offset_miles = 50.0  # Maximum distance from centroid
        min_distance_km = 10.0  # Minimum distance between ghosts to prevent overlapping

        # Get number of ghost employees for this cluster
        num_ghosts = self._get_num_ghosts_for_cluster(cid, cluster_rows)

        for i in range(num_ghosts):
            if i == 0:
                # The first ghost IS the market's base. Placing it exactly
                # there (no random offset) is what makes the store-drop
                # decision in _filter_unreachable_stores reproducible AND
                # meaningful: it is measured from where the rep actually is.
                ghosts.append({
                    'ghost_id': f"Ghost-{cid}-1",
                    self._cluster_id: cid,
                    'latitude': lat_mean,
                    'longitude': lon_mean,
                })
                continue

            attempt = 0
            while True:
                # lat_offset = np.random.uniform(-max_offset_lat, max_offset_lat)
                # lon_offset = np.random.uniform(-max_offset_lon, max_offset_lon)

                # ghost_lat = lat_mean + lat_offset
                # ghost_lon = lon_mean + lon_offset

                # # Calculate distance to centroid using geodesic distance for precision
                # distance_km = self._haversine_distance_km(lat_mean, lon_mean, ghost_lat, ghost_lon)
                # if distance_km > 5.0:
                #     attempt += 1
                #     if attempt >= 100:
                #         self._logger.warning(
                #             f"Could not place ghost {i+1} within 5 km after 100 attempts in cluster {cid}."
                #         )
                #         break
                #     continue  # Exceeds maximum distance, retry

                # Generate a random point within a circle of radius 50 miles from the centroid
                angle = self._rng.uniform(0, 2 * np.pi)
                distance = self._rng.uniform(0, max_offset_miles)
                delta_lat = (distance * math.cos(angle)) / 69.0  # Approx. degrees per mile
                delta_lon = (distance * math.sin(angle)) / (69.0 * math.cos(math.radians(lat_mean)))

                ghost_lat = lat_mean + delta_lat
                ghost_lon = lon_mean + delta_lon

                # Ensure ghosts are not too close to each other
                too_close = False
                for existing_ghost in ghosts:
                    existing_distance = self._haversine_distance_km(
                        existing_ghost['latitude'],
                        existing_ghost['longitude'],
                        ghost_lat,
                        ghost_lon
                    )
                    if existing_distance < min_distance_km:
                        too_close = True
                        break
                if not too_close:
                    break  # Valid position found
                if too_close:
                    attempt += 1
                    if attempt >= 100:
                        self._logger.warning(
                            f"Ghost {i+1} in cluster {cid} is too close to existing ghosts after 100 attempts."
                        )
                        break
                    continue  # Ghost too close to existing, retry

                # Valid position found
                break

            ghost_id = f"Ghost-{cid}-{i+1}"
            ghost = {
                'ghost_id': ghost_id,
                self._cluster_id: cid,
                'latitude': ghost_lat,
                'longitude': ghost_lon
            }
            ghosts.append(ghost)

        return ghosts

    # ------------------------------------------------------------------
    #  Filter stores unreachable from any ghost
    # ------------------------------------------------------------------
    def _filter_unreachable_stores(
        self,
        cid: int,
        employees: List[Dict[str, Any]],
        cluster_stores: pd.DataFrame
    ) -> List[int]:
        """
        For each store in the given cluster's df_cluster, check if
        any of the provided employees is within ghost_distance_threshold miles.
        Return a list of indices that are unreachable.
        """
        unreachable_indices = []

        # If no employees for this cluster, everything is unreachable
        if not employees:
            return cluster_stores.index.tolist()

        if cid == -1 or len(cluster_stores) == 1:
            return []

        for idx, row in cluster_stores.iterrows():
            store_lat = row['latitude']
            store_lon = row['longitude']
            cluster_id = row['market_id']
            store_id = row['store_id']

            reachable = False
            for ghost in employees:
                g_lat = ghost['latitude']
                g_lon = ghost['longitude']
                distance_km = self._haversine_distance_km(store_lat, store_lon, g_lat, g_lon)
                dist = meters_to_miles(distance_km * 1000)
                if dist <= self.ghost_distance_threshold:
                    reachable = True
                    break
            if not reachable:
                unreachable_indices.append(idx)

        return unreachable_indices

    def _haversine_miles(self, lat1, lon1, lat2, lon2):
        """
        Simple haversine formula returning miles between two lat/lon points.
        Earth radius ~3959 miles.
        """
        R = 3959.0  # Earth radius in miles
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        return R * c

    def _nearest_osm_node(self, G: nx.MultiDiGraph, lat: float, lon: float) -> int:
        """
        Return the nearest node in graph G to (lat, lon).
        """
        node = ox_distance.nearest_nodes(G, X=[lon], Y=[lat])
        # node is usually an array or single value
        if isinstance(node, np.ndarray):
            return node[0]
        return node

    def _road_distance_miles(
        self, G: nx.MultiDiGraph,
        center_lat: float,
        center_lon: float,
        lat: float,
        lon: float
    ) -> Optional[float]:
        """
        Compute route distance in miles from node_center to (lat, lon) in G.
        If no path, return None.
        1) nearest node for center, nearest node for candidate
        2) shortest_path_length with weight='length'
        3) convert meters->miles
        If no path, return None
        """
        node_center = self._nearest_osm_node(G, center_lat, center_lon)
        node_target = self._nearest_osm_node(G, lat, lon)
        try:
            dist_m = nx.shortest_path_length(G, node_center, node_target, weight='length')
            dist_miles = dist_m * 0.000621371
            return dist_miles
        except nx.NetworkXNoPath:
            return None

    def _compute_distance_matrix(
        self,
        cluster_df: pd.DataFrame,
        G_local: nx.MultiDiGraph,
        depot_lat: float,
        depot_lon: float
    ) -> np.ndarray:
        """
        Computes the road-based distance matrix for the cluster.
        Includes the depot as the first node.
        """
        store_ids = cluster_df.index.tolist()
        all_coords = [(depot_lat, depot_lon)] + list(cluster_df[['latitude', 'longitude']].values)
        distance_matrix = np.zeros((len(all_coords), len(all_coords)), dtype=float)

        # Precompute nearest nodes
        nodes = ox_distance.nearest_nodes(
            G_local, X=[lon for lat, lon in all_coords], Y=[lat for lat, lon in all_coords]
        )

        for i in range(len(all_coords)):
            for j in range(len(all_coords)):
                if i == j:
                    distance_matrix[i][j] = 0
                else:
                    try:
                        dist_m = nx.shortest_path_length(G_local, nodes[i], nodes[j], weight='length')
                        dist_miles = dist_m * 0.000621371  # meters to miles
                        distance_matrix[i][j] = dist_miles
                    except nx.NetworkXNoPath:
                        distance_matrix[i][j] = np.inf  # No path exists

        return distance_matrix

    def _assign_routes_vrp(
        self,
        cluster_df: pd.DataFrame,
        G_local: nx.MultiDiGraph,
        depot_lat: float,
        depot_lon: float
    ) -> Dict[int, List[int]]:
        """
        Assigns stores in the cluster to ghost employees using VRP.
        Returns a dictionary where keys are ghost IDs and values are lists of store indices.
        """
        store_ids = cluster_df.index.tolist()

        # Get the number of vehicles (ghost employees) for this cluster
        cid = cluster_df[self._cluster_id].iloc[0] if not cluster_df.empty else 0
        num_vehicles = self._get_num_ghosts_for_cluster(cid, cluster_df)

        # Compute distance matrix with depot as first node
        distance_matrix = self._compute_distance_matrix(cluster_df, G_local, depot_lat, depot_lon)

        # Handle infinite distances by setting a large number
        distance_matrix[np.isinf(distance_matrix)] = 1e6

        # Create data model for VRP
        data = create_data_model(
            distance_matrix=distance_matrix.tolist(),  # OR-Tools requires lists
            num_vehicles=num_vehicles,
            depot=0,
            max_distance=self.daily_distance_cap,
            max_stores_per_vehicle=self.max_stores_per_day
        )

        # Solve VRP
        routes = solve_vrp(data)

        # Map routes to store indices (excluding depot)
        assignment = {}
        for vehicle_id, route in enumerate(routes):
            # Exclude depot (first node)
            assigned_store_indices = route[1:-1]  # Remove depot start and end
            assignment[vehicle_id] = [store_ids[idx - 1] for idx in assigned_store_indices]

        return assignment

    def _validate_clusters_by_vrp(self):
        """
        For each cluster, assign stores to ghost employees using VRP.
        Remove any stores that cannot be assigned within constraints.
        """
        df = self._data
        clusters = df[self._cluster_id].unique()

        for cid in clusters:
            if cid == -1:
                continue  # Skip outliers

            cluster_df = df[df[self._cluster_id] == cid]
            if cluster_df.empty:
                continue

            # Get number of ghost employees for this cluster
            num_ghosts = self._get_num_ghosts_for_cluster(cid, cluster_df)

            # FIXED: For small clusters, directly assign ghost_id without VRP
            if len(cluster_df) <= num_ghosts or num_ghosts == 1:
                # Simple round-robin assignment for small clusters
                for idx, (store_idx, _) in enumerate(cluster_df.iterrows()):
                    ghost_idx = (idx % num_ghosts) if num_ghosts > 0 else 0
                    ghost_id = f"Ghost-{cid}-{ghost_idx + 1}"
                    df.at[store_idx, 'ghost_id'] = ghost_id
                continue

            # For larger clusters, use VRP
            # 1) Compute bounding box with buffer
            lat_min = cluster_df['latitude'].min()
            lat_max = cluster_df['latitude'].max()
            lon_min = cluster_df['longitude'].min()
            lon_max = cluster_df['longitude'].max()

            buffer_deg = 0.1
            north = lat_max + buffer_deg
            south = lat_min - buffer_deg
            east = lon_max + buffer_deg
            west = lon_min - buffer_deg

            # 2) Build local OSMnx graph for the cluster
            G_local = self._build_osmnx_graph_for_bbox(north, south, east, west)

            # 3) Define depot (cluster centroid)
            centroid_lat = cluster_df['latitude'].mean()
            centroid_lon = cluster_df['longitude'].mean()

            # 4) Assign routes using VRP
            assignment = self._assign_routes_vrp(cluster_df, G_local, centroid_lat, centroid_lon)

            # 5) Assign ghost IDs to stores
            for vehicle_id, store_ids in assignment.items():
                ghost_id = f"Ghost-{cid}-{vehicle_id + 1}"
                df.loc[store_ids, 'ghost_id'] = ghost_id

            # 6) Identify unassigned stores (if any)
            assigned_store_ids = set()
            for route in assignment.values():
                assigned_store_ids.update(route)

            all_store_ids = set(cluster_df.index.tolist())
            unassigned_store_ids = all_store_ids - assigned_store_ids

            # FIXED: Assign remaining stores to first ghost if not assigned
            if unassigned_store_ids:
                self._logger.warning(
                    f"Cluster {cid}: {len(unassigned_store_ids)} stores not assigned by VRP, "
                    f"assigning to Ghost-{cid}-1"
                )
                for store_idx in unassigned_store_ids:
                    # Assign to first ghost as fallback
                    df.at[store_idx, 'ghost_id'] = f"Ghost-{cid}-1"

        # Update DataFrame with assignments
        self._data = df.copy()

        # Apply market labels again if needed
        self._apply_market_labels(self._data, self._data[self._cluster_id].values)

    def _reassign_rejected_stores(self):
        """
        Attempt to reassign rejected stores to existing clusters if within the borderline threshold.
        """
        if self._rejected.empty:
            return

        borderline_threshold = self.borderline_threshold
        to_remove = []
        df = self._rejected.copy()

        for idx, row in df.iterrows():
            # Find the nearest cluster centroid
            min_distance = np.inf
            assigned_cid = -1

            for cid in self._data[self._cluster_id].unique():
                if cid == -1:
                    continue
                centroid_lat = self._data[self._cluster_id == cid]['latitude'].mean()
                centroid_lon = self._data[self._cluster_id == cid]['longitude'].mean()
                distance = self._haversine_miles(centroid_lat, centroid_lon, row['latitude'], row['longitude'])
                if distance < min_distance:
                    min_distance = distance
                    assigned_cid = cid

            # Check if within the borderline threshold
            if min_distance <= self.max_cluster_distance * borderline_threshold:
                # Assign to this cluster
                self._data.at[idx, self._cluster_id] = assigned_cid
                self._data.at[idx, 'ghost_id'] = f"Ghost-{assigned_cid}-1"  # Assign to the first ghost for simplicity
                to_remove.append(idx)

        # Remove reassigned stores from rejected
        if to_remove:
            self._rejected.drop(index=to_remove, inplace=True)
            self._logger.info(
                f"Reassigned {len(to_remove)} rejected stores to existing clusters."
            )

    def _save_rejected_stores(self):
        """Save rejected stores to Excel file if file path is provided."""
        if self.rejected_stores_file and not self._rejected.empty:
            try:
                # Convert to absolute path if relative
                if isinstance(self.rejected_stores_file, str):
                    self.rejected_stores_file = self.rejected_stores_file.strip()
                    file_path = Path(self.rejected_stores_file)
                elif isinstance(self.rejected_store_file, Path):
                    file_path = self.rejected_stores_file
                if not file_path.is_absolute():
                    file_path = Path.cwd() / file_path

                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Save to Excel
                self._rejected.to_excel(file_path, index=False)

                self._logger.info(
                    f"Saved {len(self._rejected)} rejected stores to {file_path}"
                )
            except Exception as e:
                self._logger.error(
                    f"Failed to save rejected stores to {self.rejected_stores_file}: {e}"
                )
        elif self.rejected_stores_file and self._rejected.empty:
            self._logger.info(
                "No rejected stores to save - all stores were assigned to markets"
            )

    def _force_assign_all_rejected_stores(self):
        """
        Force assign all rejected stores to their nearest market cluster.
        This ensures no stores are left unassigned.
        """
        if self._rejected.empty:
            return

        self._logger.info(
            f"Force assigning {len(self._rejected)} rejected stores to nearest markets..."
        )

        # FEAT-248 TASK-205: this surface scores via _nearest_absorbing_market
        # below; reset once at the top (not per store in the loop, which
        # would defeat the cache).
        self._reset_state_score_cache()

        # Get all valid cluster centroids (excluding outliers)
        valid_clusters = self._data[self._data[self._cluster_id] != -1][self._cluster_id].unique()

        if len(valid_clusters) == 0:
            self._logger.warning("No valid clusters found for force assignment!")
            return

        # Track cluster sizes so max_cluster_size is honoured while assigning
        cluster_sizes = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size().to_dict()

        reassigned_stores = []
        still_rejected_indices = []  # Track stores that remain rejected

        # Exact-markets mode (max_markets set): distances are soft, so no
        # store may stay rejected only because it is far from every market.
        exact_mode = self.max_markets is not None
        max_assign_distance = (
            float('inf') if exact_mode else self._max_force_assign_distance
        )

        # Standalone markets are frozen: they never take in an orphan, no
        # matter how much room they have (a Wisconsin store must not land in
        # the Honolulu market just because it is the one below capacity).
        candidate_centroids = {
            cid: (
                self._cluster_centroids[cid]['centroid_lat'],
                self._cluster_centroids[cid]['centroid_lon'],
            )
            for cid in valid_clusters
            if cid in self._cluster_centroids
            and cid not in self._standalone_clusters
        }
        partition = self._partition_mask(self._data)

        for idx, row in self._rejected.iterrows():
            # Nearest market within the distance cap, preferring those with
            # room; the size cap is soft (a full market absorbs the orphan)
            # while the distance cap stays HARD — infinite in exact
            # max_markets mode, where no store may be left out.
            eligible = candidate_centroids
            if partition is not None and idx in partition.index:
                store_partition = bool(partition.loc[idx])
                eligible = {
                    cid: centroid
                    for cid, centroid in candidate_centroids.items()
                    if self._cluster_partition.get(cid, False) == store_partition
                }
            entity_state = (
                row[self.state_column]
                if self.state_column in self._rejected.columns else None
            )
            choice = self._nearest_absorbing_market(
                row['latitude'], row['longitude'],
                eligible, cluster_sizes,
                max_assign_distance,
                entity_state=entity_state,
            )
            if choice is not None:
                nearest_cluster, min_distance, overfilled = choice
                if overfilled:
                    self._logger.warning(
                        "No market with capacity near store %s; assigning it "
                        "to market %s (%.1f miles) beyond max_cluster_size=%s.",
                        row.get('store_id', idx),
                        nearest_cluster,
                        min_distance,
                        self.max_cluster_size,
                    )

            if choice is not None:
                # Add store to main dataframe with nearest cluster assignment
                store_data = row.copy()
                store_data[self._cluster_id] = nearest_cluster
                store_data[self._cluster_name] = f"Market-{nearest_cluster}"
                store_data['ghost_id'] = f"Ghost-{nearest_cluster}-1"
                store_data['outlier'] = True

                # Add centroid coordinates
                store_data['centroid_lat'] = self._cluster_centroids[nearest_cluster]['centroid_lat']
                store_data['centroid_lon'] = self._cluster_centroids[nearest_cluster]['centroid_lon']

                # Add distance to center
                store_data['distance_to_center'] = round(min_distance, 2)

                cluster_sizes[nearest_cluster] = cluster_sizes.get(nearest_cluster, 0) + 1
                reassigned_stores.append(store_data)
            else:
                # No market has capacity within reach - keep as rejected
                still_rejected_indices.append(idx)
                self._logger.warning(
                    f"Store {row.get('store_id', idx)} has no market with capacity within "
                    f"{self._max_force_assign_distance} miles - leaving unassigned"
                )

        if reassigned_stores:
            # Convert to DataFrame and concatenate with main data
            reassigned_df = pd.DataFrame(reassigned_stores)
            self._data = pd.concat([self._data, reassigned_df], ignore_index=True)

            self._logger.info(
                f"Successfully force-assigned {len(reassigned_stores)} stores to nearest markets"
            )

        # Update rejected stores to only include those that are still too far
        if still_rejected_indices:
            self._rejected = self._rejected.loc[still_rejected_indices].copy()
            self._logger.info(
                f"{len(still_rejected_indices)} stores remain rejected (beyond {self._max_force_assign_distance} miles from nearest market)"  # noqa
            )
        else:
            # All stores were successfully assigned
            self._rejected = pd.DataFrame()

    def _add_distance_to_center_column(self, df: pd.DataFrame):
        """Add distance column showing miles from each store to its market center.

        Sub-cluster rows (FEAT-241) are exempt from the receiving market's
        distance-to-center rule: they measure to their own medoid
        (``subcluster_lat``/``subcluster_lon``) instead, since they carry
        their own centerpoint.
        """
        distances = []
        has_subclusters = 'is_subcluster' in df.columns

        for idx, row in df.iterrows():
            cluster_id = row[self._cluster_id]

            if has_subclusters and bool(row.get('is_subcluster')):
                distance_miles = self._haversine_miles(
                    row['latitude'], row['longitude'],
                    row['subcluster_lat'], row['subcluster_lon'],
                )
                distances.append(round(distance_miles, 2))
            elif cluster_id == -1 or cluster_id not in self._cluster_centroids:
                # For outliers or missing centroids, set distance as NaN
                distances.append(np.nan)
            else:
                # Calculate distance from store to its market center
                store_lat = row['latitude']
                store_lon = row['longitude']
                center_lat = self._cluster_centroids[cluster_id]['centroid_lat']
                center_lon = self._cluster_centroids[cluster_id]['centroid_lon']

                distance_miles = self._haversine_miles(store_lat, store_lon, center_lat, center_lon)
                distances.append(round(distance_miles, 2))  # Round to 2 decimal places

        df['distance_to_center'] = distances

    def _assign_predefined_markets(self) -> None:
        """Adopt the markets pre-defined in ``market_column`` (no_clustering).

        Each distinct non-null value of ``market_column`` becomes one market
        holding exactly its rows — nothing is formed, moved, merged or shed.
        Rows whose value is null/empty are delivered unassigned
        (``market_id = -1``, the Outlier convention). Formation-related
        options (``max_markets``, ``standalone_markets``, budget mode, ...)
        do not apply in this mode and are ignored with one warning.

        The centroid anchor is derived the same way standalone markets do
        it: a pre-defined market takes every store of its value regardless
        of distance, so it is just as likely to span two poles, and the
        anchored core keeps its centre inside the metro it actually serves.

        Raises:
            ComponentError: When ``market_column`` is missing from the input.
        """
        column = self.market_column
        if column not in self._data.columns:
            raise ComponentError(
                f"no_clustering is enabled but market_column '{column}' "
                "is missing from the input DataFrame."
            )

        ignored = [
            name for name, value in (
                ('max_markets', self.max_markets),
                ('standalone_markets', self.standalone_markets),
                ('subcluster_outliers', self.subcluster_outliers),
                ('max_employees', self.max_employees),
                ('optimize', self._optimize),
            ) if value
        ]
        if ignored:
            self._logger.warning(
                "no_clustering: markets are taken as-is from column %r; "
                "ignoring %s.",
                column, ", ".join(ignored),
            )

        # Same per-run state reset the per-region loop performs.
        self._rejected = pd.DataFrame()
        self._cluster_centroids = {}
        self._cluster_fte_info = {}
        self._cluster_partition = {}
        self._standalone_clusters = {}
        self._anchored_centroids = {}
        self._outlier_stores = set()
        self._readmitted_index_map = {}

        values = self._data[column]
        is_null = values.isna() | (values.astype(str).str.strip() == '')
        market_values = sorted(values[~is_null].unique(), key=str)
        mapping = {value: cid for cid, value in enumerate(market_values)}

        labels = pd.Series(-1, index=self._data.index, dtype=int)
        labels[~is_null] = values[~is_null].map(mapping)
        self._data[self._cluster_id] = labels.values

        null_count = int(is_null.sum())
        if null_count:
            self._logger.warning(
                "no_clustering: %s stores have no %r value; "
                "delivered unassigned.",
                null_count, column,
            )

        assigned = self._data[self._data[self._cluster_id] != -1]
        for cid, members in assigned.groupby(self._cluster_id):
            self._cluster_partition[cid] = False
            anchor = self._derive_core_anchor(members, min_core=2)
            if anchor is not None:
                self._anchored_centroids[cid] = anchor
            self._cluster_centroids[cid] = self._cluster_center(cid, members)

        self._logger.info(
            "no_clustering: adopted %s pre-defined markets from column %r "
            "(%s stores assigned, %s unassigned).",
            len(market_values), column, len(assigned), null_count,
        )

        # Additive region echo column, same contract as the clustering path.
        has_region = (
            bool(self.region_column)
            and self.region_column in self._data.columns
        )
        self._data['region'] = (
            self._data[self.region_column] if has_region else None
        )

    async def _run_region_pipeline(self) -> None:
        """Run the existing single-partition pipeline core on ``self._data``.

        FEAT-247 Module 2: this is the pipeline body ``run()`` executed
        directly before per-region orchestration existed, extracted
        UNCHANGED so it can run once per region frame (or once over the
        whole input when ``region_column`` is unset — the single-partition
        path). Everything from cluster creation through the FEAT-241
        overflow annotation is region-local by construction: it only ever
        sees ``self._data``, which the caller has already scoped to one
        region.

        Mutates ``self._data``, ``self._rejected``, ``self._outlier_stores``
        and the cluster-id-keyed dicts (``self._cluster_centroids`` etc.)
        exactly as the pre-FEAT-247 ``run()`` did. Does NOT renumber ids,
        label sub-clusters, resolve centroid locations, or log the final
        summary — those stay in ``run()``, run ONCE on the concatenated,
        globally-renumbered result.

        TASK-196: initializes the additive ``state_affinity_score`` column
        (NaN by default) before clustering — the five scoring surfaces
        stamp it as they place stores; it stays NaN elsewhere.

        TASK-198: initializes the additive ``ceded_from`` column (NaN by
        default) the same way — ``_cede_oversize_subclusters`` stamps the
        donor market id on ceded sub-cluster rows; NaN elsewhere.
        """
        if 'state_affinity_score' not in self._data.columns:
            self._data['state_affinity_score'] = np.nan
        if 'ceded_from' not in self._data.columns:
            self._data['ceded_from'] = np.nan
        # --- create cluster in haversine space (balltree)
        self._data = self._create_cluster(self._data)

        unreachable_stores = []  # gather all unreachable store indices globally
        grouped = self._data.groupby(self._cluster_id)
        for cid, cluster_stores in grouped:
            if cid == -1 or len(cluster_stores) <= 1:
                continue  # skip outliers
            if cid in self._standalone_clusters:
                # Standalone markets are distance-blind by definition: no
                # reachability filtering, their stores always stay.
                continue

            # Validate distances after cluster creation
            # outliers = self._validate_distance(self._data, cluster_stores)

            # Log outlier count
            # print(f"Number of outliers detected: {len(outliers)}")

            # Create the ghost employees for this Cluster:
            employees = self._create_ghost_employees(cid, self._data)
            cluster_unreachable = self._filter_unreachable_stores(
                cid=cid,
                employees=employees,
                cluster_stores=cluster_stores
            )
            unreachable_stores.extend(cluster_unreachable)

        # TODO: remove unreachable stores from the cluster
        unreachable_stores = list(set(unreachable_stores))
        self._rejected = self._data.loc[unreachable_stores].copy()
        self._data.drop(index=unreachable_stores, inplace=True)
        self._logger.info(
            f"Unreachable stores: {len(unreachable_stores)}"
        )

        # Assign stores to ghost employees (round-robin for single-ghost
        # clusters, VRP-based routing for multi-ghost clusters)
        self._validate_clusters_by_vrp()

        # Add cluster centroids to the result DataFrame
        self._add_cluster_centroids_to_result(self._data)
        self._add_outlier_column_to_result(self._data)

        # Rebalance clusters before attempting to reassign rejected stores
        self._rebalance_clusters_for_fte_constraints()

        # Force assign all rejected stores to nearest markets
        self._force_assign_all_rejected_stores()

        # Refresh cluster geometry after force assignment
        self._recompute_cluster_centroids()
        self._add_cluster_centroids_to_result(self._data)
        self._add_outlier_column_to_result(self._data)
        self._add_distance_to_center_column(self._data)
        self._apply_cadence_rules(self._data)

        # Before reassigning anything, make sure the markets themselves are
        # coherent: a market covering two cities cannot be repaired by moving
        # its stores around, whichever way they are assigned.
        if self._split_incoherent_markets():
            self._recompute_cluster_centroids()
            self._add_cluster_centroids_to_result(self._data)
            self._add_distance_to_center_column(self._data)

        # Re-evaluate distant stores for better market assignment
        self._find_borderline_stores()

        # The pass above can only move a store into a market with a free slot,
        # so a store next to a FULL market stays stranded. Let those markets
        # take it by handing one of their own to a neighbour instead.
        if self._ejection_chain_pass():
            self._recompute_cluster_centroids()
            self._add_cluster_centroids_to_result(self._data)
            self._add_distance_to_center_column(self._data)
            self._find_borderline_stores()

        # Dissolve clusters that ended below min_cluster_size, re-evaluating
        # their stores against the surviving markets
        self._dissolve_undersized_clusters()

        # Final enforcement of FTE constraints after reassignment tweaks
        self._rebalance_clusters_for_fte_constraints()

        # Restore the exact market count and the max_cluster_size ceiling
        # after all rejection/reassignment passes
        self._reconcile_final_markets()

        # Stores that no market can legitimately hold (too far, or every
        # market in range at capacity) are left unassigned rather than parked
        self._recompute_cluster_centroids()
        self._unassign_orphan_stores()
        # Nobody works more than day_hours: markets that do not fit shed their
        # costliest stores before the layout is delivered
        self._apply_cadence_rules(self._data)
        self._enforce_daily_hours_budget()
        # Unplaceable stores travel to the output as unassigned rows
        self._readmit_rejected_as_unassigned()
        # With every orphan visible, a stranded cluster can still claim a
        # market slot from one that serves almost nobody
        self._rescue_unassigned_clusters()
        # The last one-or-two stores next to a full market join it past the
        # capacity gate rather than being delivered unassigned
        self._absorb_remnant_stores()

        # Fly-out peel (FEAT-243, opt-in via subcluster_flyout): assigned
        # stores too far from — or with no road path to — their own
        # market's centroid never reach the pool below on their own, so
        # peel them here, before the pool is read.
        await self._peel_flyout_stores()

        # Outlier sub-cluster assignment (FEAT-241, opt-in via
        # subcluster_outliers): fold whatever is still unassigned into
        # day-budget pockets attached to the market with the fewest road
        # miles, so budget-mode consolidation right below sees the final
        # per-market headcount rather than deciding merges first and
        # discovering the extra load afterwards.
        await self._attach_outlier_subclusters()

        # Global employee-budget mode (FEAT-240): minimize total headcount
        # by merging markets, subject to full store coverage. Guarded on
        # _budget_mode both here and inside the pass itself, so the
        # non-budget path makes not even a guarded no-op call.
        if self._budget_mode:
            merged = self._consolidate_markets_for_headcount()
            if merged:
                # The merge changed geometry after the first daily-hours
                # sweep above; _merge_saving's condition 6 already
                # guarantees the merged market fits day_hours, so this is
                # defence in depth — expect it to move zero stores.
                self._enforce_daily_hours_budget()

        # Capacity shed (FEAT-243, opt-in via capacity_shedding): now that
        # satellite (sub-cluster) load is counted, an oversubscribed market
        # hands near-boundary normal stores to a neighbor with room, no
        # distance-gain requirement.
        self._capacity_shed_pass()

        # Scheduling feedback loop (FEAT-244, opt-in via optimize): an
        # internal SchedulingVisits run against this component's own
        # output is the ground truth for what the geometry-only heuristics
        # above missed — reclassify exception stores before the layout is
        # delivered.
        if self._optimize:
            await self._scheduling_feedback_pass()

        # Ensure centroids/distances reflect the final cluster composition
        self._recompute_cluster_centroids()

        # Every pass above moved stores and shifted centroids, so the
        # decisions that placed each store were taken against geometry that
        # no longer holds. Re-check them now that the layout has settled.
        self._repair_assignments()

        # Distance to a centre cannot see a store that sits inside another
        # market's ground while its own centroid is genuinely the nearest.
        # Let the neighbourhood decide those.
        if self._neighbourhood_repair_pass():
            self._recompute_cluster_centroids()

        self._add_cluster_centroids_to_result(self._data)
        self._add_outlier_column_to_result(self._data)
        self._add_distance_to_center_column(self._data)
        self._apply_cadence_rules(self._data)

        # Recompute FTE metrics for the final cluster layout
        self._recompute_cluster_fte_info()
        self._add_fte_columns_to_result(self._data)

        # FEAT-248 TASK-203: post-attach enforcement -- re-run
        # _enforce_max_cluster_size now that sub-cluster attachment,
        # budget-merge, capacity shed, scheduling feedback and repair have
        # all had their say, so a market pushed over its ceiling by
        # satellite load can no longer "attach for free". This pass only
        # ever sheds CORE stores (see its own docstring); whatever it
        # cannot fix -- overage made entirely of sub-cluster rows, or no
        # receiver in reach -- falls through to cession right below.
        self._enforce_max_cluster_size()

        # FEAT-247 Module 5: close the "sub-clusters attach for free"
        # bypass -- a market over max_cluster_size (counting attached
        # sub-cluster stores) cedes whole sub-clusters to the
        # best-scoring same-region receiver with room. Runs after every
        # other pass that could shift core-store counts (budget-merge,
        # capacity shed, scheduling feedback, repair/neighbourhood
        # passes above, and the enforcement pass right above) so it sees
        # the final, settled picture, and right before the overflow
        # annotation below so whatever it could not resolve is exactly
        # what gets flagged.
        self._cede_oversize_subclusters()

        # FEAT-241: annotate (never reject) markets that exceed
        # max_cluster_size because of sub-cluster incorporation. Must run
        # after _add_fte_columns_to_result(), whose per-cluster
        # constraint_warning write would otherwise clobber this
        # row-level annotation.
        self._annotate_subcluster_overflow()

    async def run(self):
        """
        1) Split by ``region_column`` (FEAT-247) and run the existing
           pipeline core once per region (or once over the whole input
           when ``region_column`` is unset — the single-partition path
           byte-identical to the pre-FEAT-247 behaviour).
        2) Concatenate every region's result and renumber markets
           globally (Market-1..Market-N).
        3) Reconcile ``max_markets`` as a hard global ceiling (in-region
           merges only, never across regions).
        4) Label sub-clusters, resolve centroid locations, add FTE/visit
           columns, log summaries, and return the final assignment +
           rejected stores.

        See ``_run_region_pipeline`` for the pipeline core itself
        (clustering, ghost employees, VRP, rebalancing, sub-cluster
        attachment, overflow annotation — unchanged from before FEAT-247).
        """
        self._logger.info(
            "=== Running MarketClustering ==="
        )

        # Reset counters for this execution
        self._constraint_removed_total = 0
        # Employee-budget consolidation counters (FEAT-240): reset here so
        # two consecutive run() calls on the same component never
        # accumulate, the same reason _constraint_removed_total is reset.
        self._budget_markets_before = None
        self._budget_markets_after = None
        self._budget_merges_applied = 0
        self._budget_headcount_saved = 0
        self._budget_relaxed_round_used = False

        if self.use_fte_constraints:
            self._logger.info(
                f"FTE Mode Enabled: "
                f"monthly_target={self.fte_monthly}, "
                f"daily_target={self.fte_daily}, "
                f"hours_per_week={self.hours_per_week}, "
                f"ghosts_range={self.num_ghosts_range}"
            )
        else:
            self._logger.info("FTE constraints disabled; computing FTE metrics for reporting only.")

        # Pre-defined markets (no_clustering): adopt market_column as-is
        # and jump straight to the delivery tail — no formation, no
        # movement passes, no max_markets reconciliation.
        if self.no_clustering:
            self._assign_predefined_markets()
            return await self._finalize_delivery()

        # --- FEAT-247: per-region orchestration (Module 2) ---------------
        full_data = self._data
        has_region = bool(self.region_column) and self.region_column in full_data.columns

        if has_region:
            region_values = sorted(full_data[self.region_column].dropna().unique())
        else:
            # Single-partition path: identical orchestration over one
            # partition, output equivalent to the pre-FEAT-247 behaviour.
            region_values = [None]

        original_max_markets = self.max_markets

        # Split the global budget before any region forms, so each region
        # drives its own formation to a real target instead of to no limit.
        # An undersized region resolves to a quota of exactly 1 by
        # construction (its floor and ceiling both collapse to 1), so the
        # max_markets=1 override below never overspends the budget.
        region_quotas = (
            self._allocate_region_market_quotas(full_data, region_values)
            if has_region else {}
        )

        region_frames: List[pd.DataFrame] = []
        region_rejected: List[pd.DataFrame] = []
        combined_cluster_centroids: Dict[Any, Dict] = {}
        combined_cluster_fte_info: Dict[Any, Dict] = {}
        combined_cluster_partition: Dict[Any, bool] = {}
        combined_standalone_clusters: Dict[Any, Tuple] = {}
        combined_anchored_centroids: Dict[Any, Tuple] = {}
        combined_readmitted_index_map: Dict[Any, Any] = {}
        row_offset = 0
        id_offset = 0
        undersized_regions: List[Any] = []

        for region_value in region_values:
            region_df = (
                full_data if region_value is None
                else full_data[full_data[self.region_column] == region_value].copy()
            )
            if region_df.empty:
                continue

            self._data = region_df
            self._rejected = pd.DataFrame()
            self._cluster_centroids = {}
            self._cluster_fte_info = {}
            self._cluster_partition = {}
            self._standalone_clusters = {}
            self._anchored_centroids = {}
            self._outlier_stores = set()
            # Reset per region: _readmit_rejected_as_unassigned() OVERWRITES
            # this (not accumulates), so a region that never readmits
            # anything must not inherit a previous region's stale entries.
            self._readmitted_index_map = {}

            undersized = (
                has_region
                and self.min_cluster_size
                and len(region_df) < self.min_cluster_size
            )
            if undersized:
                undersized_regions.append(region_value)
                self._logger.warning(
                    "region %r: %s stores < min_cluster_size=%s -- forming "
                    "ONE undersized market (reported, never merged across "
                    "regions).",
                    region_value, len(region_df), self.min_cluster_size,
                )

            # max_markets is a HARD TARGET, so each region forms against
            # its own slice of the budget rather than against no limit at
            # all. Emergent per-region counts (the original FEAT-247
            # behaviour, max_markets=None here) cannot reach the target:
            # formation births far fewer markets than configured and the
            # global pass afterwards has nothing large enough left to
            # split, so the run silently delivers under the target with
            # the overflow pushed into sub-cluster satellites.
            # The undersized-region case still reuses the existing,
            # already-tested max_markets=1 behaviour. The single-partition
            # path (region_column unset) keeps max_markets exactly as
            # configured -- byte-identical to the pre-FEAT-247 behaviour.
            if has_region:
                if undersized:
                    self.max_markets = 1
                else:
                    self.max_markets = region_quotas.get(
                        region_value, original_max_markets
                    )

            await self._run_region_pipeline()

            id_offset = self._shift_region_cluster_ids(id_offset)
            row_offset = self._shift_region_indices(row_offset)

            region_frames.append(self._data)
            region_rejected.append(self._rejected)
            combined_cluster_centroids.update(self._cluster_centroids)
            combined_cluster_fte_info.update(self._cluster_fte_info)
            combined_cluster_partition.update(self._cluster_partition)
            combined_standalone_clusters.update(self._standalone_clusters)
            combined_anchored_centroids.update(self._anchored_centroids)
            combined_readmitted_index_map.update(self._readmitted_index_map)

        self.max_markets = original_max_markets

        self._data = (
            pd.concat(region_frames) if region_frames
            else full_data.iloc[0:0].copy()
        )
        self._rejected = (
            pd.concat(region_rejected) if region_rejected
            else pd.DataFrame()
        )
        self._cluster_centroids = combined_cluster_centroids
        self._cluster_fte_info = combined_cluster_fte_info
        self._cluster_partition = combined_cluster_partition
        self._standalone_clusters = combined_standalone_clusters
        self._anchored_centroids = combined_anchored_centroids
        self._readmitted_index_map = combined_readmitted_index_map

        # Additive output column (spec §2 New Public Interfaces): echo of
        # each market's region value. None when region_column is unset.
        self._data['region'] = (
            self._data[self.region_column] if has_region else None
        )

        # max_markets global reconciliation (hard ceiling; in-region
        # merges only, never across regions).
        self._reconcile_global_max_markets()

        # Global reconciliation MUTATES membership (in-region merges, and
        # any split-up), so every geometry column stamped back at region
        # time is now stale for the markets it touched — the delivery tail
        # re-derives all of it from the final membership.
        return await self._finalize_delivery(
            has_region=has_region,
            region_values=region_values,
            undersized_regions=undersized_regions,
        )

    async def _finalize_delivery(
        self,
        has_region: bool = False,
        region_values: Optional[List[Any]] = None,
        undersized_regions: Optional[List[Any]] = None,
    ) -> pd.DataFrame:
        """Shared delivery tail of ``run()``.

        Re-derives every geometry-dependent column from the FINAL
        membership (the passes before this point mutate membership, so
        anything stamped earlier is stale for the markets they touched:
        stale `centroid_lat`/`centroid_lon` are how a market ends up
        labelled "Santa Fe, NM" at Denver's coordinates. `distance_to_
        center` and `outlier` feed SchedulingVisits, and the cadence
        rules are distance-based, so all of them are re-derived here).
        Then renumbers markets 1..N, labels sub-clusters, resolves
        centroid locations, stamps visit columns, logs the summaries,
        reconciles the rejected ledger and returns the final assignment.

        Called by both paths of ``run()``: the clustering path (after
        global max_markets reconciliation) and the no_clustering path
        (right after ``_assign_predefined_markets``).

        Args:
            has_region: Whether region orchestration ran (clustering
                path with ``region_column`` set).
            region_values: Region values processed, for the per-region
                summary log.
            undersized_regions: Regions that formed one undersized
                market, for the same summary.

        Returns:
            The final assignment DataFrame (also stored in ``_result``).
        """
        self._recompute_cluster_centroids()
        self._add_cluster_centroids_to_result(self._data)
        self._add_outlier_column_to_result(self._data)
        self._add_distance_to_center_column(self._data)
        self._apply_cadence_rules(self._data)
        self._recompute_cluster_fte_info()
        self._add_fte_columns_to_result(self._data)

        # G6 / audit item 1d: `_add_fte_columns_to_result` just overwrote
        # `constraint_warning` for every row with each market's per-cluster
        # FTE warning, clobbering whatever `_annotate_subcluster_overflow`
        # stamped per-region BEFORE global `_reconcile_global_max_markets`
        # ran. Re-stamp it here, after the per-cluster write and after
        # global reconciliation has settled final membership, so overflow
        # annotations reflect the delivered sizes, not a pre-split parent's.
        self._annotate_subcluster_overflow()

        self._check_market_invariants()

        # Deliver 1-based, sequential market ids (Market-1..Market-N)
        self._renumber_markets_from_one()

        # FEAT-241: sub_cluster = "<market>-SC<n>" labels, using the
        # delivered 1-based market ids/names from the renumbering above.
        self._label_subclusters()

        # Name the ground each market centre lands on. Resolved HERE, after
        # the renumbering, so the lookup keys are the delivered market ids
        # and the geometry is the one being shipped — one query per market.
        await self._resolve_centroid_locations()
        self._add_centroid_location_columns(self._data)

        # Deliver visit_rule (count) + visit_frequency (cadence rule name)
        self._apply_visit_rule_columns(self._data)

        # Log FTE summary
        if self.fte_mode:
            self._log_fte_summary()
        if self._budget_mode:
            self._log_employee_budget_summary()

        if self._constraint_removed_total:
            self._logger.info(
                f"Removed {self._constraint_removed_total} stores overall due to FTE constraint violations"
            )

        if has_region:
            self._log_per_region_summary(region_values, undersized_regions)

        self._logger.info(
            f"Final clusters formed: {self._count_delivered_markets()} "
            f"(excluding Outliers)"
        )
        # Readmitted stores that a later pass assigned (sub-clusters,
        # rescue, absorb) must not be logged or saved as rejected
        self._reconcile_rejected_ledger()
        self._logger.info(
            f"Total rejected stores: {len(self._rejected)}"
        )
        self._save_rejected_stores()

        self._result = self._data
        return self._result
