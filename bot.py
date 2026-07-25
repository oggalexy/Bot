import discord
from discord import app_commands
from dotenv import load_dotenv
import os

import database

from permissions import is_admin
from embeds import account_embed


load_dotenv()

TOKEN = os.getenv("TOKEN")


intents = discord.Intents.default()

bot = discord.Client(
    intents=intents
)

tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():

    database.setup()

    await tree.sync()

    print(f"Prisijungta kaip {bot.user}")


async def send_accounts(interaction, account_type, amount):

    accounts = database.get_accounts(
        account_type,
        amount
    )

    if len(accounts) == 0:

        await interaction.response.send_message(
            "❌ Nėra laisvų paskyrų.",
            ephemeral=True
        )

        return


    embed = account_embed(
        account_type,
        accounts,
        interaction.user
    )


    await interaction.response.send_message(
        embed=embed
    )



# =========================
# GET ACCOUNTS
# =========================


@tree.command(
    name="fivem",
    description="Gauti FiveM paskyras"
)
async def fivem(
    interaction: discord.Interaction,
    kiekis: int
):

    if await is_admin(interaction):

        await send_accounts(
            interaction,
            "fivem",
            kiekis
        )



@tree.command(
    name="discord",
    description="Gauti Discord paskyras"
)
async def discord_accounts(
    interaction: discord.Interaction,
    kiekis: int
):

    if await is_admin(interaction):

        await send_accounts(
            interaction,
            "discord",
            kiekis
        )



@tree.command(
    name="steam",
    description="Gauti Steam paskyras"
)
async def steam(
    interaction: discord.Interaction,
    kiekis: int
):

    if await is_admin(interaction):

        await send_accounts(
            interaction,
            "steam",
            kiekis
        )



# =========================
# ADD ACCOUNTS
# =========================


@tree.command(
    name="addfivem",
    description="Pridėti FiveM paskyrą"
)
async def addfivem(
    interaction: discord.Interaction,
    login: str,
    password: str
):

    if await is_admin(interaction):

        database.add_account(
            "fivem",
            login,
            password
        )

        await interaction.response.send_message(
            "✅ FiveM paskyra pridėta.",
            ephemeral=True
        )



@tree.command(
    name="addsteam",
    description="Pridėti Steam paskyrą"
)
async def addsteam(
    interaction: discord.Interaction,
    login: str,
    password: str
):

    if await is_admin(interaction):

        database.add_account(
            "steam",
            login,
            password
        )

        await interaction.response.send_message(
            "✅ Steam paskyra pridėta.",
            ephemeral=True
        )



@tree.command(
    name="adddiscord",
    description="Pridėti Discord paskyrą"
)
async def adddiscord(
    interaction: discord.Interaction,
    login: str,
    password: str
):

    if await is_admin(interaction):

        database.add_account(
            "discord",
            login,
            password
        )

        await interaction.response.send_message(
            "✅ Discord paskyra pridėta.",
            ephemeral=True
        )



# =========================
# STOCK
# =========================


@tree.command(
    name="stock",
    description="Parodyti paskyrų kiekį"
)
async def stock(
    interaction: discord.Interaction
):

    if await is_admin(interaction):

        embed = discord.Embed(
            title="📦 Account Stock",
            color=discord.Color.blue()
        )


        embed.add_field(
            name="🟢 FiveM",
            value=f"`{database.get_stock('fivem')}`",
            inline=False
        )


        embed.add_field(
            name="🟣 Discord",
            value=f"`{database.get_stock('discord')}`",
            inline=False
        )


        embed.add_field(
            name="🟠 Steam",
            value=f"`{database.get_stock('steam')}`",
            inline=False
        )


        await interaction.response.send_message(
            embed=embed
        )



bot.run(TOKEN)
