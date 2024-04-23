import asyncpg
import os

class DataBase:
    def __init__(self) -> None:
        self.connection = None
    
    async def connect(self):
        self.connection = await asyncpg.connect(
            host="localhost",
            database="RbotDB",
            user="postgres",
            password=os.getenv("RBOTDB_PASSWORD"),
            port=5432,
        )
        return self.connection
