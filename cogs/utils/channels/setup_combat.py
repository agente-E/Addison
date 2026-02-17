import discord
from discord.ext import commands


class SetupCombat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.__guild_id: int = self.bot.config.get("guildid")

    async def setup_combat(self, user1: discord.User, user2: discord.User) -> bool:

        if user1 == user2:
            return False

        guild: discord.Guild | None = self.bot.get_guild(self.__guild_id)

        if guild is None:
            raise ValueError("Can't find guild.")

        member1: discord.Member = guild.get_member(user1.id)
        member2: discord.Member = guild.get_member(user2.id)

        if not member1:
            raise ValueError(f"User {user1.name} is not in the server.")
            return False

        if not member2:
            raise ValueError(f"User {user2.name} is not in the server.")
            return False

        category_name: str = f"combate-{member1.name}-{member2.name}".lower().replace(
            " ", "-"
        )

        inversed_category_name: str = (
            f"combate-{member2.name}-{member1.name}".lower().replace(" ", "-")
        )

        # Evade duplicates
        if discord.utils.get(guild.categories, name=category_name) or discord.utils.get(
            guild.categories, name=inversed_category_name
        ):
            return False

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member1: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_message_history=True
            ),
            member2: discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(view_channel=True),
        }

        print("Arrived here anyways")

        category: discord.CategoryChannel = await guild.create_category(
            name=category_name, overwrites=overwrites, reason="Creación de combate"
        )

        await guild.create_text_channel(name="arena-chat", category=category)
        await guild.create_voice_channel(name="arena-vc", category=category)


async def setup(bot: commands.Bot):
    await bot.add_cog(SetupCombat(bot))
