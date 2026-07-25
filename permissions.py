import discord

async def is_admin(interaction):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Šią komandą gali naudoti tik administratoriai.",
            ephemeral=True
        )
        return False

    return True
