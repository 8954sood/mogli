import discord
from discord import Intents, app_commands
from discord.ext import commands


class Annual(commands.GroupCog, name="annual"):
    def __init__(self, app: commands.Bot) -> None:
        self.app = app

    @app_commands.command(name="test")
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Annual(bot))