from disnake.ext import commands
from utils.database import DataBase as db
import disnake


class CustomRequestsButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    # temporary unusable
    @disnake.ui.button(
        label="INT",
        emoji="📋",
        style=disnake.ButtonStyle.green,
        custom_id="requests_send_button"
    )
    async def requests_send_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomRequestsModal())
        


class CustomRequestsModal(disnake.ui.Modal):
    pass
            


class CustomRequests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(CustomRequests(bot))
    