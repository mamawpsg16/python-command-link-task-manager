from psycopg2 import OperationalError, connect
from dotenv import load_dotenv
import os

import logging

# Configure logger
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


conn_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

class DatabaseConnection():
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = connect(**conn_params)
            return self.connection
        except OperationalError as error:
            logger.critical(f"Database Connection Error : {error}")
            self.connection = None

    def close(self):
        if self.connection is not None:
            self.connection.close()

            