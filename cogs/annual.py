import discord
from discord import Intents, app_commands
from discord.ext import commands

import asyncio
from core.annualMange import AnnualManage
from core.model.memberModel import MemberModel


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



    @app_commands.command(name="정보")
    async def info_command(self, interaction: discord.Interaction):
        count = await self.db.getUserAnnual(interaction.user.id)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="B1ND 연차",
                description=f"당신의 연차는 {count}개 남았습니다."
            ),
            ephemeral=False,
        )
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Annual(bot))