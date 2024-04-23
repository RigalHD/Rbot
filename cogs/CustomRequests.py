from disnake.ext import commands
from utils.database import DataBase as db
import disnake


class CustomFormsButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    # temporary unusable
    @disnake.ui.button(
        label="INT",
        emoji="📋",
        style=disnake.ButtonStyle.green,
        custom_id="requests_send_button"
    )
    async def customm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormModal())
        


class CustomFormModal(disnake.ui.Modal):
    def __init__(self):
        self.db = db()
        self.components = [
            disnake.ui.TextInput(
                label="Количество пунктов в форме",
                placeholder="От 1 до 5",
                custom_id="count_of_rows",
                style=disnake.TextInputStyle.short
                ),
            ]
        super().__init__(
            title="Добавление формы",
            custom_id="adding_form_to_guild",
            timeout=300,
            components=self.components,
        )


class CustomForms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(CustomForms(bot))
    