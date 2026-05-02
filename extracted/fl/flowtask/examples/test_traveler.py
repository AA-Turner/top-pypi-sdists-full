import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


traveler = (25.7529793, -80.32231159999999)
stores = [
    (25.685314, -80.448545),
    (25.787051, -80.335332),
    (25.858609, -80.325508),
    (25.746027, -80.332788),
    (25.623903, -80.395205)
]

def to_miles(meters: float) -> float:
    """Convert meters to miles."""
    # return meters * 0.000621371
    return meters / 1609.344

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Change in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance

def create_data_model(coordinates):
    """Stores the data for the problem."""
    data = {}
    # Compute the distance matrix between each pair of points
    data['distance_matrix'] = calculate_distance_matrix(coordinates)
    data['num_vehicles'] = 1
    data['depot'] = 0  # Assuming the first point in coordinates is the traveler's house
    return data

def calculate_distance_matrix(coordinates):
    """Calculate the distance matrix from coordinates."""
    num_locations = len(coordinates)
    distance_matrix = [[0] * num_locations for _ in range(num_locations)]

    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                lat1, lon1 = coordinates[i]
                lat2, lon2 = coordinates[j]
                # Scale up the distance to ensure it's a sufficiently large integer
                distance_matrix[i][j] = int(haversine(lat1, lon1, lat2, lon2) * 1000)  # Convert km to meters

    return distance_matrix

def main():
    # Coordinates of the points (including the traveler's house as the first point)
    coordinates = [
        traveler,  # Traveler's house coordinates
        *stores
    ]

    # Instantiate the data problem.
    data = create_data_model(coordinates)
    distance_matrix = data['distance_matrix']

    # Print the distance matrix for debugging
    print("Distance Matrix:")
    for row in distance_matrix:
        print(row)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        data['num_vehicles'],
        data['depot']
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    distance = to_miles(solution.ObjectiveValue())
    print(f'Objective: {distance} miles')
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    print('Route distance: {} miles\n'.format(to_miles(route_distance)))

if __name__ == '__main__':
    main()
