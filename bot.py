import discord
from discord import Intents, app_commands
from discord.ext import commands

from dotenv import load_dotenv 
import os
import asyncio

app = commands.Bot(
    command_prefix="!",
    intents= Intents.all(),
)
load_dotenv()


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith("py"):
            # app.add
            print(f"loaded {filename[:-3]}")
            await app.load_extension(f"cogs.{filename[:-3]}")


@app.event
async def on_ready():
    await load()
    app.tree.copy_global_to(guild=discord.Object(id=1193910645318500463)) 
    await app.tree.sync()
    print("봇 활성화")

@app.tree.command(name="test2")
async def test2_coomand(interaction: discord.Interaction):
    await interaction.response.send_message("hihi")

@app.command("reload")
async def reload(ctx: commands.Context):
    if (ctx.author.id != 464712715487805442):
        return
    for filename in os.listdir("./cogs"):
        if filename.endswith("py"):
            # app.add
            await app.unload_extension(f"cogs.{filename[:-3]}")
            print(f"loaded {filename[:-3]}")
            await app.load_extension(f"cogs.{filename[:-3]}")
    app.tree.copy_global_to(guild=discord.Object(id=1193910645318500463)) 
    await app.tree.sync()
    
app.run(
    token=os.environ.get("token")
)