import discord
from discord import app_commands
from dotenv import load_dotenv
import os

import database

load_dotenv()

TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    database.setup()
    await tree.sync()
    print("Bot started")


async def send_accounts(interaction, type, amount):

    accounts = database.get_accounts(type, amount)

    if len(accounts) == 0:
        await interaction.response.send_message(
            "Nėra laisvų paskyrų."
        )
        return


    msg = f"{type.upper()} paskyros:\n\n"

    for i, acc in enumerate(accounts,1):
        msg += (
            f"{i}.\n"
            f"Login: `{acc[1]}`\n"
            f"Password: `{acc[2]}`\n\n"
        )

    await interaction.response.send_message(msg)


@tree.command(name="fivem")
async def fivem(interaction: discord.Interaction, kiekis:int):
    await send_accounts(interaction,"fivem",kiekis)


@tree.command(name="discord")
async def discord_acc(interaction: discord.Interaction,kiekis:int):
    await send_accounts(interaction,"discord",kiekis)


@tree.command(name="steam")
async def steam(interaction: discord.Interaction,kiekis:int):
    await send_accounts(interaction,"steam",kiekis)


@tree.command(name="addfivem")
async def addfivem(interaction:discord.Interaction,login:str,password:str):

    database.add_account(
        "fivem",
        login,
        password
    )

    await interaction.response.send_message(
        "FiveM paskyra pridėta."
    )


@tree.command(name="addsteam")
async def addsteam(interaction:discord.Interaction,login:str,password:str):

    database.add_account(
        "steam",
        login,
        password
    )

    await interaction.response.send_message(
        "Steam paskyra pridėta."
    )


@tree.command(name="adddiscord")
async def adddiscord(interaction:discord.Interaction,login:str,password:str):

    database.add_account(
        "discord",
        login,
        password
    )

    await interaction.response.send_message(
        "Discord paskyra pridėta."
    )


@tree.command(name="stock")
async def stock(interaction:discord.Interaction):

    text = (
        f"FiveM: {database.stock('fivem')}\n"
        f"Discord: {database.stock('discord')}\n"
        f"Steam: {database.stock('steam')}"
    )

    await interaction.response.send_message(text)


bot.run(TOKEN)
