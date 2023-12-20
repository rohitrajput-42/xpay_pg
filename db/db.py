import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from functools import lru_cache

class Database: 
    def __init__(self):
        self.min_connections = 1
        self.max_connections = 5
        try:
            self.connection_pool = ThreadedConnectionPool(
                self.min_connections,
                self.max_connections,

                user='xpay',
                password = '1234',
                host='localhost',
                port=5432,
                database='xpay_db'
            )
            print(self.connection_pool)
            if self.connection_pool:
                print("Connection pool created successfully")
        except (Exception, psycopg2.Error) as error:
            self.connection_pool = "ERROR"
            print("Error while connecting to PostgreSQL", error)

    @lru_cache
    def get_connection(self):
        return self.connection_pool.getconn() #creating the connection

    def put_connection(self, connection):
        print("Connection released to pool")
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        self.connection_pool.closeall()

def get_db():
    db = Database()
    return db