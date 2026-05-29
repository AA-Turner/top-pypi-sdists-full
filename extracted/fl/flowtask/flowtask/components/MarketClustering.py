from collections.abc import Callable
from typing import List, Dict, Optional, Any, Union, Tuple
import asyncio
import math
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
from sklearn.cluster import KMeans
from sklearn.neighbors import BallTree
from ..interfaces.flow import FlowComponent
from ..exceptions import (
    DataNotFound,
    ConfigError,
    ComponentError,
)


# -----------------------------
# Utility Functions
# -----------------------------
def meters_to_miles(m):
    return m * 0.000621371


def miles_to_radians(miles):
    earth_radius_km = 6371.0087714150598
    km_per_mi = 1.609344
    return miles / (earth_radius_km * km_per_mi)

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
    """Stores the data for the VRP problem."""
    return {
        'distance_matrix': distance_matrix,
        'num_vehicles': num_vehicles,
        'depot': depot,
        'max_distance': max_distance,
        'max_stores_per_vehicle': max_stores_per_vehicle,
    }


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
        int(data['max_distance'] * 1000),  # maximum distance per vehicle
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
        visit_frequency: Optional[float] = None,
        fte_monthly_target: Optional[float] = None,
        fte_daily_target: Optional[float] = None,
        num_ghosts_range: Optional[Tuple[int, int]] = None
    ):
        self.day_hours = day_hours
        self.hours_per_week = hours_per_week
        self.working_days_per_week = working_days_per_week
        self.in_store_hours = in_store_hours
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
        setup_time_per_store: float = 0.5,  # hours for setup/teardown per store
        visit_frequencies: Optional[pd.Series] = None,
        in_store_hours: Optional[pd.Series] = None,
    ) -> Dict[str, float]:
        """
        Calculate hours needed for a cluster based on stores and distances.

        Returns:
            Dictionary with daily_hours, monthly_hours, travel_hours, work_hours
        """
        # Travel time between stores
        travel_time_per_store = (avg_distance_between_stores / avg_speed_mph) if avg_speed_mph > 0 else 0

        weeks_per_month = self._weeks_per_month()

        frequency_series: Optional[pd.Series] = None
        if visit_frequencies is not None:
            frequency_series = pd.to_numeric(visit_frequencies, errors='coerce')
            frequency_series = frequency_series.fillna(self.default_visit_frequency)

        service_time_series: Optional[pd.Series] = None
        if in_store_hours is not None:
            service_time_series = pd.to_numeric(in_store_hours, errors='coerce')
            service_time_series = service_time_series.fillna(self.in_store_hours)

        if frequency_series is None and service_time_series is None:
            work_hours_per_store = self.in_store_hours
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
                    self.in_store_hours,
                    index=frequency_series.index,
                    dtype=float
                )
            else:
                service_time_series = service_time_series.reindex(frequency_series.index)
                service_time_series = service_time_series.fillna(self.in_store_hours)

            per_store_total = service_time_series + travel_time_per_store + setup_time_per_store
            monthly_hours = float((per_store_total * frequency_series).sum())
            monthly_visits = float(frequency_series.sum())
            work_hours_per_store = float(service_time_series.mean()) if len(service_time_series) > 0 else self.in_store_hours
            total_time_per_store = float(per_store_total.mean()) if len(per_store_total) > 0 else (
                work_hours_per_store + travel_time_per_store + setup_time_per_store
            )

        if frequency_series is None or len(frequency_series) == 0:
            work_hours_per_store = self.in_store_hours
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
            'travel_hours_per_store': travel_time_per_store,
            'work_hours_per_store': work_hours_per_store,
            'setup_hours_per_store': setup_time_per_store,
            'total_hours_per_store': total_time_per_store
        }

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
            # Simple heuristic: more stores = more employees (within range)
            stores_per_employee = max(1, num_stores / max_ghosts)
            num_employees = min(max_ghosts, max(min_ghosts, int(np.ceil(num_stores / max_stores_per_employee))))

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

        max_cluster_distance (default: 50.0)

        Purpose: Controls outlier detection within already-formed clusters
        Usage: Used in _detect_outliers() to check if stores are too far from their cluster's centroid
        Effect: Stores farther than this distance from their cluster center get marked as outliers
        Location: Used in validation after clusters are formed

        max_stores_per_day: Max stores per ghost employee per day
        day_hours: Working hours per day
        max_distance_by_day: Max travel distance per day


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
        visit_frequency (float, optional): Default number of visits per store each
            month when a ``visit_frequency`` column is not provided in the input
            data. Defaults to ``2`` visits per month.
        visit_frequency_column (str, optional): Name of the column in the input
            data containing per-store monthly visit frequencies. Defaults to
            ``visit_frequency``.
        in_store_hours_column (str, optional): Name of the column containing
            per-store service times. Defaults to ``in_store_hours``.

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
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # DBSCAN config
        self.max_cluster_distance = kwargs.pop('max_cluster_distance', 50.0)
        self.cluster_radius = kwargs.pop('cluster_radius', 150.0)
        self.max_cluster_size: int = kwargs.pop('max_cluster_size', 25)  # number of items in cluster
        self.min_cluster_size: int = kwargs.pop('min_cluster_size', 5)  # minimum number of items in cluster
        self.rejected_stores_file: Path = kwargs.pop('rejected_stores', None)
        self.distance_unit = kwargs.pop('distance_unit', 'miles')  # or 'km'
        self.min_samples = kwargs.pop('min_samples', 1)
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
        # Ghost employees config
        self.num_ghosts_per_cluster: Union[int, List[int]] = kwargs.pop('num_ghosts_per_cluster', 2)
        self.ghost_distance_threshold = kwargs.pop('ghost_distance_threshold', 50.0)
        # Daily route constraints
        self.max_stores_per_day = kwargs.pop('max_stores_per_day', 3)
        self.day_hours = kwargs.pop('day_hours', 8.0)
        self.max_distance_by_day = kwargs.pop('max_distance_by_day', 150.0)
        # e.g. 150 miles, or if using km, adapt accordingly

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
        self.in_store_hours_column = kwargs.pop('in_store_hours_column', 'in_store_hours')
        self.visit_frequency_column = kwargs.pop('visit_frequency_column', 'visit_frequency')

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

        if self.use_fte_constraints and self.num_ghosts_range is None:
            self.use_fte_constraints = False
            self.fte_mode = False
            self._logger.warning(
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
            visit_frequency=self.default_visit_frequency,
            fte_monthly_target=fte_monthly_target,
            fte_daily_target=fte_daily_target,
            num_ghosts_range=num_ghosts_range
        )
        self.default_visit_frequency = self.fte_calculator.default_visit_frequency

        # Relaxed threshold for outlier reassignment
        # e.g. 25 miles or km to consider a store "reachable" from that ghost
        self.reassignment_threshold_factor = kwargs.pop(
            'reassignment_threshold_factor', 0.5
        )  # 50% of max_cluster_distance
        # Default 20% of max_cluster_size
        self.max_reassignment_percentage = kwargs.pop('max_reassignment_percentage', 0.2)
        # Refinement with OSMnx route-based distances?
        self.borderline_threshold = kwargs.pop('borderline_threshold', 2.5)
        # max force distance to assign a rejected store to the nearest market:
        self._max_force_assign_distance = kwargs.pop('max_assign_distance', 50)
        # bounding box or place
        self.bounding_box = kwargs.pop('bounding_box', None)
        self.place_name = kwargs.pop('place_name', None)

        # Internals
        self._data: pd.DataFrame = pd.DataFrame()
        self._result: Optional[pd.DataFrame] = None
        self._rejected: pd.DataFrame = pd.DataFrame()  # for stores that get dropped
        self._ghosts: List[Dict[str, Any]] = []
        self._graphs: dict = {}
        self._cluster_centroids: Dict[int, Dict[str, float]] = {}  # Store cluster centroids
        # Store FTE info per cluster
        self._cluster_fte_info: Dict[int, Dict[str, Any]] = {}
        self._constraint_removed_total: int = 0
        self._constraint_rebalance_required: bool = False
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._outlier_stores: set = set()  # Track stores that were marked as outliers

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

        return True

    async def close(self):
        pass

    def get_rejected_stores(self) -> pd.DataFrame:
        """Return the DataFrame of rejected stores (those removed from any final market)."""
        return self._rejected

    # ------------------------------------------------------------------
    # FTE Calculations
    # ------------------------------------------------------------------

    def _calculate_cluster_avg_distance(self, cluster_df: pd.DataFrame) -> float:
        """
        Calculate average distance between stores in a cluster.
        """
        if len(cluster_df) < 2:
            return 0.0

        coords = cluster_df[['latitude', 'longitude']].values
        distances = []

        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                dist = self._haversine_miles(
                    coords[i][0], coords[i][1],
                    coords[j][0], coords[j][1]
                )
                distances.append(dist)

        return np.mean(distances) if distances else 0.0

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
        # Check if 'fte' column already exists (from previous calculation)
        if 'fte' in cluster_df.columns:
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

        if self.use_fte_constraints:
            optimization_result = self.fte_calculator.optimize_num_employees(
                num_stores=num_stores,
                avg_distance=avg_distance,
                max_stores_per_employee=self.max_stores_per_day,
                visit_frequencies=visit_frequencies,
                in_store_hours=in_store_hours,
            )
            cluster_info = optimization_result
        else:
            cluster_hours = self.fte_calculator.calculate_cluster_hours(
                num_stores=num_stores,
                avg_distance_between_stores=avg_distance,
                visit_frequencies=visit_frequencies,
                in_store_hours=in_store_hours,
            )
            fte_totals = self.fte_calculator.calculate_fte_requirements(cluster_hours)

            num_ghosts = self.num_ghosts_per_cluster
            if isinstance(num_ghosts, list):
                num_ghosts = num_ghosts[0] if num_ghosts else 1

            if not num_ghosts or num_ghosts < 1:
                num_ghosts = 1

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
                and hours_per_emp_daily > self.day_hours
            ):
                constraint_violated = True
                suggested_employees_daily = math.ceil(cluster_hours['daily_hours'] / self.day_hours)
                suggested_employees = max(suggested_employees, suggested_employees_daily)

            # Check if weekly hours constraint is violated
            if (
                self.hours_per_week is not None
                and self.hours_per_week > 0
                and hours_per_emp_weekly > self.hours_per_week
            ):
                constraint_violated = True
                suggested_employees_weekly = math.ceil(cluster_hours['weekly_hours'] / self.hours_per_week)
                suggested_employees = max(suggested_employees, suggested_employees_weekly)

            stores_per_employee = (
                num_stores / num_ghosts if num_ghosts else np.nan
            )
            stores_limit_exceeded = (
                pd.notna(stores_per_employee)
                and self.max_stores_per_day is not None
                and self.max_stores_per_day > 0
                and stores_per_employee > self.max_stores_per_day
            )
            if stores_limit_exceeded:
                constraint_violated = True
                suggested_employees_store = math.ceil(num_stores / self.max_stores_per_day)
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
                        f"Stores: {stores_per_employee:.1f}/employee (limit: {self.max_stores_per_day})"
                    )

                constraint_warning = " ".join(warning_parts)
                self._logger.error(
                    f"Cluster {cid}: {constraint_warning}"
                )
                if self._constraints_enforcement_enabled():
                    self._constraint_rebalance_required = True

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

        # Get cluster centroids
        clusters = stores[stores[self._cluster_id] != -1].groupby(self._cluster_id)
        centroids = {
            cluster_id: cluster_df[['latitude', 'longitude']].mean().values
            for cluster_id, cluster_df in clusters
        }

        # Relaxed distance threshold
        relaxed_threshold = self.cluster_radius + self.relaxed_threshold

        for outlier_idx in list(unassigned):
            outlier_lat = stores.at[outlier_idx, 'latitude']
            outlier_lon = stores.at[outlier_idx, 'longitude']

            # Find nearest cluster within relaxed threshold
            nearest_cluster = None
            min_distance = float('inf')

            for cluster_id, centroid in centroids.items():
                distance = self._haversine_miles(centroid[0], centroid[1], outlier_lat, outlier_lon)
                if distance < relaxed_threshold and distance < min_distance:
                    nearest_cluster = cluster_id
                    min_distance = distance

            # Assign to the nearest cluster if valid
            if nearest_cluster is not None:
                stores.at[outlier_idx, self._cluster_id] = nearest_cluster
                self._outlier_stores.discard(outlier_idx)  # Remove from outliers if reassigned
                unassigned.remove(outlier_idx)

        print(f"Post-processing completed. Remaining unassigned: {len(unassigned)}")

    def _add_outlier_column_to_result(self, df: pd.DataFrame):
        """Add outlier boolean column to indicate stores that were marked as outliers."""
        df['outlier'] = df.index.isin(self._outlier_stores)

    def _recompute_cluster_centroids(self):
        """Recalculate centroids for all current clusters."""
        new_centroids: Dict[int, Dict[str, float]] = {}

        if self._data.empty:
            self._cluster_centroids = {}
            return

        for cid, grp in self._data.groupby(self._cluster_id):
            if cid == -1 or grp.empty:
                continue

            new_centroids[cid] = {
                'centroid_lat': float(grp['latitude'].mean()),
                'centroid_lon': float(grp['longitude'].mean()),
            }

        self._cluster_centroids = new_centroids

    def _recompute_cluster_fte_info(self):
        """Recalculate FTE metrics for each cluster based on current assignments."""
        self._cluster_fte_info.clear()

        if self._data.empty:
            return

        for cid, cluster_df in self._data.groupby(self._cluster_id):
            if cid == -1 or cluster_df.empty:
                continue

            self._get_num_ghosts_for_cluster(cid, cluster_df)

    def _cluster_satisfies_constraints(self, info: Dict[str, Any]) -> bool:
        """Return True when the provided cluster metrics respect configured constraints."""
        if not info:
            return True

        if info.get('constraint_warning'):
            return False

        daily_hours = info.get('daily_hours_per_employee')
        if pd.notna(daily_hours) and self.day_hours > 0 and daily_hours > self.day_hours + 1e-6:
            return False

        stores_per_employee = info.get('stores_per_employee')
        if (
            pd.notna(stores_per_employee)
            and self.max_stores_per_day > 0
            and stores_per_employee > self.max_stores_per_day + 1e-6
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
        else:
            self._cluster_centroids[cid] = {
                'centroid_lat': float(updated_cluster['latitude'].mean()),
                'centroid_lon': float(updated_cluster['longitude'].mean()),
            }

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

    def _create_cluster(self, stores: pd.DataFrame):
        """
        1) BFS with BallTree to create a provisional cluster.
        2) Post-check each cluster with a distance validation (centroid-based or K-Means).
        3) Mark outliers as -1 or store them as rejected.
        """
        # 1) Sort by latitude and longitude to ensure spatial proximity in clustering
        stores = stores.sort_values(by=['latitude', 'longitude']).reset_index(drop=True)
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

        # Convert self.cluster_radius (in miles) to radians for BallTree search
        radius_radians = miles_to_radians(self.cluster_radius)

        while unassigned:

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
            # Get the first unassigned store
            current_idx = unassigned_list[0]
            cluster_indices.append(current_idx)
            stores.at[current_idx, self._cluster_id] = cluster_label
            unassigned.remove(current_idx)

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
                elif not new_candidates:
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
        """Map cluster_id => Market1, Market2, etc."""
        cluster_map = {}
        cluster_ids = sorted(set(labels))
        market_idx = 0
        for cid in cluster_ids:
            if cid == -1:
                cluster_map[cid] = "Outlier"
            else:
                cluster_map[cid] = f"Market-{market_idx}"
                market_idx += 1
        df[self._cluster_name] = df[self._cluster_id].map(cluster_map)

    def _add_cluster_centroids_to_result(self, df: pd.DataFrame):
        """Add cluster centroid coordinates to the result DataFrame."""
        df['centroid_lat'] = df[self._cluster_id].map(
            lambda cid: self._cluster_centroids.get(cid, {}).get('centroid_lat', np.nan)
        )
        df['centroid_lon'] = df[self._cluster_id].map(
            lambda cid: self._cluster_centroids.get(cid, {}).get('centroid_lon', np.nan)
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
        """
        Re-evaluate stores that are > half cluster radius from their center
        to see if they should be reassigned to a closer market center.
        Respects maximum cluster size limits during reassignment.
        """
        reassignment_threshold = self.max_cluster_distance * self.reassignment_threshold_factor
        reassigned_count = 0
        # 20% of max_cluster_size
        max_reassignment_limit = int(self.max_cluster_size * self.max_reassignment_percentage)

        # Track current cluster sizes
        cluster_sizes = self._data[
            self._data[self._cluster_id] != -1
        ].groupby(self._cluster_id).size().to_dict()

        # Group stores by current market
        for current_cid in self._data[self._cluster_id].unique():
            if current_cid == -1:
                continue

            current_market_stores = self._data[self._data[self._cluster_id] == current_cid].copy()

            for idx, store in current_market_stores.iterrows():
                store_distance = store.get('distance_to_center', 0)

                # Only re-evaluate stores beyond the threshold
                if store_distance > reassignment_threshold:
                    store_lat = store['latitude']
                    store_lon = store['longitude']

                    # Find the closest market center (including current one)
                    min_distance = float('inf')
                    best_market = current_cid

                    for other_cid in self._data[self._cluster_id].unique():
                        if other_cid == -1:
                            continue

                        # Check if target market would exceed size limit
                        current_size = cluster_sizes.get(other_cid, 0)
                        if current_size >= (self.max_cluster_size - max_reassignment_limit):
                            continue  # Skip this market - too close to size limit

                        if other_cid in self._cluster_centroids:
                            center_lat = self._cluster_centroids[other_cid]['centroid_lat']
                            center_lon = self._cluster_centroids[other_cid]['centroid_lon']

                            distance = self._haversine_miles(store_lat, store_lon, center_lat, center_lon)

                            # Only reassign if significantly closer (at least 5 miles difference)
                            # and within max_cluster_distance
                            if (
                                distance < min_distance and distance <= self.max_cluster_distance and distance < (store_distance - 5.0)  # noqa
                            ):  # Must be at least 5 miles closer
                                min_distance = distance
                                best_market = other_cid

                    # Reassign if we found a better market
                    if best_market != current_cid:
                        self._data.at[idx, self._cluster_id] = best_market
                        self._data.at[idx, self._cluster_name] = f"Market-{best_market}"
                        self._data.at[idx, 'ghost_id'] = f"Ghost-{best_market}-1"

                        # Update centroid coordinates
                        self._data.at[idx, 'centroid_lat'] = self._cluster_centroids[best_market]['centroid_lat']
                        self._data.at[idx, 'centroid_lon'] = self._cluster_centroids[best_market]['centroid_lon']

                        reassigned_count += 1

                        self._logger.info(
                            f"Reassigned store {store.get('store_id', idx)} from Market-{current_cid} "
                            f"(dist: {store_distance:.1f}mi) to Market-{best_market} (dist: {min_distance:.1f}mi)"
                        )

        if reassigned_count > 0:
            self._logger.info(
                f"Re-evaluated and reassigned {reassigned_count} distant stores to closer markets"
            )
            # FIXED: Recalculate FTE info after reassignment
            self._recalculate_cluster_ftes_after_reassignment()
            # Recalculate distances after reassignment
            self._add_distance_to_center_column(self._data)

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

        # Centroid of this Cluster
        lat_mean = cluster_rows['latitude'].mean()
        lon_mean = cluster_rows['longitude'].mean()

        max_offset_lat = 0.002  # ~5 km
        max_offset_lon = 0.002  # ~5 km at 40° latitude
        max_offset_miles = 50.0  # Maximum distance from centroid
        min_distance_km = 10.0  # Minimum distance between ghosts to prevent overlapping

        # Get number of ghost employees for this cluster
        num_ghosts = self._get_num_ghosts_for_cluster(cid, cluster_rows)

        for i in range(num_ghosts):
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
                angle = np.random.uniform(0, 2 * np.pi)
                distance = np.random.uniform(0, max_offset_miles)
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
            max_distance=self.max_distance_by_day,
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

        # Get all valid cluster centroids (excluding outliers)
        valid_clusters = self._data[self._data[self._cluster_id] != -1][self._cluster_id].unique()

        if len(valid_clusters) == 0:
            self._logger.warning("No valid clusters found for force assignment!")
            return

        reassigned_stores = []
        still_rejected_indices = []  # Track stores that remain rejected

        for idx, row in self._rejected.iterrows():
            min_distance = float('inf')
            nearest_cluster = None

            # Find the nearest cluster centroid
            for cid in valid_clusters:
                if cid in self._cluster_centroids:
                    centroid_lat = self._cluster_centroids[cid]['centroid_lat']
                    centroid_lon = self._cluster_centroids[cid]['centroid_lon']
                    distance = self._haversine_miles(
                        centroid_lat, centroid_lon,
                        row['latitude'], row['longitude']
                    )
                    if distance < min_distance:
                        min_distance = distance
                        nearest_cluster = cid

            if nearest_cluster is not None and min_distance <= self._max_force_assign_distance:
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

                reassigned_stores.append(store_data)
            else:
                # Store is too far even from nearest cluster - keep as rejected
                still_rejected_indices.append(idx)
                self._logger.warning(
                    f"Store {row.get('store_id', idx)} is {min_distance:.1f} miles from nearest market - leaving unassigned"  # noqa
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
        """Add distance column showing miles from each store to its market center."""
        distances = []

        for idx, row in df.iterrows():
            cluster_id = row[self._cluster_id]

            if cluster_id == -1 or cluster_id not in self._cluster_centroids:
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

    async def run(self):
        """
        1) Cluster with BallTree + K-Means validation.
        2) Calculate optimal ghost employees per cluster based on FTE
        3) Road-based validation: assign stores to ghost employees via VRP.
        4) Remove any stores that cannot be assigned within constraints.
        5) Re-assign rejected stores if possible.
        6) Add cluster centroids to result DataFrame.
        7) Add FTE columns to result DataFrame
        8) Log FTE summary
        9) Return final assignment + rejected stores.

        """
        self._logger.info(
            "=== Running MarketClustering ==="
        )

        # Reset counters for this execution
        self._constraint_removed_total = 0

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

        # --- create cluster in haversine space (balltree)
        self._data = self._create_cluster(self._data)

        unreachable_stores = []  # gather all unreachable store indices globally
        grouped = self._data.groupby(self._cluster_id)
        for cid, cluster_stores in grouped:
            if cid == -1 or len(cluster_stores) <= 1:
                continue  # skip outliers

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

        # Re-evaluate distant stores for better market assignment
        self._find_borderline_stores()

        # Final enforcement of FTE constraints after reassignment tweaks
        self._rebalance_clusters_for_fte_constraints()

        # Ensure centroids/distances reflect the final cluster composition
        self._recompute_cluster_centroids()
        self._add_cluster_centroids_to_result(self._data)
        self._add_outlier_column_to_result(self._data)
        self._add_distance_to_center_column(self._data)

        # Recompute FTE metrics for the final cluster layout
        self._recompute_cluster_fte_info()
        self._add_fte_columns_to_result(self._data)

        # Log FTE summary
        if self.fte_mode:
            self._log_fte_summary()

        if self._constraint_removed_total:
            self._logger.info(
                f"Removed {self._constraint_removed_total} stores overall due to FTE constraint violations"
            )

        self._logger.info(
            f"Final clusters formed: {self._data[self._cluster_id].nunique() - 1} (excluding Outliers)"
        )
        self._logger.info(
            f"Total rejected stores: {len(self._rejected)}"
        )
        self._save_rejected_stores()

        self._result = self._data
        return self._result
