import asyncio
import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import logging

from discord.ext import commands, tasks
from discord import PCMAudio, VoiceClient, VoiceChannel

CDT = ZoneInfo('America/Chicago')
CHANNEL = 333436482498985984  # Balls
SOUND = Path(__file__).parent / 'sounds' / 'its3am.wav'
TIME = datetime.time(hour=3, minute=0, second=0, tzinfo=CDT)

logger = logging.getLogger('discord').getChild(__name__)


class Wotn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.play_at_time.start()

    @tasks.loop(time=TIME)
    async def play_at_time(self):
        voice_channel: VoiceChannel = await self.bot.fetch_channel(CHANNEL)
        logger.info(f'Connecting to voice channel: {voice_channel}')
        logger.info(f'Channel type: {voice_channel.type}')
        voice_client: VoiceClient = await voice_channel.connect()

        await self.play_sound_in_channel(SOUND, voice_client)

    @commands.command()
    async def play(self, ctx: commands.Context):
        channel = ctx.author.voice.channel

        if channel:
            voice_client = await channel.connect()
            logger.info(f'Joined voice channel: {channel}')

            if voice_client and voice_client.is_connected():
                if voice_client.is_playing():
                    voice_client.stop()

                await self.play_sound_in_channel(SOUND, voice_client)
                logger.info(f'Playing {SOUND}')
            else:
                logger.info('I am not connected to a voice channel.')
        else:
            logger.info('You are not in a voice channel.')

    async def play_sound_in_channel(self, sound: Path, voice_client: VoiceClient = None):
        if voice_client is None:
            voice_channel: VoiceChannel = await self.bot.fetch_channel(CHANNEL)
            voice_client: VoiceClient = await voice_channel.connect()
            logger.info(f'Connecting to voice channel: {voice_channel}')
            logger.info(f'Channel type: {voice_channel.type}')

        def disconnect_after_playing(error):
            coro = voice_client.disconnect()
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                logger.error(f'Error disconnecting from voice channel: {e}')
                pass

        if voice_client and voice_client.is_connected():
            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(PCMAudio(sound.open('rb')), after=disconnect_after_playing)
