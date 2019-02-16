import pyhdb  # install with: pip install git+https://github.com/rlindner81/PyHDB.git@fb_ssl_connection
from dotenv import find_dotenv, load_dotenv
import os

import pandas as pd
load_dotenv(dotenv_path=".env", verbose=True)


class HanaConnector():
    """ connects to the HANA Database and executes the sql queries
    example:
        hana =HanaConnector()
        connection = hana.connect()
        print(pd.read_sql("SELECT 'Hello Python World' FROM DUMMY", connection))
        hana.close()
    """

    def __init__(self):
        self.connection = None

    def __del__(self):
        self.close()

    def connect(self):
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
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall(), cursor.description

    def close(self):
        if not self.connection == None:
            self.connection.close()
            self.connection = None

