import discord


def account_embed(type, accounts, user):

    embed = discord.Embed(
        title=f"🟢 {type.upper()} paskyros",
        description="Paskyros išduotos sėkmingai.",
        color=discord.Color.green()
    )


    for i, acc in enumerate(accounts, 1):

        embed.add_field(
            name=f"🔹 Paskyra #{i}",
            value=(
                f"📧 Login:\n"
                f"`{acc[1]}`\n\n"
                f"🔑 Password:\n"
                f"`{acc[2]}`"
            ),
            inline=False
        )


    embed.set_footer(
        text=f"Pasiėmė: {user}"
    )

    return embed
