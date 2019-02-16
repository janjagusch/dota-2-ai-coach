import pyhdb
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(dotenv_path=".env", verbose=True)


class HanaConnector():
    """ connects to the HANA Database and executes the sql queries
    example:
        hana = HanaConnector()
        print(hana.execute("SELECT 'Hello Python World' FROM DUMMY"))
        hana.close()
    """

    def __init__(self):
        self.connection = None

    def __del__(self):
        self.close()

    def execute(self, sql):
        if self.connection == None:
            self.connection = pyhdb.connect(
                host=os.getenv("HANA_DB"),
                port=os.getenv("HANA_PORT"),
                user=os.getenv("HANA_USER"),
                password=os.getenv("HANA_PW"),
                encrypt=True,
                encrypt_verify=False
            )
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def close(self):
        if not self.connection == None:
            self.connection.close()
            self.connection = None
