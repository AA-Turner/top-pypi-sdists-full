import traceback

from BoschRpaMagicBox.smb_functions import *
from BoschRpaMagicBox.database_functions import *


class MiniRpaDatabaseAutomation:
    def __init__(self, user_name: str, user_password: str, server_name: str, share_name: str, port: int):
        """

        Args:
            user_name(str): This is the username
            user_password(str): This is the password
            server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
            share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
            port(int): This is the port number of the server name
        """
        self.user_name = user_name
        self.user_password = user_password
        self.server_name = server_name
        self.share_name = share_name
        self.port = port
        self.mysql_connection = None

        self.database_host = None
        self.database_port = None
        self.database_user = None
        self.database_password = None
        self.database_name = None

    def connect_to_mysql_server(self, database_host, database_port, database_user, database_password, database_name):
        """ This function is used to connect to the mysql server.

        Args:
            database_host(str): The host of the MySQL server.
            database_port(int): The port of the MySQL server.
            database_user(str): The user of the MySQL server.
            database_password(str): The password of the MySQL server.
            database_name(str): The database of the MySQL server.

        """
        # try:
        (self.database_host,
         self.database_port,
         self.database_user,
         self.database_password,
         self.database_name) = (
            database_host,
            database_port,
            database_user,
            database_password,
            database_name)
        self.mysql_connection = start_mysql_server_connection(self.database_host, self.database_port, self.database_user, self.database_password, self.database_name)
        print("Connected to MySQL server successfully!")

    def disconnect_from_mysql_server(self):
        """ This function is used to disconnect from the mysql server.
        """
        if self.mysql_connection:
            close_mysql_server_connection(self.mysql_connection)
            self.mysql_connection = None
            print("Disconnected from MySQL server successfully!")
        else:
            print("No MySQL connection to close!")

    def fetch_mysql_data_and_save_data(self, sql_query, username, password, server_name, share_name, remote_file_path, port=445, sheet_name='Sheet1', sql_query_params=None):
        """ This function is used to fetch data from the mysql server and save data into an Excel file.

        Args:
            sql_query(str): The SQL query to execute.
            username(str): This is the username
            password(str): This is the password
            server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
            share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
            remote_file_path(str): This is the public file path that file will be saved under share name folder
            port(int): This is the port number of the server name
            sheet_name(str): The name of the sheet in the Excel file.
            sql_query_params(tuple): The parameters for the SQL query.
        """
        if self.mysql_connection:
            save_mysql_data_to_excel(self.database_host, self.database_port, self.database_user, self.database_password, self.database_name, sql_query, username, password,
                                     server_name, share_name, remote_file_path, port, sheet_name, sql_query_params)
        else:
            print("No MySQL connection to fetch data from.")
