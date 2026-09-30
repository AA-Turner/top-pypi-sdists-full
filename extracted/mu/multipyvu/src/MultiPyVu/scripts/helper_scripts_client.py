"""
A few helpful client scripts used in the MultiPyVu module
"""


from MultiPyVu.MultiVuClient import Client


def run_status(ip: str, port: int):
    """
    Queries the server for its status.
    """
    ip_address = ip
    if ip_address == '0.0.0.0':
        ip_address = 'localhost'

    client = Client(host=ip_address,
                    port=port)
    response = client.get_server_status()
    print(f'Server status: {response}')


def is_running(ip: str, port: int):
    """
    Queries the server to see if it is running
    """
    ip_address = ip
    if ip_address == '0.0.0.0':
        ip_address = 'localhost'

    client = Client(host=ip_address,
                    port=port)
    response = client.is_server_running()
    if response:
        print(f'Server is running at {client.address}')
    else:
        print(f'Server not running at {client.address}')


def force_quit(ip: str, port: int) -> str:
    """
    Quits the server.
    """
    ip_address = ip
    if ip_address == '0.0.0.0':
        ip_address = 'localhost'

    client = Client(host=ip_address,
                    port=port)
    response = client.force_quit_server()
    if response:
        return response
    else:
        return f'Sent quit command to {client.address}'
