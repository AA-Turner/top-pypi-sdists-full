import socket

MY_HOST = None

def get_my_host():
    global MY_HOST

    if MY_HOST:
       return MY_HOST

    MY_HOST = get_ip_from_hostname('host.docker.internal')
    if not MY_HOST:
       MY_HOST = socket.gethostname()

    if not MY_HOST:
       MY_HOST = 'NA'

    return MY_HOST

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None