import discord
from discord import app_commands

from dotenv import load_dotenv

import os
import asyncio

import database

from permissions import is_admin
from embeds import account_embed, stock_embed



load_dotenv()

TOKEN = os.getenv("TOKEN")



intents = discord.Intents.default()


bot = discord.Client(
    intents=intents
)


tree = app_commands.CommandTree(bot)


stock_message = None



@bot.event
async def on_ready():

    database.setup()

    await tree.sync()

    bot.loop.create_task(
        update_stock()
    )

    print(
        f"Prisijungta: {bot.user}"
    )



async def update_stock():

    global stock_message


    while True:


        if stock_message:


            embed = stock_embed(

                database.get_stock("fivem"),

                database.get_stock("discord"),

                database.get_stock("steam")

            )


            await stock_message.edit(
                embed=embed
            )


        await asyncio.sleep(30)




async def send_accounts(interaction, account_type, amount):


    accounts = database.get_accounts(
        account_type,
        amount
    )


    if not accounts:


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




@tree.command(name="fivem")
async def fivem(
    interaction: discord.Interaction,
    kiekis:int
):

    if await is_admin(interaction):

        await send_accounts(
            interaction,
            "fivem",
            kiekis
        )




@tree.command(name="discord")
async def discord_accounts(
    interaction: discord.Interaction,
    kiekis:int
):

    if await is_admin(interaction):

        await send_accounts(
            interaction,
            "discord",
            kiekis
        )




@tree.command(name="steam")
async def steam(
    interaction: discord.Interaction,
    kiekis:int
):

    if await is_admin(interaction):

        await send_accounts(
            interaction,
            "steam",
            kiekis
        )




@tree.command(name="addfivem")
async def addfivem(
    interaction:discord.Interaction,
    login:str,
    password:str
):

    if await is_admin(interaction):

        database.add_account(
            "fivem",
            login,
            password
        )


        await interaction.response.send_message(
            "✅ FiveM pridėta.",
            ephemeral=True
        )




@tree.command(name="adddiscord")
async def adddiscord(
    interaction:discord.Interaction,
    login:str,
    password:str
):

    if await is_admin(interaction):

        database.add_account(
            "discord",
            login,
            password
        )


        await interaction.response.send_message(
            "✅ Discord pridėta.",
            ephemeral=True
        )




@tree.command(name="addsteam")
async def addsteam(
    interaction:discord.Interaction,
    login:str,
    password:str
):

    if await is_admin(interaction):

        database.add_account(
            "steam",
            login,
            password
        )


        await interaction.response.send_message(
            "✅ Steam pridėta.",
            ephemeral=True
        )





@tree.command(name="stock")
async def stock(
    interaction:discord.Interaction
):

    global stock_message


    if await is_admin(interaction):


        embed = stock_embed(

            database.get_stock("fivem"),

            database.get_stock("discord"),

            database.get_stock("steam")

        )


        await interaction.response.send_message(
            embed=embed
        )


        stock_message = await interaction.original_response()



bot.run(TOKEN)
