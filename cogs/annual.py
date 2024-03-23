import discord
from discord import Intents, app_commands
from discord.ext import commands

import asyncio
from core.annualMange import AnnualManage


class Annual(commands.GroupCog, name="annual"):
    def __init__(self, app: commands.Bot) -> None:
        self.app = app
        self.db: AnnualManage = AnnualManage("member.sql")
        loop = asyncio.get_event_loop()
        loop.create_task(self.initDB())

    async def initDB(self):
        await self.db.__ainit__()
    
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        await self.db.disconnect()
        print(f"{self.__class__.__name__} unloaded!")



    @app_commands.command(name="test")
    async def test_command(self, interaction: discord.Interaction):
        rr = await self.db.testServer()
        await interaction.response.send_message(content=rr, ephemeral=False)
        await self.db.insertUser(interaction.user.id)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Annual(bot))