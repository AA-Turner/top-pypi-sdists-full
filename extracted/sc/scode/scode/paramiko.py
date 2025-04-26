import time
import paramiko


def ssh_connect(hostname: str, username: str, password: str, timeout: float = None) -> paramiko.SSHClient:
    """
    > This function takes a hostname, username, and password as arguments and returns an SSHClient
    object
    
    :param hostname: The IP address or hostname of the server you want to connect to
    :type hostname: str
    :param username: The username to log into the server with
    :type username: str
    :param password: The password for the user you're logging in as
    :type password: str
    :return: A SSHClient object.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password, timeout=timeout)
    return ssh


def command(ssh: paramiko.SSHClient, query: str, timeout: float = None, sleep: float = 1):
    """
    It executes a command on a remote server and returns the output and error text
    
    :param ssh: paramiko.SSHClient
    :type ssh: paramiko.SSHClient
    :param query: The command you want to run on the remote server
    :type query: str
    :param timeout: The time in seconds to wait for the command to finish. If the command doesn't finish
    in the given time, the function will return the output of the command so far
    :type timeout: float
    :return: stdout_text, err_text
    """

    stdin, stdout, stderr = ssh.exec_command(query)
    
    if timeout:
        start_time = time.time()
    
    # Wait for the command to terminate  
    while not stdout.channel.exit_status_ready():
        time.sleep(sleep)
        if timeout:
            latest_time = time.time()

            if latest_time - start_time > timeout:
                stdout_text = stdout.read().decode('utf-8')
                err_text = stderr.read().decode('utf-8').strip()
                return stdout_text, err_text
    
    stdout_text = stdout.read().decode('utf-8')
    err_text = stderr.read().decode('utf-8').strip()
    return stdout_text, err_text


def execute_sql_query(ssh: paramiko.SSHClient, user_id: str, user_pw: str, db_name: str, query: str, timeout = None, sleep: float = 1):
    """execute sql query

    Args:
        ssh (paramiko.SSHClient): paramiko ssh client.
        user_id (str): ID to log in.
        user_pw (str): Password to log in.
        db_name (str): Name of the database to be connected to.
        query (str): query statement to execute.

    Returns:
        tuple[str, str]: stdout, stderr
    """    
    query = query.replace('\'','\"')
    fquery = f"""mysql -u{user_id} -p{user_pw} {db_name} -e '{query}'"""
    return command(ssh, fquery, timeout=timeout, sleep=sleep)
