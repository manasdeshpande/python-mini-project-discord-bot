#main
import os
from discord.ext import commands
import discord
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    async with bot:
        await load_extensions()
        await bot.start('your token')


@bot.event
async def on_member_join(member):
    # Get the system channel for the member's guild
    channel = member.guild.system_channel
    if channel is not None:
        # Send a welcome message to the system channel
        welcome_message = f"Welcome to the server, {member.mention}! Type `!help` to see a list of my commands."
        await channel.send(welcome_message)


@bot.event
async def on_guild_join(guild):
    # Send a message to the general channel of the server
    for channel in guild.text_channels:
        if channel.name == "general":
            await channel.send("Hi! I'm your new bot. Type !help for a list of commands.")
            break


asyncio.run(main())
