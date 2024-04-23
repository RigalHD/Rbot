from disnake.ext import commands
import disnake


class RequestsModal(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
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
        
        conn = await self.pool.acquire()
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS discord_guild_requests(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            about TEXT NOT NULL
            )"""
            )
        await conn.execute(
            """
            INSERT INTO discord_guild_requests(name, age, about) 
            VALUES($1, $2, $3)
            """, *user_info)
        
        await self.pool.release(conn)
        
        await inter.response.send_message("Успешно!", ephemeral=True)


class Requests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.is_owner()
    async def request_to_guild(self, inter: disnake.CommandInteraction):
        await inter.response.send_modal(RequestsModal(self.bot))
                


def setup(bot):
    bot.add_cog(Requests(bot))
    