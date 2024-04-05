from discord.ext import commands
import discord


class Help(commands.Cog):
    def __init__(self, app: commands.Bot) -> None:
        self.app = app
        self.commands = {
            "강제설정": '''
                    !강제설정 **{MENTION}** **{INT}**
                    !강제설정 **{MENTION}** **{STR}**

                    example)
                    
                    !강제설정 @박병준 "3, 4" -> Means 박병준 use annual two count
                    !강제설정 @박병준 2 -> Means 박병준 use annual two count
                    '''
        }

    @commands.command("help")
    async def help_command(self, ctx: commands.Context):
        embed = discord.Embed(title="모글리 명령어")
        for key, item in self.commands.items():
            embed.add_field(
                name=key,
                value=item
            )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Help(bot))