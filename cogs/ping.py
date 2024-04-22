from disnake.ext import commands
import disnake

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="ping")
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Pong!")


def setup(bot):
    bot.add_cog(Ping(bot))
    