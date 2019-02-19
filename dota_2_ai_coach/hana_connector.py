"""
hana_connector holds an connection to the HANA database provided in the .env file

Note:
    This was tested with a PyHDB fork:
    pip install git+https://github.com/rlindner81/PyHDB.git@fb_ssl_connection
"""
import pyhdb 
from dotenv import find_dotenv, load_dotenv
import os
import pandas as pd


load_dotenv(dotenv_path=".env", verbose=True)

class HanaConnector():
    """ 
    Connects to the HANA Database and executes the sql queries
    Example:
        hana =HanaConnector()
        connection = hana.connect()
        print(pd.read_sql("SELECT 'Hello Python World' FROM DUMMY", connection))
        hana.close()
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        """
        Opens connection to the HANA database provided in the .env files
        Returns:
            sql connection object, usable for example for pandas.read_sql()
        """
        self.connection = pyhdb.connect(
            host=os.getenv("HANA_DB"),
            port=os.getenv("HANA_PORT"),
            user=os.getenv("HANA_USER"),
            password=os.getenv("HANA_PW"),
            encrypt=True,
            encrypt_verify=False
        )
        return self.connection

    def execute(self, sql):
        """
        Executes the given sql query on the HANA database
        Args:
            sql: sql query to be executed
        Returns:
            tuple of records and column names
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall(), cursor.description

    def close(self):
        """
        Closes the connection to the database
        """
        if not self.connection == None:
            self.connection.close()
            self.connection = None
