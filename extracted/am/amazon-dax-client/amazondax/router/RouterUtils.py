import random


def random_route(prev_client, routes):
    '''Select a random route, avoiding prev_client when alternatives exist.'''
    if not routes:
        return None
    if len(routes) == 1:
        return routes[0]
    i = random.randrange(len(routes))
    route = routes[i]
    if route.client is prev_client:
        route = routes[(i + 1) % len(routes)]
    return route
