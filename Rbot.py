from disnake.ext import commands
import asyncpg
import os

class RBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.pool = None

    async def start(self, *args, **kwargs):
        self.pool = await asyncpg.create_pool(
            host="localhost",
            database="RbotDB",
            user="postgres",
            password=os.getenv("RBOTDB_PASSWORD"),
            port=5432,
        )
        await super().start(*args, **kwargs)

    async def close(self):
        await self.pool.close()
        await super().close()