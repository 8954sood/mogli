import discord
from discord import Intents, app_commands
from discord.ext import commands

import asyncio
from core.annualMange import AnnualManage
from core.model.memberModel import MemberModel
import os
from typing import Optional
import datetime


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

    async def getLogChannel(self) -> discord.abc.GuildChannel | discord.abc.PrivateChannel | discord.Thread:
        return await self.app.fetch_channel(os.environ.get("log"))
    
    async def sendLogChannel(self, category: str, user: Optional[discord.User | discord.Member], **args):
        userInfo = await self.db.getUser(user.id)
        if (category == "연차"):
            if user == None:
                return

            nowAnnual = await self.db.getUserAnnualCount(user.id)
            await (await self.getLogChannel()).send(
                embed=discord.Embed(
                    title="연차 사용 로그",
                    description=f"사용자 : {user.mention}\n사용자ID : {user.id}\n연차 개수 : {nowAnnual+int(args['useCnt'])} -> {nowAnnual}\n시간 : {datetime.datetime.now()}"
                )
            )
        

    @app_commands.command(name="정보")
    async def info_command(self, interaction: discord.Interaction):
        count = await self.db.getUserAnnualCount(interaction.user.id)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="B1ND 연차",
                description=f"당신의 연차는 {count}개 남았습니다."
            ),
            ephemeral=False,
        )

    @app_commands.command(name="연차사용")
    async def use_annaul_command(self, interaction: discord.Interaction):
        db = self.db
        log = self.sendLogChannel
        class AnnualModal(discord.ui.Modal, title='연차 사용'):
            annual = discord.ui.TextInput(
                label="언제 연차를 사용하실건가요?",
                placeholder="8,9",
            )

            reason = discord.ui.TextInput(
                label="연차를 사용하는 사유를 적어주세요.",
                style=discord.TextStyle.long,
                placeholder="대회에 결과물을 제출하기전 회의가 꼭 필요해 연차를 신청합니다.",
                max_length=300,
                min_length=10
            )

            async def on_submit(self, interaction: discord.Interaction):
                annualCnt = len(list(map(int, self.annual.value.split(","))))

                isSuccess, cause = await db.insertUerAnnual(
                    userId=interaction.user.id,
                    annual=self.annual.value,
                    annualCnt=annualCnt,
                    reason=self.reason.value
                )
                
                if (isSuccess is True):
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="연차 사용 성공",
                            description=f"연차 {annualCnt}개를 소모하였습니다.",
                            colour=discord.Colour.green()
                        )
                    )
                    await log(
                        category="연차", 
                        user=interaction.user,
                        useCnt=annualCnt
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="연차 사용 실패",
                            description=f"사유: {cause}",
                            colour=discord.Colour.red()
                        )
                    )

            async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
                await interaction.response.send_message(
                        embed=discord.Embed(
                            title="연차 사용 실패",
                            description=f"사유: {error}",
                            colour=discord.Colour.red()
                        )
                    )
                print(error)
        await interaction.response.send_modal(AnnualModal())
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Annual(bot))