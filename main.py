import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import asyncpg

load_dotenv(".env")


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


bot = RBot(
    command_prefix="!!",
    help_command=None,  
    activity=disnake.Game("NewSide"),
    intents=disnake.Intents.all(),
    status=disnake.Status.idle,
    test_guilds=[1097125882876923954, 1117027821827670089],
    )

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


def main():
    bot.run(os.getenv("RBOT_TOKEN"))


if __name__ == "__main__":
    main()
