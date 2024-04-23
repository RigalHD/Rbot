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
            columns_and_types: Dict[str, Any] = ""
            ):     
        self.connection = await self.connect()
        table_name = re.sub(r'[^a-zA-Z0-9_]', '', table_name).replace(" ", "_")
        # for t in table_name:
        #     if not re.match(r'^[a-zA-Z0-9_]+\s+[a-zA-Z0-9_]+$', t):
        #         return
        await self.connection.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
            id SERIAL PRIMARY KEY
            )''')
        for column_name, column_type in columns_and_types.items():
            column = re.sub(
                r'[^a-zA-Z0-9_]', '', column_name
                ).replace(" ", "_") + " " + column_type
            # for col_name in column_name:
            #     if not re.match(r'^[a-zA-Z0-9_]+\s+[a-zA-Z0-9_]+$', col_name):
            #         return
            query = f"""
            ALTER TABLE {table_name}
            ADD COLUMN IF NOT EXISTS {column}
            """
            await self.connection.execute(query)
        await self.connection.close()
        return True
        