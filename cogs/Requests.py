from disnake.ext import commands
from utils.database import DataBase as db
import disnake


class RequestsSendButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Отправить заявку",
        emoji="📋",
        style=disnake.ButtonStyle.green,
        custom_id="requests_send_button"
    )
    async def requests_send_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(RequestsModal())


class RequestsModal(disnake.ui.Modal):
    def __init__(self):
        self.db = db()
        self.components = [
            disnake.ui.TextInput(
                label="Ваше имя",
                placeholder="Ваше имя",
                custom_id="name",
                style=disnake.TextInputStyle.short
                ),
            disnake.ui.TextInput(
                label="Ваш возраст",
                placeholder="Ваш возраст",
                custom_id="age",
                style=disnake.TextInputStyle.short
                ),
            disnake.ui.TextInput(
                label="О вас",
                placeholder="Немного о себе",
                custom_id="about",
                style=disnake.TextInputStyle.paragraph
                ),
            ]
        super().__init__(
            title="Заявка на сервер",
            custom_id="request_to_guild",
            timeout=300,
            components=self.components,
        )
    
    async def callback(self, inter: disnake.ModalInteraction):
        user_info = list(inter.text_values.values())
        user_info[1] = int(user_info[1])

        connection = await self.db.connect()

        try:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS discord_guild_requests(
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                about TEXT NOT NULL
                )"""
                )
            
            await connection.execute(
                """
                INSERT INTO discord_guild_requests(name, age, about) 
                VALUES($1, $2, $3)
                """, *user_info)
            a = await self.db.create_table("t", {"colname": "TEXT"})
            if a is None:
                print("!")
            await inter.response.send_message("Успешно!", ephemeral=True)

        except Exception as e:
            raise e

        finally:
            await connection.close()
            


class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.is_owner()
    async def request_to_guild(self, inter: disnake.CommandInteraction):
        await inter.response.send_message("Отправь заявку!", view=RequestsSendButton())


def setup(bot):
    bot.add_cog(Requests(bot))
    