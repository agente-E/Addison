import discord
from discord.ext import commands
from discord import app_commands
from cogs.utils.channels.setup_combat import SetupCombat


class TestUtils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(
        name="testutil",
        description="Prueba una utilidad añadida",
    )
    @app_commands.default_permissions(administrator=True)
    async def test_util(
        self,
        interaction: discord.Interaction,
        user1: discord.User,
        user2: discord.User,
    ):
        create_cog: SetupCombat | None = self.bot.get_cog("SetupCombat")

        if create_cog is None:
            await interaction.response.send_message(
                "SetupCombat cog no está cargado.", ephemeral=True
            )
            return

        await create_cog.setup_combat(user1, user2)

        if await create_cog.setup_combat(user1, user2):
            await interaction.response.send_message(
                "Canales creados correctamente.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Error al crear los canales", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(TestUtils(bot))
