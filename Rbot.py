from disnake.ext import commands


class RBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def start(self, *args, **kwargs):
        # Можно добавить что-нибудь. Сейчас найдена замена
        await super().start(*args, **kwargs)

    async def close(self):
        await super().close()
        