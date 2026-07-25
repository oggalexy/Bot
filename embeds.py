import discord


def account_embed(account_type, accounts, user):

    embed = discord.Embed(
        title=f"🎁 {account_type.upper()} ACCOUNTS",
        description="✅ Paskyros išduotos",
        color=discord.Color.green()
    )

    for i, acc in enumerate(accounts, 1):

        embed.add_field(
            name=f"🔹 Account #{i}",
            value=(
                f"📧 Login:\n"
                f"```{acc[1]}```\n"
                f"🔑 Password:\n"
                f"```{acc[2]}```"
            ),
            inline=False
        )

    embed.set_footer(
        text=f"Requested by {user.name}"
    )

    return embed



def stock_embed(fivem, discord_acc, steam):

    embed = discord.Embed(
        title="📦 LIVE ACCOUNT STOCK",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🎮 FiveM",
        value=f"```{fivem} available```",
        inline=True
    )

    embed.add_field(
        name="💬 Discord",
        value=f"```{discord_acc} available```",
        inline=True
    )

    embed.add_field(
        name="🚂 Steam",
        value=f"```{steam} available```",
        inline=True
    )

    embed.set_footer(
        text="Auto updating every 30 seconds"
    )

    return embed
