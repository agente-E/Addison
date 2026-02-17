import discord
from discord.ext import commands


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    # For every message sent to the bot or in the server
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Stops if the message is from the bot
        if message.author.bot:
            return

        await self.bot.process_commands(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessage(bot))
