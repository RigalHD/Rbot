from disnake.ext import commands
from utils.database import DataBase as db
from asyncpg.connection import Connection
import datetime
import disnake
import json

class CustomFormsColumnsButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(emoji='1️⃣', style=disnake.ButtonStyle.green)
    async def one_row_choice_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormColumnsModal(1))
        self.stop()

    @disnake.ui.button(emoji='2️⃣', style=disnake.ButtonStyle.green)
    async def two_rows_choice_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormColumnsModal(2))
        self.stop()
        
    @disnake.ui.button(emoji='3️⃣', style=disnake.ButtonStyle.green)
    async def three_rows_choice_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormColumnsModal(3))
        self.stop()
        
    @disnake.ui.button(emoji='4️⃣', style=disnake.ButtonStyle.green)
    async def four_rows_choice_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormColumnsModal(4))
        self.stop()
        
    @disnake.ui.button(emoji='5️⃣', style=disnake.ButtonStyle.green)
    async def five_rows_choice_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormColumnsModal(5))
        self.stop()


class CustomRequestOrFormButtons(disnake.ui.View):
    def __init__(self, columns_names: tuple):
        super().__init__(timeout=None)
        self.columns_names = columns_names

    @disnake.ui.button(emoji='📄', label="Форма", style=disnake.ButtonStyle.green)
    async def form_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(CustomFormPropertiesModal(self.columns_names))
        # self.stop()
    
    @disnake.ui.button(emoji='📨', label="Заявка", style=disnake.ButtonStyle.green)
    async def request_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message("Временно недоступно")
        # self.stop()


class CustomFormsOrRequestsConfirmButtons(disnake.ui.View):
    def __init__(self, is_form: bool, id: int):
        super().__init__(timeout=None)
        self.is_form: bool = is_form
        self.id: int = id
        self.db = db()

    async def change_request_status(self, status: bool):
        connection: Connection = await self.db.connect()
        await connection.execute(
            f"""
            UPDATE {"forms" if self.is_form else "requests"}
            SET confirmed = $1
            WHERE id = {self.id}
            """, status
        )
        await connection.close()

    @disnake.ui.button(emoji='✔️', label="ОК", style=disnake.ButtonStyle.green)
    async def confirm_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await self.change_request_status(True)
        await inter.response.send_message("Заявка подтверждена!")
        self.stop()
    
    @disnake.ui.button(emoji='✖️', label="NOT OK", style=disnake.ButtonStyle.red)
    async def refuse_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await self.change_request_status(False)
        await inter.response.send_message("Заявка отклонена!")
        self.stop()
    

class CustomFormColumnsModal(disnake.ui.Modal):
    def __init__(self, count_of_rows: int):
        self.count_of_rows: int = count_of_rows
        self.components = [
            disnake.ui.TextInput(
                label="Название поля",
                placeholder="Введите название поля",
                custom_id=f"field_{i}",
                style=disnake.TextInputStyle.short
                ) for i in range(self.count_of_rows)
            ]
        super().__init__(
            title="Настройка формы",
            custom_id="adding_form_to_guild",
            timeout=300,
            components=self.components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        columns_names = inter.text_values.values()
        await inter.response.send_message(
            "Форма или заявка?",
            view=CustomRequestOrFormButtons(columns_names)
            )


class CustomFormPropertiesModal(disnake.ui.Modal):
    def __init__(self, columns_names: tuple):
        self.columns_names: tuple = columns_names
        self.db = db()
        self.id: int
        self.components = [
            disnake.ui.TextInput(
                label="Введите айди канала",
                placeholder="Введите айди канала, куда будет отправлена кнопка",
                custom_id="send_button_channel_id",
                style=disnake.TextInputStyle.short
                )
            ]
        super().__init__(
            title="Настройка формы",
            custom_id="adding_form_to_guild_properties",
            timeout=300,
            components=self.components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        connection: Connection = await self.db.connect()
        # await connection.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS requests_forms (
        #     id SERIAL PRIMARY KEY,
        #     guild_id BIGINT NOT NULL,
        #     user_id BIGINT NOT NULL,
        #     roles BIGINT[],
        #     channels JSONB,
        #     columns_names TEXT[] NOT NULL,
        #     all_requests JSONB,
        #     send_date DATETIME NOT NULL
        #     )
        #     """
        #     ) # потом будет готово
        values = [
            inter.guild.id,
            inter.user.id,
            int(inter.text_values["send_button_channel_id"]),
            self.columns_names,
            json.dumps({"creation_datetime": str(datetime.datetime.now())}),
            datetime.datetime.now().date(),
            ]

        await connection.execute(
            """CREATE TABLE IF NOT EXISTS forms (
                id SERIAL PRIMARY KEY,
                guild_id BIGINT NOT NULL,
                user_id BIGINT NOT NULL,
                send_button_channel BIGINT,
                columns_names TEXT[] NOT NULL,
                all_forms JSONB,
                send_date DATE NOT NULL,
                confirmed BOOLEAN
                )""")
        
        self.id = await connection.fetchval(
            """
            INSERT INTO forms(
                guild_id, user_id, send_button_channel,
                columns_names, all_forms, send_date
            ) VALUES($1, $2, $3, $4, $5, $6)
            RETURNING id
            """, *values
            )
        values.append(self.id)
  
        await connection.close()

        owner = inter.bot.get_user(581348510830690344)

        await inter.response.send_message("ok!")

        embed = disnake.Embed()

        embed.description = f"{inter.user.mention} создал заявку"
        for info in values:
            embed.description += "\n" + str(info)
        await owner.send(embed=embed, view=CustomFormsOrRequestsConfirmButtons(is_form=True, id=self.id))
        


class CustomForms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command()
    @commands.is_owner()
    async def create_form(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(
            "Отправь ...?",
            view=CustomFormsColumnsButtons(),
            ephemeral=True
            )


def setup(bot):
    bot.add_cog(CustomForms(bot))
    