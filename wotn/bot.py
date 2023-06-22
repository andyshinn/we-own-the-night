import os

from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv

from wotn.cogs.wotn import Wotn

load_dotenv()


class WotnBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_connect(self):
        await bot.add_cog(Wotn(bot))


bot = WotnBot(commands.when_mentioned, intents=Intents.default())
bot.run(token=os.getenv("DISCORD_TOKEN"))
