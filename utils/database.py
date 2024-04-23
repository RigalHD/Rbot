from typing import Dict, Any
import asyncpg
import os
import re


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

    async def create_table(
            self,
            table_name: str,
            columns_and_types: Dict[str, str]
            ) -> bool:     
        pass