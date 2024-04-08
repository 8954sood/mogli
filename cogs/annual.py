import discord
from discord import app_commands
from discord.ext import commands

import asyncio
import os
from typing import Optional
import datetime

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

    async def getLogChannel(self) -> discord.abc.GuildChannel | discord.abc.PrivateChannel | discord.Thread:
        return await self.app.fetch_channel(os.environ.get("log"))
    
    async def sendLogChannel(self, category: str, user: discord.User | discord.Member, **args):
        '''
        Param category: 연차 
        '''
        userInfo = await self.db.getUser(user.id)
        if (category == "연차"):
            if user == None:
                return

            nowAnnual = await self.db.getUserAnnualCount(user.id)
            await (await self.getLogChannel()).send(
                embed=discord.Embed(
                    title="연차 사용 로그",
                    description=f'''
                                사용자 : {user.mention}{f"({userInfo.name})" if userInfo.name != None else ""}
                                사용자ID : {user.id}
                                연차 개수 : {nowAnnual+int(args['useCnt'])} -> {nowAnnual}
                                연차 사용 교시 : {args["annual"]}교시
                                사유 : {args["reason"]}
                                이벤트 발생 시간 : {datetime.datetime.now()}
                                '''
                )
            )
        

    @app_commands.command(name="정보")
    async def info_command(self, interaction: discord.Interaction, target: Optional[discord.User | discord.Member]):
        if (target != None):
            userInfo = await self.db.getUser(
                userId=target.id, 
                userName=target.display_name
            )
            count = await self.db.getUserAnnualCount(
                userId=target.id, 
                userName=target.display_name
            )
        else:
            userInfo = await self.db.getUser(
                userId=interaction.user.id, 
                userName=interaction.user.display_name
            )
            count = await self.db.getUserAnnualCount(
                userId=interaction.user.id, 
                userName=interaction.user.display_name
            )
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"B1ND({userInfo.name}) 연차",
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
                        useCnt=annualCnt,
                        reason=self.reason.value,
                        annual=self.annual.value
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

    @commands.command("강제설정")
    async def user_set_command(self, ctx: commands.Context, user: discord.User | discord.Member, annual: str | int):
        ""
        if (not ctx.author.id in [464712715487805442, 809432781604126740]):
            return
        message = await ctx.send(
            embed=discord.Embed(
                title="작업을 진행하고 있습니다.",
                color=discord.Color.dark_blue()
            )
        )
        try:
            admin = await self.db.getUser(
                userId=ctx.author.id,
                userName=ctx.author.display_name
            )

            #db에 유저 생성
            await self.db.getUser(
                userId=user.id,
                userName=user.display_name
            )
            setAnnual = "관리자에 의한 강제 사용"
            if isinstance(annual, str):
                setAnnual = annual
                annual = len(list(map(int, annual.split(","))))

            for i in range(annual):
                await self.db.insertUerAnnual(
                    userId=user.id,
                    annual=setAnnual,
                    annualCnt=1,
                    reason="관리자에 의한 강제 사용"
                )
                await self.sendLogChannel(
                    category="연차",
                    user=user,
                    useCnt=1,
                    reason=f"관리자({admin.name})에 의한 강제 사용",
                    annual=setAnnual
                )
            await message.edit(
                content=".",
                embed=None
            )
            await message.edit(
                content="",
                embed=discord.Embed(
                    title="정상적으로 처리되었습니다.",
                    color=discord.Color.green()
                )
            )
        except Exception as Error:
            await message.edit(
                content=".",
                embed=None
            )
            await message.edit(
                content="",
                embed=discord.Embed(
                    title="실패",
                    description=f"사유 : {Error}",
                    color=discord.Color.red()
                )
            )


        
        

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Annual(bot))